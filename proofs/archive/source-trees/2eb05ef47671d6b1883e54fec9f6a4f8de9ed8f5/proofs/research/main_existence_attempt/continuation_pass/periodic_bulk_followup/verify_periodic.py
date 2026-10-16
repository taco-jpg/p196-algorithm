"""Independent replay of saved periodic graphs and actual-word controls.

Imports no discovery module. Interior equations are reconstructed by finite
two-ended decimal scans; whole-word checks use ordinary integer arithmetic.
Finite controls validate code, not the all-exponent lemma in the proof note.
"""
from collections import Counter, deque
from functools import lru_cache
from pathlib import Path
import gzip
import hashlib
import json
import sys

ROOT = Path(__file__).parent
sys.setrecursionlimit(100000)


def frozen(x):
    return tuple(map(frozen, x)) if isinstance(x, list) else x


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_saved(stem):
    data = gzip.decompress((ROOT / (stem + '.json.gz')).read_bytes())
    return json.loads(data), digest(data)


def scan(q, carry):
    digits = []
    for a in q:
        digits.append((a + carry) % 10)
        carry = int(a + carry >= 10)
    return tuple(digits), carry


@lru_cache(None)
def phase_edges(p):
    # Central period of five copies is insulated from both boundaries.
    q = p * 5
    records = []
    for clock in (0, 1):
        possibilities = []
        for left in (0, 1):
            lo, _ = scan(q, left)
            for right in (0, 1):
                back, _ = scan(q[::-1], right)
                hi = back[::-1]
                target = tuple(lo[i] + hi[i - clock] for i in range(8, 12))
                possibilities.append(target)
                if set(p) == {9}:
                    records.append(dict(clock=clock, left_carry=left,
                                        right_carry=right, target=target))
        if set(p) != {9}:
            assert len(set(possibilities)) == 1
            records.append(dict(clock=clock, target=possibilities[0]))
    return records


def number_image(q):
    # Evaluate the symmetric coefficient polynomial, independently of carries.
    n = 0
    for a in reversed(q):
        n = n * 10 + a
    digits = tuple(map(int, str(n)[::-1]))
    assert len(digits) in (len(q), len(q) + 1)
    return tuple(a + b for a, b in zip(digits, digits[::-1])), len(digits) - len(q), n


@lru_cache(None)
def outer_edges(a):
    # The even center 0/18 realizes each possible incoming carry exactly.
    records = set()
    for center in (0, 18):
        target, clock, _ = number_image((a, center, a))
        records.add((clock, target[0]))
    return sorted(records)


def key(edge):
    return json.dumps(edge, sort_keys=True, separators=(',', ':'))


def components(graph):
    # Recursive Tarjan, independently of the discovery's two-pass traversal.
    ticks = 0
    indices, low, stack, active, result = {}, {}, [], set(), []

    def visit(v):
        nonlocal ticks
        indices[v] = low[v] = ticks
        ticks += 1
        stack.append(v)
        active.add(v)
        for edge in graph[v]:
            w = frozen(edge['target'])
            if w not in indices:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in active:
                low[v] = min(low[v], indices[w])
        if low[v] == indices[v]:
            found = set()
            while True:
                w = stack.pop()
                active.remove(w)
                found.add(w)
                if w == v:
                    break
            result.append(frozenset(found))

    for vertex in graph:
        if vertex not in indices:
            visit(vertex)
    return result


def audit_graph(payload, expected_edges, result):
    graph = {frozen(row['source']): row['edges'] for row in payload['graph']}
    assert len(graph) == len(payload['graph'])
    for vertex, edges in graph.items():
        assert Counter(map(key, edges)) == Counter(map(key, expected_edges(vertex)))
        assert all(frozen(e['target']) in graph for e in edges)
    starts = payload['initial']
    if starts and isinstance(starts[0], int):
        starts = [starts]
    reached = set(map(frozen, starts))
    todo = deque(reached)
    while todo:
        for edge in graph[todo.popleft()]:
            w = frozen(edge['target'])
            if w not in reached:
                reached.add(w)
                todo.append(w)
    assert reached == set(graph)
    comps = components(graph)
    saved = {frozenset(map(frozen, c)) for c in payload['components']}
    assert set(comps) == saved
    n = result.get('reachable_states', result.get('reachable_indexed_phases'))
    assert n == len(graph)
    assert result['edges'] == sum(map(len, graph.values()))
    assert result['strong_components'] == len(comps)
    sizes = {str(k): v for k, v in sorted(Counter(map(len, comps)).items())}
    assert result['component_size_distribution'] == sizes
    return graph, comps


