#!/usr/bin/env python3
"""Exact cyclic-core hierarchy for saturated decimal prefix extensions.

Every cyclic (k+1)-prefix projects to a cyclic k-prefix. Extend only the
already retained cyclic k-prefixes by one free coefficient 0..18; still
allow either incoming high carry. This discards no possible prefix cycle.
CAP/TIME_LIMIT labels are incomplete calculations, never exclusions.

    python3 calculation/agent-106/prefix_hierarchy.py
"""

import argparse
from collections import Counter
from time import monotonic

from prefix_extension import advance, component_period, crosscheck, skeleton, strongly_connected


def retained_graph(states):
    profile = skeleton()
    phase_of = {word: phase for phase, word in enumerate(profile)}
    candidates = [word + (coefficient,) for word in states for coefficient in range(19)]
    index = {word: i for i, word in enumerate(candidates)}
    adjacency = [[] for _ in candidates]
    reverse = [[] for _ in candidates]
    for source, word in enumerate(candidates):
        for inward in (0, 1):
            out, overflow = advance(word, inward)
            target = index.get(out)
            if target is not None and target not in adjacency[source]:
                phase = phase_of[word[:3]]
                assert out[:3] == profile[(phase + 1) % 8]
                assert overflow == phase % 2
                adjacency[source].append(target)
                reverse[target].append(source)
    return candidates, adjacency, reverse


def period8_roots(candidates, adjacency, membership, cyclic):
    phase0 = skeleton()[0]
    roots = [vertex for _, members in cyclic for vertex in members
             if candidates[vertex][:3] == phase0]
    count = 0
    witness = None
    for root in roots:
        region = membership[root]
        frontier = {root}
        parents = []
        for _ in range(8):
            previous = {}
            for source in frontier:
                for target in adjacency[source]:
                    if membership[target] == region:
                        previous.setdefault(target, source)
            parents.append(previous)
            frontier = set(previous)
        if root in frontier:
            count += 1
            if witness is None:
                path = [root]
                for previous in reversed(parents):
                    path.append(previous[path[-1]])
                path.reverse()
                assert path[0] == path[-1] == root
                witness = [candidates[vertex] for vertex in path[:-1]]
    return count, witness


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-width", type=int, default=20)
    parser.add_argument("--candidate-cap", type=int, default=500000)
    parser.add_argument("--seconds", type=float, default=55)
    parser.add_argument("--witness", action="store_true")
    args = parser.parse_args()
    assert 4 <= args.max_width <= 40
    assert 152 <= args.candidate_cap <= 500000
    assert 0 < args.seconds <= 60
    print("bigint_crosschecks=" + str(crosscheck()), flush=True)
    states = skeleton()
    started = monotonic()
    for width in range(4, args.max_width + 1):
        wanted = len(states) * 19
        if wanted > args.candidate_cap:
            print(f"CAPPED width={width} candidate_vertices={wanted} cap={args.candidate_cap} "
                  "status=UNDECIDED", flush=True)
            return
        if monotonic() - started >= args.seconds:
            print(f"TIME_LIMIT width={width} status=UNDECIDED", flush=True)
            return
        t0 = monotonic()
        candidates, adjacency, reverse = retained_graph(states)
        membership, components = strongly_connected(adjacency, reverse)
        cyclic = [(index, members) for index, members in enumerate(components)
                  if len(members) > 1 or members[0] in adjacency[members[0]]]
        periods = Counter(component_period(members, index, membership, adjacency)
                          for index, members in cyclic)
        sizes = Counter(len(members) for _, members in cyclic)
        p8_count, p8_witness = period8_roots(candidates, adjacency, membership, cyclic)
        states = [candidates[vertex] for _, members in cyclic for vertex in members]
        print(f"width={width} candidates={len(candidates)} edges={sum(map(len, adjacency))} "
              f"cyclic_vertices={len(states)} cyclic_sccs={len(cyclic)} "
              f"period_gcd_histogram={dict(sorted(periods.items()))} "
              f"scc_size_histogram={dict(sorted(sizes.items()))} "
              f"period8_phase0_roots={p8_count} sec={monotonic()-t0:.3f}", flush=True)
        if args.witness and p8_witness:
            inputs = []
            for i, word in enumerate(p8_witness):
                target = p8_witness[(i + 1) % 8]
                choices = [inward for inward in (0, 1)
                           if advance(word, inward) == (target, i % 2)]
                assert choices
                inputs.append(choices[0])
            print(f"width={width} period8_witness={p8_witness} high_inputs={inputs}", flush=True)
        if not states:
            print(f"ACYCLIC_PREFIX width={width} status=COMPUTED", flush=True)
            return


if __name__ == "__main__":
    main()
