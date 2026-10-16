#!/usr/bin/env python3
"""Exact literal controls for the written collision safety corollary.

These four examples are controls and scope witnesses, not an
enumeration proving the unrestricted theorem.
"""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def digits(n):
    return [int(c) for c in str(n)[::-1]]


def pair(ds):
    return [a + b for a, b in zip(ds, reversed(ds))]


def normalize(q, incoming=0):
    c = incoming
    ds = []
    for a in q:
        c, d = divmod(a + c, 10)
        ds.append(d)
    return ds + ([c] if c else []), c


def prefix9(q):
    k = 0
    for a in q:
        if a != 9:
            break
        k += 1
    return k


def canonical(q):
    return (q == q[::-1] and q[0] > 0 and
            all(0 <= a <= 18 for a in q) and
            (len(q) % 2 == 0 or q[len(q) // 2] % 2 == 0))


def trim(q):
    q = list(q)
    while q and q[-1] == 0:
        q.pop()
    return q


def check(seed, b, h, expected_step, expected_active, expected_closure,
          expected_palindrome=False, canonical_core=True):
    q = b + h + b
    assert canonical(b) and canonical(q)
    assert canonical(h) == canonical_core
    assert pair(digits(seed)) == q
    step = seed + int(str(seed)[::-1])
    assert step == expected_step
    actual_digits, final = normalize(q)
    assert actual_digits == digits(step)
    actual = pair(actual_digits)
    bd, e = normalize(b)
    hd, a = normalize(h)
    _, carry_h = normalize(h, e)
    gb, gh = pair(bd), pair(hd)
    target = [0] * (len(q) + 2)
    for word, offset in ((gb, 0), (gh, len(b)), (gb, len(b) + len(h))):
        for i, v in enumerate(word):
            target[offset + i] += v
    target = trim(target)
    f = [0] * (len(q) + 1)
    for offset, length, c in ((len(b), prefix9(h), e),
                              (len(b) + len(h), prefix9(b), carry_h)):
        for i in range(length):
            f[offset + i] += c
    f = trim(f)
    active = any(f)
    closure = actual == target
    pal = str(step) == str(step)[::-1]
    assert active == expected_active and closure == expected_closure
    assert pal == expected_palindrome
    if canonical_core:
        assert closure == (not active and e == a)
        assert not (active or e != a) or not pal
    return {"seed": seed, "next": step, "B": b, "H": h,
            "canonical_core": canonical_core,
            "pair_word": q, "G_actual": actual, "S_independent": target,
            "isolated_B_overflow": e, "isolated_H_overflow": a,
            "actual_H_outgoing": carry_h, "actual_final_overflow": final,
            "F_coefficients": f, "active_seam": active,
            "independent_closure": closure, "next_is_palindrome": pal,
            "actual_pair_mass": sum(actual), "independent_pair_mass": sum(target)}


records = [
    check(22900, [2, 2], [18], 23822, False, False),
    check(99900, [9, 9], [18], 100899, True, False),
    check(1115000, [1, 1], [1, 10, 1], 1120111, False, True),
    check(99022, [11, 11], [0], 121121, False, True,
          expected_palindrome=True, canonical_core=False),
]
assert records[0]["G_actual"] == [4, 5, 16, 5, 4]
assert records[0]["S_independent"] == [4, 4, 9, 13, 4]
assert records[0]["actual_pair_mass"] == records[0]["independent_pair_mass"] == 34
assert records[3]["isolated_B_overflow"] != records[3]["isolated_H_overflow"]
result = {"status": "PASS", "scope": "Three exact in-domain controls and one excluded-domain counterexample; unrestricted proof is written separately",
          "main_existence_proved": False, "records": records}
(HERE / "collision_safety_examples.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": "PASS", "controls": len(records)}))
