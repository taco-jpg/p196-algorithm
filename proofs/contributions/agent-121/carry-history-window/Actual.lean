import Targets
import Budget

namespace Agent121.CarryWindow
open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

/-- Exact exterior projection of a finite pair-sum word. -/
def project (q : Nat → Nat) (L : Nat) : State :=
  if L = 1 then ⟨true, q 0, 0⟩ else ⟨false, q 0, q 1⟩

def innerControl (q : Nat → Nat) (L : Nat) : Nat :=
  if L = 1 then 0 else carry q (L-2)

theorem actual_control_bound (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    innerControl q L ≤ 1 := by
  unfold innerControl
  split
  · omega
  · exact carry_bounded q L ha.2.2.1 (L-2) (by omega)

/-- Symmetry identifies both high-side carries from the two exterior
pair sums and a single actual interior carry. -/
theorem wide_carries (q : Nat → Nat) (L : Nat) (ha : Admissible L q)
    (hL : 2 ≤ L) :
    carry q 1 = q 0 / 10 ∧
    carry q (L-1) = (q 1 + carry q (L-2)) / 10 ∧
    carry q L = (q 0 + (q 1 + carry q (L-2)) / 10) / 10 := by
  have hs0 : q (L-1) = q 0 := by
    have h := ha.2.2.2.1 0 (by omega)
    simpa only [Nat.sub_zero] using h.symm
  have hs1 : q (L-2) = q 1 := by
    have h := ha.2.2.2.1 1 (by omega)
    have hi : L-1-1 = L-2 := by omega
    simpa only [hi] using h.symm
  have hlow : carry q 1 = q 0 / 10 := by simp [carry]
  have hhigh : carry q (L-1) = (q 1 + carry q (L-2)) / 10 := by
    calc
      carry q (L-1) = carry q ((L-2)+1) := by congr 1; omega
      _ = (q (L-2) + carry q (L-2)) / 10 := rfl
      _ = (q 1 + carry q (L-2)) / 10 := by rw [hs1]
  refine ⟨hlow, hhigh, ?_⟩
  calc
    carry q L = carry q ((L-1)+1) := by congr 1; omega
    _ = (q (L-1) + carry q (L-1)) / 10 := rfl
    _ = (q 0 + (q 1 + carry q (L-2)) / 10) / 10 := by rw [hs0, hhigh]

theorem actual_boundary (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    boundaryCarry (project q L) (innerControl q L) = carry q L := by
  by_cases hL : L = 1
  · subst L
    simp [project, innerControl, boundaryCarry, carry]
  · have hw : 2 ≤ L := by have := ha.1; omega
    have h := (wide_carries q L ha hw).2.2
    simpa only [project, innerControl, hL, if_false, boundaryCarry,
      Bool.false_eq_true, if_false] using h.symm

theorem projection_mem_states (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    project q L ∈ states := by
  have h0 := ha.2.1
  have hb0 := ha.2.2.1 0 ha.1
  by_cases hL : L = 1
  · simp only [project, hL, if_true]
    apply mem_states
    · exact h0
    · exact hb0
    · decide
    · intro _; rfl
  · have hw : 1 < L := by have := ha.1; omega
    have hb1 := ha.2.2.1 1 hw
    simp only [project, hL, if_false]
    apply mem_states
    · exact h0
    · exact hb0
    · exact hb1
    · intro h; cases h

/-- The abstract successor agrees with the actual pair map, including
width one and width two. Free inner bits are used only as an overapproximation. -/
theorem actual_projection (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    project (nextColumns q L) (nextWidth q L) =
      nextState (project q L) (innerControl q L) := by
  by_cases hsingle : L = 1
  · subst L
    have hb := ha.2.2.1 0 (by omega)
    have hcf : carry q 1 = q 0 / 10 := by simp [carry]
    by_cases hz : q 0 / 10 = 0
    · have hcarry : carry q 1 = 0 := by rw [hcf, hz]
      simp [project, innerControl, nextState, boundaryCarry, nextWidth,
        nextColumns, hcarry, hz, columnSum, reflected, output, carry, Nat.two_mul]
    · have ho : q 0 / 10 = 1 := by omega
      have hcarry : carry q 1 = 1 := by rw [hcf, ho]
      simp [project, innerControl, nextState, boundaryCarry, nextWidth,
        nextColumns, hcarry, ho, columnSum, reflected, extended, output, carry,
        Nat.add_comm]
  · have hL : 2 ≤ L := by have := ha.1; omega
    have hpos : 0 < L := by omega
    have hinner : 1 < L := by omega
    have hlast : L-1 < L := by omega
    have hs0 : q (L-1) = q 0 := by
      have h := ha.2.2.2.1 0 hpos
      simpa only [Nat.sub_zero] using h.symm
    have hs1 : q (L-2) = q 1 := by
      have h := ha.2.2.2.1 1 hinner
      have hi : L-1-1 = L-2 := by omega
      simpa only [hi] using h.symm
    obtain ⟨hlo, hhi, hfinal⟩ := wide_carries q L ha hL
    have hout0 : output q 0 = q 0 % 10 := by simp [output, carry]
    have hout1 : output q 1 = (q 1 + q 0 / 10) % 10 := by rw [output, hlo]
    have houtLast : output q (L-1) =
        (q 0 + (q 1 + carry q (L-2)) / 10) % 10 := by rw [output, hs0, hhi]
    have houtBefore : output q (L-2) = (q 1 + carry q (L-2)) % 10 := by
      rw [output, hs1]
    have hnextWide : nextWidth q L ≠ 1 := by
      unfold nextWidth
      split <;> omega
    have hpnext : project (nextColumns q L) (nextWidth q L) =
        ⟨false, nextColumns q L 0, nextColumns q L 1⟩ := by
      simp only [project, hnextWide, if_false]
    rw [hpnext]
    simp only [project, innerControl, hsingle, if_false]
    by_cases hz : carry q L = 0
    · have hcol0 : nextColumns q L 0 = output q 0 + output q (L-1) := by
        simp only [nextColumns, hz, if_true, columnSum, reflected, Nat.sub_zero]
      have hcol1 : nextColumns q L 1 = output q 1 + output q (L-2) := by
        simp only [nextColumns, hz, if_true, columnSum, reflected]
        have hi : L-1-1 = L-2 := by omega
        rw [hi]
      rw [hcol0, hcol1]
      simp [nextState, boundaryCarry, ← hfinal, hz,
        hout0, hout1, houtLast, houtBefore]
    · have hb := carry_bounded q L ha.2.2.1 L (by omega)
      have ho : carry q L = 1 := by omega
      have hcol0 : nextColumns q L 0 = output q 0 + 1 := by
        simp [nextColumns, ho, columnSum, reflected, extended, hpos]
      have hcol1 : nextColumns q L 1 = output q 1 + output q (L-1) := by
        simp [nextColumns, ho, columnSum, reflected, extended, hinner, hlast]
      rw [hcol0, hcol1]
      simp [nextState, boundaryCarry, ← hfinal, ho, hout0, hout1, houtLast]

/-- The finite lower-bound calculation bounds the count on every actual
arbitrary-width orbit; no symbolic realizability assumption is required. -/
theorem actual_budget (q : Nat → Nat) (L K : Nat) (ha : Admissible L q) :
    budget K (project q L) ≤
      noOverflowCount (fun t => (iterPairs q L t).2)
        (fun t => (iterPairs q L t).1) K := by
  apply budget_le_path_cost
    (fun t => project (iterPairs q L t).2 (iterPairs q L t).1)
    (fun t => innerControl (iterPairs q L t).2 (iterPairs q L t).1)
    (noOverflowCount (fun t => (iterPairs q L t).2)
      (fun t => (iterPairs q L t).1)) K
  · intro t
    exact actual_control_bound _ _ (iterPairs_admissible q L t ha)
  · intro t
    exact actual_projection _ _ (iterPairs_admissible q L t ha)
  · intro t
    simp only [noOverflowCount, stepCost,
      actual_boundary _ _ (iterPairs_admissible q L t ha)]
  · rfl

theorem nine_steps_four_nonoverflows (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) :
    4 ≤ noOverflowCount (fun t => (iterPairs q L t).2)
      (fun t => (iterPairs q L t).1) 9 := by
  exact Nat.le_trans (checked_nine_budget _ (projection_mem_states q L ha))
    (actual_budget q L 9 ha)

/-- Ten complete carry words determine the initial pair sums at any width. -/
theorem ten_carry_words_determine_pair_sums : ReconstructionWindow 10 := by
  intro q r L hq hr hc
  apply iterPairs_endpoint_carry_history_injective q r L 9 hq hr
  · intro t ht i hi
    exact hc t (by omega) i hi
  · exact nine_steps_four_nonoverflows q L hq

#print axioms actual_control_bound
#print axioms wide_carries
#print axioms actual_boundary
#print axioms projection_mem_states
#print axioms actual_projection
#print axioms actual_budget
#print axioms nine_steps_four_nonoverflows
#print axioms ten_carry_words_determine_pair_sums
end Agent121.CarryWindow
