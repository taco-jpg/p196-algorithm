import P196.OddTargetPredecessorParity.Definitions

/-!
# The exact numeric range of the shifted palindrome candidate

Agent #6: canonical width and a leading digit at most five are
equivalent to the ordinary interval used by the parity criterion.
-/

set_option autoImplicit false

namespace OddTargetPredecessorParity

open DecimalDigits Agent101

/-- The leading-digit cutoff is exactly the upper endpoint of the
candidate's numeric interval. -/
theorem canonical_leading_le_five_iff
    (p L : Nat) (d : Nat → Nat) (hc : Canonical p d L) :
    d (L - 1) ≤ 5 ↔ p < 6 * 10 ^ (L - 1) := by
  obtain ⟨K, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hc.1)
  have hv := hc.2.2.2
  have htail := bounded_value_lt_pow d K
    (fun i hi => hc.2.1 i (by omega))
  simp only [Nat.succ_sub_one, value] at hv ⊢
  constructor
  · intro hlead
    have hm := Nat.mul_le_mul_right (10 ^ K) hlead
    omega
  · intro hu
    by_cases hlead : d K ≤ 5
    · exact hlead
    have hm := Nat.mul_le_mul_right (10 ^ K)
      (show 6 ≤ d K by omega)
    omega

/-- The candidate interval supplies precisely a canonical numeral of
the requested positive width whose leading digit is at most five. -/
theorem candidate_canonical_iff
    (p L : Nat) (hL : 0 < L) :
    (10 ^ (L - 1) ≤ p ∧ p < 6 * 10 ^ (L - 1)) ↔
      ∃ d, Canonical p d L ∧ d (L - 1) ≤ 5 := by
  constructor
  · rintro ⟨hlo, hu⟩
    have hpow : 6 * 10 ^ (L - 1) ≤ 10 ^ L := by
      obtain ⟨K, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hL)
      simp only [Nat.succ_sub_one, Nat.pow_succ]
      omega
    obtain ⟨d, hc⟩ := (decimalWidth_iff_canonical p L).mp
      ⟨hL, hlo, Nat.lt_of_lt_of_le hu hpow⟩
    exact ⟨d, hc, (canonical_leading_le_five_iff p L d hc).mpr hu⟩
  · rintro ⟨d, hc, hlead⟩
    exact ⟨(canonical_decimalWidth p d L hc).2.1,
      (canonical_leading_le_five_iff p L d hc).mp hlead⟩

#print axioms canonical_leading_le_five_iff
#print axioms candidate_canonical_iff

end OddTargetPredecessorParity
