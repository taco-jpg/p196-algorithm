#!/usr/bin/env python3
"""Agent #104: rebuild the 13-module generic prefix dependency closure.

Every source is read from an immutable Git commit and checked against both
its pinned SHA256 and actual Git blob. No source is rewritten. Each invocation
requires a previously absent build directory and a new logs directory.
The module-origin theorem audit follows the inspected repository verifier
proofs/verify_project.py at the preserved 2eb05ef source tree.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import traceback

BASE = "2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5"
SOURCE_REF = "ae8bbdfd2a18e8910eebc25fd2a81661c01abc16"
KERNEL = f"proofs/archive/source-trees/{BASE}/proofs/contributions/agent-104/seven-column-kernel/"
PINNED = {
    "PrefixCertificate": (KERNEL + "PrefixCertificate.lean", "2b125b95c61604da41821eee4e58ce9a50f4039a7e43117a42194e6560adfca9"),
    "PrefixInverse": (KERNEL + "PrefixInverse.lean", "0a93622752fa22cf6c8de2efc8500dc313498d59831bb0e5381b3b351e0ab03e"),
    "LongRowsBase": (KERNEL + "certificate/LongRowsBase.lean", "6568c04797f1e4cf1388c08c6142c6566bbfce59ef3d41a0c8df95cd8b7d07aa"),
    "FastInverse": (KERNEL + "FastInverse.lean", "585cb4d197479714edbdbe147c2c1c489742fa0f8eb978571abdc602eada4eee"),
    "FastRowsBase": (KERNEL + "certificate/FastRowsBase.lean", "e6ae5bcf64ca61d4c3d5aba5f1e08a956f969a8c4b98a85bb2b62867064a1984"),
    "Agent124FastPred": ("proofs/archive/versions/43632c45bbebfd6c14e441b995922ee67064f1f21d78530b3b2cf314048e4e57/proofs/contributions/agent-124/prefix-five-six/Agent124FastPred.lean", "cb88c693b7161446232df1c8a45cc8e71a84731ccfb9d4164c9dac26b2a91b5f"),
    "LychrelDigitSums": (f"proofs/archive/source-trees/{BASE}/proofs/research/continuation/LychrelDigitSums.lean", "ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57"),
    "ActualPrefix": (KERNEL + "ActualPrefix.lean", "c136216ed9c4100a268643be9a471b6746320f63d0af2030b6418429e5551e76"),
    "PalindromeBridge": (KERNEL + "PalindromeBridge.lean", "6c1de8cf02ec9381e80388e6b4915db6cfa4d1189d3e47c273400f0d37948093"),
    "ShortBoundary": (KERNEL + "ShortBoundary.lean", "a018a0b73bfc82f12bc6d866dd3b396bf6b217cae3e0448883be04e2c50e50c9"),
    "Agent124PrefixK": ("proofs/archive/versions/d840b483e24a5b30c93569580b402c111aac4863a1e0ba712e5102e1bdcefb8f/proofs/contributions/agent-124/prefix-five-six/Agent124PrefixK.lean", "7b9de533a36b5cb684c5a751940af5a98150ea6dba6519fe5a11651933171314"),
    "Agent124PrefixR": ("proofs/archive/versions/c9375213bdf13cc4aa4e478251fea50d8d7b2ca40ab0f733844adf2e7764442e/proofs/contributions/agent-124/prefix-five-six/Agent124PrefixR.lean", "bcb76dbc980957229c1d983bd6b5e36e974a64d7eb2049d30f93b0150c1fcdd2"),
    "Agent124CodeCert": ("proofs/archive/versions/7a27f5f80a6e34725a0629b24d9b1f99ae93ed3bc02a333109bcc7a03a8c7b29/proofs/contributions/agent-124/prefix-five-six/Agent124CodeCert.lean", "7feaa64ac30fa69a8b2961d2dc5341eb089087850088d065f8146f07078ea000"),
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def code_only(text: str) -> str:
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
                string = text[i] != '"'; out.append("\n" if text[i] == "\n" else " "); i += 1
        elif pair == "/-":
            depth = 1; out.extend("  "); i += 2
        elif pair == "--":
            end = text.find("\n", i); end = len(text) if end < 0 else end
            out.extend(" " * (end - i)); i = end
        elif text[i] == '"':
            string = True; out.append(" "); i += 1
        else:
            out.append(text[i]); i += 1
    if depth or string:
        raise ValueError("Unterminated Lean comment/string")
    return "".join(out)


def audit_source(modules: list[str]) -> str:
    return "import Agent124CodeCert\nimport Lean\nopen Lean Elab Command\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n" + """
