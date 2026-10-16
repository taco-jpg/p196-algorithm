import LychrelDigitSums

/-!
Agent #221: finite-seed arithmetic bridge.

This packages the two existing exact interfaces
  FoldedDecimal.valid_word_realizable
and
  FoldedDecimal.step_eq_word_value
into one theorem. It does not strengthen the finite-word hypotheses and
does not assert any infinite-time or 196-specific Lychrel conclusion.
-/

namespace Agent221FiniteSeedBridge

open DecimalDigits FoldedDecimal Lychrel196

/-- Every finite admissible folded word has an actual positive decimal seed
whose ordinary reverse-and-add successor is exactly the word's numeric value. -/
theorem realizable_step_value (q : Nat → Nat) (L : Nat)
    (hL : 0 < L) (houter : 0 < q 0)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i))
    (hcenter : ∀ i, i < L → i = L - 1 - i → q i % 2 = 0) :
    ∃ n d, 0 < n ∧ Canonical n d L ∧
      (∀ i, i < L → columnSum d L i = q i) ∧
      Lychrel196.step n = value q L := by
  obtain ⟨n, d, hn, hc, hrep⟩ :=
    valid_word_realizable q L hL houter hq hs hcenter
  refine ⟨n, d, hn, hc, hrep, ?_⟩
  exact step_eq_word_value n d q L hc hrep

#print axioms Agent221FiniteSeedBridge.realizable_step_value

end Agent221FiniteSeedBridge
