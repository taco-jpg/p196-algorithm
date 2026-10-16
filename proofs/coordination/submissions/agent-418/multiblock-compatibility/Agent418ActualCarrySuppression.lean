import Agent15ActualFourthColumn
import Agent418SaturatedCarrySuppression

/-! Agent #418: exact ordinary-decimal consequence of the cross-block bound.
No symbolic transition or guard preservation is assumed. -/
namespace Agent418.ActualCarrySuppression
open DecimalDigits FoldedDecimal P196.Agent4.Saturation
open Agent15.FourthColumn Agent15.ActualFourthColumn Agent418.CarrySuppression
set_option maxRecDepth 10000
set_option maxHeartbeats 4000000

/-- Canonical arithmetic alone supplies every four-column transition. -/
theorem canonical_window_fourth_le_eight (n : Nat)
    (d : Nat → Nat → Nat) (L : Nat → Nat)
    (hc : ∀ i ≤ 4, Canonical (Lychrel196.orbit n i) (d i) (L i))
    (hL : 4 ≤ L 0)
    (hp : ∀ i ≤ 4, (projectQuad (columnSum (d i) (L i))).p = windowPrefix i) :
    4 ≤ L 4 ∧ columnSum (d 4) (L 4) 3 ≤ 8 := by
  have c0 := hc 0 (by decide)
  have c1 := hc 1 (by decide)
  have c2 := hc 2 (by decide)
  have c3 := hc 3 (by decide)
  have c4 := hc 4 (by decide)
  obtain ⟨hL1,e0,he0,hs0⟩ := canonical_step_projection n (d 0) (d 1)
    (L 0) (L 1) c0 c1 hL
  obtain ⟨hL2,e1,he1,hs1⟩ := canonical_step_projection _ (d 1) (d 2)
    (L 1) (L 2) c1 c2 hL1
  obtain ⟨hL3,e2,he2,hs2⟩ := canonical_step_projection _ (d 2) (d 3)
    (L 2) (L 3) c2 c3 hL2
  obtain ⟨hL4,e3,he3,hs3⟩ := canonical_step_projection _ (d 3) (d 4)
    (L 3) (L 4) c3 c4 hL3
  have hinit : projectQuad (columnSum (d 0) (L 0)) =
      ⟨windowPrefix 0,columnSum (d 0) (L 0) 3⟩ := by
    calc projectQuad (columnSum (d 0) (L 0)) =
        ⟨(projectQuad (columnSum (d 0) (L 0))).p,columnSum (d 0) (L 0) 3⟩ := rfl
      _ = _ := by rw [hp 0 (by decide)]
  have hm : windowMatches (columnSum (d 0) (L 0) 3) e0 e1 e2 e3 := by
    unfold windowMatches
    rw [← hinit]
    simp only [walk,List.foldl_cons,List.foldl_nil]
    rw [hs0,hs1,hs2,hs3]
    exact ⟨hp 1 (by decide),hp 2 (by decide),hp 3 (by decide),hp 4 (by decide)⟩
  have hb := four_step_bound _ e0 e1 e2 e3
    (columnSum_bounded (d 0) (L 0) c0.2.1 3 (by omega)) he0 he1 he2 he3 hm
  rw [← hinit] at hb
  simp only [walk,List.foldl_cons,List.foldl_nil] at hb
  rw [hs0,hs1,hs2,hs3] at hb
  exact ⟨hL4,hb⟩

/-- The observed third-column carry equals the inner carry of the exact
four-column model, including all overlapping words of width at least four. -/
theorem canonical_carry_zero_of_fourth_bound (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hL : 4 ≤ L) (hd : columnSum d L 3 ≤ 8) :
    carry (columnSum d L) (L - 3) = 0 := by
  have hb := carry_bounded (columnSum d L) L
    (columnSum_bounded d L hc.2.1) (L - 4) (by omega)
  have ht := (folded_carry_transition (columnSum d L) L 3 (by omega)
    (columnSum_symmetric d L)).2
  have heq : L - 1 - 3 = L - 4 := by omega
  rw [heq] at ht
  omega

theorem canonical_window_carry_zero (n : Nat)
    (d : Nat → Nat → Nat) (L : Nat → Nat)
    (hc : ∀ i ≤ 4, Canonical (Lychrel196.orbit n i) (d i) (L i))
    (hL : 4 ≤ L 0)
    (hp : ∀ i ≤ 4, (projectQuad (columnSum (d i) (L i))).p = windowPrefix i) :
    carry (columnSum (d 4) (L 4)) (L 4 - 3) = 0 := by
  have hb := canonical_window_fourth_le_eight n d L hc hL hp
  exact canonical_carry_zero_of_fourth_bound _ _ _ (hc 4 (by decide)) hb.1 hb.2

/-- A two-step prelude rules out the width-three overlap without assuming it. -/
def extendedPrefix : Nat → Prefix
  | 0 => ⟨17,6,11⟩
  | 1 => ⟨8,14,8⟩
  | i+2 => windowPrefix i

/-- Ordinary seven-state window theorem. The only inputs are canonical
representations and the observed three-column prefixes; width four is derived. -/
theorem extended_window_carry_zero (n : Nat)
    (d : Nat → Nat → Nat) (L : Nat → Nat)
    (hc : ∀ i ≤ 6, Canonical (Lychrel196.orbit n i) (d i) (L i))
    (hL : 3 ≤ L 0)
    (hp : ∀ i ≤ 6, (projectQuad (columnSum (d i) (L i))).p = extendedPrefix i) :
    carry (columnSum (d 6) (L 6)) (L 6 - 3) = 0 := by
  have hL0 : 4 ≤ L 0 := width_four_of_prefix n (d 0) (L 0)
    (extendedPrefix 0) (hc 0 (by decide)) hL (hp 0 (by decide)) (by decide)
  have hL1 := (canonical_step_projection n (d 0) (d 1) (L 0) (L 1)
    (hc 0 (by decide)) (hc 1 (by decide)) hL0).1
  have hL2 := (canonical_step_projection _ (d 1) (d 2) (L 1) (L 2)
    (hc 1 (by decide)) (hc 2 (by decide)) hL1).1
  refine canonical_window_carry_zero (Lychrel196.orbit n 2)
    (fun i => d (i+2)) (fun i => L (i+2)) ?_ hL2 ?_
  · intro i hi
    have h := hc (i+2) (by omega)
    simpa only [Nat.add_comm i 2, LychrelCertificates.orbit_add] using h
  · intro i hi
    exact hp (i+2) (by omega)

#print axioms extended_window_carry_zero

#print axioms canonical_window_fourth_le_eight
#print axioms canonical_carry_zero_of_fourth_bound
#print axioms canonical_window_carry_zero
end Agent418.ActualCarrySuppression
