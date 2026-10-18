import P196.Drafts.Agent3TwoHistory.ActualHistories
import P196.Agent101ProtectedFamily.IntegerInterfaces
import P196.Agent101ProtectedFamily.FiniteHorizonTheorem

/-!
Ordinary-integer safety for the explicit two incoming histories.
The history transitions are imported from `ActualHistories`; the integer
transition and finite-horizon safety arguments use the existing interfaces.
Every conclusion concerns a prescribed finite horizon.
-/

namespace P196.Agent3.TwoHistory

open Lychrel196
open P196.Agent3.OverflowHorizon

theorem history_realizes_one (xs : List Bool) (k n : Nat)
    (hr : IntegerRealizes n (historyWord0 xs k)) :
    IntegerRealizes (orbit n 1) (historyWord1 xs k) := by
  have hnext := integer_realizes_next n (historyWord0 xs k)
    (historyWord0_canonical xs k) hr
  simpa only [historyWord0_step] using hnext

theorem history_realizes_two (xs : List Bool) (k n : Nat)
    (hr : IntegerRealizes n (historyWord0 xs k)) :
    IntegerRealizes (orbit n 2) (historyWord2 xs k) := by
  have hnext := integer_realizes_next (orbit n 1) (historyWord1 xs k)
    (historyWord1_canonical xs k) (history_realizes_one xs k n hr)
  simpa only [historyWord1_step] using hnext

/-- At time three, every original realization reaches the already proved
normalized output of the completed protected family word. -/
theorem history_orbit_three (xs : List Bool) (k n : Nat)
    (hr : IntegerRealizes n (historyWord0 xs k)) :
    orbit n 3 = digitValue (Agent8.normalize (inputWord (completedBits xs) k) 0) := by
  have hstep := integer_step_of_realizes (orbit n 2) (historyWord2 xs k)
    (history_realizes_two xs k n hr)
  simpa only [historyWord2] using hstep

/-- Every ordinary realization of the initial history word avoids
palindromes at all times from zero through `k + 3`. -/
theorem history_integer_safe_prefix (xs : List Bool) (k : Nat) (hk : 0 < k)
    (n : Nat) (hr : IntegerRealizes n (historyWord0 xs k)) :
    ∀ t, t ≤ k + 3 → ¬ Palindrome (orbit n t) := by
  intro t ht
  by_cases hsmall : t < 3
  · have hcases : t = 0 ∨ t = 1 ∨ t = 2 := by omega
    rcases hcases with rfl | rfl | rfl
    · exact integer_nonpalindrome_of_odd_outer n (historyWord0 xs k) hr
        (by rw [historyWord0_head])
    · exact integer_nonpalindrome_of_odd_outer (orbit n 1) (historyWord1 xs k)
        (history_realizes_one xs k n hr) (by rw [historyWord1_head])
    · exact integer_step_nonpalindrome_of_eighteen (orbit n 1) (historyWord1 xs k)
        (history_realizes_one xs k n hr) (historyWord1_has_eighteen xs k hk)
  · have htime : 3 + (t - 3) = t := by omega
    have hsplit := LychrelCertificates.orbit_add n 3 (t - 3)
    rw [htime] at hsplit
    rw [hsplit, history_orbit_three xs k n hr]
    exact (inputWord_normalized_safe (completedBits xs) k hk).2 (t - 3) (by omega)

/-- The ordinary integer at time four depends only on the original free
choice length and the reservoir length, not on the choices or realization. -/
theorem history_integer_common_time_four (xs : List Bool) (k : Nat) (hk : 0 < k)
    (n : Nat) (hr : IntegerRealizes n (historyWord0 xs k)) :
    orbit n 4 = digitValue (target (xs.length + 6) k) := by
  change step (orbit n 3) = digitValue (target (xs.length + 6) k)
  rw [history_orbit_three xs k n hr]
  simpa only [completedBits_length, digitValue, digitColumn, targetColumn] using
    inputWord_common_next_value (completedBits xs) k hk

/-- The complete numeric conclusion for any canonical original realization. -/
theorem history_integer_realization_package (xs : List Bool) (k : Nat) (hk : 0 < k)
    (n : Nat) (hr : IntegerRealizes n (historyWord0 xs k)) :
    0 < n ∧
      (∀ t, t ≤ k + 3 → ¬ Palindrome (orbit n t)) ∧
      orbit n 4 = digitValue (target (xs.length + 6) k) := by
  exact ⟨integer_realizes_positive n (historyWord0 xs k) hr,
    history_integer_safe_prefix xs k hk n hr,
    history_integer_common_time_four xs k hk n hr⟩

/-- Every free choice word has a positive original integer realizing the
initial history, with the full finite safe prefix and common time-four value. -/
theorem history_positive_integer_exists (xs : List Bool) (k : Nat) (hk : 0 < k) :
    ∃ n, 0 < n ∧ IntegerRealizes n (historyWord0 xs k) ∧
      (∀ t, t ≤ k + 3 → ¬ Palindrome (orbit n t)) ∧
      orbit n 4 = digitValue (target (xs.length + 6) k) := by
  obtain ⟨n, hn, hr⟩ := even_canonical_realizable (historyWord0 xs k)
    (historyWord0_canonical xs k) (historyWord0_even xs k)
  obtain ⟨_, hsafe, hcommon⟩ := history_integer_realization_package xs k hk n hr
  exact ⟨n, hn, hr, hsafe, hcommon⟩

end P196.Agent3.TwoHistory
