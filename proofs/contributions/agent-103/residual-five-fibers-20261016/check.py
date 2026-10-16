#!/usr/bin/env python3
"""Agent103 residual-five inverse-fiber contribution: exact-source fresh build and full project-module axiom audit.

Usage: python3 check.py --repo /path/to/p196-algorithm --lean /path/to/lean
                       --evidence /new/empty/directory
The supplied Git repository must already contain the pinned source commits.
No source download, source rewrite beyond the recorded import forwarder, or
previously compiled project object is used. All failures retain their evidence.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
NAME = re.compile(r"[A-Za-z_][\w']*(?:\.[A-Za-z_][\w']*)*\Z", re.ASCII)
IDENT = re.compile(r"[A-Za-z_][\w']*(?:\.[A-Za-z_][\w']*)*", re.ASCII)
FORBIDDEN = re.compile(r"(?<![\w'])\b(?:sorry|admit|axiom|native_decide|sorryAx|ofReduceBool|skipKernelTC)\b(?![\w'])")
BASE_ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "TZ": "UTC"}
GIT_ENV = dict(BASE_ENV, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null", GIT_TERMINAL_PROMPT="0")
BUILTIN = {"Std", "Init", "Lean"}
COMPILE_ARGS = ["--trust=0", "-j1", "-DElab.async=false"]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def name_ok(name: str) -> str:
    if not NAME.fullmatch(name):
        raise ValueError("Unsupported module name: " + name)
    return name


def relative(value: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(p in {"..", ".git"} for p in path.parts) or "\\" in value:
        raise ValueError("Unsafe relative source path: " + value)
    return str(path)


def code_only(text: str) -> str:
    """Nested-comment/string mask, adapted from the inspected original checkers."""
    out, i, depth, string = [], 0, 0, False
    while i < len(text):
        pair = text[i:i + 2]
        if depth:
            if pair == "/-":
                depth += 1; out.extend("  "); i += 2
            elif pair == "-/":
                depth -= 1; out.extend("  "); i += 2
            else:
                out.append("\n" if text[i] == "\n" else " "); i += 1
        elif string:
            if text[i] == "\\":
                out.extend("  "); i += 2
            else:
                string = text[i] != '"'
                out.append("\n" if text[i] == "\n" else " "); i += 1
        elif pair == "/-":
            depth = 1; out.extend("  "); i += 2
        elif pair == "--":
            end = text.find("\n", i)
            end = len(text) if end < 0 else end
            out.extend(" " * (end - i)); i = end
        elif text[i] == '"':
            string = True; out.append(" "); i += 1
        else:
            out.append(text[i]); i += 1
    if depth or string:
        raise ValueError("Unterminated Lean comment/string")
    return "".join(out)


def imports_of(data: bytes) -> list[str]:
    """Lean 4.19 header: optional prelude, then one identifier per import."""
    text = code_only(data.decode("utf-8"))
    hit = FORBIDDEN.search(text)
    if hit:
        raise ValueError("Forbidden source token: " + hit.group())
    pos, deps = 0, []
    def skip(p):
        while p < len(text) and text[p].isspace():
            p += 1
        return p
    def keyword(word, p):
        return re.match(re.escape(word) + r"(?![\w'.])", text[p:]) is not None
    pos = skip(pos)
    if keyword("prelude", pos):
        pos = skip(pos + len("prelude"))
    while keyword("import", pos):
        pos += len("import")
        if pos >= len(text) or not text[pos].isspace():
            raise ValueError("Unsupported import syntax")
        pos = skip(pos)
        if keyword("runtime", pos):
            raise ValueError("Runtime imports are not part of this source manifest")
        match = IDENT.match(text, pos)
        if not match:
            raise ValueError("Unsupported imported module identifier")
        deps.append(name_ok(match.group()))
        pos = match.end()
        if pos < len(text) and not text[pos].isspace():
            raise ValueError("Unsupported module identifier suffix")
        pos = skip(pos)
    return deps


def audit_source(modules: list[str]) -> str:
    """Discover every theorem constant by compiled module origin, then #print axioms."""
    return (
        "\n".join("import " + name_ok(m) for m in modules) +
        "\nimport Lean\nopen Lean Elab Command\n"
        "set_option maxRecDepth 100000\nset_option maxHeartbeats 0\n"
        "run_cmd do\n  let env ← getEnv\n"
        "  let selected : List String := " + json.dumps(modules) + "\n"
        "  let mut count := 0\n"
        "  for (name, info) in env.constants.toList do\n"
        "    if let some idx := env.getModuleIdxFor? name then\n"
        "      let mod := env.allImportedModuleNames[idx.toNat]!\n"
        "      if selected.contains mod.toString then\n"
        "        match info with\n"
        "        | .axiomInfo v =>\n"
        "          if v.isUnsafe then logInfo m!\"UNSAFE_IMPL {mod} {name}\"\n"
        "          else throwError m!\"CUSTOM_AXIOM {mod} {name}\"\n"
        "        | .thmInfo _ =>\n"
        "          count := count + 1\n"
        "          logInfo m!\"AUDIT_THEOREM {mod} {name}\"\n"
        "          elabCommand (← " + chr(96) + "(command| #print axioms $(mkIdent name)))\n"
        "        | _ => pure ()\n"
        "  logInfo m!\"AUDIT_COMPLETE {count}\"\n"
    )


