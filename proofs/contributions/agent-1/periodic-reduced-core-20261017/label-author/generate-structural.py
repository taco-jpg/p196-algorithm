from pathlib import Path
import re,hashlib,json
here=Path(__file__).resolve().parent
repo=here.parents[4]
original=repo/'proofs/Agent1PeriodicOuterRank.lean'
text=original.read_text().split('/-- Reverse the stored indices;')[0]
patterns=[tuple(map(int,s.split(','))) for s in re.findall(r'^  \| \[([0-9,]+)\] =>',text,re.M)]
assert len(patterns)==31 and len(set(patterns))==31 and all(len(x)==4 for x in patterns)
lines=['import Agent1PeriodicOuterRank','', '/-!', 'The preserved total component-label definition assigns label130 only to', 'the constant-eighteen phase. The proof follows its existing constructor', 'and digit decisions directly; no graph rows or catalog premise are used.', '-/', '', 'set_option maxHeartbeats 1600000', '', 'namespace Agent1.Periodic', '', 'theorem outerComponent_eighteen_phase (s : OuterNode)', '    (hc : outerComponent s = 130) : s.1 = [18,18,18,18] := by', '  rcases s with ⟨w, a⟩', '  delta outerComponent outerComponent.match_9 at hc']
def emit(n,s):lines.append(' '*n+s)
def walk(n,prefix,pats,tail):
 depth=len(prefix)
 emit(n,f'cases {tail} with')
 if depth==4:
  emit(n,'| nil =>')
  emit(n+4,'dsimp only at hc')
  if prefix==(18,18,18,18):emit(n+4,'rfl')
  elif prefix in [(0,0,0,0),(9,9,9,9)]:emit(n+4,'contradiction')
  else:emit(n+4,'split at hc <;> contradiction')
  emit(n,'| cons _ _ =>')
  emit(n+4,'dsimp only at hc')
  emit(n+4,'contradiction')
  return
 emit(n,'| nil =>')
 emit(n+4,'dsimp only at hc')
 emit(n+4,'contradiction')
 var=f'x{depth}';newtail=f'tail{depth}'
 emit(n,f'| cons {var} {newtail} =>')
 emit(n+4,'dsimp only at hc')
 children=list(dict.fromkeys(x[depth] for x in pats))
 def children_go(n,items):
  if not items:emit(n,'contradiction');return
  v=items[0];h=f'h{depth}_{v}'
  emit(n,f'by_cases {h} : {var} = {v}')
  emit(n,f'· rw [dif_pos {h}] at hc')
  emit(n+2,f'subst {var}')
  emit(n+2,'dsimp only at hc')
  walk(n+2,prefix+(v,),[x for x in pats if x[depth]==v],newtail)
  emit(n,f'· rw [dif_neg {h}] at hc')
  children_go(n+2,items[1:])
 children_go(n+4,children)
walk(2,(),patterns,'w')
lines+=['','end Agent1.Periodic','','#print axioms Agent1.Periodic.outerComponent_eighteen_phase','']
out=repo/'proofs/Agent1PeriodicEighteenLabel.lean';out.write_text('\n'.join(lines))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(here/'structural-generation.json').write_text(json.dumps({'generator':str(Path(__file__).relative_to(repo)),'input':str(original.relative_to(repo)),'input_sha256':sha(original),'phase_pattern_count':len(patterns),'output':str(out.relative_to(repo)),'output_sha256':sha(out),'method':'Constructor/digit case script following existing total definition; no graph-row evaluation or new finite certificate.'},indent=2)+'\n')
print('Generated',len(lines),'lines',sha(out))
