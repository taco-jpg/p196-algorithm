#!/usr/bin/env python3
"""Independent arithmetic controls for the Agent 111 compiled center runner.

The reference normalizes by whole-integer positional evaluation, not by the
column-transfer or segment algorithms in cauto_fast.  Existing certificates are
read from their actual Lean source files.  Neutral-padding schedule changes use
the covariance/scheduling results credited to Agents 7, 107, and 110 in #289;
this file supplies regression checks, not a new proof of those results.

Run arithmetic/source controls:
  python3 calculation/agent-111/center_controls.py
Add finite brute-force and long-period executable comparisons:
  python3 calculation/agent-111/center_controls.py --binary /tmp/agent111_cauto
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import random
import re
from typing import NamedTuple


class Edge(NamedTuple):
    B: tuple[int, ...]
    C: tuple[int, ...]
    B2: tuple[int, ...]
    C2: tuple[int, ...]
    u: int
    v: int


def require(condition: bool, message: str) -> None:
    """Proof-critical tests remain active under python -O."""
    if not condition:
        raise RuntimeError(message)


def integer_norm(base: int, word: tuple[int, ...], carry: int):
    """Fixed-width digits and outgoing carry from exact integer arithmetic."""
    n = 0
    for x in reversed(word):
        n = n * base + x
    n += carry
    digits = []
    for _ in word:
        n, d = divmod(n, base)
        digits.append(d)
    return tuple(digits), n


def center_step(base: int, center, e: int, g: int, trim: int):
    """Exact forced center edge; None means malformed or arithmetically illegal.

    Coefficients are least significant first.  This reference permits arbitrary
    nonnegative trim counts, unlike the compiled binary-trim interface.
    """
    center = tuple(center)
    if (any(type(x) is not int for x in (base, e, g, trim))
            or base < 2 or e not in (0, 1) or g not in (0, 1) or trim < 0
            or not center or center != center[::-1]
            or any(type(x) is not int or x < 0 or x > 2 * (base - 1)
                   for x in center)):
        return None
    digits, carry = integer_norm(base, center, e)
    if carry != 1 - e:
        return None
    if g:
        digits += ((base - 1) * e,)
    raw = tuple(a + b for a, b in zip(digits, reversed(digits)))
    if len(raw) - 2 * trim < 1:
        return None
    if any(x != base - 1 for x in raw[:trim] + raw[len(raw) - trim:]):
        return None
    return raw[trim:len(raw) - trim]


def _naturals(source: str) -> tuple[int, ...]:
    if not source.strip():
        return ()
    pieces = source.split(",")
    require(all(re.fullmatch(r"\s*\d+\s*", x) for x in pieces),
            "nonliteral Nat list in certificate source")
    return tuple(int(x) for x in pieces)


def read_certificates(root: Path) -> dict[int, tuple[Edge, ...]]:
    sources = [
        root / "lean/P196/Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean",
        root / "lean/P196/Agent213KnownBaseMechanisms/KnownBases.lean",
    ]
    result = {}
    for source in sources:
        text = source.read_text()
        definitions = {name: _naturals(body) for name, body in re.findall(
            r"def\s+(\w+)\s*:\s*List Nat\s*:=\s*\[([^\]]*)\]", text)}
        for base_text, body in re.findall(
                r"def\s+cert(\d+)\s*:\s*List Edge\s*:=\s*(\[.*?\])\s*\n\s*\n",
                text, re.S):
            edges = []
            for fields in re.findall(r"⟨([^⟩]*)⟩", body):
                parts = re.findall(r"\[[^\]]*\]|\w+", fields)
                require(len(parts) == 6, "unexpected Edge literal")
                words = tuple(_naturals(x[1:-1]) if x.startswith("[")
                              else definitions[x] for x in parts[:4])
                edges.append(Edge(*words, int(parts[4]), int(parts[5])))
            base = int(base_text)
            require(base not in result and bool(edges), "missing/duplicate certificate")
            result[base] = tuple(edges)
    expected = {2: 4, 4: 6, 8: 8, 11: 6, 16: 10, 17: 6, 26: 4, 32: 12}
    require({b: len(es) for b, es in result.items()} == expected,
            "source certificate set/counts differ from audited eight-base baseline")
    return result


def inspect_certificate(base: int, edges: tuple[Edge, ...]):
    e_bits, g_bits = [], []
    require(bool(edges), "empty source cycle")
    for i, edge in enumerate(edges):
        nxt = edges[(i + 1) % len(edges)]
        require((edge.B2, edge.C2) == (nxt.B, nxt.C), "source chain does not close")
        db, e = integer_norm(base, edge.B, 0)
        _, exit_c = integer_norm(base, edge.C, e)
        dr, g = integer_norm(base, edge.B[::-1], exit_c)
        require(e in (0, 1) and g in (0, 1) and exit_c == 1 - e,
                "source carry mismatch")
        lhs = db + ((base - 1) * (1 - e),) if g else db
        rhs = (1,) + dr[::-1] if g else dr[::-1]
        raw_b = tuple(a + b for a, b in zip(lhs, rhs))
        require(raw_b == edge.B2 + (base - 1,) * edge.u,
                "independent exterior control failed")
        require(center_step(base, edge.C, e, g, edge.v) == edge.C2,
                "independent center control failed")
        e_bits.append(e)
        g_bits.append(g)
    require(sum(edge.u for edge in edges) == sum(g_bits), "exterior length ledger")
    require(2 * sum(edge.v for edge in edges) == sum(g_bits), "center length ledger")
    return tuple(e_bits), tuple(g_bits)


def alternating_trim(g_bits, start_level: int = 0) -> tuple[int, ...]:
    require(start_level in (0, 1) and all(x in (0, 1) for x in g_bits),
            "invalid alternating-overflow input")
    level = start_level
    trims = []
    for g in g_bits:
        trims.append(level if g else 0)
        level ^= g
    require(level == start_level, "odd overflow count cannot close center length")
    return tuple(trims)


def pad_to_schedule(base: int, edges: tuple[Edge, ...], target, extra_pad=0):
    require(bool(edges) and len(target) == len(edges) and extra_pad >= 0
            and all(isinstance(x, int) and x >= 0 for x in target),
            "invalid target trim schedule")
    offsets = [0]
    for edge, trim in zip(edges, target):
        offsets.append(offsets[-1] + edge.v - trim)
    require(offsets[-1] == 0, "target trim total differs")
    shift = -min(offsets) + extra_pad
    pads = tuple(x + shift for x in offsets[:-1])
    centers = tuple((base - 1,) * p + edge.C + (base - 1,) * p
                    for edge, p in zip(edges, pads))
    padded = tuple(Edge(edge.B, centers[i], edge.B2,
                        centers[(i + 1) % len(edges)], edge.u, target[i])
                   for i, edge in enumerate(edges))
    return padded, pads


def source_controls(certificates):
    rng = random.Random(111)
    cycles = padded_edges = originals = 0
    bases = []
    for base, source in sorted(certificates.items()):
        inspect_certificate(base, source)
        originals += len(source)
        bases.append(base)
        for repetitions in (1, 2, 3, 4):
            edges = source * repetitions
            e, g = inspect_certificate(base, edges)
            total = sum(edge.v for edge in edges)
            schedules = [alternating_trim(g, low) for low in (0, 1)]
            for phase in range(len(edges)):
                w = [0] * len(edges)
                w[phase] = total
                schedules.append(tuple(w))
            for _ in range(20):
                w = [0] * len(edges)
                for _ in range(total):
                    w[rng.randrange(len(edges))] += 1
                schedules.append(tuple(w))
            for schedule in schedules:
                padded, _ = pad_to_schedule(base, edges, schedule, extra_pad=1)
                ep, gp = inspect_certificate(base, padded)
                require((ep, gp) == (e, g), "padding changed exterior streams")
                if schedule in (alternating_trim(g, 0), alternating_trim(g, 1)):
                    widths = [len(edge.C) for edge in padded]
                    require(max(widths) - min(widths) <= 1,
                            "alternating-overflow width range exceeds one")
                cycles += 1
                padded_edges += len(padded)
    return {"bases": bases, "original_edges": originals,
            "padded_cycles": cycles, "padded_edges": padded_edges}


def invalid_controls():
    # Each malformed or impossible transition must reject even under python -O.
    cases = [
        (1, (0,), 0, 0, 0), (10, (), 0, 0, 0),
        (10, (-1,), 0, 0, 0), (10, (19,), 0, 0, 0),
        (10, (1, 2), 0, 0, 0), (10, (10,), 2, 0, 0),
        (10, (10,), 0, 2, 0), (10, (10,), 0, 0, -1),
        (10, (9,), 0, 0, 0), (10, (9,), 1, 0, 0),
        (2, (0, 0), 1, 1, 2), (2, (0, 0), 0, 0, 0),
        (10, (10,), 0.0, 0, 0), (10, (10,), 0, 0.0, 0),
    ]
    for case in cases:
        require(center_step(*case) is None, f"invalid center case accepted: {case}")
    return {"rejected_cases": len(cases)}


def brute_counts(base, e_bits, g_bits, trims, maximum_width):
    counts = {}
    starts = 0
    for width in range(1, maximum_width + 1):
        count = 0
        for half in itertools.product(range(2 * base - 1), repeat=(width + 1) // 2):
            start = half + half[:width // 2][::-1]
            current = start
            starts += 1
            for e, g, v in zip(e_bits, g_bits, trims):
                current = center_step(base, current, e, g, v)
                if current is None:
                    break
            if current == start:
                count += 1
        counts[width] = count
    return counts, starts


def _bits(word) -> str:
    return "".join(map(str, word))


def finite_cases():
    # Exhaust all carries and positive even overflow words at P=2..4 in
    # bases 2 and 3, both alternating-overflow schedules, C0 width 1..5.
    for base in (2, 3):
        for period in range(2, 5):
            for g in itertools.product((0, 1), repeat=period):
                if sum(g) == 0 or sum(g) % 2:
                    continue
                for e in itertools.product((0, 1), repeat=period):
                    for level in (0, 1):
                        yield base, e, g, alternating_trim(g, level), 5
    # Separate bounded random binary trim schedules, not just normalized ones.
    rng = random.Random(111)
    for _ in range(100):
        base = rng.choice((4, 10))
        period = rng.choice((4, 5, 6))
        ones = rng.choice(tuple(range(2, period + 1, 2)))
        overflow_slots = set(rng.sample(range(period), ones))
        trim_slots = set(rng.sample(range(period), ones // 2))
        g = tuple(int(i in overflow_slots) for i in range(period))
        v = tuple(int(i in trim_slots) for i in range(period))
        e = tuple(rng.randrange(2) for _ in range(period))
        yield base, e, g, v, 4
    # The actual long decimal driver streams, independently enumerated at small
    # initial widths only.  These are controls, not all-width negative claims.
    for es, gs, repetitions in (("10100110011", "11100010000", 3),
                               ("101010010101", "100010001000", 4)):
        e = tuple(map(int, es)) * repetitions
        g = tuple(map(int, gs)) * repetitions
        for level in (0, 1):
            yield 10, e, g, alternating_trim(g, level), 5 if repetitions == 3 else 4


def _engine(run, binary, base, e, g, v, mlo, mhi, witness=False):
    result = run(binary, base, _bits(e), _bits(g), mlo, mhi, _bits(v),
                 all_lengths=False, cap=1000000, timeout=30, witness=witness)
    require(result.returncode == 0, f"engine failed: {result.stderr}")
    require(not re.search(r"CAPPED|NOPERIOD|UNDECIDED|UNSUPPORTED", result.stdout),
            f"finite differential engine run did not decide: {result.args}; "
            f"stdout={result.stdout[-1200:]}")
    require(re.search(r"^DONE .*status=(?:hit|none)(?: |$)", result.stdout, re.M)
            is not None, "missing explicit completed fixed-width status")
    feasible = {int(x) for x in re.findall(r"^FEASIBLE .*?\bm0=(\d+)",
                                          result.stdout, re.M)}
    return feasible, result.stdout


def binary_controls(binary: Path, certificates):
    from long_center import run

    patterns = instances = starts = positives = negatives = 0
    for base, e, g, v, maximum in finite_cases():
        expected, n = brute_counts(base, e, g, v, maximum)
        actual, _ = _engine(run, binary, base, e, g, v, 1, maximum)
        wanted = {m for m, count in expected.items() if count}
        require(actual == wanted,
                f"finite mismatch b={base} e={_bits(e)} g={_bits(g)} "
                f"v={_bits(v)} expected={sorted(wanted)} actual={sorted(actual)}")
        patterns += 1
        instances += maximum
        starts += n
        positives += len(wanted)
        negatives += maximum - len(wanted)

    # P36 and P48 controls stay within the engine's explicit 256-bit packing
    # guard.  Long repeated base-2/26 P48 controls do not and are not used.
    long_specs = ((2, 9), (4, 6), (8, 6), (16, 4), (32, 4))
    witnessed_edges = 0
    for base, repetitions in long_specs:
        edges = certificates[base] * repetitions
        e, g = inspect_certificate(base, edges)
        for level in (0, 1):
            trims = alternating_trim(g, level)
            padded, _ = pad_to_schedule(base, edges, trims)
            width = len(padded[0].C)
            actual, stdout = _engine(run, binary, base, e, g, trims,
                                     width, width, witness=True)
            require(actual == {width}, "known long-period source control lost")
            line = next(x for x in stdout.splitlines() if x.startswith("FEASIBLE "))
            witness = {int(i): _naturals(w) for i, w in re.findall(
                r"\bC(\d+)=\[([^\]]*)\]", line)}
            require(set(witness) == set(range(len(edges))), "incomplete long witness")
            for i in range(len(edges)):
                require(center_step(base, witness[i], e[i], g[i], trims[i])
                        == witness[(i + 1) % len(edges)], "long witness replay failed")
                witnessed_edges += 1
    return {"patterns": patterns, "fixed_width_instances": instances,
            "enumerated_initial_centers": starts, "feasible_instances": positives,
            "infeasible_instances": negatives, "long_positive_cases": 2 * len(long_specs),
            "independently_replayed_long_edges": witnessed_edges}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    certificates = read_certificates(root)
    print("SOURCE_CONTROLS " + json.dumps(source_controls(certificates), sort_keys=True))
    print("INVALID_CONTROLS " + json.dumps(invalid_controls(), sort_keys=True))
    if args.binary:
        print("BINARY_CONTROLS " + json.dumps(binary_controls(args.binary, certificates),
                                              sort_keys=True))
    print("ALL CENTER CONTROLS PASSED")


if __name__ == "__main__":
    main()
