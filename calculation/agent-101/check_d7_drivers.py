#!/usr/bin/env python3
"""Independent replay and joint-label checks for the D7 driver catalog.

The established check_prefix_sink integer oracle is credited and reused.
Driver periods describe aligned (e,g) labels; literal C/prefix walks retain
their own seams and are never shortened merely because those labels repeat.
No positive projection is a finite exterior or a cycleOK certificate.

  python3 calculation/agent-101/check_d7_drivers.py --selftest
  python3 calculation/agent-101/check_d7_drivers.py --catalog FILE.jsonl
  python3 calculation/agent-101/check_d7_drivers.py --engine /tmp/a101_d7_catalog

--engine adds independent Tarjan fixtures and the complete R1,D5 product.
The latter uses scipy.sparse.csgraph; other checks use the standard library.
Every check survives -O. UNDECIDED producer output is retained, not a negative.
"""
import argparse
import copy
import itertools
import json
import random
import subprocess
import sys
from collections import Counter, deque
from pathlib import Path

import check_prefix_sink as integer_oracle


class CheckFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


KNOWN = {
    'Agent101_P24': {
        'e': '010100110100101011001011', 'g': '110001001000110001001000',
        'v': '100001000000100001000000', 'C0': [9, 14, 13, 18, 13, 14, 9]},
    'Agent6_P42': {
        'e': '010100010111000101010101011101000111010101',
        'g': '101000101001001010100101000101001001010100',
        'v': '000000010000200000010000000010000200000010',
        'C0': [18, 13, 13, 18]},
}


def least_period(sequence):
    require(len(sequence) > 0, 'An empty word has no positive period here')
    for d in range(1, len(sequence)+1):
        if len(sequence) % d == 0 and all(x == sequence[i % d]
                                         for i, x in enumerate(sequence)):
            return d
    raise CheckFailure('Period search failed')


def driver_key(e, g, primitive=False):
    """Return (key, rotation, length); rotate aligned pairs together."""
    require(type(e) is str and type(g) is str and e and len(e) == len(g)
            and set(e+g) <= {'0', '1'}, 'Invalid binary driver')
    symbols = tuple(2*int(a)+int(b) for a, b in zip(e, g))
    length = least_period(symbols) if primitive else len(symbols)
    word = symbols[:length]
    rotation = min(range(length), key=lambda r: word[r:]+word[:r])
    canonical = word[rotation:]+word[:rotation]
    return str(length)+':'+''.join(map(str, canonical)), rotation, length


def known_family(e, g):
    key = driver_key(e, g, True)[0]
    return next((name for name, item in KNOWN.items()
                 if driver_key(item['e'], item['g'], True)[0] == key), None)


def coefficient_word(word, prefix=False, bound=None):
    require(isinstance(word, (list, tuple)) and word
            and all(type(x) is int and 0 <= x <= 18 for x in word),
            'Coefficient word lies outside the decimal domain')
    if prefix:
        require(word[0] > 0, 'An exterior prefix needs a positive head')
    else:
        require(integer_oracle.admissible(tuple(word), True),
                'Center is asymmetric, neutral, or has an odd odd-width middle')
        require(bound is None or len(word) <= bound, 'Center exceeds its cap')