def parse_audit(text: str, modules: list[str]) -> dict:
    inventory = re.findall(r"^AUDIT_THEOREM (\S+) ([^\n]+)$", text, re.M)
    completion = re.findall(r"^AUDIT_COMPLETE ([0-9]+)$", text, re.M)
    names = [n for _, n in inventory]
    if not inventory or len(set(names)) != len(names) or len(completion) != 1 or int(completion[0]) != len(inventory):
        raise ValueError("Incomplete, empty, or duplicate module-origin theorem inventory")
    if any(m not in modules for m, _ in inventory):
        raise ValueError("Unexpected module in theorem audit")
    entries = [(n, []) for n in re.findall(r"^'([^\n]+)' does not depend on any axioms$", text, re.M)]
    entries += [(n, sorted(a.strip() for a in values.split(",") if a.strip()))
                for n, values in re.findall(r"^'([^\n]+)' depends on axioms:\s*\[([^\]]*)\]$", text, re.M)]
    if Counter(n for n, _ in entries) != Counter(names):
        raise ValueError("Each discovered theorem must have exactly one #print axioms result")
    axioms = dict(entries)
    for name, used in entries:
        if not set(used) <= ALLOWED:
            raise ValueError("Disallowed axioms for " + name + ": " + repr(used))
    by_module = {m: 0 for m in modules}
    for m, _ in inventory:
        by_module[m] += 1
    return {
        "theorem_count": len(inventory), "module_theorem_counts": by_module,
        "axiom_union": sorted(set().union(*(set(a) for _, a in entries))),
        "unsafe_implementation_constants": re.findall(r"^UNSAFE_IMPL (\S+) ([^\n]+)$", text, re.M),
        "theorems": {n: {"module": m, "axioms": axioms[n]} for m, n in inventory},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, required=True, help="Git object repository containing all pinned commits")
    ap.add_argument("--lean", type=Path, required=True)
    ap.add_argument("--evidence", type=Path, required=True, help="Must not already exist")
    ap.add_argument("--manifest", type=Path, default=HERE / "SOURCES.json")
    ap.add_argument("--module", action="append", default=[], help="Select frozen new modules; include their local module imports (default: all)")
    ap.add_argument("--timeout-seconds", type=int, default=1800)
    args = ap.parse_args()
    repo, lean, evidence = args.repo.resolve(), args.lean.resolve(), args.evidence.resolve()
    if args.timeout_seconds <= 0:
        ap.error("--timeout-seconds must be positive")
    evidence.mkdir(parents=True, exist_ok=False)
    originals = evidence / "originals"; originals.mkdir()
    snapshot = evidence / "snapshot"; snapshot.mkdir()
    logs = evidence / "logs"; logs.mkdir()
    report = {"status": "IN_PROGRESS", "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "fresh_project_snapshot": True, "repository_wide_pass": False, "sources": {}, "commands": [],
              "scope": "Exact contribution closure build and transitive axiom facts; no independent semantic proof claim."}
    def save():
        (evidence / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    def git(*argv):
        p = subprocess.run(["git", "-C", str(repo), *argv], env=GIT_ENV, capture_output=True)
        if p.returncode:
            raise RuntimeError("Pinned Git source unavailable; fetch the commits listed in SOURCES.json into --repo first. " +
                               p.stderr.decode("utf-8", "replace"))
        return p.stdout
    env = dict(BASE_ENV, LEAN_PATH=str(snapshot))
    def run(label, command):
        path = logs / (label.replace(".", "_") + ".log")
        started = time.monotonic()
        with path.open("wb") as stream:
            try:
                code = subprocess.run(command, cwd=snapshot, env=env, stdout=stream, stderr=subprocess.STDOUT,
                                      timeout=args.timeout_seconds).returncode
            except subprocess.TimeoutExpired:
                code = 124
        report["commands"].append({"label": label, "argv": command, "cwd": str(snapshot), "environment": env,
                                   "exit_code": code, "seconds": round(time.monotonic() - started, 6),
                                   "log": str(path.relative_to(evidence)), "log_sha256": file_sha(path)})
        save()
        print(label + ": exit=" + str(code), flush=True)
        if code:
            raise RuntimeError(label + " failed; see " + str(path))
        return path.read_text()
    try:
        manifest_bytes = args.manifest.read_bytes()
        manifest = json.loads(manifest_bytes)
        if manifest["schema_version"] != 1 or set(manifest["toolchain"]["allowed_axioms"]) != ALLOWED:
            raise ValueError("Unexpected source-manifest schema or axiom policy")
        if manifest["toolchain"]["arguments"] != COMPILE_ARGS:
            raise ValueError("The source manifest must require the exact trust-zero compiler arguments")
        report.update(manifest_sha256=sha(manifest_bytes), driver_sha256=file_sha(Path(__file__)),
                      git_object_repository=str(repo), git_object_repository_head=git("rev-parse", "HEAD").decode().strip())
        selected = args.module or list(manifest["new_modules"])
        if not selected or len(set(selected)) != len(selected) or set(selected) - manifest["new_modules"].keys():
            raise ValueError("Select a nonempty, nonrepeated set of frozen contribution modules")
        records = dict(manifest["dependencies"])
        for name in selected:
            rec = manifest["new_modules"][name]
            if not rec.get("sha256") or rec.get("imports") is None:
                raise ValueError("New source has not yet been frozen in the manifest: " + name)
            records[name] = rec
        raw, compiled, source_paths = {}, {}, {}
        for name, rec in records.items():
            name_ok(name)
            if name in manifest["dependencies"]:
                commit, path = rec["commit"], relative(rec["path"])
                if not re.fullmatch(r"[0-9a-f]{40}", commit) or not re.fullmatch(r"[0-9a-f]{40}", rec["git_blob"]):
                    raise ValueError("Invalid immutable Git source identifier")
                data = git("cat-file", "blob", commit + ":" + path)
                oid = git("rev-parse", commit + ":" + path).decode().strip()
                if oid != rec["git_blob"] or git_blob(data) != oid or sha(data) != rec["sha256"]:
                    raise ValueError("Dependency commit/path/blob/SHA pin mismatch: " + name)
                origin = {"kind": "pinned_git_source", "commit": commit, "original_path": path, "git_blob": oid}
                if imports_of(data) != rec["original_imports"]:
                    raise ValueError("Original dependency imports differ from manifest: " + name)
            else:
                path = args.manifest.resolve().parent / relative(rec["path"])
                if path.is_symlink() or not path.resolve().is_relative_to(args.manifest.resolve().parent):
                    raise ValueError("Unsafe contribution source path: " + str(path))
                data = path.read_bytes()
                if sha(data) != rec["sha256"]:
                    raise ValueError("Frozen new-source SHA mismatch: " + name)
                source_paths[name] = path
                origin = {"kind": "frozen_contribution_source", "path": rec["path"], "git_blob_of_bytes": git_blob(data)}
            raw[name] = data
            (originals / (name.replace(".", "_") + ".lean")).write_bytes(data)
            report["sources"][name] = dict(origin, original_sha256=sha(data), original_bytes=len(data))
        for name, rec in records.items():
            data = raw[name]
            if rec.get("adapter"):
                adapter = rec["adapter"]
                if adapter["kind"] != "verified_embedded_foundation_import_forwarder":
                    raise ValueError("Unsupported source adapter")
                container = raw[adapter["container_module"]]
                excluded = adapter["excluded_exact_prefix_utf8"].encode()
                if not data.startswith(excluded) or not container.startswith(excluded):
                    raise ValueError("Foundation import header differs")
                body = data[len(excluded):]
                offset = container.find(body)
                if offset < 0 or container.find(body, offset + 1) >= 0:
                    raise ValueError("Original foundation body is not uniquely byte-contained")
                if len(body.splitlines(keepends=True)) != adapter["body_line_count"] or container[:offset].count(b"\n") + 1 != adapter["container_start_line_1_based"]:
                    raise ValueError("Foundation containment location differs from the approved adapter")
                data = adapter["exact_compiled_source_utf8"].encode()
                if data != b"import LychrelDigitSums\n" or sha(data) != adapter["compiled_sha256"]:
                    raise ValueError("Import forwarder differs from the approved exact bytes")
                report["sources"][name]["adapter"] = dict(adapter, body_sha256=sha(body), body_bytes=len(body),
                                                         container_start_byte_0_based=offset, complete_body_byte_identical=True)
            deps = imports_of(data)
            if deps != rec["imports"]:
                raise ValueError("Compiled-source import manifest mismatch: " + name)
            compiled[name] = data
            report["sources"][name].update(compiled_sha256=sha(data), imports=deps, origin_group="new" if name in selected else "dependency")
        order, active, done = [], [], set()
        def visit(name):
            if name in done:
                return
            if name in active:
                raise ValueError("Import cycle: " + " -> ".join(active + [name]))
            if name not in records:
                if name.split(".")[0] not in BUILTIN:
                    raise ValueError("Unregistered import: " + name)
                return
            active.append(name)
            for dep in records[name]["imports"]:
                visit(dep)
            active.pop(); done.add(name); order.append(name)
        for name in selected:
            visit(name)
        report.update(selected_new_modules=selected, build_order=order, module_count=len(order),
                      dependency_modules=[m for m in order if m not in selected],
                      unused_manifest_dependencies=sorted(set(manifest["dependencies"]) - done))
        version = run("version", [str(lean), "--version"]).strip()
        if not re.search(r"version 4\.19\.0, .*commit 6caaee842e94, Release", version):
            raise ValueError("Incorrect Lean release/commit: " + version)
        runtime = Path(run("prefix", [str(lean), "--print-prefix"]).strip()).resolve()
        runtime_files = {str(p): file_sha(p) for p in [lean, runtime / "bin/lean", *sorted((runtime / "lib/lean").glob("*.so"))]}
        report["lean"] = {"version": version, "path": str(lean), "runtime_prefix": str(runtime), "files_sha256": runtime_files}
        for name in order:
            for dep in records[name]["imports"]:
                if dep not in records and not (runtime / "lib/lean" / (dep.replace(".", "/") + ".olean")).is_file():
                    raise ValueError("Unavailable toolchain import: " + dep)
            dest = snapshot / (name.replace(".", "/") + ".lean")
            dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(compiled[name])
        save()
        for name in order:
            relative_name = name.replace(".", "/")
            run(name, [str(lean), *COMPILE_ARGS, "-o", relative_name + ".olean", relative_name + ".lean"])
            report["sources"][name]["object_sha256"] = file_sha(snapshot / (relative_name + ".olean"))
            save()
        audit = snapshot / "AuditAllContributionModules.lean"
        audit.write_text(audit_source(order))
        report["audit_source_sha256"] = file_sha(audit)
        result = parse_audit(run("AuditAllContributionModules", [str(lean), *COMPILE_ARGS, audit.name]), order)
        report.update(result)
        report["new_theorem_count"] = sum(result["module_theorem_counts"][m] for m in selected)
        report["dependency_theorem_count"] = result["theorem_count"] - report["new_theorem_count"]
        for name in order:
            if (snapshot / (name.replace(".", "/") + ".lean")).read_bytes() != compiled[name]:
                raise ValueError("Build snapshot changed: " + name)
        for name, path in source_paths.items():
            if path.read_bytes() != raw[name]:
                raise ValueError("Contribution source changed during the build: " + name)
        if args.manifest.read_bytes() != manifest_bytes:
            raise ValueError("Source manifest changed during the build")
        if any(file_sha(Path(p)) != pin for p, pin in runtime_files.items()):
            raise ValueError("Compiler/runtime files changed during the build")
        report.update(status="PASS", all_source_hashes_unchanged=True)
        print(f"PASS: {len(order)} fresh modules; {report['new_theorem_count']} new-module and "
              f"{report['dependency_theorem_count']} dependency theorem constants individually audited", flush=True)
        return 0
    except Exception as error:
        report.update(status="FAIL", failure=str(error))
        (evidence / "failure.txt").write_text(traceback.format_exc())
        print("FAIL: " + str(error), file=sys.stderr, flush=True)
        return 1
    finally:
        report["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        save()
        files = {str(p.relative_to(evidence)): {"bytes": p.stat().st_size, "sha256": file_sha(p)}
                 for p in sorted(evidence.rglob("*")) if p.is_file() and p.suffix != ".olean" and p.name != "FILES.json"}
        (evidence / "FILES.json").write_text(json.dumps(files, indent=2) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
