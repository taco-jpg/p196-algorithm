from pathlib import Path
p=Path(__file__).resolve().parent
links={0:[(0,1)],1:[(52,2)],2:[(234,3),(278,4)],4:[(173,5)],5:[(459,6)],6:[(3079,7)],7:[(5241,8)],8:[(9643,9)],9:[(10716,10)],10:[(860,11)],11:[(3350,12),(4628,15)],12:[(3239,13)],13:[(10589,14)]}
s=''.join(f'import JobChecks{i}\n'for i in range(16))+'import ActualJobFamily\n\nnamespace ScalarHierarchy\nopen ScalarFinite ScalarJobData ActualPrefixLift\nset_option maxHeartbeats 0\n\ninductive Job where\n'+''.join(f'  | j{i}\n'for i in range(16))+'  deriving DecidableEq\n\n'
for name,typ,expr in [('data','Data',lambda i:f'data{i}'),('ranking','Ranking',lambda i:f'ranking{i}'),('width','Nat',lambda i:f'jobWidth {i}'),('bound','Nat',lambda i:f'jobBound {i}')]:
 s+=f'def {name} : Job → {typ}\n'+''.join(f'  | .j{i} => {expr(i)}\n'for i in range(16))+'\n'
s+='def child : Job → Nat → Job\n'
for i in range(16):s+=f'  | .j{i}, c => '+''.join(f'if c={c} then .j{j} else 'for c,j in links.get(i,[]))+'.j0\n'
s+='\ndef encode : Job → Nat → Nat × Fin 19 → Nat\n'
for i in range(16):s+=f'  | .j{i}, c => '+''.join(f'if c={c} then ScalarFinite.encode lift_certificate{j} else 'for c,j in links.get(i,[]))+'fun _ => 0\n'
s+='''
def graph (j : Job) := ScalarFinite.graph (data j)
def component (j : Job) := (ranking j).component
def cyclic (j : Job) := (ranking j).cyclic
def rank (j : Job) := (ranking j).rank
def height (j : Job) := 14-width j

theorem checked (j : Job) : CheckedRank (data j) (ranking j) := by
  cases j
'''+''.join(f'  · exact checked_rank{i}\n'for i in range(16))
def branches(i, success, fallback, k=0, indent=4):
 ls=links.get(i,[])
 if k==len(ls):return ' '*indent+fallback+'\n'
 c,ch=ls[k]
 return (' '*indent+f'by_cases h{k} : c={c}\n'+' '*indent+'· subst c\n'+
         '\n'.join(' '*(indent+2)+l for l in success(ch).split('\n'))+'\n'+
         ' '*indent+'· '+branches(i,success,fallback,k+1,indent+2).lstrip())
s+="\ntheorem weight_eq (j : Job) (c : Nat) :\n    ComponentHierarchy.jobWeight cyclic child bound j c = (ranking j).weight c := by\n  cases j\n"
for i in range(16):
 fb=f'simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking{i}, childCode{i}, child'+''.join(f', h{k}'for k in range(len(links.get(i,[]))))+']'
 s+='  · '+branches(i,lambda _: 'decide',fb).lstrip()
for theorem,statement in [
 ('height_decreases','height (child j c) < height j'),
 ('width_valid','1 ≤ width j ∧ width j < L ∧ width (child j c) = width j + 1'),
 ('realizes','Realization (BoundedPrefixLift.bounded (ActualPrefixLift.lift (ActualPrefixLift.select (graph j) (fun v => component j v=c)))) (graph (child j c)) (encode j c)')]:
 params='(L : Nat) (hL : 14 ≤ L) 'if theorem=='width_valid' else ''
 s+=f'\ntheorem {theorem} {params}(j : Job) (c : Nat) (hc : cyclic j c=true) :\n    {statement} := by\n  cases j\n'
 for i in range(16):
  fb=f'simp [cyclic, ranking, ranking{i}, childCode{i}'+''.join(f', h{k}'for k in range(len(links.get(i,[]))))+'] at hc'
  def success(ch):
   if theorem=='realizes':return f'exact lift_complete{ch}'
   if theorem=='height_decreases':return 'decide'
   return 'dsimp [width, child, jobWidth, widths]\nomega'
  s+='  · '+branches(i,success,fb).lstrip()
s+="""
theorem bound_eq (j : Job) : (ranking j).bound = bound j := by
  cases j <;> rfl

theorem vertex_bounds (j : Job) (v : Nat) (hv : (graph j).valid v) :
    ComponentHierarchy.jobWeight cyclic child bound j (component j v) ≤ rank j (component j v) ∧
    rank j (component j v) ≤ bound j := by
  rw [weight_eq, ← bound_eq]
  exact checked_vertex_bounds (checked j) v hv

theorem edge_bounds (j : Job) (u v bit : Nat)
    (hu : (graph j).valid u) (hv : (graph j).valid v)
    (_hb : bit ≤ 1) (he : (graph j).edge u v bit) :
    (cyclic j (component j u)=false → component j u ≠ component j v) ∧
    (component j u ≠ component j v →
      ComponentHierarchy.jobWeight cyclic child bound j (component j u)+rank j (component j v) ≤
      rank j (component j u)) := by
  rw [weight_eq]
  exact checked_edge_bounds (checked j) u v bit hu hv he

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

theorem finite_root_bound (q : Nat → Nat) (L a s n : Nat) (path : Nat → Nat)
    (ha : Admissible L q) (hL : 14 ≤ L)
    (hp : ActualPath (ScalarFinite.graph data0) q L 1 a s path n) : n ≤ 659 := by
  exact ActualJobFamily.actual_path_vertices_le graph width component cyclic child encode
    height bound rank q L ha height_decreases (width_valid L hL) realizes
    vertex_bounds edge_bounds Job.j0 a s path n hp

end ScalarHierarchy
"""
# Keep structural arithmetic independent of the lengthy row-check modules.
start=s.index('def encode :');end=s.index('def graph ', start)
enc=s[start:end];s=s[:start]+s[end:]
start=s.index('theorem checked ');end=s.index('theorem weight_eq ', start)
checked=s[start:end];s=s[:start]+s[end:]
start=s.index('theorem realizes ');end=s.index('theorem bound_eq ', start)
realizes=s[start:end];s=s[:start]+s[end:]
start=s.index('theorem vertex_bounds ')
endpoints=s[start:];s=s[:start]+'end ScalarHierarchy\n'
s=s.replace('import JobChecks','import JobData')
(p/'ScalarHierarchyData.lean').write_text(s)
final='import ScalarHierarchyData\n'+''.join(f'import JobChecks{i}\n'for i in range(16))
final+='namespace ScalarHierarchy\nopen ScalarFinite ScalarJobData ActualPrefixLift\nset_option maxHeartbeats 0\n\n'
(p/'ScalarHierarchy.lean').write_text(final+enc+checked+realizes+endpoints)

