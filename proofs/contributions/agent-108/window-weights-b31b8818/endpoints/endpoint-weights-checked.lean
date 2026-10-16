import Agent108WindowEndpoints
import Agent108WindowWeights

/-!
Agent #108, session b31b8818.  The endpoint constants from section 3 of the
existing folded-weight obstruction, with the original unpadded convention.
Only legal coefficient windows are required to have positive potential.
-/

namespace Agent108.WindowWeights

/-- The varying endpoint windows stop at min k b, including short centers. -/
noncomputable def endpointRatio (b k : Nat) (psi : List Nat → ℝ) : ℝ :=
  ((List.range (min k b + 1)).map (fun j =>
    psi (List.replicate (b-j) 9 ++ [14] ++ List.replicate j 18) /
    psi (List.replicate (b-j) 9 ++ [9] ++ List.replicate j 18))).prod

/-- Both independent endpoint corrections, without a width-only factor. -/
noncomputable def endpointConstant (b k : Nat) (psi : List Nat → ℝ) : ℝ :=
  (psi ([5] ++ buffer b) / psi ([11] ++ buffer b)) * endpointRatio b k psi

private theorem endpoint_prod_map_div {α : Type} (l : List α) (f g : α → ℝ) :
    (l.map (fun x => f x / g x)).prod = (l.map f).prod / (l.map g).prod := by
  induction l with
  | nil => simp
  | cons a l ih => simp only [List.map_cons, List.prod_cons, ih, div_mul_div_comm]

private theorem endpoint_prod_map_pos {α : Type} (l : List α) (f : α → ℝ)
    (hp : ∀ x ∈ l, 0 < f x) : 0 < (l.map f).prod := by
  induction l with
  | nil => simp
  | cons a l ih =>
      simp only [List.map_cons, List.prod_cons]
      exact mul_pos (hp a (by simp)) (ih (fun x hx => hp x (by simp [hx])))

/-- Exact product formula; no positivity assumption is needed for this identity. -/
theorem endpoint_product (b k a : Nat) (psi : List Nat → ℝ) :
    windowProduct b psi (endpoint b k a) =
      ((List.range (min k b + 1)).map (fun j =>
        psi (List.replicate (b-j) 9 ++ [a] ++ List.replicate j 18))).prod *
      psi (List.replicate (b+1) 18) ^ (k-b) := by
  simp only [windowProduct, endpoint_windows, List.map_append, List.prod_append,
    List.map_map, Function.comp_def, List.map_replicate, List.prod_replicate]

theorem endpoint_cross_potential_pos (b a j : Nat) (psi : List Nat → ℝ)
    (hp : PositivePotential b psi) (ha : a ≤ 18) (hj : j ≤ b) :
    0 < psi (List.replicate (b-j) 9 ++ [a] ++ List.replicate j 18) := by
  apply hp
  · simp only [List.length_append, List.length_replicate, List.length_cons,
      List.length_nil]
    omega
  · intro x hx
    simp only [List.mem_append, List.mem_replicate, List.mem_singleton] at hx
    omega

theorem endpoint_eighteen_potential_pos (b : Nat) (psi : List Nat → ℝ)
    (hp : PositivePotential b psi) :
    0 < psi (List.replicate (b+1) 18) := by
  apply hp _ (by simp)
  intro x hx
  have he := List.eq_of_mem_replicate hx
  omega

theorem endpoint_first_potential_pos (b a : Nat) (psi : List Nat → ℝ)
    (hp : PositivePotential b psi) (ha : a ≤ 18) :
    0 < psi ([a] ++ buffer b) := by
  apply hp
  · simp [buffer, Nat.add_comm]
  · intro x hx
    simp only [buffer, List.mem_append, List.mem_replicate, List.mem_singleton] at hx
    omega

/-- The common terminal all-eighteen factor cancels, also when its exponent is zero. -/
theorem endpoint_ratio (b k : Nat) (psi : List Nat → ℝ)
    (hp : PositivePotential b psi) :
    windowProduct b psi (endpoint b k 14) /
      windowProduct b psi (endpoint b k 9) = endpointRatio b k psi := by
  rw [endpoint_product, endpoint_product]
  rw [mul_div_mul_right _ _
    (pow_ne_zero _ (ne_of_gt (endpoint_eighteen_potential_pos b psi hp)))]
  exact (endpoint_prod_map_div _ _ _).symm

theorem endpoint_ratio_pos (b k : Nat) (psi : List Nat → ℝ)
    (hp : PositivePotential b psi) : 0 < endpointRatio b k psi := by
  apply endpoint_prod_map_pos
  intro j hj
  have hh : j < min k b + 1 := List.mem_range.mp hj
  exact div_pos
    (endpoint_cross_potential_pos b 14 j psi hp (by decide) (by omega))
    (endpoint_cross_potential_pos b 9 j psi hp (by decide) (by omega))

theorem endpoint_first_ratio_pos (b : Nat) (psi : List Nat → ℝ)
    (hp : PositivePotential b psi) :
    0 < psi ([5] ++ buffer b) / psi ([11] ++ buffer b) := by
  exact div_pos (endpoint_first_potential_pos b 5 psi hp (by decide))
    (endpoint_first_potential_pos b 11 psi hp (by decide))

theorem endpoint_constant_pos (b k : Nat) (psi : List Nat → ℝ)
    (hp : PositivePotential b psi) : 0 < endpointConstant b k psi := by
  exact mul_pos (endpoint_first_ratio_pos b psi hp) (endpoint_ratio_pos b k psi hp)

/-- The exact head correction times the exact unpadded endpoint ratio. -/
theorem endpoint_constant_formula (b k : Nat) (psi : List Nat → ℝ)
    (hp : PositivePotential b psi) :
    (psi ([5] ++ buffer b) / psi ([11] ++ buffer b)) *
      (windowProduct b psi (endpoint b k 14) /
        windowProduct b psi (endpoint b k 9)) = endpointConstant b k psi := by
  rw [endpoint_ratio b k psi hp]
  rfl

#print axioms endpoint_product
#print axioms endpoint_cross_potential_pos
#print axioms endpoint_eighteen_potential_pos
#print axioms endpoint_first_potential_pos
#print axioms endpoint_ratio
#print axioms endpoint_ratio_pos
#print axioms endpoint_first_ratio_pos
#print axioms endpoint_constant_pos
#print axioms endpoint_constant_formula

end Agent108.WindowWeights
