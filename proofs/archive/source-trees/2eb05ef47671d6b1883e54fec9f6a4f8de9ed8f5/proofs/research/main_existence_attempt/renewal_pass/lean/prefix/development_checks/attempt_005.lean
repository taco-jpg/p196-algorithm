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

theorem prefix_transport (q s : Nat → Nat) (L W a b c : Nat) (hw : L = W)
    (he : ∀ i, i < L → q i = s i) :
    Prefix q L a b c ↔ Prefix s W a b c := by
  subst W
  constructor
  · rintro ⟨hL, h0, h1, h2⟩
    refine ⟨hL, ?_, ?_, ?_⟩
    · rw [← he 0 (by omega)]; exact h0
    · rw [← he 1 (by omega)]; exact h1
    · rw [← he 2 (by omega)]; exact h2
  · rintro ⟨hL, h0, h1, h2⟩
    refine ⟨hL, ?_, ?_, ?_⟩
    · rw [he 0 (by omega)]; exact h0
    · rw [he 1 (by omega)]; exact h1
    · rw [he 2 (by omega)]; exact h2

/-- The obstruction concerns any proposed fixed finite target with this
prefix, using finite-prefix equality and its actual width. -/
theorem no_two_step_ancestor_of_prefix (target : Nat → Nat) (L : Nat)
    (hp : Prefix target L 2 12 4) :
    ¬ ∃ q W, Admissible W q ∧ (iterPairs q W 2).1 = L ∧
      ∀ i, i < L → (iterPairs q W 2).2 i = target i := by
  rintro ⟨q, W, ha, hw, he⟩
  apply no_two_step_prefix_two_twelve_four q W ha
  apply (prefix_transport (iterPairs q W 2).2 target (iterPairs q W 2).1 L 2 12 4 hw ?_).mpr hp
  intro i hi
  exact he i (by simpa only [← hw] using hi)

theorem canonical_columns_agree (n : Nat) (d e : Nat → Nat) (L W : Nat)
    (hd : Canonical n d L) (he : Canonical n e W) :
    L = W ∧ ∀ i, i < L → columnSum d L i = columnSum e W i := by
  have hw : L = W :=
    (DecimalQuantitativeMass.decimalLength_of_canonical n d L hd).symm.trans
      (DecimalQuantitativeMass.decimalLength_of_canonical n e W he)
  subst W
  have hdigits := value_injective d e L hd.2.1 he.2.1
    (hd.2.2.2.trans he.2.2.2.symm)
  refine ⟨rfl, ?_⟩
  intro i hi
  simp only [columnSum, reflected]
  rw [hdigits i hi, hdigits (L - 1 - i) (by omega)]

/-- Transfer is independent of the chosen canonical decimal digits and
does not identify the irrelevant infinite tails of coefficient functions. -/
theorem represented_prefix_iff (n : Nat) (d e q : Nat → Nat) (L W a b c : Nat)
    (hd : Canonical n d L) (he : Canonical n e W)
    (hq : ∀ i, i < L → columnSum d L i = q i) :
    Prefix q L a b c ↔ Prefix (columnSum e W) W a b c := by
  obtain ⟨hw, hcols⟩ := canonical_columns_agree n d e L W hd he
  exact prefix_transport q (columnSum e W) L W a b c hw
    (fun i hi => (hq i hi).symm.trans (hcols i hi))

/-- Every positive ordinary decimal input avoids the forbidden pair prefix
(1,6,2) after one actual reverse-and-add step. -/
theorem numeric_one_step_no_prefix (n : Nat) (hn : 0 < n)
    (d : Nat → Nat) (L : Nat) (hd : Canonical (orbit n 1) d L) :
    ¬ Prefix (columnSum d L) L 1 6 2 := by
  obtain ⟨e, W, he⟩ := canonical_exists n hn
  let q := columnSum e W
  have ha : Admissible W q := NormalizationBridge.canonical_admissible n e W he
  obtain ⟨f, hf, hrep⟩ := representation_next n e q W he (fun _ _ => rfl)
  intro hp
  exact no_output_prefix_one_six_two q W ha
    ((represented_prefix_iff (orbit n 1) f d (nextColumns q W) (nextWidth q W) L
      1 6 2 hf hd hrep).mpr hp)

/-- The pair obstruction applies to the actual ordinary integer after two
steps, with any canonical representation supplied by the caller. -/
theorem numeric_two_step_no_prefix (n : Nat) (hn : 0 < n)
    (d : Nat → Nat) (L : Nat) (hd : Canonical (orbit n 2) d L) :
    ¬ Prefix (columnSum d L) L 2 12 4 := by
  obtain ⟨e, W, he⟩ := canonical_exists n hn
  let q := columnSum e W
  have ha : Admissible W q := NormalizationBridge.canonical_admissible n e W he
  obtain ⟨f, hf, hrep⟩ := iterPairs_representation n e q W 2 he (fun _ _ => rfl)
  intro hp
  exact no_two_step_prefix_two_twelve_four q W ha
    ((represented_prefix_iff (orbit n 2) f d (iterPairs q W 2).2
      (iterPairs q W 2).1 L 2 12 4 hf hd hrep).mpr hp)

/-- No positive ordinary orbit has pair prefix (2,12,4) at any time t>=2. -/
theorem numeric_after_two_no_prefix (n t : Nat) (hn : 0 < n) (ht : 2 ≤ t)
    (d : Nat → Nat) (L : Nat) (hd : Canonical (orbit n t) d L) :
    ¬ Prefix (columnSum d L) L 2 12 4 := by
  have hs : t - 2 + 2 = t := by omega
  have he := LychrelCertificates.orbit_add n (t - 2) 2
  rw [hs] at he
  have hcan : Canonical (orbit (orbit n (t - 2)) 2) d L := by
    rw [← he]
    exact hd
  exact numeric_two_step_no_prefix (orbit n (t - 2)) (orbit_positive n hn _)
    d L hcan

end DecimalPrefixObstruction
