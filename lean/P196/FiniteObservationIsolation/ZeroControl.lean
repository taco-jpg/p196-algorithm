import P196.PhaseEighteenIsolation.Isolation

/-!
# The first high observation identifies the empty zero-phase state

For an original valid exterior, a zero first high output forces both an
empty word and phase zero. The statement allows every natural phase. The
coefficient bound comes from validity, while its positive-head condition
excludes a nonempty word with a zero first high output.
-/

namespace Agent5.FiniteObservationIsolation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.FiniteExteriorHistories

/-- Among original valid states at arbitrary natural phases, the first
literal high output is zero exactly at the empty zero-phase state. -/
theorem first_high_zero_iff (c : Nat) (B : List Nat)
    (hv : validOuter { c := c, B := B } = true) :
    fractionDigits 1 (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2) = [0] ↔
      c = 0 ∧ B = [] := by
  constructor
  · intro hzero
    let k : Nat := if 10 ≤ c then 1 else 0
    let gamma := (normalize B.reverse k).2
    have hk : k ≤ 1 := by
      dsimp only [k]
      split <;> decide
    have hck : 9 * k ≤ c := by
      dsimp only [k]
      split <;> omega
    have hB := entries_le_of_valid c B hv
    have hgamma : gamma ≤ 1 :=
      normalize_carry_le B.reverse k
        (fun x hx => hB x (List.mem_reverse.mp hx)) hk
    have hvalue :
        lowValue (normalize B.reverse k).1 + 10 ^ B.length * gamma =
          highValue B + k := by
      simpa only [List.length_reverse, lowValue_reverse] using
        normalize_value_conservation B.reverse k
    have hquot :
        10 * rhoNum c B / (9 * 10 ^ B.length * 10 ^ gamma) = 0 := by
      simpa only [fractionDigits, List.cons.injEq, and_true] using hzero
    have hD : 0 < 9 * 10 ^ B.length * 10 ^ gamma :=
      Nat.mul_pos (Nat.mul_pos (by decide) (Nat.pow_pos (by decide)))
        (Nat.pow_pos (by decide))
    have hsmall := Nat.lt_of_div_eq_zero hD hquot
    have hgamma0 : gamma = 0 := by
      by_cases hg : gamma = 0
      · exact hg
      · have hgamma1 : gamma = 1 := by omega
        rw [hgamma1, Nat.mul_one] at hvalue
        rw [hgamma1, Nat.pow_one] at hsmall
        unfold rhoNum at hsmall
        omega
    rw [hgamma0, Nat.pow_zero, Nat.mul_one] at hsmall
    cases B with
    | nil =>
        refine ⟨?_, rfl⟩
        simp only [rhoNum, highValue, List.foldl_nil, List.length_nil,
          Nat.pow_zero, Nat.mul_zero, Nat.zero_add, Nat.mul_one] at hsmall
        omega
    | cons b bs =>
        exfalso
        have hb : 0 < b := by
          simp only [validOuter, Bool.and_eq_true, decide_eq_true_eq] at hv
          exact hv.1.2
        have hhead : 10 ^ bs.length ≤ highValue (b :: bs) := by
          rw [highValue_cons]
          have hmul := Nat.mul_le_mul_right (10 ^ bs.length)
            (show 1 ≤ b by omega)
          simp only [Nat.one_mul] at hmul
          omega
        simp only [rhoNum, List.length_cons, Nat.pow_succ] at hsmall
        omega
  · rintro ⟨rfl, rfl⟩
    rfl

/-- A single original observation isolates the empty zero-phase state
among all original valid states, with no bound on the competing phase. -/
theorem zero_empty_state_isolated (d : Nat) (A : List Nat)
    (hvA : validOuter { c := d, B := A } = true)
    (hobs : sameObservation 1
      { c := 0, B := [] } { c := d, B := A }) :
    d = 0 ∧ A = [] := by
  apply (first_high_zero_iff d A hvA).mp
  exact hobs.2.2

#print axioms first_high_zero_iff
#print axioms zero_empty_state_isolated

end Agent5.FiniteObservationIsolation
