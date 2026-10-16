from pathlib import Path
import re,ast,json,hashlib
root=Path(__file__).resolve().parents[5];base=Path(__file__).resolve().parent
old=(base/'attempt-001/Agent1PeriodicOuterCatalog.lean').read_text()
ntext=old.split('def outerCatalog : List OuterNode := [\n')[1].split('\n]')[0]
etext=old.split('def outerEdges : List OuterEdge := [\n')[1].split('\n]')[0]
nlines=ntext.splitlines();elines=etext.splitlines()
phase=lambda l:tuple(ast.literal_eval(re.search(r'\[[0-9,]+\]',l).group()))
phases=list(dict.fromkeys(map(phase,nlines)));assert len(phases)==59
ng=[[l.strip().rstrip(',') for l in nlines if phase(l)==p]for p in phases]
eg=[[l.strip().rstrip(',') for l in elines if phase(l)==p]for p in phases]
assert [x for g in ng for x in g]==[l.strip().rstrip(',') for l in nlines]
assert [x for g in eg for x in g]==[l.strip().rstrip(',') for l in elines]
parts=['import Agent1PeriodicOuter\nimport Agent1PeriodicCatalogOrder\n\n/-! Exact original product certificate, split into phase blocks for kernel checking.\nNo label, ordering, node or edge changes. Arbitrary paths are not realized. -/\nset_option maxRecDepth 16384\nset_option maxHeartbeats 16000000\nnamespace Agent1.Periodic\nopen Agent8\n']
for i,(ns,es)in enumerate(zip(ng,eg)):
 parts.append(f'private def outerNodes{i:02d} : List OuterNode := [\n  '+',\n  '.join(ns)+'\n]\n')
 parts.append(f'private def outerEdges{i:02d} : List OuterEdge := [\n  '+',\n  '.join(es)+'\n]\n')
 parts.append(f'private theorem outerBlockSpec{i:02d} : outerEdges{i:02d} = outerNodes{i:02d}.flatMap outerOutputs := by rfl\n')
parts.append('def outerCatalog : List OuterNode :=\n  '+' ++\n  '.join(f'outerNodes{i:02d}'for i in range(59))+'\n')
parts.append('def outerEdges : List OuterEdge :=\n  '+' ++\n  '.join(f'outerEdges{i:02d}'for i in range(59))+'\n')
parts.append('/-- Exact retained ordered edges, assembled from independently checked small blocks. -/\ntheorem outerEdges_spec : outerEdges = outerCatalog.flatMap outerOutputs := by\n  simp only [outerCatalog, outerEdges, List.flatMap_append,\n    '+',\n    '.join('← outerBlockSpec%02d'%i for i in range(59))+']\n')
parts.append('theorem outerCatalog_length : outerCatalog.length = 878 := by decide\ntheorem outerCatalog_nodup : outerCatalog.Nodup := by\n  exact outerCatalog_nodup_of_checked outerCatalog (by decide)\ntheorem outerEdges_length : outerEdges.length = 1458 := by decide\n')
parts.append('theorem outerCatalog_initial : ∀ p : Fin 19, 0 < p.val →\n    ([14,14,4,4],p.val) ∈ outerCatalog := by decide\n')
for i in range(59):
 parts.append(f'private theorem outerBlockPhases{i:02d} :\n    outerNodes{i:02d}.all (fun s => decide (s.1 ∈ phaseCatalog)) = true := by decide\n')
 parts.append(f'private theorem outerBlockTargets{i:02d} :\n    outerEdges{i:02d}.all (fun e => decide (e.target ∈ outerCatalog)) = true := by decide\n')
for name,what,fun,lem in [('outerCatalog_phases_checked','outerCatalog','fun s => decide (s.1 ∈ phaseCatalog)','outerBlockPhases'),('outerEdges_targets_checked','outerEdges','fun e => decide (e.target ∈ outerCatalog)','outerBlockTargets')]:
 parts.append(f'theorem {name} :\n    {what}.all ({fun}) = true := by\n  simp only [{what}, List.all_append, '+', '.join(lem+'%02d'%i for i in range(59))+', Bool.and_self]\n')
parts.append('theorem outerCatalog_phase_mem'+old.split('theorem outerCatalog_phase_mem',1)[1])
source='\n'.join(parts);(root/'proofs/Agent1PeriodicOuterCatalog.lean').write_text(source)
receipt={'original_snapshot_sha256':hashlib.sha256(old.encode()).hexdigest(),'new_source_sha256':hashlib.sha256(source.encode()).hexdigest(),'method':'Exact consecutive phase grouping, literal node and edge order asserted byte-for-byte unchanged after whitespace/comma normalization. Internal spec by rfl, target/phase checks by ordinary decide, Nodup via proved adjacent-key checker.','phase_blocks':59,'nodes':sum(map(len,ng)),'edges':sum(map(len,eg)),'node_block_sizes':list(map(len,ng)),'edge_block_sizes':list(map(len,eg))}
(base/'chunk-generation.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt)
