import P196.LowDigitSumTermination.Main

/-!
The isolated central carry changes only the two adjacent exterior pair
coefficients. Keeping this location information strengthens the scalar
termination argument while retaining the original ordinary integer map.
-/

namespace DigitSumTenTermination

open DecimalDigits FoldedDecimal Lychrel196

/-- Away from the high center, a pair coefficient doubles, with an extra
one exactly at the two positions adjacent to that center. -/
theorem central_next_exterior_exact (q : Nat → Nat) (m : Nat) (hm : 0 < m)
    (hlo : 10 ≤ q m) (hhi : q m ≤ 18)
    (hsmall : ∀ j, j < 2 * m + 1 → j ≠ m → q j ≤ 8)
    (hsym : ∀ j, j < 2 * m + 1 → q j = q (2 * m + 1 - 1 - j))
    (i : Nat) (hi : i < 2 * m + 1) (hic : i ≠ m) :
    nextColumns q (2 * m + 1) i =
      2 * q i + (if i + 1 = m ∨ i = m + 1 then 1 else 0) := by
  have hc := LowDigitSumTermination.central_carry_no_overflow q m hm hlo hhi hsmall
  have heq := next_column_no_overflow q (2 * m + 1) i hi hsym hc
  have hloOut : carry q (i + 1) = 0 := by
    have h := LowDigitSumTermination.central_carry_exact q m hm hlo hhi hsmall
      (i + 1) (by omega)
    have hne : i + 1 ≠ m + 1 := by omega
    simpa only [if_neg hne] using h
  have hhiOut : carry q (2 * m + 1 - i) = 0 := by
    have h := LowDigitSumTermination.central_carry_exact q m hm hlo hhi hsmall
      (2 * m + 1 - i) (by omega)
    have hne : 2 * m + 1 - i ≠ m + 1 := by omega
    simpa only [if_neg hne] using h
  have hloIn := LowDigitSumTermination.central_carry_exact q m hm hlo hhi hsmall
    i (by omega)
  have hhiIn := LowDigitSumTermination.central_carry_exact q m hm hlo hhi hsmall
    (2 * m + 1 - 1 - i) (by omega)
  have hreflect : (2 * m + 1 - 1 - i = m + 1) ↔ i + 1 = m := by omega
  simp only [hreflect] at hhiIn
  have hsum : carry q i + carry q (2 * m + 1 - 1 - i) =
      if i + 1 = m ∨ i = m + 1 then 1 else 0 := by
    rw [hloIn, hhiIn]
    by_cases hleft : i + 1 = m
    · have hright : i ≠ m + 1 := by omega
      have hnear : i + 1 = m ∨ i = m + 1 := Or.inl hleft
      simp only [if_neg hright, if_pos hleft, if_pos hnear]
    · by_cases hright : i = m + 1
      · have hnear : i + 1 = m ∨ i = m + 1 := Or.inr hright
        simp only [if_pos hright, if_neg hleft, if_pos hnear]
      · have hnear : ¬ (i + 1 = m ∨ i = m + 1) := by omega
        simp only [if_neg hright, if_neg hleft, if_neg hnear]
  rw [hloOut, hhiOut] at heq
  omega

/-- Central coefficient sixteen, exterior coefficients at most two, and
adjacent coefficients at most one give a palindromic third ordinary step. -/
theorem central_three_steps_refined (n : Nat) (d : Nat → Nat) (m : Nat)
    (hm : 0 < m) (hcan : Canonical n d (2 * m + 1))
    (hcenter : columnSum d (2 * m + 1) m = 16)
    (hsmall : ∀ i, i < 2 * m + 1 → i ≠ m →
      columnSum d (2 * m + 1) i ≤ 2)
    (hnear : ∀ i, i < 2 * m + 1 → (i + 1 = m ∨ i = m + 1) →
      columnSum d (2 * m + 1) i ≤ 1) :
    Palindrome (step (step (step n))) := by
  let q := columnSum d (2 * m + 1)
  have hsmall8 : ∀ i, i < 2 * m + 1 → i ≠ m → q i ≤ 8 := by
    intro i hi hic
    have h := hsmall i hi hic
    change q i ≤ 2 at h
    omega
  have hlo : 10 ≤ q m := by change q m = 16 at hcenter; omega
  have hhi : q m ≤ 18 := by change q m = 16 at hcenter; omega
  have hsym : ∀ i, i < 2 * m + 1 → q i = q (2 * m + 1 - 1 - i) :=
    columnSum_symmetric d (2 * m + 1)
  have hc := LowDigitSumTermination.central_carry_no_overflow q m hm hlo hhi hsmall8
  have hcan' := canonical_next_no_overflow n d (2 * m + 1) hcan hc
  have heq : ∀ i, nextColumns q (2 * m + 1) i =
      columnSum (output q) (2 * m + 1) i := by
    intro i
    simp only [nextColumns, hc, ite_true]
  have hnextcenter : columnSum (output q) (2 * m + 1) m = 12 := by
    have h := LowDigitSumTermination.central_next_center q m hm hlo hhi hsmall8 hsym
    rw [heq m] at h
    change q m = 16 at hcenter
    omega
  have hnextsmall : ∀ i, i < 2 * m + 1 → i ≠ m →
      columnSum (output q) (2 * m + 1) i ≤ 4 := by
    intro i hi hic
    have h := central_next_exterior_exact q m hm hlo hhi hsmall8 hsym i hi hic
    rw [heq i] at h
    by_cases hneari : i + 1 = m ∨ i = m + 1
    · have hsource := hnear i hi hneari
      change q i ≤ 1 at hsource
      simp only [if_pos hneari] at h
      omega
    · have hsource := hsmall i hi hic
      change q i ≤ 2 at hsource
      simp only [if_neg hneari] at h
      omega
  exact LowDigitSumTermination.central_two_steps_palindrome (step n) (output q) m hm
    hcan' (by omega) (by omega) hnextsmall

