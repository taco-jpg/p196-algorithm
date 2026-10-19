import P196.Foundations.LychrelDigitSums

/-!
# The terminal carry for an odd low outer coefficient

Agent #6: at width at least three, symmetry identifies the final two
coefficients with the first two. An even penultimate coefficient cannot
equal nine, so its outgoing carry depends only on its own size.
-/

set_option autoImplicit false

namespace OddPredecessorTargetCensus

open DecimalDigits FoldedDecimal

/-- An admissible word with an odd outer coefficient at most nine and
an even next coefficient overflows exactly at the outer-nine boundary
with next coefficient at least ten. -/
theorem odd_outer_carry_iff
    (q : Nat → Nat) (L : Nat) (ha : Admissible L q)
    (hL : 3 ≤ L) (hsmall : q 0 ≤ 9) (hodd : q 0 % 2 = 1)
    (heven : q 1 % 2 = 0) :
    carry q L = 1 ↔ q 0 = 9 ∧ 10 ≤ q 1 := by
  have hlastindex : L - 1 + 1 = L := by omega
  have hprevindex : L - 2 + 1 = L - 1 := by omega
  have hreflect : L - 1 - 1 = L - 2 := by omega
  have hlastcoeff : q (L - 1) = q 0 := by
    simpa only [Nat.sub_zero] using (ha.2.2.2.1 0 (by omega)).symm
  have hprevcoeff : q (L - 2) = q 1 := by
    simpa only [hreflect] using (ha.2.2.2.1 1 (by omega)).symm
  have hlast : carry q (L - 1 + 1) =
      (q (L - 1) + carry q (L - 1)) / 10 := rfl
  rw [hlastindex, hlastcoeff] at hlast
  have hprev : carry q (L - 2 + 1) =
      (q (L - 2) + carry q (L - 2)) / 10 := rfl
  rw [hprevindex, hprevcoeff] at hprev
  have hcarry := carry_bounded q L ha.2.2.1
  have hbprev := hcarry (L - 1) (by omega)
  have hbinner := hcarry (L - 2) (by omega)
  have hqone := ha.2.2.1 1 (by omega)
  omega

#print axioms odd_outer_carry_iff

end OddPredecessorTargetCensus
