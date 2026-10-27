#!/usr/bin/env python3
"""All-length center audit for the G<=4 obstruction; no Lean claim.

Run from any directory. The existing cauto_fast.cpp is compiled into a temporary
directory unless --binary is supplied. No search output files are created.
All caps, timeouts, missing coverage, and unexpected positive results fail closed.
"""
from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "calculation/neutral_band/structure/cauto_fast.cpp"
E11, G11 = "10100110011", "11100010000"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def command(args: list[str], timeout: float) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    require(result.returncode == 0, f"command failed: {args}\n{result.stderr[-3000:]}")
    return result


def check_stream(binary: str, base: int, e: str, g: str, *, all_patterns: bool,
                 legacy: bool, expect_hit: bool, timeout: float) -> dict[str, int]:
    p, k = len(g), g.count("1") // 2
    require(len(e) == p and g.count("1") % 2 == 0, "bad driver")
    require(set(e + g) <= {"0", "1"}, "nonbinary driver")
    require(1 <= k <= p <= 32, "unsupported period/trim budget")
    # The legacy serializer uses 2P + 6G + 7K bits in a 256-bit key.
    require(2*p + 6*g.count("1") + 7*k <= 256, "packed-key overflow")
    args = [binary, str(base), e, g, "1", "1", "-allm", "-cap", "3000000"]
    args += ["-vall"] if all_patterns else ["-v", "1"*k + "0"*(p-k)]
    if legacy:
        args.append("-legacy")
    result = command(args, timeout)
    require("warning:" not in result.stderr, "solver warning")
    require(not re.search(r"^(?:CAPPED|NOPERIOD)\b", result.stdout, re.M),
            "center decision is UNDECIDED")
    rows = []
    for line in result.stdout.splitlines():
        if line.startswith("DONE "):
            rows.append(dict(re.findall(r"([a-z_]+)=([^ ]+)", line)))
    expected = math.comb(p, k) if all_patterns else 1
    require(len(rows) == expected, f"missing patterns: {len(rows)}/{expected}")
    patterns = {row["v"] for row in rows}
    require(len(patterns) == expected, "duplicate/missing pattern")
    require(all(len(v) == p and set(v) <= {"0", "1"} and v.count("1") == k
                for v in patterns), "bad reported pattern")
    require(all(row["status"] in {"none", "hit"} and int(row["period"]) > 0
                for row in rows), "incomplete all-length periodic-tail check")
    summary = re.search(r"instances (\d+) feasible (\d+) capped/noperiod (\d+)",
                        result.stderr)
    require(summary is not None and int(summary[3]) == 0, "missing complete summary")
    hits = sum(row["status"] == "hit" for row in rows)
    require((hits > 0) == expect_hit, f"unexpected center feasibility: {hits}")
    require((int(summary[2]) > 0) == expect_hit, "inconsistent feasible count")
    if not expect_hit:
        require(not re.search(r"^FEASIBLE", result.stdout, re.M), "unexpected witness")
        require(all(int(row["feasible_classes"]) == 0 for row in rows),
                "unexpected unbounded feasible class")
    answer = {
        "patterns": expected,
        "instances": int(summary[1]),
        "hits": hits,
        "maxstates": max(int(row["maxstates"]) for row in rows),
        "max_jstar": max(int(row["jstar"]) for row in rows),
        "max_period": max(int(row["period"]) for row in rows),
    }
    mode = "legacy" if legacy else "fast"
    print(f"CENTER base={base} p={p} G={2*k} mode={mode} "
          + " ".join(f"{key}={value}" for key, value in answer.items()), flush=True)
    return answer


def controls(binary: str, timeout: float) -> None:
    sys.path.insert(0, str(ROOT / "calculation"))
    import neutral_band_search as mirror
    certificates = mirror._lean_certs()
    require({b for b, _ in certificates} == {2, 4, 8, 11, 16, 17, 26, 32},
            "known certificate source set changed")
    count = 0
    for base, edges in sorted(certificates):
        require(mirror.cycleOK(base, edges, edges[0][0], edges[0][1]),
                f"base-{base} source certificate does not replay")
        h = base - 1
        for B, C, B2, C2, u, v in edges:
            raw = mirror.nextC(base, B, C)
            for padding in (0, 1, 2, 5):
                padded = [h]*padding + C + [h]*padding
                require(mirror.hyp(base, B, padded), "padding changed Hyp")
                require(mirror.e2(base, B, padded) == mirror.e2(base, B, C),
                        "padding changed the center carry")
                require(mirror.nextC(base, B, padded) == [h]*padding + raw + [h]*padding,
                        "center padding covariance failed")
                count += 1
        e = "".join(str(mirror.e1(base, edge[0])) for edge in edges)
        g = "".join(str(mirror.gam(base, edge[0], edge[1])) for edge in edges)
        # Move the single center trim to the first phase, using unrestricted padding.
        check_stream(binary, base, e, g, all_patterns=False, legacy=False,
                     expect_hit=True, timeout=timeout)
    print(f"POSITIVE_CONTROLS bases=8 edges=56 padding_checks={count} PASS", flush=True)


def run(binary: str, timeout: float) -> None:
    print("cauto_source_sha256=" + hashlib.sha256(SOURCE.read_bytes()).hexdigest(), flush=True)
    controls(binary, timeout)
    result = check_stream(binary, 10, E11, G11, all_patterns=True, legacy=False,
                          expect_hit=False, timeout=timeout)
    require(result["patterns"] == 55, "p11 coverage mismatch")
    # Distinct full-state layer implementation; no segment factorization/cache.
    check_stream(binary, 10, E11, G11, all_patterns=False, legacy=True,
                 expect_hit=False, timeout=timeout)
    print("CENTER_G4_SURVIVOR_EXCLUDED all_lengths=true status=COMPUTED", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", help="existing cauto_fast binary")
    parser.add_argument("--timeout", type=float, default=120)
    args = parser.parse_args()
    require(0 < args.timeout <= 1500, "timeout must be in (0,1500]")
    if args.binary:
        run(str(Path(args.binary).resolve()), args.timeout)
    else:
        with tempfile.TemporaryDirectory(prefix="agent104-center-") as tmp:
            binary = str(Path(tmp) / "cauto_fast")
            command(["g++", "-O2", "-std=c++17", str(SOURCE), "-o", binary], 120)
            run(binary, args.timeout)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.TimeoutExpired) as error:
        print(f"UNDECIDED / CHECK FAILED: {error}", file=sys.stderr)
        sys.exit(1)
