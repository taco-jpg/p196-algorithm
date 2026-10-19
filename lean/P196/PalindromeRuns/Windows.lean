import P196.PalindromeRuns.Basic
import P196.Agent9DigitSumWindows.Agent9WindowIntervalCounts

/-!
Sharp finite windows of nonpalindromes in ordinary positive decimal orbits.
The classification imported from `Basic` concerns consecutive palindromic
states. The window and counting conclusions do not assert that any orbit
avoids all palindromes, or that the lower counting bound is asymptotically sharp.
-/

namespace PalindromeRuns

open Lychrel196 DecimalDigits

/-- A positive orbit cannot contain five consecutive palindromic states,
including the state at time zero. Zero is excluded deliberately. -/
theorem not_five_palindromes (n : Nat) (hn : 0 < n) :
    ¬ (∀ j, j ≤ 4 → Palindrome (orbit n j)) := by
  intro h
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have hbound := ((palindrome_prefix_iff n d L 4 hc).mp h).2
    (L - 1) (by have := hc.1; omega)
  change 16 * d (L - 1) ≤ 9 at hbound
  have hlead := hc.2.2.1
  omega

/-- Every positive seed has a nonpalindromic state among times zero to four. -/
theorem nonpalindrome_first_five (n : Nat) (hn : 0 < n) :
    ∃ j, j ≤ 4 ∧ ¬ Palindrome (orbit n j) := by
  classical
  apply Classical.byContradiction
  intro h
  apply not_five_palindromes n hn
  intro j hj
  exact Classical.byContradiction (fun hp => h ⟨j, hj, hp⟩)

/-- Every inclusive five-state window of an ordinary positive orbit
contains a nonpalindrome. -/
theorem nonpalindrome_in_five (n s : Nat) (hn : 0 < n) :
    ∃ t, s ≤ t ∧ t ≤ s + 4 ∧ ¬ Palindrome (orbit n t) := by
  obtain ⟨j, hj, hp⟩ := nonpalindrome_first_five (orbit n s)
    (orbit_positive n hn s)
  refine ⟨s + j, by omega, by omega, ?_⟩
  simpa only [LychrelCertificates.orbit_add] using hp

/-- At least one state out of every complete five-state block is
nonpalindromic. The interval is `[s, s + N)`. -/
theorem nonpalindrome_interval_count (n s N : Nat) (hn : 0 < n) :
    N / 5 ≤ ((List.range' s N).filter
      (fun t => decide (¬ Palindrome (orbit n t)))).length := by
  apply P196.Agent9.IntervalCounts.window_property_interval_count
    (fun t => ¬ Palindrome (orbit n t)) 5 (by decide)
  intro a
  obtain ⟨t, hlo, hhi, hp⟩ := nonpalindrome_in_five n a hn
  exact ⟨t, hlo, by omega, hp⟩

/-- Exact sharpness control: four consecutive palindromes, followed by
the first nonpalindrome. This concerns the window length, not a density limit. -/
theorem four_palindromes_sharp :
    (∀ j, j ≤ 3 → Palindrome (orbit 1 j)) ∧
      orbit 1 4 = 16 ∧ ¬ Palindrome (orbit 1 4) := by
  decide +kernel

/-- The same four-state run can occur strictly after the initial state. -/
theorem positive_time_four_palindromes :
    ¬ Palindrome 10 ∧
      (∀ j, 1 ≤ j → j ≤ 4 → Palindrome (orbit 10 j)) ∧
      orbit 10 5 = 176 ∧ ¬ Palindrome (orbit 10 5) := by
  have hrun : ∀ j, j ≤ 4 → 1 ≤ j → Palindrome (orbit 10 j) := by
    decide +kernel
  refine ⟨by decide +kernel, ?_, by decide +kernel, by decide +kernel⟩
  intro j hlo hhi
  exact hrun j hhi hlo

end PalindromeRuns
