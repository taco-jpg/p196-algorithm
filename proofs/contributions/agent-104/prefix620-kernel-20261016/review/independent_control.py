#!/usr/bin/env python3
"""独立有限控制：不导入证书生成器、FastPred 或其逆像实现。

长来源的转移表直接穷举每列 19 个来源系数和 2 个高端进位，
检查普通除法和余数等式。短来源用完整整数十进制展开计算下一对和字。
这些 Python 检查属于有限交叉控制，不代替 Lean 的全称语义证明。
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import random
import time


EXPECTED_HASH = "e6c447fa7efa26e94d1a8064a9336922d3eeb2e1e55176f8043e1cd9dbe3cea5"
WIDTH = 7


def ordinary_pair_word(n: int) -> tuple[int, ...]:
    ds = tuple(map(int, reversed(str(n))))
    return tuple(x + y for x, y in zip(ds, reversed(ds)))


def exact_pair_step(q: tuple[int, ...]) -> tuple[int, ...]:
    # The evaluated pair word is the genuine reverse-and-add output integer.
    return ordinary_pair_word(sum(x * 10**i for i, x in enumerate(q)))


def short_words():
    for n in range(1, WIDTH):
        for half in product(range(19), repeat=(n + 1) // 2):
            if half[0] == 0 or (n % 2 and half[-1] % 2):
                continue
            yield tuple(half[min(i, n - 1 - i)] for i in range(n))


def forward_prefix(q: tuple[int, ...], inner: int) -> tuple[int, ...]:
    low, c = [], 0
    for x in q:
        c, d = divmod(x + c, 10)
        low.append(d)
    high, c = [], inner
    for x in reversed(q):
        c, d = divmod(x + c, 10)
        high.append(d)
    high.reverse()
    if c:
        high = [1] + high
    return tuple(a + b for a, b in zip(low, high))


def independent_tables():
    no, overflow = defaultdict(list), defaultdict(list)
    # No algebraic candidate formula is used: enumerate literal digit sums.
    for x, y, a, z in product(range(2), range(2), range(19), range(2)):
        nxt, lo = divmod(a + x, 10)
        out, hi = divmod(a + z, 10)
        if out == y:
            no[(lo + hi, x, y)].append((a, nxt, z))
    for prev, x, y, a, z in product(range(19), range(2), range(2), range(19), range(2)):
        nxt, lo = divmod(a + x, 10)
        out, hi = divmod(prev + z, 10)
        if out == y:
            overflow[(lo + hi, prev, x, y)].append((a, nxt, z))
    return no, overflow


NO_TABLE, OVERFLOW_TABLE = independent_tables()


def long_predecessors(p: tuple[int, ...]) -> set[tuple[int, ...]]:
    if len(p) != WIDTH:
        return set()
    found = set()

    def no_walk(i, x, y, source):
        if i == WIDTH:
            found.add(source)
            return
        for a, nxt, z in NO_TABLE[(p[i], x, y)]:
            if i == 0 and a == 0:
                continue
            no_walk(i + 1, nxt, z, source + (a,))

    def overflow_walk(i, prev, x, y, source):
        if i == WIDTH:
            if any((prev + z) // 10 == y for z in range(2)):
                found.add(source)
            return
        for a, nxt, z in OVERFLOW_TABLE[(p[i], prev, x, y)]:
            overflow_walk(i + 1, a, nxt, z, source + (a,))

    no_walk(0, 0, 0, ())
    # Exhaust the positive outer sum; do not call overflowFirst.
    for outer in range(1, 19):
        if outer % 10 + 1 == p[0] and any((outer + z) // 10 == 1 for z in range(2)):
            overflow_walk(1, outer, outer // 10, 1, (outer,))
    return found


def expected_initial() -> set[tuple[int, ...]]:
    result = set()
    for n in range(3, WIDTH + 1):
        for tail in product(range(10), repeat=n - 3):
            w = (6, 2, 0) + tail
            if n == WIDTH or (w == w[::-1] and (n % 2 == 0 or w[n // 2] % 2 == 0)):
                result.add(w)
    return result


def rank_failure(ranks, graph):
    for target, preds in graph.items():
        if target not in ranks:
            continue
        for source in preds:
            if source not in ranks:
                return "missing_predecessor"
            if not ranks[source] < ranks[target]:
                return "nondecreasing_rank"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("certificate", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    started = time.monotonic()
    raw = args.certificate.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_HASH
    data = json.loads(raw)
    assert data["width"] == WIDTH and data["prefix"] == "620"
    nodes = data["nodes"]
    ranks = {tuple(row["word"]): row["rank"] for row in nodes}
    assert len(ranks) == len(nodes) == 59189, "duplicate or missing node"
    assert all(0 < q[0] and len(q) <= 32 and all(0 <= x < 19 for x in q) for q in ranks)
    assert all(isinstance(r, int) and r >= 0 for r in ranks.values())
    initials = {tuple(w) for w in data["initial"]}
    assert len(initials) == len(data["initial"]) == 10002
    assert initials == expected_initial()
    assert all(w in ranks and ranks[w] <= 11 for w in initials)
    assert max(ranks[w] for w in initials) == 11
    print("initial and source-data checks passed", flush=True)

    short_inverse = defaultdict(set)
    counts = Counter()
    for q in short_words():
        counts[len(q)] += 1
        short_inverse[exact_pair_step(q)].add(q)
    assert sum(counts.values()) == 10467
    graph, long_graph, short_edges = {}, {}, []
    forward_checks = 0
    for target in ranks:
        lp = long_predecessors(target)
        long_graph[target] = lp
        sp = short_inverse.get(target, set())
        graph[target] = lp | sp
        for source in lp:
            assert target in {forward_prefix(source, 0), forward_prefix(source, 1)}
            forward_checks += 1
        for source in sp:
            short_edges.append({"source": source, "target": target,
                                "source_rank": ranks.get(source), "target_rank": ranks[target]})
    assert rank_failure(ranks, graph) is None
    for target, preds in graph.items():
        exact_rank = 0 if not preds else 1 + max(ranks[q] for q in preds)
        assert ranks[target] == exact_rank, (target, ranks[target], exact_rank)
    edges = sum(map(len, graph.values()))
    assert edges == 71560
    assert len(short_edges) == 6
    print("all 59,189 rows and 71,560 edges independently checked", flush=True)

    def layers(initial, edges):
        current, counts = initial, []
        reached = set()
        while current:
            counts.append(len(current))
            reached.update(current)
            current = set().union(*(edges[w] for w in current))
            assert len(counts) <= 12
        counts.append(0)
        return counts, reached

    all_layers, reached = layers(initials, graph)
    long_layers, _ = layers({w for w in initials if len(w) == WIDTH}, long_graph)
    assert all_layers == data["layer_counts"]
    assert long_layers == data["long_only_layer_counts"]
    assert reached == set(ranks)
    assert data["palindrome_height_bound"] == 1 + max(ranks[w] for w in initials) == 12

    # Independent ordinary-integer checks cover short words, the seven-column
    # boundary, overlapping prefixes, long separated prefixes and trailing zeros.
    rng = random.Random(104620)
    samples = list(range(1, 100000))
    for width in range(7, 61):
        lo, hi = 10**(width - 1), 10**width
        samples.extend(rng.randrange(lo, hi) for _ in range(64))
        samples.extend([lo, hi - 1, 6 * lo, 62 * 10**(width - 2), 620 * 10**(width - 3)])
    sample_widths = Counter()
    for n in samples:
        q = ordinary_pair_word(n)
        nxt_n = n + int(str(n)[::-1])
        nxt_q = ordinary_pair_word(nxt_n)
        assert exact_pair_step(q) == nxt_q
        source, target = q[:WIDTH], nxt_q[:WIDTH]
        sample_widths[len(q)] += 1
        if len(q) >= WIDTH:
            assert target in {forward_prefix(source, 0), forward_prefix(source, 1)}
        if target in ranks:
            assert source in graph[target] and ranks[source] < ranks[target]

    # Negative controls are run on in-memory copies only.
    edge = short_edges[0]
    source, target = tuple(edge["source"]), tuple(edge["target"])
    missing = dict(ranks)
    del missing[source]
    assert rank_failure(missing, graph) == "missing_predecessor"
    equal_rank = dict(ranks)
    equal_rank[source] = ranks[target]
    assert rank_failure(equal_rank, graph) == "nondecreasing_rank"
    omitted_initial = initials - {(6, 2, 0, 2, 6)}
    assert omitted_initial != expected_initial()
    assert not all(ranks[w] <= 10 for w in initials)

    report = {
        "status": "PASS",
        "evidence_class": "independent finite Python controls, not Lean proof",
        "certificate_sha256": EXPECTED_HASH,
        "control_script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "independence": "No generator or Lean inverse implementation imported. Literal 19-by-2 arithmetic table enumeration; short images through Python integer decimal expansion.",
        "node_count": len(ranks),
        "node_width_counts": dict(sorted(Counter(map(len, ranks)).items())),
        "rank_counts": dict(sorted(Counter(ranks.values()).items())),
        "initial_count": len(initials),
        "initial_max_rank": max(ranks[w] for w in initials),
        "palindrome_height_bound": 12,
        "edge_count": edges,
        "long_edge_count": sum(map(len, long_graph.values())),
        "all_edges_crosschecked_by_forward_prefix": forward_checks,
        "short_source_count": sum(counts.values()),
        "short_source_width_counts": dict(sorted(counts.items())),
        "short_edges": sorted(short_edges, key=lambda e: (e["source"], e["target"])),
        "layer_counts": all_layers,
        "long_only_layer_counts": long_layers,
        "all_nodes_reached_from_initials": reached == set(ranks),
        "ordinary_integer_sample_count": len(samples),
        "ordinary_integer_width_counts": dict(sorted(sample_widths.items())),
        "ordinary_random_seed": 104620,
        "negative_controls": {"missing_short_predecessor": "rejected", "equal_rank_edge": "rejected",
                              "omitted_short_initial": "rejected", "incorrect_bound_10": "rejected"},
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ["status", "node_count", "initial_count", "edge_count", "palindrome_height_bound", "elapsed_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
