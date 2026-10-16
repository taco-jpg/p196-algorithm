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
  unfold windowProduct
  rw [windows_append_overlap b a pad c hp]
  simp

theorem window_mem_valid {b : Nat} {v w : List Nat}
    (hw : w ∈ windows (b+1) v) :
    w.length = b+1 ∧ ∀ x ∈ w, x ∈ v := by
  rw [windows_eq_range_map] at hw
  obtain ⟨i, hi, rfl⟩ := List.mem_map.mp hw
  have hi' := List.mem_range.mp hi
  constructor
  · simp only [List.length_take, List.length_drop]
    omega
  · intro x hx
    exact List.mem_of_mem_drop (List.mem_of_mem_take hx)

theorem positive_list_product {α : Type} (f : α → ℝ) (xs : List α)
    (hf : ∀ x ∈ xs, 0 < f x) : 0 < (xs.map f).prod := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
      simp only [List.map_cons, List.prod_cons]
      exact mul_pos (hf x (by simp)) (ih (fun y hy => hf y (by simp [hy])))

theorem windowProduct_pos {b : Nat} {psi : List Nat → ℝ}
    (hpsi : PositivePotential b psi) (v : List Nat)
    (hv : ∀ x ∈ v, x ≤ 18) : 0 < windowProduct b psi v := by
  apply positive_list_product
  intro w hw
  obtain ⟨hlen, hmem⟩ := window_mem_valid hw
  exact hpsi w hlen (fun x hx => hv x (hmem x hx))

theorem windowProduct_single (b : Nat) (psi : List Nat → ℝ)
    (w : List Nat) (hw : w.length = b+1) :
    windowProduct b psi w = psi w := by
  have hn : w.length-b = 1 := by omega
  simp [windowProduct, windows_eq_range_map, hn, List.range_succ,
    List.take_of_length_le hw.le]

theorem windows_replicate (b n a : Nat) :
    windows (b+1) (List.replicate n a) =
      List.replicate (n-b) (List.replicate (b+1) a) := by
  rw [windows_eq_range_map]
  simp only [List.length_replicate]
  calc
    (List.range (n-b)).map (fun i => ((List.replicate n a).drop i).take (b+1)) =
        (List.range (n-b)).map (fun _ => List.replicate (b+1) a) := by
      apply List.map_congr_left
      intro i hi
      have hi' := List.mem_range.mp hi
      simp only [List.drop_replicate, List.take_replicate]
      rw [Nat.min_eq_left (by omega)]
    _ = _ := by simp

theorem windowProduct_replicate (b n a : Nat) (psi : List Nat → ℝ) :
    windowProduct b psi (List.replicate n a) =
      psi (List.replicate (b+1) a) ^ (n-b) := by
  simp [windowProduct, windows_replicate]

end Agent108.WindowWeights
