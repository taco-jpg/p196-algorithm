#!/usr/bin/env python3
"""Strict adapters for the proposed Agent106/116 exterior DFA exports.

Exported DFAs are untrusted candidate languages, never presumed invariants.
The external verifier must still prove every arithmetic obligation. Block
symbols expand to a prefix-code trie; no minimization or determinization is
used. A separate local-path audit checks the complete expansion relation.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from exterior_first_language import Candidate, render, symbol, validate


def natural(value, name, bound=None):
    if type(value) is not int or value < 0 or (bound is not None and value >= bound):
        raise ValueError(f"invalid {name}")
    return value


def model(document, base=None, e=None, g=None):
    supplied = {"base": base, "e": e, "g": g}
    for name in supplied:
        if name in document:
            if supplied[name] is not None and supplied[name] != document[name]:
                raise ValueError(f"export and explicit {name} disagree")
            supplied[name] = document[name]
        if supplied[name] is None:
            raise ValueError(f"missing {name}; supply the exact external driver")
    validate(supplied["base"], supplied["e"], supplied["g"])
    return supplied["base"], supplied["e"], supplied["g"]


def rows(raw, states):
    if not isinstance(raw, list):
        raise ValueError("transition row must be a list")
    result = {}
    for edge in raw:
        if not isinstance(edge, list) or len(edge) != 2:
            raise ValueError("edge must be [integer_symbol,target]")
        label, target = natural(edge[0], "symbol", 2**64), natural(edge[1], "target", states)
        if label in result:
            raise ValueError("duplicate deterministic label")
        result[label] = target
    return result


def single_phase(document, base=None, e=None, g=None):
    base, e, g = model(document, base, e, g)
    raw = document.get("dfa", document)
    transitions = raw.get("transitions")
    if not isinstance(transitions, list) or not transitions:
        raise ValueError("single-phase export needs nonempty transitions rows")
    count = len(transitions)
    start = natural(raw.get("start"), "start", count)
    finals = raw.get("finals")
    if not isinstance(finals, list):
        raise ValueError("finals must be a list of accepting state indices")
    accepting = [False] * count
    for state in finals:
        state = natural(state, "final", count)
        if accepting[state]:
            raise ValueError("duplicate accepting state")
        accepting[state] = True
    edges = [rows(row, count) for row in transitions]
    for row in edges:
        for label in row:
            phase, rest = divmod(label, 4 * base)
            if phase >= len(g) or (g[phase] == "0" and rest % base):
                raise ValueError("symbol outside typed phase alphabet")
    return Candidate(base, e, g, start, accepting, edges)


def decode_block(base: int, g: str, label: int) -> tuple[int, ...]:
    natural(label, "block symbol", 2**64)
    start, packed = divmod(label, 2**32)
    if start >= len(g) or g[start] != "1":
        raise ValueError("block starts outside an overflow phase")
    length = 1
    while length < len(g) and g[(start + length) % len(g)] != "1":
        length += 1
    if 2 * length + (base - 1).bit_length() > 32:
        raise ValueError("block exceeds the declared 32-bit local encoding")
    digit = packed >> (2 * length)
    if digit >= base:
        raise ValueError("block digit outside base")
    return tuple(symbol(base, (start + j) % len(g),
                        (packed >> j) & 1, (packed >> (length + j)) & 1,
                        digit if j == 0 else 0) for j in range(length))


def audit_expansion(base, g, original_edges, original_accepting, expanded):
    """Check every complete source-codeword path, including cycles between them.

    Intermediate trie nodes must not accept. Enumerate their acyclic paths
    until an original node is reached and compare the full relation exactly.
    This local codeword correspondence proves the language map at all lengths.
    """
    original_count = len(original_edges)
    if expanded.accepting[:original_count] != original_accepting:
        raise ValueError("expansion changed original acceptance")
    if any(expanded.accepting[original_count:]):
        raise ValueError("partial block node accepts")
    paths = 0
    for source, row in enumerate(original_edges):
        expected = {(decode_block(base, g, label), target) for label, target in row.items()}
        actual = set()
        todo = [(target, (label,), frozenset()) for label, target in expanded.edges[source].items()]
        while todo:
            current, word, seen = todo.pop()
            if current < original_count:
                actual.add((word, current))
                continue
            if current in seen or len(word) >= len(g):
                raise ValueError("invalid partial-block cycle/depth")
            for label, target in expanded.edges[current].items():
                todo.append((target, word + (label,), seen | {current}))
        if actual != expected:
            raise ValueError("block expansion does not preserve the exact local path relation")
        paths += len(actual)
    return paths


def blocks(document, base=None, e=None, g=None):
    base, e, g = model(document, base, e, g)
    if g[0] != "1":
        raise ValueError("block import needs phase0 overflow; rotate driver and labels together")
    raw = document.get("dfa", document)
    states = raw.get("states")
    if not isinstance(states, list) or not states:
        raise ValueError("block export requires nonempty states list")
    count = len(states)
    start = natural(raw.get("start"), "start", count)
    accepting, original = [], []
    for state in states:
        if not isinstance(state, dict) or type(state.get("final")) is not bool:
            raise ValueError("block state final must be a Boolean")
        accepting.append(state["final"])
        original.append(rows(state.get("edges"), count))
    result = Candidate(base, e, g, start, accepting.copy(), [{} for _ in states])
    for source, row in enumerate(original):
        for label, target in sorted(row.items()):
            word, current = decode_block(base, g, label), source
            for position, letter in enumerate(word):
                if position + 1 == len(word):
                    previous = result.edges[current].get(letter)
                    if previous is not None and previous != target:
                        raise ValueError("noninjective or non-prefix-free block encoding")
                    result.edges[current][letter] = target
                elif letter in result.edges[current]:
                    current = result.edges[current][letter]
                    if current < count:
                        raise ValueError("one block codeword is a proper prefix of another")
                else:
                    following = len(result.edges)
                    result.edges.append({})
                    result.accepting.append(False)
                    result.edges[current][letter] = following
                    current = following
    checked = audit_expansion(base, g, original, accepting, result)
    return result, {"original_states": count, "codeword_paths_checked": checked,
                    "expanded_states": len(result.edges),
                    "expanded_edges": sum(map(len, result.edges))}


def selftest():
    from exterior_first_language import TARGET_E, TARGET_G, first_candidate
    candidate, _ = first_candidate(10, TARGET_E, TARGET_G)
    raw = {"base": 10, "e": TARGET_E, "g": TARGET_G, "start": candidate.start,
           "finals": [i for i, value in enumerate(candidate.accepting) if value],
           "transitions": [[[label, target] for label, target in row.items()]
                           for row in candidate.edges]}
    if render(single_phase(raw)) != render(candidate):
        raise RuntimeError("single-phase schema changed complete language graph")
    codec = 0
    starts = [i for i, bit in enumerate(TARGET_G) if bit == "1"]
    for start in starts:
        length = next(i for i in range(1, len(TARGET_G) + 1)
                      if TARGET_G[(start + i) % len(TARGET_G)] == "1")
        for packed in range(10 << (2 * length)):
            word = decode_block(10, TARGET_G, (start << 32) | packed)
            rebuilt, digit = 0, None
            for j, label in enumerate(word):
                phase, rest = divmod(label, 40)
                low, rest = divmod(rest, 20)
                high, previous = divmod(rest, 10)
                if phase != (start + j) % len(TARGET_G) or (j and previous):
                    raise RuntimeError("block phase/digit mapping mismatch")
                rebuilt |= low << j
                rebuilt |= high << (length + j)
                if j == 0:
                    digit = previous
            rebuilt |= digit << (2 * length)
            if rebuilt != packed:
                raise RuntimeError("block encoding is not injective")
            codec += 1
    # Correlated cyclic source graph, sharing partial block prefixes. Every
    # edge path is audited, so cycles may traverse arbitrarily many codewords.
    labels = [(start << 32) | local for start in starts for local in (0, 1, 2, 3)]
    raw_blocks = {"base": 10, "e": TARGET_E, "g": TARGET_G,
                  "dfa": {"start": 0, "states": [
                      {"final": bool(q % 2), "edges": [[label, (q + i + 1) % 7]
                                                          for i, label in enumerate(labels)]}
                      for q in range(7)]}}
    expanded, metadata = blocks(raw_blocks)
    original = [{label: target for label, target in node["edges"]}
                for node in raw_blocks["dfa"]["states"]]
    finals = [node["final"] for node in raw_blocks["dfa"]["states"]]
    corruptions = 0
    broken = Candidate(expanded.base, expanded.e, expanded.g, expanded.start,
                       expanded.accepting.copy(), [row.copy() for row in expanded.edges])
    broken.accepting[7] = True
    try:
        audit_expansion(10, TARGET_G, original, finals, broken)
    except ValueError:
        corruptions += 1
    else:
        raise RuntimeError("accepted a partial-block corruption")
    broken = Candidate(expanded.base, expanded.e, expanded.g, expanded.start,
                       expanded.accepting.copy(), [row.copy() for row in expanded.edges])
    first_label = next(iter(broken.edges[0]))
    broken.edges[0][first_label] = 0
    try:
        audit_expansion(10, TARGET_G, original, finals, broken)
    except ValueError:
        corruptions += 1
    else:
        raise RuntimeError("accepted a truncated-codeword corruption")
    return {"single_phase_roundtrips": 1, "exhaustive_block_codec_cases": codec,
            "expansion": metadata, "rejected_expansion_corruptions": corruptions}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path)
    parser.add_argument("--schema", choices=("single-phase", "overflow-block"))
    parser.add_argument("--base", type=int)
    parser.add_argument("--e")
    parser.add_argument("--g")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        print("EXTERIOR_IMPORT_CONTROLS " + json.dumps(selftest(), sort_keys=True))
    if args.input:
        if not args.schema or not args.output:
            parser.error("an import requires --schema and --output")
        document = json.loads(args.input.read_text())
        if args.schema == "single-phase":
            candidate = single_phase(document, args.base, args.e, args.g)
            metadata = {}
        else:
            candidate, metadata = blocks(document, args.base, args.e, args.g)
        args.output.write_text(render(candidate))
        print(json.dumps({"output": str(args.output), "status": "UNTRUSTED_CANDIDATE",
                          "states": len(candidate.edges), **metadata}, sort_keys=True))
    if not args.selftest and not args.input:
        parser.error("provide an input or --selftest")


if __name__ == "__main__":
    main()
