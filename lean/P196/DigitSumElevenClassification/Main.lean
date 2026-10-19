import P196.DigitSumElevenClassification.EasyCases
import P196.DigitSumElevenClassification.SmallWidths
import P196.DigitSumElevenClassification.SparseTrajectories
import P196.DigitSumElevenClassification.Predecessor

/-!
# The exact exceptional profile at decimal digit sum eleven

Every positive ordinary decimal seed with digit sum at most eleven reaches
a palindrome within twelve positive steps, except for the two seeds
100090001 and 200090000. Their common positive orbit is not asserted to be
palindrome-free forever. The first seed is itself a palindrome at time zero.

The second seed has no positive reverse-and-add predecessor. Consequently
every positive-time state of a hypothetical Lychrel orbit has digit sum at
least twelve. This does not construct a Lychrel number or settle 196.
-/

namespace DigitSumElevenClassification

open DecimalDigits DecimalMass FoldedDecimal Lychrel196 LowDigitSumTermination

/-- The arbitrary-width digit-sum-eleven termination bound, with its exact
two exceptions to a positive-time bound. -/
theorem palindrome_within_twelve_of_digitSum_le_eleven_except_two
    (n : Nat) (hn : 0 < n) (hs : digitSum n ≤ 11)
    (hne₁ : n ≠ 100090001) (hne₂ : n ≠ 200090000) :
    ∃ k : Nat, 1 ≤ k ∧ k ≤ 12 ∧ Palindrome (orbit n k) := by
  classical
  by_cases hten : digitSum n ≤ 10
  · obtain ⟨k, hkpos, hkbound, hp⟩ :=
      DigitSumTenTermination.palindrome_within_seven_of_digitSum_le_ten n hn hten
    exact ⟨k, hkpos, by omega, hp⟩
  have heleven : digitSum n = 11 := by omega
  obtain ⟨d, L, hcan⟩ := canonical_exists n hn
  have hmass : wordSum d L = 11 := by
    rw [← digitSum_value d L hcan.2.1, hcan.2.2.2]
    exact heleven
  have hmulti : L ≠ 1 := by
    intro heq
    subst L
    have hd := hcan.2.1 0 (by decide)
    simp only [wordSum, Nat.zero_add] at hmass
    omega
  by_cases hsmall : ∀ i, i < L → columnSum d L i ≤ 9
  · have hp := (step_palindrome_iff d L hcan.1 hcan.2.1 hcan.2.2.1).mpr
      (Or.inl hsmall)
    rw [hcan.2.2.2] at hp
    exact ⟨1, by decide, by decide, hp⟩
  have hex : ∃ i, i < L ∧ 9 < columnSum d L i := by
    apply Classical.byContradiction
    intro hnone
    apply hsmall
    intro i hi
    by_cases hbound : columnSum d L i ≤ 9
    · exact hbound
    · exact False.elim (hnone ⟨i, hi, by omega⟩)
  obtain ⟨m, hmL, hmhigh⟩ := hex
  by_cases hmid : m ≠ L - 1 - m
  · exact ⟨2, by decide, by decide,
      second_step_palindrome_of_noncentral_high n d L m hcan hs hmL hmid (by omega)⟩
  have hwidth : L = 2 * m + 1 := by omega
  subst L
  have hm : 0 < m := by omega
  have hcenter : columnSum d (2 * m + 1) m = 2 * d m := by
    have heq : 2 * m + 1 - 1 - m = m := by omega
    simp only [columnSum, reflected, heq]
    omega
  have hdmin : 5 ≤ d m := by omega
  have hdmax := hcan.2.1 m (by omega)
  have hlead : 0 < d (2 * m) := by simpa using hcan.2.2.1
  by_cases height : d m = 8
  · rcases center_eight_profiles d m hm hlead hmass height with heasy | houter | hnear
    · exact ⟨3, by decide, by decide,
        DigitSumTenTermination.central_three_steps_refined n d m hm hcan
          (by omega) heasy.1 heasy.2⟩
    · by_cases hlarge : 3 ≤ m
      · exact ⟨4, by decide, by decide, outer_eight_large n d m hlarge hcan houter⟩
      · exact outer_eight_small n d m hm (by omega) hcan houter
    · by_cases hlarge : 4 ≤ m
      · exact ⟨6, by decide, by decide, near_eight_large n d m hlarge hcan hnear.2⟩
      · exact near_eight_small n d m hnear.1 (by omega) hcan hnear.2
  by_cases hnine : d m = 9
  · rcases center_nine_profiles d m hm hlead hmass hnine with heasy | houter | hnear
    · exact ⟨4, by decide, by decide,
        DigitSumTenTermination.central_four_steps_refined n d m hm hcan
          (by omega) heasy.1 heasy.2⟩
    · by_cases hlarge : 5 ≤ m
      · exact ⟨10, by decide, by decide, outer_nine_large n d m hlarge hcan houter⟩
      · by_cases hfour : m = 4
        · subst m
          rcases width_nine_outer_two n d hcan houter with hex₁ | hex₂
          · exact False.elim (hne₁ hex₁)
          · exact False.elim (hne₂ hex₂)
        · exact outer_nine_small n d m hm (by omega) hcan houter
    · by_cases hlarge : 4 ≤ m
      · exact ⟨6, by decide, by decide, near_nine_large n d m hlarge hcan hnear.2⟩
      · exact near_nine_small n d m hnear.1 (by omega) hcan hnear.2
  · have hext : ∀ i, i < 2 * m + 1 → i ≠ m →
        columnSum d (2 * m + 1) i ≤ 6 := by
      intro i hi hic
      have hb := noncentral_column_add_middle_le_mass d m i hi hic
      omega
    obtain ⟨k, hkpos, hkbound, hp⟩ := central_small_within_five n d m hm hcan hs
      (by omega) (by omega) hext
    exact ⟨k, hkpos, by omega, hp⟩

