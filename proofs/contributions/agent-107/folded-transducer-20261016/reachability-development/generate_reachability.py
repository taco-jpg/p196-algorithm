#!/usr/bin/env python3
"""Produce explicit BFS proof witnesses; Python discovery is checked by Lean."""
from collections import deque, Counter
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
TABLE_EVIDENCE=HERE.parent/'table-development'
DATA=TABLE_EVIDENCE/'extracted-tables.json'
record=json.loads(DATA.read_text())
states,edges=record['states'],record['edges']
assert record['counts']==dict(states=46,edges=872,terminals=251)
freeze=json.loads((TABLE_EVIDENCE/'source-freeze.json').read_text())['files']
for name in ['Agent107TransducerTablesData.lean','Agent107TransducerTablesChecks.lean','Agent107TransducerTables.lean']:
    path=REPO/'proofs'/name
    assert hashlib.sha256(path.read_bytes()).hexdigest()==freeze[str(path)], 'Table source changed: '+name

parents={0:None,1:None}
depth={0:0,1:0}
paths={0:[],1:[]}
roots={0:0,1:1}
todo=deque([0,1])
while todo:
    s=todo.popleft()
    for ei,(a,q,o,b) in enumerate(edges):
        if a==s and b not in parents:
            parents[b]=dict(parent=s,input=q,edge_index=ei)
            depth[b]=depth[s]+1
            paths[b]=paths[s]+[q]
            roots[b]=roots[s]
            todo.append(b)
assert set(parents)==set(range(46))
assert all(parents[i] is None or parents[i]['parent']<i for i in range(46))

lines=['import Agent107TransducerTables','',
       '/-! Exact finite-transition reachability of the original 46-state table.',
       'Every noninitial witness is an explicit prior witness and a kernel-decided Transition. -/','',
       'namespace Agent107.FoldedTransducer','',
       'inductive Reachable : State → Prop where',
       '  | initial (h : Nat) (bounded : h ≤ 1) : Reachable (initial h)',
       '  | step {s t : State} (q : Nat) (previous : Reachable s)',
       '      (transition : Transition s q t) : Reachable t','',
       'theorem reachable_mem_states {s : State} (h : Reachable s) : s ∈ Table.states := by',
       '  induction h with',
       '  | initial h hh => exact Table.starts_mem h hh',
       '  | @step s t q _ htrans ih => exact Table.states_closed s t q ih htrans','']
for i in range(46):
    lines += [f'theorem reachable_state{i} : Reachable Table.state{i} :=']
    if parents[i] is None:
        lines += [f'  Reachable.initial {i} (by decide)','']
    else:
        p=parents[i]
        lines += [f'  Reachable.step {p["input"]} reachable_state{p["parent"]} (by decide)','']
lines += ['theorem mem_states_reachable (s : State) (hs : s ∈ Table.states) : Reachable s := by',
          '  simp only [Table.states, List.mem_cons, List.mem_nil_iff, or_false] at hs',
          '  rcases hs with '+' | '.join('rfl' for _ in range(46))]
lines += [f'  · exact reachable_state{i}' for i in range(46)]
lines += ['', 'theorem reachable_iff_mem_states (s : State) : Reachable s ↔ s ∈ Table.states :=',
          '  ⟨reachable_mem_states, mem_states_reachable s⟩','']
names=['reachable_mem_states']+[f'reachable_state{i}' for i in range(46)]+['mem_states_reachable','reachable_iff_mem_states']
lines += ['#print axioms '+name for name in names]
lines += ['', 'end Agent107.FoldedTransducer','']
OUTPUT=REPO/'proofs/Agent107TransducerReachable.lean'
OUTPUT.write_text('\n'.join(lines))
witness=dict(input_table_sha256=hashlib.sha256(DATA.read_bytes()).hexdigest(),
             table_sources_sha256={str(p):h for p,h in freeze.items() if 'Tables' in p},
             states=[dict(index=i,state=states[i],root=roots[i],parent=parents[i],depth=depth[i],inputs=paths[i]) for i in range(46)],
             depth_counts=dict(Counter(depth.values())),
             generated_source_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
             generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(HERE/'bfs-witnesses.json').write_text(json.dumps(witness,indent=2)+'\n')
print(json.dumps(dict(states=len(parents),depth_counts=witness['depth_counts'],source_sha256=witness['generated_source_sha256'])))
