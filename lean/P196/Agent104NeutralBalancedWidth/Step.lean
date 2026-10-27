import P196.Agent119NeutralCenterPadding.Main
import P196.Agent119NeutralLengthAccounting.StepLengths

/-!
# Neutral centers within two adjacent widths

Pad each center to the largest width at most W with its original parity.
The local checked edge then has a binary center trim, forced by overflow and
the padded source width. All transition lengths and padding covariance are
imported from Agent119; the original Agent120 checker is unchanged.
-/

namespace Agent104.NeutralBalancedWidth

open Agent120.Neutral

/-- The number of neutral pairs that fit below the common width ceiling. -/
def reserve (W : Nat) (C : List Nat) : Nat := (W - C.length) / 2

/-- Pad to the largest width at most W having the original center parity. -/
def balanceCenter (b W : Nat) (C : List Nat) : List Nat :=
  Agent119.NeutralCenterPadding.padC b (reserve W C) C

/-- The transported trim. Valid edges below W satisfy the additive balance,
so this natural subtraction does not discard a negative difference. -/
def balanceTrim (W : Nat) (E : Edge) : Nat :=
  E.v + reserve W E.C - reserve W E.C2

/-- Pad both centers, preserving both exterior interfaces and the exterior trim. -/
def balanceEdge (b W : Nat) (E : Edge) : Edge :=
  { E with C := balanceCenter b W E.C,
           C2 := balanceCenter b W E.C2,
           v := balanceTrim W E }

theorem balanceCenter_length (b W : Nat) (C : List Nat) (hC : C.length ≤ W) :
    (balanceCenter b W C).length = W - (W - C.length) % 2 := by
  simp only [balanceCenter, Agent119.NeutralCenterPadding.padC_length, reserve]
  omega

theorem balanceCenter_length_bounds (b W : Nat) (C : List Nat)
    (hC : C.length ≤ W) :
    (balanceCenter b W C).length ≤ W ∧ W ≤ (balanceCenter b W C).length + 1 := by
  have h := balanceCenter_length b W C hC
  omega

/-- No center exceeds the original width ceiling. -/
theorem balanceCenter_lengths (b W : Nat) (C : List Nat) (hC : C.length ≤ W) :
    (balanceCenter b W C).length = W - 1 ∨ (balanceCenter b W C).length = W := by
  have h := balanceCenter_length_bounds b W C hC
  omega

/-- Imported edge accounting makes the new trim an exact nonnegative transfer. -/
theorem balanceTrim_balance {b W : Nat} {E : Edge} (he : edgeOK b E = true)
    (hC : E.C.length ≤ W) (hC2 : E.C2.length ≤ W) :
    reserve W E.C + E.v = balanceTrim W E + reserve W E.C2 := by
  have hlen := (Agent119.NeutralLengthAccounting.edge_lengths he).2
  have hs := balanceCenter_length_bounds b W E.C hC
  have ht := balanceCenter_length_bounds b W E.C2 hC2
  simp only [balanceCenter, Agent119.NeutralCenterPadding.padC_length] at hs ht
  have hn : reserve W E.C2 ≤ E.v + reserve W E.C := by omega
  unfold balanceTrim
  omega

/-- The balanced edge is accepted by the unchanged original checker. -/
theorem edgeOK_balance {b W : Nat} {E : Edge} (he : edgeOK b E = true)
    (hC : E.C.length ≤ W) (hC2 : E.C2.length ≤ W) :
    edgeOK b (balanceEdge b W E) = true := by
  have hb := balanceTrim_balance he hC hC2
  have ht := Agent119.NeutralCenterPadding.edgeOK_transport he
    (reserve W E.C) (reserve W E.C2) (balanceTrim W E) hb
  simpa only [Agent119.NeutralCenterPadding.transportEdge, balanceEdge,
    balanceCenter] using ht

/-- Balancing preserves the actual overflow bit. -/
theorem balanceEdge_gam {b W : Nat} {E : Edge} (he : edgeOK b E = true) :
    gam b (balanceEdge b W E).B (balanceEdge b W E).C = gam b E.B E.C := by
  exact Agent119.NeutralCenterPadding.gam_padC (a := reserve W E.C)
    (edgeOK_sound he).1

/-- The existing edge-length theorem also applies to the transported edge. -/
theorem balanced_length_balance {b W : Nat} {E : Edge} (he : edgeOK b E = true)
    (hC : E.C.length ≤ W) (hC2 : E.C2.length ≤ W) :
    (balanceCenter b W E.C2).length + 2 * balanceTrim W E =
      (balanceCenter b W E.C).length + gam b E.B E.C := by
  have hl := (Agent119.NeutralLengthAccounting.edge_lengths
    (edgeOK_balance he hC hC2)).2
  rw [balanceEdge_gam he] at hl
  exact hl

/-- Only a zero or one-pair center trim is needed at the balanced widths. -/
theorem balanceTrim_le_one {b W : Nat} {E : Edge} (he : edgeOK b E = true)
    (hC : E.C.length ≤ W) (hC2 : E.C2.length ≤ W) :
    balanceTrim W E ≤ 1 := by
  have hl := balanced_length_balance he hC hC2
  have hs := balanceCenter_length_bounds b W E.C hC
  have ht := balanceCenter_length_bounds b W E.C2 hC2
  have hg := (edgeOK_sound he).1.gam_le
  omega

/-- A pair is removed exactly when overflow occurs at padded source width W. -/
theorem balanceTrim_exact {b W : Nat} {E : Edge} (he : edgeOK b E = true)
    (hC : E.C.length ≤ W) (hC2 : E.C2.length ≤ W) :
    balanceTrim W E =
      if gam b E.B E.C = 1 ∧ (balanceCenter b W E.C).length = W then 1 else 0 := by
  have hl := balanced_length_balance he hC hC2
  have hs := balanceCenter_length_bounds b W E.C hC
  have ht := balanceCenter_length_bounds b W E.C2 hC2
  have hg := (edgeOK_sound he).1.gam_le
  have hw := balanceTrim_le_one he hC hC2
  by_cases h : gam b E.B E.C = 1 ∧ (balanceCenter b W E.C).length = W
  · rw [if_pos h]
    obtain ⟨hg1, hsW⟩ := h
    omega
  · rw [if_neg h]
    by_cases hn : balanceTrim W E = 0
    · exact hn
    · have hg1 : gam b E.B E.C = 1 := by omega
      have hsW : (balanceCenter b W E.C).length = W := by omega
      exact False.elim (h ⟨hg1, hsW⟩)

end Agent104.NeutralBalancedWidth

#print axioms Agent104.NeutralBalancedWidth.balanceCenter_length
#print axioms Agent104.NeutralBalancedWidth.balanceCenter_length_bounds
#print axioms Agent104.NeutralBalancedWidth.balanceCenter_lengths
#print axioms Agent104.NeutralBalancedWidth.balanceTrim_balance
#print axioms Agent104.NeutralBalancedWidth.edgeOK_balance
#print axioms Agent104.NeutralBalancedWidth.balanceEdge_gam
#print axioms Agent104.NeutralBalancedWidth.balanced_length_balance
#print axioms Agent104.NeutralBalancedWidth.balanceTrim_le_one
#print axioms Agent104.NeutralBalancedWidth.balanceTrim_exact
