import ResidualFiveFiberConclusion
import ResidualFiveResidueCount

set_option autoImplicit false

namespace Agent103.ResidualFiveFibers

open Lychrel196 Agent119.EightFamilies Agent103.ResidualFiveResidueCount

/-- The complete predecessor fiber after imposing the proved 196 temporal phase. -/
def modularFiber (r : Nat) : List Nat :=
  (fiber r).filter (fun n => decide (n % 99 = 77))

/-- Exact membership over every ordinary natural number, with no width premise. -/
theorem mem_modularFiber_iff (r n : Nat) :
    n ∈ modularFiber r ↔ step n = middle r ∧ n % 99 = 77 := by
  simp only [modularFiber, List.mem_filter, decide_eq_true_eq, fiber_mem_iff]

/-- The original196 predecessor belongs to this exact residue-filtered list. -/
theorem occurrence_predecessor_modularFiber (t r : Nat)
    (h : orbit 196 t = fam 5 r) : orbit 196 (t - 2) ∈ modularFiber r := by
  simp only [modularFiber, List.mem_filter, decide_eq_true_eq]
  exact ⟨occurrence_predecessor_mem t r h, occurrence_predecessor_mod99 t r h⟩

/-- Complete finite reduction and exact cardinality for every parameter,
including zero. This does not assert that a listed integer is196-reachable. -/
theorem complete_modular_predecessor_fiber (r : Nat) :
    (modularFiber r).Nodup ∧
    (modularFiber r).length =
      (if r % 2 = 0 then (14 * 10 ^ r + 8) / 11 else (14 * 10 ^ r - 8) / 11) ∧
    (∀ n, n ∈ modularFiber r ↔
      step n = 33 * 10 ^ (2 * r + 2) + 22 ∧ n % 99 = 77) := by
  exact ⟨fiber_filter_mod99_nodup r, fiber_filter_mod99_length r,
    mem_modularFiber_iff r⟩

#print axioms modularFiber
#print axioms mem_modularFiber_iff
#print axioms occurrence_predecessor_modularFiber
#print axioms complete_modular_predecessor_fiber

end Agent103.ResidualFiveFibers
