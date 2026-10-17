import P196.Agent51ReciprocalMoment.ResidueSums

/-!
# Reciprocal coefficient moments and derivative residue redundancy

Source: astra_spectral_carry_quotient.md, lines 103-118, Git blob
 eac5b8f61385a615d9cc3e7796a4d698c66b716b. The original identity is
2 Q'(1) = (L-1) Q(1). This module proves its exact finite coefficient
meaning, including signed coefficients and the empty-width extension.

The reflection helper generalizes the natural-valued finite-sum argument
of DecimalMass.wordSum_reflected in the original LychrelDigitSums source.
It is a supporting generalization, not a claim of mathematical discovery.
The imported ResidueSums and its polynomialValue definition are unchanged.
-/

namespace P196.Agent51

/-- Additivity of the existing integer finite-sum helper. -/
theorem finiteSum_add_values (f g : Nat → Int) (L : Nat) :
    finiteSum (fun i => f i + g i) L = finiteSum f L + finiteSum g L := by
  induction L with
  | zero => rfl
  | succ L ih => simp only [finiteSum, ih]; omega

/-- Splitting off the first term, without any coefficient restriction. -/
theorem finiteSum_shift (f : Nat → Int) (L : Nat) :
    finiteSum f (L + 1) = f 0 + finiteSum (fun i => f (i + 1)) L := by
  induction L with
  | zero => simp [finiteSum]
  | succ L ih => simp only [finiteSum] at ih ⊢; omega

/-- Integer version of DecimalMass.wordSum_reflected, with the same finite reversal. -/
theorem finiteSum_reflected (f : Nat → Int) (L : Nat) :
    finiteSum (fun i => f (L - 1 - i)) L = finiteSum f L := by
  induction L generalizing f with
  | zero => rfl
  | succ L ih =>
    have href : finiteSum (fun i => f (L + 1 - 1 - i)) L =
        finiteSum (fun i => f (L - 1 - i + 1)) L := by
      apply finiteSum_congr
      intro i hi
      congr 1
      omega
    rw [finiteSum, href, ih (fun i => f (i + 1)), finiteSum_shift]
    simp
    omega

/-- The exact reciprocal first-moment identity for arbitrary signed coefficients. -/
theorem reciprocal_first_moment (q : Nat → Int) (L : Nat)
    (hsymm : ∀ i < L, q i = q (L - 1 - i)) :
    2 * finiteSum (fun i => (i : Int) * q i) L =
      ((L : Int) - 1) * finiteSum q L := by
  let m := finiteSum (fun i => (i : Int) * q i) L
  have href : finiteSum (fun i => ((L - 1 - i : Nat) : Int) * q i) L = m := by
    calc
      _ = finiteSum (fun i => ((L - 1 - i : Nat) : Int) * q (L - 1 - i)) L := by
        apply finiteSum_congr
        intro i hi
        rw [hsymm i hi]
      _ = m := finiteSum_reflected (fun i => (i : Int) * q i) L
  calc
    _ = finiteSum (fun i => (i : Int) * q i) L +
        finiteSum (fun i => ((L - 1 - i : Nat) : Int) * q i) L := by
      change 2 * m = m + _
      rw [href]
      omega
    _ = finiteSum (fun i => (i : Int) * q i +
        ((L - 1 - i : Nat) : Int) * q i) L :=
      (finiteSum_add_values _ _ L).symm
    _ = finiteSum (fun i => ((L : Int) - 1) * q i) L := by
      apply finiteSum_congr
      intro i hi
      rw [← Int.add_mul]
      have hindex : (i : Int) + ((L - 1 - i : Nat) : Int) = (L : Int) - 1 := by omega
      rw [hindex]
    _ = _ := finiteSum_mul_left _ _ _

/-- The same source identity in literal finite List.range sums. -/
theorem reciprocal_first_moment_literal (q : Nat → Int) (L : Nat)
    (hsymm : ∀ i < L, q i = q (L - 1 - i)) :
    2 * ((List.range L).map (fun (i : Nat) => (i : Int) * q i)).sum =
      ((L : Int) - 1) * ((List.range L).map q).sum := by
  simpa only [finiteSum_eq_range] using reciprocal_first_moment q L hsymm

/-- Literal coefficient formula for formal polynomial differentiation evaluated at x.
The index-zero summand vanishes because its multiplier is zero. -/
def formalDerivativeValue (q : Nat → Int) (L : Nat) (x : Int) : Int :=
  ((List.range L).map (fun (i : Nat) => (i : Int) * q i * x ^ (i - 1))).sum

