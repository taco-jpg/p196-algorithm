import ResidualFiveResidues
import ResidualFiveResidueBridge
import ResidualFiveCountArithmetic

set_option autoImplicit false

/-!
# Exact residue counts in the complete residual-five ordinary-integer fiber

The counted list is the original `Agent101.numericFiber`, specialized by
`ResidualFiveFibers`. No selected subfamily or sampled digit assignment is used.
-/

namespace Agent103.ResidualFiveResidueCount

open Agent101
open Agent103.ResidualFiveFibers Agent103.ResidualFiveResidues

/-- The inner residue which makes the two outside mirrored pairs divisible by 11. -/
def outerTarget (a b c d : Nat) : Nat :=
  (11 - (a + 10 * c + d + b * 10) % 11) % 11

theorem double_wrap_zero_iff (a b c d r : Nat) (ds : List Nat)
    (hlen : ds.length = 2 * r) :
    natValue (wrapDigits a b (wrapDigits c d ds)) % 11 = 0 ↔
      natValue ds % 11 = outerTarget a b c d := by
  rw [natValue_wrap_mod11 a b (r + 1) (wrapDigits c d ds)
    (by rw [length_wrapDigits, hlen]; omega)]
  rw [natValue_wrap_mod11 c d r ds hlen]
  unfold outerTarget
  omega

theorem raw_double_wrap_count (a b c d r : Nat) :
    (rawNine r).countP
      (fun ds => decide (natValue (wrapDigits a b (wrapDigits c d ds)) % 11 = 0)) =
        rawCount r (outerTarget a b c d) := by
  unfold rawCount
  apply List.countP_congr
  intro ds hds
  simp only [decide_eq_true_eq]
  exact double_wrap_zero_iff a b c d r ds (rawNine_word_length r ds hds)

theorem pairChoices_two : pairChoices true 2 = [(0, 2), (1, 1)] := by decide

theorem pairChoices_twelve : pairChoices false 12 =
    [(3, 9), (4, 8), (5, 7), (6, 6), (7, 5), (8, 4), (9, 3)] := by decide

theorem canonicalWords_half (r : Nat) :
    canonicalWords (half r) none =
      (pairChoices true 2).flatMap (fun p =>
        ((pairChoices false 12).flatMap
          (fun q => (rawNine r).map (wrapDigits q.1 q.2))).map
            (wrapDigits p.1 p.2)) := rfl

/-- Fourteen complete outside assignments contain exactly two zero offsets;
the other twelve consume the already proved uniform nonzero residue count. -/
theorem canonical_zero_count (r : Nat) :
    (canonicalWords (half r) none).countP (fun ds => decide (natValue ds % 11 = 0)) =
      2 * rawCount r 0 + 12 * rawCount r 1 := by
  simp only [canonicalWords_half, pairChoices_two, pairChoices_twelve,
    List.flatMap_cons, List.flatMap_nil, List.append_nil,
    List.map_nil, List.map_append, List.map_map, List.countP_append,
    List.countP_map, Function.comp_def]
  simp only [raw_double_wrap_count, outerTarget, Nat.reduceAdd, Nat.reduceMul,
    Nat.reduceMod, Nat.reduceSub]
  simp only [rawCount_nonzero r 2 (by decide) (by decide),
    rawCount_nonzero r 4 (by decide) (by decide),
    rawCount_nonzero r 5 (by decide) (by decide),
    rawCount_nonzero r 6 (by decide) (by decide),
    rawCount_nonzero r 7 (by decide) (by decide),
    rawCount_nonzero r 8 (by decide) (by decide),
    rawCount_nonzero r 9 (by decide) (by decide)]
  omega

/-- This statement already counts ordinary natural numbers in the full fiber. -/
theorem fiber_count_mod11 (r : Nat) :
    (fiber r).countP (fun n => decide (n % 11 = 0)) =
      2 * rawCount r 0 + 12 * rawCount r 1 := by
  unfold fiber numericFiber
  rw [List.countP_map]
  exact canonical_zero_count r

