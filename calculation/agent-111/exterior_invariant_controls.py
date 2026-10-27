#!/usr/bin/env python3
"""Production controls for both directions of the external exterior checker.

Fixtures are untrusted candidate languages. Rejected invariants are not
nonexistence proofs, and a terminal overlap is not a physical B certificate.
The base6 two-lap exterior fixture is credited to Agent105, issue289
comment6433504667; this script independently replays it without a new census.
"""
from __future__ import annotations

import argparse
from collections import deque
import json
import os
from pathlib import Path
import re
import tempfile

from exterior_first_language import (Candidate, TARGET_E, TARGET_G,
    empty_candidate, first_candidate, positive_phase_product, render, universal_candidate)
import exterior_invariant_arithmetic as arithmetic
from exterior_invariant import run


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def bits(word):
    return tuple(map(int, word))


def accepts(candidate, word):
    state = candidate.start
    for label in word:
        state = candidate.edges[state].get(label)
        if state is None:
            return False
    return candidate.accepting[state]


def positive_power(word, unit):
    return bool(word) and len(word) % len(unit) == 0 and all(
        label == unit[i % len(unit)] for i, label in enumerate(word))


def terminal_candidate(base, e, g):
    word = arithmetic.terminal_word(base, bits(e), bits(g))
    return positive_phase_product(base, e, g, [[label] for label in word])


