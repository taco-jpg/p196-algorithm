import P196.Agent112NeutralNumericalArithmetic.Normalization

/-!
# A single neutral-pair peel from numerical divisibility

For a bounded symmetric center of width at least two, divisibility of its
signed value by the base forces both exterior coefficients to be neutral.
Removing those coefficients preserves bounds 和 symmetry, 和 divides the
signed value by the base. Zero values 和 empty interiors are included.

This is the one-pair sufficiency step for Agent 112's numerical trim
converse. The forward neutral-padding identities 和 accepted-chain scope
are Agent 119's separate work. Only the existential peel is public here;
the elementary one-pair value calculation is private proof support.
No choice of maximal trim, padding quotient, cycle, or Lychrel claim is made.
-/

namespace Agent112.NeutralNumericalArithmetic

open Agent120.Neutral

private theorem head_neutral_of_signed_multiple (b : Nat) (hb : 2 ≤ b)
    (d : Nat) (T : List Nat) (hd : d ≤ 2 * (b - 1)) (z : Int)
    (hz : signedValue b (d :: T) = (b : Int) * z) : d = b - 1 := by
  have hvalue : ((d + 1 : Nat) : Int) +
      (b : Int) * ((val b T : Int) - ((b ^ T.length : Nat) : Int)) = (b : Int) * z := by
    unfold signedValue at hz
    simp only [val_cons, List.length_cons, Nat.pow_succ,
      Int.natCast_add, Int.natCast_mul] at hz
    simp only [Int.natCast_add, Int.natCast_one, Int.mul_sub]
    rw [Int.mul_comm (b : Int) ((b ^ T.length : Nat) : Int)]
    omega
  have hmod : (d + 1) % b = 0 := by
    have hm := congrArg (fun n : Int => n % (b : Int)) hvalue
    simp only [Int.add_mul_emod_self_left, Int.mul_emod_right] at hm
    change (((d + 1) % b : Nat) : Int) = 0 at hm
    omega
  by_cases hsmall : d + 1 < b
  · rw [Nat.mod_eq_of_lt hsmall] at hmod
    omega
  · rw [Nat.mod_eq_sub_mod (by omega), Nat.mod_eq_of_lt (by omega : d + 1 - b < b)] at hmod
    omega

private theorem signedValue_one_pair (b : Nat) (hb : 2 ≤ b) (D : List Nat) :
    signedValue b ((b - 1) :: (D ++ [b - 1])) = (b : Int) * signedValue b D := by
  have hh : ((b - 1 : Nat) : Int) = (b : Int) - 1 := by omega
  have hlen : ((b - 1) :: (D ++ [b - 1])).length = D.length + 2 := by simp
  have hpow : b ^ (D.length + 2) = b ^ D.length * b * b := by
    rw [Nat.pow_succ, Nat.pow_succ]
  unfold signedValue
  rw [hlen, hpow, val_cons, val_append]
  simp only [val_cons, val_nil, Nat.mul_zero, Nat.add_zero,
    Int.natCast_add, Int.natCast_mul, hh, Int.mul_add, Int.mul_sub,
    Int.sub_mul, Int.mul_one, Int.one_mul]
  have hcomm : (b : Int) * (((b ^ D.length : Nat) : Int) * (b : Int)) =
      ((b ^ D.length : Nat) : Int) * (b : Int) * (b : Int) := by ac_rfl
  omega

/-- A base factor in the signed value forces one literal neutral pair,
provided the bounded symmetric source has at least two coefficients. -/
theorem exists_center_peel_of_signedValue (b : Nat) (hb : 2 ≤ b) (C : List Nat)
    (hbound : ∀ d ∈ C, d ≤ 2 * (b - 1)) (hsym : C.reverse = C)
    (hlen : 2 ≤ C.length) (z : Int)
    (hz : signedValue b C = (b : Int) * z) :
    ∃ D : List Nat,
      C = (b - 1) :: (D ++ [b - 1]) ∧ D.length + 2 = C.length ∧
      (∀ d ∈ D, d ≤ 2 * (b - 1)) ∧ D.reverse = D ∧ signedValue b D = z := by
  cases C with
  | nil => simp at hlen
  | cons d T =>
      have hd := head_neutral_of_signed_multiple b hb d T
        (hbound d List.mem_cons_self) z hz
      have hlast : T.getLast? = some d := by
        cases T with
        | nil => simp at hlen
        | cons a A =>
            have hh := congrArg (fun W : List Nat => W.getLast?) hsym
            simpa only [List.getLast?_reverse, List.head?_cons, List.getLast?_cons_cons]
              using hh.symm
      obtain ⟨D, hD⟩ := List.getLast?_eq_some_iff.mp hlast
      have hDs : D.reverse = D := by
        have hh := hsym
        rw [hD] at hh
        simpa using hh
      refine ⟨D, ?_, ?_, ?_, hDs, ?_⟩
      · rw [hD, hd]
      · simp [hD, Nat.add_assoc]
      · intro a ha
        exact hbound a (by simp [hD, ha])
      · have hp : signedValue b (d :: T) = (b : Int) * signedValue b D := by
          rw [hD, hd]
          exact signedValue_one_pair b hb D
        exact Int.eq_of_mul_eq_mul_left (by omega : (b : Int) ≠ 0) (hp.symm.trans hz)

end Agent112.NeutralNumericalArithmetic
