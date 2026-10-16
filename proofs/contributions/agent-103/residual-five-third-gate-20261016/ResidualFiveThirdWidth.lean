import ResidualFiveFiberConclusion
import PrefixObstruction

/-!
# The exact source width and exterior digits at the residual-five third layer

This module uses the original numeric fiber and the original pair obstructions.
Every conclusion concerns an actual ordinary reverse-and-add predecessor.
Terminal carry zero does not assert that the interior carries vanish.
-/

set_option autoImplicit false

namespace Agent103.ResidualFiveThirdWidth

open Lychrel196 DecimalDigits FoldedDecimal
open Agent103.ResidualFiveFibers Agent103.ResidualFive
open DecimalPrefixObstruction SevenColumnKernel.PalindromeBridge

/-- Every canonical representation of an enumerated ordinary integer has the
original residual coefficient profile at every relevant position. -/
theorem fiber_columns (r n : Nat) (e : Nat → Nat)
    (hn : n ∈ fiber r) (he : Canonical n e (2 * r + 4)) :
    ∀ i, i < 2 * r + 4 →
      columnSum e (2 * r + 4) i = fiveSourceDigit r i := by
  obtain ⟨ds, hds, hp, hv⟩ :=
    (Agent101.mem_numericFiber_digits (half r) none n).mp hn
  have hlen := congrArg List.length hp
  rw [Agent101.numeric_length_digitPairSums, profile_length] at hlen
  have hc : Canonical n (Agent101.digitFn ds) ds.length := by
    simpa only [hv] using (Agent101.canonicalDigits_iff ds).mp hds
  have hcols := (canonical_columns_agree n (Agent101.digitFn ds) e
    ds.length (2 * r + 4) hc he).2
  intro i hi
  have hid : i < ds.length := by omega
  rw [← hcols i hid, ← Agent101.digitFn_digitPairSums ds i hid, hp]
  exact profile_digit r i hi

/-- A predecessor of any member of the complete fiber has this same width,
has no terminal overflow, and begins with pair coefficients one and six.
The supplied canonical source already entails that the source is positive. -/
theorem predecessor_width_and_source (r n z L : Nat) (d : Nat → Nat)
    (hn : n ∈ fiber r) (hstep : step z = n) (hd : Canonical z d L) :
    L = 2 * r + 4 ∧ carry (columnSum d L) L = 0 ∧
      columnSum d L 0 = 1 ∧ columnSum d L 1 = 6 := by
  obtain ⟨⟨e, he⟩, _⟩ := (fiber_mem_canonical r n).mp hn
  let q := columnSum d L
  have ha : Admissible L q := NormalizationBridge.canonical_admissible z d L hd
  obtain ⟨f, hf, hrep⟩ := representation_next z d q L hd (fun _ _ => rfl)
  rw [hstep] at hf
  obtain ⟨hw, hagree⟩ := canonical_columns_agree n f e
    (nextWidth q L) (2 * r + 4) hf he
  have hnext (i : Nat) (hi : i < 2 * r + 4) :
      nextColumns q L i = fiveSourceDigit r i := by
    have hiw : i < nextWidth q L := by omega
    exact (hrep i hiw).symm.trans
      ((hagree i hiw).trans (fiber_columns r n e hn he i hi))
  have h0 : nextColumns q L 0 = 2 :=
    (hnext 0 (by omega)).trans (fiveSourceDigit_zero r)
  have h1 : nextColumns q L 1 = 12 :=
    (hnext 1 (by omega)).trans (fiveSourceDigit_one r)
  have hL : 2 ≤ L := by
    unfold nextWidth at hw
    split at hw <;> omega
  have hb := carry_bounded q L ha.2.2.1 L (Nat.le_refl L)
  have hc : carry q L = 0 := by
    by_cases hz : carry q L = 0
    · exact hz
    · have hcarry : carry q L = 1 := by omega
      have hle := overflow_outer_two_second_le_eleven q L ha hL hcarry h0
      omega
  have hwidth : L = 2 * r + 4 := by
    simpa only [nextWidth, hc, ite_true] using hw
  have hi0 := even_no_overflow_inverse q L 0 1 ha ha.1 hc rfl
    (by simpa only [Nat.sub_zero] using hc) h0
  have hi1 := even_no_overflow_inverse q L 1 6 ha (by omega) hc hi0.2.1
    (by simpa only [Nat.sub_zero] using hi0.2.2) h1
  exact ⟨hwidth, hc, hi0.1, hi1.1⟩

/-- An actual positive predecessor forces all four exterior target digits.
This is independent of the caller's chosen canonical representation, and
includes the empty central word at r = 0. -/
theorem predecessor_boundary (r n z L : Nat) (d e : Nat → Nat)
    (hn : n ∈ fiber r) (_hz : 0 < z) (hstep : step z = n)
    (hd : Canonical z d L) (he : Canonical n e (2 * r + 4)) :
    L = 2 * r + 4 ∧ carry (columnSum d L) L = 0 ∧
      columnSum d L 0 = 1 ∧ columnSum d L 1 = 6 ∧
      e 0 = 1 ∧ e (2 * r + 3) = 1 ∧
      e 1 = 6 ∧ e (2 * r + 2) = 6 := by
  obtain ⟨hw, hc, hq0, hq1⟩ :=
    predecessor_width_and_source r n z L d hn hstep hd
  have hcan : Canonical n (output (columnSum d L)) L := by
    rw [← hstep]
    exact canonical_next_no_overflow z d L hd hc
  have heq := (canonical_unique hcan he).2
  have he0 : e 0 = 1 := by
    rw [← heq 0 (by omega)]
    simp only [output, carry, hq0]
  have he1 : e 1 = 6 := by
    rw [← heq 1 (by omega)]
    simp only [output, carry, hq0, hq1]
  have hout0 := (fiber_columns r n e hn he 0 (by omega)).trans
    (fiveSourceDigit_zero r)
  have hout1 := (fiber_columns r n e hn he 1 (by omega)).trans
    (fiveSourceDigit_one r)
  have hehi0 : e (2 * r + 3) = 1 := by
    simp only [columnSum, reflected, Nat.sub_zero,
      show 2 * r + 4 - 1 = 2 * r + 3 by omega, he0] at hout0
    omega
  have hehi1 : e (2 * r + 2) = 6 := by
    simp only [columnSum, reflected,
      show 2 * r + 4 - 1 - 1 = 2 * r + 2 by omega, he1] at hout1
    omega
  exact ⟨hw, hc, hq0, hq1, he0, hehi0, he1, hehi1⟩

#print axioms fiber_columns
#print axioms predecessor_width_and_source
#print axioms predecessor_boundary

end Agent103.ResidualFiveThirdWidth
