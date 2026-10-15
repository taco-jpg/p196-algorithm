#!/usr/bin/env python3
"""Finite controls for exact complementary-bulk block identities.

This is a formula audit, not a graph/cycle search. Every displayed source
is realized as an ordinary integer and its actual reverse-and-add output
is compared with both the raw and trimmed symbolic block formulas.
"""

from __future__ import annotations

import gzip
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHASES = tuple(c for c in range(1, 18) if c != 9)
B_CASES = ((), (1,), (9,), (18,), (2, 9), (9, 0), (18, 8))
A_CASES = ((), (0,), (9,), (18,), (4, 14), (9, 9), (2, 16))
C_CASES = ((), (0,), (8,), (18,), (0, 0), (9, 9), (0, 8, 0), (18, 0, 18))
GAPS = ((2, 2), (2, 3), (3, 2), (5, 7), (31, 32))


def F(c):
    return 2*c if c < 9 else 2*c-18


def normalize(block, incoming=0):
    ds, carry = [], incoming
    for a in block:
        carry, digit = divmod(a+carry, 10)
        assert carry in (0, 1)
        ds.append(digit)
    return tuple(ds), carry


def add(xs, ys):
    assert len(xs) == len(ys)
    return tuple(x+y for x, y in zip(xs, ys))


def pair(ds):
    return add(ds, ds[::-1])


def assemble(c, blocks, g, h):
    B, A, C = blocks
    d = 18-c
    assert g >= 0 and h >= 0
    return B+(c,)*g+A+(d,)*h+C+(d,)*h+A[::-1]+(c,)*g+B[::-1]


