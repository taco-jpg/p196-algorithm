#!/usr/bin/env python3
"""Finite single-worker sweep; retain every attempted query, answer, and failure."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import subprocess
import sys
import time


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solver-packages", type=Path, required=True)
    ap.add_argument("--first-width", type=int, default=7)
    ap.add_argument("--last-width", type=int, default=24)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=False)
    script = Path(__file__).with_name("search_bounded.py").resolve()
    start = time.monotonic()
    report = {
        "agent": "Agent #104",
        "claim": "b02a458471626627d5e13541acc855f9f4e2edd1",
        "status": "RUNNING",
        "verification_level": "BOUNDED_SOLVER_EXPERIMENT_ONLY",
        "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "domain": {"first_width": args.first_width, "last_width": args.last_width, "steps": 12, "prefix": "620"},
        "limits": {"one_worker": True, "solver_timeout_ms": 15000, "solver_memory_mb": 512, "worker_wall_seconds": 25, "sweep_wall_seconds": 330},
        "search_source_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "attempts": [],
    }
    def save():
        (root / "sweep.json").write_text(json.dumps(report, indent=2) + "\n")
    save()
    for width in range(args.first_width, args.last_width + 1):
        if time.monotonic() - start + 25 > 330:
            report["status"] = "STOPPED_AT_DECLARED_WALL_BUDGET"
            break
        target = root / f"width{width:02d}"
        argv = [sys.executable, str(script), "--solver-packages", str(args.solver_packages.resolve()), "--width", str(width), "--steps", "12", "--prefix", "620", "--timeout-ms", "15000", "--memory-mb", "512", "--output", str(target)]
        log = root / f"width{width:02d}.log"
        before = time.monotonic()
        with log.open("xb") as stream:
            try:
                rc = subprocess.run(argv, stdout=stream, stderr=subprocess.STDOUT, timeout=25).returncode
                kind = "EXIT"
            except subprocess.TimeoutExpired:
                rc = 124
                kind = "WORKER_WALL_TIMEOUT"
        result_path = target / "result.json"
        result = json.loads(result_path.read_text()) if result_path.exists() else {}
        item = {"width": width, "command": argv, "exit_code": rc, "termination": kind, "elapsed_seconds": time.monotonic() - before, "solver_status": result.get("status"), "reason_unknown": result.get("reason_unknown"), "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest()}
        report["attempts"].append(item)
        save()
        print(json.dumps(item), flush=True)
        if rc == 0 and result.get("status") == "sat":
            report["status"] = "CANDIDATE_FOUND_AND_INTEGER_REPLAYED"
            report["candidate"] = result["orbit"]
            break
    else:
        report["status"] = "BOUNDED_SWEEP_FINISHED"
    report["elapsed_seconds"] = time.monotonic() - start
    report["completed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save()
    print(json.dumps({"status": report["status"], "elapsed_seconds": report["elapsed_seconds"], "attempts": len(report["attempts"])}), flush=True)


if __name__ == "__main__":
    main()
