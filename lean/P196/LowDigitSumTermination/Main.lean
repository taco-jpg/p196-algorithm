import P196.LowDigitSumTermination.CentralCarry
import P196.LowDigitSumTermination.DigitMass

/-!
# Small decimal digit sum forces a palindrome within three steps

The scalar bound applies to every positive integer, with no restriction on
its decimal width. The middle digit of an odd-width numeral is handled by
the exact central-carry lemmas. The original ordinary-integer map is used
throughout. The bound is sharp, and the same three-step conclusion fails
if the digit-sum threshold is raised to ten.

The necessary digit-mass bound for a hypothetical Lychrel orbit is
conditional on that orbit being palindrome-free. No statement here
decides whether the orbit of 196 reaches a palindrome.
-/

namespace LowDigitSumTermination

open DecimalDigits DecimalMass Lychrel196

/-- A positive one-digit seed reaches a palindrome within two steps. -/
theorem single_digit_terminates (n : Nat) (hn : 0 < n) (hsmall : n ≤ 9) :
    ∃ k : Nat, 1 ≤ k ∧ k ≤ 2 ∧ Palindrome (orbit n k) := by
  have hcases : n = 1 ∨ n = 2 ∨ n = 3 ∨ n = 4 ∨ n = 5 ∨
      n = 6 ∨ n = 7 ∨ n = 8 ∨ n = 9 := by omega
  rcases hcases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  all_goals first
    | exact ⟨1, by decide, by decide, by decide⟩
    | exact ⟨2, by decide, by decide, by decide⟩

/-- Every positive ordinary integer with digit sum at most nine reaches a
palindrome in one, two, or three actual reverse-and-add steps. -/
theorem palindrome_within_three_of_digitSum_le_nine
    (n : Nat) (hn : 0 < n) (hs : digitSum n ≤ 9) :
    ∃ k : Nat, 1 ≤ k ∧ k ≤ 3 ∧ Palindrome (orbit n k) := by
  classical
  obtain ⟨d, L, hcan⟩ := canonical_exists n hn
  have hmass : wordSum d L ≤ 9 := by
    rw [← digitSum_value d L hcan.2.1, hcan.2.2.2]
    exact hs
  by_cases hsingle : L = 1
  · have hnsmall : n ≤ 9 := by
      have hd := hcan.2.1 0 (by omega)
      have hv := hcan.2.2.2
      simp only [hsingle, value, Nat.pow_zero, Nat.mul_one, Nat.zero_add] at hv
      omega
    obtain ⟨k, hkpos, hkbound, hp⟩ := single_digit_terminates n hn hnsmall
    exact ⟨k, hkpos, by omega, hp⟩
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
  have hmid : m = L - 1 - m := by
    apply Classical.byContradiction
    intro hne
    have hpair := wordSum_pair_le d L m (L - 1 - m) hmL (by omega) hne
    simp only [columnSum, reflected] at hmhigh
    omega
  have hwidth : L = 2 * m + 1 := by omega
  subst L
  have hm : 0 < m := by omega
  have hcenter : columnSum d (2 * m + 1) m = 2 * d m := by
    have heq : 2 * m + 1 - 1 - m = m := by omega
    simp only [columnSum, reflected, heq]
    omega
  have hdmin : 5 ≤ d m := by omega
  have hleadmass := wordSum_pair_le d (2 * m + 1) m
    (2 * m + 1 - 1) (by omega) (by omega) (by omega)
  have hlead := hcan.2.2.1
  have hdmax : d m ≤ 8 := by omega
  by_cases height : d m = 8
  · have hext : ∀ i, i < 2 * m + 1 → i ≠ m →
        columnSum d (2 * m + 1) i ≤ 1 := by
      intro i hi hne
      have hb := noncentral_column_add_middle_le_mass d m i hi hne
      omega
    have hp := central_three_steps_palindrome n d m hm hcan
      (by omega) hext
    exact ⟨3, by decide, by decide, hp⟩
  · have hext : ∀ i, i < 2 * m + 1 → i ≠ m →
        columnSum d (2 * m + 1) i ≤ 4 := by
      intro i hi hne
      have hb := noncentral_column_add_middle_le_mass d m i hi hne
      omega
    have hp := central_two_steps_palindrome n d m hm hcan
      (by omega) (by omega) hext
    exact ⟨2, by decide, by decide, hp⟩

/-- The bound three is attained: 180, 261, and 423 are nonpalindromes,
and the next state is the palindrome 747. -/
theorem sharp_example_180 :
    digitSum 180 = 9 ∧
    (∀ k, k < 3 → ¬ Palindrome (orbit 180 k)) ∧
    orbit 180 3 = 747 ∧ Palindrome (orbit 180 3) := by
  exact ⟨by simp [digitSum], noPalindromeFor_sound 3 180 (by decide), by decide, by decide⟩

/-- Raising the digit-sum threshold to ten does not preserve the
three-step bound: the first palindrome from 190 occurs at time seven. -/
theorem threshold_control_190 :
    digitSum 190 = 10 ∧
    (∀ k, k < 7 → ¬ Palindrome (orbit 190 k)) ∧
    orbit 190 7 = 45254 ∧ Palindrome (orbit 190 7) := by
  exact ⟨by simp [digitSum], noPalindromeFor_sound 7 190 (by decide), by decide, by decide⟩

/-- Every point of a hypothetical palindrome-free decimal orbit has
digit sum at least ten. This implication supplies no Lychrel seed. -/
theorem lychrel_orbit_digitSum_ge_ten
    (n : Nat) (hlychrel : IsLychrel n) (t : Nat) :
    10 ≤ digitSum (orbit n t) := by
  have hn : 0 < n := by
    apply Classical.byContradiction
    intro hnonpos
    have hnzero : n = 0 := by omega
    subst n
    exact hlychrel 0 (by decide)
  apply Classical.byContradiction
  intro hmass
  obtain ⟨k, _, _, hpal⟩ := palindrome_within_three_of_digitSum_le_nine
    (orbit n t) (orbit_positive n hn t) (by omega)
  apply hlychrel (t + k)
  simpa only [LychrelCertificates.orbit_add] using hpal

end LowDigitSumTermination