def validate_driver(row, *, prefix_width=3, center_bound=7, max_period=64):
    """Validate one DRIVER without rotating or modifying its literal edges."""
    require(isinstance(row, dict) and row.get('type') == 'DRIVER', 'Expected DRIVER record')
    edges = row.get('edges')
    require(isinstance(edges, list) and 1 <= len(edges) <= max_period,
            'Missing witness or unsupported literal period')
    require(row.get('certificate') is False, 'Projection must be labelled certificate:false')
    for edge in edges:
        require(isinstance(edge, dict), 'An edge must be an object')
        for name in ('e', 'g', 'boundary_carry'):
            require(type(edge.get(name)) is int and edge[name] in (0, 1),
                    'A witnessed carry is not a binary integer')
        require(type(edge.get('v')) is int and edge['v'] >= 0, 'Invalid center trim')
        for name in ('prefix', 'next_prefix'):
            coefficient_word(edge.get(name), True)
            require(len(edge[name]) == prefix_width, 'Wrong exterior-prefix width')
        for name in ('C', 'next_C'):
            coefficient_word(edge.get(name), bound=center_bound)
    # This oracle evaluates whole positional integers. The sentinel's e is
    # auxiliary and must never be identified with the actual center entry e.
    try:
        replay = integer_oracle.witness_check({'edges': edges})
    except (integer_oracle.CheckFailure, KeyError, TypeError) as error:
        raise CheckFailure(str(error)) from error
    e = ''.join(str(edge['e']) for edge in edges)
    g = ''.join(str(edge['g']) for edge in edges)
    v = [edge['v'] for edge in edges]
    period = len(edges)
    full_key, rotation, _ = driver_key(e, g)
    primitive_key, primitive_rotation, primitive = driver_key(e, g, True)
    expected = {'period': period, 'primitive_eg_period': primitive,
                'e': e, 'g': g, 'v': v,
                'sum_g': sum(map(int, g)), 'sum_v': sum(v)}
    for key, value in expected.items():
        require(row.get(key) == value, 'Incorrect DRIVER metadata: '+key)
        if type(value) is int:
            require(type(row[key]) is int, 'Noninteger DRIVER metadata: '+key)
    require(isinstance(row['v'], list) and all(type(x) is int for x in row['v']),
            'Trim stream must be a list of integers')
    require(expected['sum_g'] > 0, 'Catalog witness lacks positive total overflow')
    center_signatures = [(tuple(a['C']), a['e'], a['g'], a['v'], tuple(a['next_C']))
                         for a in edges]
    product_signatures = [(tuple(a['prefix']), center_signatures[i],
                           tuple(a['next_prefix']), a['boundary_carry'])
                          for i, a in enumerate(edges)]
    center_seam = edges[primitive-1]['next_C'] == edges[0]['C']
    prefix_seam = edges[primitive-1]['next_prefix'] == edges[0]['prefix']
    return dict(expected, edges=edges, canonical_eg_key=full_key,
                primitive_eg_key=primitive_key, canonical_rotation=rotation,
                primitive_rotation=primitive_rotation,
                literal_center_period=least_period(center_signatures),
                literal_product_period=least_period(product_signatures),
                center_returns_at_primitive_eg=center_seam,
                product_returns_at_primitive_eg=center_seam and prefix_seam,
                excluded_known_driver=known_family(e, g),
                integer_replayed_edges=replay['projected_cycle_edges'],
                actual_certificate=False)


def validate_catalog(rows):
    require(isinstance(rows, list) and rows and isinstance(rows[-1], dict)
            and rows[-1].get('type') == 'SUMMARY',
            'Catalog lacks its final status record')
    summary = rows[-1]
    require(summary.get('status') in ('SCC_COMPLETE', 'CATALOG_SAMPLED', 'UNDECIDED'),
            'Unsupported or overstated catalog status')
    seen, drivers, cores, scc_rows = set(), [], [], []
    for row in rows[:-1]:
        require(isinstance(row, dict) and row.get('type') in ('SCC', 'CORE', 'DRIVER'),
                'Unexpected catalog record')
        if row['type'] == 'SCC':
            scc_rows.append(row)
        if row['type'] == 'CORE':
            cores.append((row, validate_core(row)))
        if row['type'] == 'DRIVER':
            item = validate_driver(row)
            require(item['excluded_known_driver'] is None, 'Catalog includes an excluded owned driver')
            require(item['canonical_eg_key'] not in seen, 'Duplicate joint-rotation driver')
            seen.add(item['canonical_eg_key'])
            drivers.append(item)
    require(len(cores) <= 1, 'Repeated CORE records')
    if cores:
        core, checked = cores[0]
        states = {(tuple(v['prefix']), tuple(v['C'])) for v in core['vertices']}
        for driver in drivers:
            require(all((tuple(e['prefix']), tuple(e['C'])) in states for e in driver['edges']),
                    'Driver uses a state omitted by the exported cyclic core')
        for scc in scc_rows:
            for source_key, target_key in [('cyclic_vertices', 'vertices'),
                                           ('cyclic_arcs', 'arcs'),
                                           ('cyclic_components', 'components')]:
                require(scc.get(source_key) == checked[target_key], 'CORE/SCC totals disagree')
    return {'status': 'UNDECIDED' if summary['status'] == 'UNDECIDED' else 'PASS',
            'producer_status': summary['status'], 'driver_records': len(drivers),
            'replayed_edges': sum(d['period'] for d in drivers),
            'primitive_driver_classes': len({d['primitive_eg_key'] for d in drivers}),
            'core': cores[0][1] if cores else None,
            'catalog_exhaustiveness_verified': False, 'actual_certificate': False}


