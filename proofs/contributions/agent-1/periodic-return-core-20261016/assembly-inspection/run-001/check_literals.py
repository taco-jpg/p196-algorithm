from pathlib import Path
import re,json,hashlib,datetime
base=Path(__file__).resolve().parent
manifest={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Source-only adversarial assembly inspection of OuterRank and ReturnCore, with supporting contracts; no Lean invocation; excludes independent review of reviewer-authored ZeroPath.','files':{}}
for p in sorted((base/'source').iterdir()):
 b=p.read_bytes();manifest['files'][p.name]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
r=(base/'source/Agent1PeriodicOuterRank.lean').read_text();c=(base/'source/Agent1PeriodicOuterCatalog.lean').read_text()
def rows(body):return [re.sub(r'\s+','',x.rstrip().rstrip(',')) for x in body.splitlines() if x.strip()]
def block(s,name,kind):
 m=re.search(r'(?:private )?def '+name+r' : List '+kind+r' := \[(.*?)\n\]',s,re.S)
 assert m,name
 return rows(m.group(1))
rank_nodes=[];rank_edges=[];catalog=[];edges=[]
for i in range(59):
 n=str(i).zfill(2)
 rank_nodes.extend(block(r,'rankNodes'+n,'OuterNode'));rank_edges.extend(block(r,'rankEdges'+n,'OuterEdge'))
 catalog.extend(block(c,'outerNodes'+n,'OuterNode'));edges.extend(block(c,'outerEdges'+n,'OuterEdge'))
manifest['literal_snapshot_checks']={'phase_blocks':59,'node_count':len(rank_nodes),'edge_count':len(rank_edges),'node_order_exact_text_after_whitespace_comma_normalization':rank_nodes==catalog,'edge_order_and_all_fields_exact_text_after_whitespace_comma_normalization':rank_edges==edges,'nodeCheck_decl_count':len(re.findall(r'private theorem nodeCheck\d\d :',r)),'edgeCheck_decl_count':len(re.findall(r'private theorem edgeCheck\d\d :',r))}
assert rank_nodes==catalog and rank_edges==edges
(base/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
for name in ['Agent1PeriodicOuterRank.lean','Agent1PeriodicReturnCore.lean']:print(name,manifest['files'][name]['sha256'])
print(json.dumps(manifest['literal_snapshot_checks'],indent=2))
for name,patterns in [('Agent1PeriodicOuterRank.lean',['def outerComponent','def componentRank','private def edgeRankCheck','private def nodeLabelCheck','private theorem rankNodeBlocks_eq','private theorem rankEdgeBlocks_eq','theorem outerEdge_rank_drop','theorem outerEdge_internal_component','theorem outerComponent_zero_phase','theorem outerComponent_initial_core']),('Agent1PeriodicReturnCore.lean',['def returnCore','theorem quotient_return_component_constant','have hcert','have hinter','theorem quotient_return_core','have hnonzero','theorem quotient_return_initial_outside'])]:
 lines=(base/'source'/name).read_text().splitlines();print(name)
 for pat in patterns:print(pat,next(i+1 for i,line in enumerate(lines) if pat in line))
