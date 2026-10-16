"""Exact all-length DFA synthesis for the canonical decimal folded map.

The automaton reads pair sums 0..18 and uses 11 end predicates (absent
center, then even centers 0..18). Both final carry choices are included.
SAT means only a proposed certificate, until independently checked.
UNSAT excludes this precise bounded-state template when the encoding and
LRAT proof have both been checked. No seed or clock is prescribed.
"""
from collections import deque
from pathlib import Path
import argparse, hashlib, itertools, json, time

CENTERS = [None] + list(range(0, 19, 2))


class CNF:
    def __init__(self):
        self.ids = {}
        self.clauses = []

    def var(self, *name):
        if name not in self.ids:
            self.ids[name] = len(self.ids) + 1
        return self.ids[name]

    def add(self, *row):
        self.clauses.append(row)

    def one(self, row):
        self.add(*row)
        for a, b in itertools.combinations(row, 2):
            self.add(-a, -b)

    def save(self, path):
        with path.open('w') as f:
            f.write(f'p cnf {len(self.ids)} {len(self.clauses)}\n')
            for row in self.clauses:
                f.write(' '.join(map(str, row)) + ' 0\n')


def transducer():
    # (overflow, low incoming carry, high outgoing carry, retained high
    # digit for shifted overflow alignment, has consumed a pair).
    states = [(0, 0, 0, -1, False), (1, 0, 1, 1, False)]
    ids = {s: i for i, s in enumerate(states)}
    edges, terms = [], []
    for x, (h, a, b, t, started) in enumerate(states):
        for q in range(0 if started else 1, 19):
            for bn in (0, 1):
                if (q + bn) // 10 != b:
                    continue
                an, lo = divmod(q + a, 10)
                hi = (q + bn) % 10
                output = lo + (t if h else hi)
                nxt = (h, an, bn, hi if h else -1, True)
                if nxt not in ids:
                    ids[nxt] = len(states)
                    states.append(nxt)
                edges.append((x, q, output, ids[nxt]))
        for ci, center in enumerate(CENTERS):
            if not started and (center is None or center == 0):
                continue
            if center is None:
                if a != b:
                    continue
                extra, oc = None, 2 * t if h else None
            else:
                if (center + a) // 10 != b:
                    continue
                remainder = (center + a) % 10
                extra = remainder + t if h else None
                oc = None if h else 2 * remainder
            terms.append((x, ci, extra, CENTERS.index(oc)))
    return states, edges, terms


