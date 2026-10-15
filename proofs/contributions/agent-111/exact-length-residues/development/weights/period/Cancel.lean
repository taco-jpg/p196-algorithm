import Std
namespace ExactLengthResidues

theorem dvd_sub_of_mod_eq {x y q : Nat} (h : x % q = y % q) : q ∣ x - y := by
  refine ⟨x / q - y / q, ?_⟩
  rw [Nat.mul_sub]
  have hx := Nat.mod_add_div x q
  have hy := Nat.mod_add_div y q
  omega

theorem dvd_of_dvd_mul_of_gcd_eq_one {q a b : Nat}
    (hc : q.gcd a = 1) (hd : q ∣ a * b) : q ∣ b := by
  have hh := Nat.dvd_gcd_mul_iff_dvd_mul.mpr hd
  simpa only [hc, Nat.one_mul] using hh

theorem period_of_repeated_powers {a q i j : Nat}
    (ha : 0 < a) (hc : q.gcd a = 1) (hij : i < j)
    (heq : a ^ i % q = a ^ j % q) :
    a ^ (j - i) % q = 1 % q := by
  have hd : q ∣ a ^ j - a ^ i := dvd_sub_of_mod_eq heq.symm
  have hj : j = i + (j - i) := by omega
  rw [hj, Nat.pow_add] at hd
  have hd' : q ∣ a ^ i * (a ^ (j - i) - 1) := by
    simpa only [Nat.mul_sub, Nat.mul_one] using hd
  have hcop : q.gcd (a ^ i) = 1 := Nat.gcd_pow_right_of_gcd_eq_one hc
  have hdiv : q ∣ a ^ (j - i) - 1 :=
    dvd_of_dvd_mul_of_gcd_eq_one hcop hd'
  have hdiv' : q ∣ a ^ (j - i) - 1 := by simpa using hdiv
  have hpos := Nat.pow_pos (n := j - i) ha
  have hs : a ^ (j - i) = (a ^ (j - i) - 1) + 1 := by omega
  calc
    a ^ (j - i) % q = ((a ^ (j - i) - 1) + 1) % q := by rw [← hs]
    _ = 1 % q := by rw [Nat.add_mod, Nat.mod_eq_zero_of_dvd hdiv', Nat.zero_add, Nat.mod_mod]

end ExactLengthResidues
#print axioms ExactLengthResidues.period_of_repeated_powers
