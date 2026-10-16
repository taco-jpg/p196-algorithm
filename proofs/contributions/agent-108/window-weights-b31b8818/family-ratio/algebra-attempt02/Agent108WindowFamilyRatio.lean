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

private theorem ratio_endpoint_product_pos (b k a : Nat) (psi : List Nat → ℝ)
    (hp : PositivePotential b psi) (ha : a ≤ 18) :
    0 < windowProduct b psi (endpoint b k a) := by
  apply windowProduct_pos hp
  intro x hx
  simp only [endpoint, buffer, List.mem_append, List.mem_replicate,
    List.mem_singleton] at hx
  omega

private theorem endpoint_constant_cancel (b k : Nat) (psi : List Nat → ℝ)
    (hp : PositivePotential b psi) :
    endpointConstant b k psi *
        (psi ([11] ++ buffer b) * windowProduct b psi (endpoint b k 9)) =
      psi ([5] ++ buffer b) * windowProduct b psi (endpoint b k 14) := by
  have h11 := ne_of_gt (endpoint_first_potential_pos b 11 psi hp (by decide))
  have h9 := ne_of_gt (ratio_endpoint_product_pos b k 9 psi hp (by decide))
  rw [← endpoint_constant_formula b k psi hp]
  calc
    (psi ([5] ++ buffer b) / psi ([11] ++ buffer b) *
          (windowProduct b psi (endpoint b k 14) /
            windowProduct b psi (endpoint b k 9))) *
        (psi ([11] ++ buffer b) * windowProduct b psi (endpoint b k 9)) =
      (psi ([5] ++ buffer b) / psi ([11] ++ buffer b) * psi ([11] ++ buffer b)) *
        (windowProduct b psi (endpoint b k 14) /
          windowProduct b psi (endpoint b k 9) *
            windowProduct b psi (endpoint b k 9)) := by ring
    _ = _ := by rw [div_mul_cancel₀ _ h11, div_mul_cancel₀ _ h9]

private theorem buffered_power_product (q : ℝ) (b c n : Nat) :
    q ^ (c * (n+1)) * q ^ ((b+4) * n) = q ^ (n * (b+c+4) + c) := by
  rw [← pow_add]
  congr 1
  ring

private theorem buffered_ratio_algebra (b c n : Nat)
    (q H5 H11 E14 E9 C bitWeight : ℝ) (hC : C * (H11 * E9) = H5 * E14) :
    H5 * q ^ (c * (n+1)) * (q ^ ((b+4) * n) * bitWeight) * E14 =
      C * (H11 * q ^ (n * (b+c+4) + c) * E9) * bitWeight := by
  calc
    H5 * q ^ (c * (n+1)) * (q ^ ((b+4) * n) * bitWeight) * E14 =
      (H5 * E14) * (q ^ (c * (n+1)) * q ^ ((b+4) * n)) * bitWeight := by ring
    _ = (C * (H11 * E9)) * q ^ (n * (b+c+4) + c) * bitWeight := by
      rw [← hC, buffered_power_product]
    _ = _ := by ring

#print axioms ratio_buffer_potential_pos
#print axioms binary_block_products
#print axioms ratio_endpoint_product_pos
#print axioms endpoint_constant_cancel
#print axioms buffered_power_product
#print axioms buffered_ratio_algebra

end Agent108.WindowWeights
