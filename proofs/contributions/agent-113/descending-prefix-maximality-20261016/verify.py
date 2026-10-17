#!/usr/bin/env python3
"""Replay the finite evidence, strict four-module build, full audit and consumer.

The unchanged shared verifier first checks every registry source and import.
All subsequent Lean invocations explicitly use --trust=0, including dependencies.
Use a new output directory. This command verifies only the PR108 contribution.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PROJECT = "agent113-triple-maximality"
REGISTRY = ROOT / "proofs/Agent113TripleMaximality.registry.json"
VERIFIER = ROOT / "proofs/verify_project__214bf7673efe116b.py"
VERIFIER_SHA256 = "c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a"
FLAGS = ["--trust=0", "-j1", "-DElab.async=false"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    lean, out = args.lean.resolve(), args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    logs = out / "logs"
    logs.mkdir()
    report = {"status": "RUNNING", "project": PROJECT,
              "repository_wide_pass": False, "commands": [],
              "started_at_epoch": time.time(), "lean_arguments": FLAGS}

    def save():
        (out / "verification.json").write_text(json.dumps(report, indent=2) + "\n")

    def run(label, argv, cwd=ROOT, env=None):
        log = logs / (label + ".log")
        start = time.monotonic()
        with log.open("wb") as stream:
            try:
                rc = subprocess.run(argv, cwd=cwd, env=env, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=900).returncode
            except subprocess.TimeoutExpired:
                rc = 124
        report["commands"].append({"label": label, "argv": list(map(str, argv)),
            "cwd": str(cwd), "exit_code": rc,
            "elapsed_seconds": round(time.monotonic() - start, 6),
            "log": str(log.relative_to(out)), "log_sha256": sha(log)})
        save()
        print(label, "exit=" + str(rc), flush=True)
        if rc:
            raise RuntimeError(label + " failed; retained log: " + str(log))
        return log.read_text()

    try:
        if sha(VERIFIER) != VERIFIER_SHA256:
            raise ValueError("Shared source/import verifier changed; re-review its use")
        registry = json.loads(REGISTRY.read_bytes())
        report["registry_sha256"] = sha(REGISTRY)
        report["runner_sha256"] = sha(Path(__file__))
        bound_controls = {REGISTRY: report["registry_sha256"],
                          Path(__file__): report["runner_sha256"],
                          VERIFIER: VERIFIER_SHA256}
        report["source_commit"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        report["source_tree_clean"] = not subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT)
        (out / "registry.json").write_bytes(REGISTRY.read_bytes())
        spec = registry["projects"][PROJECT]
        pins = {ROOT / v["path"]: v["sha256"] for v in spec["modules"].values()}
        pins.update({HERE / n: h for n, h in registry["replay_inputs"].items()})
        for path, expected in pins.items():
            if sha(path) != expected:
                raise ValueError("Input identity mismatch: " + str(path))
        report["input_sha256"] = {str(p.relative_to(ROOT)): h for p, h in pins.items()}
        run("source-import-check", [sys.executable, str(VERIFIER), "--check-only",
            "--lean", str(lean), "--registry", str(REGISTRY), "--project", PROJECT,
            "--output", str(out / "source-check")])
        checked = json.loads((out / "source-check/verification.json").read_text())
        if checked["status"] != "SOURCE_AND_IMPORT_CHECK_ONLY":
            raise ValueError("Source/import preflight did not complete")
        report["compiler"] = checked["compiler"]
        selected = checked["projects"][PROJECT]
        order = selected["build_order"]
        if set(order) != set(spec["modules"]) or len(order) != 4:
            raise ValueError("Expected exactly the complete four-module closure")
        source = out / "source-check" / PROJECT / "source"
        report["build_order"] = order
        audit_json = run("finite-audit", [sys.executable, str(HERE / "check.py"),
                        "--verify", str(HERE / "witnesses.txt")])
        witnesses = run("finite-witnesses", [sys.executable, str(HERE / "check.py"),
                                            "--generate"])
        if audit_json.encode() != (HERE / "audit.json").read_bytes():
            raise ValueError("Finite audit regeneration differs")
        if witnesses.encode() != (HERE / "witnesses.txt").read_bytes():
            raise ValueError("Witness regeneration differs")
        generation = out / "generator-replay"
        generation.mkdir()
        for name in registry["replay_inputs"]:
            shutil.copyfile(HERE / name, generation / name)
        run("finite-generator", [sys.executable, str(generation / "generate_lean.py")],
            cwd=generation)
        if (generation / "Agent113TripleCycles.lean").read_bytes() != (source / "Agent113TripleCycles.lean").read_bytes():
            raise ValueError("Generated Lean certificate differs from checked source")
        report["finite_replay"] = "PASS_BYTE_IDENTICAL"
        env = dict(os.environ)
        for key in ["LEAN_PATH", "LEAN_SRC_PATH", "LEAN_SYSROOT", "LD_PRELOAD"]:
            env.pop(key, None)
        env["LEAN_PATH"] = str(source)
        env["PATH"] = str(lean.parent) + ":/usr/bin:/bin"
        env["LANG"] = "C.UTF-8"
        if any(source.rglob("*.olean")):
            raise ValueError("Fresh source preflight unexpectedly contains compiled objects")
        for module in order:
            relative = module.replace(".", "/")
            run(module, [str(lean), *FLAGS, "-o", relative + ".olean", relative + ".lean"],
                cwd=source, env=env)
        endpoints = [n for c in registry["claims"] if c["project"] == PROJECT
                     for n in c["endpoints"]]
        if len(endpoints) != 42 or len(set(endpoints)) != 42 or any(
                not re.fullmatch(r"[A-Za-z_][\w]*(?:\.[A-Za-z_][\w]*)*", n)
                for n in endpoints):
            raise ValueError("Expected the 42 distinct public theorem endpoints")
        audit = "import Agent113TripleRepeat\nimport Lean\nopen Lean Elab Command\n"
        audit += "set_option maxRecDepth 100000\nset_option maxHeartbeats 0\n"
        audit += "run_cmd do\n  let env ← getEnv\n  let selected : List String := " + json.dumps(order) + "\n"
        audit += '''  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut safeCount := 0
  let mut implementationCount := 0
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let mod := env.allImportedModuleNames[idx.toNat]!
      if selected.contains mod.toString then
        if info.isUnsafe || info.isPartial then
          implementationCount := implementationCount + 1
          logInfo m!"AUDIT_IMPLEMENTATION {mod} {name} unsafe={info.isUnsafe} partial={info.isPartial}"
        else
          if let .axiomInfo _ := info then
            throwError m!"CUSTOM_AXIOM {mod} {name}"
          let kind := match info with
            | .thmInfo _ => "theorem"
            | .defnInfo _ => "definition"
            | .opaqueInfo _ => "opaque"
            | .inductInfo _ => "inductive"
            | .ctorInfo _ => "constructor"
            | .recInfo _ => "recursor"
            | .quotInfo _ => "quotient"
            | .axiomInfo _ => "axiom"
          let axs ← liftCoreM (Lean.collectAxioms name)
          let axl := axs.toList
          if axl.any (fun ax => !(allowed.contains ax)) then
            throwError m!"DISALLOWED_AXIOMS {mod} {name} : {axl}"
          safeCount := safeCount + 1
          logInfo m!"AUDIT_SAFE {mod} {name} {kind} : {axl}"
  logInfo m!"FULL_MODULE_AUDIT safe={safeCount} implementation={implementationCount}"
'''
        (source / "ProjectAudit.lean").write_text(audit)
        audit_log = run("ProjectAudit", [str(lean), *FLAGS, "ProjectAudit.lean"],
                        cwd=source, env=env)
        safe = re.findall(r"^AUDIT_SAFE (\S+) (\S+) (\S+) : (.*)$", audit_log, re.M)
        implementation = re.findall(r"^AUDIT_IMPLEMENTATION (\S+) (\S+) (.*)$", audit_log, re.M)
        totals = re.findall(r"^FULL_MODULE_AUDIT safe=(\d+) implementation=(\d+)$", audit_log, re.M)
        if len(totals) != 1 or tuple(map(int, totals[0])) != (len(safe), len(implementation)):
            raise ValueError("Missing or incomplete full module-origin audit")
        if not safe or len({x[1] for x in safe + implementation}) != len(safe) + len(implementation):
            raise ValueError("Empty or duplicate declaration audit")
        if not set(endpoints).issubset({x[1] for x in safe if x[2] == "theorem"}):
            raise ValueError("A public theorem is absent from the safe declaration audit")
        report["audit"] = {"safe_count": len(safe), "implementation_count": len(implementation),
            "safe_kinds": dict(collections.Counter(x[2] for x in safe)),
            "safe_modules": dict(collections.Counter(x[0] for x in safe)),
            "allowed_axioms": ["propext", "Classical.choice", "Quot.sound"]}
        (out / "declarations.json").write_text(json.dumps(
            {"safe": safe, "implementation": implementation}, indent=2) + "\n")
        consumer = out / "consumer"
        consumer.mkdir()
        (consumer / "ConsumerSmoke.lean").write_text("import Agent113TripleRepeat\n" +
            "\n".join("#check " + n + "\n#print axioms " + n for n in endpoints) + "\n")
        run("ConsumerSmoke", [str(lean), *FLAGS, "ConsumerSmoke.lean"], cwd=consumer, env=env)
        report["consumer_endpoints"] = endpoints
        for path, expected in pins.items():
            if sha(path) != expected:
                raise ValueError("Input changed during verification: " + str(path))
        for module, rec in spec["modules"].items():
            if sha(source / (module.replace(".", "/") + ".lean")) != rec["sha256"]:
                raise ValueError("Build snapshot changed: " + module)
        for path, expected in report["compiler"]["files"].items():
            if sha(Path(path)) != expected:
                raise ValueError("Compiler changed during verification")
        for path, expected in bound_controls.items():
            if sha(path) != expected:
                raise ValueError("Verification control changed during execution: " + str(path))
        report["status"] = "PASS"
        return 0
    except Exception as error:
        report["status"] = "FAIL"
        report["error"] = str(error)
        (out / "failure.txt").write_text(traceback.format_exc())
        print("FAIL:", error, flush=True)
        return 1
    finally:
        report["finished_at_epoch"] = time.time()
        save()
        files = {str(p.relative_to(out)): {"bytes": p.stat().st_size, "sha256": sha(p)}
                 for p in sorted(out.rglob("*")) if p.is_file()
                 and p.suffix not in {".olean", ".ilean", ".pyc"} and p.name != "FILES.json"}
        (out / "FILES.json").write_text(json.dumps(files, indent=2) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
