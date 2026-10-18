import P196.Drafts.Agent7OddNooverflowFibers.OddCenter

/- Independent review fixtures for the frozen OddCenter source.
These use kernel reduction of explicit finite cases, not the author's center_iff
or enumeration theorems. They are interpretation checks, not new research claims.
-/
namespace P196.Agent7.ReviewOddCenter

open P196.Agent9.InverseFibers P196.Agent7.OddFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

theorem center_zero_exact : ∀ (v : Fin 10) (p : State),
    Center v p 0 ↔ (v = 0 ∧ p = 0) ∨ (v = 1 ∧ p = 2) := by
  decide

theorem center_eighteen_exact : ∀ (v : Fin 10) (p : State),
    Center v p 18 ↔ (v = 8 ∧ p = 1) ∨ (v = 9 ∧ p = 3) := by
  decide

/-- Separate four-row decimal interpretation of every bounded center case. -/
theorem center_carry_table : ∀ (v : Fin 10) (p : State) (z : Fin 19),
    Center v p z.val ↔
      (p = 0 ∧ v.val % 2 = 0 ∧ z.val = v.val) ∨
      (p = 1 ∧ v.val % 2 = 0 ∧ z.val = v.val + 10) ∨
      (p = 2 ∧ v.val % 2 = 1 ∧ z.val = v.val - 1) ∨
      (p = 3 ∧ v.val % 2 = 1 ∧ z.val = v.val + 9) := by
  decide

theorem terminal_boundary_enumeration :
    oddPreimages [] 0 0 = [([], 0)] ∧
    oddPreimages [] 1 2 = [([], 0)] ∧
    oddPreimages [] 8 1 = [([], 18)] ∧
    oddPreimages [] 9 3 = [([], 18)] := by
  decide

theorem terminal_parity_exclusions :
    oddPreimages [] 0 2 = [] ∧ oddPreimages [] 1 0 = [] ∧
    oddPreimages [] 8 3 = [] ∧ oddPreimages [] 9 1 = [] := by
  decide

#print axioms center_zero_exact
#print axioms center_eighteen_exact
#print axioms center_carry_table
#print axioms terminal_boundary_enumeration
#print axioms terminal_parity_exclusions

end P196.Agent7.ReviewOddCenter
