import PrefixAncestry

/-!
# Lower-bound witnesses for the three prefix families (Agent #118)

Kernel-checked examples, outside the endpoint import graph. Each gives an explicit positive
start that reaches a palindrome of the family after `t` reverse-and-add steps, so the true
maximum ancestry depth of the family is at least `t`. Together with the certified upper bounds:

| family | witness | lower bound | certified upper bound |
|---|---|---:|---:|
| 218 | 10199522000 → 2189992442999812 | 15 | 34 |
| 777 | 183981000 → 7779554559777 | 14 | 25 |
| 217 | 1020400000 → 217459000954712 | 15 | 23 |

The witnesses were found by an exhaustive exact search over palindromes of widths up to 16
(`sharpness/`); wider palindromes may have deeper ancestry. Nothing is claimed about sharpness.
-/

namespace Agent118.Witnesses

open Lychrel196 DecimalDigits Agent118.PrefixKernel

/-- `PalindromeStarts3 a b c P` for a concrete numeral, via its canonical digit function. -/
theorem starts_of_digits {a b c P W : Nat} (hP : Palindrome P) (hW : 3 ≤ W)
    (hval : value (fun i => P / 10 ^ i % 10) W = P) (hlead : 0 < P / 10 ^ (W - 1) % 10)
    (ha : P / 10 ^ (W - 1) % 10 = a) (hb : P / 10 ^ (W - 2) % 10 = b)
    (hc : P / 10 ^ (W - 3) % 10 = c) : PalindromeStarts3 a b c P := by
  refine ⟨hP, fun i => P / 10 ^ i % 10, W, ⟨by omega, ?_, hlead, hval⟩, hW, ha, hb, hc⟩
  intro i _
  show P / 10 ^ i % 10 ≤ 9
  omega

theorem w218_orbit : orbit 10199522000 15 = 2189992442999812 := by decide
theorem w218_family : PalindromeStarts3 2 1 8 2189992442999812 :=
  starts_of_digits (W := 16) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)
theorem depth15_218 : ∃ A P, 0 < A ∧ PalindromeStarts3 2 1 8 P ∧ orbit A 15 = P :=
  ⟨_, _, by decide, w218_family, w218_orbit⟩

theorem w777_orbit : orbit 183981000 14 = 7779554559777 := by decide
theorem w777_family : PalindromeStarts3 7 7 7 7779554559777 :=
  starts_of_digits (W := 13) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)
theorem depth14_777 : ∃ A P, 0 < A ∧ PalindromeStarts3 7 7 7 P ∧ orbit A 14 = P :=
  ⟨_, _, by decide, w777_family, w777_orbit⟩

theorem w217_orbit : orbit 1020400000 15 = 217459000954712 := by decide
theorem w217_family : PalindromeStarts3 2 1 7 217459000954712 :=
  starts_of_digits (W := 15) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide) (by decide)
theorem depth15_217 : ∃ A P, 0 < A ∧ PalindromeStarts3 2 1 7 P ∧ orbit A 15 = P :=
  ⟨_, _, by decide, w217_family, w217_orbit⟩

#print axioms depth15_218
#print axioms depth14_777
#print axioms depth15_217

end Agent118.Witnesses
