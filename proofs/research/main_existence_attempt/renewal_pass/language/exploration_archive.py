"""Preserve the finite exploratory probes, including every negative outcome.

This recreates the earlier inline probes in a durable, bounded artifact and
adds a six-level check of the other safe inverse branches above Q_r. No
finite-horizon UNKNOWN is called a Lychrel number.
"""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
SOURCE = PROJECT/'main_existence_attempt/return_pass/language'
OLD = PROJECT/'main_existence_attempt/correlation_pass/language'
sys.path.insert(0, str(SOURCE))
sys.path.insert(0, str(OLD))
from image_ancestry import predecessors
from residual_kernel import bad, canonical, realize, numeric_word
from correlated_cegar import Stored, Extension


def encoded(word):
    p, c = word
    return dict(pairs=p, center=c)


def sorted_words(words):
    return sorted(words, key=lambda w: (len(w[0]), w[0], -1 if w[1] is None else w[1]))


def run():
    start = time.monotonic()
    nfa = json.loads((SOURCE/'safe_image2_nfa.json').read_text())
    transitions = [dict(row) for row in nfa['transitions']]
    observer_data = json.loads((SOURCE/'observation_depth4.json').read_text())
    machines = [Stored(observer_data)]
    for _ in range(6):
        machines.append(Extension(machines[-1]))

    def config(word):
        current = set(nfa['initial'])
        for q in word[0]:
            current = {v for u in current for v in transitions[u].get(q, ())}
        return tuple(sorted(current))

    def member(word):
        center = 0 if word[1] is None else word[1]//2+1
        return any(nfa['terminal_masks'][q] & (1 << center) for q in config(word))

    def observation(p, depth):
        state = 0
        for q in p:
            state = machines[depth-4].step(state, q)
        return state

    def orbit(word, horizon):
        if not canonical(*word):
            return dict(first_hit=None, status='NONCANONICAL', horizon=horizon, orbit=[])
        n = realize(*word)
        values = [str(n)]
        hit = None
        for index in range(1, horizon+1):
            n += int(str(n)[::-1])
            values.append(str(n))
            if str(n) == str(n)[::-1]:
                hit = index
                break
        return dict(first_hit=hit, status='FIRST_HIT' if hit is not None else 'UNKNOWN_HORIZON',
                    horizon=horizon, orbit=values)

    gates = []
    for outer in range(1, 5):
        for u, v in ((1, 5), (1, 6), (1, 7), (2, 5), (2, 6), (3, 5)):
            for r in (5, 10, 15):
                word = ((outer, outer)+(0,)*(r-1)+(u, u+v), 2*v)
                gates.append(dict(outer=outer, u=u, v=v, r=r, word=encoded(word),
                                  safe_two_member=member(word), full_subset=config(word),
                                  **orbit(word, 60)))

    targets = [dict(word=((18, 17, 17), 14), depth=4, first_hit=10),
               dict(word=((3, 6, 4, 6, 12, 12), None), depth=10, first_hit=13)]
    insertions = []
    insertion_families = []
    for target_index, target in enumerate(targets):
        p, c = target['word']
        cfg = config(target['word'])
        d4 = observation(p, 4)
        deep = observation(p, target['depth'])
        for position in range(len(p)+1):
            for q in range(19):
                ids = []
                for r in range(1, 13):
                    word = (p[:position]+(q,)*r+p[position:], c)
                    equal_subset = config(word) == cfg
                    equal4 = observation(word[0], 4) == d4
                    equal_full = equal_subset and equal4 and observation(word[0], target['depth']) == deep
                    record = dict(target=target_index, position=position, symbol=q, repeats=r,
                                  word=encoded(word), equal_full_subset=equal_subset,
                                  equal_D4=equal4, equal_complete_class=equal_full, **orbit(word, 20))
                    ids.append(len(insertions))
                    insertions.append(record)
                if all(insertions[i]['equal_complete_class'] and
                       insertions[i]['first_hit'] == target['first_hit'] for i in ids[3:]):
                    insertion_families.append(dict(target=target_index, position=position, symbol=q,
                                                   tested_repeat_interval=[4, 12]))

    inverse_selected = []
    for r in range(5, 13):
        A = ((2, 12, 4, 4)+(9,)*(r-5)+(14, 16, 16, 15), None)
        preds, operations = predecessors(A, all_paths=True)
        pred_rows = []
        for parent in preds:
            older, older_operations = predecessors(parent, all_paths=True)
            pred_rows.append(dict(word=encoded(parent), canonical_integer=str(realize(*parent)),
                                  predecessors=[encoded(w) for w in older], operations=older_operations))
        inverse_selected.append(dict(r=r, target=encoded(A), predecessors=pred_rows, operations=operations))

    local_inverse = []
    for r in range(5, 9):
        Q = ((1, 1)+(0,)*(r-1)+(1, 7), 12)
        C = ((10,)+(9,)*r+(10, 6), None)
        for label, target in (('Q', Q), ('C', C)):
            ps, operations = predecessors(target, all_paths=True)
            local_inverse.append(dict(r=r, family=label, target=encoded(target), operations=operations,
                                      predecessors=[dict(word=encoded(w), full_subset=config(w),
                                                         safe_two_member=member(w), bad=bad(*w)) for w in ps]))

    all_branches = []
    for r in range(5, 9):
        root = ((1, 1)+(0,)*(r-1)+(1, 7), 12)
        layer = {root}
        layers = []
        for depth in range(1, 7):
            next_layer = set()
            edges = []
            rejected = []
            for target in sorted_words(layer):
                ps, operations = predecessors(target, all_paths=True)
                for parent in ps:
                    row = dict(source=encoded(parent), target=encoded(target))
                    if bad(*parent):
                        rejected.append(row)
                    else:
                        next_layer.add(parent)
                        edges.append(row)
            layers.append(dict(depth=depth, count=len(next_layer),
                               nodes=[encoded(w) for w in sorted_words(next_layer)],
                               edges=edges, rejected_unsafe_edges=rejected))
            layer = next_layer
        all_branches.append(dict(r=r, target=encoded(root), layers=layers))

    result = dict(status='COMPLETE_FINITE_EXPLORATION', seconds=time.monotonic()-start,
                  nfa_sha256=hashlib.sha256((SOURCE/'safe_image2_nfa.json').read_bytes()).hexdigest(),
                  gate_horizon60=gates, insertion_targets=[dict(word=encoded(t['word']), depth=t['depth'],
                                                               first_hit=t['first_hit']) for t in targets],
                  insertion_probes=insertions, insertion_candidates=insertion_families,
                  selected_A_inverse=inverse_selected, Q_and_C_inverse=local_inverse,
                  Q_safe_inverse_trees=all_branches, positive_invariant_found=False)
    with gzip.open(HERE/'exploration_archive.json.gz', 'wt') as stream:
        json.dump(result, stream, separators=(',', ':'))
    summary = dict(status=result['status'], seconds=result['seconds'],
                   gate_cases=len(gates), gate_first_hits=sum(x['first_hit'] is not None for x in gates),
                   gate_unknown=sum(x['first_hit'] is None for x in gates),
                   single_symbol_insertion_probes=len(insertions), insertion_candidates=insertion_families,
                   selected_A_counts=[dict(r=x['r'], predecessors=len(x['predecessors']),
                                           second_predecessors=sum(len(y['predecessors']) for y in x['predecessors']))
                                      for x in inverse_selected],
                   all_Q_safe_inverse_counts=[dict(r=x['r'], counts=[y['count'] for y in x['layers']])
                                              for x in all_branches],
                   every_substantive_probe_retained=True, positive_invariant_found=False)
    (HERE/'exploration_archive_summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    run()
