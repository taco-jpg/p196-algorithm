import P196.Drafts.Agent120NeutralBandCalibration.A120Certificate
import P196.Foundations.PeriodObstructions

/-!
# Actual neutral-band edges satisfy the exterior clock

This file connects the existing `Agent120.Neutral` transition to Agent 8's
finite first-coefficient potential certificate. An empty exterior is assigned
effective head 9, so every permitted exterior and every natural suffix trim
are covered. The original transition is imported without redefinition.
-/

namespace Agent104.NeutralExteriorBounds

open Agent120.Neutral

/-- The first exterior coefficient, or its neutral continuation when empty. -/
def effectiveHead (B : List Nat) : Nat := B.headD 9

theorem effectiveHead_bounds {B C : List Nat} (h : Hyp 10 B C) :
    0 < effectiveHead B ∧ effectiveHead B ≤ 18 := by
  cases B with
  | nil => decide
  | cons x xs =>
      have hx := h.boundB x List.mem_cons_self
      have hn := h.ext
      simp only [List.head?_cons, ne_eq, Option.some.injEq] at hn
      change 0 < x ∧ x ≤ 18
      omega

/-- Removing any neutral suffix preserves the effective first coefficient. -/
theorem effectiveHead_append_neutral (B : List Nat) (u : Nat) :
    effectiveHead (B ++ List.replicate u 9) = effectiveHead B := by
  cases B with
  | nil => cases u <;> simp [effectiveHead, List.replicate_succ]
  | cons x xs => rfl

private theorem raw_head_bridge {B C : List Nat} (h : Hyp 10 B C) :
    ∃ c : Nat, c ≤ 1 ∧
      gam 10 B C = Agent8.overflow (effectiveHead B) c ∧
      effectiveHead (nextB 10 B C) = Agent8.nextExterior (effectiveHead B) c := by
  cases B with
  | nil =>
      have hf := h.flip
      have hc := h.e2_le
      have he : e2 10 [] C = 1 := by
        simp only [e1, norm_nil] at hf
        omega
      refine ⟨1, by decide, ?_, ?_⟩
      · simp [gam, he, effectiveHead, Agent8.overflow]
      · simp [nextB, gam, he, DB, DR, xd, e1, effectiveHead,
          Agent8.nextExterior]
  | cons x xs =>
      let c := (norm 10 xs.reverse (e2 10 (x :: xs) C)).2
      have hc : c ≤ 1 := by
        apply norm_carry_le_one 10 (by decide) xs.reverse _
        · intro z hz
          exact h.boundB z (List.mem_cons_of_mem x (List.mem_reverse.mp hz))
        · exact h.e2_le
      have hx : x ≤ 18 := by
        have := h.boundB x List.mem_cons_self
        omega
      have hg : gam 10 (x :: xs) C = (x + c) / 10 := by
        simp [gam, List.reverse_cons, norm_append, norm_cons, c]
      have hr : (DR 10 (x :: xs) C).reverse =
          (x + c) % 10 :: (norm 10 xs.reverse (e2 10 (x :: xs) C)).1.reverse := by
        simp [DR, List.reverse_cons, norm_append, norm_cons, c]
      refine ⟨c, hc, ?_, ?_⟩
      · rw [hg]
        change (x + c) / 10 = Agent8.overflow x c
        unfold Agent8.overflow
        split <;> omega
      · by_cases hsmall : x + c < 10
        · have hgam : gam 10 (x :: xs) C = 0 := by rw [hg]; omega
          have hxm : x % 10 = x := Nat.mod_eq_of_lt (by omega)
          have hsm : (x + c) % 10 = x + c := Nat.mod_eq_of_lt hsmall
          simp [nextB, hgam, hr, DB, norm_cons, effectiveHead,
            Agent8.nextExterior, hsmall, hxm, hsm]
          omega
        · have hgam : gam 10 (x :: xs) C = 1 := by rw [hg]; omega
          simp [nextB, hgam, DB, norm_cons, effectiveHead,
            Agent8.nextExterior, hsmall]

/-- Every checked edge follows the existing positive exterior head map. -/
theorem edge_head_bridge {E : Edge} (h : edgeOK 10 E = true) :
    ∃ c : Nat, c ≤ 1 ∧
      gam 10 E.B E.C = Agent8.overflow (effectiveHead E.B) c ∧
      effectiveHead E.B2 = Agent8.nextExterior (effectiveHead E.B) c := by
  obtain ⟨hyp, hB, _⟩ := edgeOK_sound h
  obtain ⟨c, hc, hg, hn⟩ := raw_head_bridge hyp
  refine ⟨c, hc, hg, ?_⟩
  rw [hB] at hn
  change effectiveHead (E.B2 ++ List.replicate E.u 9) = _ at hn
  simpa only [effectiveHead_append_neutral] using hn

/-- Agent 8's two finite potentials apply to actual checked neutral-band edges. -/
theorem edge_potential_bounds {E : Edge} (h : edgeOK 10 E = true) :
    2 * (gam 10 E.B E.C : Int) ≤
      1 + Agent8.upperPotential (effectiveHead E.B) -
        Agent8.upperPotential (effectiveHead E.B2) ∧
    1 ≤ 4 * (gam 10 E.B E.C : Int) +
      Agent8.lowerPotential (effectiveHead E.B) -
        Agent8.lowerPotential (effectiveHead E.B2) := by
  have hp := effectiveHead_bounds (edgeOK_sound h).1
  obtain ⟨c, hc, hg, hn⟩ := edge_head_bridge h
  have hb := Agent8.exterior_bounds (effectiveHead E.B) c hp.1 hp.2 hc
  rw [← hg, ← hn] at hb
  exact hb

end Agent104.NeutralExteriorBounds

#print axioms Agent104.NeutralExteriorBounds.effectiveHead_bounds
#print axioms Agent104.NeutralExteriorBounds.effectiveHead_append_neutral
#print axioms Agent104.NeutralExteriorBounds.edge_head_bridge
#print axioms Agent104.NeutralExteriorBounds.edge_potential_bounds
