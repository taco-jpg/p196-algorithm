#!/usr/bin/env python3
"""Reconstruct five finite rank certificates from column equations; write beside this script."""
from collections import defaultdict, deque
from itertools import product
from pathlib import Path
import json
from verify_certificates import raw_words, F, prefix_predecessors

WIDTH = 7
DIRECTORY = Path(__file__).resolve().parent
SHORT = defaultdict(set)
for n in range(1, WIDTH):
    for s in raw_words(n):
        SHORT[F(s)].add(s)


def generate(prefix):
    head = tuple(map(int, prefix))
    initial = {head + tail for tail in product(range(10), repeat=WIDTH - 3)}
    for n in range(3, WIDTH):
        for half in product(range(10), repeat=(n + 1) // 2):
            p = half + half[:n // 2][::-1]
            if p[:3] == head and (n % 2 == 0 or p[n // 2] % 2 == 0):
                initial.add(p)
    todo, seen = list(initial), set(initial)
    parents, children = {}, defaultdict(list)
    while todo:
        p = todo.pop()
        ps = set(SHORT[p])
        if len(p) == WIDTH:
            ps |= prefix_predecessors(p)
        parents[p] = ps
        for s in ps:
            children[s].append(p)
            if s not in seen:
                seen.add(s)
                todo.append(s)
        if len(seen) > 2_000_000:
            raise RuntimeError('Resource limit: no certificate was generated; this is not an exclusion result')
    rank = {p: 0 for p in seen if not parents[p]}
    degree = {p: len(parents[p]) for p in seen}
    queue = deque(rank)
    while queue:
        s = queue.popleft()
        for p in children[s]:
            degree[p] -= 1
            if degree[p] == 0:
                rank[p] = 1 + max(rank[q] for q in parents[p])
                queue.append(p)
    if len(rank) != len(seen):
        raise RuntimeError('Uneliminated states remain: this does not establish a finite-depth theorem')

    def counts(long_only=False):
        layer = {p for p in initial if not long_only or len(p) == WIDTH}
        values = []
        while layer:
            values.append(len(layer))
            layer = {q for p in layer for q in parents[p]
                     if not long_only or len(q) == WIDTH}
        return values + [0]

    cert = {'schema': 1, 'width': WIDTH, 'prefix': prefix,
            'initial': [list(p) for p in sorted(initial)],
            'nodes': [{'word': list(p), 'rank': rank[p]} for p in sorted(seen)],
            'layer_counts': counts(), 'long_only_layer_counts': counts(True),
            'palindrome_height_bound': 1 + max(rank[p] for p in initial)}
    path = DIRECTORY / ('certificate_' + prefix + '.json')
    path.write_text(json.dumps(cert, separators=(',', ':')) + '\n')
    print(prefix, 'states', len(seen), 'upper bound', cert['palindrome_height_bound'])


if __name__ == '__main__':
    for prefix in ('217', '218', '620', '739', '777'):
        generate(prefix)
