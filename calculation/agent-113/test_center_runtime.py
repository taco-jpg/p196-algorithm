#!/usr/bin/env python3
"""Finite independent arithmetic and regression checks for Agent113's runtime.

Run with --binary PATH from extend_cauto.py --build-only.  --baseline PATH
also checks the unmodified cauto_fast executable on its safe original range.
No finite arithmetic test here proves the all-length automaton reduction.
"""
from __future__ import annotations

import argparse
from itertools import product
from pathlib import Path
import random
import re
import resource
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def center_step(base, word, entry, overflow, trim):
    """Independent positional-integer normalization, then exact pair sums."""
    width = len(word)
    if not width or tuple(word) != tuple(reversed(word)):
        return None
    if any(not 0 <= digit <= 2 * base - 2 for digit in word):
        return None
    value = sum(digit * base ** index for index, digit in enumerate(word)) + entry
    exit_carry, value = divmod(value, base ** width)
    if exit_carry != 1 - entry:
        return None
    digits = []
    for _ in word:
        value, digit = divmod(value, base)
        digits.append(digit)
    if overflow:
        digits.append((base - 1) * entry)
    image = tuple(left + right for left, right in zip(digits, reversed(digits)))
    if len(image) <= 2 * trim:
        return None
    if any(digit != base - 1 for digit in image[:trim] + image[len(image) - trim:]):
        return None
    return image[trim:len(image) - trim]


def direct_feasible(base, es, gs, vs, width):
    """Every symmetric initial word; the prescribed trim makes its path unique."""
    tested = 0
    feasible = False
    for half in product(range(2 * base - 1), repeat=(width + 1) // 2):
        word = half + half[:width // 2][::-1]
        initial = word
        tested += 1
        for entry, overflow, trim in zip(es, gs, vs):
            word = center_step(base, word, int(entry), int(overflow), int(trim))
            if word is None:
                break
        if word == initial:
            feasible = True
    return feasible, tested


def source_certificates():
    """Parse existing Lean certificate data only; no mirror arithmetic imports."""
    directory = ROOT / "lean/P196"
    paths = [directory / "Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean",
             directory / "Agent213KnownBaseMechanisms/KnownBases.lean"]
    certificates = {}
    for path in paths:
        source = path.read_text()
        definitions = {
            match[1]: tuple(map(int, match[2].split(','))) if match[2].strip() else ()
            for match in re.finditer(r"def (\w+)\s*:\s*List Nat\s*:=\s*\[([^\]]*)\]", source)
        }
        def word(text):
            text = text.strip()
            if text.startswith('['):
                return tuple(map(int, text[1:-1].split(','))) if text[1:-1].strip() else ()
            return definitions[text]
        for match in re.finditer(r"def cert(\d+)\s*:\s*List Edge\s*:=\s*(\[.*?\])\n\n", source, re.S):
            edges = []
            for fields in re.findall(r"⟨(.*?)⟩", match[2], re.S):
                tokens = re.findall(r"\[[^\]]*\]|[A-Za-z_]\w*|\d+", fields)
                require(len(tokens) == 6, "unexpected Lean edge data")
                edges.append(tuple(word(token) for token in tokens[:4]) +
                             (int(tokens[4]), int(tokens[5])))
            certificates[int(match[1])] = edges
    require(set(certificates) == {2, 4, 8, 11, 16, 17, 26, 32}, "missing source certificates")
    return certificates


def driver_for_certificate(base, edges):
    es, gs, vs = '', '', ''
    centers = []
    for exterior, center, _, center2, _, trim in edges:
        size = len(exterior)
        e = sum(value * base ** i for i, value in enumerate(exterior)) // base ** size
        g = (sum(value * base ** i for i, value in enumerate(reversed(exterior))) + 1 - e) // base ** size
        require(e in (0, 1) and g in (0, 1) and trim in (0, 1), "invalid control bits")
        require(center_step(base, center, e, g, trim) == center2, "source center edge failed")
        es += str(e)
        gs += str(g)
        vs += str(trim)
        centers.append(center)
    require(all(edges[t][3] == edges[(t + 1) % len(edges)][1]
                for t in range(len(edges))), "source center cycle failed")
    return es, gs, vs, centers


def padding_control(base, es, gs, vs, centers, new_vs):
    """Construct and individually verify one finite test with a long segment."""
    shifts = [0]
    for old, new in zip(vs, new_vs):
        shifts.append(shifts[-1] + int(old) - int(new))
    require(shifts[-1] == 0, "control does not close")
    offset = -min(shifts)
    padded = [((base - 1,) * (offset + shifts[t]) + center +
               (base - 1,) * (offset + shifts[t])) for t, center in enumerate(centers)]
    for t, center in enumerate(padded):
        require(center_step(base, center, int(es[t]), int(gs[t]), int(new_vs[t])) ==
                padded[(t + 1) % len(padded)], "finite padded control failed")
    return es, gs, new_vs, padded


def invoke(binary, arguments, timeout, memory_mib=0):
    def limit_memory():
        ceiling = memory_mib * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (ceiling, ceiling))
    try:
        return subprocess.run([str(binary), *map(str, arguments)], text=True,
                              capture_output=True, timeout=timeout,
                              preexec_fn=limit_memory if memory_mib else None)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"UNDECIDED: test command timed out: {arguments}") from exc


