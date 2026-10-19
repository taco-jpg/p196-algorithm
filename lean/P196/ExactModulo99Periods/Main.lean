import P196.ExactModulo99Periods.Arithmetic
import P196.Agent119EightFamilies.TemporalResidues
import P196.Drafts.Agent1CeilhalfVerification.PairWeights

set_option autoImplicit false

/-!
Agent #7: exact eventual modulo-99 dynamics for every positive decimal seed.

The ordinary integer orbit is used throughout. The existing divisibility-by-11
absorption theorem supplies the uniform starting time six; the new finite
arithmetic classifies the resulting residues and their least positive periods.
Residue equality does not assert equality or periodicity of integer states,
and these results do not assert palindrome avoidance or a Lychrel number.
-/

namespace Agent7.ResiduePeriods

open Lychrel196

/-- Modulo nine, every ordinary reverse-and-add step doubles the residue. -/
theorem orbit_mod9_pow (n k : Nat) :
    orbit n k % 9 = (2 ^ k * n) % 9 := by
  induction k with
  | zero => simp [orbit]
  | succ k ih =>
    change step (orbit n k) % 9 = _
    rw [Lychrel196.step_mod9]
    calc
      (2 * orbit n k) % 9 = (2 * (orbit n k % 9)) % 9 := by omega
      _ = (2 * ((2 ^ k * n) % 9)) % 9 := by rw [ih]
      _ = (2 * (2 ^ k * n)) % 9 := by omega
      _ = (2 ^ (k + 1) * n) % 9 := by
        rw [Nat.pow_succ]
        simp only [Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm]

/-- The complete eventual residue is determined by the seed modulo nine
and the absolute time modulo six. -/
theorem orbit_mod99_eq_phase99 (n t : Nat)
    (hn : 0 < n) (ht : 6 ≤ t) :
    orbit n t % 99 = phase99 n t := by
  have h11 := AstraModular.orbit_mod11_eq_zero_of_six_le n t hn ht
  have hlift : orbit n t % 99 = 11 * ((5 * orbit n t) % 9) := by omega
  have hp := ExactLengthResidues.pow_mod_reduce_period 2 9 6 t (by decide)
  have hprod : (5 * (2 ^ t * n)) % 9 = (5 * (2 ^ (t % 6) * n)) % 9 := by
    simp only [Nat.mul_mod, Nat.mod_mod, hp]
  calc
    orbit n t % 99 = 11 * ((5 * orbit n t) % 9) := hlift
    _ = 11 * ((5 * (2 ^ t * n)) % 9) := by
      simp only [Nat.mul_mod, orbit_mod9_pow, Nat.mod_mod]
    _ = 11 * ((5 * (2 ^ (t % 6) * n)) % 9) := by rw [hprod]
    _ = phase99 n t := by
      unfold phase99
      simp only [Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm]

/-- At the uniform absorption time, multiplication by fifty-five lifts
the seed residue modulo nine to the unique multiple of eleven modulo 99. -/
theorem orbit_mod99_at_six (n : Nat) (hn : 0 < n) :
    orbit n 6 % 99 = 11 * ((5 * n) % 9) := by
  simpa [phase99] using orbit_mod99_eq_phase99 n 6 hn (by decide)

/-- An individual late return of the residue occurs exactly at a multiple
of the period determined by the initial seed. Zero shifts are included. -/
theorem orbit_mod99_shift_iff (n s P : Nat)
    (hn : 0 < n) (hs : 6 ≤ s) :
    (orbit n (s + P) % 99 = orbit n s % 99) ↔ residuePeriod n ∣ P := by
  rw [orbit_mod99_eq_phase99 n (s + P) hn (by omega),
    orbit_mod99_eq_phase99 n s hn hs]
  exact phase99_shift_iff n s P

/-- Every period of any suffix beginning at time six or later is an exact
multiple of the same least positive period. -/
theorem orbit_mod99_suffix_period_iff (n s P : Nat)
    (hn : 0 < n) (hs : 6 ≤ s) :
    (∀ k, orbit n (s + k + P) % 99 = orbit n (s + k) % 99) ↔
      residuePeriod n ∣ P := by
  constructor
  · intro h
    exact (orbit_mod99_shift_iff n s P hn hs).mp (by simpa using h 0)
  · intro h k
    exact (orbit_mod99_shift_iff n (s + k) P hn (by omega)).mpr h

/-- Positive minimality accompanies the full classification of periods. -/
theorem orbit_mod99_least_period (n s : Nat)
    (hn : 0 < n) (hs : 6 ≤ s) :
    0 < residuePeriod n ∧
      (∀ k, orbit n (s + k + residuePeriod n) % 99 = orbit n (s + k) % 99) ∧
      (∀ P, 0 < P →
        (∀ k, orbit n (s + k + P) % 99 = orbit n (s + k) % 99) →
          residuePeriod n ≤ P) := by
  refine ⟨residuePeriod_pos n,
    (orbit_mod99_suffix_period_iff n s (residuePeriod n) hn hs).mpr (Nat.dvd_refl _),
    ?_⟩
  intro P hP hperiod
  exact Nat.le_of_dvd hP ((orbit_mod99_suffix_period_iff n s P hn hs).mp hperiod)

/-- Equal-time residue synchronization is exactly equality of initial
residues modulo nine; the integer trajectories need not coincide. -/
theorem orbit_mod99_seed_iff (n m t : Nat)
    (hn : 0 < n) (hm : 0 < m) (ht : 6 ≤ t) :
    (orbit n t % 99 = orbit m t % 99) ↔ n % 9 = m % 9 := by
  rw [orbit_mod99_eq_phase99 n t hn ht, orbit_mod99_eq_phase99 m t hm ht]
  exact phase99_seed_iff n m t

/-- The displayed phase formula cannot be extended uniformly to time five.
The seed is the existing sharp absorption example from the foundation. -/
theorem phase_formula_fails_at_five :
    orbit 100 5 % 99 ≠ phase99 100 5 := by decide

#print axioms orbit_mod9_pow
#print axioms orbit_mod99_eq_phase99
#print axioms orbit_mod99_at_six
#print axioms orbit_mod99_shift_iff
#print axioms orbit_mod99_suffix_period_iff
#print axioms orbit_mod99_least_period
#print axioms orbit_mod99_seed_iff
#print axioms phase_formula_fails_at_five

end Agent7.ResiduePeriods
