import P196.Agent105NumericDecoder.Agent105DecoderScan9df76b
import P196.Agent105InverseBoundaries.Agent105CrossWidthWitness9df76b

/-!
Closed numerical controls for the target decoder, Agent105 / session 9df76b.
These tests reuse the previously kernel-checked ordinary reverse-add witnesses.
The two retained nonpalindromic profiles come from persist_inverse_notes.txt;
their concrete integer realizations are not a newly discovered counterexample.

Only finite scanner evaluations are decided here. Large reverseFuel numerals
are never unfolded: the actual large steps use the existing witness theorems.
-/

namespace Agent105DecoderControls9df76b

open DecimalDigits Lychrel196 Agent101 Agent105DecoderLocal9df76b
open Agent105DecoderScan9df76b Agent105.CrossWidthWitness9df76b

/-- A zero low payload remains valid after removal of an overflow digit. -/
theorem five_to_ten :
    step 5 = 10 ∧
      decodeAtWidth (literalDigit 10) 1 1 = some [10] ∧
      decodeAtWidth (literalDigit 10) 2 0 = none := by
  exact ⟨by decide, by decide, by decide⟩

/-- The minimal positive source uses a one-column even coefficient. -/
theorem one_to_two :
    step 1 = 2 ∧
      decodeAtWidth (literalDigit 2) 1 0 = some [2] ∧
      decodeAtWidth (literalDigit 2) 0 1 = none := by
  exact ⟨by decide, by decide, by decide⟩

/-- The shorter source joins two inner carries equal to one. -/
theorem boundary_121 :
    step 29 = 121 ∧ step 110 = 121 ∧
      decodeAtWidth (literalDigit 121) 2 1 = some [11, 11] ∧
      decodeAtWidth (literalDigit 121) 3 0 = some [1, 2, 1] := by
  refine ⟨?_, ?_, by decide, by decide⟩
  · change 29 + reverse10 29 = 121
    rw [boundary_reversals.1]
  · change 110 + reverse10 110 = 121
    rw [boundary_reversals.2.1]

/-- An odd target middle digit is possible when the target is nonpalindromic. -/
theorem retained_nonpalindromic_1197801 :
    step 200799 = 1197801 ∧ step 1098900 = 1197801 ∧
      ¬ Palindrome 1197801 ∧
      decodeAtWidth (literalDigit 1197801) 6 1 =
        some [11, 9, 7, 7, 9, 11] ∧
      decodeAtWidth (literalDigit 1197801) 7 0 =
        some [1, 0, 18, 16, 18, 0, 1] := by
  exact ⟨short_step, long_step, target_not_palindrome, by decide, by decide⟩

/-- Truncated subtraction cannot manufacture a valid negative coefficient. -/
theorem truncated_subtraction_rejects :
    decodePair 0 0 1 0 = none ∧ decodeCenter 0 1 0 = none := by
  decide

/-- Out-of-domain digits illustrate why the physical decoder theorem carries
an output-digit-bound premise. This does not assert a fault in that contract. -/
theorem output_digit_bound_contract :
    decodeAtWidth (fun _ => 10) 1 0 = some [10] ∧
      output (digitFn [10]) 0 = 0 ∧ carry (digitFn [10]) 1 = 1 := by
  decide

#print axioms five_to_ten
#print axioms one_to_two
#print axioms boundary_121
#print axioms retained_nonpalindromic_1197801
#print axioms truncated_subtraction_rejects
#print axioms output_digit_bound_contract

end Agent105DecoderControls9df76b
