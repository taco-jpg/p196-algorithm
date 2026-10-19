import P196.DigitSumTenTermination.CentralRefinement
import P196.DigitSumTenTermination.DigitGeometry

/-!
# Sharp termination at decimal digit sum ten

Every positive ordinary decimal integer of digit sum at most ten reaches
a palindrome within four positive steps, except for 190, whose first hit
is seven. The proof applies at arbitrary width and imports the previously
proved digit-sum-nine bound and its exact 190 control.

The resulting lower bound on every digit sum in a hypothetical Lychrel
orbit is conditional. No Lychrel seed or conclusion about 196 is supplied.
-/

namespace DigitSumTenTermination

open DecimalDigits DecimalMass FoldedDecimal Lychrel196 LowDigitSumTermination

/-- A middle digit five at mass at most ten terminates within three steps.
If an exterior pair is too large for the two-step criterion, its doubled
successor and reflection force two carries and a digit sum at most four. -/
theorem central_five_within_three (n : Nat) (d : Nat → Nat) (m : Nat)
    (hm : 0 < m) (hcan : Canonical n d (2 * m + 1))
    (hs : digitSum n ≤ 10)
    (hcenter : columnSum d (2 * m + 1) m = 10)
    (hsmall : ∀ i, i < 2 * m + 1 → i ≠ m →
      columnSum d (2 * m + 1) i ≤ 5) :
    ∃ k : Nat, 1 ≤ k ∧ k ≤ 3 ∧ Palindrome (orbit n k) := by
  classical
  by_cases hfour : ∀ i, i < 2 * m + 1 → i ≠ m →
      columnSum d (2 * m + 1) i ≤ 4
  · exact ⟨2, by decide, by decide,
      central_two_steps_palindrome n d m hm hcan (by omega) (by omega) hfour⟩
  have hex : ∃ i, i < 2 * m + 1 ∧ i ≠ m ∧
      4 < columnSum d (2 * m + 1) i := by
    apply Classical.byContradiction
    intro hnone
    apply hfour
    intro i hi hic
    by_cases hbound : columnSum d (2 * m + 1) i ≤ 4
    · exact hbound
    · exact False.elim (hnone ⟨i, hi, hic, by omega⟩)
  obtain ⟨i, hi, hic, hhigh⟩ := hex
  let q := columnSum d (2 * m + 1)
  have hsmall8 : ∀ j, j < 2 * m + 1 → j ≠ m → q j ≤ 8 := by
    intro j hj hjc
    have h := hsmall j hj hjc
    change q j ≤ 5 at h
    omega
  have hlo : 10 ≤ q m := by change q m = 10 at hcenter; omega
  have hhi : q m ≤ 18 := by change q m = 10 at hcenter; omega
  have hsym : ∀ j, j < 2 * m + 1 → q j = q (2 * m + 1 - 1 - j) :=
    columnSum_symmetric d (2 * m + 1)
  have hc := central_carry_no_overflow q m hm hlo hhi hsmall8
  have hcan' := canonical_next_no_overflow n d (2 * m + 1) hcan hc
  have hnext := central_next_exterior_exact q m hm hlo hhi hsmall8 hsym i hi hic
  simp only [nextColumns, hc, ite_true] at hnext
  have hnexti : 10 ≤ columnSum (output q) (2 * m + 1) i := by
    change 4 < q i at hhigh
    omega
  have hr : 2 * m + 1 - 1 - i < 2 * m + 1 := by omega
  have hdistinct : i ≠ 2 * m + 1 - 1 - i := by omega
  have hnextr : 10 ≤ columnSum (output q) (2 * m + 1)
      (2 * m + 1 - 1 - i) := by
    rw [← columnSum_symmetric (output q) (2 * m + 1) i hi]
    exact hnexti
  have hfirst := digitSum_step_add_nine_le n d (2 * m + 1) m hcan
    (by omega) hlo
  have hsecond := digitSum_step_add_eighteen_le (step n) (output q)
    (2 * m + 1) i (2 * m + 1 - 1 - i) hcan' hi hr hdistinct hnexti hnextr
  have hmass : digitSum (step (step n)) ≤ 4 := by omega
  have hn : 0 < n := by
    rw [← hcan.2.2.2]
    exact value_positive d (2 * m + 1) hcan.1 hcan.2.2.1
  have hnnext : 0 < step (step n) := by unfold step; omega
  exact ⟨3, by decide, by decide,
    step_palindrome_of_digitSum_le_four (step (step n)) hnnext hmass⟩

