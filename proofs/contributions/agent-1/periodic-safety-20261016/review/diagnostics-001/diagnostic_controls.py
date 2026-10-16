#!/usr/bin/env python3
"""Selected finite controls for the period-state safety test.

These are diagnostics only. The assigned authors supply all universal and
boundary Lean theorems. No numeral or infinite-orbit interpretation is inferred.
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


def head(xs):
    return xs[0] if xs else 0


def state_test(B, H, w):
    alphabet = B+H+w
    return not (all(x <= 9 for x in alphabet) or
                (head(B+w) == 11 and all(x == 0 or x == 11 for x in alphabet)))


def bad_word(Q):
    # Literal finite interpretation of the two FoldedDecimal.BadWord clauses.
    return (all(Q[i] <= 9 for i in range(len(Q))) or
            (head(Q) == 11 and
             all(Q[i] == 0 or Q[i] == 11 for i in range(len(Q)))))


def strip(B, H, w):
    if not w:
        return (B, H, w), 0, 0
    m = len(w)
    u = v = 0
    while len(B) >= m and B[-m:] == w:
        B = B[:-m]
        u += 1
    while len(H) >= 2*m and H[:m] == w and H[-m:] == w[::-1]:
        H = H[m:-m]
        v += 1
    return (B, H, w), u, v


CASES = [
    ("empty_context_small", (), (), (1, 2, 3, 4)),
    ("empty_context_all_zero", (), (), (0, 0, 0, 0)),
    ("empty_context_all_nine", (), (), (9, 9, 9, 9)),
    ("empty_context_all_ten", (), (), (10, 10, 10, 10)),
    ("empty_context_all_eighteen", (), (), (18, 18, 18, 18)),
    ("eleven_zero_pattern", (11,), (0,), (0, 11, 11, 0)),
    ("eleven_wrong_alphabet", (11,), (1,), (0, 11, 11, 0)),
    ("wrong_outside_for_eleven_pattern", (0,), (), (0, 11, 11, 0)),
    ("original_probe", (17,), (), (0, 9, 18, 9)),
    ("nonsymmetric_unbounded_algebra_only", (25, 0), (2, 19, 7), (18, 0, 1, 4)),
    ("one_symbol_general_period", (), (3,), (11,)),
    ("two_symbol_general_period", (0, 11, 0), (19,), (11, 0)),
]
EXPS = (1, 2, 3, 7)
expansion_results = []
for name, B, H, w in CASES:
    assert w
    expected = state_test(B, H, w)
    assert expected == bool(old.safe((B, H, w))), name
    samples = []
    for k in EXPS:
        Q = old.full((B, H, w), k)
        assert set(Q) == set(B+H+w), (name, k)
        assert head(Q) == head(B+w), (name, k)
        assert expected == (not bad_word(Q)), (name, k)
        samples.append({"k": k, "length": len(Q), "bad_word": bad_word(Q)})
    expansion_results.append({"name": name, "input": (B, H, w),
                              "state_test": expected, "samples": samples})

STRIP_CASES = [
    ("empty_input_with_nonempty_period", (), (), (18,)*4),
    ("complete_nonconstant_blocks", (1, 2, 3, 18)*2,
     (1, 2, 3, 18)*2+(18, 3, 2, 1)*2, (1, 2, 3, 18)),
    ("outside_eleven_removed_completely", (11, 0)*3,
     (11, 0)*2+(0, 11)*2, (11, 0)),
    ("outside_eleven_retained", (11,)+(0,)*8, (0,)*16, (0,)*4),
    ("period_remains_in_alphabet", (18,)*8, (18,)*16, (18,)*4),
    ("constant_short_remainders", (9,)*11, (9,)*19, (9,)*4),
    ("overlapping_center_must_stop", (9,)*3, (9,)*7, (9,)*4),
    ("nonprimitive_period", (7,)+(1, 2)*4, (1, 2)*2+(19,)+(2, 1)*2, (1, 2, 1, 2)),
    ("empty_period_public_convention", (11,), (0, 11, 0), ()),
    ("everything_empty_public_convention", (), (), ()),
]
strip_results = []
for name, B, H, w in STRIP_CASES:
    target, u, v = strip(B, H, w)
    br, hr, _ = target
    assert B == br+w*u, name
    assert H == w*v+hr+w[::-1]*v, name
    assert set(B+H+w) == set(br+hr+w), name
    assert head(B+w) == head(br+w), name
    assert state_test(B, H, w) == state_test(*target), name
    strip_results.append({"name": name, "input": (B, H, w), "target": target,
                          "outer_removed": u, "center_removed": v,
                          "state_test": state_test(*target)})

# Fixed boundary controls explicitly included in the parent's current claim.
k0_state = ((1,), (), (18,)*4)
k0_Q = old.full(k0_state, 0)
assert old.valid(k0_state)
assert state_test(*k0_state) and bad_word(k0_Q)
k0_control = {"input": k0_state, "k": 0, "word": k0_Q,
              "state_test": state_test(*k0_state), "bad_word": bad_word(k0_Q)}

failure_state = ((), (), (10,)*4)
assert old.valid(failure_state) and old.safe(failure_state)
edge = old.transition(failure_state)
expected_target = ((1, 2, 2, 2), (2,), (2, 2, 2, 2))
assert edge["target"] == expected_target
assert edge["kind"] == "unsafe_target" and not state_test(*edge["target"])
assert old.valid(edge["target"])
assert edge["absorbed_outer_periods"] == 0 and edge["absorbed_center_pairs"] == 1
assert edge["clock"] == 1 and edge["exponent_delta"] == -1
failure_control = {"input": failure_state, "edge": edge,
                   "source_test": True, "target_test": False,
                   "target_valid": True,
                   "note": "Finite diagnostic only; boundary theorem authored separately."}

print(json.dumps({
    "status": "PASS",
    "scope": "Finite controls only; universal and fixed-boundary Lean proofs are separate author work",
    "source_sha256": SOURCE_SHA256,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "python": sys.version,
    "positive_exponent_cases": expansion_results,
    "stripping_cases": strip_results,
    "zero_exponent_boundary": k0_control,
    "unsafe_target_boundary": failure_control,
    "positive_case_count": len(expansion_results),
    "positive_expansion_checks": len(expansion_results)*len(EXPS),
    "strip_case_count": len(strip_results),
}, indent=2))
