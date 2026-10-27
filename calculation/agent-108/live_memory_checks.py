#!/usr/bin/env python3
"""Independent regression for live-memory exterior MDD evaluation.

Reference: a preserved published binary without live collection.  Candidate:
the new binary, tested both without --live and with collection every 1, 2, 7
completed images.  Small reference frontiers are independently reconstructed
with the tuple oracle.  Live frontiers are compared as complete word sets at
selected widths (quick suite) or every reported width (full suite).

Brent may detect a true layer recurrence later than the historical evaluator.
The reference recurrence reduces those later widths exactly; both reported
equal frontiers are then compared as actual sets.  Witnesses are checked by
the A120 mirror and ordinary integer arithmetic in their original phase order.

The SQ5 suite compares all 40 layer counts and selected complete sets.  It does
not repeat the earlier expensive standalone tuple run or claim a new result.

Usage:
  python3 calculation/agent-108/live_memory_checks.py --reference OLD --candidate NEW
  python3 calculation/agent-108/live_memory_checks.py --reference OLD --candidate NEW --suite full
  python3 calculation/agent-108/live_memory_checks.py --reference OLD --candidate NEW --suite sq5
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

import exterior_controls as controls
import saturation_oracle as oracle


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def binary_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def command(binary, pattern, carry=None, cadence=None, depth=256,
            nodes=2000000, operations=400000000, seconds=60):
    args = [binary, pattern, str(nodes), str(operations), str(depth), str(seconds)]
    if carry is not None:
        args += ["--e", carry]
    if cadence is not None:
        args += ["--live", "--collect-every", str(cadence)]
    return args


def run(args, witness=False, allow_cap=False):
    executed = subprocess.run(args + (["--witness"] if witness else []),
                              text=True, capture_output=True, timeout=70)
    records = [json.loads(line) for line in executed.stdout.splitlines()]
    results = [record for record in records if isinstance(record, dict) and record.get("type") == "RESULT"]
    require(len(results) == 1, ("Missing unique result", args, executed.stderr))
    result = results[0]
    require(executed.returncode in ((0, 3) if allow_cap else (0,)),
            ("Unexpected process status", args, executed.returncode, result))
    if not allow_cap:
        require(result["status"] != "UNDECIDED", ("Incomplete regression", args, result))
    layers = [record for record in records if record.get("type") == "LAYER"]
    require([layer["depth"] for layer in layers] == list(range(len(layers))),
            ("Nonconsecutive driver layers", args))
    witnesses = [record for record in records if record.get("type") == "WITNESS"]
    return result, layers, witnesses


def export(args, depth):
    completed = subprocess.run(args + ["--export-layer", str(depth)], text=True,
                               capture_output=True, timeout=70, check=True)
    record = json.loads(completed.stdout.strip().splitlines()[-1])
    require(isinstance(record, list), ("Export ended before requested width", args, depth, record))
    return frozenset(tuple(word) for word in record)


class TupleFrontiers:
    def __init__(self):
        self.cache = {}

    def at(self, pattern, depth):
        bits = tuple(map(int, pattern))
        if pattern not in self.cache:
            period = len(bits)
            self.cache[pattern] = [frozenset({((0,) * period, bits, (1,) * sum(bits))})]
        sequence = self.cache[pattern]
        while len(sequence) <= depth:
            previous_depth = len(sequence) - 1
            following = frozenset(
                target
                for source in sequence[-1]
                for target in oracle._successor_columns(10, bits, source, previous_depth == 0)
            )
            require(len(following) <= 1000000, "Small tuple control exceeded its declared state budget")
            sequence.append(following)
        return sequence[depth]


class Reference:
    def __init__(self, binary, pattern, carry, tuples=None):
        self.pattern, self.carry = pattern, carry
        self.args = command(binary, pattern, carry)
        self.result, self.layers, _ = run(self.args)
        self.word_cache = {}
        self.tuples = tuples
        if tuples is not None:
            bits = tuple(map(int, pattern))
            wanted = None if carry is None else tuple(map(int, carry))
            for layer in self.layers:
                frontier = tuples.at(pattern, layer["depth"])
                accepted = sum(oracle.is_accepting(10, bits, state)
                               and (wanted is None or state[0] == wanted) for state in frontier)
                require(len(frontier) == int(layer["states"]) and accepted == int(layer["accepts"]),
                        ("Published reference differs from tuple oracle", pattern, carry, layer["depth"]))

    def reduced_depth(self, depth):
        if depth < len(self.layers):
            return depth
        if self.result["reason"] == "empty_layer":
            return self.result["depth"]
        if self.result["reason"] == "exact_layer_repeat":
            start = self.result["cycle_start"]
            period = self.result["depth"] - start
            require(start >= 1 and period > 0, "Malformed reference recurrence")
            return start + (depth - start) % period
        raise RuntimeError(("Reference has no justified later frontier", self.pattern, depth))

    def counts(self, depth):
        layer = self.layers[self.reduced_depth(depth)]
        return int(layer["states"]), int(layer["accepts"])

    def words(self, depth):
        reduced = self.reduced_depth(depth)
        if reduced not in self.word_cache:
            words = export(self.args, reduced)
            if self.tuples is not None:
                expected = frozenset(controls.encode_cut(state, self.pattern)
                                     for state in self.tuples.at(self.pattern, reduced))
                require(words == expected, ("Published reference word-set differs from tuple oracle",
                                            self.pattern, self.carry, reduced))
            self.word_cache[reduced] = words
        return self.word_cache[reduced]


def check_telemetry(result, layers, cadence):
    require(result["mode"] == "live", "Requested live mode was not enabled")
    require(result["nodes"] == result["nodes_created"] - result["collected_nodes"],
            "Live node accounting is inconsistent")
    require(result["nodes"] <= result["peak_live_nodes"] <= result["nodes_created"],
            "Live peak accounting is inconsistent")
    for layer in layers:
        require(layer["nodes"] == layer["nodes_created"] - layer["collected_nodes"],
                ("Layer node accounting is inconsistent", layer["depth"]))
    if result["depth"] >= max(7, cadence):
        require(result["collections"] > 0 and result["collected_nodes"] > 0,
                "Deep forced-collection control collected no nodes")
    retained_bound = 2 * math.ceil(math.log2(result["depth"] + 1)) + 8
    require(result["peak_retained_roots"] <= retained_bound,
            ("Retained roots exceed generous logarithmic replay bound", result))


def compare_case(candidate, reference, cadence, every_layer=False, selected=None):
    args = command(candidate, reference.pattern, reference.carry, cadence)
    result, layers, witnesses = run(args, witness=True)
    require(result["status"] == reference.result["status"],
            ("Live result scope differs from reference", reference.pattern, reference.carry, cadence, result))
    require(result["g"] == reference.pattern and result["requested_e"] == (reference.carry or ""),
            "Live result lost original phase/filter metadata")
    for layer in layers:
        require((int(layer["states"]), int(layer["accepts"])) == reference.counts(layer["depth"]),
                ("Live frontier count differs", reference.pattern, reference.carry, cadence, layer["depth"]))
    if result["status"] == "FEASIBLE":
        require(result["depth"] == reference.result["depth"], "First terminal depth changed")
        require(result["witness_complete"] and witnesses, "Uncapped positive replay lost its witness")
    if result["reason"] == "exact_layer_repeat":
        require(1 <= result["cycle_start"] < result["depth"], "Brent recurrence includes invalid first mode")
        require(reference.words(result["cycle_start"]) == reference.words(result["depth"]),
                "Brent claimed equality of different exact frontiers")
    depth = result["depth"]
    if every_layer:
        widths = set(range(depth + 1))
    elif selected is not None:
        widths = {width for width in selected if width <= depth}
    else:
        widths = {0, 1, 2, 3, 7, 12, 17, depth // 2, max(0, depth - 1), depth}
        widths = {width for width in widths if width <= depth}
    if result["cycle_start"] >= 0:
        widths.add(result["cycle_start"])
        widths.add(depth)
    word_records = 0
    for width in sorted(widths):
        words = export(args, width)
        require(words == reference.words(width),
                ("Collected exact word-set differs", reference.pattern, reference.carry, cadence, width))
        word_records += len(words)
    mirror_edges = integer_edges = 0
    for witness in witnesses:
        require(witness["g"] == reference.pattern, "Live witness lost the original overflow rotation")
        if reference.carry is not None:
            require(witness["e"] == reference.carry, "Live witness lost the requested carry rotation")
        carry = tuple(map(int, witness["e"]))
        replay = oracle.mirror_check_witness(10, reference.pattern, carry, witness["B_t"])
        mirror_edges += replay["edges"]
        integer_edges += oracle.integer_witness_controls(10, reference.pattern, carry, witness["B_t"])
    check_telemetry(result, layers, cadence)
    summary = {
        "g": reference.pattern, "e": reference.carry, "cadence": cadence,
        "status": result["status"], "depth": depth, "cycle_start": result["cycle_start"],
        "layer_counts": len(layers), "exact_word_sets": len(widths), "word_records": word_records,
        "mirror_edges": mirror_edges, "integer_edges": integer_edges,
        "nodes_created": result["nodes_created"], "peak_live_nodes": result["peak_live_nodes"],
        "collections": result["collections"], "collected_nodes": result["collected_nodes"],
        "peak_retained_roots": result["peak_retained_roots"],
        "historical_reference_nodes": reference.result["nodes"],
    }
    print("LIVE_CASE", json.dumps(summary, sort_keys=True), "PASS", flush=True)
    return summary


def malformed_and_caps(candidate):
    prefix = command(candidate, "100010001000")
    malformed = [
        prefix + ["--live", "--collect-every", "0"],
        prefix + ["--live", "--collect-every", "-1"],
        prefix + ["--live", "--collect-every", "nan"],
        prefix + ["--live", "--collect-every"],
        prefix + ["--collect-every", "1"],
        prefix + ["--live", "--export-layer", "257"],
    ]
    for args in malformed:
        executed = subprocess.run(args, text=True, capture_output=True, timeout=10)
        require(executed.returncode == 2, ("Malformed live input was not rejected", args))
        record = json.loads(executed.stderr.strip().splitlines()[-1])
        require(record["status"] == "ERROR", "Malformed live input became a mathematical outcome")
    caps = [
        (command(candidate, "100010001000", cadence=1, nodes=2), "node_cap"),
        (command(candidate, "100010001000", cadence=1, operations=1), "operation_cap"),
        (command(candidate, "100010001000", cadence=1, depth=0), "depth_cap"),
    ]
    for args, reason in caps:
        result, _, witnesses = run(args, witness=True, allow_cap=True)
        require(result["status"] == "UNDECIDED" and result["reason"] == reason and not witnesses,
                ("Live resource cap was misclassified", reason, result))
    print(f"LIVE_GUARDS malformed={len(malformed)} explicit_caps={len(caps)} PASS", flush=True)


def semantic_caps(candidate):
    """Exercise live-node budget recovery and a cap after positive detection."""
    pattern = "11100010000"
    history, _, _ = run(command(candidate, pattern, nodes=700), allow_cap=True)
    live, _, witnesses = run(command(candidate, pattern, cadence=1, nodes=700),
                             witness=True, allow_cap=True)
    require(history["status"] == "UNDECIDED" and history["reason"] == "node_cap",
            "Historical cap700 control unexpectedly completed")
    require(live["status"] == "FEASIBLE" and live["reason"] == "terminal_reached"
            and live["depth"] == 29 and live["witness_complete"] and len(witnesses) == 1,
            "Live cap700 control did not recover a complete positive witness")
    require(live["peak_live_nodes"] <= 700 < live["nodes_created"],
            "Live capacity was not measured on resident nodes")
    positive, _, _ = run(command(candidate, pattern, cadence=1))
    replay_cap, _, witnesses = run(command(candidate, pattern, cadence=1,
                                           operations=positive["operations"]),
                                   witness=True, allow_cap=True)
    require(replay_cap["status"] == "FEASIBLE"
            and replay_cap["reason"] == "operation_cap"
            and replay_cap["depth"] == positive["depth"]
            and not replay_cap["witness_complete"] and not witnesses,
            "A witness reconstruction cap changed or overstated the established positive")
    print("LIVE_SEMANTIC_CAPS", json.dumps({
        "cap700_history_status": history["status"],
        "cap700_live_status": live["status"],
        "cap700_live_peak_nodes": live["peak_live_nodes"],
        "cap700_live_nodes_created": live["nodes_created"],
        "positive_search_operations": positive["operations"],
        "replay_cap_status": replay_cap["status"],
        "replay_cap_reason": replay_cap["reason"],
        "replay_cap_witness_complete": replay_cap["witness_complete"],
    }, sort_keys=True), "PASS", flush=True)


def check_legacy(candidate, reference):
    result, layers, _ = run(command(candidate, reference.pattern, reference.carry))
    require(result["mode"] == "history", "Default mode silently enabled collection")
    require(result["status"] == reference.result["status"]
            and result["depth"] == reference.result["depth"]
            and result["cycle_start"] == reference.result["cycle_start"], "Historical driver changed")
    require([(int(x["states"]), int(x["accepts"])) for x in layers]
            == [(int(x["states"]), int(x["accepts"])) for x in reference.layers],
            "Historical frontier counts changed")
    require(result["collections"] == 0 and result["collected_nodes"] == 0,
            "Historical mode unexpectedly deleted nodes")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--suite", choices=("quick", "full", "sq5"), default="quick")
    args = parser.parse_args()
    fingerprints = {path: binary_digest(path) for path in (args.reference, args.candidate)}
    malformed_and_caps(args.candidate)
    semantic_caps(args.candidate)
    summaries = []
    if args.suite == "sq5":
        reference = Reference(args.reference, controls.TARGET_G, None)
        require(reference.result["reason"] == "empty_layer" and reference.result["depth"] == 39,
                "Published SQ5 baseline differs from the established control")
        check_legacy(args.candidate, reference)
        for cadence in (1, 2, 7):
            summaries.append(compare_case(args.candidate, reference, cadence,
                                          selected=(0, 1, 5, 6, 22, 23, 30, 38, 39)))
    else:
        tuples = TupleFrontiers()
        cases = [
            ("11100010000", None),
            ("00011100010", "01110100110"),
            ("100010001000", None),
            ("001000100010", "101001010110"),
            ("100010001000", "000000000000"),
            ("1000100010001000", None),
            ("10000", None),
        ]
        for pattern, carry in cases:
            reference = Reference(args.reference, pattern, carry, tuples)
            check_legacy(args.candidate, reference)
            for cadence in (1, 2, 7):
                summaries.append(compare_case(args.candidate, reference, cadence,
                                              every_layer=args.suite == "full"))
    for path, original in fingerprints.items():
        require(binary_digest(path) == original, ("Binary changed during verification", path))
    totals = {key: sum(summary[key] for summary in summaries)
              for key in ("layer_counts", "exact_word_sets", "word_records", "mirror_edges", "integer_edges")}
    totals.update({"cases": len(summaries), "suite": args.suite,
                   "reference_sha256": fingerprints[args.reference],
                   "candidate_sha256": fingerprints[args.candidate]})
    print("LIVE_MEMORY_CHECKS", json.dumps(totals, sort_keys=True), "PASS", flush=True)


if __name__ == "__main__":
    main()