/-- The only positive seed of digit sum at most ten needing more than
four positive steps is 190. -/
theorem palindrome_within_four_of_digitSum_le_ten_except_190
    (n : Nat) (hn : 0 < n) (hs : digitSum n ≤ 10) (hne : n ≠ 190) :
    ∃ k : Nat, 1 ≤ k ∧ k ≤ 4 ∧ Palindrome (orbit n k) := by
  classical
  by_cases hnine : digitSum n ≤ 9
  · obtain ⟨k, hkpos, hkbound, hp⟩ :=
      palindrome_within_three_of_digitSum_le_nine n hn hnine
    exact ⟨k, hkpos, by omega, hp⟩
  have hten : digitSum n = 10 := by omega
  obtain ⟨d, L, hcan⟩ := canonical_exists n hn
  have hmass : wordSum d L = 10 := by
    rw [← digitSum_value d L hcan.2.1, hcan.2.2.2]
    exact hten
  have hmulti : L ≠ 1 := by
    intro hsingle
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
  by_cases hfive : d m = 5
  · have hext : ∀ i, i < 2 * m + 1 → i ≠ m →
        columnSum d (2 * m + 1) i ≤ 5 := by
      intro i hi hic
      have hb := noncentral_column_add_middle_le_mass d m i hi hic
      omega
    obtain ⟨k, hkpos, hkbound, hp⟩ :=
      central_five_within_three n d m hm hcan hs (by omega) hext
    exact ⟨k, hkpos, by omega, hp⟩
  by_cases height : d m = 8
  · by_cases hmone : m = 1
    · subst m
      have hcases := width_three_middle_eight n d (by simpa using hcan)
        (by simpa using hmass) height
      rcases hcases with rfl | rfl
      all_goals exact ⟨4, by decide, by decide, by decide⟩
    · have hext : ∀ i, i < 2 * m + 1 → i ≠ m →
          columnSum d (2 * m + 1) i ≤ 2 := by
        intro i hi hic
        have hb := noncentral_column_add_middle_le_mass d m i hi hic
        omega
      have hnear : ∀ i, i < 2 * m + 1 → (i + 1 = m ∨ i = m + 1) →
          columnSum d (2 * m + 1) i ≤ 1 := by
        intro i hi hneari
        have hb := neighbor_column_add_middle_lt_mass d m (by omega) hlead i hi hneari
        omega
      exact ⟨3, by decide, by decide,
        central_three_steps_refined n d m hm hcan (by omega) hext hnear⟩
  by_cases hninecenter : d m = 9
  · by_cases hmone : m = 1
    · subst m
      have hexception := width_three_middle_nine n d (by simpa using hcan)
        (by simpa using hmass) hninecenter
      exact False.elim (hne hexception)
    · have hext : ∀ i, i < 2 * m + 1 → i ≠ m →
          columnSum d (2 * m + 1) i ≤ 1 := by
        intro i hi hic
        have hb := noncentral_column_add_middle_le_mass d m i hi hic
        omega
      have hnear : ∀ i, i < 2 * m + 1 → (i + 1 = m ∨ i = m + 1) →
          columnSum d (2 * m + 1) i = 0 := by
        intro i hi hneari
        have hb := neighbor_column_add_middle_lt_mass d m (by omega) hlead i hi hneari
        omega
      exact ⟨4, by decide, by decide,
        central_four_steps_refined n d m hm hcan (by omega) hext hnear⟩
  · have hext : ∀ i, i < 2 * m + 1 → i ≠ m →
        columnSum d (2 * m + 1) i ≤ 4 := by
      intro i hi hic
      have hb := noncentral_column_add_middle_le_mass d m i hi hic
      omega
    exact ⟨2, by decide, by decide,
      central_two_steps_palindrome n d m hm hcan (by omega) (by omega) hext⟩

