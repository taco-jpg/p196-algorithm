#!/usr/bin/env python3
"""Explicit closure, FIRST, malformed-input and resource controls.

This imports the independently authored whole-column reference, never the MDD
search.  All 256 subsets of the eight-state base-2/P1/g=1 universe are checked
for both terminal carry bits.  Search metadata is deliberately untrusted.
The much larger scientific closure certificate is not opened by this script.
"""
import copy
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
from unittest.mock import patch


HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CERT = load("independent_closure_checker", HERE / "p24_reverse_certificate.py")
REF = load("independent_explicit_columns", HERE / "p24_reverse_reference.py")


def blocks(g):
    starts = [t for t, digit in enumerate(g) if digit == "1"]
    return [{"start": s, "length": (starts[(i + 1) % len(starts)] - s - 1) % len(g) + 1}
            for i, s in enumerate(starts)]


def encode(oracle, state):
    low, high, lag = state
    values = []
    for block in blocks(oracle.g):
        s, n = block["start"], block["length"]
        l = sum((low >> ((s + j) % oracle.p) & 1) << j for j in range(n))
        h = sum((high >> ((s + j) % oracle.p) & 1) << j for j in range(n))
        values.append(l | h << n | lag[oracle.yindex[s]] << (2 * n))
    return tuple(values)


def certificate(oracle, states):
    """An ordinary unminimized trie; no primary canonicalizer or metadata."""
    geometry = blocks(oracle.g)
    nodes = [{"level": 0, "arcs": []}, {"level": len(geometry), "arcs": []}]
    words = sorted({encode(oracle, state) for state in states})

    def build(rows, level):
        if not rows:
            return 0
        if level == len(geometry):
            return 1
        groups = {}
        for row in rows:
            groups.setdefault(row[level], []).append(row)
        arcs = [[label, build(group, level + 1)] for label, group in sorted(groups.items())]
        nodes.append({"level": level, "arcs": arcs})
        return len(nodes) - 1

    root = build(words, 0)
    return {"base": oracle.base, "e": oracle.e, "g": oracle.g,
            "blocks": geometry, "nodes": nodes, "root": root}


