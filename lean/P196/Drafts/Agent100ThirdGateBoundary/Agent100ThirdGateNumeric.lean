import P196.Drafts.Agent100ThirdGateBoundary.Agent100ThirdGateBoundary

/-!
The third proposed two-step overlap repair of the actual (1,1,6) family
fails at time six. The component and whole still have compatible widths,
but their outer coefficients are 14 and 15 respectively.
All pair-word comparisons use the actual represented finite prefix.
-/

namespace Agent100.ThirdGate

set_option maxHeartbeats 2000000
set_option maxRecDepth 10000

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

abbrev componentOrbit (r k : Nat) : Nat × (Nat → Nat) :=
  iterPairs (DelayedOverlapGate.component r 1 1 6) (2 * r + 6) k

abbrev wholeOrbit (r k : Nat) : Nat × (Nat → Nat) :=
  iterPairs (DoubleGate.initial r) (2 * r + 7) k

def spacerBit (r : Nat) : Nat := if r = 1 then 1 else 0

/-- Discard the irrelevant infinite function tail before forming an overlap. -/
def finiteWord (L : Nat) (q : Nat → Nat) (i : Nat) : Nat :=
  if i < L then q i else 0

theorem spacerBit_le_one (r : Nat) : spacerBit r ≤ 1 := by
  unfold spacerBit
  split <;> omega

theorem returned_component_front (r : Nat) (hr : 1 ≤ r) :
    GroupII.returnedComponent r 4 5 5 0 = 16 ∧
      GroupII.returnedComponent r 4 5 5 1 = spacerBit r := by
  constructor
  · simp [GroupII.returnedComponent]
  · by_cases he : r = 1
    · subst r
      decide
    · have hr2 : 2 ≤ r := by omega
      simp only [spacerBit, he, if_false, GroupII.returnedComponent]
      repeat (first | omega | split)

theorem returned_whole_front (r : Nat) (hr : 1 ≤ r) :
    GroupII.returned r 4 5 5 0 = 16 ∧
      GroupII.returned r 4 5 5 1 = 16 + spacerBit r := by
  constructor
  · simp [GroupII.returned, DelayedOverlapGate.shiftOne, GroupII.returnedComponent]
  · simpa [spacerBit] using GroupII.returned_first_neighbor r 4 5 5 hr

theorem component_four_front (r : Nat) (hr : 1 ≤ r) :
    (componentOrbit r 4).1 = 2 * r + 6 ∧
      (componentOrbit r 4).2 0 = 16 ∧
      (componentOrbit r 4).2 1 = spacerBit r := by
  have hf := DoubleGate.component_four_return r hr
  have he := returned_component_front r hr
  exact ⟨hf.1, (hf.2 0 (by omega)).trans he.1,
    (hf.2 1 (by omega)).trans he.2⟩

theorem whole_four_front (r : Nat) (hr : 1 ≤ r) :
    (wholeOrbit r 4).1 = 2 * r + 7 ∧
      (wholeOrbit r 4).2 0 = 16 ∧
      (wholeOrbit r 4).2 1 = 16 + spacerBit r := by
  have hf := DoubleGate.whole_four_return r hr
  have he := returned_whole_front r hr
  exact ⟨hf.1, (hf.2 0 (by omega)).trans he.1,
    (hf.2 1 (by omega)).trans he.2⟩

theorem component_six_boundary (r : Nat) (hr : 1 ≤ r) :
    (componentOrbit r 6).1 = 2 * r + 7 ∧
      (componentOrbit r 6).2 0 = 14 := by
  have hf := component_four_front r hr
  have ha := iterPairs_admissible (DelayedOverlapGate.component r 1 1 6)
    (2 * r + 6) 4
    (DelayedOverlapGate.component_admissible r 1 1 6 (DoubleGate.first_domain r hr))
  have haw : Admissible (2 * r + 6) (componentOrbit r 4).2 := by
    simpa only [hf.1] using ha
  have hg := two_steps_outer_fourteen (componentOrbit r 4).2
    (2 * r + 6) (spacerBit r) haw (by omega) hf.2.1 hf.2.2 (spacerBit_le_one r)
  unfold componentOrbit
  rw [DoubleGate.iterPairs_add _ _ 4 2, hf.1]
  exact hg

theorem whole_six_boundary (r : Nat) (hr : 1 ≤ r) :
    (wholeOrbit r 6).1 = 2 * r + 8 ∧
      (wholeOrbit r 6).2 0 = 15 := by
  have hf := whole_four_front r hr
  have ha := iterPairs_admissible (DoubleGate.initial r) (2 * r + 7) 4
    (DelayedOverlapGate.initial_admissible r 1 1 6 (DoubleGate.first_domain r hr))
  have haw : Admissible (2 * r + 7) (wholeOrbit r 4).2 := by
    simpa only [hf.1] using ha
  have hg := two_steps_outer_fifteen (wholeOrbit r 4).2
    (2 * r + 7) (spacerBit r) haw (by omega) hf.2.1 hf.2.2 (spacerBit_le_one r)
  unfold wholeOrbit
  rw [DoubleGate.iterPairs_add _ _ 4 2, hf.1]
  exact hg

