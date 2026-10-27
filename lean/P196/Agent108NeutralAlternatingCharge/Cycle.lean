import P196.Agent108NeutralAlternatingCharge.Step

/-!
# Alternating charge along checked neutral-band cycles

The edge recurrence resets the residue modulo 11 at an overflow, and a zero
residue persists along subsequent checked edges.  A closed checked chain with
positive total overflow therefore has zero charge at every interface.  This
excludes empty and entirely neutral exterior interfaces within that scope.

These are necessary conditions on the existing decimal certificate format.
They neither construct a decimal certificate nor exclude arbitrary nonneutral
exterior cycles.  Positive total overflow remains an explicit hypothesis.
-/

namespace Agent108.NeutralCharge

open Agent120.Neutral

/-- A checked edge preserves charge zero, whether or not it overflows. -/
theorem edge_preserves_zero {E : Edge} (he : edgeOK 10 E = true)
    (hz : charge E.B % 11 = 0) : charge E.B2 % 11 = 0 := by
  rw [edge_charge_step he]
  split <;> omega

/-- Zero charge propagates to the endpoint of any checked chain. -/
theorem chain_preserves_zero {es : List Edge} {B C : List Nat}
    (hc : chainOK 10 es B C = true) (hz : charge B % 11 = 0) :
    charge (endB es B) % 11 = 0 := by
  induction es generalizing B C with
  | nil => simpa only [endB] using hz
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨hB, _hC⟩, he⟩, hrest⟩ := hc
      have hsource : charge E.B % 11 = 0 := by simpa only [hB] using hz
      have htarget := edge_preserves_zero he hsource
      simpa only [endB] using ih hrest htarget

/-- Every checked edge of a chain starting at zero has zero source and target. -/
theorem chain_each_edge_charge_zero {es : List Edge} {B C : List Nat}
    (hc : chainOK 10 es B C = true) (hz : charge B % 11 = 0) :
    ∀ E ∈ es, charge E.B % 11 = 0 ∧ charge E.B2 % 11 = 0 := by
  induction es generalizing B C with
  | nil =>
      intro E hE
      simp at hE
  | cons head es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨hB, _hC⟩, he⟩, hrest⟩ := hc
      have hsource : charge head.B % 11 = 0 := by simpa only [hB] using hz
      have htarget := edge_preserves_zero he hsource
      intro E hE
      rcases List.mem_cons.mp hE with hhead | htail
      · subst E
        exact ⟨hsource, htarget⟩
      · exact ih hrest htarget E htail

/-- One or more overflows reset the endpoint charge of a checked chain. -/
theorem chain_zero_of_positive_overflow {es : List Edge} {B C : List Nat}
    (hc : chainOK 10 es B C = true) (hpos : 0 < sumGam 10 es) :
    charge (endB es B) % 11 = 0 := by
  induction es generalizing B C with
  | nil => simp only [sumGam, Nat.lt_irrefl] at hpos
  | cons E es ih =>
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨_hB, _hC⟩, he⟩, hrest⟩ := hc
      by_cases hzero : gam 10 E.B E.C = 0
      · have htail : 0 < sumGam 10 es := by
          simpa only [sumGam, hzero, Nat.zero_add] using hpos
        simpa only [endB] using ih hrest htail
      · have htarget : charge E.B2 % 11 = 0 := by
          simpa only [hzero, if_false, Int.zero_emod] using edge_charge_step he
        simpa only [endB] using chain_preserves_zero hrest htarget

/-- A checked decimal cycle with positive total overflow starts at charge zero. -/
theorem cycle_charge_zero {es : List Edge} {B C : List Nat}
    (hcert : cycleOK 10 es B C = true) (hpos : 0 < sumGam 10 es) :
    charge B % 11 = 0 := by
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hcert
  obtain ⟨⟨⟨⟨_hne, hchain⟩, hB⟩, _hC⟩, _hgain⟩ := hcert
  have hz := chain_zero_of_positive_overflow hchain hpos
  simpa only [hB] using hz

/-- The same charge condition holds at every edge source and target. -/
theorem cycle_each_edge_charge_zero {es : List Edge} {B C : List Nat}
    (hcert : cycleOK 10 es B C = true) (hpos : 0 < sumGam 10 es) :
    ∀ E ∈ es, charge E.B % 11 = 0 ∧ charge E.B2 % 11 = 0 := by
  have hz := cycle_charge_zero hcert hpos
  simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at hcert
  obtain ⟨⟨⟨⟨_hne, hchain⟩, _hB⟩, _hC⟩, _hgain⟩ := hcert
  exact chain_each_edge_charge_zero hchain hz

/-- Empty exterior words have nonzero charge modulo 11. -/
theorem charge_zero_ne_nil {B : List Nat} (hz : charge B % 11 = 0) : B ≠ [] := by
  exact charge_zero_implies_nonempty B hz

/-- Entirely neutral exterior words likewise have nonzero charge modulo 11. -/
theorem charge_zero_ne_replicate {B : List Nat} (hz : charge B % 11 = 0)
    (n : Nat) : B ≠ List.replicate n 9 := by
  intro hB
  rw [hB, charge_replicate] at hz
  omega

/-- Positive-overflow certificates cannot start with an empty exterior. -/
theorem cycle_exterior_ne_nil {es : List Edge} {B C : List Nat}
    (hcert : cycleOK 10 es B C = true) (hpos : 0 < sumGam 10 es) : B ≠ [] := by
  exact charge_zero_ne_nil (cycle_charge_zero hcert hpos)

/-- Positive-overflow certificates cannot start with an entirely neutral exterior. -/
theorem cycle_exterior_ne_replicate {es : List Edge} {B C : List Nat}
    (hcert : cycleOK 10 es B C = true) (hpos : 0 < sumGam 10 es)
    (n : Nat) : B ≠ List.replicate n 9 := by
  exact charge_zero_ne_replicate (cycle_charge_zero hcert hpos) n

end Agent108.NeutralCharge

#print axioms Agent108.NeutralCharge.cycle_charge_zero
#print axioms Agent108.NeutralCharge.cycle_each_edge_charge_zero
#print axioms Agent108.NeutralCharge.cycle_exterior_ne_nil
#print axioms Agent108.NeutralCharge.cycle_exterior_ne_replicate
