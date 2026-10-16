import LychrelDigitSums

/-! Exact all-width obstructions for the actual decimal pair dynamics.
No bounded search, finite-language approximation, or Lychrel assertion. -/

namespace DecimalPrefixObstruction

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

def Prefix (q : Nat → Nat) (L a b c : Nat) : Prop :=
  3 ≤ L ∧ q 0 = a ∧ q 1 = b ∧ q 2 = c

/-- Short widths are discharged by the actual symmetry, including centers. -/
theorem prefix_width_ge_five (q : Nat → Nat) (L a b c : Nat)
    (ha : Admissible L q) (hp : Prefix q L a b c) (hac : a ≠ c) (hbc : b ≠ c) :
    5 ≤ L := by
  have hL := hp.1
  by_cases h3 : L = 3
  · have hs := ha.2.2.2.1 0 (by omega)
    have he : q 0 = q 2 := by simpa only [h3] using hs
    have := hp.2.1
    have := hp.2.2.2
    omega
  · by_cases h4 : L = 4
    · have hs := ha.2.2.2.1 1 (by omega)
      have he : q 1 = q 2 := by simpa only [h4] using hs
      have := hp.2.2.1
      have := hp.2.2.2
      omega
    · omega

theorem input_width_ge_four (q : Nat → Nat) (L a b c : Nat)
    (ha : Admissible L q)
    (hp : Prefix (nextColumns q L) (nextWidth q L) a b c)
    (hac : a ≠ c) (hbc : b ≠ c) : 4 ≤ L := by
  have hw := prefix_width_ge_five _ _ a b c (NormalizationBridge.admissible_next q L ha)
    hp hac hbc
  unfold nextWidth at hw
  split at hw <;> omega

theorem no_overflow_outer_ge_two (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hc : carry q L = 0) : 2 ≤ nextColumns q L 0 := by
  have ht := folded_carry_transition q L 0 ha.1 ha.2.2.2.1
  have he := folded_emission_no_overflow q L 0 ha.1 ha.2.2.2.1 hc
  have hb := carry_bounded q L ha.2.2.1 (L - 1) (by omega)
  have hq := ha.2.1
  have hz : carry q 0 = 0 := rfl
  simp only [Nat.sub_zero, Nat.zero_add, hz] at ht he
  rw [hc] at ht
  omega

/-- With overflowing outer output 2, the delayed leading digit is at
most 2, so the following pair coefficient cannot exceed 11. -/
theorem overflow_outer_two_second_le_eleven (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 2 ≤ L) (hc : carry q L = 1)
    (ho : nextColumns q L 0 = 2) : nextColumns q L 1 ≤ 11 := by
  have houter := next_column_overflow_outer q L ha.1 hc
  have hc1 := carry_bounded q L ha.2.2.1 1 (by omega)
  have hb := carry_bounded q L ha.2.2.1 (L - 1) (by omega)
  have ht := (folded_carry_transition q L 0 ha.1 ha.2.2.2.1).2
  simp only [Nat.sub_zero] at ht
  rw [hc] at ht
  have hq0 : q 0 = 11 := by omega
  have hd := folded_delay_update q L 0 ha.1 ha.2.2.2.1
  simp only [Nat.zero_add, Nat.sub_zero, hq0] at hd
  have hdelay : extended q L (L - 1) ≤ 2 := by omega
  have he := folded_emission_overflow q L 1 (by omega) hc
  omega

/-- An overflowing output beginning (1,6) has a delayed high digit at
least four before its third coefficient, even when that coefficient is
a center. The two possible second input coefficients are exactly 5,14. -/
theorem overflow_one_six_forces_large_delay (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 3 ≤ L) (hc : carry q L = 1)
    (h0 : nextColumns q L 0 = 1) (h1 : nextColumns q L 1 = 6) :
    q 0 = 10 ∧ (q 1 = 5 ∨ q 1 = 14) ∧ 4 ≤ extended q L (L - 2) := by
  have houter := next_column_overflow_outer q L ha.1 hc
  have hc1 := carry_bounded q L ha.2.2.1 1 (by omega)
  have hq0pos := ha.2.1
  have hq0 : q 0 = 10 := by omega
  have hc1eq : carry q 1 = 1 := by omega
  have hb1 := carry_bounded q L ha.2.2.1 (L - 1) (by omega)
  have hb2 := carry_bounded q L ha.2.2.1 (L - 2) (by omega)
  have hq1 := ha.2.2.1 1 (by omega)
  have ht1 := (folded_carry_transition q L 1 (by omega) ha.2.2.2.1).2
  have hd0 := folded_delay_update q L 0 ha.1 ha.2.2.2.1
  have hd1 := folded_delay_update q L 1 (by omega) ha.2.2.2.1
  have he1 := folded_emission_overflow q L 1 (by omega) hc
  have hidx : L - 1 - 1 = L - 2 := by omega
  rw [hidx] at ht1 hd1
  simp only [Nat.zero_add, Nat.sub_zero, hq0] at hd0
  change extended q L (L - 2) = (q 1 + carry q (L - 2)) % 10 at hd1
  have hdelay0 : extended q L (L - 1) = carry q (L - 1) := by omega
  rw [h1, hc1eq, hdelay0] at he1
  have hq1cases : q 1 = 5 ∨ q 1 = 14 := by
    by_cases hb0 : carry q (L - 1) = 0
    · left
      omega
    · right
      omega
  refine ⟨hq0, hq1cases, ?_⟩
  rcases hq1cases with hq1eq | hq1eq <;> omega