/-- Seven is a uniform positive-time bound for decimal digit sum at most ten. -/
theorem palindrome_within_seven_of_digitSum_le_ten
    (n : Nat) (hn : 0 < n) (hs : digitSum n ≤ 10) :
    ∃ k : Nat, 1 ≤ k ∧ k ≤ 7 ∧ Palindrome (orbit n k) := by
  by_cases hexception : n = 190
  · subst n
    exact ⟨7, by decide, by decide, threshold_control_190.2.2.2⟩
  · obtain ⟨k, hkpos, hkbound, hp⟩ :=
      palindrome_within_four_of_digitSum_le_ten_except_190 n hn hs hexception
    exact ⟨k, hkpos, by omega, hp⟩

/-- Within the digit-sum-ten threshold, avoidance at positive times one
through four characterizes the single ordinary seed 190. -/
theorem no_palindrome_in_first_four_iff_190
    (n : Nat) (hn : 0 < n) (hs : digitSum n ≤ 10) :
    (∀ k, 1 ≤ k → k ≤ 4 → ¬ Palindrome (orbit n k)) ↔ n = 190 := by
  constructor
  · intro hfree
    apply Classical.byContradiction
    intro hne
    obtain ⟨k, hkpos, hkbound, hp⟩ :=
      palindrome_within_four_of_digitSum_le_ten_except_190 n hn hs hne
    exact hfree k hkpos hkbound hp
  · intro heq
    subst n
    intro k _ hkbound
    exact threshold_control_190.2.1 k (by omega)

/-- The four-step bound away from 190 is attained by 280. -/
theorem sharp_example_280 :
    digitSum 280 = 10 ∧
    (∀ k, k < 4 → ¬ Palindrome (orbit 280 k)) ∧
    orbit 280 4 = 2662 ∧ Palindrome (orbit 280 4) := by
  exact ⟨by simp [digitSum], noPalindromeFor_sound 4 280 (by decide), by decide, by decide⟩

/-- The uniform seven-step bound does not extend to digit sum eleven:
20900 first reaches a palindrome at time twelve. -/
theorem threshold_control_20900 :
    digitSum 20900 = 11 ∧
    (∀ k, k < 12 → ¬ Palindrome (orbit 20900 k)) ∧
    orbit 20900 12 = 466888664 ∧ Palindrome (orbit 20900 12) := by
  exact ⟨by simp [digitSum], noPalindromeFor_sound 12 20900 (by decide), by decide, by decide⟩

/-- Every term of a hypothetical Lychrel orbit has digit sum at least eleven. -/
theorem lychrel_orbit_digitSum_ge_eleven
    (n : Nat) (hlychrel : IsLychrel n) (t : Nat) :
    11 ≤ digitSum (orbit n t) := by
  have hn : 0 < n := by
    apply Classical.byContradiction
    intro hnonpos
    have hnzero : n = 0 := by omega
    subst n
    exact hlychrel 0 (by decide)
  apply Classical.byContradiction
  intro hmass
  obtain ⟨k, _, _, hpal⟩ := palindrome_within_seven_of_digitSum_le_ten
    (orbit n t) (orbit_positive n hn t) (by omega)
  apply hlychrel (t + k)
  simpa only [LychrelCertificates.orbit_add] using hpal

end DigitSumTenTermination
