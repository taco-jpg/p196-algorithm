import P196.AllTimePowerResidues.Arithmetic

/-!
Exact fixed-exponent root counts modulo 99 at every time in the ordinary
orbit of 196. The first three residues have a second root-count factor
from the nonzero modulo-eleven coordinate. From time three onward that
coordinate is zero, and the existing six-phase count applies.

Compatibility is a congruence statement. It does not assert an actual
power occurrence, a periodic integer orbit, or a Lychrel conclusion.
-/

set_option autoImplicit false

namespace P196.AllTimePowerResidues

open Lychrel196

/-- Exact count of all distinct residue roots from time zero onward. -/
theorem power_residue_root_count (e k : Nat) (he : 0 < e) :
    ((List.range 99).filter (fun a =>
      decide (a ^ e % 99 = orbit 196 k % 99))).length =
      if Nat.gcd e 6 ∣ k + 4 ∧
          (k < 3 → Nat.gcd e 10 ∣ k + 6) then
        Nat.gcd e 6 * (if k < 3 then Nat.gcd e 10 else 1)
      else 0 := by
  by_cases hk : k < 3
  · rw [orbit_residue_of_lt_three k hk]
    change (Arithmetic.initialRoots e k).length = _
    rw [Arithmetic.initial_root_count e k he hk]
    simp only [hk, true_implies, if_true]
  · rw [orbit_residue_of_three_le k (by omega)]
    change (P196.OrbitPowerResidues.Arithmetic.residueRoots e k).length = _
    rw [P196.OrbitPowerResidues.Arithmetic.root_count e k he]
    simp only [hk, false_implies, and_true, if_false, Nat.mul_one]

/-- Both independent initial phase conditions, followed by the later one. -/
theorem power_residue_compatible_iff (e k : Nat) (he : 0 < e) :
    (∃ a : Nat, a ^ e % 99 = orbit 196 k % 99) ↔
      Nat.gcd e 6 ∣ k + 4 ∧ (k < 3 → Nat.gcd e 10 ∣ k + 6) := by
  constructor
  · rintro ⟨a, ha⟩
    have hres : (a % 99) ^ e % 99 = orbit 196 k % 99 :=
      (P196.OrbitPowerResidues.Arithmetic.power_base_mod a e 99).trans ha
    have hmem : a % 99 ∈ ((List.range 99).filter (fun b =>
        decide (b ^ e % 99 = orbit 196 k % 99))) := by
      simp only [List.mem_filter, List.mem_range, decide_eq_true_eq]
      exact ⟨Nat.mod_lt _ (by decide), hres⟩
    have hpos := List.length_pos_of_mem hmem
    have hcount := power_residue_root_count e k he
    by_cases hc : Nat.gcd e 6 ∣ k + 4 ∧ (k < 3 → Nat.gcd e 10 ∣ k + 6)
    · exact hc
    · rw [if_neg hc] at hcount
      omega
  · intro hc
    have hfactor : 0 < (if k < 3 then Nat.gcd e 10 else 1) := by
      split
      · exact Nat.gcd_pos_of_pos_right e (by decide)
      · decide
    have hpos : 0 < ((List.range 99).filter (fun a =>
        decide (a ^ e % 99 = orbit 196 k % 99))).length := by
      rw [power_residue_root_count e k he, if_pos hc]
      exact Nat.mul_pos (Nat.gcd_pos_of_pos_right e (by decide)) hfactor
    obtain ⟨a, ha⟩ := List.exists_mem_of_length_pos hpos
    have hmem : a < 99 ∧ a ^ e % 99 = orbit 196 k % 99 := by
      simpa only [List.mem_filter, List.mem_range, decide_eq_true_eq] using ha
    exact ⟨a, hmem.2⟩

/-- Every actual power occurrence satisfies the full initial-time restriction. -/
theorem actual_power_time_condition (a e k : Nat) (he : 0 < e)
    (h : a ^ e = orbit 196 k) :
    Nat.gcd e 6 ∣ k + 4 ∧ (k < 3 → Nat.gcd e 10 ∣ k + 6) :=
  (power_residue_compatible_iff e k he).mp
    ⟨a, congrArg (fun n => n % 99) h⟩

/-- Fifth-power compatibility begins exactly at time three. -/
theorem fifth_power_residue_compatible_iff (k : Nat) :
    (∃ a : Nat, a ^ 5 % 99 = orbit 196 k % 99) ↔ 3 ≤ k := by
  rw [power_residue_compatible_iff 5 k (by decide)]
  change (1 ∣ k + 4 ∧ (k < 3 → 5 ∣ k + 6)) ↔ 3 ≤ k
  simp only [Nat.one_dvd, true_and]
  constructor
  · intro h
    by_cases hk : k < 3
    · have hm := Nat.mod_eq_zero_of_dvd (h hk)
      omega
    · omega
  · intro h hk
    omega

/-- Exponent zero is incompatible at every time, including time zero. -/
theorem zero_exponent_incompatible (a k : Nat) :
    a ^ 0 % 99 ≠ orbit 196 k % 99 := by
  change 1 ≠ orbit 196 k % 99
  exact Ne.symm (orbit_residue_ne_one k)

end P196.AllTimePowerResidues
