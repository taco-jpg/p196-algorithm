import P196.Foundations.LychrelDigitSums

/-!
An isolated high central pair coefficient produces exactly one actual carry.
The resulting bounds concern the ordinary decimal reverse-and-add map through
the existing canonical-digit bridge. No infinite palindrome-free orbit is
constructed or ruled out by these local statements.
-/

namespace LowDigitSumTermination

open DecimalDigits FoldedDecimal Lychrel196

/-- A high central coefficient surrounded by coefficients at most eight has
exactly one nonzero actual carry, immediately after the central column. -/
theorem central_carry_exact (q : Nat → Nat) (m : Nat) (_hm : 0 < m)
    (hlo : 10 ≤ q m) (hhi : q m ≤ 18)
    (hsmall : ∀ j, j < 2 * m + 1 → j ≠ m → q j ≤ 8)
    (i : Nat) (hi : i ≤ 2 * m + 1) :
    carry q i = if i = m + 1 then 1 else 0 := by
  induction i with
  | zero => simp [carry]
  | succ i ih =>
    have hprev := ih (by omega)
    simp only [carry]
    rw [hprev]
    by_cases hic : i = m
    · subst i
      have hne : m ≠ m + 1 := by omega
      have hdiv : q m / 10 = 1 := by omega
      simpa [hne] using hdiv
    · have hbound := hsmall i (by omega) hic
      have hne : i + 1 ≠ m + 1 := by omega
      simp only [if_neg hne]
      by_cases hip : i = m + 1
      · simp only [if_pos hip]
        omega
      · simp only [if_neg hip, Nat.add_zero]
        omega

/-- The isolated central carry stops before the high end of the word. -/
theorem central_carry_no_overflow (q : Nat → Nat) (m : Nat) (hm : 0 < m)
    (hlo : 10 ≤ q m) (hhi : q m ≤ 18)
    (hsmall : ∀ j, j < 2 * m + 1 → j ≠ m → q j ≤ 8) :
    carry q (2 * m + 1) = 0 := by
  have hc := central_carry_exact q m hm hlo hhi hsmall (2 * m + 1) (by omega)
  have hne : 2 * m + 1 ≠ m + 1 := by omega
  simpa only [if_neg hne] using hc

/-- Exact center update, expressed without truncated subtraction. -/
theorem central_next_center (q : Nat → Nat) (m : Nat) (hm : 0 < m)
    (hlo : 10 ≤ q m) (hhi : q m ≤ 18)
    (hsmall : ∀ j, j < 2 * m + 1 → j ≠ m → q j ≤ 8)
    (hsym : ∀ j, j < 2 * m + 1 → q j = q (2 * m + 1 - 1 - j)) :
    nextColumns q (2 * m + 1) m + 20 = 2 * q m := by
  have hc := central_carry_no_overflow q m hm hlo hhi hsmall
  have heq := next_column_no_overflow q (2 * m + 1) m (by omega) hsym hc
  have hm0 : carry q m = 0 := by
    have h := central_carry_exact q m hm hlo hhi hsmall m (by omega)
    have hne : m ≠ m + 1 := by omega
    simpa [hne] using h
  have hm1 : carry q (m + 1) = 1 := by
    simpa using central_carry_exact q m hm hlo hhi hsmall (m + 1) (by omega)
  have hright : 2 * m + 1 - m = m + 1 := by omega
  have hreflect : 2 * m + 1 - 1 - m = m := by omega
  rw [hright, hreflect, hm0, hm1] at heq
  omega

/-- Outside the center, the next coefficient is at most twice the old one
plus one; the two reflected positions cannot both receive the isolated carry. -/
theorem central_next_exterior_bound (q : Nat → Nat) (m : Nat) (hm : 0 < m)
    (hlo : 10 ≤ q m) (hhi : q m ≤ 18)
    (hsmall : ∀ j, j < 2 * m + 1 → j ≠ m → q j ≤ 8)
    (hsym : ∀ j, j < 2 * m + 1 → q j = q (2 * m + 1 - 1 - j))
    (i : Nat) (hi : i < 2 * m + 1) (_hic : i ≠ m) :
    nextColumns q (2 * m + 1) i ≤ 2 * q i + 1 := by
  have hc := central_carry_no_overflow q m hm hlo hhi hsmall
  have heq := next_column_no_overflow q (2 * m + 1) i hi hsym hc
  have hl := central_carry_exact q m hm hlo hhi hsmall i (by omega)
  have hr := central_carry_exact q m hm hlo hhi hsmall
    (2 * m + 1 - 1 - i) (by omega)
  have hsum : carry q i + carry q (2 * m + 1 - 1 - i) ≤ 1 := by
    rw [hl, hr]
    by_cases hil : i = m + 1
    · have hir : 2 * m + 1 - 1 - i ≠ m + 1 := by omega
      simp only [if_pos hil, if_neg hir]
      omega
    · by_cases hir : 2 * m + 1 - 1 - i = m + 1
      · simp only [if_neg hil, if_pos hir]
        omega
      · simp only [if_neg hil, if_neg hir]
        omega
  omega

