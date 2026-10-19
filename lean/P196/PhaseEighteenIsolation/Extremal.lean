import P196.FiniteExteriorHistories.Obstruction

/-!
# The maximal exterior tail quotient

The positional bound for coefficients at most eighteen bounds the original
high numerator by eighteen times its width scale. Equality forces both the
phase and every tail coefficient to be eighteen. The quotient characterized
here can equal two; it is distinct from the actual normalization carry.
-/

namespace Agent5.PhaseEighteenIsolation

open Agent115.ExteriorFactorization

private theorem highValue_maximum_word (S : List Nat)
    (hS : ∀ x ∈ S, x ≤ 18)
    (hmax : highValue S + 2 = 2 * 10 ^ S.length) :
    S = List.replicate S.length 18 := by
  induction S with
  | nil => rfl
  | cons x xs ih =>
      have hx := hS x List.mem_cons_self
      have hxs : ∀ y ∈ xs, y ≤ 18 :=
        fun y hy => hS y (List.mem_cons_of_mem x hy)
      have ht := highValue_lt xs hxs
      have hm : x * 10 ^ xs.length ≤ 18 * 10 ^ xs.length :=
        Nat.mul_le_mul_right (10 ^ xs.length) hx
      rw [highValue_cons, List.length_cons, Nat.pow_succ] at hmax
      have hhead : x * 10 ^ xs.length = 18 * 10 ^ xs.length := by omega
      have htail : highValue xs + 2 = 2 * 10 ^ xs.length := by omega
      have hx18 : x = 18 :=
        Nat.eq_of_mul_eq_mul_right (Nat.pow_pos (by decide)) hhead
      simp only [List.length_cons, List.replicate_succ]
      rw [hx18]
      exact congrArg (List.cons 18) (ih hxs htail)

private theorem rhoNum_le_boundary (d : Nat) (S : List Nat)
    (hd : d ≤ 18) (hS : ∀ x ∈ S, x ≤ 18) :
    rhoNum d S ≤ 18 * 10 ^ S.length := by
  have h := highValue_lt S hS
  unfold rhoNum
  omega

/-- The original tail quotient is at most two for every phase and coefficient
at most eighteen, including an empty tail and phases zero and nine. -/
theorem rho_quotient_le_two (d : Nat) (S : List Nat)
    (hd : d ≤ 18) (hS : ∀ x ∈ S, x ≤ 18) :
    rhoNum d S / (9 * 10 ^ S.length) ≤ 2 := by
  have hb := rhoNum_le_boundary d S hd hS
  have hP : 0 < 10 ^ S.length := Nat.pow_pos (by decide)
  have hD : 0 < 9 * 10 ^ S.length := Nat.mul_pos (by decide) hP
  have hlt : rhoNum d S < 3 * (9 * 10 ^ S.length) := by omega
  have hq := (Nat.div_lt_iff_lt_mul hD).mpr hlt
  omega

/-- The maximal tail quotient identifies exactly phase eighteen followed
by a tail consisting entirely of eighteens. This quotient is not a carry bit. -/
theorem rho_quotient_eq_two_iff (d : Nat) (S : List Nat)
    (hd : d ≤ 18) (hS : ∀ x ∈ S, x ≤ 18) :
    rhoNum d S / (9 * 10 ^ S.length) = 2 ↔
      d = 18 ∧ S = List.replicate S.length 18 := by
  constructor
  · intro hq
    have hlo := Nat.div_mul_le_self (rhoNum d S) (9 * 10 ^ S.length)
    rw [hq] at hlo
    have hhi := rhoNum_le_boundary d S hd hS
    have hvalue := highValue_lt S hS
    unfold rhoNum at hlo hhi
    have hd18 : d = 18 := by omega
    have hmax : highValue S + 2 = 2 * 10 ^ S.length := by omega
    exact ⟨hd18, highValue_maximum_word S hS hmax⟩
  · rintro ⟨rfl, hrep⟩
    have hr := rhoNum_append_replicate 18 ([] : List Nat) S.length
    have hz : rhoNum 18 [] = 18 := rfl
    rw [List.nil_append, hz] at hr
    have hnum : rhoNum 18 S = 10 ^ S.length * 18 :=
      (congrArg (rhoNum 18) hrep).trans hr
    rw [hnum, Nat.mul_comm 9 (10 ^ S.length),
      Nat.mul_div_mul_left _ _ (Nat.pow_pos (by decide) : 0 < 10 ^ S.length)]

#print axioms rho_quotient_le_two
#print axioms rho_quotient_eq_two_iff

end Agent5.PhaseEighteenIsolation
