import Agent108WindowFamilyProducts
import Agent108WindowEndpointWeights
import Agent108WindowObstruction
import Mathlib.Tactic.Ring

/-!
Agent #108, session b31b8818. Exact finite-window family weight ratios,
using the concrete buffered-word product formulas and the original
unpadded endpoint constants. All buffer and terminal lengths are retained.
-/

namespace Agent108.WindowWeights

private theorem ratio_buffer_potential_pos (b : Nat) (psi : List Nat → ℝ)
    (hp : PositivePotential b psi) : 0 < psi (buffer (b+1)) := by
  apply hp _ (by simp [buffer])
  intro x hx
  have he := List.eq_of_mem_replicate hx
  omega

/-- The relative weight of the true block against the all-nine block. -/
noncomputable def localBeta (b : Nat) (psi : List Nat → ℝ) : ℝ :=
  windowProduct b psi (localBlock b true) / psi (buffer (b+1)) ^ (b+4)

theorem localBeta_pos (b : Nat) (psi : List Nat → ℝ)
    (hp : PositivePotential b psi) : 0 < localBeta b psi := by
  unfold localBeta
  apply div_pos
  · apply windowProduct_pos hp
    intro x hx
    simp [localBlock, block, buffer] at hx
    omega
  · exact pow_pos (ratio_buffer_potential_pos b psi hp) _

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

/-- Every target coefficient is legal for the original window potential. -/
theorem targetHalf_weight_pos (b c k r : Nat) (psi : List Nat → ℝ)
    (hp : PositivePotential b psi) :
    0 < windowProduct b psi (targetHalf (b+c) k r) := by
  apply windowProduct_pos hp
  intro x hx
  simp only [targetHalf, List.mem_append, List.mem_replicate,
    List.mem_singleton] at hx
  omega

/-- Extract the common all-nine weight from each of the binary blocks. -/
theorem blockProducts_binary_factor (b : Nat) (psi : List Nat → ℝ)
    (es : List Bool) (hp : PositivePotential b psi) :
    (es.map (blockProduct b psi)).prod =
      psi (buffer (b+1)) ^ ((b+4) * es.length) *
        binaryWeight (localBeta b psi) es := by
  refine binary_block_products (psi (buffer (b+1))) (localBeta b psi) (b+4)
    (blockProduct b psi) (blockProduct_false b psi) ?_ es
  simpa only [localBeta, blockProduct] using
    (mul_div_cancel₀ (windowProduct b psi (localBlock b true))
      (pow_ne_zero (b+4) (ne_of_gt (ratio_buffer_potential_pos b psi hp)))).symm

/-- Exact source/target weight ratio for arbitrary extra buffer length c. -/
theorem inputHalf_product_ratio (b c k : Nat) (psi : List Nat → ℝ)
    (es : List Bool) (hp : PositivePotential b psi) :
    windowProduct b psi (inputHalf (b+c) k es) =
      endpointConstant b k psi *
        windowProduct b psi (targetHalf (b+c) k es.length) *
          binaryWeight (localBeta b psi) es := by
  rw [inputHalf_product b c k psi es, blockProducts_binary_factor b psi es hp,
    targetHalf_product b c k es.length psi]
  exact buffered_ratio_algebra b c es.length _ _ _ _ _ _ _
    (endpoint_constant_cancel b k psi hp)

/-- The exact total over every binary choice, including the zero-block family. -/
theorem inputHalf_exact_total (b c k r : Nat) (psi : List Nat → ℝ)
    (hp : PositivePotential b psi) :
    ((choices r).map (fun es => windowProduct b psi (inputHalf (b+c) k es))).sum =
      endpointConstant b k psi * windowProduct b psi (targetHalf (b+c) k r) *
        (1 + localBeta b psi) ^ r := by
  refine weighted_family_total r _ _ _ _ ?_
  intro es hes
  simpa only [choices_mem_length r hes] using
    inputHalf_product_ratio b c k psi es hp

#print axioms ratio_buffer_potential_pos
#print axioms localBeta_pos
#print axioms binary_block_products
#print axioms ratio_endpoint_product_pos
#print axioms endpoint_constant_cancel
#print axioms buffered_power_product
#print axioms buffered_ratio_algebra
#print axioms targetHalf_weight_pos
#print axioms blockProducts_binary_factor
#print axioms inputHalf_product_ratio
#print axioms inputHalf_exact_total

end Agent108.WindowWeights
