#!/usr/bin/env python3
"""Independent integer-arithmetic audit for the Agent 118 center search.

No transition code is imported from cauto or the repository mirror.  A finite
brute-force check concerns its stated initial width only; it is not an all-width
negative.  The Lean source is read solely for pre-existing positive witnesses.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import itertools
from pathlib import Path
import random
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def value(base, word):
    n = 0
    for coefficient in reversed(word):
        n = n * base + coefficient
    return n


def digits(base, n, width):
    """Exactly width digits, retaining positional zeroes."""
    result = []
    for _ in range(width):
        n, digit = divmod(n, base)
        result.append(digit)
    return tuple(result)


def center_step(base, center, entering, overflow, trim):
    """Exact fixed-trim center successor, or None if an edge is invalid."""
    center = tuple(center)
    if (base < 2 or not center or center != center[::-1]
            or entering not in (0, 1) or overflow not in (0, 1)
            or not isinstance(trim, int) or trim < 0
            or any(not isinstance(x, int) or not 0 <= x <= 2 * base - 2
                   for x in center)):
        return None
    width = len(center)
    n = value(base, center) + entering
    if n // base**width != 1 - entering:
        return None
    word = digits(base, n, width)
    if overflow:
        word += ((base - 1) * entering,)
    raw = tuple(word[i] + word[-1 - i] for i in range(len(word)))
    if len(raw) <= 2 * trim:
        return None
    if any(raw[i] != base - 1 or raw[-1 - i] != base - 1
           for i in range(trim)):
        return None
    return raw[trim:len(raw) - trim]


def verify_centers(base, entering, overflow, trims, centers):
    if not centers or not len(entering) == len(overflow) == len(trims) == len(centers):
        return False
    return all(center_step(base, centers[t], entering[t], overflow[t], trims[t])
               == tuple(centers[(t + 1) % len(centers)])
               for t in range(len(centers)))


def brute_centers(base, entering, overflow, trims, width):
    """Exhaust symmetric initial centers of one specified width."""
    count = 0
    for half in itertools.product(range(2 * base - 1), repeat=(width + 1) // 2):
        initial = half + half[:width // 2][::-1]
        current = initial
        for e, g, v in zip(entering, overflow, trims):
            current = center_step(base, current, e, g, v)
            if current is None:
                break
        if current == initial:
            count += 1
    return count


def source_certificates():
    """Parse only named Nat-list data and concrete List Edge definitions."""
    paths = [ROOT / "lean/P196/Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean",
             ROOT / "lean/P196/Agent213KnownBaseMechanisms/KnownBases.lean"]
    certificates = {}
    for path in paths:
        text = path.read_text()
        names = {name: tuple(ast.literal_eval(literal)) for name, literal in
                 re.findall(r"def\s+(\w+)\s*:\s*List Nat\s*:=\s*(\[[^\]]*\])", text)}
        for base, block in re.findall(r"def cert(\d+)\s*:\s*List Edge\s*:=\s*(.*?)\n\n", text, re.S):
            edges = []
            for body in re.findall(r"⟨(.*?)⟩", block):
                fields = re.findall(r"\[[^\]]*\]|\w+", body)
                require(len(fields) == 6, f"unrecognized source edge in {path}")
                words = [tuple(ast.literal_eval(x)) if x.startswith("[") else names[x]
                         for x in fields[:4]]
                edges.append((*words, int(fields[4]), int(fields[5])))
            require(bool(edges), f"empty source certificate {base}")
            certificates[int(base)] = edges
    require(set(certificates) == {2, 4, 8, 11, 16, 17, 26, 32}, "source certificate set changed")
    return certificates


def source_stream(base, edges):
    es, gs, vs, centers = [], [], [], []
    for exterior, center, _, _, _, trim in edges:
        e = value(base, exterior) // base**len(exterior)
        g = (value(base, exterior[::-1]) + 1 - e) // base**len(exterior)
        es.append(e); gs.append(g); vs.append(trim); centers.append(center)
    return tuple(es), tuple(gs), tuple(vs), tuple(centers)


def audit_positive_sources(certificates):
    edge_count = transported = 0
    rng = random.Random(118)
    for base, edges in sorted(certificates.items()):
        es, gs, vs, centers = source_stream(base, edges)
        require(verify_centers(base, es, gs, vs, centers), f"source center replay failed: {base}")
        require(all(edges[t][3] == centers[(t + 1) % len(edges)] for t in range(len(edges))),
                f"source target discrepancy: {base}")
        edge_count += len(edges)
        for repeat in (1, 2, 3):
            e, g, v, cs = es * repeat, gs * repeat, vs * repeat, centers * repeat
            schedules = []
            for slot in (0, len(v) // 2, len(v) - 1):
                target = [0] * len(v); target[slot] = sum(v); schedules.append(target)
            target = [0] * len(v)
            for _ in range(sum(v)):
                target[rng.randrange(len(v))] += 1
            schedules.append(target)
            for target in schedules:
                offsets = [0]
                for old, new in zip(v, target):
                    offsets.append(offsets[-1] + old - new)
                require(offsets[-1] == 0, "padding transport did not close")
                shift = -min(offsets)
                padded = [((base - 1,) * (offsets[t] + shift) + center
                           + (base - 1,) * (offsets[t] + shift))
                          for t, center in enumerate(cs)]
                require(verify_centers(base, e, g, target, padded),
                        f"trim-schedule transport failed: base {base}, repeat {repeat}")
                transported += len(padded)
    return edge_count, transported


def audit_integer_templates(trials=10000):
    rng = random.Random(118120)
    checked = 0
    while checked < trials:
        base = rng.choice((2, 3, 4, 7, 10, 11, 17, 26, 32))
        exterior = tuple(rng.randrange(2 * base - 1) for _ in range(rng.randrange(0, 9)))
        if exterior and exterior[0] == 0:
            continue
        width = rng.randrange(1, 16)
        half = tuple(rng.randrange(2 * base - 1) for _ in range((width + 1) // 2))
        center = half + half[:width // 2][::-1]
        e = value(base, exterior) // base**len(exterior)
        if (value(base, center) + e) // base**width != 1 - e:
            continue
        g = (value(base, exterior[::-1]) + 1 - e) // base**len(exterior)
        raw = center_step(base, center, e, g, 0)
        gap = rng.randrange(2, 9)
        neutral = (base - 1,) * gap
        template = exterior + neutral + center + neutral + exterior[::-1]
        n = value(base, template)
        full = []
        while n:
            n, digit = divmod(n, base); full.append(digit)
        require(len(full) == len(template) + g, "full template length mismatch")
        pairs = tuple(x + y for x, y in zip(full, reversed(full)))
        start = len(exterior) + gap
        require(pairs[start:start + width + g] == raw, "integer center extraction mismatch")
        checked += 1
    return checked


def parse_witness(line):
    match = re.match(r"FEASIBLE(?:_CLASS)? b=(\d+) e=([01]+) g=([01]+) v=([01]+) m0=(\d+)", line)
    if not match:
        raise ValueError("unrecognized witness header")
    base = int(match[1])
    e, g, v = (tuple(map(int, match[i])) for i in (2, 3, 4))
    indexed = [(int(index), tuple(map(int, data.split(",")))) for index, data in
               re.findall(r" C(\d+)=\[([^\]]+)\]", line)]
    require([i for i, _ in indexed] == list(range(len(e))), "missing/duplicate witness phase")
    centers = [center for _, center in indexed]
    require(len(centers[0]) == int(match[5]), "witness initial width mismatch")
    require(verify_centers(base, e, g, v, centers), "invalid center witness")
    return base, len(e), len(centers[0])


def solver_case(executable, base, e, g, v, width, timeout=20):
    bits = lambda word: "".join(map(str, word))
    cmd = [str(executable), str(base), bits(e), bits(g), str(width), str(width),
           "-v", bits(v), "-w", "-cap", "200000"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    require(result.returncode == 0, f"solver exited {result.returncode}: {result.stderr}")
    require(not any(word in result.stdout for word in ("CAPPED", "NOPERIOD", "UNDECIDED")),
            "solver did not decide bounded control")
    lines = result.stdout.splitlines()
    witnesses = [line for line in lines if line.startswith("FEASIBLE")]
    require(sum(line.startswith("DONE ") for line in lines) == 1, "missing solver completion")
    require(any("status=hit" in line for line in lines) == bool(witnesses), "solver hit inconsistency")
    for line in witnesses:
        parse_witness(line)
    return bool(witnesses)


def differential(executable, certificates, random_cases=256):
    tally = Counter()
    for period in (2, 3):
        for e in itertools.product((0, 1), repeat=period):
            for ones in itertools.combinations(range(period), 2):
                g = tuple(int(t in ones) for t in range(period))
                for cut in range(period):
                    v = tuple(int(t == cut) for t in range(period))
                    for width in range(1, 7):
                        expected = brute_centers(2, e, g, v, width) > 0
                        actual = solver_case(executable, 2, e, g, v, width)
                        require(expected == actual, f"bounded mismatch: {(2,e,g,v,width)}")
                        tally["small_feasible" if actual else "small_none"] += 1
    rng = random.Random(11848)
    for _ in range(random_cases):
        base = rng.choice((2, 3, 4)); period = rng.randrange(4, 9)
        ones = rng.sample(range(period), rng.choice((2, 4)))
        cuts = rng.sample(range(period), len(ones) // 2)
        e = tuple(rng.randrange(2) for _ in range(period))
        g = tuple(int(t in ones) for t in range(period))
        v = tuple(int(t in cuts) for t in range(period))
        width = rng.randrange(1, 7)
        expected = brute_centers(base, e, g, v, width) > 0
        actual = solver_case(executable, base, e, g, v, width)
        require(expected == actual, f"bounded mismatch: {(base,e,g,v,width)}")
        tally["random_feasible" if actual else "random_none"] += 1
    for base in (2, 4):
        original_e, original_g, _, _ = source_stream(base, certificates[base])
        period = len(original_e)
        for phase in range(period):
            e = original_e[phase:] + original_e[:phase]
            g = original_g[phase:] + original_g[:phase]
            for cut in range(period):
                v = tuple(int(t == cut) for t in range(period))
                for width in range(1, 7):
                    expected = brute_centers(base, e, g, v, width) > 0
                    actual = solver_case(executable, base, e, g, v, width)
                    require(expected == actual, f"positive-family mismatch: {(base,e,g,v,width)}")
                    tally["family_feasible" if actual else "family_none"] += 1
    for base, edges in sorted(certificates.items()):
        e, g, v, centers = source_stream(base, edges)
        require(solver_case(executable, base, e, g, v, len(centers[0])),
                f"known positive rejected: base {base}")
        tally["source_positive"] += 1
    e, g, v, centers = source_stream(32, certificates[32])
    require(solver_case(executable, 32, e * 4, g * 4, v * 4, len(centers[0])),
            "period48 repeated base32 positive rejected")
    tally["period48_positive"] += 1
    e, g, v, centers = source_stream(2, certificates[2])
    bits = lambda word: "".join(map(str, word))
    oversized = subprocess.run([str(executable), "2", bits(e * 12), bits(g * 12),
                                "2", "2", "-v", bits(v * 12), "-w"],
                               capture_output=True, text=True, timeout=20)
    require(oversized.returncode != 0 and "UNDECIDED" in oversized.stderr + oversized.stdout,
            "oversized period48 base2 packing was not rejected explicitly")
    tally["period48_capacity_rejected"] += 1
    return dict(sorted(tally.items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, help="also run independent bounded differential checks")
    parser.add_argument("--random-cases", type=int, default=256)
    parser.add_argument("--replay-stdin", action="store_true", help="verify FEASIBLE lines from stdin")
    args = parser.parse_args()
    if args.replay_stdin:
        count = 0
        for line in sys.stdin:
            if line.startswith("FEASIBLE"):
                parse_witness(line); count += 1
        require(count > 0, "no witnesses supplied")
        print(f"witnesses_replayed={count}")
        return
    certificates = source_certificates()
    edges, transported = audit_positive_sources(certificates)
    integer_checks = audit_integer_templates()
    print(f"known_bases={sorted(certificates)} source_edges={edges} "
          f"transported_edges={transported} integer_template_checks={integer_checks}")
    if args.solver:
        print("bounded_solver_differential", differential(args.solver, certificates, args.random_cases))
    print("COMPUTED CHECKS PASSED; no new Lean theorem or all-length negative asserted")


if __name__ == "__main__":
    main()
