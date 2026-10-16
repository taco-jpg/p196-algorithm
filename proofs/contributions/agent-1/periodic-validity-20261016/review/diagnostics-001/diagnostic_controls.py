#!/usr/bin/env python3
"""Finite diagnostics for strict original periodic-state validity.

No universal proof, safety preservation, numerical realization, or iteration
claim is made by these selected controls. The source algorithms are pinned.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / "proofs/periodic_word_quotient__8404d0a63dd1fa13.py"
SOURCE_SHA256 = "122fcd390283f956f97d21327ec6cb9d4ae193e9bd3ab1b155bb65e1e61c2425"
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256
spec = importlib.util.spec_from_file_location("preserved_periodic_quotient", SOURCE)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def fields(state):
    B, H, w = state
    return {
        "outer_bounded": all(0 <= a <= 18 for a in B),
        "center_bounded": all(0 <= a <= 18 for a in H),
        "period_bounded": all(0 <= a <= 18 for a in w),
        "period_length": len(w) == 4,
        "center_symmetric": H[::-1] == H,
        "center_even": len(H) % 2 == 0 or H[len(H)//2] % 2 == 0,
        "outside_positive": bool(B+w) and (B+w)[0] > 0,
    }


def check_predicate(state):
    fs = fields(state)
    assert all(fs.values()) == bool(old.valid(state)), (state, fs)
    return fs


def strip(B, H, w):
    u = v = 0
    while len(B) >= 4 and B[-4:] == w:
        B = B[:-4]
        u += 1
    while len(H) >= 8 and H[:4] == w and H[-4:] == w[::-1]:
        H = H[4:-4]
        v += 1
    return (B, H, w), u, v


VALID_CASES = [
    ("empty_context_all_one_unsafe", (), (), (1, 1, 1, 1)),
    ("empty_context_all_nine_unsafe", (), (), (9, 9, 9, 9)),
    ("empty_context_all_eighteen", (), (), (18, 18, 18, 18)),
    ("empty_outer_nonconstant_even_center", (), (8,), (1, 2, 3, 4)),
    ("empty_outer_nonprimitive_empty_center", (), (), (1, 2, 1, 2)),
    ("positive_outer_zero_period", (1,), (), (0, 0, 0, 0)),
    ("positive_outer_all_eleven_unsafe", (11,), (0,), (11, 11, 11, 11)),
    ("original_probe_empty_center", (17,), (), (0, 9, 18, 9)),
    ("original_probe_zero_center", (17,), (0,), (0, 9, 18, 9)),
    ("original_probe_eighteen_center", (17,), (18,), (0, 9, 18, 9)),
    ("nine_exterior_no_overflow", (9,), (), (0, 0, 0, 0)),
    ("nine_exterior_carry_displacement", (9,), (18,), (18, 18, 18, 18)),
    ("ten_exterior_leading_digit_zero", (10,), (), (0, 0, 0, 0)),
    ("eighteen_exterior_empty_center", (18,), (), (9, 9, 9, 9)),
    ("odd_center_even_middle", (2, 0), (3, 8, 3), (18, 0, 9, 1)),
    ("even_center_odd_coefficients", (3, 0, 7), (1, 3, 3, 1), (2, 9, 18, 0)),
]
INVALID_CASES = [
    ("odd_single_center", (), (1,), (1, 2, 3, 4), "center_even"),
    ("odd_middle_long_center", (1,), (2, 1, 2), (1, 2, 3, 4), "center_even"),
    ("nonsymmetric_even_center", (1,), (2, 4), (1, 2, 3, 4), "center_symmetric"),
    ("zero_outer_with_positive_period", (0,), (), (1, 2, 3, 4), "outside_positive"),
    ("empty_outer_zero_period_head", (), (), (0, 9, 18, 9), "outside_positive"),
    ("outer_coefficient_nineteen", (19,), (), (1, 2, 3, 4), "outer_bounded"),
    ("center_coefficient_nineteen", (1,), (19, 19), (1, 2, 3, 4), "center_bounded"),
    ("period_coefficient_nineteen", (1,), (), (1, 2, 19, 4), "period_bounded"),
    ("three_symbol_period", (1,), (), (1, 2, 3), "period_length"),
    ("empty_period_with_positive_outer", (1,), (), (), "period_length"),
]

valid_results = []
for name, B, H, w in VALID_CASES:
    source = (B, H, w)
    assert all(check_predicate(source).values()), name
    # Input canonical-pair shape at exponent one is distinct from applying the
    # raw guard, whose actual transition checks below only use k >= 3.
    word1 = old.full(source, 1)
    assert word1 and word1 == word1[::-1] and word1[0] > 0, name
    assert all(0 <= x <= 18 for x in word1), name
    image3, gamma = old.image(old.full(source, 3))
    b, h = len(B), len(H)
    raw = (image3[:b+4], image3[b+8:b+h+16+gamma], image3[b+4:b+8])
    raw_fields = check_predicate(raw)
    assert all(raw_fields.values()), (name, "raw", raw_fields)
    target, u, v = strip(*raw)
    target_fields = check_predicate(target)
    assert all(target_fields.values()), (name, "quotient", target_fields)
    samples = []
    for k in (3, 4, 7):
        output, carry = old.image(old.full(source, k))
        new_k = (k-2)+u+v
        assert carry == gamma and new_k >= 1, (name, k)
        assert output == old.full(target, new_k), (name, k)
        samples.append({"k": k, "target_exponent": new_k})
    valid_results.append({
        "name": name, "input": source, "input_safe": old.safe(source),
        "raw": raw, "raw_fields": raw_fields, "gamma": gamma,
        "target": target, "target_fields": target_fields,
        "outer_removed": u, "center_removed": v, "samples": samples,
    })

invalid_results = []
for name, B, H, w, rejected_field in INVALID_CASES:
    state = (B, H, w)
    fs = check_predicate(state)
    assert not fs[rejected_field] and not all(fs.values()), name
    invalid_results.append({"name": name, "input": state, "fields": fs,
                            "expected_rejected_field": rejected_field})

assert {r["gamma"] for r in valid_results} == {0, 1}
assert any(not r["input_safe"] for r in valid_results)
assert any(not r["target"][0] for r in valid_results)
assert any(not r["target"][1] for r in valid_results)

result = {
    "status": "PASS",
    "scope": "Selected finite strict-validity diagnostics only; no safe closure or iteration claim",
    "source_sha256": SOURCE_SHA256,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "python": sys.version,
    "valid_cases": valid_results,
    "invalid_input_controls": invalid_results,
    "valid_case_count": len(valid_results),
    "invalid_input_count": len(invalid_results),
    "actual_transition_checks": len(valid_results)*3,
    "valid_but_unsafe_input_count": sum(not r["input_safe"] for r in valid_results),
    "carry_values": sorted({r["gamma"] for r in valid_results}),
    "empty_quotient_outer_count": sum(not r["target"][0] for r in valid_results),
    "empty_quotient_center_count": sum(not r["target"][1] for r in valid_results),
    "minimum_target_exponent_observed": min(s["target_exponent"] for r in valid_results for s in r["samples"]),
}
print(json.dumps(result, indent=2))
