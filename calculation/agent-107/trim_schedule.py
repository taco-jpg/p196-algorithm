#!/usr/bin/env python3
"""Retiming center trims in neutral-band cycles (all bases >= 2).

For fixed periodic carry/overflow streams, every nonnegative center trim
schedule with the required total is equivalent over unrestricted center
widths.  Padding the center at phase t by a_t neutral layers changes
v_t to v_t + a_t - a_(t+1).  The minimum nonnegative offsets are computed
exactly; each is at most K = sum(v), so width increases by at most 2*K.

This is a constructive PAPER PROOF implementation, not a Lean result.
The checks below use explicit conditionals and remain active under python -O.
Core operations use only the standard library.  The selftest reads the eight
existing Lean certificate fixtures and also replays outputs in the repository
mirror; it does not treat those tests as the proof of the general statement.

Usage (repository root):
  python3 calculation/agent-107/trim_schedule.py selftest
  python3 calculation/agent-107/trim_schedule.py schedule 111000100001110001000011100010000
  python3 calculation/agent-107/trim_schedule.py retime cycle.json --target 1,0,0,0

Input for retime: {"base": b, "edges": [[B,C,B2,C2,u,v], ...]}.
Output includes the complete transformed edges, streams, and padding offsets.
No finite-width negative result is transferable without the width allowance.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
import importlib.util
import itertools
import json
from pathlib import Path
import random
import re
import sys
from typing import Iterable, Sequence


Word = tuple[int, ...]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def natural(value: object) -> bool:
    return type(value) is int and value >= 0


def checked_base(base: int) -> None:
    require(natural(base) and base >= 2, "base must be an integer >= 2")


def checked_word(base: int, word: Sequence[int]) -> None:
    require(all(natural(x) and x <= 2 * base - 2 for x in word),
            "coefficient outside 0..2*base-2")


def normalize(base: int, word: Sequence[int], entry: int) -> tuple[Word, int]:
    checked_base(base)
    checked_word(base, word)
    require(type(entry) is int and entry in (0, 1), "entry carry must be a bit")
    digits = []
    carry = entry
    for coefficient in word:
        carry, digit = divmod(coefficient + carry, base)
        digits.append(digit)
    return tuple(digits), carry


def pad(base: int, word: Sequence[int], amount: int) -> Word:
    checked_base(base)
    require(natural(amount), "padding must be a nonnegative integer")
    band = (base - 1,) * amount
    return band + tuple(word) + band


def raw_center(base: int, center: Sequence[int], entry: int, overflow: int) -> Word:
    """Raw center update, with the required opposite exit carry checked."""
    require(type(overflow) is int and overflow in (0, 1), "overflow must be a bit")
    require(len(center) > 0, "center must be nonempty")
    digits, exit_carry = normalize(base, center, entry)
    require(exit_carry == 1 - entry, "center does not flip the carry")
    if overflow:
        digits += ((base - 1) * entry,)
    return tuple(digits[i] + digits[-1 - i] for i in range(len(digits)))


def validate_center_cycle(base: int, centers: Sequence[Sequence[int]],
                          carry: Sequence[int], overflow: Sequence[int],
                          trims: Sequence[int]) -> None:
    checked_base(base)
    period = len(centers)
    require(period > 0, "cycle must be nonempty")
    require(len(carry) == len(overflow) == len(trims) == period,
            "stream lengths must match the period")
    require(all(natural(v) for v in trims), "trim counts must be natural numbers")
    for t, center in enumerate(centers):
        require(tuple(center) == tuple(reversed(center)), "center must be symmetric")
        output = raw_center(base, center, carry[t], overflow[t])
        require(output == pad(base, centers[(t + 1) % period], trims[t]),
                f"center edge {t} fails its exact trim equality")
    require(2 * sum(trims) == sum(overflow), "center length balance fails")


def center_cycle_ok(base: int, centers: Sequence[Sequence[int]],
                    carry: Sequence[int], overflow: Sequence[int],
                    trims: Sequence[int]) -> bool:
    try:
        validate_center_cycle(base, centers, carry, overflow, trims)
    except (ValueError, TypeError, IndexError):
        return False
    return True


def padding_offsets(source: Sequence[int], target: Sequence[int]) -> Word:
    """Unique cyclic offsets with min(a)=0 and a[t+1]-a[t]=source[t]-target[t]."""
    require(len(source) > 0 and len(source) == len(target), "schedule lengths differ")
    require(all(natural(v) for v in tuple(source) + tuple(target)),
            "schedule entries must be natural numbers")
    require(sum(source) == sum(target), "schedule totals differ")
    prefix = [0]
    for old, new in zip(source, target):
        prefix.append(prefix[-1] + old - new)
    require(prefix[-1] == 0, "offsets do not close")
    minimum = min(prefix[:-1])
    offsets = tuple(value - minimum for value in prefix[:-1])
    require(max(offsets) <= sum(source), "offset bound failed")
    return offsets


def retime_center_cycle(base: int, centers: Sequence[Sequence[int]],
                        carry: Sequence[int], overflow: Sequence[int],
                        source: Sequence[int], target: Sequence[int]) -> tuple[tuple[Word, ...], Word]:
    validate_center_cycle(base, centers, carry, overflow, source)
    offsets = padding_offsets(source, target)
    transformed = tuple(pad(base, center, a) for center, a in zip(centers, offsets))
    validate_center_cycle(base, transformed, carry, overflow, target)
    return transformed, offsets


def binary_schedules(period: int, total: int) -> Iterable[Word]:
    require(natural(period) and period > 0 and natural(total) and total <= period,
            "binary schedule requires 0 <= total <= period")
    for positions in itertools.combinations(range(period), total):
        chosen = set(positions)
        yield tuple(int(t in chosen) for t in range(period))


def balanced_schedule(period: int, total: int, phase: int = 0) -> Word:
    """Binary schedule with cyclic gaps floor(P/K) or ceil(P/K), first trim at phase."""
    require(natural(period) and period > 0 and natural(total) and total <= period,
            "binary schedule requires 0 <= total <= period")
    require(natural(phase) and phase < period, "phase must lie in 0..period-1")
    positions = {(phase + j * period // total) % period for j in range(total)}
    return tuple(int(t in positions) for t in range(period))


@dataclass(frozen=True)
class Edge:
    B: Word
    C: Word
    B2: Word
    C2: Word
    u: int
    v: int

    def row(self) -> list:
        return [list(self.B), list(self.C), list(self.B2), list(self.C2), self.u, self.v]


def cycle_streams(base: int, edges: Sequence[Edge]) -> tuple[Word, Word]:
    carries, overflows = [], []
    for edge in edges:
        _, entry = normalize(base, edge.B, 0)
        _, exit_carry = normalize(base, edge.C, entry)
        require(exit_carry == 1 - entry, "Hyp carry flip fails")
        _, overflow = normalize(base, tuple(reversed(edge.B)), exit_carry)
        carries.append(entry)
        overflows.append(overflow)
    return tuple(carries), tuple(overflows)


def validate_cycle(base: int, edges: Sequence[Edge]) -> None:
    """Independent complete structural replay of a closed neutral-band certificate."""
    checked_base(base)
    require(len(edges) > 0, "cycle must be nonempty")
    carry, overflow = cycle_streams(base, edges)
    for t, edge in enumerate(edges):
        require(natural(edge.u) and natural(edge.v), "trim counts must be natural numbers")
        require(not edge.B or edge.B[0] != 0, "exterior has a zero first coefficient")
        require((edge.B2, edge.C2) == (edges[(t + 1) % len(edges)].B,
                                        edges[(t + 1) % len(edges)].C),
                f"edge {t} is not linked to its cyclic successor")
        left, _ = normalize(base, edge.B, 0)
        right, _ = normalize(base, tuple(reversed(edge.B)), 1 - carry[t])
        right = tuple(reversed(right))
        if overflow[t]:
            left += ((base - 1) * (1 - carry[t]),)
            right = (1,) + right
        require(len(left) == len(right), "exterior arm lengths differ")
        raw = tuple(x + y for x, y in zip(left, right))
        require(raw == edge.B2 + (base - 1,) * edge.u,
                f"exterior edge {t} fails its exact trim equality")
    validate_center_cycle(base, tuple(edge.C for edge in edges), carry, overflow,
                          tuple(edge.v for edge in edges))
    require(sum(overflow) <= sum(edge.u + edge.v for edge in edges),
            "certificate gain inequality fails")


def cycle_ok(base: int, edges: Sequence[Edge]) -> bool:
    try:
        validate_cycle(base, edges)
    except (ValueError, TypeError, IndexError, AttributeError):
        return False
    return True


def retime_cycle(base: int, edges: Sequence[Edge], target: Sequence[int]) -> tuple[tuple[Edge, ...], Word]:
    """Keep every B/B2/u unchanged and replace only C/C2/v."""
    validate_cycle(base, edges)
    carry, overflow = cycle_streams(base, edges)
    centers, offsets = retime_center_cycle(base, tuple(edge.C for edge in edges),
        carry, overflow, tuple(edge.v for edge in edges), target)
    transformed = tuple(replace(edge, C=centers[t], C2=centers[(t + 1) % len(edges)],
                                v=target[t]) for t, edge in enumerate(edges))
    validate_cycle(base, transformed)
    require(cycle_streams(base, transformed) == (carry, overflow), "driver streams changed")
    return transformed, offsets


def fixture_cycles(repo: Path) -> dict[int, tuple[Edge, ...]]:
    """Read literal fixtures from the two existing Lean certificate sources."""
    root = repo / "lean/P196"
    paths = [root / "Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean",
             root / "Agent213KnownBaseMechanisms/KnownBases.lean"]
    cycles = {}
    word_pattern = r"\[([^\]]*)\]"
    def word(body: str) -> Word:
        return tuple(int(x.strip()) for x in body.split(",") if x.strip())
    for path in paths:
        text = path.read_text()
        named = {name: word(body) for name, body in re.findall(
            r"def\s+(\w+)\s*:\s*List Nat\s*:=\s*" + word_pattern, text)}
        for base_text, body in re.findall(r"def cert(\d+)\s*:\s*List Edge\s*:=\s*\[(.*?)\]\s*\n\n",
                                          text, re.S):
            edges = []
            for fields in re.findall(r"⟨([^⟩]+)⟩", body):
                tokens = re.findall(r"\[[^\]]*\]|\w+", fields)
                require(len(tokens) == 6, f"cannot parse fixture in {path}")
                words = [word(token[1:-1]) if token.startswith("[") else named[token]
                         for token in tokens[:4]]
                edges.append(Edge(*words, int(tokens[4]), int(tokens[5])))
            require(len(edges) > 0, f"empty parsed fixture cert{base_text}")
            cycles[int(base_text)] = tuple(edges)
    require(set(cycles) == {2, 4, 8, 16, 32, 11, 17, 26}, "expected eight fixture bases")
    return cycles


def _selftest(repo: Path) -> None:
    # The implementation above does not import the existing mirror.  Use it
    # here as a second checker of the complete transformed edge lists.
    spec = importlib.util.spec_from_file_location("a107_mirror", repo / "calculation/neutral_band_search.py")
    require(spec is not None and spec.loader is not None, "mirror loader unavailable")
    mirror = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mirror)
    cycles = fixture_cycles(repo)
    binary_count = nonbinary_count = edge_count = 0
    for base, original in sorted(cycles.items()):
        require(cycle_ok(base, original), f"original base-{base} fixture failed")
        n_binary = n_nonbinary = 0
        for repeats in (1, 2):
            source = original * repeats
            mass = sum(edge.v for edge in source)
            for target in binary_schedules(len(source), mass):
                transformed, offsets = retime_cycle(base, source, target)
                rows = [edge.row() for edge in transformed]
                require(mirror.cycleOK(base, rows, rows[0][0], rows[0][1]),
                        f"mirror rejected binary retiming in base {base}")
                require(min(offsets) == 0 and max(offsets) <= mass, "offset minimality/bound")
                n_binary += 1
                edge_count += len(source)
        for repeats in (2, 3):
            source = original * repeats
            mass = sum(edge.v for edge in source)
            for position in range(len(source)):
                target = tuple(mass if t == position else 0 for t in range(len(source)))
                transformed, _ = retime_cycle(base, source, target)
                rows = [edge.row() for edge in transformed]
                require(mirror.cycleOK(base, rows, rows[0][0], rows[0][1]),
                        f"mirror rejected nonbinary retiming in base {base}")
                n_nonbinary += 1
                edge_count += len(source)
        binary_count += n_binary
        nonbinary_count += n_nonbinary
        print(f"base={base} binary_schedules={n_binary} nonbinary_targets={n_nonbinary} PASS")

    # Same-sum and minimum-offset construction across arbitrary distributions,
    # including periods with more mass than slots (outside binary scheduling).
    rng = random.Random(107)
    schedule_cases = 5000
    for _ in range(schedule_cases):
        period, mass = rng.randrange(1, 40), rng.randrange(0, 80)
        source, target = [0] * period, [0] * period
        for _ in range(mass):
            source[rng.randrange(period)] += 1
            target[rng.randrange(period)] += 1
        offsets = padding_offsets(source, target)
        require(min(offsets) == 0 and max(offsets) <= mass, "random offset bound")
        for t in range(period):
            require(source[t] + offsets[t] - offsets[(t + 1) % period] == target[t],
                    "random retiming equation")

    covariance_cases = 0
    for _ in range(10000):
        base = rng.choice((2, 3, 4, 5, 10, 11, 17, 26, 32, 64, 101))
        size = rng.randrange(1, 15)
        half = tuple(rng.randrange(2 * base - 1) for _ in range((size + 1) // 2))
        center = half + half[:size // 2][::-1]
        for entry in (0, 1):
            digits, exit_carry = normalize(base, center, entry)
            # Independent integer normalization checks every digit and carry.
            integer = sum(coefficient * base ** i for i, coefficient in enumerate(center)) + entry
            integer_digits = []
            for _ in center:
                integer, digit = divmod(integer, base)
                integer_digits.append(digit)
            require(tuple(integer_digits) == digits and integer == exit_carry,
                    "integer normalization mismatch")
            if exit_carry != 1 - entry:
                continue
            amount = rng.randrange(0, 9)
            for overflow in (0, 1):
                require(raw_center(base, pad(base, center, amount), entry, overflow)
                        == pad(base, raw_center(base, center, entry, overflow), amount),
                        "padding covariance mismatch")
                covariance_cases += 1

    # Explicit multiple trim: after a non-overflow decimal step, two neutral
    # layers can be removed at once.  Binary schedules need retiming, not a
    # pointwise assumption v<=1.
    require(raw_center(10, (4, 4, 10, 4, 4), 1, 0) == pad(10, (0,), 2),
            "two-layer decimal example failed")

    # Rejections are checked explicitly, including while running python -O.
    bad = cycles[2]
    require(not cycle_ok(2, (replace(bad[0], v=-1),) + bad[1:]), "negative trim accepted")
    require(not cycle_ok(2, (replace(bad[0], C=(1, 1)),) + bad[1:]), "bad center accepted")
    require(not cycle_ok(2, (replace(bad[0], B=(0,)),) + bad[1:]), "zero exterior accepted")
    require(not center_cycle_ok(10, [()], [0], [0], [0]), "empty center accepted")
    for source, target in (([0], [1]), ([1], [-1]), ([], []), ([1, 0], [1])):
        rejected = False
        try:
            padding_offsets(source, target)
        except ValueError:
            rejected = True
        require(rejected, "malformed schedule accepted")
    for period in range(1, 81):
        for mass in range(period + 1):
            schedule = balanced_schedule(period, mass)
            positions = [t for t, value in enumerate(schedule) if value]
            require(len(positions) == mass, "balanced schedule mass")
            if mass:
                gaps = [((positions[(i + 1) % mass] - position - 1) % period) + 1
                        for i, position in enumerate(positions)]
                require(max(gaps) - min(gaps) <= 1, "balanced schedule gaps")
    print(f"transformed_cycles={binary_count + nonbinary_count} "
          f"binary={binary_count} nonbinary={nonbinary_count} mirror_edges={edge_count}")
    print(f"padding_covariance={covariance_cases} random_schedules={schedule_cases} "
          "two_layer_example=PASS rejection_checks=PASS")
    print("SELFTEST PASSED")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    test = sub.add_parser("selftest")
    test.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    schedule = sub.add_parser("schedule")
    schedule.add_argument("overflow", help="complete overflow bit stream")
    schedule.add_argument("--phase", type=int, default=0)
    retime = sub.add_parser("retime")
    retime.add_argument("input", help="JSON certificate path, or - for stdin")
    retime.add_argument("--target", required=True, help="comma-separated nonnegative trim counts")
    args = parser.parse_args()
    try:
        if args.command == "selftest":
            _selftest(args.repo)
        elif args.command == "schedule":
            require(bool(args.overflow) and set(args.overflow) <= {"0", "1"},
                    "overflow stream must be a nonempty bit string")
            total = args.overflow.count("1")
            require(total % 2 == 0, "odd overflow total excludes a closed center")
            print("".join(map(str, balanced_schedule(len(args.overflow), total // 2, args.phase))))
        else:
            data = json.load(sys.stdin) if args.input == "-" else json.loads(Path(args.input).read_text())
            rows = data["edges"]
            require(isinstance(rows, list) and all(isinstance(row, list) and len(row) == 6 for row in rows),
                    "edges must be lists [B,C,B2,C2,u,v]")
            edges = tuple(Edge(*(tuple(word) for word in row[:4]), row[4], row[5]) for row in rows)
            target = tuple(int(value) for value in args.target.split(","))
            transformed, offsets = retime_cycle(data["base"], edges, target)
            carry, overflow = cycle_streams(data["base"], transformed)
            print(json.dumps({"base": data["base"], "edges": [edge.row() for edge in transformed],
                              "padding_offsets": offsets, "carry": carry, "overflow": overflow,
                              "center_trims": target, "checked": True}, separators=(",", ":")))
    except (ValueError, TypeError, IndexError, KeyError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
