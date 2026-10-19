import P196.OddPredecessorTargetCensus.Integration

/-!
# Cumulative enumeration of targets with odd predecessor count

Agent #6: append the exact census at each positive decimal width.
Uniqueness of ordinary decimal width makes the successive lists disjoint.
This module preserves the complete positive predecessor semantics and
establishes the strict numerical cutoff for the cumulative enumeration.
-/

set_option autoImplicit false

namespace OddPredecessorTargetSparsity

open DecimalDigits Agent101 Agent105Predecessors9df76b
open OddPredecessorTargetCensus

/-- Every target with odd complete predecessor count below `10^W`,
enumerated by its ordinary decimal width. -/
def belowPower : Nat → List Nat
  | 0 => []
  | W + 1 => belowPower W ++ targets (W + 1)

private theorem mem_belowPower_iff_target (W Y : Nat) :
    Y ∈ belowPower W ↔ ∃ K, K ≤ W ∧ Y ∈ targets K := by
  induction W with
  | zero =>
    constructor
    · intro h
      exact False.elim (List.not_mem_nil h)
    · rintro ⟨K, hK, hY⟩
      have hzero : K = 0 := by omega
      subst K
      exact False.elim (List.not_mem_nil hY)
  | succ W ih =>
    rw [belowPower, List.mem_append, ih]
    constructor
    · rintro (⟨K, hK, hY⟩ | hY)
      · exact ⟨K, by omega, hY⟩
      · exact ⟨W + 1, Nat.le_refl _, hY⟩
    · rintro ⟨K, hK, hY⟩
      by_cases hsmall : K ≤ W
      · exact Or.inl ⟨K, hsmall, hY⟩
      · have hlast : K = W + 1 := by omega
        exact Or.inr (by simpa only [hlast] using hY)

/-- Every numerical target appears once across all included widths. -/
theorem belowPower_nodup (W : Nat) : (belowPower W).Nodup := by
  induction W with
  | zero => simp only [belowPower, List.nodup_nil]
  | succ W ih =>
    rw [belowPower]
    apply List.pairwise_append.mpr
    refine ⟨ih, targets_nodup (W + 1), ?_⟩
    intro Y hY Z hZ hYZ
    subst Z
    obtain ⟨K, hK, hYK⟩ := (mem_belowPower_iff_target W Y).mp hY
    have hwidth := decimalWidth_unique Y K (W + 1)
      (targets_have_width K Y hYK) (targets_have_width (W + 1) Y hZ)
    omega

/-- For any canonical target, cumulative membership is exactly the width
cutoff together with odd cardinality of its complete positive predecessor list. -/
theorem mem_belowPower (Y : Nat) (e : Nat → Nat) (K W : Nat)
    (hY : Canonical Y e K) :
    Y ∈ belowPower W ↔
      K ≤ W ∧ (predecessors e K).length % 2 = 1 := by
  rw [mem_belowPower_iff_target]
  constructor
  · rintro ⟨L, hL, hYL⟩
    have hLK := decimalWidth_unique Y L K
      (targets_have_width L Y hYL) (canonical_decimalWidth Y e K hY)
    subst L
    exact ⟨hL, (mem_targets Y e K hY).mp hYL⟩
  · rintro ⟨hK, ho⟩
    exact ⟨K, hK, (mem_targets Y e K hY).mpr ho⟩

/-- The cumulative enumeration contains only positive integers strictly
below the corresponding power of ten, including the empty width-zero case. -/
theorem belowPower_bounds (W Y : Nat) (h : Y ∈ belowPower W) :
    0 < Y ∧ Y < 10 ^ W := by
  obtain ⟨K, hK, hY⟩ := (mem_belowPower_iff_target W Y).mp h
  have hw := targets_have_width K Y hY
  exact ⟨Nat.lt_of_lt_of_le (Nat.pow_pos (by decide : 0 < 10)) hw.2.1,
    Nat.lt_of_lt_of_le hw.2.2 (Nat.pow_le_pow_right (by decide : 0 < 10) hK)⟩

end OddPredecessorTargetSparsity

#print axioms OddPredecessorTargetSparsity.belowPower
#print axioms OddPredecessorTargetSparsity.belowPower_nodup
#print axioms OddPredecessorTargetSparsity.mem_belowPower
#print axioms OddPredecessorTargetSparsity.belowPower_bounds
