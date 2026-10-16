import ActualOverflowBirths
import OverflowEndpoints

/-!
Canonical one-step reverse-add specialization of the complete all-base
overflow birth classification. The digit representation, normalization,
computed carries and numerical value map are the unchanged original APIs.
No orbit persistence or all-time conclusion is asserted.
-/

namespace P196.Agent7.AllBaseOverflow

open ResetNormalization PhysicalWidth ReverseAdd ActualBaseBirths

/-- The full overflowing ordinary reverse-add update, including every interior
birth case and both genuine output endpoints. Width one is retained: its
interior quantifier is empty, while its canonical output and endpoints remain
covered. The endpoint maximum criterion includes the exact binary exception. -/
theorem canonical_reverse_add_overflow_theorem
    (b : Int) (digits : List Int) (xs : List (Int × Bool))
    (hb : 2 ≤ b) (hd : DigitBounds b digits) (hp : PositiveLast digits)
    (hqs : xs.map Prod.fst = pairs digits)
    (ho : terminal b 0 (ordinaryTags xs) = 1) :
    let output := actualDigits b xs
    let Q := pairs output
    let q0 := (xs.getD 0 (0, false)).1
    (∀ d ∈ output, 0 ≤ d ∧ d < b) ∧
    PositiveLast output ∧
    output.length = digits.length + 1 ∧
    SignedDigitUniqueness.eval b output =
      SignedDigitUniqueness.eval b digits + reversedValue b digits ∧
    (Q.getD 0 0 = 1 + q0 % b ∧ Q.getD xs.length 0 = 1 + q0 % b) ∧
    (0 < Q.getD 0 0 ∧ 0 < Q.getD xs.length 0) ∧
    ((Q.getD 0 0 = 2 * b - 2 ↔ b = 2 ∧ q0 = 1) ∧
      (Q.getD xs.length 0 = 2 * b - 2 ↔ b = 2 ∧ q0 = 1)) ∧
    (∀ (i : Nat) (hi0 : 0 < i) (hi : i < xs.length),
      let a := (xs[i - 1]'(by omega)).1
      let z := xs[i].1
      let u := incoming b xs i
      let v := incoming b xs (xs.length - i)
      (Q.getD i 0 = 0 ↔
        (a = 0 ∧ z = 0) ∨
        (a = b - 1 ∧ z = b - 1 ∧ u = 1 ∧ v = 1) ∨
        (a = b - 1 ∧ z = b ∧ u = 0) ∨
        (a = b ∧ z = b - 1 ∧ v = 0)) ∧
      (Q.getD i 0 = 2 * b - 2 ↔
        (a = 2 * b - 2 ∧ z = 2 * b - 2) ∨
        (a = b - 1 ∧ z = b - 1 ∧ u = 0 ∧ v = 0) ∨
        (a = b - 1 ∧ z = b - 2 ∧ u = 1) ∨
        (a = b - 2 ∧ z = b - 1 ∧ v = 1)) ∧
      (((Q.getD i 0 = 0 ∧ ¬ (a = 0 ∧ z = 0)) ∨
        (Q.getD i 0 = 2 * b - 2 ∧
          ¬ (a = 2 * b - 2 ∧ z = 2 * b - 2))) →
        a = b - 1 ∨ z = b - 1)) := by
  dsimp only
  have hbound := tagged_pairs_bound b digits xs hd hqs
  have hs : (xs.map Prod.fst).reverse = xs.map Prod.fst := by
    rw [hqs]
    exact pairs_symmetric digits
  obtain ⟨hout, hpos, hlen, hvalue⟩ :=
    reverse_add_normalization b digits xs hb hd hp hqs
  have hwidth : (actualDigits b xs).length = digits.length + 1 := by
    simpa [ho] using hlen
  refine ⟨hout, hpos, hwidth, hvalue,
    actual_overflow_endpoints b xs ho,
    actual_overflow_endpoints_pos b xs hb ho,
    actual_overflow_endpoints_max_iff b xs hb hbound ho, ?_⟩
  intro i hi0 hi
  refine ⟨actual_overflow_zero_iff b xs i hb hbound ho hi0 hi hs,
    actual_overflow_max_iff b xs i hb hbound ho hi0 hi hs, ?_⟩
  intro hnew
  exact actual_overflow_new_extreme_neutral b xs i hb hbound ho hi0 hi hs hnew

#print axioms canonical_reverse_add_overflow_theorem

end P196.Agent7.AllBaseOverflow
