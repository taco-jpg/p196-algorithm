#!/usr/bin/env python3
"""Expand actual literal/append catalog definitions, without running Lean."""
import argparse
import ast
import gzip
import hashlib
import json
from pathlib import Path
import re


def parse_edges(body):
    edges=[]
    for line in body.splitlines():
        match=re.fullmatch(r'\s*⟨(\(\[[0-9, ]+\],\s*[0-9]+\)), ([01]), (none|some \(([01]),([01])\)), (\(\[[0-9, ]+\],\s*[0-9]+\))⟩,?',line)
        assert match,('Unparsed edge',line)
        edge=dict(source=json.loads(json.dumps(ast.literal_eval(match[1]))),clock=int(match[2]),
                  target=json.loads(json.dumps(ast.literal_eval(match[6]))))
        if match[3]!='none':
            edge.update(left_carry=int(match[4]),right_carry=int(match[5]))
        edges.append(edge)
    return edges


def parse_catalog(source):
    """Accept literal lists and explicit append chains only, preserving order."""
    node_matches=list(re.finditer(r'^(?:private )?def (\w+) : List OuterNode := (\[.*?^\])',source,re.M|re.S))
    edge_matches=list(re.finditer(r'^(?:private )?def (\w+) : List OuterEdge := \[\n(.*?)^\]',source,re.M|re.S))
    node_defs={m[1]:json.loads(json.dumps(ast.literal_eval(m[2]))) for m in node_matches}
    edge_defs={m[1]:parse_edges(m[2]) for m in edge_matches}
    assert len(node_defs)==len(node_matches),'Duplicate node declaration names'
    assert len(edge_defs)==len(edge_matches),'Duplicate edge declaration names'

    def expand(public_name,type_name,definitions):
        if public_name in definitions:
            assert set(definitions)=={public_name},'Unexpected unused literal definitions'
            return definitions[public_name],[public_name]
        declaration=re.search(r'^def '+public_name+r' : List '+type_name+r' :=\n(.*?)(?=\n\n)',source,re.M|re.S)
        assert declaration,('Public append definition missing',public_name)
        body=declaration[1].strip()
        assert re.fullmatch(r'\w+(?:\s*\+\+\s*\w+)*',body),('Unsupported append expression',body)
        references=re.split(r'\s*\+\+\s*',body)
        assert len(references)==len(set(references))==59,('Repeated/missing block',public_name)
        assert set(references)==set(definitions),('Undefined or unused block',public_name)
        return [item for name in references for item in definitions[name]],references

    states,node_refs=expand('outerCatalog','OuterNode',node_defs)
    edges,edge_refs=expand('outerEdges','OuterEdge',edge_defs)
    metadata=dict(node_append_order=node_refs,edge_append_order=edge_refs,
                  node_block_sizes=[len(node_defs[name]) for name in node_refs],
                  edge_block_sizes=[len(edge_defs[name]) for name in edge_refs])
    if len(node_refs)==59:
        assert len(edge_refs)==59
        phases=[]
        for node_name,edge_name in zip(node_refs,edge_refs):
            nodes,block_edges=node_defs[node_name],edge_defs[edge_name]
            assert nodes and block_edges,('Empty block',node_name,edge_name)
            phase=nodes[0][0]
            assert all(node[0]==phase for node in nodes),('Mixed node phase',node_name)
            assert all(edge['source'][0]==phase for edge in block_edges),('Wrong edge phase',edge_name)
            phases.append(phase)
        assert len({tuple(phase) for phase in phases})==59,'Repeated phase block'
        metadata['phase_block_order']=phases
        metadata['representation']='59 literal blocks in actual public append order'
    else:
        metadata['representation']='single literal node and edge lists'
    return states,edges,metadata


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
states,edges,expansion=parse_catalog(catalog)
expected_states=[row['source'] for row in graph['graph']]
expected_edges=[dict(source=row['source'],**edge) for row in graph['graph'] for edge in row['edges']]
assert states==expected_states,'Literal state list/order mismatch'
assert edges==expected_edges,'Literal labelled edge list/order mismatch'
baseline=Path(__file__).resolve().parent/'lean-data-001/Agent1PeriodicOuterCatalog.lean'
baseline_bytes=baseline.read_bytes()
baseline_sha=hashlib.sha256(baseline_bytes).hexdigest()
assert baseline_sha=='6fdd1a6850553ecd56fe4663be3f9f9541e5315a1f3b489c4c9fa782b4c017d4'
old_states,old_edges,_=parse_catalog(baseline_bytes.decode())
assert states==old_states and edges==old_edges,'Expanded arrays differ from original reviewed source'
(out/'append-expansion.json').write_text(json.dumps(expansion,indent=2,sort_keys=True)+'\n')
for name,data in [('expanded-states.json',states),('expanded-labelled-edges.json',edges)]:
    (out/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
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
    previous_reviewed_catalog_sha256=baseline_sha,
    exact_previous_snapshot_arrays_match=True,
    representation=expansion['representation'],
    node_block_count=len(expansion['node_append_order']),
    edge_block_count=len(expansion['edge_append_order']),
    actual_public_append_order_expanded=True,
    expanded_states_sha256=hashlib.sha256((out/'expanded-states.json').read_bytes()).hexdigest(),
    expanded_labelled_edges_sha256=hashlib.sha256((out/'expanded-labelled-edges.json').read_bytes()).hexdigest(),
    outerImages_definition_matches_reviewed_formula=True,
    outerOutputs_definition_matches_reviewed_formula=True,source_drift=False,lean_executed=False,
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(out/'verification.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
