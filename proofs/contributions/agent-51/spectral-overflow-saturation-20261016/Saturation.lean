import OverflowWitness
import ResidueSums

namespace P196.Agent51

theorem witness_polynomialValue (L k : Nat) (x : Int) (hL : 2 * k ≤ L) :
    polynomialValue (DecimalDigits.columnSum (inputDigit L k) L) L x =
      polynomialValue (pairWord L k) L x := by
  exact polynomialValue_congr _ _ L x (fun i hi => witness_columnSum L k i hL hi)

theorem witness_value_one (L k : Nat) (hL : 2 * k ≤ L) :
    polynomialValue (DecimalDigits.columnSum (inputDigit L k) L) L 1 = 22 * (k : Int) := by
  rw [witness_polynomialValue L k 1 hL]
  exact pairWord_value_one L k hL

theorem witness_value_neg_one (L k : Nat) (hL : 2 * k ≤ L) :
    polynomialValue (DecimalDigits.columnSum (inputDigit L k) L) L (-1) =
      if L % 2 = 1 ∧ k % 2 = 1 then 22 else 0 := by
  rw [witness_polynomialValue L k (-1) hL]
  exact pairWord_value_neg_one L k hL

theorem witness_sourceS (L k : Nat) (hL : 2 * k ≤ L) :
    sourceS (DecimalDigits.columnSum (inputDigit L k) L) L =
      ((11 * k % 9 : Nat) : Int) := by
  rw [sourceS_congr _ (pairWord L k) L (fun i hi => witness_columnSum L k i hL hi)]
  exact pairWord_sourceS_nat L k hL

theorem witness_sourceR (L k : Nat) (hL : 2 * k ≤ L) :
    sourceR (DecimalDigits.columnSum (inputDigit L k) L) L = 0 := by
  rw [sourceR_congr _ (pairWord L k) L (fun i hi => witness_columnSum L k i hL hi)]
  exact pairWord_sourceR L k hL

/-- Every source s-class has an actual overflow palindrome predecessor at every
width at least eighteen. The input itself is nonpalindromic, and both numerical
widths are canonical. All residues use the literal actual mirrored coefficients. -/
theorem overflow_saturation (L s : Nat) (hL : 18 ≤ L) (hs : s < 9) :
    ∃ (n : Nat) (d : Nat → Nat),
      0 < n ∧ DecimalDigits.Canonical n d L ∧
      ¬ Lychrel196.Palindrome n ∧
      DecimalDigits.carry (DecimalDigits.columnSum d L) L = 1 ∧
      Lychrel196.Palindrome (Lychrel196.step n) ∧
      DecimalDigits.Canonical (Lychrel196.step n)
        (DecimalDigits.extended (DecimalDigits.columnSum d L) L) (L + 1) ∧
      sourceS (DecimalDigits.columnSum d L) L = (s : Int) ∧
      sourceR (DecimalDigits.columnSum d L) L = 0 := by
  obtain ⟨k, hk, hk9, hks⟩ := residue_parameter s hs
  have hpos : 0 < k := by omega
  have hwidth : 2 * k ≤ L := by omega
  refine ⟨witnessNumber L k, inputDigit L k,
    witness_positive L k hpos hwidth,
    witness_canonical L k hpos hwidth,
    witness_not_palindrome L k hpos hwidth,
    witness_overflow L k hpos hwidth,
    witness_step_palindrome L k hpos hwidth,
    witness_step_canonical L k hpos hwidth, ?_,
    witness_sourceR L k hwidth⟩
  rw [witness_sourceS L k hwidth, hks]

/-- The even-width threshold stated in the original overflow-saturation source. -/
theorem even_overflow_saturation (L s : Nat) (_heven : L % 2 = 0)
    (hL : 18 ≤ L) (hs : s < 9) :
    ∃ (n : Nat) (d : Nat → Nat),
      0 < n ∧ DecimalDigits.Canonical n d L ∧
      ¬ Lychrel196.Palindrome n ∧
      DecimalDigits.carry (DecimalDigits.columnSum d L) L = 1 ∧
      Lychrel196.Palindrome (Lychrel196.step n) ∧
      DecimalDigits.Canonical (Lychrel196.step n)
        (DecimalDigits.extended (DecimalDigits.columnSum d L) L) (L + 1) ∧
      sourceS (DecimalDigits.columnSum d L) L = (s : Int) ∧
      sourceR (DecimalDigits.columnSum d L) L = 0 := by
  exact overflow_saturation L s hL hs

/-- The odd-width threshold stated in the original overflow-saturation source. -/
theorem odd_overflow_saturation (L s : Nat) (_hodd : L % 2 = 1)
    (hL : 19 ≤ L) (hs : s < 9) :
    ∃ (n : Nat) (d : Nat → Nat),
      0 < n ∧ DecimalDigits.Canonical n d L ∧
      ¬ Lychrel196.Palindrome n ∧
      DecimalDigits.carry (DecimalDigits.columnSum d L) L = 1 ∧
      Lychrel196.Palindrome (Lychrel196.step n) ∧
      DecimalDigits.Canonical (Lychrel196.step n)
        (DecimalDigits.extended (DecimalDigits.columnSum d L) L) (L + 1) ∧
      sourceS (DecimalDigits.columnSum d L) L = (s : Int) ∧
      sourceR (DecimalDigits.columnSum d L) L = 0 := by
  exact overflow_saturation L s (by omega) hs

#print axioms witness_polynomialValue
#print axioms witness_value_one
#print axioms witness_value_neg_one
#print axioms witness_sourceS
#print axioms witness_sourceR
#print axioms overflow_saturation
#print axioms even_overflow_saturation
#print axioms odd_overflow_saturation

end P196.Agent51