/-- Central coefficient eighteen, exterior coefficients at most one, and
zero adjacent coefficients reduce to the refined three-step criterion. -/
theorem central_four_steps_refined (n : Nat) (d : Nat → Nat) (m : Nat)
    (hm : 0 < m) (hcan : Canonical n d (2 * m + 1))
    (hcenter : columnSum d (2 * m + 1) m = 18)
    (hsmall : ∀ i, i < 2 * m + 1 → i ≠ m →
      columnSum d (2 * m + 1) i ≤ 1)
    (hnear : ∀ i, i < 2 * m + 1 → (i + 1 = m ∨ i = m + 1) →
      columnSum d (2 * m + 1) i = 0) :
    Palindrome (step (step (step (step n)))) := by
  let q := columnSum d (2 * m + 1)
  have hsmall8 : ∀ i, i < 2 * m + 1 → i ≠ m → q i ≤ 8 := by
    intro i hi hic
    have h := hsmall i hi hic
    change q i ≤ 1 at h
    omega
  have hlo : 10 ≤ q m := by change q m = 18 at hcenter; omega
  have hhi : q m ≤ 18 := by change q m = 18 at hcenter; omega
  have hsym : ∀ i, i < 2 * m + 1 → q i = q (2 * m + 1 - 1 - i) :=
    columnSum_symmetric d (2 * m + 1)
  have hc := LowDigitSumTermination.central_carry_no_overflow q m hm hlo hhi hsmall8
  have hcan' := canonical_next_no_overflow n d (2 * m + 1) hcan hc
  have heq : ∀ i, nextColumns q (2 * m + 1) i =
      columnSum (output q) (2 * m + 1) i := by
    intro i
    simp only [nextColumns, hc, ite_true]
  have hnextcenter : columnSum (output q) (2 * m + 1) m = 16 := by
    have h := LowDigitSumTermination.central_next_center q m hm hlo hhi hsmall8 hsym
    rw [heq m] at h
    change q m = 18 at hcenter
    omega
  have hnextsmall : ∀ i, i < 2 * m + 1 → i ≠ m →
      columnSum (output q) (2 * m + 1) i ≤ 2 := by
    intro i hi hic
    have h := central_next_exterior_exact q m hm hlo hhi hsmall8 hsym i hi hic
    rw [heq i] at h
    by_cases hneari : i + 1 = m ∨ i = m + 1
    · have hsource := hnear i hi hneari
      change q i = 0 at hsource
      simp only [if_pos hneari] at h
      omega
    · have hsource := hsmall i hi hic
      change q i ≤ 1 at hsource
      simp only [if_neg hneari] at h
      omega
  have hnextnear : ∀ i, i < 2 * m + 1 → (i + 1 = m ∨ i = m + 1) →
      columnSum (output q) (2 * m + 1) i ≤ 1 := by
    intro i hi hneari
    have hic : i ≠ m := by omega
    have h := central_next_exterior_exact q m hm hlo hhi hsmall8 hsym i hi hic
    rw [heq i] at h
    have hsource := hnear i hi hneari
    change q i = 0 at hsource
    simp only [if_pos hneari] at h
    omega
  exact central_three_steps_refined (step n) (output q) m hm hcan'
    hnextcenter hnextsmall hnextnear

#print axioms central_next_exterior_exact
#print axioms central_three_steps_refined
#print axioms central_four_steps_refined

end DigitSumTenTermination
