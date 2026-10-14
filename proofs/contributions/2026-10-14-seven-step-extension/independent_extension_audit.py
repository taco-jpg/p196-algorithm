#!/usr/bin/env python3
"""Independent literal-integer audit of the necessary extension graphs.

Does not import extension_graph.py.  Every labeled local edge is checked
using a genuine symmetric whole coefficient word and integer arithmetic.
Graph reachability and ranks are recomputed without the producer's SCC code.
"""

from hashlib import sha256
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent


def digits(n):
    out = []
    while n:
        n, d = divmod(n, 10)
        out.append(d)
    return out


def literal_edge(prefix, a, deeper):
    # The even center 0 or 18 forces the specified outgoing carry,
    # independently of the carry entering that center column.
    q = list(prefix) + [a, 18 * deeper, a] + list(reversed(prefix))
    n = sum(v * 10**i for i, v in enumerate(q))
    d = digits(n)
    out = [u + v for u, v in zip(d, reversed(d))]
    high_a_index = len(prefix) + 2
    incoming = sum(v * 10**i for i, v in enumerate(q[:high_a_index])) // 10**high_a_index
    assert incoming == deeper
    after_a = sum(v * 10**i for i, v in enumerate(q[:high_a_index + 1])) // 10**(high_a_index + 1)
    return out[:len(prefix) + 1], len(d) - len(q), after_a, q, d


def closure_components(graph):
    reach = [set(v) for v in graph]
    changed = True
    while changed:
        changed = False
        for v in range(19):
            extended = reach[v].union(*(reach[w] for w in list(reach[v])))
            if extended != reach[v]:
                reach[v] = extended
                changed = True
    groups, unused = [], set(range(19))
    while unused:
        v = min(unused)
        group = sorted(w for w in unused if w == v or (w in reach[v] and v in reach[w]))
        groups.append(group)
        unused.difference_update(group)
    cyclic = [g for g in groups if g[0] in reach[g[0]]]
    return groups, cyclic


def main():
    input_path = HERE / 'extension_graph.json'
    source_path = HERE / 'extension_graph.py'
    data = json.loads(input_path.read_text())
    reports, controls = [], []
    for record in data['records']:
        prefixes = record['prefixes']
        phases = []
        for t, prefix in enumerate(prefixes):
            target = prefixes[(t + 1) % 7]
            edges = [[] for _ in range(19)]
            for a in range(19):
                for deeper in (0, 1):
                    nxt, overflow, carry, q, d = literal_edge(prefix, a, deeper)
                    valid = nxt[:-1] == target and overflow == record['overflow_clock'][t]
                    controls.append(dict(label=record['label'], phase=t,
                                         coefficient=a, deeper=deeper,
                                         pair_word=q, normalized_digits=d,
                                         next_prefix=nxt, overflow=overflow,
                                         accepted=valid))
                    if valid:
                        edges[a].append(dict(deeper=deeper, carry=carry, next=nxt[-1]))
            assert edges == record['phase_edges'][t], (record['label'], t)
            phases.append(edges)
        macro, loops = [], {}
        for start in range(19):
            paths = {(start,)}
            for edges in phases:
                paths = {p + (edge['next'],) for p in paths for edge in edges[p[-1]]}
            macro.append(sorted({p[-1] for p in paths}))
            closed = sorted([list(p[:-1]) for p in paths if p[-1] == start])
            if closed:
                loops[str(start)] = closed
        assert macro == record['macro_edges']
        assert loops == record['closed_one_period_paths']
        groups, cyclic = closure_components(macro)
        assert groups == record['sccs']
        assert cyclic == record['cyclic_sccs']
        ranks = {}
        for bound in range(19):
            newly_dead = [v for v in range(19) if v not in ranks
                          and all(w in ranks for w in macro[v])]
            if not newly_dead:
                break
            for v in newly_dead:
                ranks[v] = bound
        assert {str(v): ranks[v] for v in sorted(ranks)} == record['sink_deletion_ranks']
        reports.append(dict(label=record['label'],
                            literal_phase_controls=7 * 19 * 2,
                            nonempty_macro_edges={str(i): x for i, x in enumerate(macro) if x},
                            cyclic_sccs=cyclic, closed_paths=loops,
                            maximum_deletion_rank=max(ranks.values(), default=None)))
    result = dict(status='PASS',
                  checked_input_sha256=sha256(input_path.read_bytes()).hexdigest(),
                  producer_source_sha256=sha256(source_path.read_bytes()).hexdigest(),
                  literal_phase_controls=len(controls), records=reports,
                  raw_controls=controls,
                  scope='Local edge realization and graph audit only; independent carries at successive times are not asserted realizable.')
    output = HERE / 'independent_extension_audit.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('raw_controls', 'records')}))


if __name__ == '__main__':
    main()
