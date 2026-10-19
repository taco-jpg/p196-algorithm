import P196.SharpOddTargetSparsity.Counts
import P196.SharpOddTargetSparsity.Scaling
import P196.SharpOddTargetSparsity.SmallCutoffs

/-!
# The sharp integer constant for the complete odd-target census

Agent #6: combine the finite leading-block bounds with the exact
cumulative census at every decimal width. Nine works at every exclusive
cutoff, and the complete finite count below two hundred thousand proves
that every smaller integer constant fails.
-/

set_option autoImplicit false

namespace SharpOddTargetSparsity

open DecimalDigits DecimalQuantitativeMass Agent101
open OddPredecessorTargetSparsity

/-- The square of the complete odd-predecessor target count below any
exclusive numerical cutoff is at most nine times that cutoff. -/
theorem below_quadratic_nine (N : Nat) : (below N).length ^ 2 ≤ 9 * N := by
  by_cases hN : N ≤ 1
  · rw [below_eq_nil_small N hN]
    simp
  · let W := decimalLength (N - 1)
    have hd : decimalLength (N - 1) = W := rfl
    by_cases hW : W ≤ 3
    · obtain ⟨d, L, hc⟩ := canonical_exists (N - 1) (by omega)
      have hL := decimalLength_of_canonical (N - 1) d L hc
      have hw := canonical_decimalWidth (N - 1) d L hc
      have hp := Nat.pow_le_pow_right (by decide : 0 < 10) (show L ≤ 3 by omega)
      have hupper := hw.2.2
      have hsmall : N ≤ 1000 := by
        have hthousand : (10 : Nat) ^ 3 = 1000 := by decide
        rw [hthousand] at hp
        omega
      simpa only [below, hd] using small_count_bound W N hW hsmall
    · have hwide : 4 ≤ W := by omega
      obtain ⟨a, ha, ha', hlo, hhi⟩ := cutoff_interval N W (by omega) (by omega) hd
      rcases Nat.mod_two_eq_zero_or_one (W - 4) with heven | hodd
      · let k := (W - 4) / 2
        have hindex : W = 2 * k + 4 := by dsimp [k]; omega
        have hbound := below_even_envelope k N a (hd.trans hindex) ha ha'
          (by simpa only [hindex, show 2 * k + 4 - 2 = 2 * k + 2 by omega] using hhi)
        apply scale_envelope_bound (below N).length (evenEnvelope a) k 2 a N hbound
        · have h := evenEnvelope_square a ha ha'
          rw [show (72900 : Nat) = 729 * 100 by decide] at h
          simpa only [show (10 : Nat) ^ 2 = 100 by decide,
            Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm] using h
        · simpa only [hindex, show 2 * k + 4 - 2 = 2 * k + 2 by omega] using hlo
      · let k := (W - 5) / 2
        have hindex : W = 2 * k + 5 := by dsimp [k]; omega
        have hbound := below_odd_envelope k N a (hd.trans hindex) ha ha'
          (by simpa only [hindex, show 2 * k + 5 - 2 = 2 * k + 3 by omega] using hhi)
        apply scale_envelope_bound (below N).length (oddEnvelope a) k 3 a N hbound
        · have h := oddEnvelope_square a ha ha'
          rw [show (729000 : Nat) = 729 * 1000 by decide] at h
          simpa only [show (10 : Nat) ^ 3 = 1000 by decide,
            Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm] using h
        · simpa only [hindex, show 2 * k + 5 - 2 = 2 * k + 3 by omega] using hlo

/-- Nine is exactly the least natural-number constant that works for
all numerical cutoffs of the existing complete target census. -/
theorem uniform_integer_constant_iff (c : Nat) :
    (∀ N : Nat, (below N).length ^ 2 ≤ c * N) ↔ 9 ≤ c := by
  constructor
  · intro h
    by_cases hc : 9 ≤ c
    · exact hc
    · apply False.elim
      apply below_quadratic_eight_fails
      intro N
      exact Nat.le_trans (h N) (Nat.mul_le_mul_right N (show c ≤ 8 by omega))
  · intro hc N
    exact Nat.le_trans (below_quadratic_nine N) (Nat.mul_le_mul_right N hc)

/-- The sharp integer quadratic constant improves the explicit
reciprocal-proportion threshold from fifty times `r^2` to nine times
`r^2`. The natural-number inequality also includes `r = 0`. -/
theorem below_effectively_sparse_nine (r N : Nat) (hN : 9 * r ^ 2 ≤ N) :
    r * (below N).length ≤ N := by
  have hsquare : (r * (below N).length) ^ 2 ≤ N ^ 2 := by
    calc
      (r * (below N).length) ^ 2 = r ^ 2 * (below N).length ^ 2 := Nat.mul_pow _ _ _
      _ ≤ r ^ 2 * (9 * N) := Nat.mul_le_mul_left _ (below_quadratic_nine N)
      _ = (9 * r ^ 2) * N := by simp only [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
      _ ≤ N * N := Nat.mul_le_mul_right N hN
      _ = N ^ 2 := (Nat.pow_two N).symm
  by_cases h : r * (below N).length ≤ N
  · exact h
  · have hlt : N ^ 2 < (r * (below N).length) ^ 2 :=
      Nat.pow_lt_pow_left (by omega) (by decide)
    omega

end SharpOddTargetSparsity

#print axioms SharpOddTargetSparsity.below_quadratic_nine
#print axioms SharpOddTargetSparsity.uniform_integer_constant_iff
#print axioms SharpOddTargetSparsity.below_effectively_sparse_nine
