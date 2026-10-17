import P196.Agent5OrdinaryStreamPrefix.RawPrefixStreams

/-!
Agent #5: ordinary reverse-and-add correctness bundled with its literal
coordinate-stream exterior prefix.

The decimal-digit, positive-last-digit, and numerical-value conclusions are
exactly the original Agent #6 `reverseAddDigits_correct` conclusions. The
raw-prefix component is the imported stream interface; no value arithmetic is
reproved in this wrapper.
-/

namespace Agent5.OrdinaryStreamPrefix

open P196.Agent6 Agent115.ExteriorFactorization Agent5.ExactDigitStreams

/-- One ordinary reverse-and-add step preserves the original numerical and
canonical-digit semantics and has the stated coordinate-stream pair prefix.
The source digit and complementary-band shape hypotheses remain explicit. -/
theorem ordinary_reverse_add_from_streams
    (D B W : List Nat) (c gap : Nat)
    (hD : DecimalDigits D) (hp : PositiveLast D)
    (hc : nonneutralPhase c)
    (hB : Coefficients B) (hW : Coefficients W)
    (hshape : paired D = surrounded B c gap W) :
    DecimalDigits (reverseAddDigits D) ∧ PositiveLast (reverseAddDigits D) ∧
    numeral (reverseAddDigits D) = numeral D + numeral D.reverse ∧
    (paired (reverseAddDigits D)).take (B.length + 1) =
      List.zipWith Nat.add
        (adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int)))
        (fractionDigits (B.length + 1) (rhoNum c B)
          (9 * 10 ^ B.length *
            10 ^ (if 9 * 10 ^ B.length ≤ rhoNum c B then 1 else 0))) := by
  obtain ⟨hd, hpos, hval⟩ := reverseAddDigits_correct D hD hp
  exact ⟨hd, hpos, hval,
    ordinary_raw_prefix_from_streams D B W c gap hc hB hW hshape⟩

#print axioms ordinary_reverse_add_from_streams

end Agent5.OrdinaryStreamPrefix
