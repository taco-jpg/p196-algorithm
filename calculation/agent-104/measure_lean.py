#!/usr/bin/env python3
"""Measure one Lean source under lean/; write no logs or compilation artifacts.

Example (from the repository root):
  python3 calculation/agent-104/measure_lean.py P196/Result/Head.lean

Linux only: child ru_maxrss is measured in KiB.  Each invocation launches one
Lake command in a fresh process group, confines it to one available CPU, and
sets LEAN_NUM_THREADS=1.  An optional --hard-as also limits virtual address space
to 8 GiB; measured resident memory must satisfy the 8 GiB budget regardless.
"""

import argparse
import json
import math
import os
from pathlib import Path
import resource
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
LEAN = ROOT / "lean"
MEMORY_BYTES = 8 * 1024 ** 3


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--timeout", type=float, default=1200)
    parser.add_argument("--hard-as", action="store_true")
    parser.add_argument("--toolchain-bin", type=Path,
                        help="directory containing lean and lake; otherwise discover lake on PATH")
    args = parser.parse_args()
    if sys.platform != "linux":
        parser.error("this helper requires Linux ru_maxrss and CPU affinity semantics")
    if not math.isfinite(args.timeout) or not 0 < args.timeout <= 1200:
        parser.error("--timeout must be finite, positive, and at most 1200 seconds")
    source = args.source
    if not source.is_absolute():
        source = (ROOT if source.parts[:1] == ("lean",) else LEAN) / source
    source = source.resolve()
    if not source.is_relative_to(LEAN.resolve()) or not source.is_file() or source.suffix != ".lean":
        parser.error("source must be an existing .lean file inside this repository's lean/")
    if args.toolchain_bin is not None:
        toolchain = args.toolchain_bin.expanduser().resolve()
        lake = toolchain / "lake"
    else:
        installed_lake = shutil.which("lake")
        if installed_lake is None:
            parser.error("lake was not found on PATH; add the Lean toolchain bin directory "
                         "to PATH or supply --toolchain-bin")
        # Preserve a proxy's executable basename (for example an elan lake symlink).
        lake = Path(installed_lake).absolute()
        toolchain = lake.parent
    if not lake.is_file() or not (toolchain / "lean").is_file():
        parser.error("--toolchain-bin must contain the lean and lake executables")
    available = os.sched_getaffinity(0)
    if not available:
        parser.error("no CPU is available for the required single-core measurement")
    cpu = min(available)
    command = [str(lake), "env", "lean", str(source.relative_to(LEAN))]
    env = dict(os.environ, LEAN_NUM_THREADS="1")
    env["PATH"] = str(toolchain) + os.pathsep + env.get("PATH", "")

    def child_limits():
        os.sched_setaffinity(0, {cpu})
        requested_cpu = math.ceil(args.timeout)
        _, old_cpu_hard = resource.getrlimit(resource.RLIMIT_CPU)
        if old_cpu_hard != resource.RLIM_INFINITY:
            requested_cpu = min(requested_cpu, old_cpu_hard)
        resource.setrlimit(resource.RLIMIT_CPU, (requested_cpu, requested_cpu))
        if args.hard_as:
            _, old_as_hard = resource.getrlimit(resource.RLIMIT_AS)
            hard_as = MEMORY_BYTES if old_as_hard == resource.RLIM_INFINITY else min(MEMORY_BYTES, old_as_hard)
            resource.setrlimit(resource.RLIMIT_AS, (hard_as, hard_as))

    record = {"command": command, "cwd": str(LEAN),
              "environment": {"LEAN_NUM_THREADS": "1", "PATH_prefix": str(toolchain)},
              "cpu_affinity": [cpu], "wall_budget_seconds": args.timeout,
              "rss_budget_bytes": MEMORY_BYTES, "hard_as": args.hard_as}
    print("COMMAND " + json.dumps(record, sort_keys=True), flush=True)
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    started = time.perf_counter()
    timed_out = False
    try:
        process = subprocess.Popen(command, cwd=LEAN, env=env, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   start_new_session=True, preexec_fn=child_limits)
        try:
            stdout, stderr = process.communicate(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            stdout, stderr = process.communicate()
        exit_code = process.returncode
    except (OSError, subprocess.SubprocessError) as error:
        stdout, stderr, exit_code = "", str(error) + "\n", 127
    elapsed = time.perf_counter() - started
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    max_rss_kib = after.ru_maxrss
    rss_bytes = max_rss_kib * 1024
    cpu_seconds = after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime
    within_budget = (not timed_out and exit_code == 0 and 0 < rss_bytes <= MEMORY_BYTES
                     and elapsed <= args.timeout and cpu_seconds <= 1200)
    if stdout:
        sys.stdout.write(stdout)
    if stderr:
        sys.stderr.write(stderr)
    record.update({"exit_code": exit_code, "seconds": round(elapsed, 6),
                   "cpu_seconds": round(cpu_seconds, 6), "max_rss_kib": max_rss_kib,
                   "max_rss_bytes": rss_bytes, "timed_out": timed_out,
                   "budget_result": "PASS" if within_budget else "FAIL"})
    print("MEASUREMENT " + json.dumps(record, sort_keys=True), flush=True)
    return 0 if within_budget else 1


if __name__ == "__main__":
    sys.exit(main())
