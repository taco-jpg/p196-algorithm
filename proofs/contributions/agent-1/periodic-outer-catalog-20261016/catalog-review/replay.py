#!/usr/bin/env python3
"""Replay only the archived outer product; do not discover states or cycles."""
import argparse
import ast
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import platform
import re
import sys
import traceback


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


ARCHIVE = ('proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/'
           'proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/')
PINS = {
    ARCHIVE + 'outer_filtered_graph.json.gz': (
        'c3eb0a4bd4bc8e390d7681746e66300851035dff1b102412e2d14977ed1088e5',
        'c7bcc931f3cb36bd6845abeade0f7fd7b9723e08'),
    ARCHIVE + 'outer_filtered_results.json': (
        'b444d8bcea8fb07368638b2f52cea57f2b4647dd385864313c12c9d0c4498506',
        '29ff1888439d8be43f3161dbdb59846d82063d7f'),
    ARCHIVE + 'outer_filter.py': (
        '6c336a1b7d1d71e6525bec42a001572bfd7ee98115c2991b961d10c455f30d9c',
        'ca0fe5e4cf9f6df4528d1e1375c9bfc404ad04f6'),
    'proofs/outer_filter__4b3d159990f5e177.py': (
        '6c336a1b7d1d71e6525bec42a001572bfd7ee98115c2991b961d10c455f30d9c',
        'ca0fe5e4cf9f6df4528d1e1375c9bfc404ad04f6'),
    ARCHIVE + 'bulk_phases.py': (
        '5bdd7d03f0e29f081dddde9ad6e00223f3acc19a26db8d8baca2c41e0be848d4',
        '46a1ad0bbd6491685f98f6dc9201c9c16775a50c'),
    'proofs/bulk_phases__50a5613b2ee6f003.py': (
        '5bdd7d03f0e29f081dddde9ad6e00223f3acc19a26db8d8baca2c41e0be848d4',
        '46a1ad0bbd6491685f98f6dc9201c9c16775a50c'),
    ARCHIVE + 'bulk_phase_graph.json.gz': (
        'a22b2e39e4b2ed31d00b0c69694cd25b29f63135cd2378a16e3a434781855bb2',
        'ef81b2d214f37e79d04cd8c8aa9bc764c227a54e'),
    'proofs/PeriodObstructions__70ce034b31b5b218.lean': (
        '83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a',
        'a89dda20e9a9b3452f7d0272b4fbd28f7d6ce119'),
    'proofs/Agent1PeriodicPhaseCatalog.lean': (
        '44445a343635503c940ea125727d0bbb75bbf7dce24be62c28a660241363f9f9',
        'a9414bc8c9be783f5dfc48778db7161c481a96fc'),
}


def isolated_function(source, name, filename):
    tree = ast.parse(source)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    namespace = dict(itertools=itertools)
    exec(compile(ast.Module(body=[node], type_ignores=[]), filename, 'exec'), namespace)
    return namespace[name], ast.get_source_segment(source, node)


def overflow(p, inner):
    return 0 if p + inner < 10 else 1


def next_exterior(p, inner):
    return 2*p + inner if p + inner < 10 else p % 10 + 1


def outer_images(p, clock):
    # Direct interpretation of range2/filterMap followed by eraseDups.
    filtered = [next_exterior(p, inner) for inner in range(2)
                if overflow(p, inner) == clock]
    return list(dict.fromkeys(filtered))


def state_key(state):
    return tuple(state[0]), state[1]


def parse_phase_edges(text):
    section = re.search(r'^def phaseEdges : List PhaseEdge := \[\n(.*?)^\]', text, re.M | re.S)
    assert section, 'Literal phaseEdges absent'
    edges = []
    for line in section[1].splitlines():
        m = re.fullmatch(r'\s*⟨(\[[0-9, ]+\]), ([01]), (none|some \(([01]),([01])\)), (\[[0-9, ]+\])⟩,?', line)
        assert m, ('Unparsed phase edge', line)
        edge = dict(source=ast.literal_eval(m[1]), clock=int(m[2]), target=ast.literal_eval(m[6]))
        if m[3] != 'none':
            edge.update(left_carry=int(m[4]), right_carry=int(m[5]))
        edges.append(edge)
    return edges


