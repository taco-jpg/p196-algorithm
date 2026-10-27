import P196.Agent119NeutralCenterNumericChain.Trim

/-!
# Weighted signed-center accounting along accepted chains and cycles

The accepted trim law telescopes after weighting later increments by the
preceding total center trim. Center closure gives an exact integer identity
and divisibility condition. Empty chains and zero total trim remain covered;
no division or positivity assumption is used. The increments retain the
actual source words and their fixed-width digit reversal, so these results
are necessary arithmetic consequences, not a driver-only criterion or a
converse construction of coefficient cycles.
-/

namespace Agent119.NeutralCenterNumericChain

open Agent120.Neutral Agent112.NeutralNumericalArithmetic

/-- Total actual center trim, expressed with the standard list sum. -/
def trimTotal (es : List Edge) : Nat := (es.map Edge.v).sum

/-- Each subsequent raw increment is weighted by all preceding center trims. -/
def weightedIncrement (b : Nat) : List Edge → Int
  | [] => 0
  | E :: es => increment b E.B E.C + scale b E.v * weightedIncrement b es

theorem trimTotal_append (es fs : List Edge) :
    trimTotal (es ++ fs) = trimTotal es + trimTotal fs := by
  induction es with
  | nil => simp [trimTotal]
  | cons E es ih =>
      change E.v + trimTotal (es ++ fs) = (E.v + trimTotal es) + trimTotal fs
      rw [ih, Nat.add_assoc]

/-- Concatenating arithmetic traces shifts the second trace by the first trim total. -/
theorem weightedIncrement_append (b : Nat) (es fs : List Edge) :
    weightedIncrement b (es ++ fs) = weightedIncrement b es +
      scale b (trimTotal es) * weightedIncrement b fs := by
  induction es with
  | nil => simp [weightedIncrement, trimTotal, scale_zero]
  | cons E es ih =>
      change increment b E.B E.C + scale b E.v * weightedIncrement b (es ++ fs) =
        (increment b E.B E.C + scale b E.v * weightedIncrement b es) +
          scale b (E.v + trimTotal es) * weightedIncrement b fs
      rw [ih, scale_add, Int.mul_add, Int.mul_assoc, Int.add_assoc]

/-- The exact scaled signed update for an arbitrary accepted open chain. -/
theorem chain_signed_identity {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) :
    scale b (trimTotal es) * signedValue b (endC es C) =
      signedValue b C + weightedIncrement b es := by
  induction es generalizing B C with
  | nil => simp [trimTotal, scale_zero, endC, weightedIncrement]
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨_, hC⟩, he⟩, hr⟩ := hc
      subst C
      have ht := ih hr
      have hs := edge_signed_update he
      change scale b (E.v + trimTotal es) * signedValue b (endC es E.C2) =
        signedValue b E.C +
          (increment b E.B E.C + scale b E.v * weightedIncrement b es)
      rw [scale_add, Int.mul_assoc, ht, Int.mul_add, hs, Int.add_assoc]

/-- Only center closure is needed to cancel the endpoint signed value. -/
theorem closed_chain_signed_identity {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) (hC : endC es C = C) :
    (scale b (trimTotal es) - 1) * signedValue b C = weightedIncrement b es := by
  have h := chain_signed_identity hc
  rw [hC] at h
  rw [Int.sub_mul, Int.one_mul]
  omega

/-- The closed weighted increment is divisible by the actual trim multiplier minus one. -/
theorem closed_chain_divides {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) (hC : endC es C = C) :
    (scale b (trimTotal es) - 1) ∣ weightedIncrement b es :=
  ⟨signedValue b C, (closed_chain_signed_identity hc hC).symm⟩

/-- Zero total trim forces zero weighted increment, without dividing by zero. -/
theorem closed_chain_zero_trim {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) (hC : endC es C = C)
    (hv : trimTotal es = 0) : weightedIncrement b es = 0 := by
  have h := closed_chain_signed_identity hc hC
  simpa only [hv, scale_zero, Int.sub_self, Int.zero_mul] using h.symm

/-- Every certificate accepted by the original checker satisfies the weighted identity. -/
theorem cycle_signed_identity {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) :
    (scale b (trimTotal es) - 1) * signedValue b C = weightedIncrement b es := by
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hc
  exact closed_chain_signed_identity hc.1.1.1.2 hc.1.2

theorem cycle_divides {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : cycleOK b es B C = true) :
    (scale b (trimTotal es) - 1) ∣ weightedIncrement b es :=
  ⟨signedValue b C, (cycle_signed_identity hc).symm⟩

/-- Failure of this necessary integer divisibility test rejects the original checker. -/
theorem cycleOK_false_of_not_divides {b : Nat} {es : List Edge} {B C : List Nat}
    (hn : ¬ (scale b (trimTotal es) - 1) ∣ weightedIncrement b es) :
    cycleOK b es B C = false := by
  cases h : cycleOK b es B C with
  | false => rfl
  | true => exact False.elim (hn (cycle_divides h))

end Agent119.NeutralCenterNumericChain

#print axioms Agent119.NeutralCenterNumericChain.trimTotal_append
#print axioms Agent119.NeutralCenterNumericChain.weightedIncrement_append
#print axioms Agent119.NeutralCenterNumericChain.chain_signed_identity
#print axioms Agent119.NeutralCenterNumericChain.closed_chain_signed_identity
#print axioms Agent119.NeutralCenterNumericChain.closed_chain_divides
#print axioms Agent119.NeutralCenterNumericChain.closed_chain_zero_trim
#print axioms Agent119.NeutralCenterNumericChain.cycle_signed_identity
#print axioms Agent119.NeutralCenterNumericChain.cycle_divides
#print axioms Agent119.NeutralCenterNumericChain.cycleOK_false_of_not_divides