/-- Avoidance at positive times one through twelve characterizes exactly
the two exceptional seeds within the digit-sum-eleven threshold. -/
theorem no_palindrome_in_first_twelve_iff_exception
    (n : Nat) (hn : 0 < n) (hs : digitSum n ≤ 11) :
    (∀ k, 1 ≤ k → k ≤ 12 → ¬ Palindrome (orbit n k)) ↔
      n = 100090001 ∨ n = 200090000 := by
  constructor
  · intro hfree
    by_cases hfirst : n = 100090001
    · exact Or.inl hfirst
    by_cases hsecond : n = 200090000
    · exact Or.inr hsecond
    obtain ⟨k, hkpos, hkbound, hp⟩ :=
      palindrome_within_twelve_of_digitSum_le_eleven_except_two n hn hs hfirst hsecond
    exact False.elim (hfree k hkpos hkbound hp)
  · intro hex
    rcases hex with rfl | rfl
    · exact exceptional_positive_prefix.1
    · intro k _ hkbound
      exact exceptional_positive_prefix.2 k hkbound

/-- A hypothetical Lychrel seed of digit sum at most eleven must be the
single nonpalindromic seed in the exceptional profile. -/
theorem lychrel_seed_eq_exception_of_digitSum_le_eleven
    (n : Nat) (hlychrel : IsLychrel n) (hs : digitSum n ≤ 11) :
    n = 200090000 := by
  have hn : 0 < n := by
    apply Classical.byContradiction
    intro hnonpos
    have hz : n = 0 := by omega
    subst n
    exact hlychrel 0 (by decide)
  have hfree : ∀ k, 1 ≤ k → k ≤ 12 → ¬ Palindrome (orbit n k) := by
    intro k _ _
    exact hlychrel k
  rcases (no_palindrome_in_first_twelve_iff_exception n hn hs).mp hfree with hfirst | hsecond
  · subst n
    exact False.elim (hlychrel 0 exceptional_seed_controls.2.2)
  · exact hsecond

/-- Every positive-time state of a hypothetical decimal Lychrel orbit has
digit sum at least twelve. Time zero is intentionally excluded. -/
theorem lychrel_positive_orbit_digitSum_ge_twelve
    (n : Nat) (hlychrel : IsLychrel n) (t : Nat) (ht : 1 ≤ t) :
    12 ≤ digitSum (orbit n t) := by
  have hn : 0 < n := by
    apply Classical.byContradiction
    intro hnonpos
    have hz : n = 0 := by omega
    subst n
    exact hlychrel 0 (by decide)
  apply Classical.byContradiction
  intro hmass
  have htail : IsLychrel (orbit n t) := by
    intro k hp
    apply hlychrel (t + k)
    simpa only [LychrelCertificates.orbit_add] using hp
  have heq := lychrel_seed_eq_exception_of_digitSum_le_eleven (orbit n t) htail (by omega)
  obtain ⟨s, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : t ≠ 0)
  exact no_positive_predecessor_exception (orbit n s) (orbit_positive n hn s) heq

end DigitSumElevenClassification
