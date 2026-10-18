import P196.Drafts.D20261015ExternalIntrinsicReviewSources.SeamAnnihilation

/-!
Ordinary digit-sum consequences of strengthening_notes.txt, section 8.

The framed-nine family, its canonical realizations, its exact first numeric
output, and its two-step palindrome behavior are the unchanged original
SeamAnnihilation results. This module adds their scalar digit-sum consequence.
The universal scalar equalities include r = 0; the existential family uses
r > 0, matching the manuscript's even k >= 2 with k = 2*r.
-/

namespace P196.Agent9.OneStepDigitSumCollapse

open DecimalDigits DecimalMass SeamAnnihilation

/-- The initial endpoint 10 followed by a finite prefix of n interior nines. -/
theorem framedNine_prefix_wordSum (k n : Nat) (hn : n ≤ k) :
    wordSum (framedNine k) (n + 1) = 9 * n + 10 := by
  induction n with
  | zero => simp [wordSum, framedNine]
  | succ n ih =>
    rw [wordSum, ih (by omega)]
    have h : ¬ (n + 1 = 0 ∨ n + 1 = k + 1) := by omega
    simp only [framedNine, if_neg h]
    omega

/-- The pair-word sum is 20 plus nine times its interior length. -/
theorem framedNine_wordSum (k : Nat) :
    wordSum (framedNine k) (k + 2) = 9 * k + 20 := by
  change wordSum (framedNine k) ((k + 1) + 1) = _
  rw [wordSum, framedNine_prefix_wordSum k k (Nat.le_refl k)]
  simp only [framedNine, or_true, if_true]

/-- Every canonical realization has half the pair-word sum as digit sum. -/
theorem framedNine_realization_digitSum_double (k n : Nat) (d : Nat → Nat)
    (hc : Canonical n d (k + 2))
    (hr : ∀ i, i < k + 2 → columnSum d (k + 2) i = framedNine k i) :
    2 * digitSum n = 9 * k + 20 := by
  calc
    2 * digitSum n = 2 * wordSum d (k + 2) := by
      rw [← hc.2.2.2, digitSum_value d (k + 2) hc.2.1]
    _ = wordSum (columnSum d (k + 2)) (k + 2) :=
      (wordSum_columns d (k + 2)).symm
    _ = wordSum (framedNine k) (k + 2) :=
      wordSum_congr _ _ _ hr
    _ = 9 * k + 20 := framedNine_wordSum k

/-- Exact input digit sum, including the degenerate parameter r = 0. -/
theorem framedNine_realization_digitSum (r n : Nat) (d : Nat → Nat)
    (hc : Canonical n d (2 * r + 2))
    (hr : ∀ i, i < 2 * r + 2 →
      columnSum d (2 * r + 2) i = framedNine (2 * r) i) :
    digitSum n = 9 * r + 10 := by
  have h := framedNine_realization_digitSum_double (2 * r) n d hc hr
  omega

/-- The carried prefix preceding the first output one has digit sum zero. -/
theorem framedNine_output_prefix_wordSum (k n : Nat) (hn : n ≤ k + 1) :
    wordSum (output (framedNine k)) n = 0 := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [wordSum, ih (by omega), framedNine_output]
    have h : n ≠ k + 1 := by omega
    simp [h]

/-- The ordinary digit sum after the actual numeric update is exactly two. -/
theorem framedNine_realization_step_digitSum (k n : Nat) (d : Nat → Nat)
    (hc : Canonical n d (k + 2))
    (hr : ∀ i, i < k + 2 → columnSum d (k + 2) i = framedNine k i) :
    digitSum (Lychrel196.step n) = 2 := by
  have he : ∀ i, i < (k + 2) + 1 →
      extended (framedNine k) (k + 2) i ≤ 9 := by
    intro i _
    rw [framedNine_extended]
    split <;> omega
  have ho : wordSum (output (framedNine k)) (k + 2) = 1 := by
    change wordSum (output (framedNine k)) ((k + 1) + 1) = 1
    rw [wordSum, framedNine_output_prefix_wordSum k (k + 1) (Nat.le_refl _),
      framedNine_output]
    simp
  calc
    digitSum (Lychrel196.step n) = digitSum (value (framedNine k) (k + 2)) := by
      rw [framedNine_realization_step_value k n d hc hr, framedNine_value]
    _ = digitSum (value (extended (framedNine k) (k + 2)) ((k + 2) + 1)) := by
      rw [value_extended, value_output]
    _ = wordSum (extended (framedNine k) (k + 2)) ((k + 2) + 1) :=
      digitSum_value _ _ he
    _ = 2 := by
      rw [wordSum_extended, ho, framedNine_carry]
      simp

/-- Universal scalar conclusion for every realization, including r = 0. -/
theorem framedNine_realization_digitSums (r n : Nat) (d : Nat → Nat)
    (hc : Canonical n d (2 * r + 2))
    (hr : ∀ i, i < 2 * r + 2 →
      columnSum d (2 * r + 2) i = framedNine (2 * r) i) :
    digitSum n = 9 * r + 10 ∧ digitSum (Lychrel196.step n) = 2 := by
  exact ⟨framedNine_realization_digitSum r n d hc hr,
    framedNine_realization_step_digitSum (2 * r) n d hc hr⟩

/-- Positive canonical witnesses come from the unchanged original realization. -/
theorem framedNine_digitSums_realized (r : Nat) (hr : 0 < r) :
    ∃ n d, 0 < n ∧ Canonical n d (2 * r + 2) ∧
      (∀ i, i < 2 * r + 2 →
        columnSum d (2 * r + 2) i = framedNine (2 * r) i) ∧
      digitSum n = 9 * r + 10 ∧ digitSum (Lychrel196.step n) = 2 := by
  obtain ⟨n, d, hp, hc, hq, _⟩ := even_family_realized r hr
  exact ⟨n, d, hp, hc, hq, framedNine_realization_digitSums r n d hc hq⟩

/-- One positive finite integer simultaneously exceeds both thresholds. -/
theorem arbitrarily_large_digitSum_and_width (B : Nat) :
    ∃ n d L, 0 < n ∧ Canonical n d L ∧
      B < digitSum n ∧ B < L ∧ digitSum (Lychrel196.step n) = 2 := by
  obtain ⟨n, d, hp, hc, _, hs, ht⟩ :=
    framedNine_digitSums_realized (B + 1) (by omega)
  exact ⟨n, d, 2 * (B + 1) + 2, hp, hc, by omega, by omega, ht⟩

/-- Arbitrarily large initial ordinary digit sum can collapse to two. -/
theorem arbitrarily_large_digitSum (B : Nat) :
    ∃ n, 0 < n ∧ B < digitSum n ∧ digitSum (Lychrel196.step n) = 2 := by
  obtain ⟨n, _, _, hp, _, hs, _, ht⟩ := arbitrarily_large_digitSum_and_width B
  exact ⟨n, hp, hs, ht⟩

end P196.Agent9.OneStepDigitSumCollapse
