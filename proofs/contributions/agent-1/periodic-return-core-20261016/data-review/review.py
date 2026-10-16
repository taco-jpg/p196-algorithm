#!/usr/bin/env python3
"""Check the stored partition's local rank conditions; do not discover SCCs."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import platform
import sys
import traceback

ARCHIVE=('proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/'
         'proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/')
PINS={
 ARCHIVE+'outer_filtered_graph.json.gz':
  ('c3eb0a4bd4bc8e390d7681746e66300851035dff1b102412e2d14977ed1088e5',
   'c7bcc931f3cb36bd6845abeade0f7fd7b9723e08'),
 'proofs/Agent1PeriodicCatalogOrder.lean':
  ('0f59e74ecb35b9bb648150319beb3de9f7965c6a1aea7171e67a40f4bcb199c7',None),
 'proofs/CondensationBound__7ecf1469405ab8d0.lean':
  ('04bb2ec87115a532ca91d5d0d453c0062f6c46f030c1fe072ee649db000a0ef8',
   '6130c4c54acb9bf9f6f00932084eed66e3b45980'),
}

def sha(data):
 return hashlib.sha256(data).hexdigest()

def git_blob(data):
 return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def save(path,data):
 path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

def node_id(state):
 return tuple(state[0]),state[1]

def catalog_key(state):
 acc=0
 for d in state[0]: acc=19*acc+d
 return 19*acc+state[1]

def review(root,out):
 inputs={}
 provenance=[]
 for path,(expected_sha,expected_blob) in PINS.items():
  data=(root/path).read_bytes()
  assert sha(data)==expected_sha,('Input hash mismatch',path)
  assert expected_blob is None or git_blob(data)==expected_blob,('Input blob mismatch',path)
  inputs[path]=data
  provenance.append(dict(path=path,sha256=sha(data),git_blob=git_blob(data),bytes=len(data)))
 save(out/'provenance.json',provenance)
 raw=gzip.decompress(inputs[ARCHIVE+'outer_filtered_graph.json.gz'])
 assert sha(raw)=='cbd5c62ac2af58d0d0ce1cbb6f0cf9199ac49c75291d062179caf15f96e1ad50'
 graph=json.loads(raw)
 components=graph['components']
 records=graph['graph']
 assert len(components)==132 and len(records)==878
 label={}
 for index,component in enumerate(components):
  assert component,('Empty component',index)
  for state in component:
   key=node_id(state)
   assert key not in label,('Repeated component member',index,state)
   label[key]=index
 catalog=[row['source'] for row in records]
 assert len({node_id(s) for s in catalog})==878
 assert set(label)=={node_id(s) for s in catalog}
 assert dict(Counter(map(len,components)))=={1:128,18:3,696:1}
 assert len(components[8])==696
 assert all(len(set(w))>1 for w,p in components[8])
 assert len({tuple(w) for w,p in components[8]})==56
 for index,value in [(129,9),(130,18),(131,0)]:
  assert components[index]==[[[value]*4,p] for p in range(1,19)],('Constant component mismatch',index)

 checks=[]
 internal=Counter()
 cross=Counter()
 for row_index,row in enumerate(records):
  source=row['source']; a=label[node_id(source)]
  for edge_index,edge in enumerate(row['edges']):
   target=edge['target']
   assert node_id(target) in label,('Unknown target',row_index,edge_index)
   b=label[node_id(target)]
   source_rank,target_rank=132-a,132-b
   detail=dict(row_index=row_index,edge_index=edge_index,source=source,edge=edge,
    source_component=a,target_component=b,source_rank=source_rank,target_rank=target_rank)
   assert 1<=source_rank<=132 and 1<=target_rank<=132,detail
   assert a<=b and target_rank<=source_rank,detail
   if a==b:
    assert a in (8,129,130,131),detail
    internal[a]+=1
   else:
    assert a<b and target_rank+1<=source_rank,detail
    cross[(a,b)]+=1
   checks.append(detail)
 assert len(checks)==1458
 assert set(internal)=={8,129,130,131}
 save(out/'edge-rank-checks.json',checks)
 save(out/'component-transitions.json',[
  dict(source_component=a,target_component=b,edge_count=count)
  for (a,b),count in sorted(cross.items())])
 save(out/'components.json',components)

 node_table=[dict(catalog_index=i,node=state,key=catalog_key(state),component=label[node_id(state)],
                  rank=132-label[node_id(state)]) for i,state in enumerate(catalog)]
 assert all(a['key']<b['key'] for a,b in zip(node_table,node_table[1:]))
 save(out/'node-component-table.json',node_table)
 save(out/'component-by-catalog-index.json',[r['component'] for r in node_table])
 save(out/'key-component-table.json',[[r['key'],r['component']] for r in node_table])
 phase_order=list(dict.fromkeys(tuple(state[0]) for state in catalog))
 assert len(phase_order)==59
 save(out/'phase-component-table.json',[
  dict(phase=list(phase),component_by_outside=[label.get((phase,p)) for p in range(19)])
  for phase in phase_order])
 overrides=[r for r in node_table if r['component'] not in (8,129,130,131)]
 assert len(overrides)==128
 save(out/'transient-overrides.json',overrides)

 expected_initial=[[[14,14,4,4],p] for p in range(1,19)]
 assert graph['initial']==expected_initial
 initial=[]
 for state in expected_initial:
  p=state[1];c=label[node_id(state)]
  expected=129-p if p<=8 else (8 if p<=10 else 18-p)
  assert c==expected,(state,c,expected)
  initial.append(dict(node=state,component=c,rank=132-c,
                      has_internal_edge=c in internal,in_nonzero_return_core=c in (8,129,130)))
 survivors=[r['node'][1] for r in initial if r['in_nonzero_return_core']]
 assert survivors==[9,10]
 save(out/'initial-classification.json',initial)
 summaries=[dict(component=i,size=len(c),rank=132-i,
                  internal_edge_count=internal[i],nonzero_return_core=i in (8,129,130))
            for i,c in enumerate(components)]
 save(out/'component-summary.json',summaries)
 assert all((root/path).read_bytes()==data for path,data in inputs.items())
 return dict(status='PASS',scope='Stored-partition/local-rank diagnostic; not SCC discovery or Lean acceptance',
  claim_commit='efe6d4b95f53ad8fbcebf113f8da0616dfa67b22',
  script_sha256=sha(Path(__file__).read_bytes()),python_version=platform.python_version(),
  graph_gzip_sha256=sha(inputs[ARCHIVE+'outer_filtered_graph.json.gz']),graph_payload_sha256=sha(raw),
  nodes=878,edges=1458,stored_components=132,partition_exact_and_disjoint=True,
  component_index_orientation='source <= target',rank_formula='132 - component_index',
  rank_range=[1,132],weight_one_le_rank_every_node=True,
  every_edge_rank_nonincreasing=True,every_cross_component_edge_rank_drop_at_least_one=True,
  internal_edge_components=sorted(internal),internal_edge_counts=dict(internal),
  cross_component_edges=sum(cross.values()),internal_edges=sum(internal.values()),
  component_8_nonconstant_nodes=696,component_8_distinct_phases=56,
  component_129='exactly ([9,9,9,9],p), p=1..18',
  component_130='exactly ([18,18,18,18],p), p=1..18',
  component_131='exactly ([0,0,0,0],p), p=1..18',
  initial_phase_nonzero_core_surviving_outside=survivors,nonzero_return_core_nodes=732,
  singleton_components_without_internal_edges=128,source_drift=False,
  fresh_graph_search=False,scc_algorithm_executed=False,reachability_or_minimality_claimed=False,
  lean_executed=False,original_artifacts_modified=False)

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--source-root',type=Path,required=True)
 parser.add_argument('--output-dir',type=Path,required=True)
 args=parser.parse_args();out=args.output_dir.resolve()
 out.mkdir(parents=True,exist_ok=False)
 try:result=review(args.source_root.resolve(),out)
 except Exception:
  detail=traceback.format_exc();save(out/'verification.json',dict(status='FAIL',traceback=detail))
  (out/'run.log').write_text(detail);print(detail,file=sys.stderr);return 1
 save(out/'verification.json',result)
 log=json.dumps(result,indent=2,sort_keys=True)+'\n';(out/'run.log').write_text(log);print(log,end='')
 return 0

if __name__=='__main__':sys.exit(main())