def main():
    started = time.monotonic()
    failures = []
    counts = {}

    def expect(name, actual, expected):
        if actual != expected:
            failures.append({"control": name, "actual": actual, "expected": expected})

    # Complete subset census, including empty and universal sets.  Forward
    # guessed-H enumeration supplies the graph independently of local tiles.
    oracle = REF.Oracle(2, "0", "1")
    universe = [(l, h, (y,)) for l in (0, 1) for h in (0, 1) for y in (0, 1)]
    adjacency = {state: REF.brute_forward(oracle, state, False) for state in universe}
    first = REF.brute_forward(oracle, oracle.start, True)
    subset_queries = witnesses = 0
    statuses = {}
    for e in "01":
        oracle = REF.Oracle(2, e, "1")
        decode = {encode(oracle, state): state for state in universe}
        for mask in range(1 << len(universe)):
            chosen = {state for i, state in enumerate(universe) if mask >> i & 1}
            pre = {state for state in universe if adjacency[state] & chosen}
            checker = CERT.Checker(certificate(oracle, chosen), CERT.Budget(seconds=30))
            returned = None
            for initial in range(3):
                returned = checker.counterexample(checker.root, checker.root, initial, initial)
                if returned is not None:
                    break
            expect(f"subset-{e}-{mask}-closure", returned is not None, bool(pre - chosen))
            if returned is not None:
                target = decode[tuple(row[0] for row in returned)]
                source = decode[tuple(row[1] for row in returned)]
                expect(f"subset-{e}-{mask}-witness", target in chosen and source not in chosen
                       and target in adjacency[source], True)
                witnesses += 1
            if oracle.terminal not in chosen:
                expected = "TERMINAL_NOT_INCLUDED"
            elif first & chosen:
                expected = "BOUNDARY_OVERLAP"
            elif pre - chosen:
                expected = "NOT_PREDECESSOR_CLOSED"
            else:
                expected = "PREDECESSOR_CLOSED_NO_EXTERIOR"
            actual = checker.check()
            expect(f"subset-{e}-{mask}-status", actual["status"], expected)
            if actual["status"] == "PREDECESSOR_CLOSED_NO_EXTERIOR":
                expect(f"subset-{e}-{mask}-cardinality", actual["set_cardinality"], len(chosen))
            statuses[actual["status"]] = statuses.get(actual["status"], 0) + 1
            subset_queries += 1
    counts.update(exhaustive_subsets=subset_queries, replayed_subset_counterexamples=witnesses,
                  subset_statuses=statuses)

    # Actual known B cycles: terminal alone misses a predecessor; adding the
    # independently derived first cut creates a forbidden FIRST overlap.
    positives = 0
    for exponent in range(1, 6):
        base = 1 << exponent
        half = [(base, base - 1)] + [(1 << j, (1 << j) - 1) for j in range(exponent)]
        original = half * 2
        for rotation in (0, 1):
            words = original[rotation:] + original[:rotation]
            scratch = REF.Oracle(base, "0" * len(words), "0" * len(words))
            streams = [scratch.integer_step(word)[1:] for word in words]
            e = "".join(str(pair[0]) for pair in streams)
            g = "".join(str(pair[1]) for pair in streams)
            o = REF.Oracle(base, e, g)
            o.replay([tuple(word[j] for word in words) for j in range(2)])
            low = [word[0] // base for word in words]
            high = [(word[1] + 1 - int(e[t])) // base for t, word in enumerate(words)]
            lag = tuple((words[t][0] + high[t]) % base for t in o.positions)
            first_cut = (sum(x << t for t, x in enumerate(low)),
                         sum(x << t for t, x in enumerate(high)), lag)
            alone = CERT.check(certificate(o, {o.terminal}))
            expect(f"positive-{base}-{rotation}-missing-predecessor", alone["status"],
                   "NOT_PREDECESSOR_CLOSED")
            overlap = CERT.check(certificate(o, {o.terminal, first_cut}))
            expect(f"positive-{base}-{rotation}-boundary", overlap["status"], "BOUNDARY_OVERLAP")
            if overlap["status"] == "BOUNDARY_OVERLAP":
                expect(f"positive-{base}-{rotation}-known-cut", tuple(overlap["word"]), encode(o, first_cut))
                expect(f"positive-{base}-{rotation}-positive-column",
                       all(x > 0 for x in overlap["first_column"]), True)
            positives += 1
    counts["known_positive_rotations"] = positives

    o = REF.Oracle(2, "0", "1")
    good = certificate(o, {o.terminal})
    malformed = [("null-data", None), ("list-data", [])]

    def mutation(name, edit, original=good):
        data = copy.deepcopy(original)
        edit(data)
        malformed.append((name, data))

    for name, key, value in [
        ("boolean-base", "base", True), ("string-base", "base", "2"),
        ("small-base", "base", 1), ("large-base", "base", 63),
        ("bad-e", "e", "2"), ("nonstr-e", "e", 0),
        ("empty-g", "g", ""), ("zero-g", "g", "0"), ("mismatch-g", "g", "11"),
        ("boolean-root", "root", True), ("string-root", "root", "2"),
        ("negative-root", "root", -1), ("large-root", "root", 99), ("accept-root", "root", 1),
        ("bad-nodes", "nodes", {}), ("short-nodes", "nodes", []),
        ("boolean-block", "blocks", [{"start": False, "length": True}]),
        ("string-block", "blocks", [{"start": 0, "length": "1"}]),
        ("wrong-block", "blocks", [{"start": 1, "length": 1}]),
    ]:
        mutation(name, lambda d, k=key, v=value: d.update({k: v}))
    mutation("missing-blocks", lambda d: d.pop("blocks"))
    for name, node, key, value in [
        ("null-reject-arcs", 0, "arcs", None), ("bad-reject-level", 0, "level", 3),
        ("null-accept-arcs", 1, "arcs", None), ("boolean-accept-level", 1, "level", True),
        ("wrong-accept-level", 1, "level", 0), ("boolean-node-level", 2, "level", False),
        ("wrong-node-level", 2, "level", 1), ("dict-arcs", 2, "arcs", {}),
        ("short-arc", 2, "arcs", [[2]]), ("tuple-arc", 2, "arcs", [(2, 1)]),
        ("boolean-label", 2, "arcs", [[True, 1]]), ("negative-label", 2, "arcs", [[-1, 1]]),
        ("oversized-label", 2, "arcs", [[8, 1]]), ("string-child", 2, "arcs", [[2, "1"]]),
        ("boolean-child", 2, "arcs", [[2, True]]), ("oversized-child", 2, "arcs", [[2, 3]]),
        ("cyclic-child", 2, "arcs", [[2, 2]]),
        ("duplicate-label", 2, "arcs", [[2, 1], [2, 1]]),
        ("unsorted-label", 2, "arcs", [[3, 1], [2, 1]]),
    ]:
        mutation(name, lambda d, n=node, k=key, v=value: d["nodes"][n].update({k: v}))
    mutation("nondict-node", lambda d: d["nodes"].__setitem__(2, []))
    two = REF.Oracle(2, "00", "11")
    mutation("premature-accept", lambda d: d["nodes"][d["root"]]["arcs"][0].__setitem__(1, 1),
             certificate(two, {two.terminal}))
    long_gap = REF.Oracle(2, "0" * 7, "1" + "0" * 6)
    malformed.append(("unsupported-gap", certificate(long_gap, {long_gap.terminal})))
    for name, data in malformed:
        expect(name, CERT.check(data)["status"], "UNDECIDED")
    counts["malformed_structural_inputs"] = len(malformed)

    decorated = copy.deepcopy(good)
    decorated.update(status="fabricated", complete=False, cardinality=-100,
                     claimed_count="not a number", iterations=True, digest=None)
    checked = CERT.check(decorated)
    expect("untrusted-metadata-status", checked["status"], "PREDECESSOR_CLOSED_NO_EXTERIOR")
    expect("independent-cardinality", checked.get("set_cardinality"), 1)
    counts["ignored_metadata_controls"] = 2

    complete = CERT.check(good)
    for limit in (1, max(1, complete["operations"] // 2), complete["operations"] - 1):
        expect(f"operation-cap-{limit}", CERT.check(good, operations=limit)["status"], "UNDECIDED")
    with patch.object(CERT.time, "monotonic", side_effect=itertools.count()):
        wall = CERT.check(good, seconds=0.5)
    expect("forced-wall-check", wall["status"], "UNDECIDED")
    fake_rss = 65 * 1024 * (1024 if sys.platform == "darwin" else 1)
    with patch.object(CERT.resource, "getrusage", return_value=SimpleNamespace(ru_maxrss=fake_rss)):
        memory = CERT.check(good, memory_mib=64)
    expect("forced-memory-check", memory["status"], "UNDECIDED")
    counts["in_process_cap_controls"] = 5

    with tempfile.TemporaryDirectory(prefix="agent110-certificate-controls-") as temp:
        directory = Path(temp)
        valid = directory / "valid.json"
        valid.write_text(json.dumps(good))
        malformed_json = directory / "malformed.json"
        malformed_json.write_text('{"base":2,')
        invalid_utf8 = directory / "invalid-utf8.json"
        invalid_utf8.write_bytes(b"\xff")
        oversized = directory / "oversized.json"
        with oversized.open("wb") as stream:
            stream.truncate(128 * 1024 * 1024 + 1)
        cases = [("valid-cli", valid, [], "PREDECESSOR_CLOSED_NO_EXTERIOR", 0),
                 ("malformed-json", malformed_json, [], "UNDECIDED", 2),
                 ("invalid-utf8", invalid_utf8, [], "UNDECIDED", 2),
                 ("missing-file", directory / "missing.json", [], "UNDECIDED", 2),
                 ("directory-input", directory, [], "UNDECIDED", 2),
                 ("input-size-cap", oversized, [], "UNDECIDED", 2),
                 ("cli-operation-cap", valid, ["--operations", "1"], "UNDECIDED", 2),
                 ("cli-wall-cap", valid, ["--seconds", "0.000000001"], "UNDECIDED", 2)]
        for name, path, flags, expected, rc in cases:
            command = [sys.executable] + ([] if __debug__ else ["-O"])
            command += [str(HERE / "p24_reverse_certificate.py"), str(path)] + flags
            run = subprocess.run(command, text=True, capture_output=True, timeout=15, check=False)
            expect(name + "-exit", run.returncode, rc)
            try:
                status = json.loads(run.stdout)["status"]
            except (ValueError, KeyError, TypeError):
                status = "MISSING_JSON"
            expect(name + "-status", status, expected)
    counts["cli_controls"] = len(cases)
    print(json.dumps({"status": "FAIL" if failures else "PASS", **counts,
                      "failures": failures, "seconds": time.monotonic() - started}, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