def check_loop(loop, graph):
    assert loop
    for i, e in enumerate(loop):
        source, target = frozen(e['source']), frozen(e['target'])
        assert target == frozen(loop[(i + 1) % len(loop)]['source'])
        matches = [a for a in graph[source]
                   if frozen(a['target']) == target and a['clock'] == e['clock']]
        assert matches
        for attr in ('left_carry', 'right_carry'):
            if attr in e:
                assert any(a.get(attr) == e[attr] for a in matches)


def product_edges(state, width=False):
    p, a = state[:2]
    result = []
    for edge in phase_edges(p):
        for clock, outside in outer_edges(a):
            if clock != edge['clock']:
                continue
            target = (edge['target'], outside)
            if width:
                target += ((state[2] + clock) % 8,)
            result.append(dict(edge, target=target))
    return result


def reflect(p, width):
    return tuple(p[(width - 1 - i) % 4] for i in range(4))


def full(state, exponent):
    b, h, w = state
    return b + w * exponent + h + w[::-1] * exponent + b[::-1]


def canonical(q):
    return bool(q) and q[0] > 0 and q == q[::-1] and all(0 <= x <= 18 for x in q) \
        and (len(q) % 2 == 0 or q[len(q) // 2] % 2 == 0)


def safe(q):
    return not (max(q) <= 9 or (q[0] == 11 and set(q) <= {0, 11}))


def realization(q):
    # A canonical numeral having exactly this mirrored-sum word.
    assert canonical(q)
    digits = [0] * len(q)
    for i in range(len(q) // 2):
        digits[-1 - i] = min(9, q[i])
        digits[i] = q[i] - digits[-1 - i]
    if len(q) % 2:
        digits[len(q) // 2] = q[len(q) // 2] // 2
    n = int(''.join(map(str, digits[::-1])))
    assert pair_word(n) == q
    return n


def pair_word(n):
    d = tuple(map(int, str(n)[::-1]))
    return tuple(a + b for a, b in zip(d, d[::-1]))


def whole_replay(payload, result):
    graph = {frozen(row['state']): row for row in payload['graph']}
    assert len(graph) == len(payload['graph']) == result['graph_states']
    controls = (3, 4, 7, 31)
    total = 0
    for state, row in graph.items():
        b, h, w = state
        assert len(w) == 4 and canonical(full(state, 3)) and safe(full(state, 3))
        q, clock, _ = number_image(full(state, 3))
        cut = len(b) + 4
        rb, rw = q[:cut], q[cut:cut + 4]
        rh = q[cut + 4:len(q) - cut - 4]
        assert len(rh) == len(h) + 8 + clock
        assert q == full((rb, rh, rw), 1)
        outer_count = center_count = 0
        while len(rb) >= 4 and rb[-4:] == rw:
            rb = rb[:-4]
            outer_count += 1
        while len(rh) >= 8 and rh[:4] == rw and rh[-4:] == rw[::-1]:
            rh = rh[4:-4]
            center_count += 1
        target = (rb, rh, rw)
        delta = outer_count + center_count - 2
        assert frozen(row['target']) == target
        assert row['clock'] == clock and row['exponent_delta'] == delta
        assert row['absorbed_outer_periods'] == outer_count
        assert row['absorbed_center_pairs'] == center_count
        assert row['kind'] == ('edge' if safe(full(target, 3)) else 'unsafe_target')
        assert 2 * len(rb) + len(rh) + 8 * delta == 2 * len(b) + len(h) + clock
        for k in controls:
            word = full(state, k)
            actual, actual_clock, number = number_image(word)
            assert canonical(word) and safe(word)
            assert str(number) != str(number)[::-1]
            assert actual_clock == clock and actual == full(target, k + delta)
            total += 1

    expected_initials = [((17,), center, (0, 9, 18, 9))
                         for center in [()] + [(c,) for c in range(0, 19, 2)]]
    assert list(map(frozen, payload['initials'])) == expected_initials
    assert [frozen(p['initial']) for p in payload['paths']] == expected_initials
    assert payload['cycles'] == result['cycles'] == []
    used, trajectories, phases = set(), [], []
    for path in payload['paths']:
        states = list(map(frozen, path['states']))
        assert states[0] == frozen(path['initial'])
        assert len(states) == len(set(states)) == 128
        assert path['status'] == 'UNKNOWN_INTERFACE_OR_PATH_CAP'
        assert all(len(s[0]) + len(s[1]) <= 512 for s in states)
        running = minimum = 0
        for i, state in enumerate(states):
            row = graph[state]
            next_state = states[i + 1] if i + 1 < len(states) else frozen(path['final_state'])
            assert frozen(row['target']) == next_state and row['kind'] == 'edge'
            running += row['exponent_delta']
            minimum = min(minimum, running)
            used.add(state)
        floor = 3 - minimum
        assert path['exponent_floor_for_recorded_path'] == floor
        assert len(path['final_state'][0]) + len(path['final_state'][1]) <= 512
        assert frozen(path['final_state']) not in states
        n = realization(full(states[0], floor))
        assert str(n) != str(n)[::-1]
        numbers = [str(n)]
        k = floor
        phase_changes = []
        for i, state in enumerate(states):
            assert k >= 3 and pair_word(n) == full(state, k)
            phase = state[2]
            if len(set(phase)) == 1 and (not phase_changes or phase_changes[-1][1] != phase[0]):
                phase_changes.append([i, phase[0]])
            n += int(str(n)[::-1])
            assert str(n) != str(n)[::-1]
            k += graph[state]['exponent_delta']
            assert pair_word(n) == full(frozen(graph[state]['target']), k)
            numbers.append(str(n))
        assert k >= 3
        trajectories.append(dict(initial_center=path['initial'][1], initial_exponent=floor,
                                 numbers=numbers, steps=128, outcome='UNKNOWN_PATH_CAP'))
        phases.append(dict(initial_center=path['initial'][1], constant_phase_changes=phase_changes))
    assert used == set(graph)
    assert result['caps'] == dict(graph_states=50000, path_steps=128, total_interface_width=512)
    assert result['transition_counts'] == {'edge': 1408}
    assert result['path_status_counts'] == {'UNKNOWN_INTERFACE_OR_PATH_CAP': 11}
    assert result['maximum_path_steps'] == 128
    assert result['maximum_exponent_floor'] == max(p['initial_exponent'] for p in trajectories) == 23
    assert result['largest_interfaces'] == [max(len(s[i]) for s in graph) for i in (0, 1)] == [65, 85]
    data = json.dumps(dict(trajectories=trajectories, phase_changes=phases),
                      sort_keys=True, separators=(',', ':')).encode()
    (ROOT / 'ordinary_trajectories.json.gz').write_bytes(gzip.compress(data, mtime=0))
    return dict(whole_word_states=len(graph), integer_transition_controls=total,
                controls=list(controls), replayed_ordinary_trajectories=len(trajectories),
                ordinary_additions=128 * len(trajectories), constant_phase_changes=phases,
                trajectories_payload_sha256=digest(data), all_paths_unknown=True)


def main():
    input_names = ['bulk_phases.py', 'outer_filter.py', 'width_phase_filter.py',
                   'periodic_word_quotient.py']
    input_names += [stem + suffix for stem in ('bulk_phase', 'outer_filtered', 'width_phase')
                    for suffix in ('_graph.json.gz', '_results.json')]
    input_names += ['periodic_word_quotient_controls.json.gz', 'periodic_word_quotient_results.json']
    input_hashes = {name: digest((ROOT / name).read_bytes()) for name in input_names}
    bulk, bh = read_saved('bulk_phase_graph')
    br = json.loads((ROOT / 'bulk_phase_results.json').read_text())
    assert bh == br['payload_sha256']
    bg, bc = audit_graph(bulk, phase_edges, br)
    assert len(bg) == 59 and sorted(map(len, bc)) == [1, 1, 1, 56]
    for entry in bulk['overflow_cycle_witnesses']:
        check_loop(entry['loop'], bg)
        assert entry['overflow_count'] == sum(e['clock'] for e in entry['loop'])
    check_loop(bulk['ten_step_nooverflow_cycle'], bg)
    assert len(bulk['ten_step_nooverflow_cycle']) == 10
    assert all(e['clock'] == 0 for e in bulk['ten_step_nooverflow_cycle'])
    failed_loop = br['shortest_recorded_nonconstant_overflow_cycle']['loop']
    check_loop(failed_loop, bg)
    assert ''.join(str(e['clock']) for e in failed_loop) == '1000111'
    rotation_checks = reflection_checks = 0
    for p in bg:
        for e in phase_edges(p):
            for amount in range(4):
                rot = lambda q: q[amount:] + q[:amount]
                assert any(x['clock'] == e['clock'] and x['target'] == rot(e['target'])
                           for x in phase_edges(rot(p)))
                rotation_checks += 1
            for width in range(8):
                right = reflect(p, width)
                want = reflect(e['target'], width + e['clock'])
                candidates = [x for x in phase_edges(right) if x['clock'] == e['clock']]
                if 'left_carry' in e:
                    candidates = [x for x in candidates
                                  if x['left_carry'] == e['right_carry']
                                  and x['right_carry'] == e['left_carry']]
                assert any(x['target'] == want for x in candidates)
                reflection_checks += 1
    outer, oh = read_saved('outer_filtered_graph')
    ort = json.loads((ROOT / 'outer_filtered_results.json').read_text())
    assert oh == ort['payload_sha256']
    og, oc = audit_graph(outer, product_edges, ort)
    for loop in outer['shortest_cycle_candidates']:
        check_loop(loop['loop'], og)
    count = sum(1 for c in oc if any(len(set(v[0])) > 1 for v in c)
                for v in c for e in og[v] if e['clock'] and frozen(e['target']) in c)
    assert count == ort['candidate_nonconstant_overflow_cycles'] == 340
    paths = [(a,) for a in range(1, 19)]
    layers = []
    for _ in range(4):
        paths = [p + (b,) for p in paths for h, b in outer_edges(p[-1]) if h]
        layers.append(paths)
    assert frozen(outer['successive_overflow_paths']) == tuple(map(tuple, layers))
    assert layers[2] == [(18, 9, 10, 1)] and layers[3] == []
    paths = [(a,) for a in range(1, 19)]
    for h in [int(c) for c in '1000111' * 2]:
        paths = [p + (b,) for p in paths for hh, b in outer_edges(p[-1]) if hh == h]
    assert paths == []
    width, wh = read_saved('width_phase_graph')
    wr = json.loads((ROOT / 'width_phase_results.json').read_text())
    assert wh == wr['payload_sha256']
    wg, wc = audit_graph(width, lambda s: product_edges(s, True), wr)
    assert wr['checked_reflection_phase_relations'] == sum(len(phase_edges(s[0])) for s in wg) == 14912
    loop = width['width_compatible_cycle']
    assert loop == wr['representative_cycle']
    check_loop(loop, wg)
    assert len(loop) == 16 and sum(e['clock'] for e in loop) == 8
    assert wr['representative_cycle_length'] == 16 and wr['representative_cycle_overflows'] == 8
    assert wr['representative_cycle_gap_gain_if_interfaces_return'] == 1
    for e in loop:
        p, _, w = frozen(e['source'])
        assert frozen(e['right_phase']) == reflect(p, w)
    # Compare with the existing exact maximal-density three-prefix cycle.
    critical = [(8, 16, 16), (17, 13, 14), (8, 12, 9), (17, 5, 0),
                (8, 13, 5), (17, 6, 11), (8, 14, 8), (17, 8, 17)]
    for i, p in enumerate(critical):
        assert any(number_image(p + (center,) + p[::-1])[0][:3] == critical[(i + 1) % 8]
                   for center in (0, 18))
    compatible = []
    for start in range(8):
        if all(critical[(start + t) % 8][0] == e['source'][1] for t, e in enumerate(loop)):
            compatible.append(start)
    assert compatible == [1, 3, 5, 7]
    whole, qh = read_saved('periodic_word_quotient_controls')
    qr = json.loads((ROOT / 'periodic_word_quotient_results.json').read_text())
    assert qh == qr['payload_sha256']
    report = whole_replay(whole, qr)
    report.update(passed=True, discovery_modules_imported=False,
                  bulk_graph_states=len(bg), outer_product_states=len(og),
                  width_product_states=len(wg), rotation_checks=rotation_checks,
                  reflection_checks=reflection_checks,
                  rejected_bulk_clock='1000111 repeated',
                  compatible_existing_three_prefix_cycle_offsets=compatible,
                  input_sha256=input_hashes,
                  scope='Finite graphs and integer controls verified; no finite interface cycle or infinite orbit proved')
    assert input_hashes == {name: digest((ROOT / name).read_bytes()) for name in input_names}
    (ROOT / 'periodic_verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
