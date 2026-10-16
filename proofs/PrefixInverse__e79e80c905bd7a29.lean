import Std

/-!
Exact executable inverse transducers for a finite low-to-high prefix.
The unconstrained innermost carry makes these relations an overapproximation
of full words. No assertion of full-word realizability is made.
-/
namespace SevenColumn

def carry (a x : Nat) : Nat := (a + x) / 10

def lowDigit (a x : Nat) : Nat := (a + x) % 10

/-- Nonoverflow equations, with current low incoming and high outgoing carry. -/
inductive NoOverflow : List Nat → List Nat → Nat → Nat → Prop
  | nil (x y : Nat) : NoOverflow [] [] x y
  | cons {p s : List Nat} {v a x y z : Nat}
      (ha : a < 19) (hz : z < 2) (hy : carry a z = y)
      (hv : v = lowDigit a x + lowDigit a z)
      (tail : NoOverflow p s (carry a x) z) :
      NoOverflow (v :: p) (a :: s) x y

/-- Overflow equations after the outer column, carrying the previous source sum. -/
inductive OverflowTail : List Nat → List Nat → Nat → Nat → Nat → Prop
  | nil {a x y : Nat} (terminal : ∃ z, z < 2 ∧ carry a z = y) :
      OverflowTail [] [] a x y
  | cons {p s : List Nat} {v a prev x y z : Nat}
      (ha : a < 19) (hz : z < 2) (hy : carry prev z = y)
      (hv : v = lowDigit a x + lowDigit prev z)
      (tail : OverflowTail p s a (carry a x) z) :
      OverflowTail (v :: p) (a :: s) prev x y

/-- Either of the complete seven-column local recurrence branches.
The definition is width-independent and requires a positive exterior source sum. -/
inductive LongCompatible : List Nat → List Nat → Prop
  | noOverflow {p s : List Nat} {a : Nat}
      (positive : 0 < a) (equations : NoOverflow p (a :: s) 0 0) :
      LongCompatible p (a :: s)
  | overflow {p s : List Nat} {v a : Nat}
      (positive : 0 < a) (ha : a < 19)
      (outer : v = 1 + lowDigit a 0)
      (equations : OverflowTail p s a (carry a 0) 1) :
      LongCompatible (v :: p) (a :: s)

/-- Exhaust the 19 source sums and two high incoming carries at each column. -/
def noOverflowPred : List Nat → Nat → Nat → List (List Nat)
  | [], _, _ => [[]]
  | v :: p, x, y => (List.range 19).flatMap fun a =>
      (List.range 2).flatMap fun z =>
        if carry a z = y ∧ v = lowDigit a x + lowDigit a z then
          (noOverflowPred p (carry a x) z).map (a :: ·)
        else []

/-- Exhaust the shifted overflow equations; the final high column is checked. -/
def overflowTailPred : List Nat → Nat → Nat → Nat → List (List Nat)
  | [], a, _, y => if (List.range 2).any (fun z => carry a z == y) then [[]] else []
  | v :: p, prev, x, y => (List.range 19).flatMap fun a =>
      (List.range 2).flatMap fun z =>
        if carry prev z = y ∧ v = lowDigit a x + lowDigit prev z then
          (overflowTailPred p a (carry a x) z).map (a :: ·)
        else []

def overflowFirst (v : Nat) : Nat := if v ≤ 9 then v + 9 else 9

def overflowPred : List Nat → List (List Nat)
  | [] => []
  | v :: p => if v ≤ 10 then
      let a := overflowFirst v
      (overflowTailPred p a (carry a 0) 1).map (a :: ·)
    else []

def prefixPredecessors (p : List Nat) : List (List Nat) :=
  (noOverflowPred p 0 0).filter (fun s => 0 < s.headD 0) ++ overflowPred p

theorem NoOverflow.mem_noOverflowPred {p s : List Nat} {x y : Nat}
    (h : NoOverflow p s x y) : s ∈ noOverflowPred p x y := by
  induction h with
  | nil => simp [noOverflowPred]
  | @cons p s v a x y z ha hz hy hv tail ih =>
      simp only [noOverflowPred, List.mem_flatMap, List.mem_range]
      exact ⟨a, ha, z, hz, by simp [hy, hv, ih]⟩

theorem OverflowTail.mem_overflowTailPred {p s : List Nat} {a x y : Nat}
    (h : OverflowTail p s a x y) : s ∈ overflowTailPred p a x y := by
  induction h with
  | @nil a x y terminal =>
      rcases terminal with ⟨z, hz, hy⟩
      simp only [overflowTailPred]
      have hh : (List.range 2).any (fun z => carry a z == y) = true := by
        simp only [List.any_eq_true, List.mem_range, beq_iff_eq]
        exact ⟨z, hz, hy⟩
      simp [hh]
  | @cons p s v a prev x y z ha hz hy hv tail ih =>
      simp only [overflowTailPred, List.mem_flatMap, List.mem_range]
      exact ⟨a, ha, z, hz, by simp [hy, hv, ih]⟩

theorem OverflowTail.outer_carry {p s : List Nat} {a x y : Nat}
    (h : OverflowTail p s a x y) : ∃ z, z < 2 ∧ carry a z = y := by
  cases h with
  | nil terminal => exact terminal
  | cons ha hz hy hv tail => exact ⟨_, hz, hy⟩

theorem overflowFirst_eq {v a z : Nat} (ha : a < 19) (hz : z < 2)
    (hy : carry a z = 1) (hv : v = 1 + lowDigit a 0) :
    v ≤ 10 ∧ overflowFirst v = a := by
  simp only [carry, lowDigit, Nat.add_zero] at *
  unfold overflowFirst
  split <;> omega

theorem longCompatible_mem_prefixPredecessors {p s : List Nat}
    (h : LongCompatible p s) : s ∈ prefixPredecessors p := by
  cases h with
  | @noOverflow p s a positive equations =>
      apply List.mem_append_left
      simp only [List.mem_filter, List.headD_cons, decide_eq_true_eq]
      exact ⟨equations.mem_noOverflowPred, positive⟩
  | @overflow p s v a positive ha outer equations =>
      rcases equations.outer_carry with ⟨z, hz, hy⟩
      rcases overflowFirst_eq ha hz hy outer with ⟨hv, heq⟩
      apply List.mem_append_right
      simp [overflowPred, hv, heq, equations.mem_overflowTailPred]

#print axioms longCompatible_mem_prefixPredecessors
#print axioms overflowFirst_eq

end SevenColumn