def parse_result(result, base, es, gs, vs, require_complete=True):
    require(result.returncode == 0, f"solver exit {result.returncode}: {result.stderr[-1500:]}")
    if require_complete:
        require(not re.search(r"CAPPED|NOPERIOD|status=(?:capped|noperiod)", result.stdout),
                f"UNDECIDED test case: {result.stdout[-1500:]}")
    widths, witnesses = set(), 0
    for line in result.stdout.splitlines():
        if not line.startswith('FEASIBLE'):
            continue
        width = int(re.search(r"\bm0=(\d+)", line)[1])
        widths.add(width)
        rows = re.findall(r" C(\d+)=\[([^\]]*)\]", line)
        require(len(rows) == len(es), "feasible claim lacks complete requested witness")
        words = [tuple(map(int, value.split(','))) if value else () for _, value in rows]
        require([int(index) for index, _ in rows] == list(range(len(es))), "bad witness phases")
        require(len(words[0]) == width, "bad initial witness width")
        for t, center in enumerate(words):
            require(center_step(base, center, int(es[t]), int(gs[t]), int(vs[t])) ==
                    words[(t + 1) % len(words)], f"invalid solver witness at phase {t}")
        witnesses += 1
    statuses = re.findall(r"\bstatus=(\w+)", result.stdout)
    require(len(statuses) == 1, f"missing or multiple completion status: {result.stdout[-1000:]}")
    return widths, witnesses, statuses[0]


def arguments(base, es, gs, vs, lo, hi, extra=()):
    return [base, es, gs, lo, hi, '-v', vs, '-w', '-cap', 500000, *extra]


def bounded_checks(binary, baseline, timeout):
    cases = starts = witnesses = comparisons = 0
    for base in (2, 3, 4):
        for period in (1, 2, 3):
            bits = [''.join(map(str, row)) for row in product((0, 1), repeat=period)]
            for es, gs in product(bits, repeat=2):
                weight = gs.count('1')
                if weight % 2:
                    continue
                for vs in bits:
                    if vs.count('1') * 2 != weight:
                        continue
                    expected = set()
                    for width in range(1, 5):
                        possible, count = direct_feasible(base, es, gs, vs, width)
                        starts += count
                        if possible:
                            expected.add(width)
                    command = arguments(base, es, gs, vs, 1, 4)
                    actual, count, _ = parse_result(invoke(binary, command, timeout), base, es, gs, vs)
                    require(actual == expected, f"direct disagreement: {(base,es,gs,vs,expected,actual)}")
                    witnesses += count
                    legacy, count, _ = parse_result(invoke(binary, command + ['-legacy'], timeout),
                                                    base, es, gs, vs)
                    require(legacy == expected, "legacy versus integer disagreement")
                    witnesses += count
                    comparisons += 1
                    if baseline:
                        old, count, _ = parse_result(invoke(baseline, command, timeout), base, es, gs, vs)
                        require(old == expected, "baseline versus integer disagreement")
                        witnesses += count
                        comparisons += 1
                    cases += 1
    print(f"bounded stream_patterns={cases} initial_words={starts} comparisons={comparisons} witnesses={witnesses} PASS")