#check Agent124.PrefixR.actual_iterPairs_rank_R
#check Agent124.PrefixR.ancestry_bound_of_R
#check Agent124.PrefixR.no_196_of_R
#check Agent124.CodeCert.rowsClosed_of_all
run_cmd do
  let env ← getEnv
  let selected : List String := """ + json.dumps(modules) + """
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut union : List Name := []
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        match info with
        | .axiomInfo v =>
          if v.isUnsafe then logInfo m!"UNSAFE_IMPLEMENTATION_AXIOM {mod} {name}"
          else throwError m!"CUSTOM_AXIOM {mod} {name}"
        | .thmInfo _ =>
          count := count + 1
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          for ax in axl do
            if !(union.contains ax) then union := ax :: union
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          logInfo m!"AUDIT_THEOREM {mod} {name} : {axl}"
        | _ => pure ()
  logInfo m!"FULL_MODULE_AUDIT theorems={count} union={union}"
"""


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, required=True)
    p.add_argument("--lean", type=Path, required=True)
    p.add_argument("--build", type=Path, required=True)
    p.add_argument("--evidence", type=Path, required=True)
    p.add_argument("--export-root", type=Path)
    args = p.parse_args()
    repo, lean, build, evidence = (x.resolve() for x in (args.repo, args.lean, args.build, args.evidence))
    build.mkdir(parents=True, exist_ok=False)
    evidence.mkdir(parents=True, exist_ok=True)
    logs = evidence / "logs"
    logs.mkdir(exist_ok=False)
    report = {"agent": "Agent #104", "specialist": "runtime_scout", "scope": "generic 13-module CodeCert dependency closure; no 620 instance proved by this build", "status": "RUNNING", "build": str(build), "empty_build_at_start": True, "source_ref": SOURCE_REF, "started_at_epoch": time.time(), "commands": [], "reused_olean_files": []}

    def save() -> None:
        (evidence / "build.json").write_text(json.dumps(report, indent=2) + "\n")

    def git(*argv: str) -> bytes:
        return subprocess.check_output(["git", "-C", str(repo), *argv])

    def run(label: str, argv: list[str], env: dict[str, str] | None = None) -> str:
        log = logs / (label + ".log")
        start = time.monotonic()
        with log.open("xb") as stream:
            try:
                rc = subprocess.run(argv, cwd=build, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=1800).returncode
            except subprocess.TimeoutExpired:
                rc = 124
        data = log.read_bytes()
        report["commands"].append({"label": label, "argv": argv, "exit_code": rc, "elapsed_seconds": round(time.monotonic() - start, 6), "log": str(log.relative_to(evidence)), "log_sha256": sha(data)})
        save()
        print(label, "exit=" + str(rc), flush=True)
        if rc:
            raise RuntimeError("Command failed: " + label)
        return data.decode()

    try:
        version = run("000-lean-version", [str(lean), "--version"]).strip()
        if version != "Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)":
            raise ValueError("Unexpected Lean version")
        runtime = Path(run("001-lean-prefix", [str(lean), "--print-prefix"]).strip()).resolve()
        compiler_files = [lean, *sorted((runtime / "lib/lean").glob("*.so"))]
        report["compiler"] = {"version": version, "files": {str(f): sha(f.read_bytes()) for f in compiler_files}}
        records, originals = {}, {}
        for name, (path, expected_sha) in PINNED.items():
            data = git("show", SOURCE_REF + ":" + path)
            blob = git("rev-parse", SOURCE_REF + ":" + path).decode().strip()
            if sha(data) != expected_sha or hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest() != blob:
                raise ValueError("Source pin mismatch: " + name)
            if (repo / path).read_bytes() != data:
                raise ValueError("Working source differs from pinned commit: " + name)
            masked = code_only(data.decode())
            if re.search(r"(?<![\w'])\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC)\b(?![\w'])", masked):
                raise ValueError("Forbidden source token: " + name)
            imports = [w for line in re.findall(r"^\s*import\s+([^\n]+)", masked, re.M) for w in line.split()]
            for dep in imports:
                if dep not in PINNED and not (dep.split(".")[0] in {"Std", "Init", "Lean"} and (runtime / "lib/lean" / (dep.replace(".", "/") + ".olean")).is_file()):
                    raise ValueError("Unpinned import: " + name + " -> " + dep)
            record = {"source_ref": SOURCE_REF, "source_path": path, "git_blob": blob, "sha256": expected_sha, "bytes": len(data), "imports": imports, "build_module": name, "build_source": name + ".lean", "source_url": "https://github.com/taco-jpg/p196-algorithm/blob/" + SOURCE_REF + "/" + path}
            old_prefix = f"proofs/archive/source-trees/{BASE}/"
            if path.startswith(old_prefix):
                original = path[len(old_prefix):]
                if git("rev-parse", BASE + ":" + original).decode().strip() != blob:
                    raise ValueError("Preserved original blob mismatch: " + name)
                record["preserved_original_ref"] = BASE
                record["preserved_original_path"] = original
            records[name], originals[name] = record, data
            (build / (name + ".lean")).write_bytes(data)
        order, active, seen = [], set(), set()
        def visit(name: str) -> None:
            if name not in records or name in seen:
                return
            if name in active:
                raise ValueError("Import cycle: " + name)
            active.add(name)
            for dep in records[name]["imports"]:
                visit(dep)
            active.remove(name); seen.add(name); order.append(name)
        visit("Agent124CodeCert")
        if seen != set(records):
            raise ValueError("Closure contains unused modules")
        mapping = {"schema_version": 1, "agent": "Agent #104", "source_repository": "https://github.com/taco-jpg/p196-algorithm", "source_ref": SOURCE_REF, "root_modules": ["Agent124CodeCert"], "build_order": order, "modules": records}
        (evidence / "dependency-map.json").write_text(json.dumps(mapping, indent=2) + "\n")
        report["build_order"] = order
        report["dependency_map_sha256"] = sha((evidence / "dependency-map.json").read_bytes())
        save()
        env = {"PATH": str(lean.parent) + ":/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "LEAN_PATH": str(build)}
        for index, name in enumerate(order, 2):
            run(f"{index:03}-{name}", [str(lean), "-j1", "-DElab.async=false", "-o", name + ".olean", name + ".lean"], env)
        audit = audit_source(order)
        (build / "Agent104Prefix620BaseAxiomAudit.lean").write_text(audit)
        (evidence / "Agent104Prefix620BaseAxiomAudit.lean").write_text(audit)
        audit_log = run("015-module-axiom-audit", [str(lean), "-j1", "-DElab.async=false", "Agent104Prefix620BaseAxiomAudit.lean"], env)
        summaries = re.findall(r"^FULL_MODULE_AUDIT theorems=(\d+) union=([^\n]*)$", audit_log, re.M)
        declarations = re.findall(r"^AUDIT_THEOREM (\S+) (\S+) : (.*)$", audit_log, re.M)
        if len(summaries) != 1 or int(summaries[0][0]) != len(declarations) or not declarations or len({x[1] for x in declarations}) != len(declarations):
            raise ValueError("Incomplete module-origin audit")
        report["theorem_count"] = len(declarations)
        report["axiom_union"] = summaries[0][1]
        report["unsafe_implementation_axioms"] = re.findall(r"^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$", audit_log, re.M)
        report["outputs"] = {name: {"source_sha256": sha((build / (name + ".lean")).read_bytes()), "olean_sha256": sha((build / (name + ".olean")).read_bytes())} for name in order}
        for name, data in originals.items():
            if (build / (name + ".lean")).read_bytes() != data:
                raise ValueError("Build source changed: " + name)
        for path, digest in report["compiler"]["files"].items():
            if sha(Path(path).read_bytes()) != digest:
                raise ValueError("Compiler changed during build: " + path)
        if args.export_root:
            dest = args.export_root.resolve(); dest.mkdir(parents=True, exist_ok=True)
            for name in order:
                for suffix in (".lean", ".olean"):
                    data = (build / (name + suffix)).read_bytes()
                    target = dest / (name + suffix)
                    if target.exists() and target.read_bytes() != data:
                        raise ValueError("Refusing to overwrite differing author dependency: " + str(target))
                    target.write_bytes(data)
            report["author_dependency_export"] = str(dest)
        report["status"] = "PASS_GENERIC_DEPENDENCIES_ONLY"
        print(report["status"], "theorems=" + str(report["theorem_count"]), flush=True)
        return 0
    except Exception as exc:
        report["status"] = "FAIL"
        report["error"] = str(exc)
        (evidence / "failure.txt").write_text(traceback.format_exc())
        print("FAIL", str(exc), flush=True)
        return 1
    finally:
        report["finished_at_epoch"] = time.time()
        save()


if __name__ == "__main__":
    raise SystemExit(main())
