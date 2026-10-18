import P196.Drafts.Agent103ResidualFive.ResidualFiveShape
import P196.Agent101DigitSplit.Agent101NumericFibers

/-!
# The ordinary-integer fiber of the residual-five predecessor

Agent #103, task `agent103-residual-five-fibers-20261016`.

This module specializes Agent #101's complete canonical digit splitting and
numeric-fiber theorems to the residual profile. The enumeration consists of
ordinary natural numbers and includes every canonical digit split.
The removal of the width premise is supplied in the separate conclusion module.
-/

namespace Agent103.ResidualFiveFibers

open DecimalDigits Lychrel196 SevenColumnProjection
open Agent103.ResidualFive

/-- The necessary direct predecessor of a residual-five family member. -/
def middle (r : Nat) : Nat := 33 * 10 ^ (2 * r + 2) + 22

/-- Half of the complete symmetric coefficient profile, outside to center. -/
def half (r : Nat) : List Nat := 2 :: 12 :: List.replicate r 9

/-- Agent #101's duplicate-free enumeration of ordinary integer realizations. -/
def fiber (r : Nat) : List Nat := Agent101.numericFiber (half r) none

theorem half_length (r : Nat) : (half r).length = r + 2 := by
  simp [half]

theorem profile_shape (r : Nat) :
    Agent101.coefficientWord (half r) none =
      2 :: 12 :: (List.replicate (2 * r) 9 ++ [12, 2]) := by
  simp [Agent101.coefficientWord, half, show 2 * r = r + r by omega,
    List.append_assoc]
  rw [← List.append_assoc, List.replicate_append_replicate]

theorem profile_length (r : Nat) :
    (Agent101.coefficientWord (half r) none).length = 2 * r + 4 := by
  rw [Agent101.length_coefficientWord, half_length]
  simp
  omega

theorem half_bounded (r : Nat) : ∀ a ∈ half r, a ≤ 18 := by
  intro a ha
  simp [half] at ha
  omega

theorem profile_bounded (r : Nat) :
    ∀ a ∈ Agent101.coefficientWord (half r) none, a ≤ 18 :=
  Agent101.coefficientWord_bounded (half r) none (half_bounded r) (by simp)

/-- The list profile agrees with the already checked residual source function
at every used position; no assertion is made about its irrelevant tail. -/
theorem profile_digit (r i : Nat) (hi : i < 2 * r + 4) :
    Agent101.digitFn (Agent101.coefficientWord (half r) none) i =
      fiveSourceDigit r i := by
  have hword : Agent101.coefficientWord (half r) none =
      segment (fiveSourceDigit r) 0 (2 * r + 4) :=
    (profile_shape r).trans (segment_fiveSourceDigit r).symm
  rw [hword]
  unfold Agent101.digitFn
  rw [segment_eq_range_map, List.getElem?_map, List.getElem?_range' hi]
  simp

/-- The symmetric coefficients normalize to `33 0^(2r) 22` and have no
terminal carry. Internal carries remain exactly those of the Shape theorem. -/
theorem profile_value (r : Nat) :
    Agent101.natValue (Agent101.coefficientWord (half r) none) = middle r := by
  let q := Agent101.digitFn (Agent101.coefficientWord (half r) none)
  have hq : ∀ i, i < 2 * r + 4 → q i = fiveSourceDigit r i := profile_digit r
  have hcarry : carry q (2 * r + 4) = 0 := by
    rw [five_source_carry q r hq (2 * r + 4) (by omega)]
    simp
  have hv := value_output q (2 * r + 4)
  rw [hcarry, Nat.zero_mul, Nat.add_zero, five_source_output_value q r hq] at hv
  unfold Agent101.natValue
  rw [profile_length]
  exact hv.symm

/-- Exact membership at the prescribed width, directly consuming Agent #101's
original ordinary-integer theorem rather than counting digit functions. -/
theorem fiber_mem_fixed_width (r n : Nat) :
    n ∈ fiber r ↔ Agent101.decimalWidth n (2 * r + 4) ∧ step n = middle r := by
  unfold fiber
  rw [Agent101.mem_numericFiber (half r) none n (profile_bounded r),
    profile_length, profile_value]

theorem fiber_mem_canonical (r n : Nat) :
    n ∈ fiber r ↔
      (∃ d, Canonical n d (2 * r + 4)) ∧ step n = middle r := by
  rw [fiber_mem_fixed_width, Agent101.decimalWidth_iff_canonical]

theorem fiber_nodup (r : Nat) : (fiber r).Nodup :=
  Agent101.numericFiber_nodup (half r) none

/-- The outside pair has two choices, the next pair has seven choices,
and each of the remaining `r` mirrored pairs has ten choices. -/
theorem fiber_length (r : Nat) : (fiber r).length = 14 * 10 ^ r := by
  unfold fiber half
  rw [Agent101.length_numericFiber_cons]
  simp [Agent101.pairCount, Agent101.centerCount, Agent101.natProduct,
    List.map_replicate, Agent101.natProduct_replicate, Nat.mul_assoc]
  omega

#print axioms middle
#print axioms half
#print axioms fiber
#print axioms half_length
#print axioms profile_shape
#print axioms profile_length
#print axioms half_bounded
#print axioms profile_bounded
#print axioms profile_digit
#print axioms profile_value
#print axioms fiber_mem_fixed_width
#print axioms fiber_mem_canonical
#print axioms fiber_nodup
#print axioms fiber_length

end Agent103.ResidualFiveFibers
