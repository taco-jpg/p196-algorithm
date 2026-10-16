import Std
import ReverseClosure

/-!
Kernel-checked semantics of a rank/projection certificate for cyclic-word
languages. No finite certificate or external computation is trusted here.
-/

namespace Sofic

structure LEdge where
  src : Nat
  dst : Nat
  lab : Nat
  deriving DecidableEq, Repr, Inhabited

instance : BEq LEdge := ⟨fun a b => decide (a = b)⟩
instance : LawfulBEq LEdge where
  eq_of_beq := of_decide_eq_true
  rfl := by intro a; exact decide_eq_true rfl

abbrev Graph := List LEdge
abbrev Word := Nat → Nat
abbrev Node := LEdge × Nat

def Periodic (n : Nat) (w : Nat → α) : Prop := ∀ i, w (i+n) = w i

/-- A nonempty finite closed walk, extended periodically to natural indices. -/
def Accepts (g : Graph) (n : Nat) (w : Word) : Prop :=
  0 < n ∧ Periodic n w ∧ ∃ v : Nat → Nat,
    Periodic n v ∧ ∀ i, i < n → { src := v i, dst := v (i+1), lab := w i } ∈ g

/-- The exact cyclic local transducer relation, with the arrow pointing inward. -/
def Column (fiber : Nat → List Nat) (output : Nat → Nat → Option Nat)
    (n : Nat) (old new : Word) : Prop :=
  Periodic n old ∧ Periodic n new ∧ ∃ x : Nat → Nat,
    Periodic n x ∧ ∀ i, i < n →
      x i ∈ fiber (new i) ∧ output (x i) (x (i+1)) = some (old i)

def rawNodes (fiber : Nat → List Nat) (g : Graph) : List Node :=
  g.flatMap fun e => (fiber e.lab).map fun x => (e, x)

def Compatible (output : Nat → Nat → Option Nat) (a b : Node) (l : Nat) : Prop :=
  a.1.dst = b.1.src ∧ output a.2 b.2 = some l

/-- A finite, locally checkable projection; ranks may only increase on raw edges.
Every equal-rank edge must project to an edge of the destination graph. -/
def Projection (fiber : Nat → List Nat) (output : Nat → Nat → Option Nat)
    (g h : Graph) (rank project : Node → Nat) : Prop :=
  ∀ a ∈ rawNodes fiber g, ∀ b ∈ rawNodes fiber g, ∀ l,
    Compatible output a b l →
      rank a ≤ rank b ∧ (rank a = rank b →
        { src := project a, dst := project b, lab := l } ∈ h)

theorem cyclic_rank_equal {r : Nat → Nat} {n : Nat}
    (close : r n = r 0) (step : ∀ i, i < n → r i ≤ r (i+1)) :
    ∀ i, i < n → r i = r (i+1) := by
  have chain (a b : Nat) (hab : a ≤ b) (hbn : b ≤ n) : r a ≤ r b := by
    induction b generalizing a with
    | zero =>
      have : a = 0 := by omega
      subst a
      exact Nat.le_refl _
    | succ b ih =>
      by_cases heq : a = b+1
      · subst a
        exact Nat.le_refl _
      · exact Nat.le_trans (ih a (by omega) (by omega)) (step b (by omega))
  intro i hi
  apply Nat.le_antisymm (step i hi)
  have h₁ := chain (i+1) n (by omega) (Nat.le_refl _)
  have h₂ := chain 0 i (by omega) (by omega)
  rw [close] at h₁
  exact Nat.le_trans h₁ h₂

theorem projection_sound {fiber : Nat → List Nat} {output : Nat → Nat → Option Nat}
    {g h : Graph} {rank project : Node → Nat}
    (cert : Projection fiber output g h rank project)
    {n : Nat} {old new : Word}
    (accepted : Accepts g n new) (column : Column fiber output n old new) :
    Accepts h n old := by
  obtain ⟨hn, hnew, v, hvper, hv⟩ := accepted
  obtain ⟨hold, _, x, hxper, hx⟩ := column
  let nodes : Nat → Node := fun i =>
    ({ src := v i, dst := v (i+1), lab := new i }, x i)
  have nodesper : Periodic n nodes := by
    intro i
    have heq : i + n + 1 = (i+1) + n := by omega
    simp only [nodes, heq, hvper i, hvper (i+1), hnew i, hxper i]
  have nodesmem (i : Nat) (hi : i < n) : nodes i ∈ rawNodes fiber g := by
    apply List.mem_flatMap.mpr
    refine ⟨{src := v i, dst := v (i+1), lab := new i}, hv i hi, ?_⟩
    exact List.mem_map.mpr ⟨x i, (hx i hi).1, rfl⟩
  have nodesnext (i : Nat) (hi : i < n) : nodes (i+1) ∈ rawNodes fiber g := by
    by_cases hnext : i+1 < n
    · exact nodesmem (i+1) hnext
    · have heq : i+1 = n := by omega
      rw [heq, show nodes n = nodes 0 from by simpa using nodesper 0]
      exact nodesmem 0 hn
  have compatible (i : Nat) (hi : i < n) :
      Compatible output (nodes i) (nodes (i+1)) (old i) :=
    ⟨rfl, (hx i hi).2⟩
  have incr (i : Nat) (hi : i < n) : rank (nodes i) ≤ rank (nodes (i+1)) :=
    (cert _ (nodesmem i hi) _ (nodesnext i hi) _ (compatible i hi)).1
  have equal := cyclic_rank_equal
    (r := fun i => rank (nodes i))
    (show rank (nodes n) = rank (nodes 0) from by
      rw [show nodes n = nodes 0 from by simpa using nodesper 0]) incr
  refine ⟨hn, hold, (fun i => project (nodes i)), ?_, ?_⟩
  · intro i
    exact congrArg project (nodesper i)
  · intro i hi
    exact (cert _ (nodesmem i hi) _ (nodesnext i hi) _ (compatible i hi)).2 (equal i hi)

