#!/usr/bin/env python3
"""Diagnostic replay of every recorded phase edge, without graph discovery.

Only the existing generator's outputs() function is executed. Its main(),
reachability exploration, SCC algorithm and cycle search are never invoked.
The zipper calculation is a separate direct interpretation of the pinned Lean
primitive definitions. This script supplies artifact evidence, not a Lean proof.
"""
import argparse
import ast
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import platform
import sys
import traceback


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


ARCHIVE = ('proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/'
           'proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/')
PINS = {
    ARCHIVE + 'bulk_phase_graph.json.gz': (
        'a22b2e39e4b2ed31d00b0c69694cd25b29f63135cd2378a16e3a434781855bb2',
        'ef81b2d214f37e79d04cd8c8aa9bc764c227a54e'),
    ARCHIVE + 'bulk_phase_results.json': (
        '9cef6aaf456d4b39e4ed7965401f2aba40d29553b0b2241ec4dad53926d4613f',
        '4a161c89c61706da3c80387e27f204239896b1a7'),
    ARCHIVE + 'bulk_phases.py': (
        '5bdd7d03f0e29f081dddde9ad6e00223f3acc19a26db8d8baca2c41e0be848d4',
        '46a1ad0bbd6491685f98f6dc9201c9c16775a50c'),
    'proofs/bulk_phases__50a5613b2ee6f003.py': (
        '5bdd7d03f0e29f081dddde9ad6e00223f3acc19a26db8d8baca2c41e0be848d4',
        '46a1ad0bbd6491685f98f6dc9201c9c16775a50c'),
    'proofs/ActualWordBridge__7f032d27940694a8.lean': (
        '3123e8f86fe751e61307ea528390bd265515a8d69c731f51e2808fb78d0a6ec6',
        'd3f49353f9970c610d818d8f5da78ad5c739e7df'),
    'proofs/Agent1PeriodicGuard.lean': (
        '4ba3877f27250e066bbe19dd066b55fa667576281e8dc984334b9a9b82fcee91',
        '7c62748625cecbc277ddd5e01ffb17671e4db7a8'),
}


def terminal_carry(word, entry):
    for coefficient in word:
        entry = (coefficient + entry) // 10
    return entry


def fixed_digits(word, entry):
    result = []
    for coefficient in word:
        result.append((coefficient + entry) % 10)
        entry = (coefficient + entry) // 10
    return result


def zipper_period(left, right, clock):
    reflected = list(reversed(right[:clock])) + list(reversed(right[clock:]))
    return [a + b for a, b in zip(left, reflected)]


def nonnine_details(word):
    """Independent bounded cyclic neighbors and literal list primitives."""
    size = len(word)
    assert any(q != 9 for q in word)
    carry_pairs, low, high = [], [], []
    for i, coefficient in enumerate(word):
        previous = next(word[(i-d) % size] for d in range(1, size+1)
                        if word[(i-d) % size] != 9)
        following = next(word[(i+d) % size] for d in range(1, size+1)
                         if word[(i+d) % size] != 9)
        a, b = int(previous >= 10), int(following >= 10)
        carry_pairs.append([a, b])
        low.append((coefficient + a) % 10)
        high.append((coefficient + b) % 10)
    reverse = list(reversed(word))
    left_carry = terminal_carry(word, 0)
    right_carry = terminal_carry(reverse, 0)
    left = fixed_digits(word, left_carry)
    right = fixed_digits(reverse, right_carry)
    assert left == low, dict(source=word, left=left, low=low)
    assert list(reversed(right)) == high, dict(source=word, right=right, high=high)
    return dict(cyclic_carry_pairs=carry_pairs, low=low, high=high,
                stable_forward_carry=left_carry, stable_reverse_carry=right_carry,
                left_digits=left, right_digits=right)


