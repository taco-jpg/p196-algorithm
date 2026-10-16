import Agent108WindowEndpointWeights
import Agent108WindowObstruction
import Mathlib.Tactic.Ring

/-!
Agent #108, session b31b8818. Exact finite-window family weight ratios.
The real algebra is developed first; the concrete family interfaces are
imported only after their source theorems have been supplied and checked.
-/

namespace Agent108.WindowWeights

private theorem ratio_buffer_potential_pos (b : Nat) (psi : List Nat → ℝ)
    (hp : PositivePotential b psi) : 0 < psi (buffer (b+1)) := by
  apply hp _ (by simp [buffer])
  intro x hx
  have he := List.eq_of_mem_replicate hx
  omega

private theorem binary_block_products (q beta : ℝ) (m : Nat) (f : Bool → ℝ)
    (hf : f false = q ^ m) (ht : f true = q ^ m * beta)
    (es : List Bool) :
    (es.map f).prod = q ^ (m * es.length) * binaryWeight beta es := by
  induction es with
  | nil => simp [binaryWeight]
  | cons e es ih =>
      cases e <;>
        simp only [List.map_cons, List.prod_cons, List.length_cons,
          binaryWeight, hf, ht, ih, Nat.mul_add, Nat.mul_one, pow_add] <;> ring

#print axioms ratio_buffer_potential_pos
#print axioms binary_block_products

end Agent108.WindowWeights
