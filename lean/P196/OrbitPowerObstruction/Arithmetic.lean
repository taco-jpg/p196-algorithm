import P196.OrbitPowerResidues.Arithmetic

/-!
Exact image modulo 99 of all powers with exponent at least two.
The excluded residues are precisely those congruent to three or six
modulo nine. Every other residue has an explicit seventh-power
representative, using the thirteenth power to choose its base.

The finite certificate checks this explicit base for each of the 99
target residues. Generic power congruence is imported unchanged.
-/

set_option autoImplicit false

namespace P196.OrbitPowerObstruction

private theorem gcd_three_of_nonzero (a : Nat) (ha : a % 3 ≠ 0) :
    Nat.gcd a 3 = 1 := by
  have h : ∀ r : Fin 3, r.val ≠ 0 → Nat.gcd r.val 3 = 1 := by
    decide +kernel
  calc
    Nat.gcd a 3 = Nat.gcd 3 a := Nat.gcd_comm a 3
    _ = Nat.gcd (a % 3) 3 := Nat.gcd_rec 3 a
    _ = 1 := h ⟨a % 3, Nat.mod_lt _ (by decide)⟩ ha

private theorem nine_dvd_of_three_dvd_power (a e : Nat) (he : 2 ≤ e)
    (hthree : 3 ∣ a ^ e) : 9 ∣ a ^ e := by
  have ha : 3 ∣ a := by
    by_cases hz : a % 3 = 0
    · exact Nat.dvd_of_mod_eq_zero hz
    · have hg := gcd_three_of_nonzero a hz
      have hp : Nat.gcd (a ^ e) 3 = 1 :=
        Nat.gcd_pow_left_of_gcd_eq_one hg
      have hd : Nat.gcd (a ^ e) 3 = 3 := Nat.gcd_eq_right hthree
      omega
  have hs : 9 ∣ a ^ 2 := by
    simpa only [Nat.pow_two] using Nat.mul_dvd_mul ha ha
  exact Nat.dvd_trans hs (Nat.pow_dvd_pow a he)

private theorem bad_residue_iff (r : Nat) :
    (r % 9 = 3 ∨ r % 9 = 6) ↔ (3 ∣ r ∧ ¬ 9 ∣ r) := by
  simp only [Nat.dvd_iff_mod_eq_zero]
  have hm := Nat.mod_mod_of_dvd r (by decide : 3 ∣ 9)
  omega

private theorem power_avoids_bad_residues (a e : Nat) (he : 2 ≤ e) :
    ¬ (a ^ e % 9 = 3 ∨ a ^ e % 9 = 6) := by
  intro h
  obtain ⟨hthree, hnine⟩ := (bad_residue_iff (a ^ e)).mp h
  exact hnine (nine_dvd_of_three_dvd_power a e he hthree)

/-- Every compatible residue has this explicit seventh-power representative. -/
theorem seventh_power_representative (r : Nat)
    (hthree : r % 9 ≠ 3) (hsix : r % 9 ≠ 6) :
    (r ^ 13 % 99) ^ 7 % 99 = r % 99 := by
  have hfinite : ∀ q : Fin 99, q.val % 9 ≠ 3 → q.val % 9 ≠ 6 →
      (q.val ^ 13 % 99) ^ 7 % 99 = q.val := by
    decide +kernel
  have hthree' : (r % 99) % 9 ≠ 3 := by
    simpa only [Nat.mod_mod_of_dvd r (by decide : 9 ∣ 99)] using hthree
  have hsix' : (r % 99) % 9 ≠ 6 := by
    simpa only [Nat.mod_mod_of_dvd r (by decide : 9 ∣ 99)] using hsix
  have h := hfinite ⟨r % 99, Nat.mod_lt _ (by decide)⟩ hthree' hsix'
  have hp := P196.OrbitPowerResidues.Arithmetic.power_base_mod r 13 99
  rw [hp] at h
  exact h

/-- Exact modular compatibility with some exponent at least two. -/
theorem nontrivial_power_residue_iff (r : Nat) :
    (∃ a e : Nat, 2 ≤ e ∧ a ^ e % 99 = r % 99) ↔
      r % 9 ≠ 3 ∧ r % 9 ≠ 6 := by
  constructor
  · rintro ⟨a, e, he, hroot⟩
    have hm := congrArg (fun x => x % 9) hroot
    have hmod : a ^ e % 9 = r % 9 := by
      simpa only [Nat.mod_mod_of_dvd _ (by decide : 9 ∣ 99)] using hm
    have h := power_avoids_bad_residues a e he
    rw [hmod] at h
    exact not_or.mp h
  · rintro ⟨hthree, hsix⟩
    exact ⟨r ^ 13 % 99, 7, by decide,
      seventh_power_representative r hthree hsix⟩

end P196.OrbitPowerObstruction