def symbolic(c, blocks):
    B, A, C = blocks
    d = 18-c
    kc, kd = int(c >= 10), int(d >= 10)
    tc, td = c-9*kc, d-9*kd
    assert kc+kd == 1 and tc+td == 9
    DB, e0 = normalize(B)
    DA, e1 = normalize(A, kc)
    DC, e2 = normalize(C, kd)
    DRA, e3 = normalize(A[::-1], kd)
    DRB, gamma = normalize(B[::-1], kc)
    u0, u1 = c+e0-10*kc, d+e1-10*kd
    u2, u3 = d+e2-10*kd, c+e3-10*kc
    if gamma == 0:
        RB = add(DB+(u0,), DRB[::-1]+(tc,))
        RA = add((tc,)+DA+(u1,), (u3,)+DRA[::-1]+(td,))
        RC = pair((td,)+DC+(u2,))
    else:
        RB = add(DB+(u0,), (1,)+DRB[::-1])
        RA = add(DA+(u1,), (u3,)+DRA[::-1])
        RC = pair(DC+(u2,))
    cp, dp = F(c), F(d)
    assert cp+dp == 18 and cp != dp and cp in PHASES and dp in PHASES
    uB = 0
    while uB < len(RB) and RB[-1-uB] == cp:
        uB += 1
    vA = 0
    while vA < len(RA) and RA[vA] == cp:
        vA += 1
    right = len(RA)
    while right > vA and RA[right-1] == dp:
        right -= 1
    uA = len(RA)-right
    vC = 0
    while 2*vC+1 < len(RC) and RC[vC] == dp and RC[-1-vC] == dp:
        vC += 1
    target = (RB[:len(RB)-uB], RA[vA:right], RC[vC:len(RC)-vC])
    dg, dh = uB+vA-2+gamma, uA+vC-2+gamma
    assert len(RB) == len(B)+1
    assert len(RA) == len(A)+2-gamma
    assert len(RC) == len(C)+2-gamma
    assert 2*len(target[0])+2*len(target[1])+len(target[2])+2*dg+2*dh == \
        2*len(B)+2*len(A)+len(C)+gamma
    assert not target[0] or (target[0][0] > 0 and target[0][-1] != cp)
    assert not target[1] or (target[1][0] != cp and target[1][-1] != dp)
    assert target[2] == target[2][::-1]
    assert len(target[2]) < 2 or target[2][0] != dp
    assert len(target[2]) % 2 == 0 or target[2][len(target[2])//2] % 2 == 0
    assert all(0 <= x <= 18 for part in target for x in part)
    return dict(next_phase=cp, gamma=gamma, digit_blocks=(DB, DA, DC, DRA, DRB),
                entrance_digits=(u0, u1, u2, u3), interior_digits=(tc, td),
                raw=(RB, RA, RC), target=target, gap_delta=(dg, dh),
                trim_counts=(uB, vA, uA, vC))


def value(ds):
    n = 0
    for digit in reversed(ds):
        n = 10*n+digit
    return n


def digits(n):
    result = []
    while n:
        n, digit = divmod(n, 10)
        result.append(digit)
    return tuple(result or [0])


def realize(q):
    assert q and q == q[::-1] and q[0] > 0
    ds = [0]*len(q)
    for i in range(len(q)//2):
        ds[-1-i] = min(9, q[i])
        ds[i] = q[i]-ds[-1-i]
    if len(q) % 2:
        assert q[len(q)//2] % 2 == 0
        ds[len(q)//2] = q[len(q)//2]//2
    assert ds[-1] > 0 and all(0 <= d <= 9 for d in ds)
    assert pair(tuple(ds)) == q
    return value(ds)


def main():
    assert [F(c) for c in (2, 4, 8, 16, 14, 10)] == [4, 8, 16, 14, 10, 2]
    assert [F(c) for c in (6, 12)] == [12, 6]
    records = []
    controls = overflows = retained = 0
    empty_targets = [0, 0, 0]
    for c, B, A, C in itertools.product(PHASES, B_CASES, A_CASES, C_CASES):
        blocks = (B, A, C)
        data = symbolic(c, blocks)
        tests = []
        gamma = data["gamma"]
        DB, DA, DC, DRA, DRB = data["digit_blocks"]
        u0, u1, u2, u3 = data["entrance_digits"]
        tc, td = data["interior_digits"]
        for g, h in GAPS:
            q = assemble(c, blocks, g, h)
            n = realize(q)
            out = n+int(str(n)[::-1])
            actual_digits = digits(out)
            predicted_digits = DB+(u0,)+(tc,)*(g-1)+DA+(u1,)+(td,)*(h-1)+DC+\
                (u2,)+(td,)*(h-1)+DRA+(u3,)+(tc,)*(g-1)+DRB+((1,) if gamma else ())
            assert value(q) == out
            assert actual_digits == predicted_digits
            actual = pair(actual_digits)
            assert actual == assemble(data["next_phase"], data["raw"], g-2+gamma, h-2+gamma)
            gp, hp = g+data["gap_delta"][0], h+data["gap_delta"][1]
            assert actual == assemble(data["next_phase"], data["target"], gp, hp)
            assert str(out) != str(out)[::-1]
            assert len(actual) == len(q)+gamma
            controls += 1
            overflows += gamma
            retained += gp >= 2 and hp >= 2
            tests.append(dict(gaps=(g, h), target_gaps=(gp, hp), source_pair_word=q,
                              actual_output_pair_word=actual, ordinary_seed=str(n),
                              actual_output=str(out)))
        for i, part in enumerate(data["target"]):
            empty_targets[i] += not part
        records.append(dict(phase=c, blocks=blocks, symbolic=data, controls=tests))
    raw = (json.dumps(records, separators=(",", ":"))+"\n").encode()
    packed = gzip.compress(raw, mtime=0)
    (HERE/"formula_controls.json.gz").write_bytes(packed)
    report = dict(result="PASS", scope="Formula controls only; no cycle or reachable-graph search.",
                  states=len(records), integer_controls=controls, overflow_controls=overflows,
                  controls_with_both_target_gaps_at_least_two=retained,
                  empty_target_B_A_C_counts=empty_targets, phases=PHASES, gaps=GAPS,
                  B_cases=B_CASES, A_cases=A_CASES, C_cases=C_CASES,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  stored_path="formula_controls.json.gz", compressed_bytes=len(packed),
                  compressed_sha256=hashlib.sha256(packed).hexdigest(),
                  original_path="formula_controls.json", original_bytes=len(raw),
                  original_sha256=hashlib.sha256(raw).hexdigest(),
                  recovery="gzip -dc formula_controls.json.gz > formula_controls.json")
    (HERE/"verification.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k: report[k] for k in ("result", "states", "integer_controls", "overflow_controls")}))


if __name__ == "__main__":
    main()