def complement_terminal(base, e, g):
    """All positive typed phase words except the exact terminal word's powers."""
    terminal = arithmetic.terminal_word(base, bits(e), bits(g))
    alphabet = [[] for _ in g]
    for label in arithmetic.symbols(base, bits(g)):
        alphabet[label // (4 * base)].append(label)
    initial = (0, False, False)
    indices, keys = {initial: 0}, [initial]
    result = Candidate(base, e, g, 0, [], [])
    for phase, differs, started in keys:
        result.accepting.append(phase == 0 and differs and started)
        row = {}
        for label in alphabet[phase]:
            target = ((phase + 1) % len(g), differs or label != terminal[phase], True)
            if target not in indices:
                indices[target] = len(keys)
                keys.append(target)
            row[label] = indices[target]
        result.edges.append(row)
    return result


def replay_counterexamples(candidate, stdout):
    rows_checked = examples = 0
    for line in stdout.splitlines():
        if not line.startswith("COUNTEREXAMPLE "):
            continue
        match = re.fullmatch(r"COUNTEREXAMPLE obligation=(\S+) word=(\[.*?\]) "
                             r"input=(\[.*?\]) rows=(\[.*\])", line)
        require(match is not None, "unparsed production counterexample")
        obligation = match[1]
        output, source, selected = [json.loads(match[i]) for i in (2, 3, 4)]
        root = arithmetic.root_word(candidate.base, bits(candidate.g))
        terminal = arithmetic.terminal_word(candidate.base, bits(candidate.e), bits(candidate.g))
        if obligation == "TERMINAL":
            require(positive_power(output, terminal), "terminal witness is not a positive whole word")
            backward = "direction=backward" in stdout
            require(accepts(candidate, output) != backward,
                    "terminal witness has incorrect candidate membership")
            require(source == output and not selected,
                    "ordinary terminal witness has inconsistent path metadata")
        else:
            first = obligation in ("FIRST", "FIRST_DISJOINT")
            reverse = obligation == "PREDECESSOR"
            require(obligation in ("FIRST", "GENERIC", "PREDECESSOR", "FIRST_DISJOINT"),
                    "unknown cyclic obligation")
            require(bool(output) and len(output) == len(source) == len(selected),
                    "incomplete cyclic witness")
            require(positive_power(source, root) if first else accepts(candidate, source),
                    "cyclic input word misses its full source language")
            require(accepts(candidate, output) == (obligation == "FIRST_DISJOINT"),
                    "cyclic output has incorrect candidate membership")
            for i, (incoming, emitted, outgoing) in enumerate(selected):
                require(emitted == output[i] and outgoing == selected[(i + 1) % len(selected)][0],
                        "broken emitted symbol or coefficient closure")
                lookup = output[i] if reverse else source[i]
                expected_output = source[i] if reverse else output[i]
                require((incoming, expected_output, outgoing) in arithmetic.local_rows(
                    candidate.base, bits(candidate.g), lookup, first=first),
                    "counterexample row fails independent integer arithmetic")
                rows_checked += 1
        examples += 1
    return examples, rows_checked


def physical_two_lap():
    base, e, g = 6, (0, 1), (0, 1)
    original = [(4, 7, 7, 8, 3), (9, 3, 4, 5, 8),
                (4, 7, 7, 10, 2, 2), (9, 3, 4, 9)]
    trims = (0, 0, 2, 0)
    for t, word in enumerate(original):
        entering, overflow, raw = arithmetic.exterior_step(base, word)
        require((entering, overflow) == (e[t % 2], g[t % 2]), "credited fixture streams changed")
        require(raw == original[(t + 1) % 4] + (base - 1,) * trims[t],
                "credited physical exterior edge fails integer replay")
    width = max(map(len, original))
    padded = [word + (base - 1,) * (width - len(word)) for word in original]
    cuts = []
    for position in range(width + 1):
        full = arithmetic.cut_word(base, padded, e * 2, g * 2, position)
        cut = []
        for label in full:
            phase, low, high, previous = arithmetic.decode(base, g * 2, label)
            cut.append(arithmetic.encode(base, phase % 2, low, high, previous))
        cuts.append(tuple(cut))
    require(cuts[0] == arithmetic.root_word(base, g) * 2, "two-lap physical root mismatch")
    require(cuts[-1] == arithmetic.terminal_word(base, e, g) * 2, "two-lap terminal mismatch")
    checked = 0
    for position in range(width):
        for t in range(4):
            row = (padded[t][position], cuts[position + 1][t], padded[(t + 1) % 4][position])
            require(row in arithmetic.local_rows(base, g, cuts[position][t], first=position == 0),
                    "actual two-lap cut transition fails the production contract")
            checked += 1
    return {"base": base, "primitive_driver_period": 2, "physical_period": 4,
            "common_width": width, "original_edges_replayed": 4,
            "complete_cut_words": len(cuts), "cyclic_tiles_replayed": checked}


def cases():
    target_first, _ = first_candidate(10, TARGET_E, TARGET_G)
    yield "empty_valid_forward", empty_candidate(10, "0", "1"), False, 0, None, None
    yield "nonempty_valid_backward", terminal_candidate(10, "0", "1"), True, 0, None, None
    yield "base2_two_lap_FIRST", empty_candidate(2, "0", "1"), False, 1, "FIRST", 2
    yield "p24_missing_FIRST", empty_candidate(10, TARGET_E, TARGET_G), False, 1, "FIRST", 24
    yield "p24_frontier_not_invariant", target_first, False, 1, "GENERIC", 24
    yield "p24_universal_terminal", universal_candidate(10, TARGET_E, TARGET_G), False, 1, "TERMINAL", 24
    yield "p24_missing_terminal", empty_candidate(10, TARGET_E, TARGET_G), True, 1, "TERMINAL", 24
    yield "p24_terminal_not_backward_invariant", terminal_candidate(10, TARGET_E, TARGET_G), True, 1, "PREDECESSOR", 24
    yield "p24_universal_FIRST_overlap", universal_candidate(10, TARGET_E, TARGET_G), True, 1, "FIRST_DISJOINT", 24
    yield "base6_excluding_real_two_lap", complement_terminal(6, "01", "01"), False, 1, "GENERIC", None


def binary_controls(binary, sanitizer=False):
    completed, total_examples, total_rows = [], 0, 0
    with tempfile.TemporaryDirectory(prefix="agent111-exterior-controls-") as temp:
        path = Path(temp) / "candidate.txt"
        for name, candidate, backward, status, obligation, length in cases():
            path.write_text(render(candidate))
            result = run(binary, path, backward=backward, timeout=30,
                         memory_mb=None if sanitizer else 4096)
            require(result.returncode == status,
                    f"{name} wrong status{result.returncode}: {result.stdout}\n{result.stderr}")
            require(not any(x in result.stdout + result.stderr for x in
                    ("UNDECIDED", "INVALID_OR_UNSUPPORTED", "VERIFIER_ERROR")),
                    f"{name} did not complete")
            if status == 0:
                require(re.search(r"^VALID_INVARIANT ", result.stdout, re.M), "missing verified conclusion")
            else:
                require(re.search(rf"^REJECTED_INVARIANT obligation={obligation}\b", result.stdout, re.M),
                        f"{name} failed another obligation")
                if length is not None:
                    match = re.search(r"^COUNTEREXAMPLE .*? word=(\[.*?\]) ", result.stdout, re.M)
                    require(match and len(json.loads(match[1])) == length,
                            f"{name} shortest word length differs")
            examples, row_count = replay_counterexamples(candidate, result.stdout)
            require(examples == int(status != 0), "wrong number of obligation counterexamples")
            total_examples += examples
            total_rows += row_count
            completed.append(name)

        # Limits must interrupt proof obligations, never imply mathematical absence.
        limits = 0
        target = terminal_candidate(10, TARGET_E, TARGET_G)
        for backward in (False, True):
            path.write_text(render(target if backward else empty_candidate(10, TARGET_E, TARGET_G)))
            for options in ({"state_cap": 30}, {"edge_cap": 30}, {"work_cap": 1}):
                result = run(binary, path, backward=backward, timeout=30,
                             memory_mb=None if sanitizer else 4096, **options)
                require(result.returncode == 3 and "UNDECIDED" in result.stderr,
                        f"resource control did not interrupt: {options}, {result.stdout}, {result.stderr}")
                require(not re.search(r"^(?:VALID|REJECTED)_INVARIANT ", result.stdout, re.M),
                        "resource limit produced a conclusion")
                limits += 1

        text = render(empty_candidate(10, TARGET_E, TARGET_G))
        corruptions = [text.replace("P196_EXTERIOR_INVARIANT 1", "P196_EXTERIOR_INVARIANT 2"),
                       text.replace("base 10", "base 1"),
                       text.replace("period 24", "period 25"),
                       text.replace("g " + TARGET_G, "g " + "0" * 24),
                       text.replace("start 0", "start 1"),
                       text.replace("accept 0", "accept 1 2"),
                       text.replace("transitions 0", "transitions 1\n0 960 0"),
                       text.replace("transitions 0", "transitions 1\n0 81 0"),
                       text.replace("transitions 0", "transitions 2\n0 0 0\n0 0 0"),
                       text.replace("end", ""), text + "surplus\n"]
        for malformed in corruptions:
            path.write_text(malformed)
            result = run(binary, path, timeout=30, memory_mb=None if sanitizer else 4096)
            require(result.returncode == 2 and "INVALID_OR_UNSUPPORTED" in result.stderr,
                    f"malformed invariant was not rejected: {result.stdout}, {result.stderr}")
            require(not re.search(r"^(?:VALID|REJECTED)_INVARIANT ", result.stdout, re.M),
                    "malformed data yielded a conclusion")
    return {"sanitizer": sanitizer, "cases": completed, "counterexamples": total_examples,
            "independently_replayed_rows": total_rows, "resource_interruptions": limits,
            "malformed_inputs": len(corruptions)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", required=True)
    parser.add_argument("--sanitizer-binary")
    args = parser.parse_args()
    print("CREDITED_PHYSICAL_TWO_LAP " + json.dumps(physical_two_lap(), sort_keys=True), flush=True)
    print("EXTERIOR_PRODUCTION_CONTROLS " + json.dumps(binary_controls(args.binary), sort_keys=True), flush=True)
    if args.sanitizer_binary:
        # LeakSanitizer cannot inspect processes in this sandbox; address and
        # undefined-behavior checking remain enabled in the sanitizer build.
        os.environ["ASAN_OPTIONS"] = "detect_leaks=0"
        print("EXTERIOR_PRODUCTION_CONTROLS " + json.dumps(binary_controls(args.sanitizer_binary, True), sort_keys=True), flush=True)
    print("ALL EXTERIOR INVARIANT CONTROLS PASSED")


if __name__ == "__main__":
    main()