/-- An ordinary canonical input with central pair coefficient 10 through 14
and all other pair coefficients at most four has a palindromic second step. -/
theorem central_two_steps_palindrome (n : Nat) (d : Nat → Nat) (m : Nat)
    (hm : 0 < m) (hcan : Canonical n d (2 * m + 1))
    (hlo : 10 ≤ columnSum d (2 * m + 1) m)
    (hhi : columnSum d (2 * m + 1) m ≤ 14)
    (hsmall : ∀ i, i < 2 * m + 1 → i ≠ m →
      columnSum d (2 * m + 1) i ≤ 4) :
    Palindrome (step (step n)) := by
  let q := columnSum d (2 * m + 1)
  have hsmall8 : ∀ i, i < 2 * m + 1 → i ≠ m → q i ≤ 8 := by
    intro i hi hic
    have h := hsmall i hi hic
    change q i ≤ 4 at h
    omega
  have hqhi : q m ≤ 18 := by change q m ≤ 14 at hhi; omega
  have hsym : ∀ i, i < 2 * m + 1 → q i = q (2 * m + 1 - 1 - i) :=
    columnSum_symmetric d (2 * m + 1)
  have hc := central_carry_no_overflow q m hm hlo hqhi hsmall8
  have hcan' := canonical_next_no_overflow n d (2 * m + 1) hcan hc
  have hcols : ∀ i, i < 2 * m + 1 →
      columnSum (output q) (2 * m + 1) i ≤ 9 := by
    intro i hi
    have heq : nextColumns q (2 * m + 1) i =
        columnSum (output q) (2 * m + 1) i := by
      simp only [nextColumns, hc, ite_true]
    by_cases hic : i = m
    · subst i
      have hcenter := central_next_center q m hm hlo hqhi hsmall8 hsym
      rw [heq] at hcenter
      change q m ≤ 14 at hhi
      omega
    · have hbound := central_next_exterior_bound q m hm hlo hqhi hsmall8 hsym i hi hic
      rw [heq] at hbound
      have hfour := hsmall i hi hic
      change q i ≤ 4 at hfour
      omega
  rcases hcan' with ⟨hL, hd', hlead', hv'⟩
  have hp := (step_palindrome_iff (output q) (2 * m + 1) hL hd' hlead').mpr
    (Or.inl hcols)
  rw [hv'] at hp
  exact hp

/-- Central coefficient sixteen and all other coefficients at most one
reduce to the preceding criterion after one actual step. -/
theorem central_three_steps_palindrome (n : Nat) (d : Nat → Nat) (m : Nat)
    (hm : 0 < m) (hcan : Canonical n d (2 * m + 1))
    (hcenter : columnSum d (2 * m + 1) m = 16)
    (hsmall : ∀ i, i < 2 * m + 1 → i ≠ m →
      columnSum d (2 * m + 1) i ≤ 1) :
    Palindrome (step (step (step n))) := by
  let q := columnSum d (2 * m + 1)
  have hsmall8 : ∀ i, i < 2 * m + 1 → i ≠ m → q i ≤ 8 := by
    intro i hi hic
    have h := hsmall i hi hic
    change q i ≤ 1 at h
    omega
  have hlo : 10 ≤ q m := by change q m = 16 at hcenter; omega
  have hhi : q m ≤ 18 := by change q m = 16 at hcenter; omega
  have hsym : ∀ i, i < 2 * m + 1 → q i = q (2 * m + 1 - 1 - i) :=
    columnSum_symmetric d (2 * m + 1)
  have hc := central_carry_no_overflow q m hm hlo hhi hsmall8
  have hcan' := canonical_next_no_overflow n d (2 * m + 1) hcan hc
  have heq : ∀ i, nextColumns q (2 * m + 1) i =
      columnSum (output q) (2 * m + 1) i := by
    intro i
    simp only [nextColumns, hc, ite_true]
  have hnextcenter : columnSum (output q) (2 * m + 1) m = 12 := by
    have h := central_next_center q m hm hlo hhi hsmall8 hsym
    rw [heq m] at h
    change q m = 16 at hcenter
    omega
  have hnextsmall : ∀ i, i < 2 * m + 1 → i ≠ m →
      columnSum (output q) (2 * m + 1) i ≤ 4 := by
    intro i hi hic
    have h := central_next_exterior_bound q m hm hlo hhi hsmall8 hsym i hi hic
    rw [heq i] at h
    have hsource := hsmall i hi hic
    change q i ≤ 1 at hsource
    omega
  exact central_two_steps_palindrome (step n) (output q) m hm hcan'
    (by omega) (by omega) hnextsmall

end LowDigitSumTermination
