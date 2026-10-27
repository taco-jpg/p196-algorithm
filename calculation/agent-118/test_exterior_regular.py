#!/usr/bin/env python3
"""Independent arithmetic and language controls for the saturation experiment.

One symbol encodes (L,H,Y) as L+16H+256Y, with four carry bits in each
mask.  It represents four time steps with overflow pattern 1000.  No production
transition helper is imported: tiles use direct integer normalization, and the
known B witness is replayed using whole-word integers in both orientations.

The positive B0 fixture below is credited to Agent108 PR386, pinned head
9b3f0c26d3482b93e4f13a6fe9194e8d3dcb1a5f.  It was reproduced by that PR's
saturation_mdd.cpp at G=3, first terminal width53.  It is B-ONLY, not a common
center cycle or a cycleOK certificate.  Finite-G checks do not imply all-G
language equivalence.  All resource failures remain UNDECIDED.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from functools import lru_cache
import itertools
import json
from pathlib import Path
import re
import resource
import subprocess
import tempfile
import time

from test_regular import NFA, positive_blocks, finite_language, union, equivalent, difference_witness


INITIAL = 272
KNOWN_TRIPLE = (2469, 2409, 90)
KNOWN_B0 = (10, 4, 7, 5, 13, 6, 11, 1, 9, 16, 16, 18, 10, 9, 4, 8, 1, 7,
            0, 2, 15, 15, 9, 7, 7, 0, 9, 5, 17, 2, 16, 3, 10, 17, 9, 9,
            12, 11, 3, 7, 9, 15, 6, 5, 18, 7, 3, 1, 3, 16, 18, 4)
KNOWN_E = "010110101001"
KNOWN_G3_COUNTS = (1, 8, 64, 244, 472, 1017, 1338, 3186, 1758, 1017, 600,
                   456, 312, 288, 24, 60, 252, 24, 192, 1020, 1968, 2271,
                   1500, 2538, 1944, 828, 654, 1062, 2103, 2211, 1746, 2544,
                   1542, 1350, 1374, 2184, 2028, 1728, 2580, 3570, 3846,
                   6774, 4902, 4476, 5328, 5934, 4614, 4542, 4092, 4290,
                   5850, 6588, 4488, 5622)


class Limit(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def encode(low, high, partner):
    return low + 16 * high + 256 * partner


def decode(symbol):
    return symbol & 15, (symbol >> 4) & 15, symbol >> 8


def terminal(symbol):
    low, high, partner = decode(symbol)
    return high == 15 ^ low and partner == 9 * (low & 1)


def trace_tile(symbol, coefficient, new_high):
    """Normalize each of four coefficients independently from both sides."""
    low, high, partner = decode(symbol)
    new_low, new_partner, column = 0, None, []
    for phase in range(4):
        reverse_carry, reverse_digit = divmod(coefficient + ((new_high >> phase) & 1), 10)
        if reverse_carry != ((high >> phase) & 1):
            return None
        forward_carry, forward_digit = divmod(coefficient + ((low >> phase) & 1), 10)
        new_low += forward_carry * 2**phase
        column.append(coefficient)
        if phase == 0:
            new_partner = reverse_digit
            coefficient = forward_digit + partner
        else:
            coefficient = forward_digit + reverse_digit
    target = encode(new_low, new_high, new_partner)
    return target, coefficient, tuple(column), all(x > 0 for x in column)


@lru_cache(None)
def tiles(symbol, coefficient):
    return tuple(result for high in range(16)
                 if (result := trace_tile(symbol, coefficient, high)) is not None)


def relation(symbol, coefficient, first=False):
    return ((out, end) for out, end, _, positive in tiles(symbol, coefficient)
            if not first or positive)


def word_image(word, provider, boundaries=range(19)):
    """Explicit definition on a single complete input word, preserving closure."""
    if not word:
        return set()
    result, output = set(), []

    def visit(index, coefficient, initial):
        if index == len(word):
            if coefficient == initial:
                result.add(tuple(output))
            return
        for symbol, following in provider(word[index], coefficient):
            output.append(symbol)
            visit(index + 1, following, initial)
            output.pop()

    for initial in boundaries:
        visit(0, initial, initial)
    return result


def explicit_image(words, provider, boundaries=range(19)):
    return {out for word in words for out in word_image(word, provider, boundaries)}


def image_nfa(source, provider, boundaries=range(19), close=True, nonempty=True):
    """All-word image; switches disabling constraints are regression bugs only."""
    starts = {(q, x, x, False) for q in source.initials for x in boundaries}
    result = NFA(starts)
    queue, seen, finals = deque(starts), set(starts), set()
    while queue:
        state = queue.popleft()
        q, current, initial, used = state
        if q in source.finals and (used or not nonempty) and (not close or current == initial):
            finals.add(state)
        for old, targets in source.edges.get(q, {}).items():
            for out, following in provider(old, current):
                for target_q in targets:
                    target = (target_q, following, initial, True)
                    result.add(state, out, target)
                    if target not in seen:
                        require(len(seen) < 200000, "independent NFA state cap")
                        seen.add(target)
                        queue.append(target)
    result.finals = frozenset(finals)
    return result


def difference(left, right):
    """Exact DFA of a language difference via two subset constructions."""
    start = (left.initials, right.initials)
    result = NFA({start})
    queue, seen, finals = deque([start]), {start}, set()
    while queue:
        a, b = queue.popleft()
        if a & left.finals and not b & right.finals:
            finals.add((a, b))
        labels = {label for q in a for label in left.edges.get(q, {})}
        for label in labels:
            target = left.step(a, label), right.step(b, label)
            result.add((a, b), label, target)
            if target not in seen:
                require(len(seen) < 200000, "independent difference state cap")
                seen.add(target)
                queue.append(target)
    result.finals = frozenset(finals)
    return result


def arithmetic_controls(totals, deadline):
    records = set()
    for symbol in range(2560):
        if time.monotonic() > deadline:
            raise Limit("local_tile_wall_cap")
        for left in range(19):
            for out, right, column, positive in tiles(symbol, left):
                require(0 <= out < 2560 and 0 <= right <= 18, "tile range violation")
                record = (symbol, out, left, right, int(positive), *column)
                require(record not in records, "duplicate independent tile")
                records.add(record)
                totals["positive_local_tiles"] += positive
            totals["local_input_rows"] += 1
    require(len(records) == 48640, "generic tile count differs from16*16*19*10")
    totals["generic_local_tiles"] += len(records)
    neutral = {symbol for symbol in range(2560) if terminal(symbol)}
    require(len(neutral) == 16, "neutral alphabet has incorrect size")
    for symbol in neutral:
        low, high, _ = decode(symbol)
        row = trace_tile(symbol, 9, high)
        require(row == (symbol, 9, (9, 9, 9, 9), True), "all-9 neutral padding failed")
        require(decode(symbol)[1] == 15 ^ low, "neutral complement changed")
        totals["all_e_padding_controls"] += 1
    require(trace_tile(16, 10, 0) == (1, 0, (10, 0, 0, 0), False),
            "FIRST-positive control fixture changed")
    require((1, 0) in set(relation(16, 10)) and (1, 0) not in set(relation(16, 10, True)),
            "FIRST checked only the initial coefficient")
    totals["first_column_controls"] += 1

    source = positive_blocks([(INITIAL,)])
    first = image_nfa(source, lambda s, x: relation(s, x, True))
    expected = positive_blocks([(65,), (337,)])
    require(equivalent(first, expected), "unrestricted FIRST language is not{65,337}+")
    for length in (1, 2, 3, 4):
        inputs = {(INITIAL,) * length}
        require(first.words(length) == explicit_image(inputs, lambda s, x: relation(s, x, True)),
                "FIRST finite-word slice mismatch")
        totals["first_language_slices"] += 1
    totals["exact_first_language_identities"] += 1
    return records


def language_controls(totals):
    table = {("a", 0): (("p", 1),), ("a", 1): (("q", 0),)}
    provider = lambda s, x: table.get((s, x), ())
    source = positive_blocks([("a",)])
    exact = image_nfa(source, provider, (0, 1))
    missing_close = image_nfa(source, provider, (0, 1), close=False)
    require(exact.accepts(("p", "q")) and not exact.accepts(("p",)),
            "cyclic image closed at an intermediate accepting state")
    require(missing_close.accepts(("p",)), "missing final closure counterexample changed")
    require(equivalent(exact, union(positive_blocks([("p", "q")]),
                                   positive_blocks([("q", "p")]))),
            "global alternating language identity failed")
    totals["closing_counterexamples"] += 2

    def identity(s, x):
        return ((s, 0),) if x == 0 else ()

    correlated = positive_blocks([("a", "a"), ("b", "b")])
    require(not image_nfa(correlated, identity, (0,)).accepts(("a", "b")),
            "input path correlation lost")
    require(image_nfa(positive_blocks([("a",), ("b",)]), identity, (0,)).accepts(("a", "b")),
            "Cartesian relaxation control changed")
    totals["correlation_counterexamples"] += 1
    even = positive_blocks([("a", "a")])
    require(not image_nfa(even, identity, (0,)).accepts(("a",))
            and image_nfa(source, identity, (0,)).accepts(("a",)),
            "input endpoint control changed")
    totals["endpoint_counterexamples"] += 1
    empty = finite_language({()})
    require(not image_nfa(empty, identity, (0,)).accepts(())
            and image_nfa(empty, identity, (0,), nonempty=False).accepts(()),
            "empty word scope control failed")
    totals["empty_word_counterexamples"] += 1

    rotations = [KNOWN_TRIPLE[i:] + KNOWN_TRIPLE[:i] for i in range(3)]
    known = union(union(*(positive_blocks([word]) for word in rotations[:2])),
                  positive_blocks([rotations[2]]))
    mixed = positive_blocks(rotations)
    bad_mix = rotations[0] + rotations[1]
    require(mixed.accepts(bad_mix) and not known.accepts(bad_mix), "mixed known rotations accepted")
    terminal_words = positive_blocks([(s,) for s in range(2560) if terminal(s)])
    bad = difference(terminal_words, known)
    require(not bad.accepts(()) and bad.accepts((KNOWN_TRIPLE[0],))
            and all(not bad.accepts(word) for word in rotations) and bad.accepts(bad_mix),
            "Bad=T+ minus K language changed")
    require(len(known.words(3)) == len(known.words(6)) == 3 and len(mixed.words(6)) == 9,
            "known-language repetition semantics changed")
    totals["known_language_controls"] += 6

    # Only the seed subtracts K.  A K word may be a necessary intermediate
    # predecessor of Bad; removing it again would create a false obstruction.
    forward = {("s", 0): (("k", 0),), ("k", 0): (("k", 0), ("b", 0)),
               ("b", 0): (("b", 0),)}
    reverse = defaultdict(list)
    for (old, left), choices in forward.items():
        for new, right in choices:
            reverse[(new, left)].append((old, right))
    inverse = lambda s, x: reverse.get((s, x), ())
    seed, excluded = positive_blocks([("b",)]), positive_blocks([("k",)])
    pre1 = image_nfa(seed, inverse, (0,))
    pre2 = image_nfa(pre1, inverse, (0,))
    wrong = image_nfa(difference(pre1, excluded), inverse, (0,))
    require(pre1.accepts(("k",)) and pre2.accepts(("s",)) and not wrong.accepts(("s",)),
            "repeated-K-subtraction counterexample changed")
    require(difference_witness(seed, pre1, equivalence=False) is None
            and difference_witness(pre1, pre2, equivalence=False) is None,
            "self-loop seed preimages are not ascending")
    totals["backward_seed_counterexamples"] += 1


def number(word):
    result = 0
    for coefficient in reversed(word):
        result = 10 * result + coefficient
    return result


def fixed_digits(value, width):
    result = []
    for _ in range(width):
        value, digit = divmod(value, 10)
        result.append(digit)
    return tuple(result)


def exterior_step(word):
    """Whole-word integer normalization, independent of cut/column relations."""
    require(word and word[0] != 0 and all(0 <= x <= 18 for x in word), "bad B word")
    width = len(word)
    low_value = number(word)
    carry = low_value // 10**width
    require(carry in (0, 1), "invalid whole-word carry")
    right_value = number(word[::-1]) + 1 - carry
    overflow = right_value // 10**width
    require(overflow in (0, 1), "invalid whole-word overflow")
    left, right = fixed_digits(low_value, width), fixed_digits(right_value, width)[::-1]
    if overflow:
        left, right = left + (9 * (1 - carry),), (1,) + right
    raw = tuple(a + b for a, b in zip(left, right))
    end = len(raw)
    while end and raw[end - 1] == 9:
        end -= 1
    return raw[:end], carry, overflow, len(raw) - end


def positive_control(totals):
    words, e, overflow, trims = [], [], [], []
    current = KNOWN_B0
    for _ in range(12):
        words.append(current)
        current, carry, flag, trim = exterior_step(current)
        e.append(carry); overflow.append(flag); trims.append(trim)
    require(current == KNOWN_B0 and "".join(map(str, e)) == KNOWN_E
            and tuple(overflow) == (1, 0, 0, 0) * 3 and sum(trims) == 3,
            "credited P12 exterior witness failed whole-integer replay")
    width = max(map(len, words))
    require(width == 53, "credited P12 common width changed")
    padded = [word + (9,) * (width - len(word)) for word in words]
    lower, higher, right_digits = [], [], []
    for t, word in enumerate(padded):
        low = [0]
        for coefficient in word:
            low.append((coefficient + low[-1]) // 10)
        high, rd = [0] * (width + 1), [0] * width
        high[width] = 1 - e[t]
        for k in range(width - 1, -1, -1):
            high[k], rd[k] = divmod(word[k] + high[k + 1], 10)
        require(low[-1] == e[t] and high[0] == overflow[t], "padded carry boundary differs")
        lower.append(low); higher.append(high); right_digits.append(rd)
    cuts = []
    for k in range(width + 1):
        cuts.append(tuple(encode(sum(lower[4 * s + t][k] << t for t in range(4)),
                                 sum(higher[4 * s + t][k] << t for t in range(4)),
                                 1 if k == 0 else right_digits[4 * s][k - 1])
                          for s in range(3)))
    require(cuts[0] == (INITIAL,) * 3 and all(terminal(s) for s in cuts[-1]),
            "known cut path misses physical or full neutral boundary")
    for k in range(width):
        for s in range(3):
            coefficient = padded[4 * s][k]
            new_high = decode(cuts[k + 1][s])[1]
            tile = trace_tile(cuts[k][s], coefficient, new_high)
            expected_column = tuple(padded[4 * s + t][k] for t in range(4))
            require(tile is not None and tile[:3] ==
                    (cuts[k + 1][s], padded[(4 * s + 4) % 12][k], expected_column),
                    "whole-integer witness disagrees with independent block arithmetic")
            require(k != 0 or tile[3], "known FIRST column contains zero")
        totals["positive_columns_replayed"] += 1
    totals["positive_exterior_edges_replayed"] += 12
    totals["positive_terminal_words"] += 1
    return cuts


def child_limits():
    memory = 2 * 1024**3
    resource.setrlimit(resource.RLIMIT_AS, (memory, memory))


def checked_run(binary, arguments, deadline, data=None):
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise Limit("test_wall_cap")
    result = subprocess.run([str(binary), *arguments], input=data, text=True,
                            capture_output=True, timeout=min(60, remaining), preexec_fn=child_limits)
    require(result.returncode == 0 and "UNDECIDED" not in result.stdout + result.stderr,
            f"production control incomplete: {arguments}\n{result.stderr[-2000:]}")
    return result.stdout


def production_tiles(binary, records, totals, deadline):
    text = checked_run(binary, ["--tiles"], deadline)
    actual = [tuple(map(int, line.split())) for line in text.splitlines()]
    require(all(len(row) == 9 for row in actual) and len(actual) == len(set(actual)),
            "invalid or duplicate production tile record")
    require(set(actual) == records, "production tile table differs from direct integer oracle")
    totals["production_tiles_compared"] += len(actual)


def production_image(binary, frontier, blocks, first, deadline):
    data = str(len(frontier)) + "\n" + "\n".join(" ".join(map(str, word)) for word in sorted(frontier)) + "\n"
    text = checked_run(binary, ["--image", str(blocks), str(int(first))], deadline, data)
    records = json.loads(text)
    actual = {tuple(word) for word in records}
    require(len(actual) == len(records) and all(len(word) == blocks for word in actual),
            "production finite image malformed")
    return actual


def finite_controls(binary, totals, deadline, full=False):
    for blocks in (1, 2, 3):
        frontier = {(INITIAL,) * blocks}
        steps = 53 if blocks == 3 and full else 8
        for depth in range(steps):
            if time.monotonic() > deadline:
                raise Limit("finite_frontier_wall_cap")
            provider = lambda s, x, first=(depth == 0): relation(s, x, first)
            following = explicit_image(frontier, provider)
            if blocks == 3:
                require(len(following) == KNOWN_G3_COUNTS[depth + 1], "credited G3 frontier count changed")
                require(any(all(terminal(s) for s in word) for word in following) == (depth + 1 == 53),
                        "credited G3 first neutral acceptance changed")
            if binary:
                actual = production_image(binary, frontier, blocks, depth == 0, deadline)
                require(actual == following, f"full finite frontier mismatch G={blocks},depth={depth + 1}")
                totals["production_frontier_equalities"] += 1
            totals["finite_frontiers"] += 1
            totals["finite_frontier_records"] += len(following)
            frontier = following
        if blocks == 3 and full:
            require(any(all(terminal(s) for s in word) for word in frontier), "G3 positive frontier lost")
            totals["positive_full_frontiers"] += 1


def production_positive(binary, totals, deadline):
    text = checked_run(binary, ["--fixed-blocks", "3", "--stop-at-known", "--witness",
                                "--layers", "60"], deadline)
    field_map = lambda line: dict(re.findall(r"(\w+)=([^ ]+)", line))
    done = [field_map(line) for line in text.splitlines() if line.startswith("BREG_DONE ")]
    hit = [field_map(line) for line in text.splitlines() if line.startswith("BREG_HIT ")]
    witness = [line for line in text.splitlines() if line.startswith("BREG_WITNESS ")]
    require(len(done) == len(hit) == len(witness) == 1, "missing unique production positive result")
    require(done[0]["status"] == "known_driver_control" and done[0]["scope"] == "fixed_G_control"
            and done[0]["width"] == "53" and done[0]["blocks"] == "3" and done[0]["verified"] == "1",
            "production positive scope changed")
    indexed = [(int(index), tuple(map(int, data.split(","))))
               for index, data in re.findall(r" B(\d+)=\[([^\]]+)\]", witness[0])]
    require([i for i, _ in indexed] == list(range(12)), "missing or duplicated B witness phase")
    words = [word for _, word in indexed]
    carry, total_trim = [], 0
    for t, word in enumerate(words):
        following, e, g, trim = exterior_step(word)
        require(following == words[(t + 1) % 12] and g == int(t % 4 == 0),
                "production B witness failed independent whole-integer replay")
        carry.append(e); total_trim += trim
    require(total_trim == 3 and "".join(map(str, carry)) == hit[0]["e"],
            "production carry stream or trim count differs")
    symbols = tuple(map(int, hit[0]["symbols"].split(",")))
    require(symbols in {KNOWN_TRIPLE[i:] + KNOWN_TRIPLE[:i] for i in range(3)},
            "production known-language branch is not one fixed rotation")
    totals["production_exterior_edges_replayed"] += 12
    totals["production_known_positive_controls"] += 1


def production_guards(binary, totals, deadline):
    cases = [(["--states", "1"], "regular_state_cap"),
             (["--edges", "1"], "regular_edge_cap"),
             (["--ops", "1"], "regular_operation_cap"),
             (["--layers", "1"], "exterior_regular_layer_limit")]
    for arguments, reason in cases:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise Limit("test_wall_cap")
        run = subprocess.run([str(binary), *arguments], capture_output=True, text=True,
                             timeout=min(60, remaining), preexec_fn=child_limits)
        require(run.returncode == 2 and "UNDECIDED " + reason in run.stdout + run.stderr,
                f"resource guard failed: {arguments}")
        require("BREG_DONE" not in run.stdout, "resource cap became a completed classification")
        totals["production_resource_guards"] += 1


def production_backward(binary, records, cuts, totals, deadline):
    reverse, wrong_ports = defaultdict(set), defaultdict(set)
    for old, new, left, right, *_ in records:
        reverse[(new, left)].add((old, right))
        wrong_ports[(new, right)].add((old, left))
    inverse = lambda symbol, coefficient: reverse.get((symbol, coefficient), ())
    swapped = lambda symbol, coefficient: wrong_ports.get((symbol, coefficient), ())
    neutral = tuple(s for s in range(2560) if terminal(s))
    cases = [{(s,) for s in neutral}, {(65,), (337,), (INITIAL,)},
             {(65, 337), (337, 65)}]
    cases.extend({cuts[k]} for k in (1, 3, 27, 53))
    distinguishes_ports = False
    for target in cases:
        blocks = len(next(iter(target)))
        expected = explicit_image(target, inverse)
        distinguishes_ports |= expected != explicit_image(target, swapped)
        data = str(len(target)) + "\n" + "\n".join(" ".join(map(str, word)) for word in sorted(target)) + "\n"
        text = checked_run(binary, ["--reverse-image", str(blocks)], deadline, data)
        listed = json.loads(text)
        actual = {tuple(word) for word in listed}
        require(len(actual) == len(listed) and actual == expected,
                "production reverse image differs from symbol-only transposition")
        totals["production_reverse_equalities"] += 1
        totals["reverse_frontier_records"] += len(expected)
    require(distinguishes_ports, "reverse controls fail to detect incorrectly swapped coefficient ports")
    totals["reverse_port_direction_counterexamples"] += 1

    rotations = {KNOWN_TRIPLE[i:] + KNOWN_TRIPLE[:i] for i in range(3)}
    for blocks in (1, 2, 3):
        expected = set(itertools.product(neutral, repeat=blocks)) - rotations
        # Only G1 receives three further complete preimages in this bounded
        # control.  G2/G3 seed exports check the full subtraction of K.
        for depth in range(4 if blocks == 1 else 1):
            text = checked_run(binary, ["--backward", "--fixed-blocks", str(blocks),
                                        "--export-layer", str(depth), "--slice", str(blocks),
                                        "--layers", "4"], deadline)
            actual = {tuple(word) for word in json.loads(text.strip().splitlines()[-1])}
            require(actual == expected, f"backward seed/preimage mismatch G={blocks},depth={depth}")
            totals["production_bad_seed_preimage_equalities"] += 1
            totals["bad_seed_preimage_records"] += len(expected)
            if blocks == 1 and depth < 3:
                following = explicit_image(expected, inverse)
                require(expected <= following, "neutral self-loop preimage monotonicity failed")
                expected = following


def backward_witness_control(binary, cuts, totals, deadline):
    """Exercise reverse reconstruction on a credited known fixture, not Bad.

    The temporary harness deliberately supplies an empty allowed language so
    that the existing method can replay its known positive path.  Its printed
    internal hit label is NOT a new-driver result.  No production source changes.
    """
    original = Path(__file__).with_name("exterior_regular.cpp").read_text()
    anchor = "int main(int argc,char**argv){"
    require(original.count(anchor) == 1, "exterior test-main anchor changed")
    source = original.replace(anchor, "int exterior_cli118(int argc,char**argv){", 1)
    literal = "{" + ",".join("{" + ",".join(map(str, row)) + "}" for row in cuts) + "}"
    source += r'''

int main(){
  try{
    Tiles108::build_tiles(); BREG118::auditTiles();
    for(int s=0;s<2560;++s)for(int left=0;left<19;++left)
      for(const auto&t:Tiles108::tiles[s][left])
        BREG118::reverseTiles[t.out][left].push_back({s,t.right,t.coefficients,t.positive});
    BREG118::Engine engine;
    vector<vector<REG118::Label>> cuts=REPLACE_CUTS118;
    vector<REG118::DFA> history;
    for(int k=53;k>=1;--k){
      REG118::DFA one;one.q.resize(4);one.q[3].accept=true;
      for(int j=0;j<3;++j)one.q[j].arcs.push_back({cuts[k][j],REG118::Id(j+1)});
      history.push_back(std::move(one));
    }
    auto physical=BREG118::words({272},3,engine.budget);
    auto emptyAllowed=REG118::emptyDfa(engine.budget);
    engine.backwardWitness(history,physical,emptyAllowed,cuts[1],52);
    printf("BREG_BACKWARD_TEST known_fixture=1 width=53 columns=53\n");
    return 0;
  }catch(const exception&e){fprintf(stderr,"UNDECIDED %s\n",e.what());return 2;}
}
'''.replace("REPLACE_CUTS118", literal)
    with tempfile.TemporaryDirectory(prefix="p196-agent118-backward-test-", dir="/tmp") as temp:
        folder = Path(temp)
        cpp, executable = folder / "control.cpp", folder / "control"
        cpp.write_text(source)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise Limit("backward_witness_compile_wall_cap")
        build = subprocess.run(["c++", "-std=c++17", "-O2", "-I", str(binary.parent),
                                str(cpp), "-o", str(executable)], capture_output=True, text=True,
                               timeout=min(60, remaining), preexec_fn=child_limits)
        require(build.returncode == 0, "backward witness harness build failed: " + build.stderr[-2000:])
        text = checked_run(executable, [], deadline)
    require("BREG_BACKWARD_TEST known_fixture=1 width=53 columns=53" in text
            and "BREG_DONE" not in text, "backward fixture was incorrectly classified as research")
    witness = [line for line in text.splitlines() if line.startswith("BREG_WITNESS ")]
    require(len(witness) == 1, "backward fixture has no unique replay witness")
    indexed = [(int(i), tuple(map(int, data.split(","))))
               for i, data in re.findall(r" B(\d+)=\[([^\]]+)\]", witness[0])]
    require([i for i, _ in indexed] == list(range(12)), "backward witness phase coverage differs")
    words = [word for _, word in indexed]
    require(words[0] == KNOWN_B0, "backward fixture changed its known initial exterior")
    carry = []
    for t, word in enumerate(words):
        following, e, g, _ = exterior_step(word)
        require(following == words[(t + 1) % 12] and g == int(t % 4 == 0),
                "backward reconstructed column order failed whole-integer replay")
        carry.append(e)
    require("".join(map(str, carry)) == KNOWN_E, "backward known fixture carry stream differs")
    totals["production_backward_witness_edges_replayed"] += 12


def residue_returns(word):
    """Brute all nine initial residues; no affine-state implementation reused."""
    returning = []
    for initial in range(9):
        current = initial
        for symbol in word:
            low = decode(symbol)[0]
            # Four one-step digit-sum transitions, in temporal bit order.
            for phase in range(4):
                current = (2 * current + 1 - 2 * ((low >> phase) & 1)) % 9
        if current == initial:
            returning.append(initial)
    return tuple(returning)


def production_residue_seed(binary, totals, deadline):
    neutral = tuple(s for s in range(2560) if terminal(s))
    rotations = {KNOWN_TRIPLE[i:] + KNOWN_TRIPLE[:i] for i in range(3)}
    raw_expected = (6, 86, 456)
    for blocks in (1, 2, 3):
        raw = {word for word in itertools.product(neutral, repeat=blocks) if residue_returns(word)}
        require(len(raw) == raw_expected[blocks - 1], "credited residue-return count changed")
        expected = raw - rotations
        text = checked_run(binary, ["--backward", "--residue-seed", "--fixed-blocks", str(blocks),
                                    "--export-layer", "0", "--slice", str(blocks),
                                    "--layers", "1"], deadline)
        actual = {tuple(word) for word in json.loads(text.strip().splitlines()[-1])}
        require(actual == expected, f"residue seed differs from nine-start simulation at G={blocks}")
        totals["production_residue_seed_equalities"] += 1
        totals["residue_seed_records"] += len(expected)
    zero = encode(0, 15, 0)
    one = encode(1, 14, 9)
    require(residue_returns((zero,) * 3) == tuple(range(9)), "identity affine return was rejected")
    require(not residue_returns((zero, zero, one)), "nonzero translation wrongly has a fixed residue")
    require(all(residue_returns(word) == tuple(range(9)) for word in rotations),
            "known positive cycles lost their identity residue return")
    require((zero,) * 3 in actual and () not in actual, "Bad seed lost positive identity or admitted epsilon")
    totals["residue_identity_controls"] += 5


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path)
    parser.add_argument("--full-p12", action="store_true", help="compare all53 known G3 positive layers")
    parser.add_argument("--backward", action="store_true", help="also check transposed tiles and Bad-language seeds")
    parser.add_argument("--residue-seed", action="store_true", help="check the optional prior digit-sum seed filter")
    parser.add_argument("--seconds", type=float, default=60)
    args = parser.parse_args()
    if not 0 < args.seconds <= 60:
        parser.error("each run must have a wall budget in(0,60]")
    child_limits()
    deadline = time.monotonic() + args.seconds
    totals = Counter()
    try:
        records = arithmetic_controls(totals, deadline)
        language_controls(totals)
        cuts = positive_control(totals)
        binary = args.binary.resolve() if args.binary else None
        if binary:
            production_tiles(binary, records, totals, deadline)
        finite_controls(binary, totals, deadline, args.full_p12)
        if binary:
            for depth in (0, 1, 2, 26, 51, 52):
                expected = explicit_image({cuts[depth]}, lambda s, x: relation(s, x, depth == 0))
                actual = production_image(binary, {cuts[depth]}, 3, depth == 0, deadline)
                require(expected == actual and cuts[depth + 1] in actual,
                        "production rejected or altered known positive path")
                totals["production_positive_path_equalities"] += 1
            production_positive(binary, totals, deadline)
            production_guards(binary, totals, deadline)
            if args.backward:
                production_backward(binary, records, cuts, totals, deadline)
                backward_witness_control(binary, cuts, totals, deadline)
            if args.residue_seed:
                production_residue_seed(binary, totals, deadline)
    except (RuntimeError, OSError, ValueError, MemoryError, subprocess.TimeoutExpired) as error:
        print("UNDECIDED", str(error))
        return 2
    print("exterior_regular_checks", dict(sorted(totals.items())))
    print("COMPUTED CHECKS PASSED; finite controls and known B-only positive, no all-G claim")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
