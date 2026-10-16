import SourceFormula

/-!
Small kernel-checked convention and boundary controls. These finite checks
supplement the universal theorems; they do not establish them.
-/

namespace P196.Agent15.SpectralCarry

theorem control_empty : carryCharge [] = 0 := by decide

theorem control_singletons : carryCharge [0] = 0 ∧ carryCharge [1] = 0 := by decide

theorem control_length_two : carryCharge [0, 1] = 1 ∧ carryCharge [1, 0] = -1 := by decide

theorem control_free_odd_center :
    carryCharge [0, 0, 0] = 0 ∧ carryCharge [0, 1, 0] = 0 := by decide

theorem control_symmetric_even : carryCharge [1, 0, 0, 1] = 0 := by decide

theorem control_original_419 : carryCharge [0, 1, 0, 0, 1, 1] = 419 := by decide

theorem control_nonbinary_counterexample :
    carryCharge [1, 0, 21, 0] = 0 ∧ [1, 0, 21, 0].reverse ≠ [1, 0, 21, 0] := by decide

theorem control_incoming_zero_convention :
    carryCharge [1, 1] = 0 ∧ carryCharge [0, 1, 1] = 1 := by decide

theorem control_zero_overflow_convention :
    carryCharge [0, 1, 0] = 0 ∧ carryCharge [0, 1] = 1 := by decide

end P196.Agent15.SpectralCarry
