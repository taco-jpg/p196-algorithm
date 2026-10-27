import P196.Agent119NeutralLengthAccounting.StepLengths

/-!
# Exact accounting for neutral-band chains

Formalization of the length-counting argument already recorded in
`calculation/neutral_band/README.md`. The Agent120 checker remains unchanged.
All statements allow arbitrary bases, coefficient widths and legal trims.
No concrete decimal certificate or general nonexistence result is supplied.
-/

namespace Agent119.NeutralLengthAccounting

open Agent120.Neutral

/-- Exterior neutral coefficients removed along a chain. -/
def sumU : List Edge → Nat
  | [] => 0
  | e :: es => e.u + sumU es

/-- Pairs of center neutral coefficients removed along a chain. -/
def sumV : List Edge → Nat
  | [] => 0
  | e :: es => e.v + sumV es

theorem sumGain_eq (es : List Edge) : sumGain es = sumU es + sumV es := by
  induction es with
  | nil => rfl
  | cons e es ih => simp only [sumGain, sumU, sumV]; omega

/-- Additive accounting also covers empty and nonclosed checked chains. -/
theorem chain_length_balance (b : Nat) :
    ∀ (es : List Edge) (B C : List Nat), chainOK b es B C = true →
      (endB es B).length + sumU es = B.length + sumGam b es ∧
      (endC es C).length + 2 * sumV es = C.length + sumGam b es := by
  intro es
  induction es with
  | nil => intro B C hc; simp [endB, endC, sumU, sumV, sumGam]
  | cons e es ih =>
      intro B C hc
      simp only [chainOK, Bool.and_eq_true, decide_eq_true_eq] at hc
      obtain ⟨⟨⟨hB, hC⟩, he⟩, hes⟩ := hc
      obtain ⟨heB, heC⟩ := edge_lengths he
      obtain ⟨hiB, hiC⟩ := ih e.B2 e.C2 hes
      subst B
      subst C
      simp only [endB, endC, sumU, sumV, sumGam]
      constructor <;> omega

/-- Closing both interfaces forces the exact exterior, center and gain totals. -/
theorem closed_chain_totals {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) (hB : endB es B = B) (hC : endC es C = C) :
    sumU es = sumGam b es ∧ 2 * sumV es = sumGam b es ∧
      2 * sumGain es = 3 * sumGam b es := by
  obtain ⟨hlB, hlC⟩ := chain_length_balance b es B C hc
  rw [hB] at hlB
  rw [hC] at hlC
  have hg := sumGain_eq es
  omega

theorem closed_chain_gain {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) (hB : endB es B = B) (hC : endC es C = C) :
    sumGam b es ≤ sumGain es := by
  have ht := closed_chain_totals hc hB hC
  omega

theorem closed_chain_even {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) (hB : endB es B = B) (hC : endC es C = C) :
    sumGam b es % 2 = 0 := by
  have ht := closed_chain_totals hc hB hC
  omega

/-- The net band increment is exactly the total number of center-pair trims. -/
theorem closed_chain_gap {b : Nat} {es : List Edge} {B C : List Nat}
    (hc : chainOK b es B C = true) (hB : endB es B = B) (hC : endC es C = C)
    (g : Nat) : g + sumGain es - sumGam b es = g + sumV es := by
  have ht := closed_chain_totals hc hB hC
  have hg := sumGain_eq es
  omega

/-- The unchanged gain clause is redundant once a nonempty checked chain closes. -/
theorem cycleOK_iff_closed_chain (b : Nat) (es : List Edge) (B C : List Nat) :
    cycleOK b es B C = true ↔
      es ≠ [] ∧ chainOK b es B C = true ∧ endB es B = B ∧ endC es C = C := by
  constructor
  · intro h
    simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq] at h
    obtain ⟨⟨⟨⟨hne, hc⟩, hB⟩, hC⟩, _⟩ := h
    exact ⟨hne, hc, hB, hC⟩
  · rintro ⟨hne, hc, hB, hC⟩
    simp only [cycleOK, Bool.and_eq_true, decide_eq_true_eq]
    exact ⟨⟨⟨⟨hne, hc⟩, hB⟩, hC⟩, closed_chain_gain hc hB hC⟩

/-- Exact totals for a certificate accepted by the original checker. -/
theorem cycleOK_totals {b : Nat} {es : List Edge} {B C : List Nat}
    (h : cycleOK b es B C = true) :
    sumU es = sumGam b es ∧ 2 * sumV es = sumGam b es ∧
      2 * sumGain es = 3 * sumGam b es := by
  obtain ⟨_, hc, hB, hC⟩ := (cycleOK_iff_closed_chain b es B C).mp h
  exact closed_chain_totals hc hB hC

/-- Conditional Lychrel soundness needs no separate gain hypothesis. -/
theorem lychrel_of_closed_chain (b : Nat) (es : List Edge) (B C : List Nat)
    (hne : es ≠ []) (hc : chainOK b es B C = true)
    (hB : endB es B = B) (hC : endC es C = C)
    (g : Nat) (hg : 2 + sumGam b es ≤ g) :
    Lychrel b (val b (tmpl b B C g)) := by
  exact lychrel_of_cycle b es B C
    ((cycleOK_iff_closed_chain b es B C).mpr ⟨hne, hc, hB, hC⟩) g hg

end Agent119.NeutralLengthAccounting

#print axioms Agent119.NeutralLengthAccounting.sumGain_eq
#print axioms Agent119.NeutralLengthAccounting.chain_length_balance
#print axioms Agent119.NeutralLengthAccounting.closed_chain_totals
#print axioms Agent119.NeutralLengthAccounting.closed_chain_gain
#print axioms Agent119.NeutralLengthAccounting.closed_chain_even
#print axioms Agent119.NeutralLengthAccounting.closed_chain_gap
#print axioms Agent119.NeutralLengthAccounting.cycleOK_iff_closed_chain
#print axioms Agent119.NeutralLengthAccounting.cycleOK_totals
#print axioms Agent119.NeutralLengthAccounting.lychrel_of_closed_chain
