"""Independent arithmetic, full-subset, and complete inverse-graph replay.

Imports neither the archived search nor an existing transducer. The finite
observer check reconstructs raw residuals from emitted prefixes. All 72
gate cases and 2,508 insertion records, including UNKNOWN, are retained.
"""
from functools import lru_cache
from pathlib import Path
import gzip
import hashlib
import itertools
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[2]/'main_existence_attempt/return_pass/language'


def decode(row):
    return tuple(row['pairs']), row['center']


def encode(word):
    return dict(pairs=word[0], center=word[1])


def reverse(n):
    out = 0
    while n:
        out = out*10+n % 10
        n //= 10
    return out


def integer(word):
    p, c = word
    assert p and p[0] > 0 and all(0 <= q <= 18 for q in p)
    assert c is None or c in range(0, 19, 2)
    digits = [max(0, q-9) for q in p]
    if c is not None:
        digits.append(c//2)
    digits.extend(min(9, q) for q in reversed(p))
    return sum(d*10**i for i, d in enumerate(digits))


def folded(n):
    digits = tuple(map(int, str(n)))
    return tuple(digits[i]+digits[-i-1] for i in range(len(digits)//2)), (
        2*digits[len(digits)//2] if len(digits) % 2 else None)


def arithmetic_safe(word):
    n = integer(word)
    n += reverse(n)
    return n != reverse(n)


def local_edges(state, q):
    h, a, b, t, started = state
    if not started and q == 0:
        return
    for inner_high in range(2):
        high_digit = q+inner_high-10*b
        if high_digit < 0 or high_digit > 9:
            continue
        outgoing = int(q+a >= 10)
        low_digit = q+a-10*outgoing
        yield (h, outgoing, inner_high, high_digit if h else -1, True), low_digit+(t if h else high_digit)


@lru_cache(maxsize=None)
def inverse(target):
    target_pairs, target_center = target
    states = {(0, 0, 0, -1, False, ()), (1, 0, 1, 1, False, ())}
    answers = set()
    for k in range(len(target_pairs)+1):
        for h, a, b, t, started, prefix in states:
            for center in (None,)+tuple(range(0, 19, 2)):
                if not started and center in (None, 0):
                    continue
                if center is None:
                    if a != b:
                        continue
                    extra, emitted_center = None, 2*t if h else None
                else:
                    digit = center+a-10*b
                    if not 0 <= digit <= 9:
                        continue
                    extra, emitted_center = (digit+t, None) if h else (None, 2*digit)
                if emitted_center != target_center:
                    continue
                if (extra is None and k == len(target_pairs)) or (
                        extra is not None and k+1 == len(target_pairs) and extra == target_pairs[k]):
                    word = prefix, center
                    n = integer(word)
                    assert folded(n+reverse(n)) == target
                    answers.add(word)
        if k == len(target_pairs):
            break
        following = set()
        for h, a, b, t, started, prefix in states:
            for q in range(19):
                for state, output in local_edges((h, a, b, t, started), q):
                    if output == target_pairs[k]:
                        following.add(state+(prefix+(q,),))
        states = following
    return frozenset(answers)


def main():
    path = HERE/'exploration_archive.json.gz'
    with gzip.open(path, 'rt') as stream:
        data = json.load(stream)
    nfa_path = SOURCE/'safe_image2_nfa.json'
    assert hashlib.sha256(nfa_path.read_bytes()).hexdigest() == data['nfa_sha256']
    nfa = json.loads(nfa_path.read_text())
    transition = [dict(row) for row in nfa['transitions']]
    d4 = json.loads((SOURCE/'observation_depth4.json').read_text())
    d0 = json.loads((SOURCE/'observation_depth0.json').read_text())

    @lru_cache(maxsize=None)
    def subset(p):
        states = set(nfa['initial'])
        for q in p:
            states = set().union(*(transition[s].get(q, ()) for s in states))
        return sorted(states)

    def member(word):
        c = 0 if word[1] is None else word[1]//2+1
        return any(nfa['terminal_masks'][u] >> c & 1 for u in subset(word[0]))

    def table_state(table, p):
        state = 0
        for q in p:
            state = table['delta'][state][q]
        return state

    @lru_cache(maxsize=None)
    def signature(depth, p):
        if depth == 4:
            return table_state(d4, p)
        states = {(0, 0, 0, -1, False, ()), (1, 0, 1, 1, False, ())}
        for q in p:
            following = set()
            for h, a, b, t, started, emitted in states:
                for next_state, value in local_edges((h, a, b, t, started), q):
                    following.add(next_state+(emitted+(value,),))
            states = following
        return table_state(d0, p), frozenset(
            ((h, a, b, t, started), signature(depth-1, emitted))
            for h, a, b, t, started, emitted in states)

    integer_steps = noncanonical = 0

    def check_orbit(row):
        nonlocal integer_steps, noncanonical
        word = decode(row['word'])
        if row['status'] == 'NONCANONICAL':
            assert word[0][0] == 0 and row['orbit'] == [] and row['first_hit'] is None
            noncanonical += 1
            return
        n = integer(word)
        assert row['orbit'][0] == str(n)
        hit = None
        for index, value in enumerate(row['orbit'][1:], 1):
            n += reverse(n)
            integer_steps += 1
            assert str(n) == value
            if n == reverse(n):
                assert index == len(row['orbit'])-1
                hit = index
        assert hit == row['first_hit']
        assert (row['status'] == 'FIRST_HIT') == (hit is not None)
        assert len(row['orbit'])-1 == (hit if hit is not None else row['horizon'])

    gates = data['gate_horizon60']
    assert len(gates) == 4*6*3
    gate_keys = set()
    for row in gates:
        gate_keys.add((row['outer'], row['u'], row['v'], row['r']))
        check_orbit(row)
        word = decode(row['word'])
        assert word == ((row['outer'],)*2+(0,)*(row['r']-1)+(row['u'], row['u']+row['v']), 2*row['v'])
        assert subset(word[0]) == row['full_subset']
        assert member(word) == row['safe_two_member']
    assert len(gate_keys) == 72

    insertions = data['insertion_probes']
    assert len(insertions) == (4+7)*19*12
    grouped = {}
    for row in insertions:
        check_orbit(row)
        target = data['insertion_targets'][row['target']]
        p, c = decode(target['word'])
        position, q, count = row['position'], row['symbol'], row['repeats']
        word = decode(row['word'])
        assert word == (p[:position]+(q,)*count+p[position:], c)
        eq_subset = subset(word[0]) == subset(p)
        eq4 = table_state(d4, word[0]) == table_state(d4, p)
        assert eq_subset == row['equal_full_subset'] and eq4 == row['equal_D4']
        eq_full = eq_subset and eq4 and signature(target['depth'], word[0]) == signature(target['depth'], p)
        assert eq_full == row['equal_complete_class']
        grouped.setdefault((row['target'], position, q), []).append(row)
    candidates = []
    for (target, position, q), rows in grouped.items():
        rows.sort(key=lambda r: r['repeats'])
        assert [r['repeats'] for r in rows] == list(range(1, 13))
        if all(row['equal_complete_class'] and row['first_hit'] == data['insertion_targets'][target]['first_hit']
               for row in rows[3:]):
            candidates.append(dict(target=target, position=position, symbol=q, tested_repeat_interval=[4, 12]))
    assert candidates == data['insertion_candidates'] == []
    assert noncanonical == 2*12

    # Independently complete the earlier unary-prefix pump catalog too.
    with gzip.open(HERE/'pump_search_result.json.gz', 'rt') as stream:
        pump = json.load(stream)
    assert pump['status'] == 'NO_PUMP_IN_FINITE_CATALOG'
    assert len(pump['unary_prefix_records']) == 18*19
    suffixes = [()] + [(q,) for q in range(19)] + list(itertools.product(range(19), repeat=2))
    suffixes += [tuple(target['pairs'][-3:]) for target in pump['targets']]
    pump_matches = []
    seen_catalog = set()
    for record in pump['unary_prefix_records']:
        a, q = record['a'], record['q']
        assert 1 <= a <= 18 and 0 <= q <= 18 and (a, q) not in seen_catalog
        seen_catalog.add((a, q))
        previous = {}
        cycle = None
        for repeats in range(pump['max_prefix']+1):
            p = (a,)+(q,)*repeats
            key = tuple(subset(p)), table_state(d4, p)
            if key in previous:
                cycle = [previous[key], repeats-previous[key]]
                break
            previous[key] = repeats
        assert cycle == record['cycle'] and len(previous) == record['seen']
        if cycle is None or not subset(p):
            continue
        base, period = cycle
        prefix = (a,)+(q,)*base
        for suffix in suffixes:
            word_prefix = prefix+suffix
            for target in pump['targets']:
                target_prefix = tuple(target['pairs'])
                if subset(word_prefix) != subset(target_prefix):
                    continue
                if table_state(d4, word_prefix) != table_state(d4, target_prefix):
                    continue
                if signature(target['depth'], word_prefix) != signature(target['depth'], target_prefix):
                    continue
                n = integer((word_prefix, target['center']))
                hit = None
                for step in range(1, pump['max_hit']+1):
                    n += reverse(n)
                    if n == reverse(n):
                        hit = step
                        break
                pump_matches.append(dict(a=a, q=q, base=base, period=period,
                                         suffix=list(suffix), target_depth=target['depth'], first_hit=hit))
    assert pump_matches == pump['terminating_probes']
    assert all(record['first_hit'] is None for record in pump_matches)
    assert pump['certificates'] == []

    selected_counts = []
    for row in data['selected_A_inverse']:
        actual = inverse(decode(row['target']))
        assert actual == frozenset(decode(x['word']) for x in row['predecessors'])
        for parent in row['predecessors']:
            word = decode(parent['word'])
            assert str(integer(word)) == parent['canonical_integer']
            assert inverse(word) == frozenset(decode(w) for w in parent['predecessors']) == frozenset()
        selected_counts.append(dict(r=row['r'], predecessors=len(actual), second_predecessors=0))

    for row in data['Q_and_C_inverse']:
        assert inverse(decode(row['target'])) == frozenset(decode(x['word']) for x in row['predecessors'])
        for parent in row['predecessors']:
            word = decode(parent['word'])
            assert subset(word[0]) == parent['full_subset']
            assert member(word) == parent['safe_two_member']
            assert (not arithmetic_safe(word)) == parent['bad']

    all_counts = []
    inverse_edges = 0
    for tree in data['Q_safe_inverse_trees']:
        layer = {decode(tree['target'])}
        counts = []
        for index, record in enumerate(tree['layers'], 1):
            assert record['depth'] == index
            expected_edges = {(parent, target) for target in layer for parent in inverse(target)
                              if arithmetic_safe(parent)}
            rejected = {(parent, target) for target in layer for parent in inverse(target)
                        if not arithmetic_safe(parent)}
            assert expected_edges == {(decode(row['source']), decode(row['target'])) for row in record['edges']}
            assert rejected == {(decode(row['source']), decode(row['target'])) for row in record['rejected_unsafe_edges']}
            layer = {source for source, target in expected_edges}
            assert layer == {decode(row) for row in record['nodes']}
            assert len(layer) == record['count']
            counts.append(len(layer))
            inverse_edges += len(expected_edges)
        all_counts.append(dict(r=tree['r'], counts=counts))

    tree = data['Q_safe_inverse_trees'][0]
    layer3 = tree['layers'][2]
    start = next(decode(word) for word in layer3['nodes'] if decode(word)[0][:3] != (2, 12, 4))
    n = integer(start)
    witness_orbit = [str(n)]
    witness_words = [encode(folded(n))]
    for index in range(1, 15):
        n += reverse(n)
        assert (n == reverse(n)) == (index == 14)
        witness_orbit.append(str(n))
        if index <= 3:
            witness_words.append(encode(folded(n)))
    assert decode(witness_words[3]) == decode(tree['target'])
    witness = dict(r=tree['r'], ancestor_depth=3, first_hit=14,
                   words_through_Q=witness_words, ordinary_orbit=witness_orbit)
    (HERE/'outside_A_cylinder_witness.json').write_text(json.dumps(witness, indent=2)+'\n')
    result = dict(status='INDEPENDENT_FINITE_ARCHIVE_REPLAY_PASS',
                  archive_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  checked_gate_cases=len(gates), gate_first_hits=sum(r['first_hit'] is not None for r in gates),
                  gate_unknown=sum(r['first_hit'] is None for r in gates),
                  checked_insertion_records=len(insertions), noncanonical_insertion_records=noncanonical,
                  insertion_candidates=0, ordinary_orbit_steps=integer_steps,
                  unary_prefix_catalog=len(seen_catalog), unary_prefix_class_matches=len(pump_matches),
                  unary_prefix_pump_certificates=0,
                  selected_A_counts=selected_counts, all_Q_safe_inverse_counts=all_counts,
                  safe_inverse_edges=inverse_edges, exact_inverse_targets=inverse.cache_info().currsize,
                  recursive_observer_signatures=signature.cache_info().currsize,
                  outside_A_witness_seed=witness_orbit[0],
                  outside_A_witness_prefix=start[0][:3],
                  outside_A_witness_first_hit=14, positive_invariant_found=False)
    (HERE/'exploration_archive_audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
