import P196.SymmetricCarryCensus.Counts

/-!
# Cumulative counts of the original admissible coefficient words

Agent #6: the existing shortWordsK list already concatenates the original
symWords enumeration at every smaller width. Adjoining two widths gives
the exact parity formulas without a second word generator or a geometric
series library. Their recurrence implies the cubic decimal bound.

These are candidate coefficient-word counts. Numerical coincidences can
only decrease the distinct ordinary image count in the subsequent bridge.
-/

set_option autoImplicit false

namespace OrdinaryImageSparsity

open Agent124.PrefixK SymmetricCarryCensus

/-- Number of original admissible coefficient words at widths zero
through W, before evaluation, cutoff filtering, or duplicate removal. -/
def profileCount (W : Nat) : Nat := (shortWordsK (W + 1)).length

private theorem profileCount_next (W : Nat) :
    profileCount (W + 1) = profileCount W + wordCount (W + 1) := by
  unfold profileCount shortWordsK
  rw [List.range_succ, List.flatMap_append, List.flatMap_singleton,
    List.length_append, symWords_length]

private theorem profileCount_two_widths (W : Nat) :
    profileCount (W + 2) = profileCount W + wordCount (W + 1) +
      wordCount (W + 2) := by
  simp only [profileCount_next]

private theorem wordCount_even (k : Nat) :
    wordCount (2 * k + 2) = 18 * 19 ^ k := by
  have h0 : 2 * k + 2 ≠ 0 := by omega
  have h1 : 2 * k + 2 ≠ 1 := by omega
  have hdiv : (2 * k + 2) / 2 - 1 = k := by omega
  have hmod : (2 * k + 2) % 2 = 0 := by omega
  simp only [wordCount, if_neg h0, if_neg h1, hdiv, hmod,
    if_pos rfl, if_true, Nat.mul_one]

private theorem wordCount_odd (k : Nat) :
    wordCount (2 * k + 3) = 180 * 19 ^ k := by
  have h0 : 2 * k + 3 ≠ 0 := by omega
  have h1 : 2 * k + 3 ≠ 1 := by omega
  have hdiv : (2 * k + 3) / 2 - 1 = k := by omega
  have hmod : (2 * k + 3) % 2 = 1 := by omega
  simp only [wordCount, if_neg h0, if_neg h1, hdiv, hmod,
    if_neg (by decide : (1 : Nat) ≠ 0)]
  omega

/-- The original width-zero family is empty. -/
theorem profileCount_zero : profileCount 0 = 0 := by
  rfl

/-- A singleton coefficient has nine positive even choices. -/
theorem profileCount_one : profileCount 1 = 9 := by
  rw [profileCount_next, profileCount_zero]
  rfl

/-- Widths one and two contribute nine and eighteen words. -/
theorem profileCount_two : profileCount 2 = 27 := by
  rw [profileCount_next, profileCount_one]
  rfl

/-- Width three adds eighteen outer choices and ten center choices. -/
theorem profileCount_three : profileCount 3 = 207 := by
  rw [profileCount_next, profileCount_two]
  rfl

/-- Exact cumulative count through every positive odd source width. -/
theorem profileCount_odd (k : Nat) :
    profileCount (2 * k + 1) + 2 = 11 * 19 ^ k := by
  induction k with
  | zero =>
    simp only [Nat.mul_zero, Nat.zero_add, profileCount_one,
      Nat.pow_zero, Nat.mul_one]
  | succ k ih =>
    have heven := wordCount_even k
    have hodd := wordCount_odd k
    rw [show 2 * k + 2 = (2 * k + 1) + 1 by omega] at heven
    rw [show 2 * k + 3 = (2 * k + 1) + 2 by omega] at hodd
    rw [show 2 * (k + 1) + 1 = (2 * k + 1) + 2 by omega,
      profileCount_two_widths, heven, hodd]
    simp only [Nat.pow_succ]
    omega

/-- Exact cumulative count through every positive even source width. -/
theorem profileCount_even (k : Nat) :
    profileCount (2 * k + 2) + 2 = 29 * 19 ^ k := by
  induction k with
  | zero =>
    simp only [Nat.mul_zero, Nat.zero_add, profileCount_two,
      Nat.pow_zero, Nat.mul_one]
  | succ k ih =>
    have hodd := wordCount_odd k
    have heven := wordCount_even (k + 1)
    rw [show 2 * k + 3 = (2 * k + 2) + 1 by omega] at hodd
    rw [show 2 * (k + 1) + 2 = (2 * k + 2) + 2 by omega] at heven
    rw [show 2 * (k + 1) + 2 = (2 * k + 2) + 2 by omega,
      profileCount_two_widths, hodd, heven]
    simp only [Nat.pow_succ]
    omega

