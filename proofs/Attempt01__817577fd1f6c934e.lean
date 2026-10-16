import Std

/-! Bounded modular generation by two natural coefficients, proved from
Euclid's algorithm and integer remainder arithmetic. -/
namespace ExactLengthResidues

/-- An integer Bézout representation of the natural gcd. -/
theorem gcd_int_span (m n : Nat) :
    ∃ x y : Int, x * (m : Int) + y * (n : Int) = (Nat.gcd m n : Int) := by
  induction m using Nat.strongRecOn generalizing n with
  | ind m ih =>
    by_cases hm : m = 0
    · subst m
      exact ⟨0, 1, by simp⟩
    · obtain ⟨x, y, hxy⟩ := ih (n % m) (Nat.mod_lt n (by omega)) m
      refine ⟨y - x * (n / m : Nat), x, ?_⟩
      have hd : (n % m : Nat) + (m : Int) * (n / m : Nat) = (n : Int) := by
        exact_mod_cast Nat.mod_add_div n m
      rw [Nat.gcd_rec]
      calc
        (y - x * (n / m : Nat)) * (m : Int) + x * (n : Int) =
            x * (n % m : Nat) + y * (m : Int) := by
          rw [← hd, Int.sub_mul, Int.mul_add]
          have he : x * ((m : Int) * (n / m : Nat)) =
              (x * (n / m : Nat)) * (m : Int) := by ac_rfl
          rw [he]
          omega
        _ = _ := hxy

end ExactLengthResidues

#print axioms ExactLengthResidues.gcd_int_span
