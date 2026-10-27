import P196.Agent119NeutralCenterPadding.Main

/-!
# Exact inverse of neutral-center padding

Common neutral padding can be cancelled from words and source hypotheses.
With the same additive trim balance as the forward theorem, acceptance of a
transported edge is equivalent to acceptance by the original unchanged checker.
-/

namespace Agent119.NeutralCenterUnpadding

open Agent120.Neutral
open Agent119.NeutralCenterPadding

/-- Symmetric padding by a fixed word is injective, including at width zero. -/
theorem padC_injective (b a : Nat) {C D : List Nat}
    (h : padC b a C = padC b a D) : C = D := by
  unfold padC at h
  exact List.append_cancel_right (List.append_cancel_left h)

theorem padC_inj (b a : Nat) {C D : List Nat} :
    padC b a C = padC b a D ↔ C = D :=
  ⟨padC_injective b a, fun h => congrArg (padC b a) h⟩

/-- Bounded coefficients suffice for the normalized padding formula;
the original center need not already satisfy the carry-flip condition. -/
theorem norm_padC_of_bounds {b a : Nat} {B C : List Nat}
    (hb : 2 ≤ b) (hB : ∀ v ∈ B, v ≤ 2 * (b - 1))
    (hC : ∀ v ∈ C, v ≤ 2 * (b - 1)) :
    norm b (padC b a C) (e1 b B) =
      (List.replicate a (xd b B) ++ (DC b B C ++ List.replicate a (yd b B C)),
        e2 b B C) := by
  have h1 : e1 b B ≤ 1 :=
    norm_carry_le_one b (by omega) B 0 hB (by omega)
  have h2 : e2 b B C ≤ 1 :=
    norm_carry_le_one b (by omega) C (e1 b B) hC h1
  unfold padC
  rw [norm_append, norm_replicate_neutral b hb a (e1 b B) h1]
  simp only
  rw [norm_append]
  change
    (List.replicate a (xd b B) ++
      (DC b B C ++ (norm b (List.replicate a (b - 1)) (e2 b B C)).1),
      (norm b (List.replicate a (b - 1)) (e2 b B C)).2) = _
  rw [norm_replicate_neutral b hb a (e2 b B C) h2]
  rfl

theorem e2_padC_of_bounds {b a : Nat} {B C : List Nat}
    (hb : 2 ≤ b) (hB : ∀ v ∈ B, v ≤ 2 * (b - 1))
    (hC : ∀ v ∈ C, v ≤ 2 * (b - 1)) :
    e2 b B (padC b a C) = e2 b B C := by
  have hn := congrArg Prod.snd (norm_padC_of_bounds (a := a) hb hB hC)
  exact hn

/-- Padding neither creates nor destroys the complete original source hypotheses. -/
theorem Hyp_padC_iff {b a : Nat} {B C : List Nat} :
    Hyp b B (padC b a C) ↔ Hyp b B C := by
  constructor
  · intro h
    have hC : ∀ v ∈ C, v ≤ 2 * (b - 1) := by
      intro v hv
      apply h.boundC v
      simp only [padC, List.mem_append]
      exact Or.inr (Or.inl hv)
    refine ⟨h.base, h.boundB, hC, h.ext, ?_⟩
    simpa only [e2_padC_of_bounds (a := a) h.base h.boundB hC] using h.flip
  · exact Hyp_padC

/-- Cancel the prescribed source and target padding in an accepted transported edge. -/
theorem edgeOK_of_transport {b : Nat} {E : Edge} (a a' w : Nat)
    (balance : a + E.v = w + a')
    (he : edgeOK b (transportEdge b a a' w E) = true) :
    edgeOK b E = true := by
  obtain ⟨hp, hB, hC⟩ := edgeOK_sound he
  have h : Hyp b E.B E.C := Hyp_padC_iff.mp hp
  apply edgeOK_of_equations h
  · change nextB b E.B (padC b a E.C) =
      E.B2 ++ List.replicate E.u (b - 1) at hB
    rwa [nextB_padC h] at hB
  · change nextC b E.B (padC b a E.C) =
      padC b w (padC b a' E.C2) at hC
    rw [nextC_padC h a, padC_add, ← balance] at hC
    apply padC_injective b a
    rw [padC_add]
    exact hC

/-- The exact additive balance makes local checked-edge transport an equivalence. -/
theorem edgeOK_transport_iff {b : Nat} {E : Edge} (a a' w : Nat)
    (balance : a + E.v = w + a') :
    edgeOK b (transportEdge b a a' w E) = true ↔ edgeOK b E = true :=
  ⟨edgeOK_of_transport a a' w balance,
    fun he => edgeOK_transport he a a' w balance⟩

end Agent119.NeutralCenterUnpadding

#print axioms Agent119.NeutralCenterUnpadding.padC_injective
#print axioms Agent119.NeutralCenterUnpadding.padC_inj
#print axioms Agent119.NeutralCenterUnpadding.norm_padC_of_bounds
#print axioms Agent119.NeutralCenterUnpadding.e2_padC_of_bounds
#print axioms Agent119.NeutralCenterUnpadding.Hyp_padC_iff
#print axioms Agent119.NeutralCenterUnpadding.edgeOK_of_transport
#print axioms Agent119.NeutralCenterUnpadding.edgeOK_transport_iff