def strong_components(n, edges):
    """Independent iterative two-pass SCC partition, separate from Tarjan."""
    forward, reverse = [[] for _ in range(n)], [[] for _ in range(n)]
    for a, b in edges:
        forward[a].append(b); reverse[b].append(a)
    visited, finish = set(), []
    for root in range(n):
        if root in visited:
            continue
        visited.add(root); stack = [(root, 0)]
        while stack:
            vertex, offset = stack[-1]
            if offset == len(forward[vertex]):
                finish.append(vertex); stack.pop(); continue
            stack[-1] = (vertex, offset+1)
            target = forward[vertex][offset]
            if target not in visited:
                visited.add(target); stack.append((target, 0))
    visited, result = set(), set()
    for root in reversed(finish):
        if root in visited:
            continue
        visited.add(root); todo, part = [root], {root}
        while todo:
            for target in reverse[todo.pop()]:
                if target not in visited:
                    visited.add(target); part.add(target); todo.append(target)
        result.add(frozenset(part))
    return result


def validate_core(row):
    """Check every exported internal arc, partition, and internal factor edge.

    Completeness of the cyclic vertices within the whole product is a separate
    property of the controlled full sink/SCC traversal, not inferred here.
    """
    require(isinstance(row, dict) and row.get('type') == 'CORE'
            and row.get('status') == 'COMPLETE' and row.get('certificate') is False,
            'Invalid CORE header')
    require(row.get('scope') == 'internal_arcs_of_cyclic_projection_SCCs'
            and row.get('boundary_carry_role') == 'one_realizing_choice', 'Unsupported CORE semantics')
    vertices, edges = row.get('vertices'), row.get('edges')
    require(isinstance(vertices, list) and len(vertices) <= 10000
            and isinstance(edges, list) and len(edges) <= 50000, 'Unsupported CORE size')
    width, bound = row.get('prefix_width'), row.get('center_bound')
    require(type(width) is int and 1 <= width <= 3
            and type(bound) is int and 1 <= bound <= 7, 'Unsupported CORE domain')
    require(type(row.get('even_middle')) is bool, 'CORE middle policy must be explicit')
    require(type(row.get('vertex_count')) is int and row['vertex_count'] == len(vertices)
            and type(row.get('edge_count')) is int and row['edge_count'] == len(edges),
            'CORE counts disagree with its arrays')
    by_id, by_word, grouped = {}, {}, {}
    for position, vertex in enumerate(vertices):
        require(isinstance(vertex, dict) and type(vertex.get('id')) is int
                and vertex['id'] >= 0 and type(vertex.get('scc')) is int
                and vertex['scc'] >= 0, 'Invalid CORE vertex labels')
        require(type(vertex.get('e')) is int and vertex['e'] in (0, 1), 'Invalid CORE entry carry')
        coefficient_word(vertex.get('prefix'), True)
        coefficient_word(vertex.get('C'), bound=bound)
        require(len(vertex['prefix']) == width, 'CORE prefix width mismatch')
        require(integer_oracle.normalized(vertex['C'], vertex['e'])[1] == 1-vertex['e'],
                'CORE vertex carry does not flip')
        key = (tuple(vertex['prefix']), tuple(vertex['C']))
        require(vertex['id'] not in by_id and key not in by_word, 'Duplicate CORE vertex')
        by_id[vertex['id']] = (position, vertex); by_word[key] = vertex['id']
        grouped.setdefault(vertex['scc'], set()).add(position)
    actual, adjacency = set(), []
    for edge in edges:
        require(isinstance(edge, dict) and type(edge.get('source')) is int
                and type(edge.get('target')) is int and edge['source'] in by_id
                and edge['target'] in by_id, 'CORE edge has an absent endpoint')
        for field in ('g', 'boundary_carry'):
            require(type(edge.get(field)) is int and edge[field] in (0, 1), 'Invalid CORE carry')
        require(type(edge.get('v')) is int and edge['v'] >= 0, 'Invalid CORE trim')
        source_pos, source = by_id[edge['source']]; target_pos, target = by_id[edge['target']]
        require(source['scc'] == target['scc'], 'CORE contains a cross-component edge')
        raw, _auxiliary_e, growth = integer_oracle.exterior(tuple(source['prefix'])+(18*edge['boundary_carry'],))
        require((raw[:width], growth) == (tuple(target['prefix']), edge['g']),
                'CORE prefix edge fails integer replay')
        require(center_step(source['C'], source['e'], edge['g'], edge['v']) == tuple(target['C']),
                'CORE center edge fails integer replay')
        key = (edge['source'], edge['target'], edge['g'], edge['v'])
        require(key not in actual, 'Duplicate CORE arc')
        actual.add(key); adjacency.append((source_pos, target_pos))
    expected = set()
    for _position, source in by_id.values():
        for prefix, g in integer_oracle.prefix_edges(tuple(source['prefix'])):
            for center, _e, v in integer_oracle.center_edges(tuple(source['C']), g, bound, row['even_middle']):
                target_id = by_word.get((prefix, center))
                if target_id is not None and by_id[target_id][1]['scc'] == source['scc']:
                    expected.add((source['id'], target_id, g, v))
    require(actual == expected, 'CORE omits or adds an internal factor edge')
    parts = strong_components(len(vertices), adjacency)
    require(parts == {frozenset(part) for part in grouped.values()}, 'CORE SCC partition disagrees')
    loops = {source for source, target in adjacency if source == target}
    require(all(len(part) > 1 or bool(part & loops) for part in parts), 'CORE includes an acyclic component')
    return {'vertices': len(vertices), 'arcs': len(edges), 'components': len(parts),
            'internal_factor_completeness': True,
            'whole_product_core_completeness_verified': False}


