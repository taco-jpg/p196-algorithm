#!/usr/bin/env python3
"""Bounded independent integer controls of the pinned outer projection bridge.

Formula source: complementary-bulk METHOD_AND_PROOF.md, equations (1),(3)-(8),
and section 6's B-suffix strip. No author implementation is imported or run.
Block normalization uses evaluation/division of integers; actual full-word
updates use decimal string reversal of a canonical positive ordinary integer.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

SOURCE_COMMIT = "b2374410d427beb78fc601ee81cf15e34a1ac934"
PHASES = tuple(range(2, 17, 2))
PROFILES = (
    ("empty", (), ()),
    ("single_neutral_zero_center", (9,), (0,)),
    ("high_low_odd_center", (18, 0), (18, 2, 18)),
    ("mixed_even_center", (0, 9, 18), (0, 18, 18, 0)),
)
PINNED_FILES = (
    "proofs/contributions/2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md",
    "proofs/contributions/agent-109/outer-projection-bridge/OuterBridge.lean",
    "proofs/contributions/agent-109/outer-projection-bridge/OuterCompat.lean",
    "proofs/contributions/agent-109/outer-projection-bridge/agent7-deps/OuterFinite.lean",
    "proofs/contributions/agent-109/outer-projection-bridge/agent7-deps/OuterBounds.lean",
)


def require(test, label, **context):
    if not test:
        raise AssertionError({"check": label, **context})


def little_digits(n):
    require(n > 0, "positive integer", n=str(n))
    return tuple(int(ch) for ch in str(n)[::-1])


def pairword(n):
    ds = little_digits(n)
    return tuple(a + b for a, b in zip(ds, ds[::-1]))


def template(c, B, A, C, g, h):
    require(g >= 0 and h >= 0, "nonnegative target gaps", g=g, h=h)
    d = 18 - c
    return B + (c,) * g + A + (d,) * h + C + (d,) * h + A[::-1] + (c,) * g + B[::-1]


def realize(q):
    """Choose digits explicitly, with a positive most-significant digit."""
    require(q == q[::-1] and q and q[0] > 0, "canonical symmetric q", q=q)
    require(all(0 <= x <= 18 for x in q), "bounded pair coefficients", q=q)
    ds = [0] * len(q)
    for i in range(len(q) // 2):
        # The larger digit goes on the most significant side, including i=0.
        ds[-1-i] = min(9, q[i])
        ds[i] = q[i] - ds[-1-i]
    if len(q) % 2:
        mid = len(q) // 2
        require(q[mid] % 2 == 0, "even central pair coefficient", q=q)
        ds[mid] = q[mid] // 2
    require(ds[-1] > 0 and all(0 <= x <= 9 for x in ds), "canonical digit realization", digits=ds)
    n = int("".join(str(x) for x in ds[::-1]))
    require(len(str(n)) == len(q), "exact initial width", n=str(n), q=q)
    require(pairword(n) == q, "exact initial pairword", n=str(n), q=q)
    return n


def normalize_block(word, incoming):
    """Independent normalizer: evaluate once, then divide by the block place."""
    value = incoming + sum(x * 10**i for i, x in enumerate(word))
    final, retained = divmod(value, 10 ** len(word))
    ds = tuple((retained // 10**i) % 10 for i in range(len(word)))
    require(final in (0, 1), "block carry bit", word=word, incoming=incoming, final=final)
    return ds, final


def add_words(left, right):
    require(len(left) == len(right), "coordinate sum length", left=left, right=right)
    return tuple(a + b for a, b in zip(left, right))


def strip_suffix(word, letter):
    i = len(word)
    while i and word[i-1] == letter:
        i -= 1
    return word[:i], len(word)-i


def outer_formula(c, B):
    """Written (6)/(7) outer row alone; no A,C,g,h input."""
    k = int(c >= 10)
    t = c - 9*k
    DB, e0 = normalize_block(B, 0)
    DRB, gamma = normalize_block(B[::-1], k)
    other = (1,) + DRB[::-1] if gamma else DRB[::-1] + (t,)
    raw = add_words(DB + (c+e0-10*k,), other)
    stripped, count = strip_suffix(raw, 2*t)
    return 2*t, stripped, gamma, raw, count


def full_formula(c, B, A, C, g, h):
    """Written (3)-(8), then only the B strip used by OuterBridge."""
    require(g >= 2 and h >= 2, "source gap domain", g=g, h=h)
    d = 18-c
    kc, kd = int(c >= 10), int(d >= 10)
    tc, td = c-9*kc, d-9*kd
    DB, e0 = normalize_block(B, 0)
    DA, e1 = normalize_block(A, kc)
    DC, e2 = normalize_block(C, kd)
    DRA, e3 = normalize_block(A[::-1], kd)
    DRB, gamma = normalize_block(B[::-1], kc)
    u0, u1, u2, u3 = c+e0-10*kc, d+e1-10*kd, d+e2-10*kd, c+e3-10*kc
    digit_word = (DB + (u0,) + (tc,)*(g-1) + DA + (u1,) + (td,)*(h-1)
                  + DC + (u2,) + (td,)*(h-1) + DRA + (u3,) + (tc,)*(g-1)
                  + DRB + ((1,) if gamma else ()))
    if gamma:
        Br = add_words(DB+(u0,), (1,)+DRB[::-1])
        Ar = add_words(DA+(u1,), (u3,)+DRA[::-1])
        middle = DC+(u2,)
    else:
        Br = add_words(DB+(u0,), DRB[::-1]+(tc,))
        Ar = add_words((tc,)+DA+(u1,), (u3,)+DRA[::-1]+(td,))
        middle = (td,)+DC+(u2,)
    Cr = add_words(middle, middle[::-1])
    Bnext, removed = strip_suffix(Br, 2*tc)
    return (2*tc, Bnext, Ar, Cr, g-2+gamma+removed, h-2+gamma), gamma, digit_word, Br


def initial_exteriors(c):
    yield ()
    for a in range(1, 19):
        if a != c:
            yield (a,)
        for b in range(19):
            if b != c:
                yield (a, b)


def stable_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def run(source_root, output):
    output.mkdir(parents=True, exist_ok=True)
    pins = {}
    for name in PINNED_FILES:
        raw = (source_root/name).read_bytes()
        pins[name] = {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
    counts = Counter()
    exit_hist = Counter()
    per_profile = Counter()
    per_phase = Counter()
    stage_hist = Counter()
    transcript_hash = hashlib.sha256()
    failures = []
    samples = []
    min_bands = [None] * 8
    trajectory_path = output/"trajectories.jsonl.gz"
    with trajectory_path.open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as trace:
            for c0 in PHASES:
                for B0 in initial_exteriors(c0):
                    counts["initial_outer_states"] += 1
                    for profile, A0, C0 in PROFILES:
                        identifier = {"phase": c0, "B": B0, "profile": profile}
                        try:
                            state = (c0, B0, A0, C0, 14, 14)
                            n = realize(template(*state))
                            counts["canonical_realizations"] += 1
                            counts["initial_even_width" if len(str(n)) % 2 == 0 else "initial_odd_width"] += 1
                            counts["initial_zero_units_digit"] += int(n % 10 == 0)
                            records = []
                            outer_c, outer_B = c0, B0
                            first_exit = None
                            for time in range(8):
                                c, B, A, C, g, h = state
                                require((c, B) == (outer_c, outer_B), "iterate outer coordinate", time=time)
                                require(pairword(n) == template(*state), "actual full template identity", time=time)
                                require(c in PHASES, "phase domain", c=c, time=time)
                                require(all(0 <= x <= 18 for x in B+A+C), "bounded successor blocks", time=time)
                                require(C == C[::-1], "symmetric center", time=time)
                                require(not len(C) % 2 or C[len(C)//2] % 2 == 0, "even middle coefficient", time=time)
                                require(not B or (B[0] > 0 and B[-1] != c), "trimmed positive exterior", time=time)
                                require(g + 2*time >= 14 and h + 2*time >= 14, "finite band budgets", time=time, g=g, h=h)
                                if first_exit is None and len(B) > 2:
                                    first_exit = time
                                min_bands[time] = min(g, h) if min_bands[time] is None else min(min_bands[time], g, h)
                                stage_hist[str(time)] += 1
                                records.append({"time":time,"n":str(n),"c":c,"B":B,"A":A,"C":C,"g":g,"h":h})
                                if time == 7:
                                    break
                                nnext = n + int(str(n)[::-1])
                                next_state, gamma, ds, Br = full_formula(*state)
                                oc, ob, ogamma, oraw, removed = outer_formula(outer_c, outer_B)
                                require(ds == little_digits(nnext), "actual canonical output digits (5)", time=time)
                                require(len(str(nnext)) == len(str(n)) + gamma, "actual physical width", time=time)
                                require(Br == oraw and gamma == ogamma, "outer independence from A,C", time=time)
                                require(pairword(nnext)[:len(Br)] == Br, "actual raw outer prefix", time=time)
                                require(next_state[:2] == (oc,ob), "exact outer formula", time=time)
                                require(pairword(nnext) == template(*next_state), "actual next template (8) with B strip", time=time)
                                counts["overflow_transitions" if gamma else "nonoverflow_transitions"] += 1
                                counts["empty_target_exteriors"] += int(not ob)
                                counts["positive_B_strips"] += int(removed > 0)
                                counts["transitions"] += 1
                                counts["zero_units_input_transitions"] += int(n % 10 == 0)
                                n, state, outer_c, outer_B = nnext, next_state, oc, ob
                            require(first_exit is not None and 1 <= first_exit <= 7, "exit within seven", first_exit=first_exit)
                            row = {"initial":identifier,"first_exit":first_exit,"stages":records}
                            line = (stable_json(row)+"\n").encode()
                            transcript_hash.update(line)
                            trace.write(line)
                            counts["trajectories"] += 1
                            exit_hist[str(first_exit)] += 1
                            per_profile[profile] += 1
                            per_phase[str(c0)] += 1
                            if (B0 == () and profile == "empty") or (c0 == 14 and B0 == (2,17) and profile == "empty"):
                                samples.append(row)
                        except Exception as error:
                            failure = {"initial":identifier,"error_type":type(error).__name__,
                                       "detail":str(error),"last_state":state,"last_n":str(n)}
                            failures.append(failure)
                            # Preserve a concrete failed trajectory and stop: no long retry sweep.
                            raise RuntimeError(stable_json(failure)) from error
    expected_states = 8*(1+17+18*18)
    require(counts["initial_outer_states"] == expected_states, "complete finite exterior count")
    require(counts["trajectories"] == expected_states*len(PROFILES), "complete configured trajectory count")
    require(counts["transitions"] == counts["trajectories"]*7, "all seven updates performed")
    require(counts["trajectories"] < 100000, "bounded trajectory budget")
    (output/"failures.json").write_text(json.dumps(failures,indent=2)+"\n")
    (output/"sample_trajectories.json").write_text(json.dumps(samples,indent=2)+"\n")
    report = {
        "status":"PASS", "kind":"INDEPENDENT_BOUNDED_EXACT_INTEGER_CONTROLS",
        "source_commit":SOURCE_COMMIT, "source_files":pins,
        "written_formula_scope":"METHOD_AND_PROOF.md equations (1),(3)-(8), then B suffix strip only; A and C retain raw values to match OuterBridge",
        "method":"Independent Python from written formulas; integer-value block normalization; actual n+int(str(n)[::-1]); no author implementation imported, no Lean execution",
        "python":sys.version, "randomness":"none", "initial_g":14, "initial_h":14,
        "phases":PHASES,"profiles":[{"name":name,"A":A,"C":C} for name,A,C in PROFILES],
        "counts":dict(sorted(counts.items())), "first_exit_histogram":dict(sorted(exit_hist.items())),
        "trajectories_per_phase":dict(sorted(per_phase.items())), "trajectories_per_profile":dict(sorted(per_profile.items())),
        "stages":dict(sorted(stage_hist.items())), "minimum_observed_band_at_each_time":min_bands,
        "failures":0,"uncompressed_trajectory_sha256":transcript_hash.hexdigest(),
        "trajectory_gzip_sha256":hashlib.sha256(trajectory_path.read_bytes()).hexdigest(),
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "limits":["Finite controls, not a new theorem or substitute for source semantics/kernel review.",
                  "All cap<=2 valid exteriors and eight even phases, but only four fixed interface/center choices and one explicit canonical realization per initial template.",
                  "Seven updates only, beginning at g=h=14; no arbitrary-gap all-time conclusion.",
                  "Exit concerns the constructed maximally B-trimmed template coordinate; no uniqueness across all possible decompositions asserted.",
                  "No palindrome-avoidance, nontermination, cycle, larger-cap exclusion, or P196 conclusion."]}
    (output/"report.json").write_text(json.dumps(report,indent=2)+"\n")
    return report


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--source-root",type=Path,required=True)
    parser.add_argument("--output",type=Path,default=Path(__file__).resolve().parent)
    args=parser.parse_args()
    try:
        report=run(args.source_root.resolve(),args.output.resolve())
        print(json.dumps({"status":report["status"],"counts":report["counts"],"first_exit_histogram":report["first_exit_histogram"]},indent=2))
    except Exception as error:
        args.output.mkdir(parents=True,exist_ok=True)
        failure={"status":"FAIL","error_type":type(error).__name__,"detail":str(error)}
        (args.output/"failures.json").write_text(json.dumps([failure],indent=2)+"\n")
        print(json.dumps(failure,indent=2))
        raise
