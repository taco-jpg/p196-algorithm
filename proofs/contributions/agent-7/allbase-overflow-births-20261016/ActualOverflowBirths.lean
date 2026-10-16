import AdjacentBirths
import OverflowDigits

/-!
Exact extreme births in the actual overflowing paired output.
Every carry is the unchanged ordinary-prefix carry from ActualBaseBirths;
the strict interior index is measured against the old coefficient width.
No endpoint, orbit, or persistence theorem is asserted in this module.
-/
namespace P196.Agent7.AllBaseOverflow

open ResetNormalization PhysicalWidth ReverseAdd ActualBaseBirths

/-- Complete zero classification at a real interior output position.
The first row is inheritance from an old adjacent zero pair. -/
theorem actual_overflow_zero_iff (b : Int) (xs : List (Int × Bool)) (i : Nat)
    (hb : 2 ≤ b) (hbound : Bounded b xs)
    (ho : terminal b 0 (ordinaryTags xs) = 1) (hi0 : 0 < i) (hi : i < xs.length)
    (hs : (xs.map Prod.fst).reverse = xs.map Prod.fst) :
    (pairs (actualDigits b xs)).getD i 0 = 0 ↔
      ((xs[i - 1]'(by omega)).1 = 0 ∧ xs[i].1 = 0) ∨
      ((xs[i - 1]'(by omega)).1 = b - 1 ∧ xs[i].1 = b - 1 ∧
        incoming b xs i = 1 ∧ incoming b xs (xs.length - i) = 1) ∨
      ((xs[i - 1]'(by omega)).1 = b - 1 ∧ xs[i].1 = b ∧
        incoming b xs i = 0) ∨
      ((xs[i - 1]'(by omega)).1 = b ∧ xs[i].1 = b - 1 ∧
        incoming b xs (xs.length - i) = 0) := by
  have hout : i < (pairs (actualDigits b xs)).length := by
    rw [pairs_length, actual_overflow_length b xs ho]
    omega
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hout, Option.getD_some,
    actual_overflow_pair_at b xs i ho hi0 hi hs]
  exact adjacent_residues_zero_iff b (xs[i - 1]'(by omega)).1 xs[i].1
    (incoming b xs (i - 1)) (incoming b xs i) (incoming b xs (xs.length - i))
    (incoming b xs (xs.length - i - 1)) hb
    (hbound _ (List.getElem_mem (by omega))) (hbound _ (List.getElem_mem hi))
    (incoming_bit b xs (i - 1) hb hbound)
    (incoming_bit b xs (xs.length - i - 1) hb hbound)
    (incoming_predecessor b xs i hi0 (by omega))
    (incoming_mirror_predecessor b xs i hi0 hi hs)

/-- Complete maximal classification at a real interior output position.
The first row is inheritance from an old adjacent maximal pair. -/
theorem actual_overflow_max_iff (b : Int) (xs : List (Int × Bool)) (i : Nat)
    (hb : 2 ≤ b) (hbound : Bounded b xs)
    (ho : terminal b 0 (ordinaryTags xs) = 1) (hi0 : 0 < i) (hi : i < xs.length)
    (hs : (xs.map Prod.fst).reverse = xs.map Prod.fst) :
    (pairs (actualDigits b xs)).getD i 0 = 2 * b - 2 ↔
      ((xs[i - 1]'(by omega)).1 = 2 * b - 2 ∧ xs[i].1 = 2 * b - 2) ∨
      ((xs[i - 1]'(by omega)).1 = b - 1 ∧ xs[i].1 = b - 1 ∧
        incoming b xs i = 0 ∧ incoming b xs (xs.length - i) = 0) ∨
      ((xs[i - 1]'(by omega)).1 = b - 1 ∧ xs[i].1 = b - 2 ∧
        incoming b xs i = 1) ∨
      ((xs[i - 1]'(by omega)).1 = b - 2 ∧ xs[i].1 = b - 1 ∧
        incoming b xs (xs.length - i) = 1) := by
  have hout : i < (pairs (actualDigits b xs)).length := by
    rw [pairs_length, actual_overflow_length b xs ho]
    omega
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hout, Option.getD_some,
    actual_overflow_pair_at b xs i ho hi0 hi hs]
  exact adjacent_residues_max_iff b (xs[i - 1]'(by omega)).1 xs[i].1
    (incoming b xs (i - 1)) (incoming b xs i) (incoming b xs (xs.length - i))
    (incoming b xs (xs.length - i - 1)) hb
    (hbound _ (List.getElem_mem (by omega))) (hbound _ (List.getElem_mem hi))
    (incoming_bit b xs (i - 1) hb hbound)
    (incoming_bit b xs (xs.length - i - 1) hb hbound)
    (incoming_predecessor b xs i hi0 (by omega))
    (incoming_mirror_predecessor b xs i hi0 hi hs)

/-- A new actual interior extreme must have a neutral old neighbor.
Birth excludes the corresponding old homogeneous adjacent extreme pair. -/
theorem actual_overflow_new_extreme_neutral (b : Int) (xs : List (Int × Bool))
    (i : Nat) (hb : 2 ≤ b) (hbound : Bounded b xs)
    (ho : terminal b 0 (ordinaryTags xs) = 1) (hi0 : 0 < i) (hi : i < xs.length)
    (hs : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (hnew : ((pairs (actualDigits b xs)).getD i 0 = 0 ∧
        ¬ ((xs[i - 1]'(by omega)).1 = 0 ∧ xs[i].1 = 0)) ∨
      ((pairs (actualDigits b xs)).getD i 0 = 2 * b - 2 ∧
        ¬ ((xs[i - 1]'(by omega)).1 = 2 * b - 2 ∧ xs[i].1 = 2 * b - 2))) :
    (xs[i - 1]'(by omega)).1 = b - 1 ∨ xs[i].1 = b - 1 := by
  rw [actual_overflow_zero_iff b xs i hb hbound ho hi0 hi hs,
    actual_overflow_max_iff b xs i hb hbound ho hi0 hi hs] at hnew
  omega

/-- Without either neutral old neighbor, each actual extreme is exactly
inherited from its corresponding old homogeneous adjacent pair. -/
theorem actual_overflow_without_neutral (b : Int) (xs : List (Int × Bool))
    (i : Nat) (hb : 2 ≤ b) (hbound : Bounded b xs)
    (ho : terminal b 0 (ordinaryTags xs) = 1) (hi0 : 0 < i) (hi : i < xs.length)
    (hs : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (hprev : (xs[i - 1]'(by omega)).1 ≠ b - 1) (hcur : xs[i].1 ≠ b - 1) :
    ((pairs (actualDigits b xs)).getD i 0 = 0 ↔
      (xs[i - 1]'(by omega)).1 = 0 ∧ xs[i].1 = 0) ∧
    ((pairs (actualDigits b xs)).getD i 0 = 2 * b - 2 ↔
      (xs[i - 1]'(by omega)).1 = 2 * b - 2 ∧ xs[i].1 = 2 * b - 2) := by
  rw [actual_overflow_zero_iff b xs i hb hbound ho hi0 hi hs,
    actual_overflow_max_iff b xs i hb hbound ho hi0 hi hs]
  omega

#print axioms actual_overflow_zero_iff
#print axioms actual_overflow_max_iff
#print axioms actual_overflow_new_extreme_neutral
#print axioms actual_overflow_without_neutral

end P196.Agent7.AllBaseOverflow
