import P196.Foundations.LychrelDigitSums
import P196.Drafts.D20261014SevenStepFormalBoundaryTransducer.BoundaryTransducer

/-! Exact bridge from a whole admissible decimal pair word to its three
boundary columns. Controls are the actual carries of the whole word,
not freely chosen local values. No invariant family is assumed. -/

namespace ActualBoundary

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
open BoundaryTransducer

def boundary (q : Nat → Nat) : Prefix := ⟨q 0, q 1, q 2⟩

def actualControl (q : Nat → Nat) (L : Nat) : Bool :=
  decide (carry q (L - 3) = 1)

theorem actualControl_exact (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) :
    carry q (L - 3) = (actualControl q L).toNat := by
  have hb := carry_bounded q L ha.2.2.1 (L - 3) (by omega)
  by_cases hc : carry q (L - 3) = 1
  · simp [actualControl, hc]
  · have hz : carry q (L - 3) = 0 := by omega
    simp [actualControl, hz]

theorem actualControl_false_iff (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) :
    actualControl q L = false ↔ carry q (L - 3) = 0 := by
  have hb := carry_bounded q L ha.2.2.1 (L - 3) (by omega)
  simp only [actualControl, decide_eq_false_iff_not]
  omega

theorem actualControl_true_iff (q : Nat → Nat) (L : Nat) :
    actualControl q L = true ↔ carry q (L - 3) = 1 := by
  simp [actualControl]

theorem high_boundary_data (q : Nat → Nat) (L : Nat) (c : Bool)
    (hL : 6 ≤ L) (ha : Admissible L q)
    (hc : carry q (L - 3) = c.toNat) :
    output q (L - 3) = (q 2 + c.toNat) % 10 ∧
    output q (L - 2) = (q 1 + (q 2 + c.toNat) / 10) % 10 ∧
    output q (L - 1) = (q 0 + (q 1 + (q 2 + c.toNat) / 10) / 10) % 10 ∧
    carry q L = (q 0 + (q 1 + (q 2 + c.toNat) / 10) / 10) / 10 := by
  have hs0 : q (L - 1) = q 0 := by
    simpa only [Nat.sub_zero] using (ha.2.2.2.1 0 (by omega)).symm
  have hs1 : q (L - 2) = q 1 := by
    have he : L - 1 - 1 = L - 2 := by omega
    simpa only [he] using (ha.2.2.2.1 1 (by omega)).symm
  have hs2 : q (L - 3) = q 2 := by
    have he : L - 1 - 2 = L - 3 := by omega
    simpa only [he] using (ha.2.2.2.1 2 (by omega)).symm
  have hindex1 : L - 2 = (L - 3) + 1 := by omega
  have hindex2 : L - 1 = (L - 2) + 1 := by omega
  have hindex3 : L = (L - 1) + 1 := by omega
  have hk1 : carry q (L - 2) = (q 2 + c.toNat) / 10 := by
    rw [hindex1, carry, hs2, hc]
  have hk2 : carry q (L - 1) = (q 1 + (q 2 + c.toNat) / 10) / 10 := by
    rw [hindex2, carry, hs1, hk1]
  have hk3 : carry q L = (q 0 + (q 1 + (q 2 + c.toNat) / 10) / 10) / 10 := by
    calc
      carry q L = carry q ((L - 1) + 1) := congrArg (carry q) hindex3
      _ = _ := by rw [carry, hs0, hk2]
  exact ⟨by simp only [output, hs2, hc],
    by simp only [output, hs1, hk1],
    by simp only [output, hs0, hk2], hk3⟩

theorem low_boundary_data (q : Nat → Nat) :
    output q 0 = q 0 % 10 ∧
    output q 1 = (q 1 + q 0 / 10) % 10 ∧
    output q 2 = (q 2 + (q 1 + q 0 / 10) / 10) % 10 := by
  simp [output, carry]

/-- The finite transducer is exactly the actual next pair word's boundary,
including its real final carry. The input control is not independent. -/
theorem boundary_step_exact (q : Nat → Nat) (L : Nat) (c : Bool)
    (hL : 6 ≤ L) (ha : Admissible L q)
    (hc : carry q (L - 3) = c.toNat) :
    (boundary (nextColumns q L), carry q L) =
      BoundaryTransducer.step (boundary q) c := by
  obtain ⟨hh0, hh1, hh2, he⟩ := high_boundary_data q L c hL ha hc
  obtain ⟨hl0, hl1, hl2⟩ := low_boundary_data q
  simp only [BoundaryTransducer.step, boundary]
  simp only [← hl0, ← hl1, ← hl2, ← hh0, ← hh1, ← hh2, ← he]
  by_cases hz : carry q L = 0
  · simp only [hz, if_true, nextColumns, columnSum, reflected, Nat.sub_zero]
    have hi1 : L - 1 - 1 = L - 2 := by omega
    have hi2 : L - 1 - 2 = L - 3 := by omega
    simp only [hi1, hi2]
  · have hone : carry q L = 1 := by
      have hb := carry_bounded q L ha.2.2.1 L (Nat.le_refl L)
      omega
    simp only [hz, if_false, nextColumns, columnSum, reflected,
      Nat.add_sub_cancel, Nat.sub_zero, extended,
      show 0 < L by omega, show 1 < L by omega, show 2 < L by omega,
      show L - 1 < L by omega, show L - 2 < L by omega,
      Nat.lt_irrefl, if_true, if_false, hone]
    simp

theorem actual_boundary_step (q : Nat → Nat) (L : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) :
    (boundary (nextColumns q L), carry q L) =
      BoundaryTransducer.step (boundary q) (actualControl q L) :=
  boundary_step_exact q L (actualControl q L) hL ha (actualControl_exact q L ha)

end ActualBoundary
