import P196.OrbitPowerObstruction.Arithmetic

/-!
The exact modulo-99 obstruction to every exponent at least two is
invariant along each ordinary decimal reverse-and-add orbit, including
time zero. A seed divisible by three but not by nine therefore has no
integer perfect power anywhere in its orbit.

For every other seed, each orbit residue has a seventh-power
representative. This modular converse asserts no equality to a power
in the integer orbit, and gives no palindrome or Lychrel conclusion.
-/

set_option autoImplicit false

namespace P196.OrbitPowerObstruction

open Lychrel196

private theorem orbit_good_residue_iff (n t : Nat) :
    (orbit n t % 9 ≠ 3 ∧ orbit n t % 9 ≠ 6) ↔
      n % 9 ≠ 3 ∧ n % 9 ≠ 6 := by
  induction t with
  | zero => rfl
  | succ t ih =>
    change (step (orbit n t) % 9 ≠ 3 ∧ step (orbit n t) % 9 ≠ 6) ↔ _
    simp only [step_mod9]
    have hstep : ((2 * orbit n t) % 9 ≠ 3 ∧ (2 * orbit n t) % 9 ≠ 6) ↔
        (orbit n t % 9 ≠ 3 ∧ orbit n t % 9 ≠ 6) := by omega
    exact hstep.trans ih

/-- Exact modular compatibility for every seed and every natural time. -/
theorem orbit_nontrivial_power_residue_iff (n t : Nat) :
    (∃ a e : Nat, 2 ≤ e ∧ a ^ e % 99 = orbit n t % 99) ↔
      n % 9 ≠ 3 ∧ n % 9 ≠ 6 := by
  rw [nontrivial_power_residue_iff]
  exact orbit_good_residue_iff n t

/-- Every orbit from a seed with exactly one factor of three avoids all such powers. -/
theorem orbit_ne_nontrivial_power (n t a e : Nat)
    (hn : 3 ∣ n ∧ ¬ 9 ∣ n) (he : 2 ≤ e) : orbit n t ≠ a ^ e := by
  intro h
  have hgood := (orbit_nontrivial_power_residue_iff n t).mp
    ⟨a, e, he, congrArg (fun x => x % 99) h.symm⟩
  have hthree := Nat.mod_eq_zero_of_dvd hn.1
  have hnine : n % 9 ≠ 0 := fun hz => hn.2 (Nat.dvd_of_mod_eq_zero hz)
  have hm := Nat.mod_mod_of_dvd n (by decide : 3 ∣ 9)
  omega

end P196.OrbitPowerObstruction
