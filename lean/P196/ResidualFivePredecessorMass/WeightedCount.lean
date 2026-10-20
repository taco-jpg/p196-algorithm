import P196.ResidualFivePredecessorMass.SplitWeights
import P196.ResidualFivePredecessorCount.ScanSupport
import P196.Drafts.Agent103ResidualFiveFibers.ResidualFiveResidues

set_option autoImplicit false

/-!
Agent #2: exact digit-split mass of the original accepted middle words.
Every successful scan is weighted by the length of the existing raw digit
enumeration of its returned coefficient word. The recurrence is derived
from this finite sum, including the empty middle, rather than postulated.
The ordinary-integer predecessor interpretation is supplied separately.
-/

namespace P196.ResidualFivePredecessorMass

open Agent101
open Agent105DecoderLocal9df76b (decodePair)
open Agent105DecoderScan9df76b (scan)
open Agent103.ResidualFiveResidues (rawNine rawNine_succ pairChoices_nine)
open P196.ResidualFivePredecessorCount (scan_wrap)

/-- The total raw digit-split weight of every successful original scan. -/
def middleWeight (r a b : Nat) : Nat :=
  ((Agent101.rawWords (List.replicate r 9) none).map
    (fun ds => ((Agent105DecoderScan9df76b.scan ds.length
      (Agent101.digitFn ds) a b).map rawWeight).getD 0)).sum

private def scanWeight (a b : Nat) (ds : List Nat) : Nat :=
  ((scan ds.length (digitFn ds) a b).map rawWeight).getD 0

private theorem sum_append_nat (xs ys : List Nat) :
    (xs ++ ys).sum = xs.sum + ys.sum := by
  induction xs with
  | nil => simp
  | cons x xs ih => simp [ih, Nat.add_assoc]

private theorem sum_map_scaled (words : List (List Nat))
    (f : List Nat → Nat) (k : Nat) :
    (words.map (fun ds => k * f ds)).sum = k * (words.map f).sum := by
  induction words with
  | nil => simp
  | cons ds words ih => simp [ih, Nat.mul_add]

/-- The coefficient returned by the unchanged decoder contributes its
original digit-pair multiplicity to the weight of the remaining scan. -/
private theorem scanWeight_wrap (u v a b : Nat) (ds : List Nat) :
    scanWeight a b (wrapDigits u v ds) =
      match decodePair u v a b with
      | none => 0
      | some E => pairCount false E.coeff * scanWeight E.low E.high ds := by
  unfold scanWeight
  rw [length_wrapDigits, scan_wrap]
  cases hd : decodePair u v a b with
  | none => rfl
  | some E =>
    simp only [Option.some_bind]
    cases hs : scan ds.length (digitFn ds) E.low E.high with
    | none => rfl
    | some qs => exact rawWeight_wrap E.coeff qs

