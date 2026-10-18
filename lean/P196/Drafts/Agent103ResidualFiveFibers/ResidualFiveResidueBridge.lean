import P196.Drafts.Agent103ResidualFiveFibers.ResidualFiveFibers

set_option autoImplicit false

namespace Agent103.ResidualFiveFibers

open Lychrel196

/-- Every ordinary integer in the complete fiber has residue five modulo nine. -/
theorem fiber_member_mod9 (r n : Nat) (h : n ∈ fiber r) : n % 9 = 5 := by
  have hs := (fiber_mem_fixed_width r n).mp h
  have pow_residue (k : Nat) : 10 ^ k % 9 = 1 := by
    induction k with
    | zero => decide
    | succ k ih =>
      rw [Nat.pow_succ, Nat.mul_mod, ih]
  have hp := pow_residue (2 * r + 2)
  have hm : middle r % 9 = 1 := by
    unfold middle
    omega
  have ht := step_mod9 n
  rw [hs.2, hm] at ht
  omega

/-- In this fiber, the original temporal residue is exactly divisibility by eleven. -/
theorem fiber_mod99_iff_mod11 (r n : Nat) (h : n ∈ fiber r) :
    n % 99 = 77 ↔ n % 11 = 0 := by
  have hn := fiber_member_mod9 r n h
  omega

/-- Translate the actual filtered integer count, retaining the original list. -/
theorem fiber_count_mod99_eq_mod11 (r : Nat) :
    (fiber r).countP (fun n => decide (n % 99 = 77)) =
      (fiber r).countP (fun n => decide (n % 11 = 0)) := by
  apply List.countP_congr
  intro n hn
  simp only [fiber_mod99_iff_mod11 r n hn]

#print axioms fiber_member_mod9
#print axioms fiber_mod99_iff_mod11
#print axioms fiber_count_mod99_eq_mod11

end Agent103.ResidualFiveFibers
