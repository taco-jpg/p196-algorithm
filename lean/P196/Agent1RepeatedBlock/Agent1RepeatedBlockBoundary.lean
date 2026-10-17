import P196.Foundations.Agent1RepeatedBlockContext

/-!
Concrete boundary witnesses for the repeated-block statement review.
These are kernel-reduced evaluations of the original Agent8 definitions.
They preserve the empty/all-nine cases and show why the incoming, coefficient,
prefix, and middle bounds cannot simply be discarded from the stated results.
-/

namespace Agent1.RepeatedBlock.Boundary
open Agent8

/-- An empty repeated block preserves its incoming carry and appends it once. -/
theorem empty_block_retains_carry :
    fixedDigits (pow [] 2) 1 = [] ∧
    terminalCarry (pow [] 2) 1 = 1 ∧
    normalize (pow [] 2) 1 = [1] := by decide

/-- The neutral block preserves both bit carries; its digits depend on that bit. -/
theorem all_nines_retain_incoming_bit :
    terminalCarry (pow [9] 2) 0 = 0 ∧
    terminalCarry (pow [9] 2) 1 = 1 ∧
    normalize (pow [9] 2) 0 = [9, 9] ∧
    normalize (pow [9] 2) 1 = [0, 0, 1] := by decide

/-- The first digit block need not equal the stabilized later block. -/
theorem first_copy_can_be_transient :
    fixedDigits [10] 0 = [0] ∧
    fixedDigits [10] (terminalCarry [10] 0) = [1] ∧
    fixedDigits [10] 0 ≠ fixedDigits [10] (terminalCarry [10] 0) ∧
    normalize (pow [10] 2) 0 = [0, 1, 1] := by decide

/-- Zero copies cannot be included in the positive-count carry conclusion. -/
theorem zero_copies_can_have_different_carry :
    terminalCarry (pow [10] 0) 0 ≠ terminalCarry [10] 0 := by decide

/-- Coefficient 19 already destroys bit-input idempotence. -/
theorem coefficient_nineteen_breaks_idempotence :
    terminalCarry [19] 0 = 1 ∧
    terminalCarry [19] (terminalCarry [19] 0) = 2 ∧
    terminalCarry [19] (terminalCarry [19] 0) ≠ terminalCarry [19] 0 := by decide

/-- Incoming carry 2 destroys idempotence even with coefficient 8. -/
theorem incoming_two_breaks_idempotence :
    terminalCarry [8] 2 = 1 ∧
    terminalCarry [8] (terminalCarry [8] 2) = 0 ∧
    terminalCarry [8] (terminalCarry [8] 2) ≠ terminalCarry [8] 2 := by decide

/-- An unbounded prefix may deliver a non-bit carry to the repeated block. -/
theorem unbounded_prefix_breaks_context :
    terminalCarry ([100] ++ pow [0] 2 ++ []) 0 = 0 ∧
    terminalCarry ([100] ++ [0] ++ []) 0 = 1 ∧
    terminalCarry ([100] ++ pow [0] 2 ++ []) 0 ≠
      terminalCarry ([100] ++ [0] ++ []) 0 := by decide

/-- An unbounded middle may deliver a non-bit carry to the second band. -/
theorem unbounded_middle_breaks_two_bands :
    terminalCarry ([] ++ pow [] 1 ++ [100] ++ pow [0] 2 ++ []) 0 = 0 ∧
    terminalCarry ([] ++ [] ++ [100] ++ [0] ++ []) 0 = 1 ∧
    terminalCarry ([] ++ pow [] 1 ++ [100] ++ pow [0] 2 ++ []) 0 ≠
      terminalCarry ([] ++ [] ++ [100] ++ [0] ++ []) 0 := by decide

/-- An unbounded suffix can produce a non-digit terminal entry; its carry
value is then not the number of appended list entries. -/
theorem unbounded_suffix_is_not_bit_overflow :
    normalize [100] 0 = [0, 10] ∧
    terminalCarry [100] 0 = 10 ∧
    (normalize [100] 0).length ≠ ([100] : Word).length + terminalCarry [100] 0 := by decide

/-- The list normalizer retains zeros; it does not trim to canonical numeral width. -/
theorem normalization_preserves_zero_columns :
    normalize (pow [0] 2) 0 = [0, 0] ∧
    (normalize (pow [0] 2) 0).length = 2 := by decide

end Agent1.RepeatedBlock.Boundary

#print axioms Agent1.RepeatedBlock.Boundary.empty_block_retains_carry
#print axioms Agent1.RepeatedBlock.Boundary.all_nines_retain_incoming_bit
#print axioms Agent1.RepeatedBlock.Boundary.first_copy_can_be_transient
#print axioms Agent1.RepeatedBlock.Boundary.zero_copies_can_have_different_carry
#print axioms Agent1.RepeatedBlock.Boundary.coefficient_nineteen_breaks_idempotence
#print axioms Agent1.RepeatedBlock.Boundary.incoming_two_breaks_idempotence
#print axioms Agent1.RepeatedBlock.Boundary.unbounded_prefix_breaks_context
#print axioms Agent1.RepeatedBlock.Boundary.unbounded_middle_breaks_two_bands
#print axioms Agent1.RepeatedBlock.Boundary.unbounded_suffix_is_not_bit_overflow
#print axioms Agent1.RepeatedBlock.Boundary.normalization_preserves_zero_columns
