import Std

namespace ExactLengthResidues

 theorem pow_mod_reduce_period (a q r i : Nat)
    (hperiod : a ^ r % q = 1 % q) :
    a ^ i % q = a ^ (i % r) % q := by
  have hp : ∀ n : Nat, (a ^ r) ^ n % q = 1 % q := by
    intro n
    induction n with
    | zero => rfl
    | succ n ih =>
      rw [Nat.pow_succ, Nat.mul_mod, ih, hperiod, ← Nat.mul_mod, Nat.mul_one]
  calc
    a ^ i % q = a ^ (i % r + r * (i / r)) % q := by rw [Nat.mod_add_div]
    _ = (a ^ (i % r) % q * ((a ^ r) ^ (i / r) % q)) % q := by
      rw [Nat.pow_add, Nat.pow_mul, Nat.mul_mod]
    _ = (a ^ (i % r) % q * (1 % q)) % q := by rw [hp]
    _ = a ^ (i % r) % q := by rw [← Nat.mul_mod, Nat.mul_one]

 theorem pow_mod_period (a q r i j : Nat)
    (hperiod : a ^ r % q = 1 % q)
    (hij : i % r = j % r) :
    a ^ i % q = a ^ j % q := by
  rw [pow_mod_reduce_period a q r i hperiod,
    pow_mod_reduce_period a q r j hperiod, hij]

end ExactLengthResidues

#print axioms ExactLengthResidues.pow_mod_reduce_period
#print axioms ExactLengthResidues.pow_mod_period
