import Std

set_option autoImplicit false

/-!
# Exact periods of the eventual decimal residue phases

Agent #7, task #184. This module is finite modular arithmetic only.
The separate ordinary-orbit bridge identifies these phases with the actual
reverse-and-add orbit from absolute time six onward. The phase period does
not assert periodicity of an ordinary integer orbit.
-/

namespace Agent7.ResiduePeriods

/-- The exact residue period, determined by the seed modulo nine. -/
def residuePeriod (n : Nat) : Nat :=
  if n % 9 = 0 then 1 else if n % 3 = 0 then 2 else 6

/-- The modulo-99 phase at absolute time `t`, represented in `[0,99)`. -/
def phase99 (n t : Nat) : Nat :=
  11 * ((2 ^ (t % 6) * 5 * n) % 9)

theorem residuePeriod_pos (n : Nat) : 0 < residuePeriod n := by
  unfold residuePeriod
  split <;> (try split) <;> omega

theorem residuePeriod_dvd_six (n : Nat) : residuePeriod n ∣ 6 := by
  unfold residuePeriod
  split <;> (try split) <;> decide

theorem residuePeriod_mod_nine (n : Nat) :
    residuePeriod (n % 9) = residuePeriod n := by
  simp only [residuePeriod, Nat.mod_mod,
    Nat.mod_mod_of_dvd _ (by decide : 3 ∣ 9)]

theorem residuePeriod_eq_one_iff (n : Nat) :
    residuePeriod n = 1 ↔ n % 9 = 0 := by
  unfold residuePeriod
  split <;> (try split) <;> omega

theorem residuePeriod_eq_two_iff (n : Nat) :
    residuePeriod n = 2 ↔ n % 9 ≠ 0 ∧ n % 3 = 0 := by
  unfold residuePeriod
  split <;> (try split) <;> omega

theorem residuePeriod_eq_six_iff (n : Nat) :
    residuePeriod n = 6 ↔ n % 3 ≠ 0 := by
  have hmod := Nat.mod_mod_of_dvd n (by decide : 3 ∣ 9)
  unfold residuePeriod
  split <;> (try split) <;> omega

theorem residuePeriod_dvd_mod_six (n P : Nat) :
    residuePeriod n ∣ P % 6 ↔ residuePeriod n ∣ P := by
  unfold residuePeriod
  split
  · simp
  · split
    · constructor
      · intro h
        apply Nat.dvd_of_mod_eq_zero
        have := Nat.mod_eq_zero_of_dvd h
        omega
      · intro h
        apply Nat.dvd_of_mod_eq_zero
        have := Nat.mod_eq_zero_of_dvd h
        omega
    · constructor
      · intro h
        apply Nat.dvd_of_mod_eq_zero
        have := Nat.mod_eq_zero_of_dvd h
        omega
      · intro h
        apply Nat.dvd_of_mod_eq_zero
        have := Nat.mod_eq_zero_of_dvd h
        omega

theorem phase99_mod_seed (n t : Nat) : phase99 (n % 9) t = phase99 n t := by
  simp only [phase99, Nat.mul_mod, Nat.mod_mod]

theorem phase99_mod_time (n t : Nat) : phase99 n (t % 6) = phase99 n t := by
  simp only [phase99, Nat.mod_mod]

theorem phase99_add_mod (n t P : Nat) :
    phase99 n (t % 6 + P % 6) = phase99 n (t + P) := by
  unfold phase99
  rw [← Nat.add_mod]

theorem phase99_zero (n : Nat) : phase99 n 0 = 11 * ((5 * n) % 9) := by
  simp only [phase99, Nat.zero_mod, Nat.pow_zero, Nat.one_mul]

theorem phase99_lt (n t : Nat) : phase99 n t < 99 := by
  have := Nat.mod_lt (2 ^ (t % 6) * 5 * n) (by decide : 0 < 9)
  unfold phase99
  omega

theorem phase99_dvd_eleven (n t : Nat) : 11 ∣ phase99 n t := by
  exact ⟨(2 ^ (t % 6) * 5 * n) % 9, rfl⟩

private theorem finite_phase_shift : ∀ (n : Fin 9) (t P : Fin 6),
    phase99 n.val (t.val + P.val) = phase99 n.val t.val ↔
      residuePeriod n.val ∣ P.val := by
  decide

/-- At every phase, a shift returns to the same residue exactly when the
seed's exact period divides the shift. The zero shift is included. -/
theorem phase99_shift_iff (n t P : Nat) :
    phase99 n (t + P) = phase99 n t ↔ residuePeriod n ∣ P := by
  have h := finite_phase_shift
    ⟨n % 9, Nat.mod_lt _ (by decide)⟩
    ⟨t % 6, Nat.mod_lt _ (by decide)⟩
    ⟨P % 6, Nat.mod_lt _ (by decide)⟩
  change phase99 (n % 9) (t % 6 + P % 6) = phase99 (n % 9) (t % 6) ↔
    residuePeriod (n % 9) ∣ P % 6 at h
  simpa only [phase99_mod_seed, phase99_add_mod, phase99_mod_time,
    residuePeriod_mod_nine, residuePeriod_dvd_mod_six] using h

private theorem finite_phase_seed : ∀ (n m : Fin 9) (t : Fin 6),
    phase99 n.val t.val = phase99 m.val t.val ↔ n.val = m.val := by
  decide

/-- At a common time, the phase distinguishes exactly the nine seed
classes modulo nine. -/
theorem phase99_seed_iff (n m t : Nat) :
    phase99 n t = phase99 m t ↔ n % 9 = m % 9 := by
  have h := finite_phase_seed
    ⟨n % 9, Nat.mod_lt _ (by decide)⟩
    ⟨m % 9, Nat.mod_lt _ (by decide)⟩
    ⟨t % 6, Nat.mod_lt _ (by decide)⟩
  change phase99 (n % 9) (t % 6) = phase99 (m % 9) (t % 6) ↔
    n % 9 = m % 9 at h
  simpa only [phase99_mod_seed, phase99_mod_time] using h

#print axioms residuePeriod_pos
#print axioms residuePeriod_dvd_six
#print axioms residuePeriod_eq_one_iff
#print axioms residuePeriod_eq_two_iff
#print axioms residuePeriod_eq_six_iff
#print axioms phase99_shift_iff
#print axioms phase99_seed_iff

end Agent7.ResiduePeriods
