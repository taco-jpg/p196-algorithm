import P196.PhaseEighteenIsolation.Quotients

/-!
# Literal fractional prefixes from positional values

The first output of the original long-division function may exceed nine.
Every later output is an ordinary decimal digit, so the fixed-length
positional value still determines the entire output list. Combining this
fact with the existing positive-prefix quotient identity shows that a
sufficiently small appended numerator tail preserves the literal prefix.
-/

namespace Agent5.FiniteObservationIsolation

open Agent115.ExteriorFactorization Agent5.ExactDigitStreams
open Agent5.PhaseEighteenIsolation

/-- At a common cutoff, the positional value determines the literal
long-division output even when either initial fraction is improper. -/
theorem fractionDigits_eq_of_highValue_eq
    (cut r s D E : Nat)
    (hD : 0 < D) (hE : 0 < E)
    (hvalue : highValue (fractionDigits cut r D) =
      highValue (fractionDigits cut s E)) :
    fractionDigits cut r D = fractionDigits cut s E := by
  induction cut generalizing r s with
  | zero => rfl
  | succ cut ih =>
      have hr : highValue (fractionDigits cut ((10 * r) % D) D) <
          10 ^ cut := by
        have h := highValue_lt_pow _
          (fractionDigits_digits_lt_ten cut ((10 * r) % D) D
            (Nat.mod_lt _ hD))
        simpa only [fractionDigits_length] using h
      have hs : highValue (fractionDigits cut ((10 * s) % E) E) <
          10 ^ cut := by
        have h := highValue_lt_pow _
          (fractionDigits_digits_lt_ten cut ((10 * s) % E) E
            (Nat.mod_lt _ hE))
        simpa only [fractionDigits_length] using h
      have hp : 0 < 10 ^ cut := Nat.pow_pos (by decide)
      simp only [fractionDigits, highValue_cons_digit,
        fractionDigits_length] at hvalue
      have hhead := congrArg (fun v : Nat => v / 10 ^ cut) hvalue
      change (((10 * r) / D) * 10 ^ cut +
          highValue (fractionDigits cut ((10 * r) % D) D)) / 10 ^ cut =
        (((10 * s) / E) * 10 ^ cut +
          highValue (fractionDigits cut ((10 * s) % E) E)) / 10 ^ cut at hhead
      rw [Nat.add_comm, Nat.add_mul_div_right _ _ hp,
        Nat.div_eq_of_lt hr, Nat.zero_add,
        Nat.add_comm, Nat.add_mul_div_right _ _ hp,
        Nat.div_eq_of_lt hs, Nat.zero_add] at hhead
      have htail : highValue (fractionDigits cut ((10 * r) % D) D) =
          highValue (fractionDigits cut ((10 * s) % E) E) := by
        rw [hhead] at hvalue
        omega
      simp only [fractionDigits]
      rw [hhead]
      exact congrArg (List.cons ((10 * s) / E)) (ih _ _ htail)

/-- A numerator tail smaller than one observed place after scaling cannot
change any output in the requested literal long-division prefix. -/
theorem fractionDigits_add_small_tail
    (cut r D scale tail : Nat)
    (hD : 0 < D) (hscale : 0 < scale)
    (htail : 10 ^ cut * tail < scale) :
    fractionDigits cut (scale * r + tail) (scale * D) =
      fractionDigits cut r D := by
  cases cut with
  | zero => rfl
  | succ cut =>
      apply fractionDigits_eq_of_highValue_eq (cut + 1)
        (scale * r + tail) r (scale * D) D (Nat.mul_pos hscale hD) hD
      rw [fractionDigits_value cut _ _ (Nat.mul_pos hscale hD),
        fractionDigits_value cut _ _ hD]
      have hnum : 10 ^ (cut + 1) * (scale * r + tail) =
          scale * (10 ^ (cut + 1) * r) + 10 ^ (cut + 1) * tail := by
        rw [Nat.mul_add]
        ac_rfl
      rw [hnum, ← Nat.div_div_eq_div_mul, Nat.mul_add_div hscale,
        Nat.div_eq_of_lt htail, Nat.add_zero]

#print axioms fractionDigits_eq_of_highValue_eq
#print axioms fractionDigits_add_small_tail

end Agent5.FiniteObservationIsolation