def center_step(center, e, g, v, base=10):
    digits, carry = integer_oracle.normalized(tuple(center), e, base)
    require(carry == 1-e, 'Independent center does not flip its incoming carry')
    word = digits+((base-1)*e,) if g else digits
    raw = tuple(a+b for a, b in zip(word, word[::-1]))
    require(type(v) is int and 0 <= 2*v < len(raw), 'Center trim removes the whole word')
    require(raw[:v] == (base-1,)*v and (not v or raw[-v:] == (base-1,)*v),
            'Center trim is not neutral')
    return raw[v:len(raw)-v]


def canonical_controls():
    counts = Counter()
    for length in range(1, 7):
        for symbols in itertools.product(range(4), repeat=length):
            e = ''.join(str(x//2) for x in symbols)
            g = ''.join(str(x % 2) for x in symbols)
            key = driver_key(e, g)[0]
            primitive = driver_key(e, g, True)[0]
            for offset in range(length):
                ee, gg = e[offset:]+e[:offset], g[offset:]+g[:offset]
                require(driver_key(ee, gg)[0] == key, 'Aligned rotation changes its key')
                counts['rotations'] += 1
            for repeat in (2, 3):
                require(driver_key(e*repeat, g*repeat, True)[0] == primitive,
                        'Literal repetition changes the primitive driver')
                require(driver_key(e*repeat, g*repeat)[0] != key,
                        'Full-period identity incorrectly ignores lap count')
                counts['repetitions'] += 1
            counts['pair_words'] += 1
    require(driver_key('0011', '0011')[0] != driver_key('0011', '0110')[0],
            'Independent stream rotation erased relative phase')
    for name, item in KNOWN.items():
        for repeat in (1, 2, 3):
            e, g = item['e']*repeat, item['g']*repeat
            for offset in range(len(e)):
                require(known_family(e[offset:]+e[:offset], g[offset:]+g[:offset]) == name,
                        'Owned rotation/repetition was not recognized')
                counts['known_exclusions'] += 1
    return dict(counts)


def arithmetic_controls():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import neutral_band_search as mirror
    counts = Counter()
    for base, edges in mirror._lean_certs():
        entries, growths = [], []
        for B, C, B2, C2, _u, v in edges:
            _raw, e, g = integer_oracle.exterior(tuple(B), base)
            require(center_step(C, e, g, v, base) == tuple(C2), 'Source center replay failed')
            padded = tuple(B)+(base-1,)*max(0, 3-len(B))
            cut = integer_oracle.normalized(padded[3:][::-1], 1-e, base)[1]
            sentinel = padded[:3]+((2*base-2)*cut,)
            raw, _auxiliary_e, gg = integer_oracle.exterior(sentinel, base)
            require((raw[:3], gg) == (integer_oracle.pad_prefix(B2, 3, base), g),
                    'Known exterior misses the sentinel projection')
            entries.append(str(e)); growths.append(str(g))
            counts['source_edges'] += 1
        primitive = driver_key(''.join(entries), ''.join(growths), True)[2]
        if edges[primitive-1][3] != edges[0][1]:
            counts['driver_period_without_center_return'] += 1
        counts['source_cycles'] += 1
    require(counts['driver_period_without_center_return'] > 0,
            'Missing positive control for invalid period descent')
    for item in KNOWN.values():
        current = tuple(item['C0'])
        require(len(item['e']) == len(item['g']) == len(item['v']), 'Known stream lengths disagree')
        for e, g, v in zip(item['e'], item['g'], item['v']):
            current = center_step(current, int(e), int(g), int(v))
            counts['owned_center_edges'] += 1
        require(current == tuple(item['C0']), 'Owned center cycle fails literal closure')
    return dict(counts)


def owned_decimal_fixture():
    """Reconstruct the credited P24 projection without an external data file."""
    item = KNOWN['Agent101_P24']
    prefix, center, edges = (9, 17, 17), tuple(item['C0']), []
    cuts = '001001010100'*2
    for e, g, v, cut in zip(item['e'], item['g'], item['v'], cuts):
        e, g, v, cut = map(int, (e, g, v, cut))
        raw, _auxiliary_e, actual_g = integer_oracle.exterior(prefix+(18*cut,))
        require(actual_g == g, 'Owned prefix reconstruction changed overflow')
        target, next_center = raw[:3], center_step(center, e, g, v)
        edges.append({'prefix': list(prefix), 'C': list(center), 'e': e, 'g': g,
                      'v': v, 'boundary_carry': cut, 'next_prefix': list(target),
                      'next_C': list(next_center)})
        prefix, center = target, next_center
    return {'type': 'DRIVER', 'period': 24, 'primitive_eg_period': 24,
            'e': item['e'], 'g': item['g'], 'v': list(map(int, item['v'])),
            'sum_g': 8, 'sum_v': 4, 'certificate': False, 'edges': edges}


def witness_controls():
    original = owned_decimal_fixture()
    unchanged = json.dumps(original, sort_keys=True)
    result = validate_driver(original)
    require(result['excluded_known_driver'] == 'Agent101_P24', 'Owned witness lost attribution')
    require(json.dumps(original, sort_keys=True) == unchanged, 'Validation mutated its input')
    rotated = copy.deepcopy(original)
    for name in ('e', 'g', 'v', 'edges'):
        rotated[name] = rotated[name][3:]+rotated[name][:3]
    require(validate_driver(rotated)['canonical_eg_key'] == result['canonical_eg_key'],
            'Literal rotated witness changed driver class')
    repeated = copy.deepcopy(original)
    for name in ('e', 'g', 'v', 'edges'):
        repeated[name] *= 2
    repeated.update(period=48, sum_g=16, sum_v=8)
    doubled = validate_driver(repeated)
    require(doubled['period'] == 48 and doubled['primitive_eg_period'] == 24
            and doubled['literal_center_period'] == 24,
            'Validator silently shortened the literal witness')

    corruptions = []
    for key, value in [('period', 12), ('primitive_eg_period', 12),
                       ('sum_g', 9), ('sum_v', 5), ('certificate', True)]:
        broken = copy.deepcopy(original); broken[key] = value; corruptions.append(broken)
    for key, value in [('e', 1), ('g', 0), ('v', -1), ('boundary_carry', 2)]:
        broken = copy.deepcopy(original); broken['edges'][0][key] = value; corruptions.append(broken)
    broken = copy.deepcopy(original); broken['edges'][0]['prefix'][0] = 0; corruptions.append(broken)
    broken = copy.deepcopy(original); broken['edges'][0]['C'][3] = 17; corruptions.append(broken)
    broken = copy.deepcopy(original)
    for name in ('e', 'g', 'v', 'edges'):
        broken[name] = broken[name][:12]
    broken.update(period=12, primitive_eg_period=12, sum_g=4, sum_v=2)
    corruptions.append(broken)  # The shorter g period does not close the center.
    for broken in corruptions:
        try:
            validate_driver(broken)
        except CheckFailure:
            continue
        raise CheckFailure('Malformed or shortened projection was accepted')
    try:
        validate_catalog([original, {'type': 'SUMMARY', 'status': 'CATALOG_SAMPLED'}])
    except CheckFailure:
        pass
    else:
        raise CheckFailure('New-driver catalog accepted the owned P24 family')
    malformed_catalogs = [None, 'invalid', [], [None],
                          [17, {'type': 'SUMMARY', 'status': 'SCC_COMPLETE'}],
                          [{'type': 'SUMMARY', 'status': 'COMPLETE'}]]
    for broken in malformed_catalogs:
        try:
            validate_catalog(broken)
        except CheckFailure:
            continue
        raise CheckFailure('Malformed catalog container/status was accepted')
    return {'accepted_witnesses': 3, 'replayed_edges': 96,
            'rejected_witnesses': len(corruptions), 'owned_catalog_rejections': 1,
            'malformed_catalog_rejections': len(malformed_catalogs)}


def core_controls():
    fixture = owned_decimal_fixture()
    core = {'type': 'CORE', 'status': 'COMPLETE', 'certificate': False,
            'scope': 'internal_arcs_of_cyclic_projection_SCCs',
            'boundary_carry_role': 'one_realizing_choice',
            'prefix_width': 3, 'center_bound': 7, 'even_middle': True,
            'vertex_count': 24, 'edge_count': 24, 'vertices': [], 'edges': []}
    for i, edge in enumerate(fixture['edges']):
        core['vertices'].append({'id': i, 'scc': 0, 'prefix': edge['prefix'],
                                 'C': edge['C'], 'e': edge['e']})
        core['edges'].append({'source': i, 'target': (i+1) % 24, 'g': edge['g'],
                              'v': edge['v'], 'boundary_carry': edge['boundary_carry']})
    checked = validate_core(core)
    corruptions = []
    bad = copy.deepcopy(core); bad['vertices'][0]['scc'] = 1; corruptions.append(bad)
    bad = copy.deepcopy(core); bad['edges'].pop(); bad['edge_count'] -= 1; corruptions.append(bad)
    bad = copy.deepcopy(core); bad['edges'].append(bad['edges'][0]); bad['edge_count'] += 1; corruptions.append(bad)
    bad = copy.deepcopy(core); bad['edges'][0]['source'] = 999; corruptions.append(bad)
    bad = copy.deepcopy(core); bad['edges'][0]['boundary_carry'] = 2; corruptions.append(bad)
    bad = copy.deepcopy(core); bad['vertices'][0]['e'] ^= 1; corruptions.append(bad)
    bad = copy.deepcopy(core); bad['scope'] = 'all_finite_exteriors'; corruptions.append(bad)
    bad = copy.deepcopy(core); bad['vertices'][0] = None; corruptions.append(bad)
    bad = copy.deepcopy(core); bad['edges'][0] = None; corruptions.append(bad)
    for bad in corruptions:
        try:
            validate_core(bad)
        except CheckFailure:
            continue
        raise CheckFailure('Malformed or incomplete CORE was accepted')
    return {'positive_vertices': checked['vertices'], 'positive_arcs': checked['arcs'],
            'rejected_core_mutations': len(corruptions)}


def fixture_partition(n, edges):
    reach = [(1 << i) for i in range(n)]
    for source, target in edges:
        reach[source] |= 1 << target
    for k in range(n):
        for i in range(n):
            if reach[i] & (1 << k):
                reach[i] |= reach[k]
    unseen, result = set(range(n)), set()
    while unseen:
        i = min(unseen)
        part = frozenset(j for j in unseen if reach[i] & (1 << j) and reach[j] & (1 << i))
        result.add(part); unseen.difference_update(part)
    return result


def tarjan_controls(engine):
    rng = random.Random(101)
    cases = [(0, []), (1, []), (1, [(0, 0)]),
             (2, [(0, 1)]), (2, [(0, 1), (1, 0), (0, 1)])]
    for _ in range(100):
        n = rng.randrange(1, 25)
        cases.append((n, [(rng.randrange(n), rng.randrange(n))
                          for _ in range(rng.randrange(3*n+1))]))
    for n, edges in cases:
        payload = str(n)+' '+str(len(edges))+'\n'+''.join(f'{a} {b}\n' for a, b in edges)
        process = subprocess.run([engine, '--scc-fixture'], input=payload, text=True,
                                 capture_output=True, timeout=15, check=False)
        require(process.returncode == 0, 'Tarjan fixture command failed: '+process.stderr[:200])
        rows = [json.loads(line) for line in process.stdout.splitlines() if line.strip()]
        fixtures = [row for row in rows if isinstance(row, dict) and row.get('type') == 'SCC_FIXTURE']
        require(len(fixtures) == 1, 'Expected one Tarjan fixture result')
        row = fixtures[0]
        require(row.get('type') == 'SCC_FIXTURE' and row.get('status') == 'COMPLETE',
                'Tarjan fixture was not complete')
        labels = row['component']
        require(len(labels) == n, 'Tarjan omitted a vertex')
        actual = {frozenset(i for i, value in enumerate(labels) if value == label)
                  for label in set(labels)}
        expected = fixture_partition(n, edges)
        require(strong_components(n, edges) == expected,
                'Two-pass checker differs from transitive closure')
        require(actual == expected, 'Tarjan differs from transitive-closure SCCs')
        loops = {a for a, b in edges if a == b}
        cyclic = [part for part in expected if len(part) > 1 or bool(part & loops)]
        for key, value in [('vertices', n), ('arcs', len(edges)), ('components', len(expected)),
                           ('cyclic_components', len(cyclic)),
                           ('cyclic_vertices', sum(map(len, cyclic)))]:
            require(row[key] == value, 'Wrong Tarjan fixture count: '+key)
    return {'fixtures': len(cases), 'vertices': sum(n for n, _ in cases),
            'arcs_with_multiplicity': sum(len(edges) for _, edges in cases)}


def product_scc_control(engine):
    import numpy as np
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import connected_components
    prefixes = list(integer_oracle.prefixes(1))
    centers = list(integer_oracle.centers(5, False))
    pids, cids = {w: i for i, w in enumerate(prefixes)}, {w: i for i, w in enumerate(centers)}
    pf = [[(pids[target], g) for target, g in integer_oracle.prefix_edges(word)] for word in prefixes]
    cf = [[(cids[target], g) for g in (0, 1)
           for target, _e, _v in integer_oracle.center_edges(word, g, 5, False)] for word in centers]
    n, nc = len(prefixes)*len(centers), len(centers)
    forward, reverse = [[] for _ in range(n)], [[] for _ in range(n)]
    for p, pe in enumerate(pf):
        for c, ce in enumerate(cf):
            source = p*nc+c
            targets = {pp*nc+cc for pp, g in pe for cc, h in ce if g == h}
            forward[source] = sorted(targets)
            for target in targets:
                reverse[target].append(source)
    degree = [len(row) for row in forward]
    queue = deque(i for i, d in enumerate(degree) if not d)
    while queue:
        target = queue.popleft()
        for source in reverse[target]:
            degree[source] -= 1
            if degree[source] == 0:
                queue.append(source)
    live = [i for i, d in enumerate(degree) if d]
    indptr = [0]; targets = []
    for row in forward:
        targets.extend(row); indptr.append(len(targets))
    graph = csr_matrix((np.ones(len(targets), dtype=np.int8),
                        np.array(targets, dtype=np.int32), np.array(indptr, dtype=np.int32)), shape=(n, n))
    _components, labels = connected_components(graph, directed=True, connection='strong')
    sizes = Counter(int(labels[i]) for i in live)
    internal = Counter()
    self_loops = set()
    for source in live:
        for target in forward[source]:
            if degree[target] and labels[source] == labels[target]:
                internal[int(labels[source])] += 1
                if source == target:
                    self_loops.add(int(labels[source]))
    cyclic = {label for label, size in sizes.items() if size > 1 or label in self_loops}
    expected = {'vertices': n, 'arcs': len(targets), 'residual_vertices': len(live),
                'residual_arcs': sum(degree[i] for i in live), 'components': len(sizes),
                'cyclic_components': len(cyclic), 'cyclic_vertices': sum(sizes[i] for i in cyclic),
                'cyclic_arcs': sum(internal[i] for i in cyclic)}
    process = subprocess.run([engine, '--scc-only', '--prefix', '1', '--center', '5',
                              '--all-middles', '--seconds', '120', '--memory-mb', '1024'],
                             text=True, capture_output=True, timeout=125, check=False)
    require(process.returncode == 0, 'Product SCC control did not complete')
    rows = [json.loads(line) for line in process.stdout.splitlines()]
    row = next(item for item in rows if item.get('type') == 'SCC')
    require(row['status'] == 'COMPLETE', 'Incomplete product SCC record')
    for key, value in expected.items():
        require(row[key] == value, 'Product SCC count mismatch: '+key)
    actual_hist = {x['size']: x['count'] for x in row['size_histogram']}
    require(actual_hist == dict(Counter(sizes.values())), 'Product SCC size histogram differs')
    return expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('--catalog', type=Path)
    parser.add_argument('--engine')
    args = parser.parse_args()
    output = {'status': 'PASS'}
    if args.selftest or not (args.catalog or args.engine):
        output['canonicalization'] = canonical_controls()
        output['arithmetic'] = arithmetic_controls()
        output['witnesses'] = witness_controls()
        output['core_controls'] = core_controls()
    if args.catalog:
        with args.catalog.open() as source:
            output['catalog'] = validate_catalog([json.loads(line) for line in source if line.strip()])
        if output['catalog']['status'] == 'UNDECIDED':
            output['status'] = 'UNDECIDED'
    if args.engine:
        output['tarjan'] = tarjan_controls(args.engine)
        output['product_scc'] = product_scc_control(args.engine)
    print(json.dumps(output, sort_keys=True))
    return 3 if output['status'] == 'UNDECIDED' else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (CheckFailure, KeyError, TypeError, ValueError, OSError, subprocess.TimeoutExpired) as error:
        print(json.dumps({'status': 'FAIL', 'reason': str(error)}))
        sys.exit(1)