/-- Two additional source widths multiply the cumulative count by
nineteen and contribute the fixed boundary correction. -/
theorem profileCount_recurrence (W : Nat) (hW : 1 ≤ W) :
    profileCount (W + 2) = 19 * profileCount W + 36 := by
  rcases Nat.mod_two_eq_zero_or_one W with heven | hodd
  · obtain ⟨k, rfl⟩ : ∃ k, W = 2 * k + 2 := ⟨W / 2 - 1, by omega⟩
    have hfirst := profileCount_even k
    have hnext := profileCount_even (k + 1)
    rw [show 2 * (k + 1) + 2 = (2 * k + 2) + 2 by omega] at hnext
    simp only [Nat.pow_succ] at hnext
    omega
  · obtain ⟨k, rfl⟩ : ∃ k, W = 2 * k + 1 := ⟨W / 2, by omega⟩
    have hfirst := profileCount_odd k
    have hnext := profileCount_odd (k + 1)
    rw [show 2 * (k + 1) + 1 = (2 * k + 1) + 2 by omega] at hnext
    simp only [Nat.pow_succ] at hnext
    omega

private theorem profileCount_ge_eighteen (W : Nat) (hW : 2 ≤ W) :
    18 ≤ profileCount W := by
  have hprefix : profileCount 2 ≤ profileCount W := by
    unfold profileCount shortWordsK
    rw [show W + 1 = 3 + (W - 2) by omega,
      List.range_add (n := 3) (m := W - 2), List.flatMap_append,
      List.length_append]
    exact Nat.le_add_right _ _
  rw [profileCount_two] at hprefix
  omega

private theorem profileCount_growth (W : Nat) (hW : 2 ≤ W) :
    profileCount (W + 2) ≤ 21 * profileCount W := by
  rw [profileCount_recurrence W (by omega)]
  have h := profileCount_ge_eighteen W hW
  omega

/-- The cumulative coefficient-word count obeys a uniform cubic bound
at every decimal power, including all exceptional initial widths. -/
theorem profileCount_cubic (W : Nat) :
    profileCount W ^ 3 ≤ 9 * 10 ^ (2 * W) := by
  induction W using Nat.strongRecOn with
  | ind W ih =>
    match W with
    | 0 => rw [profileCount_zero]; decide
    | 1 => rw [profileCount_one]; decide
    | 2 => rw [profileCount_two]; decide
    | 3 => rw [profileCount_three]; decide
    | k + 4 =>
      have hstep := profileCount_growth (k + 2) (by omega)
      have hprevious := ih (k + 2) (by omega)
      calc
        profileCount (k + 4) ^ 3 ≤ (21 * profileCount (k + 2)) ^ 3 :=
          Nat.pow_le_pow_left hstep 3
        _ = 21 ^ 3 * profileCount (k + 2) ^ 3 := Nat.mul_pow _ _ _
        _ ≤ 21 ^ 3 * (9 * 10 ^ (2 * (k + 2))) :=
          Nat.mul_le_mul_left _ hprevious
        _ ≤ 10 ^ 4 * (9 * 10 ^ (2 * (k + 2))) :=
          Nat.mul_le_mul_right _ (by decide : (21 : Nat) ^ 3 ≤ 10 ^ 4)
        _ = 9 * 10 ^ (2 * (k + 4)) := by
          rw [show 2 * (k + 4) = 4 + 2 * (k + 2) by omega,
            Nat.pow_add 10 4 (2 * (k + 2))]
          simp only [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]

end OrdinaryImageSparsity

#print axioms OrdinaryImageSparsity.profileCount
#print axioms OrdinaryImageSparsity.profileCount_zero
#print axioms OrdinaryImageSparsity.profileCount_one
#print axioms OrdinaryImageSparsity.profileCount_two
#print axioms OrdinaryImageSparsity.profileCount_three
#print axioms OrdinaryImageSparsity.profileCount_odd
#print axioms OrdinaryImageSparsity.profileCount_even
#print axioms OrdinaryImageSparsity.profileCount_recurrence
#print axioms OrdinaryImageSparsity.profileCount_cubic
