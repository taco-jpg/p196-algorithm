import Std

/-!
Existence of a positive multiplicative period modulo a positive modulus,
proved by finite-range repetition and coprime cancellation. The proof
also covers modulus one and arbitrary natural bases.
-/

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


theorem bounded_sequence_repeats (q : Nat) :
    ∀ (f : Nat → Nat), (∀ i, f i < q) → ∃ i j, i < j ∧ f i = f j := by
  classical
  induction q with
  | zero =>
    intro f hf
    have := hf 0
    omega
  | succ q ih =>
    intro f hf
    by_cases hit : ∃ j, 0 < j ∧ f 0 = f j
    · obtain ⟨j, hj, heq⟩ := hit
      exact ⟨0, j, hj, heq⟩
    · have hav : ∀ n, f (n + 1) ≠ f 0 := by
        intro n heq
        apply hit
        exact ⟨n + 1, by omega, heq.symm⟩
      let g : Nat → Nat := fun n =>
        if f (n + 1) < f 0 then f (n + 1) else f (n + 1) - 1
      have hg : ∀ n, g n < q := by
        intro n
        have hn := hf (n + 1)
        have hzero := hf 0
        have hne := hav n
        dsimp [g]
        split <;> omega
      obtain ⟨i, j, hij, heq⟩ := ih g hg
      refine ⟨i + 1, j + 1, by omega, ?_⟩
      have hi := hav i
      have hj := hav j
      dsimp [g] at heq
      split at heq <;> split at heq <;> omega


theorem exists_positive_pow_period (a q : Nat)
    (hq : 0 < q) (hc : q.gcd a = 1) :
    ∃ r : Nat, 0 < r ∧ a ^ r % q = 1 % q := by
  by_cases ha : a = 0
  · subst a
    have hqone : q = 1 := by simpa using hc
    subst q
    exact ⟨1, by decide, by decide⟩
  · have hapos : 0 < a := by omega
    obtain ⟨i, j, hij, heq⟩ := bounded_sequence_repeats q
      (fun i => a ^ i % q) (fun i => Nat.mod_lt (a ^ i) hq)
    exact ⟨j - i, by omega, period_of_repeated_powers hapos hc hij heq⟩

theorem exists_positive_ten_period (q : Nat)
    (hq : 0 < q) (hc : q.gcd 10 = 1) :
    ∃ r : Nat, 0 < r ∧ 10 ^ r % q = 1 % q :=
  exists_positive_pow_period 10 q hq hc

end ExactLengthResidues

#print axioms ExactLengthResidues.dvd_sub_of_mod_eq
#print axioms ExactLengthResidues.dvd_of_dvd_mul_of_gcd_eq_one
#print axioms ExactLengthResidues.period_of_repeated_powers
#print axioms ExactLengthResidues.bounded_sequence_repeats
#print axioms ExactLengthResidues.exists_positive_pow_period
#print axioms ExactLengthResidues.exists_positive_ten_period
