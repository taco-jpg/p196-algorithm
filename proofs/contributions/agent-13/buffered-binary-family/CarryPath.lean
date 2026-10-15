import Indexing

namespace Agent13BufferedFamily
open DecimalDigits FoldedDecimal Agent13FoldedFamily

abbrev CarryState := Nat × Nat

def CarryEdge (p q : CarryState) (x s : Nat) : Prop :=
  q.1 = (x+p.1)/10 ∧ p.2 = (x+q.2)/10 ∧ (x+p.1)%10+(x+q.2)%10=s

/-- A finite compositional record of the original ordinary-addition equations.
It is not an abstract substitute for the actual folded map. -/
inductive CarryPath : CarryState → List Nat → List Nat → CarryState → Prop
  | nil (p : CarryState) : CarryPath p [] [] p
  | cons {p q z : CarryState} {x s : Nat} {H R : List Nat}
      (edge : CarryEdge p q x s) (tail : CarryPath q H R z) :
      CarryPath p (x::H) (s::R) z

theorem path_append {p q z : CarryState} {H R U V : List Nat}
    (hp : CarryPath p H R q) (hq : CarryPath q U V z) :
    CarryPath p (H++U) (R++V) z := by
  induction hp with
  | nil _ => exact hq
  | cons he ht ih => exact CarryPath.cons he (ih hq)

theorem path_lengths {p q : CarryState} {H R : List Nat} (hp : CarryPath p H R q) :
    H.length=R.length := by
  induction hp with
  | nil _ => rfl
  | cons he ht ih => simpa using ih

theorem path_repeat (p : CarryState) (x s n : Nat) (he : CarryEdge p p x s) :
    CarryPath p (List.replicate n x) (List.replicate n s) p := by
  induction n with
  | zero => exact CarryPath.nil p
  | succ n ih => exact CarryPath.cons he ih

/-- Every compositional path supplies all carry values, including both ends. -/
theorem path_trace {p q : CarryState} {H R : List Nat} (hp : CarryPath p H R q) :
    ∃ a b : Nat → Nat, a 0=p.1 ∧ b 0=p.2 ∧ a H.length=q.1 ∧ b H.length=q.2 ∧
      ∀ i, i < H.length →
        a (i+1)=(H.getD i 0+a i)/10 ∧
        b i=(H.getD i 0+b (i+1))/10 ∧
        (H.getD i 0+a i)%10+(H.getD i 0+b (i+1))%10=R.getD i 0 := by
  induction hp with
  | nil p =>
    exact ⟨fun _ => p.1,fun _ => p.2,rfl,rfl,rfl,rfl,fun i hi => by simp at hi⟩
  | @cons p q z x s H R he ht ih =>
    obtain ⟨a,b,ha0,hb0,haend,hbend,hedges⟩ := ih
    let a' : Nat → Nat := fun | 0 => p.1 | i+1 => a i
    let b' : Nat → Nat := fun | 0 => p.2 | i+1 => b i
    refine ⟨a',b',rfl,rfl,haend,hbend,?_⟩
    intro i hi
    cases i with
    | zero =>
      simpa only [a',b',List.getD_cons_zero,ha0,hb0] using he
    | succ i =>
      have hs := hedges i (by simpa using hi)
      simpa only [a',b',List.getD_cons_succ] using hs

/-- Center-closed paths have actual ordinary carries on their reflected word. -/
theorem path_actual_carries {H R : List Nat} {c : Nat}
    (hp : CarryPath (0,0) H R (c,c)) :
    ∃ a b : Nat → Nat,
      (∀ i, i ≤ H.length → a i = carry (reflectHalf (fun j => H.getD j 0) H.length) i) ∧
      (∀ i, i ≤ H.length → b i = carry (reflectHalf (fun j => H.getD j 0) H.length) (2*H.length-i)) ∧
      carry (reflectHalf (fun j => H.getD j 0) H.length) (2*H.length)=0 ∧
      ∀ i, i < H.length →
        (H.getD i 0+a i)%10+(H.getD i 0+b (i+1))%10=R.getD i 0 := by
  obtain ⟨a,b,ha0,hb0,haend,hbend,hedges⟩ := path_trace hp
  have h := even_folded_trace_sound
    (reflectHalf (fun j => H.getD j 0) H.length) a b H.length
    (reflect_symm _ _) ha0
    (fun i hi => by rw [reflect_low _ _ _ hi]; exact (hedges i hi).1)
    (fun i hi => by rw [reflect_low _ _ _ hi]; exact (hedges i hi).2.1)
    (haend.trans hbend.symm)
  exact ⟨a,b,h.1,h.2.1,h.2.2.symm.trans hb0,fun i hi => (hedges i hi).2.2⟩

/-- A full reflected transition follows from the closed ordinary carry path. -/
theorem path_actual_transition {H R : List Nat} {c : Nat}
    (hp : CarryPath (0,0) H R (c,c)) :
    nextWidth (reflectHalf (fun j => H.getD j 0) H.length) (2*H.length)=2*H.length ∧
    ∀ i, i < 2*H.length →
      nextColumns (reflectHalf (fun j => H.getD j 0) H.length) (2*H.length) i =
      reflectHalf (fun j => R.getD j 0) H.length i := by
  obtain ⟨a,b,ha,hb,hcarry,hem⟩ := path_actual_carries hp
  have hhalf : ∀ i, i < H.length →
      nextColumns (reflectHalf (fun j => H.getD j 0) H.length) (2*H.length) i = R.getD i 0 := by
    intro i hi
    rw [folded_emission_no_overflow _ _ _ (by omega) (reflect_symm _ _) hcarry,
      reflect_low _ _ _ hi, ← ha i (by omega)]
    have hr : 2*H.length-1-i=2*H.length-(i+1) := by omega
    rw [hr, ← hb (i+1) (by omega)]
    exact hem i hi
  refine ⟨by simp only [nextWidth,hcarry,if_true],?_⟩
  intro i hi
  by_cases hl : i < H.length
  · rw [hhalf i hl,reflect_low _ _ _ hl]
  · have hr : 2*H.length-1-i < H.length := by omega
    rw [nextColumns_symm_no_overflow _ _ _ hi hcarry,hhalf _ hr]
    simp [reflectHalf,hl]

end Agent13BufferedFamily
