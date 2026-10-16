#!/usr/bin/env python3
"""Finite diagnostic controls for the preserved block-removal loops.

This checks selected finite lists and exponents. It is neither a Lean proof
nor an all-state search, a canonical-numeral bridge, or an iteration claim.
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


def literal_loops(B, H, W):
    """The two original transition loops, with explicit length-four domain."""
    assert len(W) == 4
    B, H, W = tuple(B), tuple(H), tuple(W)
    u = v = 0
    while len(B) >= 4 and B[-4:] == W:
        B = B[:-4]
        u += 1
    while len(H) >= 8 and H[:4] == W and H[-4:] == W[::-1]:
        H = H[4:-4]
        v += 1
    return B, H, u, v


def finite_spec(B, H, W):
    """Independent finite enumeration of admissible total removal counts."""
    assert len(W) == 4
    outer = [u for u in range(len(B) // 4 + 1)
             if B == B[:len(B)-4*u] + W*u]
    center = [v for v in range(len(H) // 8 + 1)
              if H == W*v + H[4*v:len(H)-4*v] + W[::-1]*v]
    u, v = max(outer), max(center)
    return B[:len(B)-4*u], H[4*v:len(H)-4*v], u, v


def check_loops(name, B, H, W, expected=None):
    B, H, W = tuple(B), tuple(H), tuple(W)
    result = literal_loops(B, H, W)
    assert result == finite_spec(B, H, W), name
    if expected is not None:
        assert result == expected, (name, result, expected)
    br, hr, u, v = result
    assert B == br + W*u, name
    assert H == W*v + hr + W[::-1]*v, name
    assert len(br) < 4 or br[-4:] != W, name
    assert len(hr) < 8 or hr[:4] != W or hr[-4:] != W[::-1], name
    assert literal_loops(br, hr, W) == (br, hr, 0, 0), name
    for j in (0, 1, 2, 3, 7):
        assert old.full((B, H, W), j) == old.full((br, hr, W), j+u+v), (name, j)
    return {"name": name, "B": B, "H": H, "W": W,
            "outer_remainder": br, "center_remainder": hr,
            "outer_count": u, "center_count": v}


W = (1, 2, 3, 4)
N = (9, 9, 9, 9)
P = (1, 2, 1, 2)
GENERIC_CASES = [
    ("both_empty", (), (), W, ((), (), 0, 0)),
    ("short_exterior_and_center", (7, 8, 9), (6, 5, 6), W,
     ((7, 8, 9), (6, 5, 6), 0, 0)),
    ("exact_nonconstant_blocks", W*3, W*2+W[::-1]*2, W, ((), (), 3, 2)),
    ("nonconstant_short_residuals", (7,)+W*2, W*2+(8, 6, 8)+W[::-1]*2, W,
     ((7,), (8, 6, 8), 2, 2)),
    ("whole_block_suffix_mismatch", W+(1, 2, 3, 5), W+(7,)+W, W,
     (W+(1, 2, 3, 5), W+(7,)+W, 0, 0)),
    ("constant_overlap_seven_columns", N+(9, 9, 9), (9,)*7, N,
     ((9, 9, 9), (9,)*7, 1, 0)),
    ("constant_exact_pair", N*2, N*2, N, ((), (), 2, 1)),
    ("constant_residual_three_columns", (9,)*11, (9,)*19, N,
     ((9, 9, 9), (9, 9, 9), 2, 2)),
    ("nonprimitive_period", (7, 8)+P*3, P*3+(6,)+P[::-1]*3, P,
     ((7, 8), (6,), 3, 3)),
    ("zero_period_empty_residuals", (0,)*8, (0,)*16, (0,)*4, ((), (), 2, 2)),
    ("center_prefix_only", (6,), W+(5,)+(4, 3, 2, 0), W,
     ((6,), W+(5,)+(4, 3, 2, 0), 0, 0)),
    ("palindromic_period", (1, 2, 2, 1)*2, (1, 2, 2, 1)*3,
     (1, 2, 2, 1), ((), (1, 2, 2, 1), 2, 1)),
]
generic_results = [check_loops(*case) for case in GENERIC_CASES]

ACTUAL_CASES = [
    ("empty_context_zero", (), (), (0, 0, 0, 0)),
    ("empty_context_all_nine", (), (), (9, 9, 9, 9)),
    ("empty_context_all_eighteen", (), (), (18, 18, 18, 18)),
    ("empty_context_nonconstant", (), (), (1, 2, 3, 4)),
    ("empty_outer_even_single_center", (), (8,), (1, 2, 1, 2)),
    ("asymmetric_center_bounded_only", (7,), (1, 4, 8), (0, 9, 18, 9)),
    ("odd_center_not_realizable", (7,), (1,), (9, 9, 9, 9)),
    ("nonpositive_outside_bounded_only", (0,), (0, 8, 0), (0, 0, 0, 0)),
    ("original_probe_empty_center", (17,), (), (0, 9, 18, 9)),
    ("original_probe_zero_center", (17,), (0,), (0, 9, 18, 9)),
    ("original_probe_eighteen_center", (17,), (18,), (0, 9, 18, 9)),
    ("long_context_with_zeros", (18, 0, 7, 0, 8), (6, 0, 0, 6), (18, 0, 0, 18)),
    ("all_nine_transient_low", (1,), (8, 8), (9, 9, 9, 9)),
    ("all_nine_transient_high", (18,), (8, 8), (9, 9, 9, 9)),
]
EXPONENTS = (3, 4, 5, 7, 12)
actual_results = []
for name, B, H, w in ACTUAL_CASES:
    state = (B, H, w)
    out3, gamma = old.image(old.full(state, 3))
    b, h = len(B), len(H)
    br = out3[:b+4]
    rw = out3[b+4:b+8]
    hr = out3[b+8:b+h+16+gamma]
    assert (len(br), len(rw), len(hr)) == (b+4, 4, h+8+gamma), name
    assert out3 == old.full((br, hr, rw), 1), name
    record = check_loops(name, br, hr, rw)
    B1, H1, u, v = literal_loops(br, hr, rw)
    delta = u+v-2
    assert 2*len(B1)+len(H1)+8*delta == 2*b+h+gamma, name
    samples = []
    for k in EXPONENTS:
        out, g = old.image(old.full(state, k))
        exponent = (k-2)+u+v
        assert g == gamma, (name, k)
        assert out == old.full((br, hr, rw), k-2), (name, k)
        assert out == old.full((B1, H1, rw), exponent), (name, k)
        samples.append({"k": k, "target_exponent": exponent, "output_length": len(out)})
    valid = old.valid(state)
    safe = old.safe(state)
    # The preserved public transition has a narrower valid-and-safe domain.
    if valid and safe:
        edge = old.transition(state)
        assert edge["target"] == (B1, H1, rw), name
        assert edge["exponent_delta"] == delta and edge["clock"] == gamma, name
    record.update(input_state=state, input_valid=valid, input_safe=safe,
                  raw_gamma=gamma, signed_delta=delta, samples=samples,
                  original_transition_checked=bool(valid and safe))
    actual_results.append(record)

summary = {
    "status": "PASS",
    "scope": "Finite diagnostic controls only; no universal proof, numeral realization or iterated guard-domain closure",
    "source_relative_path": str(SOURCE.relative_to(ROOT)),
    "source_sha256": SOURCE_SHA256,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "python": sys.version,
    "generic_cases": generic_results,
    "actual_raw_cases": actual_results,
    "generic_case_count": len(generic_results),
    "actual_case_count": len(actual_results),
    "actual_exponent_checks": len(actual_results)*len(EXPONENTS),
    "carry_cases_observed": sorted({r["raw_gamma"] for r in actual_results}),
    "signed_deltas_observed": sorted({r["signed_delta"] for r in actual_results}),
    "minimum_target_exponent_observed": min(s["target_exponent"] for r in actual_results for s in r["samples"]),
    "original_transition_checks": sum(r["original_transition_checked"] for r in actual_results),
}
print(json.dumps(summary, indent=2))
