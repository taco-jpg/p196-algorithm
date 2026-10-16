#!/usr/bin/env python3
"""Compare literal outer catalog data/formulas, without running Lean."""
import argparse
import ast
import gzip
import hashlib
import json
from pathlib import Path
import re

parser=argparse.ArgumentParser()
parser.add_argument('--source-root',type=Path,required=True)
parser.add_argument('--output-dir',type=Path,required=True)
args=parser.parse_args()
root,out=args.source_root.resolve(),args.output_dir.resolve()
out.mkdir(parents=True,exist_ok=False)
archive=root/('proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/'
    'proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/outer_filtered_graph.json.gz')
compressed=archive.read_bytes()
assert hashlib.sha256(compressed).hexdigest()=='c3eb0a4bd4bc8e390d7681746e66300851035dff1b102412e2d14977ed1088e5'
graph=json.loads(gzip.decompress(compressed))
names=['Agent1PeriodicOuterCatalog.lean','Agent1PeriodicOuterChoices.lean']
sources={name:(root/'proofs'/name).read_bytes() for name in names}
for name,data in sources.items():
    (out/name).write_bytes(data)
catalog=sources[names[0]].decode()
choices=sources[names[1]].decode()
state_section=re.search(r'^def outerCatalog : List OuterNode := (\[.*?^\])',catalog,re.M|re.S)
edge_section=re.search(r'^def outerEdges : List OuterEdge := \[\n(.*?)^\]',catalog,re.M|re.S)
assert state_section and edge_section,'Literal outer data not found'
states=json.loads(json.dumps(ast.literal_eval(state_section[1])))
edges=[]
for line in edge_section[1].splitlines():
    match=re.fullmatch(r'\s*⟨(\(\[[0-9, ]+\],\s*[0-9]+\)), ([01]), (none|some \(([01]),([01])\)), (\(\[[0-9, ]+\],\s*[0-9]+\))⟩,?',line)
    assert match,('Unparsed edge',line)
    edge=dict(source=json.loads(json.dumps(ast.literal_eval(match[1]))),clock=int(match[2]),
              target=json.loads(json.dumps(ast.literal_eval(match[6]))))
    if match[3]!='none':
        edge.update(left_carry=int(match[4]),right_carry=int(match[5]))
    edges.append(edge)
expected_states=[row['source'] for row in graph['graph']]
expected_edges=[dict(source=row['source'],**edge) for row in graph['graph'] for edge in row['edges']]
assert states==expected_states,'Literal state list/order mismatch'
assert edges==expected_edges,'Literal labelled edge list/order mismatch'
expected_definitions={
 'outerImages': '''((List.range 2).filterMap (fun e =>
    if Agent8.overflow q e = g then some (Agent8.nextExterior q e) else none)).eraseDups''',
 'outerOutputs': '''(phaseEdges.filter (fun e => decide (e.source = s.1))).flatMap (fun e =>
    (outerImages s.2 e.clock).map (fun q' =>
      ⟨s, e.clock, e.carries, (e.target, q')⟩))''',
}
for name,expected in expected_definitions.items():
    match=re.search(r'^def '+name+r'[^\n]*:=\n(.*?)(?=\n\n)',choices,re.M|re.S)
    assert match,('Definition not found',name)
    assert ''.join(match[1].split())==''.join(expected.split()),('Formula changed',name)
assert all((root/'proofs'/name).read_bytes()==data for name,data in sources.items()),'Source drift'
result=dict(status='PASS',scope='Literal data/formula comparison only; not Lean acceptance',
    source_sha256={name:hashlib.sha256(data).hexdigest() for name,data in sources.items()},
    state_count=len(states),labelled_edge_count=len(edges),exact_order_and_labels_match=True,
    outerImages_definition_matches_reviewed_formula=True,
    outerOutputs_definition_matches_reviewed_formula=True,source_drift=False,lean_executed=False,
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(out/'verification.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
