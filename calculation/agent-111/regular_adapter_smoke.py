#!/usr/bin/env python3
"""Small production regular-center positives and fail-closed adapter guards.

Source cycles come from Lean files; every returned center edge is replayed by
center_controls' independent whole-integer arithmetic. Positive controls use
fixed widths; cap guards also enter generic/all-width modes. Children have
CPU/wall and ordinary memory bounds.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import re
import resource
import subprocess

import center_controls as arithmetic
import regular_center as adapter


def require(good, why):
    if not good:
        raise RuntimeError(why)


def detail(result):
    return (f"args={result.args!r} returncode={result.returncode} "
            f"stdout={result.stdout[-3000:]!r} stderr={result.stderr[-3000:]!r}")


def clean_sanitizer(result):
    require(not re.search(r"AddressSanitizer|LeakSanitizer|runtime error:", result.stderr),
            "sanitizer finding: " + detail(result))


@contextmanager
def sanitizer_environment(enabled):
    previous = os.environ.get("ASAN_OPTIONS")
    if enabled:
        os.environ["ASAN_OPTIONS"] = (previous or "") + ":detect_leaks=0"
    try:
        yield
    finally:
        if enabled:
            if previous is None:
                os.environ.pop("ASAN_OPTIONS", None)
            else:
                os.environ["ASAN_OPTIONS"] = previous


def source_cases(root):
    certificates = arithmetic.read_certificates(root)
    for name, base, copies, clustered in (
        ("base2_K1", 2, 1, False),
        ("base2_K2", 2, 2, False),
        ("base2_K2_asymmetric", 2, 2, True),
        ("base26_K1", 26, 1, False),
    ):
        edges = certificates[base] * copies
        if clustered:
            target = (1, 1) + (0,) * (len(edges) - 2)
            edges, _ = arithmetic.pad_to_schedule(base, edges, target)
        e, g = arithmetic.inspect_certificate(base, edges)
        trims = tuple(edge.v for edge in edges)
        yield name, base, e, g, trims, len(edges[0].C)


def positive_controls(binary, root, sanitizer):
    reports = []
    replayed = 0
    for name, base, e, g, trims, width in source_cases(root):
        result = adapter.run(binary, base, "".join(map(str, e)), "".join(map(str, g)),
                             width, width, "".join(map(str, trims)), witness=True,
                             timeout=10, memory_mb=None if sanitizer else 512)
        clean_sanitizer(result)
        require(result.returncode == 0 and re.search(r"^DONE .*\bstatus=hit\b", result.stdout, re.M)
                and "quantifier=all_positive_repetitions" in result.stdout,
                "source positive lost completed verdict: " + detail(result))
        require(not re.search(r"UNDECIDED|CAPPED|NOPERIOD|INVALID_OR_UNSUPPORTED",
                              result.stdout + result.stderr),
                "source positive incomplete: " + detail(result))
        lines = [line for line in result.stdout.splitlines() if line.startswith("FEASIBLE ")]
        require(len(lines) == 1, "expected one fixed-width source witness: " + detail(result))
        line = lines[0]
        fields = dict(re.findall(r"\b(m0|repeats|actual_period)=(\d+)", line))
        require(set(fields) == {"m0", "repeats", "actual_period"}, "missing witness metadata")
        repeats, actual_period = int(fields["repeats"]), int(fields["actual_period"])
        require(int(fields["m0"]) == width and repeats >= 1 and actual_period == repeats * len(e),
                "incorrect witness period or initial width")
        centers = {}
        for index, values in re.findall(r"\bC(\d+)=\[([^\]]*)\]", line):
            index = int(index)
            require(index not in centers, "duplicate witness center index")
            require(re.fullmatch(r"\s*\d+(?:\s*,\s*\d+)*\s*", values) is not None,
                    "malformed or empty witness center")
            centers[index] = tuple(map(int, values.split(",")))
        require(set(centers) == set(range(actual_period)), "incomplete witness center sequence")
        require(len(centers[0]) == width, "witness has wrong actual initial width")
        for i in range(actual_period):
            j = i % len(e)
            next_center = arithmetic.center_step(base, centers[i], e[j], g[j], trims[j])
            require(next_center == centers[(i + 1) % actual_period],
                    f"independent witness replay failed: {name} edge {i}")
            replayed += 1
        reports.append({"name": name, "base": base, "unit_period": len(e),
                        "segments": sum(trims), "initial_width": width,
                        "repeats": repeats, "actual_period": actual_period})
    return {"sanitizer": sanitizer, "positive_cases": reports,
            "independently_replayed_edges": replayed}


def direct(binary, args, sanitizer):
    def bounds():
        if not sanitizer:
            resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2,) * 2)
        resource.setrlimit(resource.RLIMIT_CPU, (10, 11))
    return subprocess.run([str(binary), *args], text=True, capture_output=True,
                          check=False, timeout=10, preexec_fn=bounds)


def guard_controls(binary, sanitizer):
    ordinary = ["2", "1010", "1010", "2", "2", "-v", "0001"]
    rejected = [
        ["2", "00", "00", "1", "1", "-v", "00"],  # K=0 unsupported
        ordinary + ["-legacy"], ordinary + ["-edge-cap", "0"],
        ordinary + ["-work-cap", "0"], ordinary + ["-layers", "0"],
        ordinary + ["-layers", "10001"], ordinary + ["-edge-cap"],
        ordinary + ["-work-cap", "1x"],
    ]
    for args in rejected:
        result = direct(binary, args, sanitizer)
        clean_sanitizer(result)
        require(result.returncode == 2 and "INVALID_OR_UNSUPPORTED:" in result.stderr,
                "direct input rejection lost: " + detail(result))
        require("DONE " not in result.stdout
                and not re.search(r"\bstatus=(?:none|hit)\b", result.stdout + result.stderr),
                "unsupported input acquired a completed verdict: " + detail(result))

    def incomplete(result, expected_status, reason):
        clean_sanitizer(result)
        require(not re.search(r"\bstatus=(?:none|hit)\b", result.stdout + result.stderr),
                "incomplete run acquired a completed verdict: " + detail(result))
        require(result.returncode == 0 and f"status={expected_status}" in result.stdout
                and "UNDECIDED:" in result.stderr and reason in result.stderr,
                "incomplete result lost precise status/reason: " + detail(result))
        require("INVALID_OR_UNSUPPORTED:" not in result.stderr,
                "valid bounded input became input rejection: " + detail(result))

    resource_cases = 0
    for mode in ({}, {"generic_only": True}, {"all_lengths": True}):
        for settings, reason in (({"cap": 1}, "state cap"),
                                 ({"edge_cap": 1}, "edge cap"),
                                 ({"work_cap": 1}, "work cap")):
            # This is a known positive at width 2, so ignoring the cap cannot
            # accidentally pass as an exact width-1 empty result.
            result = adapter.run(binary, 2, "1010", "1010", 2, 2, "0001",
                                 timeout=10, memory_mb=None if sanitizer else 512,
                                 **mode, **settings)
            incomplete(result, "noperiod" if mode else "capped", reason)
            resource_cases += 1
    horizon = adapter.run(binary, 10, "10100110011", "11100010000", 1, 1, "00100010000",
                          generic_only=True, layers=1, timeout=10,
                          memory_mb=None if sanitizer else 512)
    incomplete(horizon, "noperiod", "generic layer horizon=1")

    invalid_wrapper = [dict(cap=0), dict(edge_cap=0), dict(work_cap=0),
                       dict(layers=0), dict(layers=10001), dict(layers=1.0)]
    for kwargs in invalid_wrapper:
        try:
            adapter.run(binary, 2, "1010", "1010", 2, 2, "0001", **kwargs)
        except ValueError:
            pass
        else:
            raise RuntimeError(f"invalid wrapper limit accepted: {kwargs!r}")
    try:
        adapter.run(binary, 2, "00", "00", 1, 1, "00")
    except ValueError:
        pass
    else:
        raise RuntimeError("wrapper accepted unsupported K=0")
    return {"sanitizer": sanitizer, "direct_rejections": len(rejected),
            "resource_cap_cases": resource_cases, "generic_horizon_cases": 1,
            "wrapper_rejections": len(invalid_wrapper) + 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--sanitizer-binary", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    binaries = [(args.binary.resolve(), False)]
    if args.sanitizer_binary:
        binaries.append((args.sanitizer_binary.resolve(), True))
    for binary, sanitizer in binaries:
        with sanitizer_environment(sanitizer):
            print("REGULAR_SOURCE_POSITIVES " + json.dumps(
                positive_controls(binary, root, sanitizer), sort_keys=True), flush=True)
            print("REGULAR_ADAPTER_GUARDS " + json.dumps(
                guard_controls(binary, sanitizer), sort_keys=True), flush=True)
    print("ALL REGULAR ADAPTER SMOKES PASSED", flush=True)


if __name__ == "__main__":
    main()