def review(root, out):
    provenance, contents = [], {}
    for path, (expected_sha, expected_blob) in PINS.items():
        data = (root / path).read_bytes()
        assert sha(data) == expected_sha, ('SHA256 mismatch', path, sha(data))
        assert blob(data) == expected_blob, ('Git blob mismatch', path, blob(data))
        contents[path] = data
        provenance.append(dict(path=path, bytes=len(data), sha256=sha(data), git_blob=blob(data)))
    write_json(out / 'provenance.json', provenance)
    raw = gzip.decompress(contents[ARCHIVE + 'bulk_phase_graph.json.gz'])
    assert sha(raw) == '4100f332c808b277d8d3052fc6b16aef0637aa185c45bd3525ddac5267ebc3c6'
    graph = json.loads(raw)
    prior = json.loads(contents[ARCHIVE + 'bulk_phase_results.json'])
    assert prior['payload_sha256'] == sha(raw)
    assert graph['initial'] == prior['initial'] == [14, 14, 4, 4]
    source = contents[ARCHIVE + 'bulk_phases.py'].decode()
    tree = ast.parse(source)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'outputs')
    isolated = ast.Module(body=[node], type_ignores=[])
    namespace = dict(itertools=itertools)
    exec(compile(isolated, ARCHIVE + 'bulk_phases.py', 'exec'), namespace)
    original_outputs = namespace['outputs']
    (out / 'generator-outputs.txt').write_text(ast.get_source_segment(source, node) + '\n')
    (out / 'original-payload.json').write_bytes(raw)

    records = graph['graph']
    phases = [row['source'] for row in records]
    phase_tuples = [tuple(p) for p in phases]
    assert len(phases) == len(set(phase_tuples)) == prior['reachable_indexed_phases'] == 59
    assert phase_tuples == sorted(phase_tuples)
    assert tuple(graph['initial']) in phase_tuples
    assert all(len(p) == 4 and all(type(x) is int and 0 <= x <= 18 for x in p) for p in phases)
    phase_set = set(phase_tuples)
    components = [tuple(p) for c in graph['components'] for p in c]
    assert len(components) == len(set(components)) == 59
    assert set(components) == phase_set
    assert sorted(map(len, graph['components'])) == [1, 1, 1, 56]
    assert len(graph['components']) == prior['strong_components'] == 4
    constants = sorted(p[0] for p in phases if len(set(p)) == 1)
    assert constants == prior['constants_reachable'] == [0, 9, 18]

    edges, checks, label_keys = [], [], []
    for row_index, row in enumerate(records):
        word = row['source']
        expected = json.loads(json.dumps(original_outputs(tuple(word))))
        assert row['edges'] == expected, dict(row_index=row_index, source=word,
            stored=row['edges'], generator=expected)
        nine = word == [9, 9, 9, 9]
        details = None if nine else nonnine_details(word)
        required_labels = list(itertools.product((0, 1), repeat=3)) if nine else [(0,), (1,)]
        observed_labels = []
        for edge_index, edge in enumerate(row['edges']):
            target, clock = edge['target'], edge['clock']
            assert clock in (0, 1), (row_index, edge_index, edge)
            assert tuple(target) in phase_set, (row_index, edge_index, edge)
            if nine:
                assert set(edge) == {'clock', 'left_carry', 'right_carry', 'target'}
                a, b = edge['left_carry'], edge['right_carry']
                assert a in (0, 1) and b in (0, 1)
                label = (clock, a, b)
                left, right = fixed_digits(word, a), fixed_digits(list(reversed(word)), b)
                formula = [18 - 9*(a+b)] * 4
                details_for_edge = dict(left_digits=left, right_digits=right,
                    actual_left_carry=a, actual_right_carry=b,
                    all_nine_exception=True)
            else:
                assert set(edge) == {'clock', 'target'}
                label = (clock,)
                left, right = details['left_digits'], details['right_digits']
                formula = [details['low'][i] + details['high'][(i-clock) % 4]
                           for i in range(4)]
                details_for_edge = dict(details, all_nine_exception=False)
            zipper = zipper_period(left, right, clock)
            assert formula == zipper == target, dict(row_index=row_index,
                edge_index=edge_index, source=word, edge=edge, cyclic_formula=formula,
                zipper_formula=zipper, details=details_for_edge)
            observed_labels.append(label)
            label_keys.append((tuple(word), label))
            edges.append(dict(source=word, **edge))
            checks.append(dict(row_index=row_index, edge_index=edge_index, source=word,
                label=list(label), stored_target=target, generator_target=expected[edge_index]['target'],
                cyclic_formula_target=formula, zipper_target=zipper, **details_for_edge))
        assert observed_labels == required_labels, (row_index, observed_labels, required_labels)
    assert len(edges) == len(label_keys) == len(set(label_keys)) == prior['edges'] == 124
    assert len({json.dumps(e, sort_keys=True) for e in edges}) == 124
    write_json(out / 'phases.json', phases)
    write_json(out / 'labelled-edges.json', edges)
    write_json(out / 'edge-checks.json', checks)
    # Re-read every pinned input after diagnostics to detect concurrent source drift.
    assert all((root / path).read_bytes() == data for path, data in contents.items())
    result = dict(status='PASS', scope='Diagnostic artifact review; no Lean proof or new search',
        claim_commit='6db01dafab1ec876d24c9964bc6086440ed21266',
        script_sha256=sha(Path(__file__).read_bytes()), python_version=platform.python_version(),
        graph_gzip_sha256=sha(contents[ARCHIVE+'bulk_phase_graph.json.gz']),
        graph_payload_sha256=sha(raw), phase_count=59, labelled_edge_count=124,
        nonnine_phase_count=58, nonnine_edge_checks=116, all_nine_label_checks=8,
        distinct_unlabelled_arcs=len({(tuple(e['source']),tuple(e['target'])) for e in edges}),
        distinct_clock_arcs=len({(tuple(e['source']),e['clock'],tuple(e['target'])) for e in edges}),
        phase_nodup=True, complete_labelled_edge_nodup=True,
        exact_generator_outputs_match=True, exact_label_sets_match=True,
        every_target_in_catalog=True, zipper_orientation_all_edges_match=True,
        forward_digits_equal_cyclic_low=True, reversed_backward_digits_equal_cyclic_high=True,
        initial=[14,14,4,4], constants=constants, stored_component_partition_sizes=[1,1,1,56],
        graph_discovery_executed=False, scc_algorithm_executed=False,
        reachability_recomputed=False, lean_executed=False, original_artifacts_modified=False,
        source_drift=False)
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source-root', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    args = p.parse_args()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=False)
    try:
        result = review(args.source_root.resolve(), out)
    except Exception:
        detail = traceback.format_exc()
        write_json(out / 'verification.json', dict(status='FAIL', traceback=detail))
        (out / 'run.log').write_text(detail)
        print(detail, file=sys.stderr)
        return 1
    write_json(out / 'verification.json', result)
    log = json.dumps(result, indent=2, sort_keys=True) + '\n'
    (out / 'run.log').write_text(log)
    print(log, end='')
    return 0


if __name__ == '__main__':
    sys.exit(main())