/-- The comparison has the correct enlarged physical width. -/
theorem sixth_widths_compatible (r : Nat) (hr : 1 ≤ r) :
    (wholeOrbit r 6).1 = (componentOrbit r 6).1 + 1 := by
  rw [(whole_six_boundary r hr).1, (component_six_boundary r hr).1]

/-- The obstruction lies in the first valid column, not an undefined tail. -/
theorem third_overlap_fails (r : Nat) (hr : 1 ≤ r) :
    ¬ ∀ i, i < (wholeOrbit r 6).1 →
      (wholeOrbit r 6).2 i =
        DelayedOverlapGate.shiftOne
          (finiteWord (componentOrbit r 6).1 (componentOrbit r 6).2) i := by
  intro he
  have ha := component_six_boundary r hr
  have hq := whole_six_boundary r hr
  have hx := he 0 (by rw [hq.1]; omega)
  simp only [DelayedOverlapGate.shiftOne, finiteWord, ha.1, hq.2,
    Nat.zero_lt_succ, if_true, Nat.add_zero, ha.2] at hx
  omega

/-- Every ordinary integer realization has the same exact sixth pair boundary. -/
theorem numeric_six_boundary (n : Nat) (d : Nat → Nat) (r : Nat) (hr : 1 ≤ r)
    (hc : Canonical n d (2 * r + 7))
    (hq : ∀ i, i < 2 * r + 7 →
      columnSum d (2 * r + 7) i = DoubleGate.initial r i) :
    ∃ e, Canonical (orbit n 6) e (2 * r + 8) ∧
      columnSum e (2 * r + 8) 0 = 15 ∧
      (∀ i, i < 2 * r + 8 →
        columnSum e (2 * r + 8) i = (wholeOrbit r 6).2 i) := by
  obtain ⟨e, he, hrep⟩ := iterPairs_representation n d (DoubleGate.initial r)
    (2 * r + 7) 6 hc hq
  have hb := whole_six_boundary r hr
  change Canonical (orbit n 6) e (wholeOrbit r 6).1 at he
  change ∀ i, i < (wholeOrbit r 6).1 →
    columnSum e (wholeOrbit r 6).1 i = (wholeOrbit r 6).2 i at hrep
  rw [hb.1] at he hrep
  exact ⟨e, he, (hrep 0 (by omega)).trans hb.2, hrep⟩

theorem numeric_third_overlap_fails (n : Nat) (d : Nat → Nat) (r : Nat)
    (hr : 1 ≤ r) (hc : Canonical n d (2 * r + 7))
    (hq : ∀ i, i < 2 * r + 7 →
      columnSum d (2 * r + 7) i = DoubleGate.initial r i) :
    ∃ e, Canonical (orbit n 6) e (2 * r + 8) ∧
      ¬ ∀ i, i < 2 * r + 8 →
        columnSum e (2 * r + 8) i =
          DelayedOverlapGate.shiftOne
            (finiteWord (componentOrbit r 6).1 (componentOrbit r 6).2) i := by
  obtain ⟨e, he, _, hrep⟩ := numeric_six_boundary n d r hr hc hq
  refine ⟨e, he, ?_⟩
  intro hx
  apply third_overlap_fails r hr
  intro i hi
  have hib : i < 2 * r + 8 := by simpa only [(whole_six_boundary r hr).1] using hi
  exact (hrep i hib).symm.trans (hx i hib)

/-- No hypothetical certificate or unrealized symbolic seed remains. -/
theorem realized_six_boundary (r : Nat) (hr : 1 ≤ r) :
    ∃ n d, 0 < n ∧ Canonical n d (2 * r + 7) ∧
      (∀ i, i < 2 * r + 7 →
        columnSum d (2 * r + 7) i = DoubleGate.initial r i) ∧
      (∃ e, Canonical (orbit n 6) e (2 * r + 8) ∧
        columnSum e (2 * r + 8) 0 = 15) := by
  obtain ⟨n, d, hn, hc, hrep, _, _⟩ := DoubleGate.realized_safe_double_gate r hr
  obtain ⟨e, he, h0, _⟩ := numeric_six_boundary n d r hr hc hrep
  exact ⟨n, d, hn, hc, hrep, e, he, h0⟩

end Agent100.ThirdGate

#print axioms Agent100.ThirdGate.spacerBit_le_one
#print axioms Agent100.ThirdGate.returned_component_front
#print axioms Agent100.ThirdGate.returned_whole_front
#print axioms Agent100.ThirdGate.component_four_front
#print axioms Agent100.ThirdGate.whole_four_front
#print axioms Agent100.ThirdGate.component_six_boundary
#print axioms Agent100.ThirdGate.whole_six_boundary
#print axioms Agent100.ThirdGate.sixth_widths_compatible
#print axioms Agent100.ThirdGate.third_overlap_fails
#print axioms Agent100.ThirdGate.numeric_six_boundary
#print axioms Agent100.ThirdGate.numeric_third_overlap_fails
#print axioms Agent100.ThirdGate.realized_six_boundary
