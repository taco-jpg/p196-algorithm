import Lychrel196Research

/-!
Agent #315 — temporal/column restriction follow-up.

The main modular engine already proves exact modulo-99 transition laws.  This
module closes the missing orbit-level lifting for the special divisor 99:
once an actual positive orbit state is divisible by 99, every later state is
also divisible by 99.  This is a conditional absorbing-state theorem; it does
not assert that the orbit of 196 ever enters the 99-class.

The result is useful because a temporal certificate may separately exclude
entry into 99|n, after which the whole future branch is ruled out at once.
-/

namespace Agent315.TemporalColumn99

open Lychrel196 DecimalDigits DecimalModular

/-- Divisibility by 99 is preserved by one ordinary reverse-and-add step. -/
theorem step_preserves_dvd99 (n : Nat) (h : 99 ∣ n) : 99 ∣ step n := by
  by_cases hn : n = 0
  · subst n
    decide
  · obtain ⟨d, L, hc⟩ := canonical_exists n (by omega)
    have hr := DecimalModular.step_mod_of_dvd99 99 n d L (by decide) hc
    have hz := Nat.mod_eq_zero_of_dvd h
    apply Nat.dvd_of_mod_eq_zero
    omega

/-- A 99-divisible orbit state remains 99-divisible forever. -/
theorem orbit_preserves_dvd99 (n k : Nat) (h : 99 ∣ n) :
    99 ∣ orbit n k := by
  induction k with
  | zero => exact h
  | succ k ih =>
      exact step_preserves_dvd99 (orbit n k) ih

/-- Temporal form: if an orbit ever enters the 99-divisible class, every
later time remains in that class. -/
theorem orbit_dvd99_of_dvd99_at
    (n t k : Nat) (h : 99 ∣ orbit n t) :
    99 ∣ orbit n (t + k) := by
  have h' := orbit_preserves_dvd99 (orbit n t) k h
  simpa only [← LychrelCertificates.orbit_add] using h'

#print axioms step_preserves_dvd99
#print axioms orbit_preserves_dvd99
#print axioms orbit_dvd99_of_dvd99_at

end Agent315.TemporalColumn99
