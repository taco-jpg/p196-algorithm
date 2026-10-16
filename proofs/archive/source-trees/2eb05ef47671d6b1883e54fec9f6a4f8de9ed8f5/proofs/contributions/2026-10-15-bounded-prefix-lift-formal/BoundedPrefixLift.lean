import ActualPrefixLift

/-! The stored finite graphs use bit labels. The unrestricted semantic
graph admits other labels, so finite table transport must explicitly restrict
to bits. Every actual path satisfies that restriction. -/

namespace BoundedPrefixLift

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory ActualPrefixLift

def bounded {V : Type} (G : Graph V) : Graph V :=
  { G with edge := fun u v c => c ≤ 1 ∧ G.edge u v c }

theorem actual_label_bound (q : Nat → Nat) (L k a i : Nat)
    (ha : Admissible L q) : label q L k a i ≤ 1 := by
  have had := state_admissible q L a i ha
  exact carry_bounded (state q L a i).2 (state q L a i).1 had.2.2.1
    ((state q L a i).1 - k) (by omega)

theorem actual_path_bounded {V : Type} (G : Graph V) (q : Nat → Nat)
    (L k a s n : Nat) (path : Nat → V) (ha : Admissible L q)
    (hp : ActualPath G q L k a s path n) :
    ActualPath (bounded G) q L k a s path n := by
  refine ⟨hp.clock, hp.vertices, ?_⟩
  intro i hi
  exact ⟨actual_label_bound q L k a i ha, hp.edges i hi⟩

theorem actual_path_unbounded {V : Type} (G : Graph V) (q : Nat → Nat)
    (L k a s n : Nat) (path : Nat → V)
    (hp : ActualPath (bounded G) q L k a s path n) :
    ActualPath G q L k a s path n :=
  ⟨hp.clock, hp.vertices, fun i hi => (hp.edges i hi).2⟩

/-- Actual-path transport needs completeness only for the two bit labels. -/
theorem actual_path_encode {V W : Type} (G : Graph V) (H : Graph W)
    (encode : V → W) (hr : Realization (bounded G) H encode)
    (q : Nat → Nat) (L k a s n : Nat) (path : Nat → V)
    (ha : Admissible L q) (hp : ActualPath G q L k a s path n) :
    ActualPath H q L k a s (fun i => encode (path i)) n :=
  ActualPrefixLift.actual_path_encode (bounded G) H encode hr q L k a s n path
    (actual_path_bounded G q L k a s n path ha hp)

/-- Component intervals lift into the exact bit-labeled source needed by
the finite certificate. Both endpoints and all parent projections survive. -/
theorem actual_component_interval_lifts {V C : Type} (G : Graph V)
    (component : V → C) (c : C) (q : Nat → Nat) (L k a s n start length : Nat)
    (path : Nat → V) (ha : Admissible L q) (hk0 : 1 ≤ k) (hk : k < L)
    (hp : ActualPath G q L k a s path n) (hr : start + length ≤ n)
    (hc : ∀ i, i < length → component (path (start + i)) = c) :
    ∃ lifted, ActualPath (bounded (lift (select G (fun v => component v = c))))
      q L (k + 1) (a + start) (s + start) lifted length ∧
      ∀ i, (lifted i).1 = path (start + i) := by
  obtain ⟨lifted, hp, hprojection⟩ := ActualPrefixLift.actual_component_interval_lifts
    G component c q L k a s n start length path ha hk0 hk hp hr hc
  exact ⟨lifted, actual_path_bounded _ q L (k + 1) (a + start) (s + start)
    length lifted ha hp, hprojection⟩

end BoundedPrefixLift
