#!/usr/bin/env python3
"""Regression tests for the U44 two-epoch alert checker."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "tools" / "alert_check.py"
spec = importlib.util.spec_from_file_location("alert_check", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError("could not import tools/alert_check.py")
ac = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ac)
ac.ROOT = ROOT


def test_independent_engines() -> None:
    values = [1, 10, 196, 349, 9999, 1234567890, 10**80 + 123456789]
    rng = random.Random(4402)
    values.extend(rng.randrange(1, 10**100) for _ in range(200))
    for n in values:
        d = ac.bigint_digits(n)
        if ac.digits_to_int(d) != n:
            raise RuntimeError(f"digit decode mismatch for {n}")
        if ac.pairword_digits(d) != ac.pairword_bigint(n):
            raise RuntimeError(f"pairword engine mismatch for {n}")
        expected = ac.bigint_step(n)
        got = ac.digit_array_step(d)
        if ac.digits_to_int(got) != expected or ac.bigint_digits(expected) != got:
            raise RuntimeError(f"successor engine mismatch for {n}")


def test_known_nonreturning_control() -> None:
    lattice = ROOT / "calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt"
    raw = {
        "name": "R30 documented non-returning T* control",
        "base": 10, "lattice": str(lattice),
        "J": [5], "U": [9, 14, 4], "C": [10],
        "samples": [[20, 20]], "q_gain": 0, "k_gain": 5,
        "epoch_steps": 120, "epochs": 2,
        "overflow_clock": "1000", "overflow_repeats": 30,
        "require_odd_pair_guard": True,
    }
    claim = ac.normalize_claim(raw, ROOT / "calculation/new_structures/U44/r30_nearmiss.json")
    result = ac.run_sample(claim, 20, 20)
    if result["status"] != "FAIL" or result["steps"] != 240:
        raise RuntimeError("known non-returning control was not rejected")
    if not result["overflow_clock_matches"] or result["engine_mismatch_times"]:
        raise RuntimeError("known control's independent arithmetic/clock audit failed")
    if result["palindrome_times"] or result["odd_guard_missing_times"]:
        raise RuntimeError("known control unexpectedly violated its phase guard")
    endpoints = result["endpoint_returns"]
    if len(endpoints) != 2 or endpoints[0]["step"] != 120 or endpoints[0]["first_mismatch"] != 194:
        raise RuntimeError(f"first-epoch control mismatch not reproduced: {endpoints}")
    if endpoints[0]["return"] or endpoints[1]["return"]:
        raise RuntimeError("known non-returning control was falsely accepted")


def test_prefix_only_seam_rejected() -> None:
    lattice = ROOT / "calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt"
    raw = {
        "name": "S30 complementary-18 prefix-only control",
        "base": 10, "lattice": str(lattice),
        "J": [18,0,9,3,7,14,5,1,12,11,12,14,3,9,8,14,18,18,14,13,12,12,6,13,11,13,5,5,2,7,2,4,8,7,13,1,16,3,4,10,9,8,14,15,2,17,5,11,10,14,16,11,16,13,13,5,7,5,12,6,6,5,4,0,0,4,10,9,15,4,6,7,6,17,13,4,11,15,9,18,0],
        "U": [9, 18, 0], "C": [8, 8],
        "samples": [[20, 20]], "q_gain": 0, "k_gain": 5,
        "epoch_steps": 120, "epochs": 2,
        "overflow_clock": "1000", "overflow_repeats": 30,
        "require_odd_pair_guard": True,
    }
    claim = ac.normalize_claim(raw, ROOT / "calculation/new_structures/U44/prefix_only.json")
    result = ac.run_sample(claim, 20, 20)
    if result["status"] != "FAIL" or not result["overflow_clock_matches"]:
        raise RuntimeError("prefix-only seam was not correctly rejected")
    endpoints = result["endpoint_returns"]
    if len(endpoints) != 2 or endpoints[0]["first_mismatch"] != 214:
        raise RuntimeError(f"expected full-seam mismatch at index 214, got {endpoints}")
    if result["engine_mismatch_times"] or result["palindrome_times"]:
        raise RuntimeError("prefix-only control's independent engine/guard audit failed")


def test_invalid_template_rejected() -> None:
    lattice = ROOT / "calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt"
    raw = {"base": 10, "lattice": str(lattice), "J": [5], "U": [9, 14, 4], "C": [9]}
    try:
        ac.normalize_claim(raw, ROOT / "bad.json")
    except ac.CheckError:
        return
    raise RuntimeError("unrealizable odd midpoint coefficient was not rejected")


if __name__ == "__main__":
    test_independent_engines()
    test_known_nonreturning_control()
    test_prefix_only_seam_rejected()
    test_invalid_template_rejected()
    print("U44_ALERT_CHECK_TESTS_PASS")
