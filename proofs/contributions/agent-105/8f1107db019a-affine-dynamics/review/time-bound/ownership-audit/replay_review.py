#!/usr/bin/env python3
"""Independent, source-pinned empty-directory review; retains every execution."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

PINS = {
    "PeriodObstructions": ("proofs/PeriodObstructions__70ce034b31b5b218.lean", "83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a"),
    "ActualWordBridge": ("proofs/ActualWordBridge__7f032d27940694a8.lean", "3123e8f86fe751e61307ea528390bd265515a8d69c731f51e2808fb78d0a6ec6"),
    "Agent105ReturnTimeBound": ("proofs/Agent105ReturnTimeBound.lean", "93384ce0e3a2443ca37fbb2c510ce927f0f2334509b6430d7b91ff252d0d57f7"),
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    source, logs = out / "source", out / "logs"
    source.mkdir(); logs.mkdir()
    receipt = {
        "executor": "Agent #105 /root/ownership_audit / agent105-8f1107db019a",
        "role": "independent semantic and compile review of root-authored ReturnTimeBound",
        "status": "RUNNING", "started_at_epoch": time.time(), "sources": {}, "commands": [],
        "scope": "Original Agent8 list dynamics; all endpoint, canonicality and positive-time hypotheses retained. No integer realizability or safe-return existence inferred.",
    }
    rc = 1
    try:
        receipt["source_commit"] = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=args.repo, text=True).strip()
        receipt["runtime_sha256"] = sha(args.lean.read_bytes())
        receipt["runtime_version"] = subprocess.check_output([str(args.lean), "--version"], text=True).strip()
        for module, (relative, expected) in PINS.items():
            data = (args.repo / relative).read_bytes()
            if sha(data) != expected:
                raise ValueError("Source pin mismatch: " + module)
            (source / (module + ".lean")).write_bytes(data)
            receipt["sources"][module] = {"path": relative, "sha256": expected, "bytes": len(data)}
        checker = Path(__file__).resolve().with_name("ReviewScope.lean")
        shutil.copyfile(checker, source / checker.name)
        env = dict(os.environ)
        env["LEAN_PATH"] = str(source)
        for module in [*PINS, "ReviewScope"]:
            cmd = [str(args.lean), "--trust=0", "-j1", "-DElab.async=false", "-o", module + ".olean", module + ".lean"]
            started = time.monotonic()
            with (logs / (module + ".log")).open("wb") as stream:
                result = subprocess.run(cmd, cwd=source, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=1800)
            receipt["commands"].append({"module": module, "argv": cmd, "exit_code": result.returncode, "elapsed_seconds": time.monotonic() - started, "log_sha256": sha((logs / (module + ".log")).read_bytes())})
            (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
            print(module, "exit=" + str(result.returncode), flush=True)
            if result.returncode:
                raise RuntimeError("Compile failed: " + module)
        for module, (relative, expected) in PINS.items():
            if sha((args.repo / relative).read_bytes()) != expected:
                raise ValueError("Source changed during review: " + module)
        receipt["status"] = "PASS"
        rc = 0
    except Exception as error:
        receipt["status"] = "FAIL"
        receipt["error"] = str(error)
        print("FAIL", error, flush=True)
    finally:
        receipt["finished_at_epoch"] = time.time()
        (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