/-- The literal weighted coefficient sum representing the formal derivative at one. -/
def derivativeAtOne (q : Nat → Int) (L : Nat) : Int :=
  ((List.range L).map (fun (i : Nat) => (i : Int) * q i)).sum

theorem derivativeAtOne_eq_finiteSum (q : Nat → Int) (L : Nat) :
    derivativeAtOne q L = finiteSum (fun i => (i : Int) * q i) L := by
  exact (finiteSum_eq_range _ _).symm

/-- Evaluation of the literal formal derivative at one agrees with its first moment. -/
theorem formalDerivativeValue_one (q : Nat → Int) (L : Nat) :
    formalDerivativeValue q L 1 = derivativeAtOne q L := by
  unfold formalDerivativeValue derivativeAtOne
  simp only [int_one_pow, Int.mul_one]

/-- The source equation 2 Q'(1) = (L-1) Q(1), using coefficientwise differentiation. -/
theorem reciprocal_derivative_at_one (q : Nat → Int) (L : Nat)
    (hsymm : ∀ i < L, q i = q (L - 1 - i)) :
    2 * formalDerivativeValue q L 1 = ((L : Int) - 1) * finiteSum q L := by
  rw [formalDerivativeValue_one, derivativeAtOne_eq_finiteSum]
  exact reciprocal_first_moment q L hsymm

/-- The derivative residue is determined by width and mass, since 2*5 = 1 modulo 9. -/
theorem reciprocal_derivative_mod_nine (q : Nat → Int) (L : Nat)
    (hsymm : ∀ i < L, q i = q (L - 1 - i)) :
    derivativeAtOne q L % 9 =
      (5 * (((L : Int) - 1) * finiteSum q L)) % 9 := by
  have h := reciprocal_first_moment q L hsymm
  rw [derivativeAtOne_eq_finiteSum]
  omega

/-- Two separately symmetric words of the same width and mass residue
have the same derivative residue; exact equality of masses is not required. -/
theorem reciprocal_derivative_mod_nine_determined (q r : Nat → Int) (L : Nat)
    (hq : ∀ i < L, q i = q (L - 1 - i))
    (hr : ∀ i < L, r i = r (L - 1 - i))
    (hmass : finiteSum q L % 9 = finiteSum r L % 9) :
    derivativeAtOne q L % 9 = derivativeAtOne r L % 9 := by
  rw [reciprocal_derivative_mod_nine q L hq,
    reciprocal_derivative_mod_nine r L hr]
  have hproduct : (((L : Int) - 1) * finiteSum q L) % 9 =
      (((L : Int) - 1) * finiteSum r L) % 9 := by
    rw [Int.mul_emod ((L : Int) - 1) (finiteSum q L) 9,
      Int.mul_emod ((L : Int) - 1) (finiteSum r L) 9, hmass]
  rw [Int.mul_emod 5 (((L : Int) - 1) * finiteSum q L) 9,
    Int.mul_emod 5 (((L : Int) - 1) * finiteSum r L) 9, hproduct]

/-- Natural coefficient mass agrees with the unchanged literal polynomialValue at one. -/
theorem natural_mass_eq_polynomialValue (q : Nat → Nat) (L : Nat) :
    finiteSum (fun i => (q i : Int)) L = polynomialValue q L 1 := by
  rw [polynomialValue_eq_finiteSum]
  apply finiteSum_congr
  intro i _
  simp only [int_one_pow, Int.mul_one]

/-- Natural-coefficient specialization linked to the original polynomialValue definition. -/
theorem natural_reciprocal_derivative (q : Nat → Nat) (L : Nat)
    (hsymm : ∀ i < L, q i = q (L - 1 - i)) :
    2 * formalDerivativeValue (fun i => (q i : Int)) L 1 =
      ((L : Int) - 1) * polynomialValue q L 1 := by
  have hs : ∀ i < L, (q i : Int) = (q (L - 1 - i) : Int) := by
    intro i hi
    rw [hsymm i hi]
  rw [← natural_mass_eq_polynomialValue]
  exact reciprocal_derivative_at_one _ L hs

#print axioms finiteSum_add_values
#print axioms finiteSum_shift
#print axioms finiteSum_reflected
#print axioms reciprocal_first_moment
#print axioms reciprocal_first_moment_literal
#print axioms formalDerivativeValue
#print axioms derivativeAtOne
#print axioms derivativeAtOne_eq_finiteSum
#print axioms formalDerivativeValue_one
#print axioms reciprocal_derivative_at_one
#print axioms reciprocal_derivative_mod_nine
#print axioms reciprocal_derivative_mod_nine_determined
#print axioms natural_mass_eq_polynomialValue
#print axioms natural_reciprocal_derivative

end P196.Agent51