/-- The exact count of modulo-99-compatible ordinary integers in the full fiber. -/
def residueCount (r : Nat) : Nat :=
  (fiber r).countP (fun n => decide (n % 99 = 77))

theorem residueCount_eq_rawCounts (r : Nat) :
    residueCount r = 2 * rawCount r 0 + 12 * rawCount r 1 := by
  unfold residueCount
  rw [fiber_count_mod99_eq_mod11, fiber_count_mod11]

theorem residueCount_zero : residueCount 0 = 2 := by
  rw [residueCount_eq_rawCounts]
  decide

/-- This recurrence is proved for the original full integer fiber itself. -/
theorem residueCount_recurrence (r : Nat) :
    residueCount (r + 1) + residueCount r = 14 * 10 ^ r := by
  rw [residueCount_eq_rawCounts, residueCount_eq_rawCounts]
  have h0 := rawCount_zero_recurrence r
  have h1 := rawCount_nonzero_recurrence r
  omega

theorem residueCount_scaled (r : Nat) :
    11 * residueCount r =
      if r % 2 = 0 then 14 * 10 ^ r + 8 else 14 * 10 ^ r - 8 :=
  Agent103.ResidualFiveCountArithmetic.scaled_closed_form
    residueCount residueCount_zero residueCount_recurrence r

theorem residueCount_closed_form (r : Nat) :
    residueCount r = if r % 2 = 0 then (14 * 10 ^ r + 8) / 11
      else (14 * 10 ^ r - 8) / 11 :=
  Agent103.ResidualFiveCountArithmetic.closed_form
    residueCount residueCount_zero residueCount_recurrence r

/-- Exact all-parameter cardinality of the requested filtered original list. -/
theorem fiber_filter_mod99_length (r : Nat) :
    ((fiber r).filter (fun n => decide (n % 99 = 77))).length =
      if r % 2 = 0 then (14 * 10 ^ r + 8) / 11
        else (14 * 10 ^ r - 8) / 11 := by
  rw [← List.countP_eq_length_filter]
  exact residueCount_closed_form r

/-- Each ordinary integer contributes once to the displayed cardinality. -/
theorem fiber_filter_mod99_nodup (r : Nat) :
    ((fiber r).filter (fun n => decide (n % 99 = 77))).Nodup :=
  (fiber_nodup r).filter _

theorem residueCount_positive (r : Nat) : 0 < residueCount r := by
  have hs := residueCount_scaled r
  have hp : 0 < 10 ^ r := Nat.pow_pos (by decide)
  by_cases he : r % 2 = 0 <;> simp only [he, if_true, if_false] at hs <;> omega

/-- Every residual profile has a local integer preimage in the required residue.
This does not assert that any such integer lies on the orbit starting at 196. -/
theorem fiber_mod99_exists (r : Nat) :
    ∃ n, n ∈ fiber r ∧ n % 99 = 77 := by
  have h := List.countP_pos_iff.mp (residueCount_positive r)
  simpa only [decide_eq_true_eq] using h

#print axioms outerTarget
#print axioms double_wrap_zero_iff
#print axioms raw_double_wrap_count
#print axioms pairChoices_two
#print axioms pairChoices_twelve
#print axioms canonicalWords_half
#print axioms canonical_zero_count
#print axioms fiber_count_mod11
#print axioms residueCount
#print axioms residueCount_eq_rawCounts
#print axioms residueCount_zero
#print axioms residueCount_recurrence
#print axioms residueCount_scaled
#print axioms residueCount_closed_form
#print axioms fiber_filter_mod99_length
#print axioms fiber_filter_mod99_nodup
#print axioms residueCount_positive
#print axioms fiber_mod99_exists

end Agent103.ResidualFiveResidueCount
