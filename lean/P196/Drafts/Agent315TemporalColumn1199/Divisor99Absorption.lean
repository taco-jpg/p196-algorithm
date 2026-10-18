import P196.Foundations.LychrelDigitSums

namespace Agent315.TemporalColumn99

open Lychrel196 DecimalDigits AstraModular

/-- Any divisor of 99 is temporally absorbing under reverse-and-add:
if M | n, then M | T(n). -/
theorem step_preserves_dvd_of_dvd99
    (M n : Nat) (hM : M ∣ 99) (h : M ∣ n) :
    M ∣ step n := by
  by_cases hn : n = 0
  · subst n
    exact Nat.dvd_zero M
  · obtain ⟨d, L, hc⟩ := canonical_exists n (by omega)
    have hr := AstraModular.step_mod_of_dvd99 M n d L hM hc
    have hz := Nat.mod_eq_zero_of_dvd h
    apply Nat.dvd_of_mod_eq_zero
    rw [hr, Nat.mul_mod, hz, Nat.mul_zero, Nat.zero_mod]

/-- Every divisor of 99 remains an invariant divisibility class along the
entire future orbit once entered. -/
theorem orbit_preserves_dvd_of_dvd99
    (M n k : Nat) (hM : M ∣ 99) (h : M ∣ n) :
    M ∣ orbit n k := by
  induction k with
  | zero => exact h
  | succ k ih =>
      exact step_preserves_dvd_of_dvd99 M (orbit n k) hM ih

end Agent315.TemporalColumn99