theorem excludes_uniform {g : Graph} {label n : Nat} {rank : Nat → Nat}
    (strict : ∀ e ∈ g, e.lab = label → rank e.src < rank e.dst) :
    ¬ Accepts g n (fun _ => label) := by
  rintro ⟨hn, _, v, hv, hedge⟩
  have hstep (i : Nat) (hi : i < n) : rank (v i) < rank (v (i+1)) :=
    strict _ (hedge i hi) rfl
  have heq := cyclic_rank_equal
    (r := fun i => rank (v i))
    (show rank (v n) = rank (v 0) from by rw [show v n = v 0 from by simpa using hv 0])
    (fun i hi => Nat.le_of_lt (hstep i hi))
  exact Nat.ne_of_lt (hstep 0 hn) (heq 0 hn)

def nodeIndex (nodes : List Node) (a : Node) : Nat := nodes.findIdx (fun b => b == a)

def rankFunction (fiber : Nat → List Nat) (g : Graph) (ranks : Array Nat) : Node → Nat :=
  let nodes := rawNodes fiber g
  fun a => ranks[nodeIndex nodes a]!

def checkProjection (fiber : Nat → List Nat) (output : Nat → Nat → Option Nat)
    (g h : Graph) (ranks maps : Array Nat) : Bool :=
  let rank := rankFunction fiber g ranks
  let project := rankFunction fiber g maps
  let data := (rawNodes fiber g).map fun a => (a, rank a, project a)
  data.all fun (a, ra, ma) => data.all fun (b, rb, mb) =>
    if a.1.dst == b.1.src then
      match output a.2 b.2 with
      | none => true
      | some l => ra ≤ rb && (ra != rb || h.contains {src := ma, dst := mb, lab := l})
    else true

theorem checkProjection_sound {fiber : Nat → List Nat} {output : Nat → Nat → Option Nat}
    {g h : Graph} {ranks maps : Array Nat}
    (checked : checkProjection fiber output g h ranks maps = true) :
    Projection fiber output g h (rankFunction fiber g ranks) (rankFunction fiber g maps) := by
  intro a ha b hb l hcomp
  simp only [checkProjection, List.all_eq_true] at checked
  have hlocal := checked (a, rankFunction fiber g ranks a, rankFunction fiber g maps a)
    (List.mem_map.mpr ⟨a, ha, rfl⟩)
    (b, rankFunction fiber g ranks b, rankFunction fiber g maps b)
    (List.mem_map.mpr ⟨b, hb, rfl⟩)
  simp only [hcomp.1, beq_self_eq_true, ↓reduceIte, hcomp.2] at hlocal
  have h' : rankFunction fiber g ranks a ≤ rankFunction fiber g ranks b ∧
      (rankFunction fiber g ranks a ≠ rankFunction fiber g ranks b ∨
        {src := rankFunction fiber g maps a, dst := rankFunction fiber g maps b, lab := l} ∈ h) := by
    simpa using hlocal
  exact ⟨h'.1, fun heq => h'.2.resolve_left (fun hne => hne heq)⟩

def checkRoot (g : Graph) (label : Nat) (ranks : Array Nat) : Bool :=
  g.all fun e => e.lab != label || ranks[e.src]! < ranks[e.dst]!

theorem checkRoot_sound {g : Graph} {label : Nat} {ranks : Array Nat}
    (checked : checkRoot g label ranks = true) (n : Nat) :
    ¬ Accepts g n (fun _ => label) := by
  apply excludes_uniform (rank := fun i => ranks[i]!)
  intro e he hl
  have := List.all_eq_true.mp checked e he
  simpa [hl] using this

#print axioms projection_sound
#print axioms excludes_uniform
#print axioms checkProjection_sound
#print axioms checkRoot_sound

end Sofic
