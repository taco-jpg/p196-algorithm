import Agent108WindowProducts
import Mathlib.Data.Real.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset

namespace Agent108.WindowWeights

def windowProduct (b : Nat) (psi : List Nat → ℝ) (w : List Nat) : ℝ :=
  ((windows (b+1) w).map psi).prod

/-- Positivity is required only on actual coefficient windows. -/
def PositivePotential (b : Nat) (psi : List Nat → ℝ) : Prop :=
  ∀ w, w.length = b+1 → (∀ x ∈ w, x ≤ 18) → 0 < psi w

theorem windowProduct_overlap (b : Nat) (psi : List Nat → ℝ)
    (a pad c : List Nat) (hp : pad.length = b) :
    windowProduct b psi (a ++ pad ++ c) =
      windowProduct b psi (a ++ pad) * windowProduct b psi (pad ++ c) := by
  simp [windowProduct, windows_append_overlap b a pad c hp]

end Agent108.WindowWeights