def review(root, out):
    provenance, contents = [], {}
    for path, (expected_sha, expected_blob) in PINS.items():
        data = (root / path).read_bytes()
        assert sha(data) == expected_sha, ('SHA256 mismatch', path, sha(data))
        assert blob(data) == expected_blob, ('Git blob mismatch', path, blob(data))
        contents[path] = data
        provenance.append(dict(path=path, bytes=len(data), sha256=sha(data), git_blob=blob(data)))
    save(out / 'provenance.json', provenance)
    raw = gzip.decompress(contents[ARCHIVE+'outer_filtered_graph.json.gz'])
    assert sha(raw) == 'cbd5c62ac2af58d0d0ce1cbb6f0cf9199ac49c75291d062179caf15f96e1ad50'
    graph = json.loads(raw)
    prior = json.loads(contents[ARCHIVE+'outer_filtered_results.json'])
    assert sha(raw) == prior['payload_sha256']
    (out / 'original-payload.json').write_bytes(raw)
    original_outer, outer_source = isolated_function(
        contents[ARCHIVE+'outer_filter.py'].decode(), 'outer', ARCHIVE+'outer_filter.py')
    original_outputs, outputs_source = isolated_function(
        contents[ARCHIVE+'bulk_phases.py'].decode(), 'outputs', ARCHIVE+'bulk_phases.py')
    (out / 'original-functions.txt').write_text(outer_source+'\n\n'+outputs_source+'\n')

    phase_payload = gzip.decompress(contents[ARCHIVE+'bulk_phase_graph.json.gz'])
    assert sha(phase_payload) == '4100f332c808b277d8d3052fc6b16aef0637aa185c45bd3525ddac5267ebc3c6'
    phase_graph = json.loads(phase_payload)
    phase_edges = parse_phase_edges(contents['proofs/Agent1PeriodicPhaseCatalog.lean'].decode())
    original_phase_edges = [dict(source=row['source'], **edge)
                            for row in phase_graph['graph'] for edge in row['edges']]
    assert phase_edges == original_phase_edges
    assert len(phase_edges) == 124
    for row in phase_graph['graph']:
        assert row['edges'] == json.loads(json.dumps(original_outputs(tuple(row['source']))))

    scalar_checks = []
    for p in range(1, 19):
        for clock in range(2):
            bit_rows = [dict(inner=inner, original_clock=(p+inner)//10,
                lean_clock=overflow(p, inner), original_target=p%10+(1 if clock else (p+inner)%10),
                lean_target=next_exterior(p, inner)) for inner in range(2)
                if (p+inner)//10 == clock]
            for entry in bit_rows:
                assert entry['original_clock'] == entry['lean_clock'] == clock
                assert entry['original_target'] == entry['lean_target']
            old, proposed = original_outer(p, clock), outer_images(p, clock)
            assert old == proposed, dict(outside=p, clock=clock, original=old, proposed=proposed)
            scalar_checks.append(dict(outside=p, clock=clock, admitted_bits=bit_rows,
                raw_targets=[e['lean_target'] for e in bit_rows],
                original_sorted_targets=old, proposed_deduplicated_targets=proposed))
    save(out / 'scalar-checks.json', scalar_checks)

    records = graph['graph']
    states = [row['source'] for row in records]
    keys = [state_key(state) for state in states]
    assert len(states) == len(set(keys)) == prior['reachable_states'] == 878
    assert keys == sorted(keys)
    state_set = set(keys)
    phase_set = {tuple(row['source']) for row in phase_graph['graph']}
    assert all(tuple(w) in phase_set and type(p) is int and 1 <= p <= 18 for w,p in states)
    initial = [[[14,14,4,4], p] for p in range(1,19)]
    assert graph['initial'] == initial
    assert len({state_key(state) for state in initial}) == 18
    assert all(state_key(state) in state_set for state in initial)
    component_keys = [state_key(state) for component in graph['components'] for state in component]
    assert len(component_keys) == len(set(component_keys)) == 878
    assert set(component_keys) == state_set
    distribution = dict(Counter(map(len, graph['components'])))
    assert distribution == {1:128, 18:3, 696:1}
    assert len(graph['components']) == prior['strong_components'] == 132
    assert {str(k):v for k,v in distribution.items()} == prior['component_size_distribution']

    flat, edge_checks, row_checks = [], [], []
    naive_count = 0
    nine_count = 0
    for row_index, row in enumerate(records):
        word, p = row['source']
        original, proposed, details = [], [], []
        for phase_edge in original_outputs(tuple(word)):
            for target_outer in original_outer(p, phase_edge['clock']):
                original.append(dict(clock=phase_edge['clock'], target=[list(phase_edge['target']),target_outer],
                    **{k:v for k,v in phase_edge.items() if k not in ('clock','target')}))
        filtered_phase_edges = [(i,e) for i,e in enumerate(phase_edges) if e['source'] == word]
        assert len(filtered_phase_edges) == (8 if word == [9,9,9,9] else 2)
        for phase_index, phase_edge in filtered_phase_edges:
            clock = phase_edge['clock']
            raw_targets = [next_exterior(p, inner) for inner in range(2) if overflow(p,inner) == clock]
            naive_count += len(raw_targets)
            for target_outer in outer_images(p, clock):
                edge = dict(clock=clock, target=[phase_edge['target'],target_outer],
                    **{k:v for k,v in phase_edge.items() if k not in ('source','clock','target')})
                proposed.append(edge)
                details.append(dict(phase_edge_index=phase_index,
                    raw_outer_targets=raw_targets, deduplicated_outer_targets=outer_images(p,clock),
                    witnessing_outer_incoming_bits=[inner for inner in range(2)
                        if overflow(p,inner) == clock and next_exterior(p,inner) == target_outer]))
        assert row['edges'] == original, dict(kind='original generator mismatch', row_index=row_index,
            source=row['source'], archived=row['edges'], original=original)
        assert row['edges'] == proposed, dict(kind='proposed formula mismatch', row_index=row_index,
            source=row['source'], archived=row['edges'], proposed=proposed)
        for edge_index, edge in enumerate(row['edges']):
            assert state_key(edge['target']) in state_set, (row_index, edge_index, edge)
            if word == [9,9,9,9]:
                assert set(edge) == {'clock','left_carry','right_carry','target'}
                assert edge['target'][0] == [18-9*(edge['left_carry']+edge['right_carry'])]*4
                nine_count += 1
            else:
                assert set(edge) == {'clock','target'}
            flat.append(dict(source=row['source'], **edge))
            edge_checks.append(dict(row_index=row_index, edge_index=edge_index,
                source=row['source'], edge=edge, original_match=True, proposed_match=True, **details[edge_index]))
        row_checks.append(dict(row_index=row_index, source=row['source'],
            original_order_and_labels_match=True, proposed_order_and_labels_match=True,
            edge_count=len(row['edges'])))
    assert len(flat) == prior['edges'] == 1458
    assert len({json.dumps(e,sort_keys=True) for e in flat}) == 1458
    save(out / 'states.json', states)
    save(out / 'initial.json', initial)
    save(out / 'labelled-edges.json', flat)
    save(out / 'row-checks.json', row_checks)
    save(out / 'edge-checks.json', edge_checks)
    assert all((root / path).read_bytes() == data for path,data in contents.items())
    return dict(status='PASS', claim_commit='db88a5c78fd5f67ac134031d8486c26df9201799',
        scope='Independent original artifact/formula review, not Lean acceptance or graph discovery',
        script_sha256=sha(Path(__file__).read_bytes()), python_version=platform.python_version(),
        graph_gzip_sha256=sha(contents[ARCHIVE+'outer_filtered_graph.json.gz']),
        graph_payload_sha256=sha(raw), state_count=878, labelled_edge_count=1458,
        state_nodup=True, complete_labelled_edge_nodup=True, initial_count=18,
        exact_initial_order_and_membership=True, all_targets_in_catalog=True,
        scalar_outer_cases_checked=36, original_outer_and_proposed_images_exact=True,
        original_phase_generator_and_literal_phase_edges_exact=True,
        all_original_product_rows_exact=True, all_proposed_product_rows_exact=True,
        source_row_and_edge_order_exact=True, all_nine_labelled_product_edges=nine_count,
        nondeduplicated_incoming_bit_edge_count=naive_count,
        duplicate_incoming_bit_edges_removed=naive_count-len(flat),
        stored_component_partition_distribution=distribution,
        graph_discovery_executed=False, scc_algorithm_executed=False,
        reachability_recomputed=False, lean_executed=False,
        original_artifacts_modified=False, source_drift=False)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-root',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args()
    out=args.output_dir.resolve()
    out.mkdir(parents=True,exist_ok=False)
    try:
        result=review(args.source_root.resolve(),out)
    except Exception:
        detail=traceback.format_exc()
        save(out/'verification.json',dict(status='FAIL',traceback=detail))
        (out/'run.log').write_text(detail)
        print(detail,file=sys.stderr)
        return 1
    save(out/'verification.json',result)
    log=json.dumps(result,indent=2,sort_keys=True)+'\n'
    (out/'run.log').write_text(log)
    print(log,end='')
    return 0


if __name__=='__main__':
    sys.exit(main())
