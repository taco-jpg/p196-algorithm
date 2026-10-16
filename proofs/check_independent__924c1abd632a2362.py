#!/usr/bin/env python3
"""Independent numerical diagnostics for the literal Lean certificate.

This is not a proof-producing program and is not part of the Lean import graph.
It does not import the author's generator, verifier, fast candidate formulas,
rank JSON, or any previous review program.  All outputs are diagnostic only.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import re
import resource
import time

HERE = Path(__file__).resolve().parent
CONTRIBUTION = HERE.parent
CERT = CONTRIBUTION / "certificate"
resource.setrlimit(resource.RLIMIT_CPU, (90, 95))
resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
START = time.monotonic()
PINS = {}


def read(path):
    b = path.read_bytes()
    PINS[str(path.relative_to(CONTRIBUTION))] = hashlib.sha256(b).hexdigest()
    return b.decode()


# Read an intentionally tiny language: constructors and earlier named trees.
# Each node's full literal word is retained, independently of its search key.
definitions = {}
literal_nodes = []


def parse_expression(source):
    tokens = re.findall(r"\.node|\.empty|[A-Za-z_][A-Za-z_0-9]*|\d+|[(),\[\]]", source)
    assert "".join(tokens) == re.sub(r"\s", "", source), "unrecognized syntax"
    i = 0

    def take(expected=None):
        nonlocal i
        token = tokens[i]
        i += 1
        if expected is not None:
            assert token == expected, (token, expected)
        return token

    def expr():
        token = take()
        if token == "(":
            value = expr()
            take(")")
            return value
        if token == ".empty":
            return None
        if token != ".node":
            return definitions[token]
        key = int(take())
        take("[")
        word = []
        while tokens[i] != "]":
            word.append(int(take()))
            if tokens[i] != "]":
                take(",")
        take("]")
        rank = int(take())
        node = (key, tuple(word), rank, expr(), expr())
        literal_nodes.append(node)
        return node

    result = expr()
    assert i == len(tokens)
    return result


for path in sorted(CERT.glob("Rank739Data??.lean")):
    for line in read(path).splitlines():
        if line.startswith("def "):
            match = re.fullmatch(r"def (\w+) : RankTree := (.+)", line)
            assert match, line
            name, expression = match.groups()
            assert name not in definitions
            definitions[name] = parse_expression(expression)
root_source = read(CERT / "Rank739.lean")
root_match = re.search(r"^def ranks : RankTree := (\w+)$", root_source, re.M)
assert root_match
root = definitions[root_match[1]]


def code(word):
    key = 1
    for entry in word:
        key = 19 * key + entry
    return key


def lookup(word):
    key = code(word)
    node = root
    while node is not None:
        pivot, stored, rank, left, right = node
        if key < pivot:
            node = left
        elif pivot < key:
            node = right
        else:
            return rank if word == stored else None
    return None


reachable = []
seen_ids = set()
todo = [root]
while todo:
    node = todo.pop()
    if node is None:
        continue
    assert id(node) not in seen_ids, "shared/repeated tree node"
    seen_ids.add(id(node))
    reachable.append(node)
    todo += [node[3], node[4]]
assert len(reachable) == len(literal_nodes)
words = {node[1]: node[2] for node in reachable}
assert len(words) == len(reachable)
assert all(lookup(word) == rank for _, word, rank, _, _ in reachable)


# Local decimal equations are exhaustively enumerated over all 19 source
# sums and both possible inner carries.  No algebraic fast-inverse candidate
# formula is used.  Ordinary division/remainder determine every local digit.
no_transitions = {}
over_transitions = {}
for low_in, high_out in itertools.product(range(2), repeat=2):
    for source_sum, high_in in itertools.product(range(19), range(2)):
        if (source_sum + high_in) // 10 == high_out:
            emitted = (source_sum + low_in) % 10 + (source_sum + high_in) % 10
            no_transitions.setdefault((low_in, high_out, emitted), []).append(
                (source_sum, (source_sum + low_in) // 10, high_in))
    for previous in range(19):
        for source_sum, high_in in itertools.product(range(19), range(2)):
            if (previous + high_in) // 10 == high_out:
                emitted = (source_sum + low_in) % 10 + (previous + high_in) % 10
                over_transitions.setdefault((previous, low_in, high_out, emitted), []).append(
                    (source_sum, (source_sum + low_in) // 10, high_in))


def predecessors(target):
    if len(target) != 7:
        return set()  # Exactly the definition of longPred 7.
    current = [((), 0, 0)]
    for digit in target:
        current = [(prefix + (a,), low_next, high_in)
                   for prefix, low_in, high_out in current
                   for a, low_next, high_in in no_transitions.get((low_in, high_out, digit), ())]
    result = {prefix for prefix, _, _ in current if prefix[0] > 0}
    # Enumerate every possible outside source sum instead of overflowFirst.
    current = [((a,), a // 10, 1) for a in range(1, 19)
               if target[0] == 1 + a % 10]
    for digit in target[1:]:
        current = [(prefix + (a,), low_next, high_in)
                   for prefix, low_in, high_out in current
                   for a, low_next, high_in in over_transitions.get(
                       (prefix[-1], low_in, high_out, digit), ())]
    for prefix, _, high_out in current:
        if any((prefix[-1] + inner) // 10 == high_out for inner in range(2)):
            result.add(prefix)
    return result


edge_count = 0
rows_without_predecessors = 0
max_predecessors = 0
for target, rank in words.items():
    previous_words = predecessors(target)
    edge_count += len(previous_words)
    rows_without_predecessors += not previous_words
    max_predecessors = max(max_predecessors, len(previous_words))
    for previous in previous_words:
        previous_rank = lookup(previous)
        assert previous_rank is not None and previous_rank < rank, (
            "bad complete predecessor row", target, rank, previous, previous_rank)


initial_ranks = []
for free in itertools.product(range(10), repeat=4):
    word = (7, 3, 9) + free
    rank = lookup(word)
    assert rank is not None and rank <= 38, ("initial", word, rank)
    initial_ranks.append(rank)
short_target = (7, 3, 9, 9, 3, 7)
assert lookup(short_target) is not None and lookup(short_target) <= 38


def digits(n):
    assert n > 0
    return tuple(map(int, str(n)[::-1]))


def pair_word(n):
    ds = digits(n)
    return tuple(x + y for x, y in zip(ds, ds[::-1]))


def realize(word):
    # Independently realize a legal symmetric pair word as a positive number.
    # A positive outer sum gives a positive leading decimal digit.
    n = len(word)
    ds = [0] * n
    for i in range(n // 2):
        high = min(9, word[i])
        ds[i], ds[n - 1 - i] = word[i] - high, high
    if n % 2:
        assert word[n // 2] % 2 == 0
        ds[n // 2] = word[n // 2] // 2
    assert ds[-1] > 0 and all(0 <= d <= 9 for d in ds)
    value = sum(d * 10**i for i, d in enumerate(ds))
    assert pair_word(value) == word
    return value


short_count = 0
six_to_seven = 0
by_width = {}
for width in range(1, 7):
    count = 0
    # Build symmetric words from arbitrary half sums and the even center.
    half_width = width // 2
    outer_choices = range(1, 19) if half_width else (None,)
    for outer in outer_choices:
        for interior in itertools.product(range(19), repeat=max(0, half_width - 1)):
            half = (outer,) + interior if half_width else ()
            centers = range(2, 19, 2) if width == 1 else range(0, 19, 2)
            for center in centers if width % 2 else (None,):
                word = half + ((center,) if width % 2 else ()) + half[::-1]
                value = realize(word)
                next_value = value + int(str(value)[::-1])
                next_word = pair_word(next_value)
                assert len(next_word) in (width, width + 1)
                assert lookup(next_word) is None, ("short boundary", word, next_word)
                six_to_seven += width == 6 and len(next_word) == 7
                count += 1
    by_width[str(width)] = count
    short_count += count
assert short_count == 10467


# Source-level completeness diagnostics for the finite proof assembly.
# The Lean type of allRowsFast provides the actual kernel guarantee.
all_rows_source = read(CERT / "AllRows739.lean")
assert set(re.findall(r"^import Rows739_(\d{3})$", all_rows_source, re.M)) == {
    f"{i:03d}" for i in range(256)}
assert len(re.findall(r"\bchecked_leaf\d{4}\b", all_rows_source)) == 1024
assert len(re.findall(r"\brow_branch\d{4}\b", all_rows_source)) == 1023
assert set(re.findall(r"\bchecked_leaf(\d{4})\b", all_rows_source)) == {
    f"{i:04d}" for i in range(1024)}
assert set(re.findall(r"\brow_branch(\d{4})\b", all_rows_source)) == {
    f"{i:04d}" for i in range(1023)}
initial_source = read(CERT / "Initial739.lean")
range_references = re.findall(r"checked_range .*? (\d+) 100 initial_(\d{3})\)", initial_source)
assert len(range_references) == 100
assert {(int(a), int(b)) for a, b in range_references} == {(100*i, i) for i in range(100)}


# Pin every local source in Conclusion739's import closure, including split
# batches; a subsequent compilation can compare the same snapshot precisely.
module_paths = {p.stem: p for p in CONTRIBUTION.glob("*.lean")}
module_paths.update({p.stem: p for p in CERT.glob("*.lean")})
base_path = CONTRIBUTION.parents[2] / "research" / "continuation" / "LychrelDigitSums.lean"
module_paths["LychrelDigitSums"] = base_path
closure = []
module_seen = set()


def import_closure(module):
    if module in module_seen or module not in module_paths:
        return
    module_seen.add(module)
    path = module_paths[module]
    if module == "LychrelDigitSums":
        source = path.read_text()
        PINS["../../../research/continuation/LychrelDigitSums.lean"] = hashlib.sha256(path.read_bytes()).hexdigest()
    else:
        source = read(path)
    for imported in re.findall(r"^import (\S+)\s*$", source, re.M):
        import_closure(imported)
    closure.append(module)


import_closure("Conclusion739")
for relative, digest in PINS.items():
    assert hashlib.sha256((CONTRIBUTION / relative).read_bytes()).hexdigest() == digest

summary = {
    "status": "PASS (independent numerical diagnostics; not a Lean proof)",
    "runtime_seconds": round(time.monotonic() - START, 6),
    "root": root_match[1],
    "tree_nodes": len(reachable),
    "tree_named_subtrees": len(definitions),
    "word_lengths": {str(n): sum(len(w) == n for w in words) for n in sorted(set(map(len, words)))},
    "lookup_every_stored_word": True,
    "complete_predecessor_edges": edge_count,
    "rows_without_predecessors": rows_without_predecessors,
    "max_predecessors_per_row": max_predecessors,
    "all_predecessors_lookup_with_strictly_smaller_rank": True,
    "long_initial_words": len(initial_ranks),
    "max_initial_rank": max(initial_ranks),
    "short_initial_rank": lookup(short_target),
    "short_words_checked_via_ordinary_integer_realization": short_count,
    "short_words_by_width": by_width,
    "six_to_seven_crossings": six_to_seven,
    "all_short_successors_absent": True,
    "all_rows_assembly_leaf_and_branch_coverage": True,
    "initial_assembly_range_coverage": True,
    "conclusion_import_closure_modules": closure,
    "source_sha256": PINS,
}
(HERE / "diagnostics.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({k: v for k, v in summary.items() if k not in ("source_sha256", "conclusion_import_closure_modules")}, indent=2))
