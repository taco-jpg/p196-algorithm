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

/-- A multiple of the three-way gcd is an integer combination of all
three generators. -/
theorem gcd_three_int_span (q c0 c1 a : Nat)
    (ha : Nat.gcd q (Nat.gcd c0 c1) ∣ a) :
    ∃ u x y : Int,
      u * (q : Int) + x * (c0 : Int) + y * (c1 : Int) = (a : Int) := by
  obtain ⟨k, hk⟩ := ha
  obtain ⟨u, v, huv⟩ := gcd_int_span q (Nat.gcd c0 c1)
  obtain ⟨s, t, hst⟩ := gcd_int_span c0 c1
  have hak : (a : Int) = (Nat.gcd q (Nat.gcd c0 c1) : Int) * (k : Int) := by
    exact_mod_cast hk
  refine ⟨u * k, v * s * k, v * t * k, ?_⟩
  calc
    (u * k) * q + (v * s * k) * c0 + (v * t * k) * c1 =
        (u * q + v * (s * c0 + t * c1)) * k := by
      simp only [Int.mul_add, Int.add_mul]
      ac_rfl
    _ = a := by rw [hst, huv]; exact hak.symm

/-- Every residue divisible by the gcd of the modulus and both generators
has a representative using coefficients below the positive modulus. -/
theorem modular_span (q c0 c1 a : Nat) (hq : 0 < q)
    (ha : Nat.gcd q (Nat.gcd c0 c1) ∣ a) :
    ∃ x, x < q ∧ ∃ y, y < q ∧ (x * c0 + y * c1) % q = a % q := by
  obtain ⟨u, x, y, hxy⟩ := gcd_three_int_span q c0 c1 a ha
  have hqz : (0 : Int) < (q : Int) := by omega
  have hqne : (q : Int) ≠ 0 := by omega
  let X := (x % (q : Int)).toNat
  let Y := (y % (q : Int)).toNat
  have hX : (X : Int) = x % (q : Int) :=
    Int.toNat_of_nonneg (Int.emod_nonneg x hqne)
  have hY : (Y : Int) = y % (q : Int) :=
    Int.toNat_of_nonneg (Int.emod_nonneg y hqne)
  have hXlt := Int.emod_lt_of_pos x hqz
  have hYlt := Int.emod_lt_of_pos y hqz
  refine ⟨X, by omega, Y, by omega, ?_⟩
  have hm : (x * (c0 : Int) + y * (c1 : Int)) % (q : Int) =
      (a : Int) % (q : Int) := by
    have he : ((x * (c0 : Int) + y * (c1 : Int)) + (q : Int) * u) %
        (q : Int) = (a : Int) % (q : Int) := by
      congr 1
      calc
        _ = u * (q : Int) + x * (c0 : Int) + y * (c1 : Int) := by ac_rfl
        _ = _ := hxy
    simpa using he
  have he : ((X : Int) * c0 + (Y : Int) * c1) % (q : Int) =
      (x * (c0 : Int) + y * (c1 : Int)) % (q : Int) := by
    rw [hX, hY]
    simp only [Int.add_emod, Int.mul_emod, Int.emod_emod]
  apply Int.ofNat_inj.mp
  simpa only [Int.ofNat_emod, Int.natCast_add, Int.natCast_mul] using he.trans hm

end ExactLengthResidues

#print axioms ExactLengthResidues.gcd_int_span

#print axioms ExactLengthResidues.gcd_three_int_span
#print axioms ExactLengthResidues.modular_span
