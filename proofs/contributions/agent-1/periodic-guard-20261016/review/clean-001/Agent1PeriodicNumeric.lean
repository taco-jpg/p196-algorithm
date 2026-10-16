import Agent1PeriodicDigits

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

/-- Every positive copy count has the same actual final carry as the
three-copy scan, whenever the input digit columns realize this word. -/
theorem periodic_actual_carry (B H w : Word) (k : Nat) (hk : 0 < k)
    (d : Nat → Nat) (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hrep : ∀ i, i < (periodicWord B H w k).length →
      DecimalDigits.columnSum d (periodicWord B H w k).length i =
        ((periodicWord B H w k)[i]?).getD 0) :
    DecimalDigits.carry
      (DecimalDigits.columnSum d (periodicWord B H w k).length)
      (periodicWord B H w k).length =
        terminalCarry (periodicWord B H w 3) 0 := by
  rw [← terminalCarry_eq_actual_carry _ d hrep]
  obtain ⟨j, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hk)
  exact scan_carry_stable B H w j hB hH hw

/-- Exact ordinary successor width for a repeated symmetric-band coefficient
word. Canonical predecessor realization is explicit; no symmetry or center
parity is inferred from the displayed band shape alone. -/
theorem periodic_actual_step_canonical_width (B H w : Word) (k : Nat) (hk : 0 < k)
    (n : Nat) (d : Nat → Nat)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hcan : DecimalDigits.Canonical n d (periodicWord B H w k).length)
    (hrep : ∀ i, i < (periodicWord B H w k).length →
      DecimalDigits.columnSum d (periodicWord B H w k).length i =
        ((periodicWord B H w k)[i]?).getD 0) :
    ∃ d', DecimalDigits.Canonical (Lychrel196.step n) d'
      (2 * B.length + 2 * (k * w.length) + H.length +
        terminalCarry (periodicWord B H w 3) 0) := by
  have hW : Bounded (periodicWord B H w k) 18 := by
    intro x hx
    simp only [periodicWord, List.mem_append] at hx
    rcases hx with (((hx | hx) | hx) | hx) | hx
    · exact hB x hx
    · exact Agent1.RepeatedBlock.bounded_pow w k 18 hw x hx
    · exact hH x hx
    · exact Agent1.RepeatedBlock.bounded_pow w.reverse k 18
        (fun y hy => hw y (List.mem_reverse.mp hy)) x hx
    · exact hB x (List.mem_reverse.mp hx)
  obtain ⟨d', hc⟩ := actual_step_canonical_width n d (periodicWord B H w k) hW hcan hrep
  have hlen : (periodicWord B H w k).length =
      2 * B.length + 2 * (k * w.length) + H.length := by
    simp only [periodicWord, List.length_append, Agent1.RepeatedBlock.pow_length,
      List.length_reverse]
    omega
  have hcarry : terminalCarry (periodicWord B H w k) 0 =
      terminalCarry (periodicWord B H w 3) 0 := by
    obtain ⟨j, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hk)
    exact scan_carry_stable B H w j hB hH hw
  exact ⟨d', by simpa only [hlen, hcarry] using hc⟩

/-- The affine repeated-band width formula is the actual decimal digit count
of the ordinary reverse-and-add successor, under the original realization. -/
theorem periodic_actual_step_decimalLength (B H w : Word) (k : Nat) (hk : 0 < k)
    (n : Nat) (d : Nat → Nat)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hcan : DecimalDigits.Canonical n d (periodicWord B H w k).length)
    (hrep : ∀ i, i < (periodicWord B H w k).length →
      DecimalDigits.columnSum d (periodicWord B H w k).length i =
        ((periodicWord B H w k)[i]?).getD 0) :
    DecimalQuantitativeMass.decimalLength (Lychrel196.step n) =
      2 * B.length + 2 * (k * w.length) + H.length +
        terminalCarry (periodicWord B H w 3) 0 := by
  obtain ⟨d', hc⟩ := periodic_actual_step_canonical_width B H w k hk n d
    hB hH hw hcan hrep
  exact DecimalQuantitativeMass.decimalLength_of_canonical _ d' _ hc

end Agent1.Periodic

#print axioms Agent1.Periodic.terminalCarry_eq_actual_carry
#print axioms Agent1.Periodic.actual_step_canonical_width
#print axioms Agent1.Periodic.actual_step_decimalLength_normalize
#print axioms Agent1.Periodic.periodic_actual_carry
#print axioms Agent1.Periodic.periodic_actual_step_canonical_width
#print axioms Agent1.Periodic.periodic_actual_step_decimalLength