def build(n, terminating_depth=0, symmetry=True):
    f = CNF()
    d = [[[f.var('d', a, q, b) for b in range(n)]
          for q in range(19)] for a in range(n)]
    end = [[f.var('end', a, c) for c in range(11)] for a in range(n)]
    for row in d:
        for col in row:
            f.one(col)
    if symmetry:
        # Name noninitial states by their first target appearance when
        # transitions are read row by row. Reachable states can always be
        # named this way; unreachable states may be completed with loops.
        previous = [[] for b in range(n)]
        for a in range(n):
            for q in list(range(1, 19)) + [0]:
                for b in range(2, n):
                    f.add(-d[a][q][b], *previous[b-1])
                for b in range(n):
                    previous[b].append(d[a][q][b])

    # Universal safety: exact four-state monitor for palindrome predecessors.
    # 0=empty, 1=all <=9, 2=outer 11 and only {0,11}, 3=neither.
    safe = [[f.var('safety', a, m) for m in range(4)] for a in range(n)]
    f.add(safe[0][0])
    for a in range(n):
        for m in range(4):
            for q in range(1 if m == 0 else 0, 19):
                if m == 0:
                    mm = 1 if q <= 9 else 2 if q == 11 else 3
                elif m == 1:
                    mm = 1 if q <= 9 else 3
                elif m == 2:
                    mm = 2 if q in (0, 11) else 3
                else:
                    mm = 3
                for b in range(n):
                    f.add(-safe[a][m], -d[a][q][b], safe[b][mm])
            for c, center in enumerate(CENTERS):
                if m == 0 and (center is None or center == 0):
                    continue
                bad = ((m == 0 and center <= 9)
                       or (m == 1 and (center is None or center <= 9))
                       or (m == 2 and (center is None or center == 0)))
                if bad:
                    f.add(-safe[a][m], -end[a][c])

    states, edges, terms = transducer()
    reach = [[[f.var('closure', x, a, b) for b in range(n)]
              for a in range(n)] for x in range(len(states))]
    f.add(reach[0][0][0])
    f.add(reach[1][0][0])
    for x, q, o, y in edges:
        for a, b, aa, bb in itertools.product(range(n), repeat=4):
            f.add(-reach[x][a][b], -d[a][q][aa], -d[b][o][bb], reach[y][aa][bb])
    for x, ci, extra, co in terms:
        for a, b in itertools.product(range(n), repeat=2):
            if extra is None:
                f.add(-reach[x][a][b], -end[a][ci], end[b][co])
            else:
                for bb in range(n):
                    f.add(-reach[x][a][b], -end[a][ci], -d[b][extra][bb], end[bb][co])

    # A nonempty canonical language has a word with at most n pair symbols.
    # Include one-digit words separately; the main path reads a positive
    # first pair and then n-1 pair-or-padding choices.
    witness = [f.var('witness', j, a) for j in range(n + 1) for a in range(n)]
    w = lambda j, a: witness[j * n + a]
    for a in range(n):
        f.add(w(0, a) if a == 0 else -w(0, a))
    for j in range(n):
        f.one([w(j + 1, a) for a in range(n)])
        letters = range(1, 19) if j == 0 else range(20)
        choices = {q: f.var('letter', j, q) for q in letters}
        f.one(list(choices.values()))
        for q, lit in choices.items():
            for a in range(n):
                if q == 19:
                    f.add(-w(j, a), -lit, w(j + 1, a))
                else:
                    for b in range(n):
                        f.add(-w(j, a), -lit, -d[a][q][b], w(j + 1, b))
    accepting = []
    for a in range(n):
        for c in range(11):
            v = f.var('witness_end', a, c)
            f.add(-v, w(n, a))
            f.add(-v, end[a][c])
            accepting.append(v)
    # Positive even center indices 2..10 are exactly one-digit inputs.
    f.add(*(accepting + end[0][2:]))

    evidence = []
    if terminating_depth:
        # Redundant unconditional exclusions, each certified by its exact
        # ordinary integer trajectory. They improve SAT propagation only.
        prefixes = {(): [int(a == 0) for a in range(n)]}
        def prefix(p):
            if p in prefixes:
                return prefixes[p]
            old = prefix(p[:-1]); q = p[-1]
            row = [f.var('negative_prefix', p, a) for a in range(n)]
            f.one(row)
            for a, b in itertools.product(range(n), repeat=2):
                if len(p) == 1:
                    if a == 0:
                        f.add(-d[a][q][b], row[b])
                else:
                    f.add(-old[a], -d[a][q][b], row[b])
            prefixes[p] = row
            return row
        for pair_count in range(terminating_depth + 1):
            ps = [()] if pair_count == 0 else ((q,) + tail for q in range(1, 19) for tail in itertools.product(range(19), repeat=pair_count-1))
            for p in ps:
                for ci, center in enumerate(CENTERS):
                    if not p and (center is None or center == 0):
                        continue
                    digits = ''.join(str(min(q,9)) for q in p)
                    digits += '' if center is None else str(center//2)
                    digits += ''.join(str(max(q-9,0)) for q in p[::-1])
                    value = int(digits); chain = [value]
                    for t in range(1, 61):
                        value += int(str(value)[::-1]); chain.append(value)
                        s = str(value)
                        if s == s[::-1]:
                            row = prefix(p)
                            if p:
                                for a in range(n):
                                    f.add(-row[a], -end[a][ci])
                            else:
                                f.add(-end[0][ci])
                            evidence.append(dict(pairs=p, center=center, orbit=chain))
                            break
    metadata = dict(states=n, variables=len(f.ids), clauses=len(f.clauses),
                    transducer_states=len(states), transducer_edges=len(edges),
                    transducer_terminals=len(terms), terminating_pair_depth=terminating_depth,
                    certified_terminating_labels=len(evidence), variable_clocks=True,
                    seed=None, exact_all_lengths=True, positive_proof=False)
    metadata['state_name_symmetry'] = symmetry
    return f, metadata, evidence


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--states', type=int, default=4)
    p.add_argument('--terminating-depth', type=int, default=0)
    p.add_argument('--stem', default=None)
    p.add_argument('--no-symmetry', action='store_true')
    args = p.parse_args()
    start = time.monotonic()
    f, meta, evidence = build(args.states, args.terminating_depth, not args.no_symmetry)
    stem = Path(args.stem or f'dfa{args.states}_neg{args.terminating_depth}')
    f.save(stem.with_suffix('.cnf'))
    import gzip
    with gzip.open(str(stem)+'.variables.json.gz', 'wt') as z:
        json.dump(list(f.ids), z, separators=(',', ':'))
    meta.update(build_seconds=time.monotonic()-start,
                cnf_sha256=hashlib.sha256(stem.with_suffix('.cnf').read_bytes()).hexdigest())
    stem.with_suffix('.json').write_text(json.dumps(meta, indent=2)+'\n')
    if evidence:
        with gzip.open(str(stem)+'.terminating.json.gz','wt') as z:
            json.dump(evidence,z,separators=(',',':'))
    print(json.dumps(meta), flush=True)


if __name__ == '__main__':
    main()
