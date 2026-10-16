#!/usr/bin/env python3
"""Post hoc reconstruction, NOT a source snapshot retained at execution time."""
import ast
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
SCRIPT=HERE/'generate_tables.py'
tree=ast.parse(SCRIPT.read_text())
cut=next(i for i,n in enumerate(tree.body) if isinstance(n,ast.Assign)
         and any(isinstance(t,ast.Name) and t.id=='cut1' for t in n.targets))
nodes=[]
for node in tree.body[:cut]:
    # Execute the retained data/line construction only, suppressing its earlier JSON write.
    if isinstance(node,ast.Expr) and isinstance(node.value,ast.Call) and isinstance(node.value.func,ast.Attribute) and node.value.func.attr=='write_text':
        continue
    nodes.append(node)
ns={'__file__':str(SCRIPT),'__name__':'__reconstruction__'}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SCRIPT),'exec'),ns)
lines=ns['lines'][:]
for i in range(46):
    j=lines.index(f'theorem row{i}_separated : edges{i}.Nodup ∧ ∀ e ∈ edges{i}, e.source = state{i} := by decide')
    assert lines[j+1]==f'theorem terminal_row{i}_separated : terminals{i}.Nodup ∧ ∀ r ∈ terminals{i}, r.source = state{i} := by decide'
    assert lines[j+2]==''
    del lines[j:j+3]
j=lines.index('theorem states_nodup : states.Nodup := by decide')+1
lines[j:j]=['theorem edges_nodup : edges.Nodup := by decide','theorem terminals_nodup : terminals.Nodup := by decide']
a=lines.index('theorem edge_mem_iff (s t : State) (q o : Nat) :')
b=lines.index('#print axioms states_nodup')
del lines[a:b]
lines.remove('#print axioms edge_mem_iff')
lines.remove('#print axioms terminal_mem_iff')
data='\n'.join(lines).encode()
attempt=json.loads((HERE/'attempt-01.json').read_text())
actual=hashlib.sha256(data).hexdigest()
assert actual==attempt['source_sha256'], 'Reconstructed bytes do not match original execution record.'
(HERE/'attempt-01-source.lean').write_bytes(data)
record=dict(provenance='Post hoc deterministic reconstruction. The temporary source used in the failed run was overwritten by the later split-module build; no contemporaneous source snapshot was retained.',
            original_execution_record='attempt-01.json',original_exit_code=attempt['exit_code'],
            expected_source_sha256=attempt['source_sha256'],reconstructed_source_sha256=actual,
            byte_hash_matches_original_record=True,
            retained_generator='generate_tables.py',retained_generator_sha256=hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
            reconstruction_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            transformations=['Run retained original table/aggregate-line construction without its writes and before module splitting.',
              'Remove later per-row separated lemmas and their separating blank lines.',
              'Restore original whole-list edges_nodup and terminals_nodup decide declarations.',
              'Remove later edge_mem_iff/terminal_mem_iff declarations and their axiom-print commands.',
              'Join with the original newline convention and require exact SHA-256 equality before saving.'])
(HERE/'attempt-01-reconstruction.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False,indent=2))