private theorem wrapped_weight_sum (words : List (List Nat))
    (u v a b : Nat) :
    ((words.map (wrapDigits u v)).map (scanWeight a b)).sum =
      match decodePair u v a b with
      | none => 0
      | some E =>
        pairCount false E.coeff * (words.map (scanWeight E.low E.high)).sum := by
  simp only [List.map_map, Function.comp_def, scanWeight_wrap]
  cases hd : decodePair u v a b with
  | none => simp [List.map_const']
  | some E =>
    exact sum_map_scaled words (scanWeight E.low E.high)
      (pairCount false E.coeff)

/-- Each entry records the original split multiplicity and the two
outgoing carries of one successful digit-pair choice. -/
private def weightedDestinations (ps : List (Nat × Nat)) (a b : Nat) :
    List (Nat × Nat × Nat) :=
  ps.filterMap (fun p => (decodePair p.1 p.2 a b).map
    (fun E => (pairCount false E.coeff, E.low, E.high)))

private theorem weighted_grid_sum (ps : List (Nat × Nat))
    (words : List (List Nat)) (a b : Nat) :
    ((ps.flatMap (fun p => words.map (wrapDigits p.1 p.2))).map
      (scanWeight a b)).sum =
      ((weightedDestinations ps a b).map (fun E =>
        E.1 * (words.map (scanWeight E.2.1 E.2.2)).sum)).sum := by
  induction ps with
  | nil => simp [weightedDestinations]
  | cons p ps ih =>
    simp only [List.flatMap_cons, List.map_append, sum_append_nat,
      wrapped_weight_sum]
    rw [ih]
    simp only [weightedDestinations, List.filterMap_cons]
    cases hd : decodePair p.1 p.2 a b with
    | none => simp [hd]
    | some E => simp [hd]

/- A finite evaluation of the original decoder and digit-split counts.
The coefficients four and fourteen each have five raw splits; coefficient
nine has ten. No replacement transition relation is introduced. -/
private theorem weighted_table :
    weightedDestinations (pairChoices false 9) 0 0 = [(5, 0, 1)] ∧
    weightedDestinations (pairChoices false 9) 0 1 = [(5, 1, 1), (10, 0, 1)] ∧
    weightedDestinations (pairChoices false 9) 1 0 = [(10, 1, 0), (5, 0, 0)] ∧
    weightedDestinations (pairChoices false 9) 1 1 = [(5, 1, 0)] := by
  simp only [weightedDestinations, pairChoices_nine]
  decide

private theorem middleWeight_step (r : Nat) :
    middleWeight (r + 1) 0 0 = 5 * middleWeight r 0 1 ∧
    middleWeight (r + 1) 0 1 =
      5 * middleWeight r 1 1 + 10 * middleWeight r 0 1 ∧
    middleWeight (r + 1) 1 0 =
      10 * middleWeight r 1 0 + 5 * middleWeight r 0 0 ∧
    middleWeight (r + 1) 1 1 = 5 * middleWeight r 1 0 := by
  have hstep (a b : Nat) :
      middleWeight (r + 1) a b =
        ((weightedDestinations (pairChoices false 9) a b).map
          (fun E => E.1 * middleWeight r E.2.1 E.2.2)).sum := by
    change ((rawNine (r + 1)).map (scanWeight a b)).sum = _
    rw [rawNine_succ, weighted_grid_sum]
    rfl
  refine ⟨?_, ?_, ?_, ?_⟩
  · simpa only [weighted_table.1, List.map_cons, List.map_nil,
      List.sum_cons, List.sum_nil, Nat.add_zero] using hstep 0 0
  · simpa only [weighted_table.2.1, List.map_cons, List.map_nil,
      List.sum_cons, List.sum_nil, Nat.add_zero] using hstep 0 1
  · simpa only [weighted_table.2.2.1, List.map_cons, List.map_nil,
      List.sum_cons, List.sum_nil, Nat.add_zero] using hstep 1 0
  · simpa only [weighted_table.2.2.2, List.map_cons, List.map_nil,
      List.sum_cons, List.sum_nil, Nat.add_zero] using hstep 1 1

private theorem middleWeight_symmetry (r : Nat) :
    middleWeight r 0 0 = middleWeight r 1 1 ∧
    middleWeight r 0 1 = middleWeight r 1 0 := by
  induction r with
  | zero => constructor <;> rfl
  | succ r ih =>
    have hstep := middleWeight_step r
    constructor <;> omega

/-- The empty accepted middle has exactly one raw digit split. -/
theorem middleWeight_zero : middleWeight 0 0 0 = 1 := by
  rfl

/-- A single complementary pair has no accepted zero-boundary scan. -/
theorem middleWeight_one : middleWeight 1 0 0 = 0 := by
  have hzero : middleWeight 0 0 1 = 0 := by rfl
  have hstep := (middleWeight_step 0).1
  simpa only [hzero, Nat.mul_zero] using hstep

/-- Exact recurrence for the digit-split mass of all accepted middle words. -/
theorem middleWeight_recurrence (r : Nat) :
    middleWeight (r + 2) 0 0 =
      10 * middleWeight (r + 1) 0 0 + 25 * middleWeight r 0 0 := by
  have hnext : middleWeight (r + 2) 0 0 =
      5 * middleWeight (r + 1) 0 1 := by
    simpa only [Nat.add_assoc] using (middleWeight_step (r + 1)).1
  have hstep := middleWeight_step r
  have hsym := (middleWeight_symmetry r).1
  omega

end P196.ResidualFivePredecessorMass

#print axioms P196.ResidualFivePredecessorMass.middleWeight_zero
#print axioms P196.ResidualFivePredecessorMass.middleWeight_one
#print axioms P196.ResidualFivePredecessorMass.middleWeight_recurrence
