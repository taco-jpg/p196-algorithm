#!/usr/bin/env python3
"""Bounded production-adapter rejection and interruption controls.

Run: python3 -O calculation/agent-111/mdd_guards.py --binary /tmp/agent111_mdd
Optionally add --sanitizer-binary /tmp/agent111_mdd_san. Every child actually
runs; timeout and allocation failures are not mocked. No output files are kept.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import resource
import subprocess

import long_center

E33 = "10100110011" * 3
G33 = "11100010000" * 3
V33 = "00100010000" * 3
E48 = "101010010101" * 4
G48 = "100010001000" * 4
V48 = "1" * 6 + "0" * 42


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def detail(result):
    return (f"args={result.args!r}; returncode={result.returncode}; "
            f"stdout={result.stdout[-2500:]!r}; stderr={result.stderr[-2500:]!r}")


def incomplete(result):
    """An interrupted computation must not issue a completed verdict."""
    require(re.search(r"\bstatus=(?:none|hit)\b", result.stdout + result.stderr) is None,
            "incomplete execution issued completed verdict: " + detail(result))
    require("INVALID_OR_UNSUPPORTED:" not in result.stderr,
            "valid resource control was rejected as input: " + detail(result))
    require(not re.search(r"AddressSanitizer|LeakSanitizer|runtime error:", result.stderr),
            "sanitizer finding: " + detail(result))


def direct(binary, extra, *, sanitizer=False):
    command = [str(binary), "10", E33, G33, "1", "10", "-v", V33, *extra]
    env = os.environ.copy()
    if sanitizer:
        # ASan's address reservation cannot coexist with a small RLIMIT_AS.
        # This sandbox also prevents LeakSanitizer from inspecting /proc/task.
        env["ASAN_OPTIONS"] = env.get("ASAN_OPTIONS", "") + ":detect_leaks=0"

    def limits():
        if not sanitizer:
            resource.setrlimit(resource.RLIMIT_AS, (256 * 1024**2,) * 2)
        resource.setrlimit(resource.RLIMIT_CPU, (10, 11))

    return subprocess.run(command, text=True, capture_output=True, check=False,
                          timeout=10, preexec_fn=limits, env=env)


def adapter_controls(binary, *, sanitizer=False):
    malformed = [
        ["-work-cap"], ["-work-cap", "0"], ["-work-cap", "-1"],
        ["-work-cap", "2x"], ["-work-cap", "999999999999999999999"],
        ["-layers"], ["-layers", "0"], ["-layers", "10001"],
        ["-layers", "1.5"], ["-diff-limit"], ["-diff-limit", "0"],
        ["-diff-limit", "-1"], ["-unknown-mdd-option"],
    ]
    for args in malformed:
        result = direct(binary, args, sanitizer=sanitizer)
        require(result.returncode == 2 and "INVALID_OR_UNSUPPORTED:" in result.stderr,
                "malformed input did not receive input rejection: " + detail(result))
        require("DONE " not in result.stdout and
                re.search(r"\bstatus=(?:none|hit)\b", result.stdout + result.stderr) is None,
                "malformed input received mathematical verdict: " + detail(result))
        require(not re.search(r"AddressSanitizer|LeakSanitizer|runtime error:", result.stderr),
                "sanitizer finding on rejected input: " + detail(result))

    cases = [
        ("allwidth_node_cap", ["-allm", "-cap", "1"], "noperiod", "node cap"),
        ("allwidth_work_cap", ["-allm", "-work-cap", "1"], "noperiod", "work cap"),
        ("fixedwidth_node_cap", ["-cap", "1"], "capped", "node cap"),
        ("fixedwidth_work_cap", ["-work-cap", "1"], "capped", "work cap"),
        ("generic_horizon", ["-allm", "-layers", "1"], "noperiod",
         "reason=generic_layer_limit horizon=1"),
        ("explicit_comparison_cap", ["-allm", "-diff", "-diff-limit", "1"],
         "noperiod", "MDD enumeration tuple cap"),
    ]
    for name, args, status, reason in cases:
        result = direct(binary, args, sanitizer=sanitizer)
        incomplete(result)
        require(result.returncode == 0 and f"status={status}" in result.stdout,
                name + " lost explicit incomplete status: " + detail(result))
        require(reason in result.stdout + result.stderr,
                name + " lost specific reason: " + detail(result))
        require("MDD_ERROR:" not in result.stderr,
                name + " became implementation error: " + detail(result))
    return {"malformed_mdd_options": len(malformed),
            "incomplete_cases": [row[0] for row in cases], "sanitizer": sanitizer}


def wrapper_controls(binary):
    # This actual production workload has a 43-step segment and exhausts a
    # 64 MiB address-space allowance before its ordinary MDD limits are reached.
    args = (binary, 10, E48, G48, 1, 1, V48)
    limited = long_center.run(*args, all_lengths=True, cap=100000000,
                              timeout=10, memory_mb=64)
    incomplete(limited)
    require(limited.returncode == 0 and "status=noperiod" in limited.stdout
            and "UNDECIDED: allocation limit" in limited.stderr,
            "actual memory-bound run lost allocation verdict: " + detail(limited))

    interrupted = long_center.run(*args, all_lengths=True, cap=100000000,
                                  timeout=0.000001, memory_mb=64)
    incomplete(interrupted)
    require(interrupted.returncode == 124
            and "UNDECIDED: wall timeout" in interrupted.stderr,
            "actual subprocess timeout was not retained: " + detail(interrupted))

    invalid = [{"timeout": v} for v in (0, -1, float("inf"), float("nan"), 1801)]
    invalid += [{"memory_mb": v} for v in (63, 8193, 64.0, True)]
    for kwargs in invalid:
        try:
            long_center.run(*args, **kwargs)
        except ValueError:
            pass
        else:
            raise RuntimeError(f"invalid wrapper setting accepted: {kwargs!r}")
    return {"actual_memory_limit_mb": 64, "actual_timeout_seconds": 0.000001,
            "timeout_returncode": interrupted.returncode,
            "invalid_wrapper_settings": len(invalid)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--sanitizer-binary", type=Path)
    args = parser.parse_args()
    binary = args.binary.resolve()
    print("INHERITED_FRONTEND_GUARDS " + json.dumps(
        long_center.guard_selftest(binary), sort_keys=True), flush=True)
    print("MDD_ADAPTER_GUARDS " + json.dumps(
        adapter_controls(binary), sort_keys=True), flush=True)
    print("PROCESS_WRAPPER_GUARDS " + json.dumps(
        wrapper_controls(binary), sort_keys=True), flush=True)
    if args.sanitizer_binary:
        print("MDD_SANITIZER_GUARDS " + json.dumps(
            adapter_controls(args.sanitizer_binary.resolve(), sanitizer=True),
            sort_keys=True), flush=True)
    print("ALL MDD GUARDS PASSED", flush=True)


if __name__ == "__main__":
    main()
