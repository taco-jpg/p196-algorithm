import Agent1RepeatedBlockContext

/-!
The actual ordinary-decimal width of one repeated-band reverse-and-add step.
The numeric input is supplied by the original canonical decimal predicate and
an explicit in-range column-sum representation. List normalization alone does
not assert canonical width or the existence of a predecessor.
-/

namespace Agent1.Periodic

open Agent8

/-- The list terminal carry is the actual carry of any digit representation
whose mirrored column sums agree with this finite coefficient word. -/
theorem terminalCarry_eq_actual_carry (W : Word) (d : Nat → Nat)
    (hrep : ∀ i, i < W.length →
      DecimalDigits.columnSum d W.length i = (W[i]?).getD 0) :
    terminalCarry W 0 =
      DecimalDigits.carry (DecimalDigits.columnSum d W.length) W.length := by
  rw [Agent1.RepeatedBlock.terminalCarry_eq_carryIn,
    IncomingCarry.carryIn_zero_eq_carry]
  exact (FoldedDecimal.carry_congr_upto _ _ W.length hrep W.length
    (Nat.le_refl _)).symm

/-- A canonical predecessor fixes the next ordinary integer's canonical
width; the only increase is the original list's computed terminal carry. -/
theorem actual_step_canonical_width (n : Nat) (d : Nat → Nat) (W : Word)
    (hW : Bounded W 18) (hcan : DecimalDigits.Canonical n d W.length)
    (hrep : ∀ i, i < W.length →
      DecimalDigits.columnSum d W.length i = (W[i]?).getD 0) :
    ∃ d', DecimalDigits.Canonical (Lychrel196.step n) d'
      (W.length + terminalCarry W 0) := by
  obtain ⟨d', hc, _⟩ := FoldedDecimal.representation_next n d
    (fun i => (W[i]?).getD 0) W.length hcan hrep
  have hcarry : DecimalDigits.carry (fun i => (W[i]?).getD 0) W.length =
      terminalCarry W 0 := by
    rw [Agent1.RepeatedBlock.terminalCarry_eq_carryIn,
      IncomingCarry.carryIn_zero_eq_carry]
  have hbit := terminalCarry_le_one W 0 hW (by decide)
  have hwidth : FoldedDecimal.nextWidth (fun i => (W[i]?).getD 0) W.length =
      W.length + terminalCarry W 0 := by
    unfold FoldedDecimal.nextWidth
    rw [hcarry]
    split <;> omega
  rw [hwidth] at hc
  exact ⟨d', hc⟩

/-- Under explicit canonical predecessor semantics, the normalized list
length equals the ordinary successor's decimal length. -/
theorem actual_step_decimalLength_normalize (n : Nat) (d : Nat → Nat) (W : Word)
    (hW : Bounded W 18) (hcan : DecimalDigits.Canonical n d W.length)
    (hrep : ∀ i, i < W.length →
      DecimalDigits.columnSum d W.length i = (W[i]?).getD 0) :
    DecimalQuantitativeMass.decimalLength (Lychrel196.step n) =
      (normalize W 0).length := by
  obtain ⟨d', hc⟩ := actual_step_canonical_width n d W hW hcan hrep
  rw [normalize_length W 0 hW (by decide)]
  exact DecimalQuantitativeMass.decimalLength_of_canonical _ d' _ hc

end Agent1.Periodic

#print axioms Agent1.Periodic.terminalCarry_eq_actual_carry
#print axioms Agent1.Periodic.actual_step_canonical_width
#print axioms Agent1.Periodic.actual_step_decimalLength_normalize
