import ResidualFiveThirdWidth

/-!
# The preceding addition must overflow

This is the residual-five specialization of the original generic outer-pair
obstruction. All predecessors are ordinary positive decimal integers through
their original canonical representations. No bound on further ancestry follows.
-/

set_option autoImplicit false

namespace Agent103.ResidualFiveFourthOverflow

open Lychrel196 DecimalDigits FoldedDecimal
open Agent103.ResidualFiveFibers Agent103.ResidualFiveThirdWidth
open DecimalPrefixObstruction SevenColumnKernel.PalindromeBridge

/-- Any earlier canonical predecessor of a third-layer source must add a digit.
The two source widths are quantified freely and determined by the actual steps. -/
theorem earlier_width_and_overflow (r n z y L K : Nat) (d e : Nat → Nat)
    (hn : n ∈ fiber r) (hzn : step z = n) (hyz : step y = z)
    (hd : Canonical z d L) (he : Canonical y e K) :
    K + 1 = 2 * r + 4 ∧ carry (columnSum e K) K = 1 := by
  obtain ⟨hL, _, hq0, _⟩ := predecessor_width_and_source r n z L d hn hzn hd
  let q := columnSum e K
  have ha : Admissible K q := NormalizationBridge.canonical_admissible y e K he
  obtain ⟨f, hf, hrep⟩ := representation_next y e q K he (fun _ _ => rfl)
  rw [hyz] at hf
  obtain ⟨hw, hagree⟩ := canonical_columns_agree z f d (nextWidth q K) L hf hd
  have hi : 0 < nextWidth q K := hf.1
  have houter : nextColumns q K 0 = 1 :=
    (hrep 0 hi).symm.trans ((hagree 0 hi).trans hq0)
  have hb := carry_bounded q K ha.2.2.1 K (Nat.le_refl K)
  have hc : carry q K = 1 := by
    by_cases hz : carry q K = 0
    · have hge := no_overflow_outer_ge_two q K ha hz
      omega
    · omega
  have hwidth : K + 1 = L := by
    simpa only [nextWidth, hc, show ¬ (1 : Nat) = 0 by decide, ite_false] using hw
  exact ⟨hwidth.trans hL, hc⟩

/-- The ordinary positive-integer formulation supplies the source representation;
the width and terminal carry are conclusions, with no digit-width premise. -/
theorem positive_earlier_predecessor (r n z y : Nat)
    (hn : n ∈ fiber r) (hz : 0 < z) (hy : 0 < y)
    (hzn : step z = n) (hyz : step y = z) :
    ∃ e, Canonical y e (2 * r + 3) ∧
      carry (columnSum e (2 * r + 3)) (2 * r + 3) = 1 := by
  obtain ⟨d, L, hd⟩ := canonical_exists z hz
  obtain ⟨e, K, he⟩ := canonical_exists y hy
  obtain ⟨hw, hc⟩ := earlier_width_and_overflow r n z y L K d e hn hzn hyz hd he
  have hK : K = 2 * r + 3 := by omega
  refine ⟨e, ?_, ?_⟩
  · simpa only [hK] using he
  · simpa only [hK] using hc

#print axioms earlier_width_and_overflow
#print axioms positive_earlier_predecessor

end Agent103.ResidualFiveFourthOverflow
