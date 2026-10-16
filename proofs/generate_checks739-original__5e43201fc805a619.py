#!/usr/bin/env python3
"""Generate bounded kernel-decide row obligations and balanced assemblies.

Generation alone is NOT a checked certificate. Build logs and the final
AllRows739/Initial739 olean files are required evidence of completion.
"""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
layout=json.loads((HERE/'rank739-layout.json').read_text())
leaves=layout['leaves']
interiors=layout['interiors']
word=lambda w:'['+','.join(map(str,w))+']'
header='namespace SevenColumn.Certificate739\nopen Certificate\nset_option maxRecDepth 100000\nset_option maxHeartbeats 100000000\n'
predicate='fun p r => checkRow ranks (fastLongPred 7) p r = true'
modules=[]
for start in range(0,len(leaves),4):
    name=f'Rows739_{start//4:03d}'
    modules.append(name)
    source='import Rank739\nimport FastRowsBase\n'+header
    for leaf in leaves[start:start+4]:
        source+=f'theorem checked_{leaf["name"]} : {leaf["name"]}.All ({predicate}) := by decide\n'
    for branch in interiors[start:start+4]:
        n=branch['row']
        source+=f'theorem row_{branch["name"]} : checkRow ranks (fastLongPred 7) {word(n["word"])} {n["rank"]} = true := by decide\n'
    source+='end SevenColumn.Certificate739\n'
    (HERE/(name+'.lean')).write_text(source)

branches={n['name']:n for n in interiors}
def proof(name):
    if name.startswith('leaf'):
        return 'checked_'+name
    n=branches[name]
    return f'⟨{proof(n["left"])}, row_{name}, {proof(n["right"])}⟩'

assembly=''.join('import '+n+'\n' for n in modules)+header
assembly+=f'theorem allRowsFast : CheckedRows ranks (fastLongPred 7) :=\n  {proof(layout["root"])}\n'
assembly+='theorem allRows : CheckedRows ranks (longPred 7) := checkedRows_fast_to_long allRowsFast\n'
assembly+='#print axioms allRowsFast\n#print axioms allRows\nend SevenColumn.Certificate739\n'
(HERE/'AllRows739.lean').write_text(assembly)

for batch in range(10):
    source='import Rank739\nimport Initial739Base\n'+header
    for chunk in range(batch*10,(batch+1)*10):
        start=chunk*100
        source+=f'theorem initial_{chunk:03d} : ∀ i : Fin 100, checkInitial ranks 38 (initialWord ({start} + i.val)) = true := by decide\n'
    source+='end SevenColumn.Certificate739\n'
    (HERE/f'Initial739_{batch:02d}.lean').write_text(source)

def range_proof(lo,hi):
    pred='fun i => checkInitial ranks 38 (initialWord i) = true'
    if hi-lo==1:
        return f'(checked_range ({pred}) {lo*100} 100 initial_{lo:03d})'
    mid=(lo+hi)//2
    return f'(join_ranges ({pred}) {lo*100} {mid*100} {hi*100} {range_proof(lo,mid)} {range_proof(mid,hi)})'

source=''.join(f'import Initial739_{i:02d}\n' for i in range(10))+header
source+='theorem initialLongChecked : ∀ i, i < 10000 → checkInitial ranks 38 (initialWord i) = true := by\n'
source+=f'  intro i hi\n  exact {range_proof(0,100)} i (Nat.zero_le i) hi\n'
source+='theorem initialShortChecked : checkInitial ranks 38 [7,3,9,9,3,7] = true := by decide\n'
source+='theorem initialDigitsChecked {a b c d : Nat} (ha : a < 10) (hb : b < 10) (hc : c < 10) (hd : d < 10) : checkInitial ranks 38 [7,3,9,a,b,c,d] = true := by\n'
source+='  have h := initialLongChecked _ (initialWord_index_lt ha hb hc hd)\n  simpa only [initialWord_digits ha hb hc hd] using h\n'
source+='#print axioms initialLongChecked\n#print axioms initialDigitsChecked\n#print axioms initialShortChecked\nend SevenColumn.Certificate739\n'
(HERE/'Initial739.lean').write_text(source)
print(json.dumps({'row_modules':len(modules),'leaf_checks':len(leaves),'individual_branch_rows':len(interiors),'initial_blocks':100,'initial_block_size':100}))
