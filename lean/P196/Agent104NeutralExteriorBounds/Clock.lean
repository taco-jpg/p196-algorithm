import P196.Agent104NeutralExteriorBounds.Head

/-!
Exterior clock bounds for the unchanged A120 neutral checker.
The scalar potentials are imported from Agent8; the new work is the
checker-level bridge, including empty exteriors and arbitrary neutral trims.
No accepted decimal certificate or unrestricted obstruction is asserted.
-/

namespace Agent104.NeutralExteriorBounds

open Agent120.Neutral

/-- Telescoping both existing exterior potentials along any checked chain. -/
theorem chain_potential_bounds (es : List Edge) (B C : List Nat)
    (hc : chainOK 10 es B C = true) :
    2 * (sumGam 10 es : Int) ≤ (es.length : Int) +
      Agent8.upperPotential (effectiveHead B) -
      Agent8.upperPotential (effectiveHead (endB es B)) ∧
    (es.length : Int) ≤ 4 * (sumGam 10 es : Int) +
      Agent8.lowerPotential (effectiveHead B) -
      Agent8.lowerPotential (effectiveHead (endB es B)) := by
  induction es generalizing B C with
  | nil => simp [sumGam, endB]
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨hB, hC⟩, he⟩, hes⟩ := hc
      subst hB
      subst hC
      have hp := edge_potential_bounds he
      have hi := ih E.B2 E.C2 hes
      simp only [sumGam, endB, List.length_cons, Int.natCast_add, Int.natCast_one]
      omega

/-- Exterior return alone cancels the potentials; no center return is needed. -/
theorem closed_chain_bounds (es : List Edge) (B C : List Nat)
    (hc : chainOK 10 es B C = true) (hB : endB es B = B) :
    2 * sumGam 10 es ≤ es.length ∧ es.length ≤ 4 * sumGam 10 es := by
  have hp := chain_potential_bounds es B C hc
  rw [hB] at hp
  omega

/-- Every nonempty checked exterior return has strictly positive overflow. -/
theorem closed_chain_positive (es : List Edge) (B C : List Nat)
    (hc : chainOK 10 es B C = true) (hB : endB es B = B)
    (hne : es ≠ []) : 0 < sumGam 10 es := by
  have hp := closed_chain_bounds es B C hc hB
  have hlen : 0 < es.length := List.length_pos_iff.mpr hne
  omega

/-- Bounds for the original executable neutral-band cycle predicate. -/
theorem cycle_bounds (es : List Edge) (B C : List Nat)
    (h : cycleOK 10 es B C = true) :
    0 < sumGam 10 es ∧ 2 * sumGam 10 es ≤ es.length ∧
      es.length ≤ 4 * sumGam 10 es := by
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at h
  obtain ⟨⟨⟨⟨hne, hc⟩, hB⟩, _hC⟩, _hgain⟩ := h
  exact ⟨closed_chain_positive es B C hc hB hne,
    closed_chain_bounds es B C hc hB⟩

/-- The finite-period reduction used by the separately computed G<=4 audit. -/
theorem low_overflow_period (es : List Edge) (B C : List Nat)
    (h : cycleOK 10 es B C = true) (hG : sumGam 10 es ≤ 4) :
    es.length ≤ 16 := by
  have hp := cycle_bounds es B C h
  omega

/-- A zero-overflow list is rejected by the unchanged cycle checker. -/
theorem zero_overflow_rejected (es : List Edge) (B C : List Nat)
    (hG : sumGam 10 es = 0) : cycleOK 10 es B C = false := by
  cases h : cycleOK 10 es B C with
  | false => rfl
  | true =>
      have hp := cycle_bounds es B C h
      omega

end Agent104.NeutralExteriorBounds

#print axioms Agent104.NeutralExteriorBounds.chain_potential_bounds
#print axioms Agent104.NeutralExteriorBounds.closed_chain_bounds
#print axioms Agent104.NeutralExteriorBounds.closed_chain_positive
#print axioms Agent104.NeutralExteriorBounds.cycle_bounds
#print axioms Agent104.NeutralExteriorBounds.low_overflow_period
#print axioms Agent104.NeutralExteriorBounds.zero_overflow_rejected