def all_length_differential(binary, baseline, timeout, count):
    rng = random.Random(113)
    cases = witnesses = undecided = 0
    while cases < count:
        base = rng.choice((2, 3, 4, 6, 10, 11))
        period = rng.randint(2, 6)
        es = ''.join(rng.choice('01') for _ in range(period))
        gs = ''.join(rng.choice('01') for _ in range(period))
        weight = gs.count('1')
        if not weight or weight % 2:
            continue
        selected = set(rng.sample(range(period), weight // 2))
        vs = ''.join('1' if t in selected else '0' for t in range(period))
        command = arguments(base, es, gs, vs, 1, 1, ['-allm'])
        new = parse_result(invoke(binary, command, timeout), base, es, gs, vs, False)
        legacy = parse_result(invoke(binary, command + ['-legacy'], timeout), base, es, gs, vs, False)
        require(new[0] == legacy[0] and new[2] == legacy[2], "all-length fast/legacy disagreement")
        witnesses += new[1] + legacy[1]
        if baseline:
            old = parse_result(invoke(baseline, command, timeout), base, es, gs, vs, False)
            require(new[0] == old[0] and new[2] == old[2], "all-length baseline disagreement")
            witnesses += old[1]
        undecided += new[2] in ('capped', 'noperiod')
        cases += 1
    print(f"allm patterns={cases} matching_undecided={undecided} witnesses={witnesses} PASS")


def positive_checks(binary, timeout):
    drivers = {base: driver_for_certificate(base, edges)
               for base, edges in source_certificates().items()}
    cases = witnesses = 0
    controls = [(f"source-base{base}", base, *driver) for base, driver in sorted(drivers.items())]
    for base, repeats in ((4, 6), (8, 5), (32, 4), (26, 10)):
        es, gs, vs, centers = drivers[base]
        controls.append((f"repeated-base{base}", base, es * repeats, gs * repeats,
                         vs * repeats, centers * repeats))
    es, gs, vs, centers = drivers[32]
    padded = padding_control(32, es * 4, gs * 4, vs * 4, centers * 4, '1111' + '0' * 44)
    controls.append(('segment45-base32', 32, *padded))
    # Independent center-only positive, P=33; no exterior certificate claimed.
    controls.append(('center-only-P33', 6, '110' * 11, '000' * 11,
                     '000' * 11, [(0,), (2,), (6,)] * 11))
    for label, base, es, gs, vs, centers in controls:
        for t, center in enumerate(centers):
            require(center_step(base, center, int(es[t]), int(gs[t]), int(vs[t])) ==
                    centers[(t + 1) % len(centers)], f"invalid independent control {label}")
        width = len(centers[0])
        extra = ['-cap', 2000000] if label == 'repeated-base26' else []
        command = arguments(base, es, gs, vs, width, width, extra)
        actual, found, _ = parse_result(invoke(binary, command, timeout), base, es, gs, vs)
        require(width in actual, f"known positive lost: {label}")
        witnesses += found
        cases += 1
        print(f"positive {label} P={len(es)} m0={width} PASS")
        if label == 'repeated-base26':
            # P40/G20/K10 requires 270 packed bits; exercise the widened key.
            actual, found, _ = parse_result(invoke(binary, command + ['-legacy'],
                                                   min(timeout, 30), memory_mib=2048),
                                            base, es, gs, vs)
            require(width in actual, '270-bit legacy positive lost')
            witnesses += found
            cases += 1
            print('positive legacy-base26 P=40 packed_bits=270 PASS')
    print(f"positive cases={cases} source_edges={sum(len(v[3]) for v in drivers.values())} solver_witnesses={witnesses} PASS")


def rejection_checks(binary, timeout):
    valid = ['2', '1010', '1010', '2', '2', '-v', '0001']
    tests = [[], valid[:-1], ['1', *valid[1:]], ['63', *valid[1:]],
             ['2', '', '', '1', '1', '-v', ''],
             ['2', '1010', '101', '1', '1', '-v', '0001'],
             ['2', '10x0', '1010', '1', '1', '-v', '0001'],
             ['2', '1010', '10x0', '1', '1', '-v', '0001'],
             ['2', '1010', '1010', '1', '1', '-v', '001'],
             ['2', '1010', '1010', '1', '1', '-v', '000x'],
             ['2', '1010', '1010', '1', '1', '-v', '0000'],
             ['2', '1' * 49, '0' * 49, '1', '1', '-v', '0' * 49],
             ['2', '1010', '1110', '1', '1', '-v', '0001'],
             [*valid, '-cap', '0'], [*valid, '-cap', '-1'],
             [*valid, '-jgen', '0'], [*valid, '-unknown'],
             ['2', '1010', '1010', '0', '1', '-v', '0001'],
             ['2', '1010', '1010', '2', '1', '-v', '0001']]
    for command in tests:
        result = invoke(binary, command, timeout)
        require(result.returncode != 0, f"invalid input accepted: {command}")
        require(not re.search(r"FEASIBLE|status=(?:none|hit)", result.stdout), "invalid input advertised result")
    print(f"invalid_inputs={len(tests)} PASS")
    # This 48-phase repetition is already known positive by direct replay.
    # It must be reported undecided at this small cap, never absent.
    es, gs, vs, centers = driver_for_certificate(26, source_certificates()[26])
    command = arguments(26, es * 12, gs * 12, vs * 12, len(centers[0]), len(centers[0]))
    result = invoke(binary, command, timeout)
    _, _, status = parse_result(result, 26, es * 12, gs * 12, vs * 12, False)
    require(status == 'capped' and 'CAPPED' in result.stdout, 'known positive cap mislabeled')
    print('known_positive_P48 cap=500000 status=CAPPED-UNDECIDED PASS')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', required=True, type=Path)
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--timeout', type=float, default=45)
    parser.add_argument('--allm-cases', type=int, default=32)
    parser.add_argument('--only', choices=('bounded', 'allm', 'positive', 'guards', 'all'), default='all')
    args = parser.parse_args()
    require(args.binary.is_file(), 'missing binary')
    if args.only in ('all', 'bounded'):
        bounded_checks(args.binary, args.baseline, args.timeout)
    if args.only in ('all', 'allm'):
        all_length_differential(args.binary, args.baseline, args.timeout, args.allm_cases)
    if args.only in ('all', 'positive'):
        positive_checks(args.binary, args.timeout)
    if args.only in ('all', 'guards'):
        rejection_checks(args.binary, args.timeout)
    print('ALL TESTS PASSED (finite COMPUTED regression only; no new Lean theorem)')


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, RuntimeError) as exc:
        print(f'FAILED: {exc}', file=sys.stderr)
        raise SystemExit(1)
