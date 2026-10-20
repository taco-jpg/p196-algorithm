import P196.Agent105AllPredecessors.Agent105WordFiber9df76b
import P196.Drafts.Agent103ResidualFiveFibers.ResidualFiveFibers

set_option autoImplicit false

/-!
Exact ordinary digit sums of the existing finite digit-split fibers.
The list-to-number bridge uses the original positional evaluation and
canonical digit enumeration. Coefficient sums are unweighted list sums;
they are not cardinalities of the fibers.

The residual-five specialization applies to the existing prescribed fiber.
No occurrence in the orbit of 196 or infinite-orbit statement is asserted.
-/

namespace P196.ResidualFivePredecessorDigitMass

open Agent101 DecimalDigits DecimalMass

/-- The original finite digit function has the same unweighted sum as its list. -/
theorem wordSum_digitFn (ds : List Nat) :
    wordSum (digitFn ds) ds.length = ds.sum := by
  induction ds with
  | nil => rfl
  | cons d ds ih =>
    rw [List.length_cons, wordSum_shift]
    change d + wordSum (digitFn ds) ds.length = d + ds.sum
    rw [ih]

/-- A bounded decimal list has its ordinary digit sum even with leading zeroes. -/
theorem digitSum_natValue (ds : List Nat) (hd : digitsBounded ds) :
    digitSum (natValue ds) = ds.sum := by
  unfold natValue
  rw [digitSum_value _ _ ((bounded_digitFn_iff ds).mpr hd), wordSum_digitFn]

/-- Summing the original reflected pair coefficients counts each list entry twice. -/
theorem digitPairSums_sum (ds : List Nat) :
    (digitPairSums ds).sum = 2 * ds.sum := by
  calc
    (digitPairSums ds).sum =
        wordSum (digitFn (digitPairSums ds)) (digitPairSums ds).length :=
      (wordSum_digitFn (digitPairSums ds)).symm
    _ = wordSum (columnSum (digitFn ds) ds.length) ds.length := by
      rw [length_digitPairSums]
      apply wordSum_congr
      intro i hi
      exact digitFn_digitPairSums ds i hi
    _ = 2 * wordSum (digitFn ds) ds.length := wordSum_columns _ _
    _ = 2 * ds.sum := by rw [wordSum_digitFn]

/-- Every ordinary integer in a finite profile fiber has half its coefficient sum. -/
theorem numericFiber_digitSum_double (h : List Nat) (c : Option Nat)
    (n : Nat) (hn : n ∈ numericFiber h c) :
    2 * digitSum n = (coefficientWord h c).sum := by
  obtain ⟨ds, hc, hp, hv⟩ := (mem_numericFiber_digits h c n).mp hn
  rw [← hv, digitSum_natValue ds hc.1, ← hp, digitPairSums_sum]

/-- Symmetric finite coefficient words retain their exact digit mass under splitting. -/
theorem wordFiber_digitSum_double (qs : List Nat) (n : Nat)
    (hrev : qs.reverse = qs)
    (hn : n ∈ Agent105WordFiber9df76b.wordFiber qs) :
    2 * digitSum n = qs.sum := by
  have hm := numericFiber_digitSum_double
    (Agent105WordFiber9df76b.half qs) (Agent105WordFiber9df76b.center qs) n hn
  rw [Agent105WordFiber9df76b.coefficientWord_roundtrip qs hrev] at hm
  exact hm

/-- Every member of the original residual-five fiber has the same ordinary digit sum. -/
theorem fiber_digitSum (r n : Nat)
    (hn : n ∈ Agent103.ResidualFiveFibers.fiber r) :
    digitSum n = 9 * r + 14 := by
  have hm := numericFiber_digitSum_double
    (Agent103.ResidualFiveFibers.half r) none n hn
  have hrep (k : Nat) : (List.replicate k 9 ++ [12, 2]).sum = 9 * k + 14 := by
    induction k with
    | zero => rfl
    | succ k ih =>
      simp only [List.replicate_succ, List.cons_append, List.sum_cons, ih]
      omega
  have hs : (coefficientWord (Agent103.ResidualFiveFibers.half r) none).sum =
      18 * r + 28 := by
    rw [Agent103.ResidualFiveFibers.profile_shape]
    simp only [List.sum_cons, hrep]
    omega
  rw [hs] at hm
  omega

end P196.ResidualFivePredecessorDigitMass

#print axioms P196.ResidualFivePredecessorDigitMass.wordSum_digitFn
#print axioms P196.ResidualFivePredecessorDigitMass.digitSum_natValue
#print axioms P196.ResidualFivePredecessorDigitMass.digitPairSums_sum
#print axioms P196.ResidualFivePredecessorDigitMass.numericFiber_digitSum_double
#print axioms P196.ResidualFivePredecessorDigitMass.wordFiber_digitSum_double
#print axioms P196.ResidualFivePredecessorDigitMass.fiber_digitSum
