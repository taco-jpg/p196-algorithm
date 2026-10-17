#!/usr/bin/env python3
"""Rebuild the exact eight-module actual-carry support closure from source.

Adapted from the original spectral carry-charge checker at commit
 e8d706dc8a67248e1531b0b828fbe05ff50052ed, Git blob
 ea730bac77298967a8be4e103b0de5b40cd2a5a8. Its exact source is preserved in
 development/author/checker/provenance/original-check.py.

The output directory must be new. This driver validates the complete explicit
local import graph and source pins, copies all eight sources, and compiles each
with trust zero. It imports no pre-existing project object. The installed Lean
runtime is a pinned external dependency; its executable, shared library, Std
root object, and complete installed object inventory are checked before and
after compilation. Full stdout, stderr, commands, source copies, and failures
are retained. Public and critical prerequisite audits are not a substitute for
the separate independent semantic review and all-origin declaration audit.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import traceback

SOURCE_SPECS = {'LychrelDigitSums': {'path': 'proofs/LychrelDigitSums__0810ace083af80c5.lean',
                      'sha256': 'ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57',
                      'git_blob': '8a865176625283648a8a20dd2411ed77670eb0a2',
                      'bytes': 218799,
                      'imports': ['Std']},
 'IncomingCarrySensitivity': {'path': 'proofs/IncomingCarrySensitivity__5d4952e23e746f6d.lean',
                              'sha256': '52850d75999a8fdad298e2e9da638965472ab6507f88630bf428698576ac631f',
                              'git_blob': '9ccc745471fd509fb68652fef40454478087e92e',
                              'bytes': 12041,
                              'imports': ['LychrelDigitSums']},
 'RawSymmetryObstruction': {'path': 'proofs/RawSymmetryObstruction__5c1be305a04af2b7.lean',
                            'sha256': '922b660e5b3ac42389cd6ea00885075327d4b44fb315b9cc496e1323890e9c87',
                            'git_blob': '9d4250f3e5daa5ff26f097a7e12ce98830dd9e89',
                            'bytes': 23848,
                            'imports': ['IncomingCarrySensitivity']},
 'SpectralWeights': {'path': 'proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472/SpectralWeights.lean',
                     'sha256': '07b3831f17a0d2e43a7e27cfd8a63d364a98ccbbcef87362a20cfbf24fb49db1',
                     'git_blob': '40afa93196976972e5c0f6772a18e50c1e635a3f',
                     'bytes': 4445,
                     'imports': ['Std']},
 'BinaryCode': {'path': 'proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472/BinaryCode.lean',
                'sha256': '8db88d52e00dddbd32610dc09b7f8833f1ec1dc623b82236060b67bd2c9171f9',
                'git_blob': '35ba9bee5afb9bb47f39738e44860a02ea9b2469',
                'bytes': 2655,
                'imports': ['SpectralWeights']},
 'ChargeSymmetry': {'path': 'proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472/ChargeSymmetry.lean',
                    'sha256': '28d11217cf147750ec2d07e64dbc6dabeee7deec7e543987817da611201b60a3',
                    'git_blob': 'f69efd4bc0642759dddf99834d5d093c929761a5',
                    'bytes': 3240,
                    'imports': ['BinaryCode']},
 'SourceFormula': {'path': 'proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472/SourceFormula.lean',
                   'sha256': 'be165a538963922f6096e63934e5f3c1010d760cabc9e08baa96a0bb43c105d8',
                   'git_blob': '1db4a109629abddf355d12e8a14f2cfb0e26a39b',
                   'bytes': 5059,
                   'imports': ['ChargeSymmetry']},
 'ActualCarrySupport': {'path': 'proofs/contributions/agent-15/spectral-carry-support-43cf6e114472/ActualCarrySupport.lean',
                        'sha256': '4c06522efae7aa254b6281003d042e49f6b60162d01d00881d50052c7a73c646',
                        'git_blob': 'c0e5562e1661570546bced3dca82dd4fb459fa5f',
                        'bytes': 10166,
                        'imports': ['SourceFormula', 'RawSymmetryObstruction']}}
MODULES = list(SOURCE_SPECS)
NEW_EXPORTS = ['P196.Agent15.SpectralSupport.outgoing',
 'P196.Agent15.SpectralSupport.actualCharge',
 'P196.Agent15.SpectralSupport.outgoing_length',
 'P196.Agent15.SpectralSupport.outgoing_getElem',
 'P196.Agent15.SpectralSupport.outgoing_getElem?',
 'P196.Agent15.SpectralSupport.outgoing_last',
 'P196.Agent15.SpectralSupport.outgoing_binary',
 'P196.Agent15.SpectralSupport.outgoing_reverse_iff',
 'P196.Agent15.SpectralSupport.actualCharge_zero_iff',
 'P196.Agent15.SpectralSupport.outgoing_reflected_eq_of_nonnine',
 'P196.Agent15.SpectralSupport.actualCharge_nonzero_iff_nine_asymmetry',
 'P196.Agent15.SpectralSupport.actualCharge_zero_of_no_nine',
 'P196.Agent15.SpectralSupport.canonical_actualCharge_zero_iff',
 'P196.Agent15.SpectralSupport.canonical_outgoing_reflected_eq_of_nonnine',
 'P196.Agent15.SpectralSupport.canonical_actualCharge_nonzero_iff_nine_asymmetry',
 'P196.Agent15.SpectralSupport.canonical_actualCharge_zero_of_no_nine',
 'P196.Agent15.SpectralSupport.actualCharge_width_zero',
 'P196.Agent15.SpectralSupport.actualCharge_width_one',
 'P196.Agent15.SpectralSupport.Controls.nine_zero_charge',
 'P196.Agent15.SpectralSupport.Controls.even_overflow_zero_charge',
 'P196.Agent15.SpectralSupport.Controls.odd_free_center',
 'P196.Agent15.SpectralSupport.Controls.odd_nine_asymmetry']
CRITICAL_PREREQUISITES = ['DecimalDigits.Canonical',
 'DecimalDigits.columnSum',
 'DecimalDigits.carry',
 'DecimalDigits.carry_bounded',
 'DecimalDigits.columnSum_bounded',
 'DecimalDigits.columnSum_symmetric',
 'RawSymmetryObstruction.nonnine_binary_div',
 'P196.Agent15.SpectralCarry.Binary',
 'P196.Agent15.SpectralCarry.carryCharge',
 'P196.Agent15.SpectralCarry.carryCharge_zero_iff',
 'P196.Agent15.SpectralCarry.carryCharge_eq_odd_source_sum',
 'P196.Agent15.SpectralCarry.carryCharge_eq_even_source_sum',
 'P196.Agent15.SpectralCarry.oddWeight_superincreasing',
 'P196.Agent15.SpectralCarry.evenWeight_superincreasing',
 'P196.Agent15.SpectralCarry.weighted_injective_binary']
EXPECTED_RUNTIME = {'version': '4.19.0',
 'commit': '6caaee842e94',
 'executable_sha256': '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023',
 'shared_library_sha256': '2ab605c74c78f9ba4431a7b5305a4b28a9071d8a826f223eb14fe5530f78e14d',
 'stdlib_root_sha256': '7d3771da25b893da62564bf8198487ff28f01af5cbd410be88d493a4921b2bb1',
 'runtime_olean_count': 1471,
 'runtime_olean_inventory_sha256': '3006ed0315f417028aac57869ba6a033fa9fb23c75e5795aa3087d9f5e039b32',
 'runtime_olean_inventory_encoding': 'UTF-8 JSON, sort_keys=True, separators=(comma,colon), '
                                     'trailing LF; entries sorted by relative POSIX path and '
                                     'containing path, sha256, bytes.'}
CHECKER_PROVENANCE = {'source_commit': 'e8d706dc8a67248e1531b0b828fbe05ff50052ed',
 'git_blob': 'ea730bac77298967a8be4e103b0de5b40cd2a5a8',
 'sha256': 'f0da79f56ca4c2e24ff90700f3491d4999247f9b88db6cc306074ac84c646ab3',
 'source_path': 'proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472/check.py'}
FLAGS = ["--trust=0", "-j1", "-DElab.async=false"]
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
TOOLCHAIN = "leanprover/lean4:v4.19.0"
TASK = "agent15-spectral-carry-support-43cf6e114472"


class CheckFailure(RuntimeError):
    """A recorded verification gate failed."""


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def blob_digest(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def runtime_fingerprint(lean, inventory_path):
    library = lean.parent.parent / "lib" / "lean"
    inventory = [
        {"path": path.relative_to(library).as_posix(),
         "sha256": digest(path), "bytes": path.stat().st_size}
        for path in sorted(library.rglob("*.olean"))
    ]
    inventory_bytes = (json.dumps(inventory, sort_keys=True,
                                 separators=(",", ":")) + "\n").encode()
    inventory_path.write_bytes(inventory_bytes)
    return {
        "executable_sha256": digest(lean),
        "shared_library_sha256": digest(library / "libleanshared.so"),
        "stdlib_root_sha256": digest(library / "Std.olean"),
        "runtime_olean_count": len(inventory),
        "runtime_olean_inventory_sha256": hashlib.sha256(inventory_bytes).hexdigest(),
    }


def source_imports(text):
    # These exact pinned sources have single-line import commands. Any changed
    # source or unexpected import spelling is rejected before compilation.
    result = []
    for line in text.splitlines():
        match = re.fullmatch(r"import[ \t]+(.+)", line)
        if match:
            modules = match.group(1).split()
            require(all(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", name)
                        for name in modules), "Unexpected import syntax")
            result.extend(modules)
    return result


def actual_public_exports(text):
    # Explicit namespaces and the terminal question mark are retained.
    # Generated declarations are handled by the independent all-origin audit.
    namespaces = []
    exports = []
    for line in text.splitlines():
        match = re.fullmatch(r"namespace[ \t]+([A-Za-z0-9_.]+)", line)
        if match:
            namespaces.append(match.group(1))
            continue
        if re.fullmatch(r"end[ \t]+[A-Za-z0-9_.]+", line):
            require(bool(namespaces), "Unexpected namespace ending")
            namespaces.pop()
            continue
        match = re.match(r"(?:@\[[^\n]*\][ \t]*)?(def|theorem)[ \t]+([A-Za-z0-9_'?]+)", line)
        if match:
            exports.append({"kind": match.group(1),
                            "name": ".".join(namespaces + [match.group(2)])})
    require(not namespaces, "Unclosed source namespace")
    return exports


def verify_graph():
    positions = {module: index for index, module in enumerate(MODULES)}
    external = set()
    for module, spec in SOURCE_SPECS.items():
        for dependency in spec["imports"]:
            if dependency in positions:
                require(positions[dependency] < positions[module],
                        "Local module order is not topological")
            else:
                external.add(dependency)
    require(external == {"Std"}, "Unexpected external import closure")
    reachable = set()

    def visit(module):
        if module in reachable:
            return
        reachable.add(module)
        for dependency in SOURCE_SPECS[module]["imports"]:
            if dependency in SOURCE_SPECS:
                visit(dependency)

    visit("ActualCarrySupport")
    require(reachable == set(MODULES), "Selected closure is not exactly the target closure")
    return {"target": "ActualCarrySupport", "modules": MODULES,
            "edges": {module: spec["imports"] for module, spec in SOURCE_SPECS.items()},
            "external_imports": sorted(external), "complete": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    lean = args.lean.resolve()
    output = args.output.resolve()
    # Existing output is never reused, cleared, or overwritten.
    output.mkdir(parents=True, exist_ok=False)
    source = output / "source"
    logs = output / "logs"
    source.mkdir()
    logs.mkdir()
    package = Path(__file__).resolve().parent
    repo = package.parents[3]
    checker = Path(__file__).resolve()
    manifest_path = package / "BUILD.json"
    toolchain_path = package / "lean-toolchain"
    env = os.environ.copy()
    env["LEAN_PATH"] = str(source)
    env.pop("LEAN_SYSROOT", None)
    records = []
    pins = {}
    receipt = {
        "status": "FAIL", "task_id": TASK, "output": str(output),
        "repository_root": str(repo), "modules": MODULES,
        "flags": FLAGS, "allowed_axioms": sorted(ALLOWED),
        "source_pins": pins, "commands": records,
        "scope": "Fresh selected eight-module source closure, exact public exports, and critical prerequisite audits. Independent semantic review and all-origin audit are separate.",
    }

    def run(name, argv):
        argv = [str(value) for value in argv]
        record = {"name": name, "argv": argv, "cwd": str(source),
                  "LEAN_PATH": str(source), "LEAN_SYSROOT": "unset",
                  "started_utc": datetime.now(timezone.utc).isoformat()}
        records.append(record)
        write_json(logs / (name + ".command.json"), record)
        started = time.monotonic()
        result = subprocess.run(argv, cwd=source, env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (logs / (name + ".stdout")).write_bytes(result.stdout)
        (logs / (name + ".stderr")).write_bytes(result.stderr)
        record.update(exit_code=result.returncode, seconds=time.monotonic() - started)
        write_json(logs / (name + ".result.json"), record)
        write_json(output / "commands.json", records)
        print(json.dumps({"command": name, "exit_code": result.returncode,
                          "seconds": record["seconds"]}), flush=True)
        require(result.returncode == 0, "Lean command failed: " + name)
        return result

    try:
        checker_sha = digest(checker)
        manifest_sha = digest(manifest_path)
        toolchain_sha = digest(toolchain_path)
        receipt["checker_sha256"] = checker_sha
        receipt["build_manifest_sha256"] = manifest_sha
        receipt["lean_toolchain_sha256"] = toolchain_sha
        receipt["checker_provenance"] = CHECKER_PROVENANCE
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for key, expected in {
            "task_id": TASK, "toolchain": TOOLCHAIN, "flags": FLAGS,
            "modules": MODULES, "source_pins": SOURCE_SPECS,
            "new_exports": NEW_EXPORTS,
            "critical_prerequisites": CRITICAL_PREREQUISITES,
            "expected_runtime": EXPECTED_RUNTIME,
            "allowed_axioms": sorted(ALLOWED),
            "external_imports": ["Std"],
            "checker_provenance": CHECKER_PROVENANCE,
        }.items():
            require(manifest.get(key) == expected, "BUILD.json mismatch: " + key)
        require(toolchain_path.read_text(encoding="utf-8") == TOOLCHAIN + "\n",
                "Unexpected lean-toolchain contents")
        graph = verify_graph()
        write_json(output / "import-closure.json", graph)
        for module, spec in SOURCE_SPECS.items():
            original = repo / spec["path"]
            target = source / (module + ".lean")
            data = original.read_bytes()
            target.write_bytes(data)
            actual = {"sha256": digest(target), "git_blob": blob_digest(data),
                      "bytes": len(data), "original_path": str(original),
                      "repository_path": spec["path"],
                      "imports": source_imports(data.decode("utf-8"))}
            pins[module] = actual
            write_json(output / "source-pins.json", pins)
            for key in ["sha256", "git_blob", "bytes", "imports"]:
                require(actual[key] == spec[key], module + " source mismatch: " + key)
        require(not list(source.rglob("*.olean")), "Pre-existing project object found")
        receipt["initial_project_object_count"] = 0
        exports = actual_public_exports((source / "ActualCarrySupport.lean").read_text(encoding="utf-8"))
        require([entry["name"] for entry in exports] == NEW_EXPORTS,
                "ActualCarrySupport public export list differs from the explicit contract")
        require(len(NEW_EXPORTS) == 22 and len(set(NEW_EXPORTS)) == 22,
                "Expected exactly 22 distinct new exports")
        require(not set(NEW_EXPORTS) & set(CRITICAL_PREREQUISITES), "Duplicate audit group member")
        receipt["public_exports"] = exports
        receipt["critical_prerequisites"] = CRITICAL_PREREQUISITES
        write_json(output / "exports.json", exports)
        write_json(output / "critical-prerequisites.json", CRITICAL_PREREQUISITES)
        before = runtime_fingerprint(lean, output / "runtime-before-inventory.json")
        receipt["compiler"] = {"path": str(lean), **before}
        for key, actual in before.items():
            require(actual == EXPECTED_RUNTIME[key], "Runtime pin mismatch: " + key)
        version = run("lean-version", [lean, *FLAGS, "--version"])
        version_text = version.stdout.decode("utf-8", errors="replace")
        receipt["compiler"]["version_output"] = version_text
        require(re.search(r"\bversion 4\.19\.0\b", version_text) is not None,
                "Unexpected Lean version")
        require(EXPECTED_RUNTIME["commit"] in version_text, "Unexpected compiler commit")
        object_pins = {}
        for module in MODULES:
            run(module, [lean, *FLAGS, "-o", module + ".olean", module + ".lean"])
            object_path = source / (module + ".olean")
            require(object_path.is_file(), "Compiler did not produce object: " + module)
            object_pins[module] = {"sha256": digest(object_path),
                                   "bytes": object_path.stat().st_size}
            write_json(output / "built-object-pins.json", object_pins)
        names = NEW_EXPORTS + CRITICAL_PREREQUISITES
        audit = "import ActualCarrySupport\n\n" + "\n".join(
            "#print " + name + "\n#print axioms " + name for name in names
        ) + "\n"
        (source / "PublicAudit.lean").write_text(audit, encoding="utf-8")
        result = run("PublicAudit", [lean, *FLAGS, "PublicAudit.lean"])
        dependencies = []
        for match in re.finditer(r"'([^']+)' (does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])",
                                 result.stdout.decode("utf-8"), re.S):
            axioms = [] if match.group(2).startswith("does not") else [
                value.strip() for value in match.group(3).split(",") if value.strip()]
            dependencies.append({"name": match.group(1), "axioms": axioms,
                                 "group": "new_export" if match.group(1) in NEW_EXPORTS else "critical_prerequisite"})
        write_json(output / "public-and-critical-axioms.json", dependencies)
        require(len(dependencies) == len(names) and
                {entry["name"] for entry in dependencies} == set(names),
                "Missing or duplicate public/prerequisite axiom report")
        require(all(set(entry["axioms"]) <= ALLOWED for entry in dependencies),
                "Disallowed transitive axiom found")
        receipt["audited_declaration_count"] = len(dependencies)
        receipt["new_export_count"] = len(NEW_EXPORTS)
        receipt["critical_prerequisite_count"] = len(CRITICAL_PREREQUISITES)
        receipt["axioms_used"] = sorted({axiom for entry in dependencies for axiom in entry["axioms"]})
        after = runtime_fingerprint(lean, output / "runtime-after-inventory.json")
        receipt["runtime_unchanged"] = after == before
        require(after == before, "Installed compiler or runtime changed during verification")
        unchanged = all(digest(source / (module + ".lean")) == spec["sha256"] and
                        digest(repo / spec["path"]) == spec["sha256"]
                        for module, spec in SOURCE_SPECS.items())
        receipt["source_unchanged"] = unchanged
        require(unchanged, "Original or copied source changed during verification")
        config_unchanged = (digest(checker) == checker_sha and
                            digest(manifest_path) == manifest_sha and
                            digest(toolchain_path) == toolchain_sha)
        receipt["configuration_unchanged"] = config_unchanged
        require(config_unchanged, "Checker configuration changed during verification")
        receipt["status"] = "PASS"
    except Exception as error:
        receipt["error_type"] = type(error).__name__
        receipt["error"] = str(error)
        (logs / "driver-error.txt").write_text(traceback.format_exc(), encoding="utf-8")
    finally:
        write_json(output / "verification.json", receipt)
        write_json(output / "commands.json", records)
        print(json.dumps({"status": receipt["status"], "output": str(output),
                          "commands": len(records),
                          "new_exports": len(NEW_EXPORTS),
                          "critical_prerequisites": len(CRITICAL_PREREQUISITES),
                          "error": receipt.get("error")}), flush=True)
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
