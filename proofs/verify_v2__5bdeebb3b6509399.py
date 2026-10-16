#!/usr/bin/env python3
"""Agent #103 v2: isolated, resumable Lean 4.19 build of the scalar finite certificate.

Identical to the original verify.py except: (1) JobData0..15 sources come from
this directory's generated/ (chunked v2 tables, same values), (2) reports are
written here, not into the original package, (3) independent modules compile
concurrently on up to WORKERS processes. Provenance, reuse and audit logic
is unchanged.

Only records containing the exact source, object, log, compiler/settings,
and direct-import fingerprints may resume. Project dependencies are validated
in topological order; no development objects or legacy manifests are imported.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
CONTRIBUTIONS = REPO / "proofs/contributions"
ORIGINAL = CONTRIBUTIONS / "2026-10-15-scalar-finite-certificate-formal"
WORKERS = 2
SCHEMA = 1
FLAGS = ["-j1", "-DElab.async=false"]
ALLOWED_AXIOMS = {"propext", "Quot.sound", "Classical.choice"}
BASE_SHA256 = "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57"


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def file_hash(path):
    return digest(Path(path).read_bytes())


def atomic_json(path, payload):
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def uncomment(source):
    depth = position = 0
    result = []
    while position < len(source):
        if source.startswith("/-", position):
            depth += 1
            position += 2
        elif depth and source.startswith("-/", position):
            depth -= 1
            position += 2
        elif depth:
            position += 1
        elif source.startswith("--", position):
            end = source.find("\n", position)
            position = len(source) if end < 0 else end
        else:
            result.append(source[position])
            position += 1
    assert depth == 0, "Unterminated source comment"
    return "".join(result)


def module_sources():
    paths = {"LychrelDigitSums": REPO / "proofs/research/continuation/LychrelDigitSums.lean"}
    groups = {
        "2026-10-15-scalar-clock-formal": ["ScalarClock", "ActualScalar", "ScalarOrbit", "WidthOne"],
        "2026-10-14-prefix-extension-formal": ["PrefixExtension"],
        "2026-10-15-actual-prefix-lift-formal": ["ActualPrefixLift", "ScalarRoot"],
        "2026-10-14-scc-bound-formal": ["CondensationBound"],
        "2026-10-14-component-hierarchy-formal": ["ComponentHierarchy"],
        "2026-10-15-bounded-prefix-lift-formal": ["BoundedPrefixLift", "ActualJobFamily"],
        "2026-10-15-scalar-period-composition": ["ScalarPeriods", "RootBridge", "ScalarBound"],
    }
    for directory, names in groups.items():
        paths.update({name: CONTRIBUTIONS / directory / (name + ".lean") for name in names})
    paths.update({name: ORIGINAL / (name + ".lean") for name in
                  ["FiniteGraph", "RankRows", "RangeChecks", "ScalarHierarchyData", "ScalarHierarchy"]})
    paths["JobCatalog"] = ORIGINAL / "generated/JobCatalog.lean"
    for i in range(16):
        paths[f"JobData{i}"] = HERE / "generated" / f"JobData{i}.lean"
        paths[f"JobChecks{i}"] = ORIGINAL / "generated" / f"JobChecks{i}.lean"
    return paths


def source_closure(paths, targets):
    blobs, imports, order, visiting = {}, {}, [], set()

    def visit(name):
        if name in order:
            return
        assert name not in visiting, f"Cyclic project imports: {name}"
        visiting.add(name)
        blob = paths[name].read_bytes()
        code = uncomment(blob.decode())
        if name == "LychrelDigitSums":
            assert digest(blob) == BASE_SHA256, "Base source does not match pinned revision"
        else:
            assert not re.search(r"\b(?:sorry|admit|native_decide|axiom|sorryAx)\b", code), name
        direct = [token for line in re.findall(r"^import\s+([^\n]+)", code, re.M)
                  for token in line.split()]
        assert len(direct) == len(set(direct)), f"Duplicate import in {name}"
        assert set(direct) <= set(paths) | {"Std", "Init"}, (name, direct)
        imports[name] = [dep for dep in direct if dep in paths]
        blobs[name] = blob
        for dep in imports[name]:
            visit(dep)
        visiting.remove(name)
        order.append(name)

    for target in targets:
        visit(target)
    return blobs, imports, order


def dependency_fingerprints(build, dependencies):
    return {dep: {"source_sha256": file_hash(build / (dep + ".lean")),
                  "olean_sha256": file_hash(build / (dep + ".olean"))}
            for dep in dependencies}


def reusable(record, name, blob, dependencies, compiler_digest, build):
    """Conservative pure resume predicate; missing legacy fields cannot pass."""
    if not isinstance(record, dict):
        return False
    required = {
        "status": "PASS", "exit_code": 0, "module": name,
        "source_sha256": digest(blob), "compiler_identity_sha256": compiler_digest,
        "dependency_fingerprints": dependencies, "dependencies_unchanged": True,
        "source_unchanged": True,
    }
    if any(record.get(key) != value for key, value in required.items()):
        return False
    try:
        return (file_hash(build / (name + ".lean")) == digest(blob)
                and file_hash(build / (name + ".olean")) == record["olean_sha256"]
                and file_hash(build / "logs" / (name + ".log")) == record["log_sha256"])
    except (OSError, KeyError):
        return False


def theorem_names(blobs):
    names = []
    for module, blob in blobs.items():
        if module == "LychrelDigitSums":
            continue
        code = uncomment(blob.decode())
        namespaces = re.findall(r"^namespace\s+(\S+)\s*$", code, re.M)
        assert len(namespaces) == 1, (module, namespaces)
        names += [namespaces[0] + "." + name for name in
                  re.findall(r"^theorem\s+(\w+)", code, re.M)]
    assert len(names) == len(set(names)), "Duplicate public theorem name"
    return names


def compiler_identity(lean, environment):
    version = subprocess.run([str(lean), "--version"], env=environment,
                             check=True, capture_output=True, text=True).stdout.strip()
    assert "version 4.19.0," in version, version
    preloads = {}
    for library in re.split(r"[:\s]+", environment.get("LD_PRELOAD", "")):
        if library:
            path = Path(library).resolve(strict=True)
            preloads[str(path)] = file_hash(path)
    return dict(version=version, executable=str(lean), executable_sha256=file_hash(lean),
                flags=FLAGS, preloaded_library_sha256=preloads)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--build-dir", required=True, type=Path)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--stage", choices=["data", "checks", "final", "all"], default="all")
    args = parser.parse_args()
    lean, build = args.lean.resolve(strict=True), args.build_dir.resolve()
    if not args.resume and build.exists():
        assert not any(build.iterdir()), "Fresh builds require an empty build directory"
    build.mkdir(parents=True, exist_ok=True)
    (build / "logs").mkdir(exist_ok=True)
    manifest_path = build / "manifest.json"
    assert not args.resume or manifest_path.exists(), "--resume requires this checker's existing manifest"
    assert args.resume or not manifest_path.exists(), "Existing manifest requires --resume or a new build directory"
    environment = dict(os.environ, LEAN_PATH=str(build))
    environment.pop("LEAN_SRC_PATH", None)
    environment.pop("LEAN_SYSROOT", None)
    identity = compiler_identity(lean, environment)
    identity_digest = digest(json.dumps(identity, sort_keys=True).encode())
    checker_digest = file_hash(__file__)
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        assert manifest.get("schema") == SCHEMA, "Legacy manifest is not resumable"
        assert manifest.get("compiler_identity") == identity, "Compiler/settings changed; use a fresh build directory"
    else:
        manifest = dict(schema=SCHEMA, compiler_identity=identity, modules={})
    manifest.update(status="RUNNING", requested_stage=args.stage)
    atomic_json(manifest_path, manifest)
    (HERE / "verification.json").unlink(missing_ok=True)
    paths = module_sources()
    assert all(path.stem in set(paths) | {"AllAxioms"} for path in build.glob("*.olean")), \
        "Foreign compiled module in isolated build directory"
    targets = [f"JobData{i}" for i in range(16)] + ["ScalarHierarchyData"]
    if args.stage != "data":
        targets += [f"JobChecks{i}" for i in range(16)]
    if args.stage in ("final", "all"):
        targets += ["ScalarBound"]
    blobs, imports, order = source_closure(paths, targets)
    expected_axioms = []
    if args.stage in ("final", "all"):
        expected_axioms = theorem_names(blobs)
        audit = "\n".join("import " + name for name in targets)
        audit += "\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n"
        audit += "\n".join("#print axioms " + name for name in expected_axioms) + "\n"
        (HERE / "AllAxioms.lean").write_text(audit)
        blobs["AllAxioms"] = audit.encode()
        imports["AllAxioms"] = targets
        order.append("AllAxioms")
    # All snapshots are copied before compilation. Only this directory is in
    # LEAN_PATH; old objects cannot enter through another project search path.
    for name, blob in blobs.items():
        (build / (name + ".lean")).write_bytes(blob)
    validated, reused = set(), []

    def compile_one(name, before):
        (build / (name + ".olean")).unlink(missing_ok=True)
        log_path = build / "logs" / (name + ".log")
        command = [str(lean), *FLAGS, "-o", name + ".olean", name + ".lean"]
        started = time.monotonic()
        print(json.dumps(dict(module=name, status="COMPILING")), flush=True)
        with log_path.open("wb") as log:
            proc = subprocess.run(command, cwd=build, env=environment, stdout=log, stderr=subprocess.STDOUT)
        return proc.returncode, round(time.monotonic() - started, 3), command, log_path

    def finish(name, before, result):
        returncode, seconds, command, log_path = result
        after = dependency_fingerprints(build, imports[name])
        source_unchanged = (build / (name + ".lean")).read_bytes() == blobs[name]
        if name in paths:
            source_unchanged = source_unchanged and paths[name].read_bytes() == blobs[name]
        output = log_path.read_text()
        accepted = (returncode == 0 and before == after and source_unchanged
                    and "declaration uses 'sorry'" not in output
                    and (build / (name + ".olean")).is_file())
        record = dict(module=name, status="PASS" if accepted else "FAIL",
                      exit_code=returncode, seconds=seconds,
                      source_sha256=digest(blobs[name]), compiler_identity_sha256=identity_digest,
                      dependency_fingerprints=before, dependencies_unchanged=before == after,
                      source_unchanged=source_unchanged, command=command,
                      log_sha256=file_hash(log_path))
        if (build / (name + ".olean")).is_file():
            record["olean_sha256"] = file_hash(build / (name + ".olean"))
        manifest["modules"][name] = record
        manifest["status"] = "RUNNING" if accepted else "FAIL"
        atomic_json(manifest_path, manifest)
        print(json.dumps(record), flush=True)
        assert accepted, f"Build failed: {name}; inspect {log_path}"
        validated.add(name)

    pending = list(order)
    running = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        while pending or running:
            progressed = True
            while progressed and len(running) < WORKERS:
                progressed = False
                for name in pending:
                    if set(imports[name]) <= validated:
                        pending.remove(name)
                        before = dependency_fingerprints(build, imports[name])
                        old = manifest["modules"].get(name)
                        if args.resume and reusable(old, name, blobs[name], before, identity_digest, build):
                            reused.append(name)
                            validated.add(name)
                            print(json.dumps(dict(module=name, status="REUSED")), flush=True)
                        else:
                            running[pool.submit(compile_one, name, before)] = (name, before)
                        progressed = True
                        break
            if not running:
                assert not pending, f"Unvalidated dependency: {pending}"
                break
            done, _ = wait(list(running), return_when=FIRST_COMPLETED)
            for future in done:
                name, before = running.pop(future)
                finish(name, before, future.result())
    # Recheck every successful record, including reused objects and logs, before
    # accepting this stage or collecting evidence. Never overwrite fingerprints.
    for name in order:
        if name in paths:
            assert paths[name].read_bytes() == blobs[name], f"Repository source changed: {name}"
        current = dependency_fingerprints(build, imports[name])
        assert reusable(manifest["modules"][name], name, blobs[name], current,
                        identity_digest, build), f"Final provenance mismatch: {name}"
    assert file_hash(__file__) == checker_digest, "Checker changed during build"
    assert compiler_identity(lean, environment) == identity, "Compiler identity changed during build"
    axioms = {}
    if expected_axioms:
        output = (build / "logs/AllAxioms.log").read_text()
        for match in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", output, re.S):
            name = match.group(1)
            assert name not in axioms, f"Duplicate axiom record: {name}"
            used = sorted({a.strip() for a in (match.group(2) or "").split(",") if a.strip()})
            assert set(used) <= ALLOWED_AXIOMS, (name, used)
            axioms[name] = used
        assert set(axioms) == set(expected_axioms), "Incomplete or extra axiom audit"
    manifest["status"] = "PASS" if expected_axioms else args.stage.upper() + "_PASS"
    manifest["validated_order"] = order
    manifest["last_run_reused"] = reused
    manifest["checker_sha256"] = checker_digest
    atomic_json(manifest_path, manifest)
    if expected_axioms:
        report = dict(status="PASS", compiler_identity=identity, checker_sha256=checker_digest,
                      manifest_schema=SCHEMA, modules=[manifest["modules"][name] for name in order],
                      source_sha256={str(paths[name].relative_to(REPO)): digest(blob)
                                     for name, blob in blobs.items() if name in paths},
                      all_axioms_source_sha256=digest(blobs["AllAxioms"]),
                      theorem_count=len(axioms), theorem_axioms=axioms,
                      axiom_union=sorted({a for used in axioms.values() for a in used}),
                      isolated_project_import_path=True, imported_development_objects=False,
                      all_sources_objects_logs_dependencies_revalidated=True,
                      resumed_modules=reused,
                      table_representation="Agent #103 v2 chunked JobData tables (generate_scalar_data_v2.py); all other sources unchanged from the original package",
                      scope="Kernel-checked scalar finite hierarchy and actual-orbit94/98 composition; no eventual-palindrome or P196 claim.")
        atomic_json(HERE / "verification.json", report)
        with (HERE / "compile.log").open("w") as output:
            output.write(json.dumps(identity, sort_keys=True) + "\n")
            for name in order:
                output.write("\n" + json.dumps(manifest["modules"][name], sort_keys=True) + "\n")
                output.write((build / "logs" / (name + ".log")).read_text())
    print(json.dumps(dict(status=manifest["status"], modules=len(order),
                         reused=len(reused), theorem_count=len(axioms))), flush=True)


if __name__ == "__main__":
    main()
