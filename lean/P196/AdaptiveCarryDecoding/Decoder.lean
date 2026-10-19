import P196.AdaptiveCarryDecoding.Bounds

set_option autoImplicit false

/-!
# Decoding initial digit sum from an observed list of carry totals

The first twelve observations determine a sufficient total observation length.
Once that many entries are available, a chronological fold decodes the initial
digit sum. The required length uses only the supplied list, with no decimal
width parameter. The exact correctness statements concern actual observations
from a positive ordinary orbit; readiness alone does not test realizability.

Every outgoing carry, including the terminal carry, is counted. Ordinary
iteration continues after palindromes. No initial-integer reconstruction,
optimal horizon, or palindrome-avoidance conclusion is asserted.
-/

namespace AdaptiveCarryDecoding

open Lychrel196 DecimalMass CarryCountGrowth CarryCountDecoding

/-- The first `M` total outgoing carry counts, in chronological order. -/
def carryPrefix (n M : Nat) : List Nat :=
  (List.range M).map (fun t => outgoingCarryCount (orbit n t))

/-- The maximum of the first twelve supplied observations, with empty default zero. -/
def observedCeiling (xs : List Nat) : Nat :=
  (xs.take 12).max?.getD 0

/-- A sufficient total number of observations, computed only from the supplied data. -/
def requiredLength (xs : List Nat) : Nat :=
  horizon (observedCeiling xs)

/-- Earlier observations receive larger powers-of-two weights. -/
def listWeight (xs : List Nat) : Nat :=
  xs.foldl (fun w c => 2 * w + c) 0

/-- Decode the requested prefix once all of its entries have arrived. -/
def decodeList (xs : List Nat) : Option Nat :=
  let N := requiredLength xs
  if N ≤ xs.length then
    some (9 * listWeight (xs.take N) / 2 ^ N + 1)
  else none

private theorem carryPrefix_length (n M : Nat) : (carryPrefix n M).length = M := by
  simp [carryPrefix]

private theorem carryPrefix_take (n M K : Nat) (hK : K ≤ M) :
    (carryPrefix n M).take K = carryPrefix n K := by
  unfold carryPrefix
  rw [← List.map_take, List.take_range, Nat.min_eq_left hK]

private theorem carryPrefix_succ (n M : Nat) :
    carryPrefix n (M + 1) =
      carryPrefix n M ++ [outgoingCarryCount (orbit n M)] := by
  simp [carryPrefix, List.range_succ]

private theorem listWeight_carryPrefix (n M : Nat) :
    listWeight (carryPrefix n M) =
      weightedCount (fun t => outgoingCarryCount (orbit n t)) M := by
  induction M with
  | zero => simp [carryPrefix, listWeight, weightedCount]
  | succ M ih =>
    calc
      listWeight (carryPrefix n (M + 1)) =
          2 * listWeight (carryPrefix n M) + outgoingCarryCount (orbit n M) := by
        rw [carryPrefix_succ]
        simp [listWeight, List.foldl_append]
      _ = weightedCount (fun t => outgoingCarryCount (orbit n t)) (M + 1) := by
        rw [ih, weightedCount]

private theorem observedCeiling_stable (n M : Nat) (hM : 12 ≤ M) :
    observedCeiling (carryPrefix n M) = observedCeiling (carryPrefix n 12) := by
  unfold observedCeiling
  rw [carryPrefix_take n M 12 hM, carryPrefix_take n 12 12 (Nat.le_refl 12)]

private theorem first_twelve_le_observedCeiling (n M : Nat) (hM : 12 ≤ M)
    (t : Nat) (ht : t < 12) :
    outgoingCarryCount (orbit n t) ≤ observedCeiling (carryPrefix n M) := by
  change outgoingCarryCount (orbit n t) ≤ ((carryPrefix n M).take 12).max?.getD 0
  apply List.le_max?_getD_of_mem
  rw [carryPrefix_take n M 12 hM]
  simp only [carryPrefix, List.mem_map, List.mem_range]
  exact ⟨t, ht, rfl⟩

/-- On every actual positive-seed prefix, the decoder returns exactly the
initial digit sum when its data-derived length requirement is met. -/
theorem decodeList_actual_prefix (n M : Nat) (hn : 0 < n) :
    decodeList (carryPrefix n M) =
      if requiredLength (carryPrefix n M) ≤ M
      then some (digitSum n) else none := by
  by_cases hready : requiredLength (carryPrefix n M) ≤ M
  · have hN : 18 ≤ requiredLength (carryPrefix n M) :=
      horizon_ge_eighteen (observedCeiling (carryPrefix n M))
    have hM : 12 ≤ M := by omega
    have hC : ∀ t, t < 12 →
        outgoingCarryCount (orbit n t) ≤ observedCeiling (carryPrefix n M) :=
      fun t ht => first_twelve_le_observedCeiling n M hM t ht
    have hdecode := digitSum_eq_decode_of_first_twelve n
      (observedCeiling (carryPrefix n M)) hn hC
    simp only [decodeList, carryPrefix_length, if_pos hready]
    rw [carryPrefix_take n M (requiredLength (carryPrefix n M)) hready,
      listWeight_carryPrefix]
    exact congrArg some hdecode.symm
  · simp only [decodeList, carryPrefix_length, if_neg hready]

/-- The first twelve observations determine an explicit finite stopping
length, and the decoder succeeds when that many actual counts are supplied. -/
theorem decodeList_terminates (n : Nat) (hn : 0 < n) :
    let N := requiredLength (carryPrefix n 12)
    decodeList (carryPrefix n N) = some (digitSum n) := by
  let N := requiredLength (carryPrefix n 12)
  change decodeList (carryPrefix n N) = some (digitSum n)
  have hN : 18 ≤ N := horizon_ge_eighteen (observedCeiling (carryPrefix n 12))
  have hstable : requiredLength (carryPrefix n N) = N :=
    congrArg horizon (observedCeiling_stable n N (by omega))
  have hready : requiredLength (carryPrefix n N) ≤ N := by omega
  simpa only [if_pos hready] using decodeList_actual_prefix n N hn

#print axioms decodeList_actual_prefix
#print axioms decodeList_terminates

end AdaptiveCarryDecoding
