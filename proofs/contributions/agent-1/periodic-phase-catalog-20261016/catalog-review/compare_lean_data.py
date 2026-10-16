#!/usr/bin/env python3
"""Compare literal Lean catalog data to the pinned archive, without Lean execution."""
import argparse
import ast
import gzip
import hashlib
import json
from pathlib import Path
import re

p = argparse.ArgumentParser()
p.add_argument('--source-root', type=Path, required=True)
p.add_argument('--output-dir', type=Path, required=True)
a = p.parse_args()
root, out = a.source_root.resolve(), a.output_dir.resolve()
out.mkdir(parents=True, exist_ok=False)
archive = root / ('proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/'
    'proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/bulk_phase_graph.json.gz')
compressed = archive.read_bytes()
assert hashlib.sha256(compressed).hexdigest() == 'a22b2e39e4b2ed31d00b0c69694cd25b29f63135cd2378a16e3a434781855bb2'
graph = json.loads(gzip.decompress(compressed))
catalog_path = root / 'proofs/Agent1PeriodicPhaseCatalog.lean'
phase_path = root / 'proofs/Agent1PeriodicPhase.lean'
catalog, phase = catalog_path.read_bytes(), phase_path.read_bytes()
(out / catalog_path.name).write_bytes(catalog)
(out / phase_path.name).write_bytes(phase)
text = catalog.decode()
catalog_block = re.search(r'^def phaseCatalog : List Word := (\[.*?^\])', text, re.M | re.S)
edge_block = re.search(r'^def phaseEdges : List PhaseEdge := \[\n(.*?)^\]', text, re.M | re.S)
assert catalog_block and edge_block, 'Literal definitions not found'
phases = ast.literal_eval(catalog_block.group(1))
edges = []
for line in edge_block.group(1).splitlines():
    m = re.fullmatch(r'\s*⟨(\[[0-9, ]+\]), ([01]), (none|some \(([01]),([01])\)), (\[[0-9, ]+\])⟩,?', line)
    assert m, ('Unparsed edge line', line)
    edge = dict(source=ast.literal_eval(m[1]), clock=int(m[2]), target=ast.literal_eval(m[6]))
    if m[3] != 'none':
        edge.update(left_carry=int(m[4]), right_carry=int(m[5]))
    edges.append(edge)
expected_phases = [row['source'] for row in graph['graph']]
expected_edges = [dict(source=row['source'], **edge) for row in graph['graph'] for edge in row['edges']]
assert phases == expected_phases, 'Literal phase list/order differs'
assert edges == expected_edges, 'Literal edge list/order/labels differs'
definition = re.search(r'^def phaseImage \(w : Word\) \(g : Nat\) : Word :=\n(.*?)(?=\n\n)',
    phase.decode(), re.M | re.S)
assert definition, 'phaseImage definition not found'
expected_definition = ('zipperPeriod (fixedDigits w (terminalCarry w 0)) '
    '(fixedDigits w.reverse (terminalCarry w.reverse 0)) g')
assert ''.join(definition[1].split()) == ''.join(expected_definition.split())
assert catalog_path.read_bytes() == catalog and phase_path.read_bytes() == phase, 'Source drift'
result = dict(status='PASS', scope='Literal source-data comparison; not Lean acceptance',
    phase_count=len(phases), labelled_edge_count=len(edges), exact_order_and_labels_match=True,
    phaseImage_definition_matches_reviewed_zipper=True,
    catalog_source_sha256=hashlib.sha256(catalog).hexdigest(),
    phase_source_sha256=hashlib.sha256(phase).hexdigest(), source_drift=False,
    lean_executed=False, script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(out / 'verification.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
print(json.dumps(result, indent=2, sort_keys=True))