/-- No actual output pair word, of any finite width, begins (1,6,2). -/
theorem no_output_prefix_one_six_two (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) :
    ¬ Prefix (nextColumns q L) (nextWidth q L) 1 6 2 := by
  intro hp
  have hL := input_width_ge_four q L 1 6 2 ha hp (by decide) (by decide)
  have hb := carry_bounded q L ha.2.2.1 L (Nat.le_refl _)
  by_cases hc : carry q L = 0
  · have ho := no_overflow_outer_ge_two q L ha hc
    have := hp.2.1
    omega
  · have hc1 : carry q L = 1 := by omega
    have hd := (overflow_one_six_forces_large_delay q L ha (by omega) hc1
      hp.2.1 hp.2.2.1).2.2
    have he := folded_emission_overflow q L 2 (by omega) hc1
    have := hp.2.2.2
    omega

/-- A no-overflow even emission with zero exterior carries forces its
input coefficient and the next two carries exactly. -/
theorem even_no_overflow_inverse (q : Nat → Nat) (L i a : Nat)
    (ha : Admissible L q) (hi : i < L) (hc : carry q L = 0)
    (hl : carry q i = 0) (hh : carry q (L - i) = 0)
    (ho : nextColumns q L i = 2 * a) :
    q i = a ∧ carry q (i + 1) = 0 ∧ carry q (L - 1 - i) = 0 := by
  have ht := folded_carry_transition q L i hi ha.2.2.2.1
  have he := folded_emission_no_overflow q L i hi ha.2.2.2.1 hc
  have hb := carry_bounded q L ha.2.2.1 (L - 1 - i) (by omega)
  rw [hl, hh] at ht
  rw [hl, ho] at he
  omega

/-- Every actual output beginning (2,12,4) is a no-overflow output, and
its predecessor begins exactly (1,6,2). -/
theorem prefix_two_twelve_four_inverse (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q)
    (hp : Prefix (nextColumns q L) (nextWidth q L) 2 12 4) :
    carry q L = 0 ∧ Prefix q L 1 6 2 := by
  have hL := input_width_ge_four q L 2 12 4 ha hp (by decide) (by decide)
  have hb := carry_bounded q L ha.2.2.1 L (Nat.le_refl _)
  have hc : carry q L = 0 := by
    by_cases hc0 : carry q L = 0
    · exact hc0
    · have hc1 : carry q L = 1 := by omega
      have he := overflow_outer_two_second_le_eleven q L ha (by omega) hc1 hp.2.1
      have := hp.2.2.1
      omega
  have h0 := even_no_overflow_inverse q L 0 1 ha ha.1 hc rfl
    (by simpa only [Nat.sub_zero] using hc) hp.2.1
  have h1 := even_no_overflow_inverse q L 1 6 ha (by omega) hc h0.2.1
    (by simpa only [Nat.sub_zero] using h0.2.2) hp.2.2.1
  have h2 := even_no_overflow_inverse q L 2 2 ha (by omega) hc h1.2.1
    (by simpa only [Nat.sub_sub] using h1.2.2) hp.2.2.2
  exact ⟨hc, by omega, h0.1, h1.1, h2.1⟩

/-- The cylinder (2,12,4) has no two-step predecessor among any finite
admissible pair words, without a restriction on either predecessor width. -/
theorem no_two_step_prefix_two_twelve_four (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) :
    ¬ Prefix (iterPairs q L 2).2 (iterPairs q L 2).1 2 12 4 := by
  intro hp
  have hnext := NormalizationBridge.admissible_next q L ha
  have hi := prefix_two_twelve_four_inverse (nextColumns q L) (nextWidth q L) hnext hp
  exact no_output_prefix_one_six_two q L ha hi.2

end DecimalPrefixObstruction
