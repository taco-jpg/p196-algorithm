#!/usr/bin/env python3
"""Independent controls for cycle-preserving p12 odd-center pruning.

Agent 3 (#303/PR318): odd-center alternating residue and even middle.
Agent 110 (PR338/370): balanced-profile all-repetition reduction.
The small arithmetic oracle below adapts this author's prior p12 controls,
but imports only the baseline mirror: there is no earlier-PR dependency.
Full graph comparison captures process output in memory, never in log files.
"""
import argparse
from collections import deque
import json
from pathlib import Path
import random
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror

E = tuple(map(int, "101010010101" * 2))
G = tuple(map(int, "100010001000" * 2))
V = tuple(sum(G[:t + 1]) // 2 - sum(G[:t]) // 2 for t in range(24))
MASK64 = (1 << 64) - 1


def decode(width, number):
    half = []
    for _ in range((width - 1) // 2):
        number, digit = divmod(number, 19)
        half.append(digit)
    if number:
        raise ValueError("source ID exceeds the selected width")
    return (9,) + tuple(half + half[:(width - 2) // 2][::-1]) + (9,)


def encode(center):
    number = 0
    for digit in reversed(center[1:1 + (len(center) - 1) // 2]):
        number = 19 * number + digit
    return number


def center_step(base, center, entry, overflow, trim):
    digits, carry = mirror.norm(base, center, entry)
    if carry != 1 - entry:
        return None
    if overflow:
        digits.append((base - 1) * entry)
    raw = tuple(a + b for a, b in zip(digits, reversed(digits)))
    if len(raw) <= 2 * trim or any(raw[i] != base - 1 or raw[-i - 1] != base - 1
                                 for i in range(trim)):
        return None
    return raw[trim:len(raw) - trim] if trim else raw


def raw_return(width, number):
    """No cycle-only source predicate is applied to this arithmetic oracle."""
    center = decode(width, number)
    for dt in range(24):
        t = (4 + dt) % 24
        expected_width = len(center) + G[t] - 2 * V[t]
        center = center_step(10, center, E[t], G[t], V[t])
        if center is None:
            return -1
        if len(center) != expected_width or len(center) not in (width - 1, width):
            raise RuntimeError("balanced width profile failed")
    if len(center) != width or center[0] != 9 or center[-1] != 9:
        return -1
    return encode(center)


class Domain:
    """Residue DP and numeric-order rank/unrank, independent of C++ generation."""
    def __init__(self, width):
        if not 2 <= width <= 17:
            raise ValueError("supported widths are 2..17")
        self.width = width
        self.half = (width - 1) // 2
        self.total = 19 ** self.half
        self.odd = width % 2 == 1
        self.weights = [(-1) ** j * (1 if j == self.half - 1 else 2)
                        for j in range(self.half)]
        self.allowed = [tuple(range(0, 19, 2)) if j == self.half - 1
                        else tuple(range(19)) for j in range(self.half)]
        self.dp = [[1] + [0] * 10]
        if self.odd:
            for j, allowed in enumerate(self.allowed):
                row = [0] * 11
                for r, count in enumerate(self.dp[-1]):
                    for digit in allowed:
                        row[(r + self.weights[j] * digit) % 11] += count
                self.dp.append(row)
        self.count = self.dp[-1][9] if self.odd else self.total
        self.flip_count = self.count // 2 if self.odd else (self.total - 1) // 2

    def candidate(self, number):
        if not 0 <= number < self.total:
            return False
        if not self.odd:
            return True
        residue = 0
        for j, weight in enumerate(self.weights):
            number, digit = divmod(number, 19)
            if j == self.half - 1 and digit % 2:
                return False
            residue += weight * digit
        return residue % 11 == 9

    def initial_flip(self, number):
        for _ in range(self.half):
            number, digit = divmod(number, 19)
            if digit != 9:
                return digit < 9
        return False

    def rank(self, number):
        """Number of candidate IDs strictly below an arbitrary raw ID."""
        if not 0 <= number <= self.total:
            raise ValueError("rank input out of range")
        if not self.odd or number == self.total:
            return number if not self.odd else self.count
        digits = []
        for _ in range(self.half):
            number, digit = divmod(number, 19)
            digits.append(digit)
        rank = residue = 0
        for j in range(self.half - 1, -1, -1):
            for digit in self.allowed[j]:
                if digit >= digits[j]:
                    break
                rank += self.dp[j][(9 - residue - self.weights[j] * digit) % 11]
            if digits[j] not in self.allowed[j]:
                return rank
            residue += self.weights[j] * digits[j]
        return rank

    def unrank(self, rank):
        if not 0 <= rank < self.count:
            raise ValueError("candidate rank out of range")
        if not self.odd:
            return rank
        residue = number = 0
        for j in range(self.half - 1, -1, -1):
            for digit in self.allowed[j]:
                block = self.dp[j][(9 - residue - self.weights[j] * digit) % 11]
                if rank < block:
                    number += digit * 19 ** j
                    residue += self.weights[j] * digit
                    break
                rank -= block
            else:
                raise RuntimeError("rank DP found no coefficient")
        if rank or not self.candidate(number):
            raise RuntimeError("candidate unranking failed")
        return number


def domain_controls(rng):
    rows = []
    brute_sources = rank_checks = 0
    for width in range(2, 18):
        domain = Domain(width)
        neutral = (domain.total - 1) // 2
        if domain.initial_flip(neutral) or (domain.odd and domain.candidate(neutral)):
            raise RuntimeError("all-nine source was incorrectly admitted")
        if domain.odd and domain.rank(neutral) != domain.count // 2:
            raise RuntimeError("complement symmetry count failed")
        if width <= 10:
            brute = [n for n in range(domain.total) if domain.candidate(n)]
            brute_sources += domain.total
            if len(brute) != domain.count or sum(domain.initial_flip(n) for n in brute) != domain.flip_count:
                raise RuntimeError("candidate DP disagrees with exhaustive small domain")
            for r, n in enumerate(brute):
                if domain.unrank(r) != n or domain.rank(n) != r:
                    raise RuntimeError("rank DP disagrees with numeric-order enumeration")
                rank_checks += 1
        elif domain.count:
            ranks = {0, domain.count - 1, domain.count // 2}
            ranks.update(rng.randrange(domain.count) for _ in range(256))
            for r in ranks:
                n = domain.unrank(r)
                if domain.rank(n) != r or domain.rank(domain.total - 1 - n) != domain.count - 1 - r:
                    raise RuntimeError("large-domain rank/complement control failed")
                rank_checks += 1
        rows.append({"width": width, "unfiltered_states": domain.total,
                     "candidates": domain.count, "initial_flip": domain.flip_count})
    return {"counts": rows, "brute_sources": brute_sources, "rank_checks": rank_checks}


def edge_digest(edges):
    digest = 14695981039346656037
    for source, target in edges:
        for value in (source, target):
            for byte in value.to_bytes(8, "little"):
                digest = ((digest ^ byte) * 1099511628211) & MASK64
    return f"{digest:016x}"


def analyze_graph(edges):
    successor = dict(edges)
    if len(successor) != len(edges):
        raise RuntimeError("multiple return edges from one source")
    active = set(successor) | set(successor.values())
    indegree = dict.fromkeys(active, 0)
    for target in successor.values():
        indegree[target] += 1
    queue = deque(node for node, degree in indegree.items() if degree == 0)
    removed = []
    while queue:
        node = queue.popleft()
        removed.append(node)
        if node in successor:
            target = successor[node]
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    remaining = {node for node, degree in indegree.items() if degree}
    cycles = 0
    visited = set()
    for node in remaining:
        if node in visited:
            continue
        cycles += 1
        while node not in visited:
            visited.add(node)
            node = successor[node]
    distance = {}
    if not remaining:
        for node in reversed(removed):
            distance[node] = 0 if node not in successor else distance[successor[node]] + 1
    return {"cycle_nodes": len(remaining), "cycles": cycles,
            "max_path_edges": max(distance.values(), default=0) if not remaining else None,
            "targets_that_are_sources": sorted(set(successor) & set(successor.values()))}


def oracle_controls():
    known = 0
    for base, edges in mirror._lean_certs():
        for B, C, _, target, _, trim in edges:
            if center_step(base, C, mirror.e1(base, B), mirror.gam(base, B, C), trim) != tuple(target):
                raise RuntimeError("known-source center arithmetic failed")
            known += 1
    graphs = [([], 0, 0), ([(1, 2)], 0, 1), ([(1, 2), (2, 3)], 0, 2),
              ([(1, 1)], 1, None), ([(1, 2), (2, 1)], 1, None),
              ([(1, 2), (2, 1), (3, 4), (4, 3), (5, 1)], 2, None)]
    for edges, cycles, length in graphs:
        result = analyze_graph(edges)
        if result["cycles"] != cycles or result["max_path_edges"] != length:
            raise RuntimeError("independent cycle detector fixture failed")
    return {"known_source_edges": known, "cycle_detector_fixtures": len(graphs)}


def compare_map(binary, width, numbers):
    expected = {number: raw_return(width, number) for number in numbers}
    run = subprocess.run([str(binary), "--map", str(width)],
                         input="".join(f"{number}\n" for number in numbers),
                         text=True, capture_output=True, timeout=60, check=False)
    if run.returncode:
        raise RuntimeError(f"map process failed: {binary}: {run.stderr}")
    actual = {}
    for line in run.stdout.splitlines():
        fields = line.split()
        if len(fields) != 2:
            raise RuntimeError("malformed map output")
        source, target = map(int, fields)
        if source in actual:
            raise RuntimeError("duplicate map source")
        actual[source] = target
    if actual != expected:
        bad = next((n for n in numbers if actual.get(n) != expected[n]), None)
        raise RuntimeError(f"map mismatch {binary} width={width} ID={bad}")
    domain = Domain(width)
    for target in expected.values():
        if target >= 0 and not domain.candidate(target):
            raise RuntimeError("completed raw return violates target invariant")
    return sum(target >= 0 for target in expected.values())


def map_controls(binaries, rng, samples):
    rows = []
    remaining = samples
    for width in range(2, 18):
        domain = Domain(width)
        if width <= 8:
            numbers = list(range(domain.total))
        else:
            quota = 512 if width <= 14 else (remaining + 17 - width) // (18 - width)
            if width >= 15:
                remaining -= quota
            numbers = {0, domain.total - 1, (domain.total - 1) // 2}
            for boundary in ((1 << 31) - 1, 1 << 31, (1 << 32) - 1, 1 << 32, (1 << 32) + 1):
                if boundary < domain.total:
                    numbers.add(boundary)
            while len(numbers) < quota:
                numbers.add(domain.unrank(rng.randrange(domain.count)) if domain.count and rng.randrange(2)
                            else rng.randrange(domain.total))
            numbers = sorted(numbers)
        hits = [compare_map(binary, width, numbers) for binary in binaries]
        rows.append({"width": width, "states": len(numbers), "successful_returns": hits[0]})
    groups = {1854137: (421084, 421255, 424333, 424504, 482815, 482986, 486064, 486235),
              1944526: (702607, 702778, 705856, 706027, 764338, 764509, 767587, 767758)}
    fixtures = {source: target for target, sources in groups.items() for source in sources}
    fixtures.update({target: -1 for target in groups})
    for source, target in fixtures.items():
        if raw_return(11, source) != target:
            raise RuntimeError("raw positive fixture failed")
    fixture_rows = []
    for padding in range(4):
        width = 11 + 2 * padding
        factor = 19 ** padding
        offset = (factor - 1) // 2
        lifted = {offset + factor * source: offset + factor * target if target >= 0 else -1
                  for source, target in fixtures.items()}
        for source, target in lifted.items():
            if raw_return(width, source) != target:
                raise RuntimeError("neutral-padding positive fixture failed")
        for binary in binaries:
            if compare_map(binary, width, sorted(lifted)) != 16:
                raise RuntimeError("cycle pruning was incorrectly applied to raw map")
        fixture_rows.append({"width": width, "states": len(lifted),
                             "successful_returns": 16,
                             "source_ids_above_uint32": sum(n > (1 << 32) - 1 for n in lifted)})
    fixture_total = sum(row["states"] for row in fixture_rows)
    return {"width_batches": rows, "positive_fixture_states": fixture_total,
            "padding_fixtures": fixture_rows,
            "maps_per_binary": sum(row["states"] for row in rows) + fixture_total}


def graph_run(binary, width, seconds):
    command = [str(binary), str(width), "--edges", "--seconds", str(seconds)]
    run = subprocess.run(command, text=True, capture_output=True, timeout=seconds + 15, check=False)
    edges = []
    summaries = []
    witnesses = []
    for line in run.stdout.splitlines():
        if line.startswith("EDGE "):
            _, source, target = line.split()
            edges.append((int(source), int(target)))
        elif line.startswith("{"):
            event = json.loads(line)
            if event.get("type") in ("center_cycle", "center_edge"):
                witnesses.append(event)
            else:
                summaries.append(event)
        elif line.startswith("CYCLE_EDGE "):
            witnesses.append({"record": line})
        elif line.strip():
            raise RuntimeError(f"unexpected graph output: {line[:120]}")
    if len(summaries) != 1:
        raise RuntimeError("missing unique graph completion summary")
    summary = summaries[0]
    if summary.get("status") == "CENTER_CYCLE" or witnesses:
        candidate = {"status": "CENTER_CYCLE", "command": command,
                     "summary": summary, "witnesses": witnesses}
        print(json.dumps({"center_cycle_found": candidate}, sort_keys=True), flush=True)
        return candidate, edges
    if (run.returncode or not summary.get("cycle_scan_complete")
            or not summary.get("enumeration_complete", True)
            or summary.get("status") not in ("NONE", "NO_CENTER_CYCLE")):
        return {"status": "UNDECIDED", "command": command,
                "returncode": run.returncode, "summary": summary}, None
    if edges != sorted(set(edges)):
        raise RuntimeError("graph edges are not sorted and unique")
    domain = Domain(width)
    checks = {"evaluated_candidates": domain.count, "initial_flip_valid": domain.flip_count}
    for key, expected in checks.items():
        if summary.get(key) != expected:
            raise RuntimeError(f"summary mismatch {key}: {summary.get(key)} != {expected}")
    if summary.get("expected_candidates", summary.get("candidate_states")) != domain.count:
        raise RuntimeError("wrong candidate-domain count")
    if summary.get("unfiltered_states", summary.get("full_source_states")) != domain.total:
        raise RuntimeError("wrong raw source-domain count")
    if summary.get("retained_edges", summary.get("edges")) != len(edges):
        raise RuntimeError("edge count differs from complete emitted edge list")
    if str(summary.get("edge_digest", "")).removeprefix("fnv1a64:") != edge_digest(edges):
        raise RuntimeError("edge digest mismatch")
    if summary.get("target_invariant_rejections", 0):
        raise RuntimeError("unexpected odd-target invariant rejection")
    if any(not domain.candidate(source) or not domain.candidate(target) for source, target in edges):
        raise RuntimeError("retained graph edge leaves the candidate domain")
    analysis = analyze_graph(edges)
    if analysis["cycle_nodes"] or summary.get("cycles_found", 0):
        raise RuntimeError("CENTER CYCLE FOUND: preserve the complete returned graph")
    if summary.get("cycle_nodes", 0) != analysis["cycle_nodes"]:
        raise RuntimeError("independent graph-cycle count disagrees")
    if summary.get("max_path_edges", analysis["max_path_edges"]) != analysis["max_path_edges"]:
        raise RuntimeError("maximum filtered-graph path mismatch")
    if summary.get("removed", domain.count) != domain.count:
        raise RuntimeError("independent graph peel was incomplete")
    return {"status": "COMPLETE", "summary": summary, "analysis": analysis}, edges


def compare_graphs(binaries, width, seconds, rng):
    started = time.monotonic()
    first, edges = graph_run(binaries[0], width, seconds)
    if first["status"] == "CENTER_CYCLE":
        return {"width": width, "status": "CENTER_CYCLE", "primary": first}
    if edges is None:
        return {"width": width, "status": "UNDECIDED", "primary": first}
    second, other = graph_run(binaries[1], width, seconds)
    if second["status"] == "CENTER_CYCLE":
        return {"width": width, "status": "CENTER_CYCLE", "independent": second}
    if other is None:
        return {"width": width, "status": "UNDECIDED", "independent": second}
    if edges != other:
        raise RuntimeError(f"complete sparse graphs disagree at width {width}")
    a, b = first["summary"], second["summary"]
    if a.get("completed_24_steps") != b.get("completed_returns"):
        raise RuntimeError("completed finite trajectory counts disagree")
    chosen = edges if len(edges) <= 256 else [edges[i] for i in sorted(rng.sample(range(len(edges)), 256))]
    for source, target in chosen:
        if raw_return(width, source) != target:
            raise RuntimeError("emitted graph edge failed independent mirror replay")
    return {"width": width, "status": "COMPLETE_IDENTICAL_ACYCLIC_GRAPHS",
            "edges": len(edges), "edge_digest": edge_digest(edges),
            "replayed_edges": len(chosen), "first_examples": edges[:8],
            "primary": first, "independent": second, "seconds": time.monotonic() - started}


def safeguard_controls(binaries):
    result = []
    for binary in binaries:
        bad = subprocess.run([str(binary), "--map", "17"], input=f"{19 ** 8}\n",
                             text=True, capture_output=True, timeout=10, check=False)
        if bad.returncode == 0 or bad.stdout.strip():
            raise RuntimeError("invalid 64-bit map ID was accepted")
        capped = subprocess.run([str(binary), "17", "--seconds", "1"],
                                text=True, capture_output=True, timeout=15, check=False)
        summaries = [json.loads(line) for line in capped.stdout.splitlines() if line.startswith("{")]
        if capped.returncode != 2 or len(summaries) != 1 or summaries[0].get("status") != "UNDECIDED":
            raise RuntimeError("wall cap was not explicitly undecided")
        result.append({"binary": str(binary), "invalid_id_exit": bad.returncode,
                       "time_cap_status": "UNDECIDED", "time_cap_exit": capped.returncode})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primary", type=Path)
    parser.add_argument("--independent", type=Path)
    parser.add_argument("--samples", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=1101715)
    parser.add_argument("--regression-widths", type=int, nargs="*", default=list(range(2, 11)))
    parser.add_argument("--full-widths", type=int, nargs="*", default=[])
    parser.add_argument("--seconds", type=int, default=1500)
    parser.add_argument("--safeguards", action="store_true")
    args = parser.parse_args()
    if args.samples < 100 or not 1 <= args.seconds <= 1500:
        parser.error("samples >= 100 and seconds in 1..1500 are required")
    if bool(args.primary) != bool(args.independent):
        parser.error("provide both executables, or neither for arithmetic-only controls")
    rng = random.Random(args.seed)
    result = {"domains": domain_controls(rng), "oracle": oracle_controls()}
    if args.primary:
        binaries = [args.primary.resolve(), args.independent.resolve()]
        result["map_controls"] = map_controls(binaries, rng, args.samples)
        if args.safeguards:
            result["safeguards"] = safeguard_controls(binaries)
        result["graphs"] = []
        for width in dict.fromkeys(args.regression_widths + args.full_widths):
            answer = compare_graphs(binaries, width, args.seconds, rng)
            result["graphs"].append(answer)
            print(json.dumps({"graph_comparison": answer}, sort_keys=True), flush=True)
            if answer["status"] == "CENTER_CYCLE":
                break
        result["status"] = ("CENTER_CYCLE" if any(row["status"] == "CENTER_CYCLE" for row in result["graphs"])
                            else "PASS" if all(row["status"].startswith("COMPLETE_")
                                               for row in result["graphs"]) else "UNDECIDED")
    else:
        result["status"] = "PASS"
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0 if result["status"] == "PASS" else 3 if result["status"] == "CENTER_CYCLE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
