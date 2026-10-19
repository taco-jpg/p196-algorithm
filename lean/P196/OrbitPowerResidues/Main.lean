import P196.OrbitPowerResidues.Arithmetic

/-!
Exact perfect-power compatibility of the eventual residues of the actual
ordinary decimal orbit of 196.  The number of root residues is zero or
gcd(e,6).  Compatibility is only a congruence statement: the converse does
not assert that a perfect power occurs in the integer orbit.

No integer-orbit periodicity, palindrome exclusion, or Lychrel conclusion
is asserted.  Existing orbit residue dynamics are imported unchanged.
-/

set_option autoImplicit false

namespace P196.OrbitPowerResidues

open Lychrel196 Agent423.TemporalResidues

/-- Exact count of distinct roots among the 99 residues, for every positive exponent. -/
theorem power_residue_root_count (e t : Nat) (he : 0 < e) :
    ((List.range 99).filter (fun a =>
      decide (a ^ e % 99 = orbit 196 (6 + t) % 99))).length =
      if Nat.gcd e 6 ∣ t + 4 then Nat.gcd e 6 else 0 := by
  simpa only [Arithmetic.residueRoots, orbit196_mod99_table] using
    Arithmetic.root_count e t he

/-- A perfect power has the orbit phase precisely in the allowed exponent-time classes. -/
theorem power_residue_compatible_iff (e t : Nat) (he : 0 < e) :
    (∃ a : Nat, a ^ e % 99 = orbit 196 (6 + t) % 99) ↔
      Nat.gcd e 6 ∣ t + 4 := by
  constructor
  · rintro ⟨a, ha⟩
    have hphase : a ^ e % 99 = phase196 t := by
      simpa only [orbit196_mod99_table] using ha
    have hres : (a % 99) ^ e % 99 = phase196 t :=
      (Arithmetic.power_base_mod a e 99).trans hphase
    have hmem : a % 99 ∈ Arithmetic.residueRoots e t := by
      simp only [Arithmetic.residueRoots, List.mem_filter, List.mem_range,
        decide_eq_true_eq]
      exact ⟨Nat.mod_lt _ (by decide), hres⟩
    have hpos := List.length_pos_of_mem hmem
    have hcount := Arithmetic.root_count e t he
    by_cases h : Nat.gcd e 6 ∣ t + 4
    · exact h
    · rw [if_neg h] at hcount
      omega
  · intro h
    have hpos : 0 < (Arithmetic.residueRoots e t).length := by
      rw [Arithmetic.root_count e t he, if_pos h]
      exact Nat.gcd_pos_of_pos_right e (by decide)
    obtain ⟨a, ha⟩ := List.exists_mem_of_length_pos hpos
    have hmem : a < 99 ∧ a ^ e % 99 = phase196 t := by
      simpa only [Arithmetic.residueRoots, List.mem_filter, List.mem_range,
        decide_eq_true_eq] using ha
    exact ⟨a, by simpa only [orbit196_mod99_table] using hmem.2⟩

/-- Actual equality to an e-th power implies the modular time restriction. -/
theorem actual_power_time_condition (a e t : Nat) (he : 0 < e)
    (h : a ^ e = orbit 196 (6 + t)) : Nat.gcd e 6 ∣ t + 4 :=
  (power_residue_compatible_iff e t he).mp
    ⟨a, congrArg (fun n => n % 99) h⟩

theorem square_residue_compatible_iff (t : Nat) :
    (∃ a : Nat, a ^ 2 % 99 = orbit 196 (6 + t) % 99) ↔ t % 2 = 0 := by
  rw [power_residue_compatible_iff 2 t (by decide)]
  change (2 ∣ t + 4) ↔ t % 2 = 0
  constructor
  · intro h
    have hm := Nat.mod_eq_zero_of_dvd h
    omega
  · intro h
    apply Nat.dvd_of_mod_eq_zero
    omega

theorem cube_residue_compatible_iff (t : Nat) :
    (∃ a : Nat, a ^ 3 % 99 = orbit 196 (6 + t) % 99) ↔ t % 3 = 2 := by
  rw [power_residue_compatible_iff 3 t (by decide)]
  change (3 ∣ t + 4) ↔ t % 3 = 2
  constructor
  · intro h
    have hm := Nat.mod_eq_zero_of_dvd h
    omega
  · intro h
    apply Nat.dvd_of_mod_eq_zero
    omega

theorem sixth_power_residue_compatible_iff (t : Nat) :
    (∃ a : Nat, a ^ 6 % 99 = orbit 196 (6 + t) % 99) ↔ t % 6 = 2 := by
  rw [power_residue_compatible_iff 6 t (by decide)]
  change (6 ∣ t + 4) ↔ t % 6 = 2
  constructor
  · intro h
    have hm := Nat.mod_eq_zero_of_dvd h
    omega
  · intro h
    apply Nat.dvd_of_mod_eq_zero
    omega

theorem actual_square_time_even (a t : Nat)
    (h : a ^ 2 = orbit 196 (6 + t)) : t % 2 = 0 :=
  (square_residue_compatible_iff t).mp
    ⟨a, congrArg (fun n => n % 99) h⟩

theorem actual_cube_time_two (a t : Nat)
    (h : a ^ 3 = orbit 196 (6 + t)) : t % 3 = 2 :=
  (cube_residue_compatible_iff t).mp
    ⟨a, congrArg (fun n => n % 99) h⟩

theorem actual_sixth_power_time_two (a t : Nat)
    (h : a ^ 6 = orbit 196 (6 + t)) : t % 6 = 2 :=
  (sixth_power_residue_compatible_iff t).mp
    ⟨a, congrArg (fun n => n % 99) h⟩

end P196.OrbitPowerResidues
