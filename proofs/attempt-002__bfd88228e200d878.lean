import ModularSpan

namespace ExactLengthResidues

theorem crt_mod_eq_of_coprime (u q p a : Nat)
    (hcop : Nat.gcd u q = 1)
    (hpu : p % u = a % u) (hpq : p % q = a % q) :
    p % (u * q) = a % (u * q) := by
  have hpuz : (p : Int) % (u : Int) = (a : Int) % (u : Int) := by
    exact_mod_cast hpu
  have hpqz : (p : Int) % (q : Int) = (a : Int) % (q : Int) := by
    exact_mod_cast hpq
  obtain ⟨k, hk⟩ := Int.dvd_of_emod_eq_zero
    (Int.emod_eq_emod_iff_emod_sub_eq_zero.mp hpuz)
  obtain ⟨l, hl⟩ := Int.dvd_of_emod_eq_zero
    (Int.emod_eq_emod_iff_emod_sub_eq_zero.mp hpqz)
  obtain ⟨s, t, hst⟩ := gcd_int_span u q
  have hbez : s * (u : Int) + t * (q : Int) = 1 := by
    simpa only [hcop, Int.natCast_one] using hst
  have hd : (u : Int) * (q : Int) ∣ (p : Int) - (a : Int) := by
    refine ⟨s * l + t * k, ?_⟩
    calc
      (p : Int) - (a : Int) =
          (s * u) * (p - a) + (t * q) * (p - a) := by
        rw [← Int.add_mul, hbez, Int.one_mul]
      _ = (s * u) * (q * l) + (t * q) * (u * k) := by
        rw [congrArg (fun x => (s * u) * x) hl,
          congrArg (fun x => (t * q) * x) hk]
      _ = (u * q) * (s * l + t * k) := by
        simp only [Int.mul_add]
        ac_rfl
  have he := Int.emod_eq_emod_iff_emod_sub_eq_zero.mpr
    (Int.emod_eq_zero_of_dvd hd)
  exact_mod_cast he

theorem crt_mod_eq (u q p a : Nat) (_hu : 0 < u) (_hq : 0 < q)
    (hcop : Nat.gcd u q = 1)
    (hpu : p % u = a % u) (hpq : p % q = a % q) :
    p % (u * q) = a % (u * q) :=
  crt_mod_eq_of_coprime u q p a hcop hpu hpq

theorem shifted_modular_span (q c0 c1 a C : Nat) (hq : 0 < q)
    (ha : Nat.gcd q (Nat.gcd c0 c1) ∣ a)
    (hC : Nat.gcd q (Nat.gcd c0 c1) ∣ C) :
    ∃ x, x < q ∧ ∃ y, y < q ∧
      (C + x * c0 + y * c1) % q = a % q := by
  let b := a + q - C % q
  have hgq : Nat.gcd q (Nat.gcd c0 c1) ∣ q := Nat.gcd_dvd_left _ _
  have hgCrem : Nat.gcd q (Nat.gcd c0 c1) ∣ C % q :=
    (Nat.dvd_mod_iff hgq).mpr hC
  have hgb : Nat.gcd q (Nat.gcd c0 c1) ∣ b :=
    Nat.dvd_sub (Nat.dvd_add ha hgq) hgCrem
  obtain ⟨x, hx, y, hy, hxy⟩ := modular_span q c0 c1 b hq hgb
  refine ⟨x, hx, y, hy, ?_⟩
  have hrem := Nat.mod_lt C hq
  have hb : C % q + b = a + q := by dsimp [b]; omega
  rw [Nat.add_assoc, Nat.add_mod C (x * c0 + y * c1) q,
    hxy, Nat.add_mod_mod, hb, Nat.add_mod_right]

end ExactLengthResidues

#print axioms ExactLengthResidues.crt_mod_eq_of_coprime
#print axioms ExactLengthResidues.crt_mod_eq
#print axioms ExactLengthResidues.shifted_modular_span
