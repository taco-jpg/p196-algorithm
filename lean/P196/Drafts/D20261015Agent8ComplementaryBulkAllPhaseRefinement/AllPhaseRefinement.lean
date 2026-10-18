import P196.Foundations.ActualWordBridge

namespace Agent8

/-- The remaining two-cycle of the complementary nonneutral phase map. -/
def TwoPhase (c : Nat) : Prop := c = 6 ∨ c = 12

def PeriodicPhase (c : Nat) : Prop := SixPhase c ∨ TwoPhase c

theorem returned_two_phase_mass_congruence (c : Nat) (B A C : Word)
    (g0 h0 g1 h1 k : Nat) (hc : TwoPhase c)
    (hr : orbit (template c B A C g0 h0) (6*k) = template c B A C g1 h1) :
    (((g1 : Int)-(g0 : Int))-((h1 : Int)-(h0 : Int))) % 3 = 0 := by
  have hm := six_multiple_mass_mod (template c B A C g0 h0) k
  rw [hr, template_mass, template_mass] at hm
  rcases hc with rfl | rfl <;> omega

theorem six_step_two_phase_forced_loss (H dg dh : Int)
    (hLower : 6 ≤ 4*H) (hUpper : 2*H ≤ 6)
    (hWidth : H = 2*(dg+dh)) (hMass : (dg-dh)%3=0) :
    H=2 ∧ dg+dh=1 ∧ (dg ≤ -1 ∨ dh ≤ -1) := by
  omega

theorem no_repeatable_six_step_periodic_template_return (c : Nat) (B A C : Word)
    (g0 h0 g1 h1 : Nat) (hc : PeriodicPhase c) (hg0 : 0 < g0)
    (hw : CanonicalPair (template c B A C g0 h0))
    (hg : g0 ≤ g1) (hh : h0 ≤ h1) :
    orbit (template c B A C g0 h0) 6 ≠ template c B A C g1 h1 := by
  rcases hc with hc | hc
  · exact no_repeatable_six_step_canonical_template_return c B A C g0 h0 g1 h1 hc hg0 hw hg hh
  · intro hr
    have hd := canonical_template_return_data c B A C g0 h0 g1 h1 6 hg0 (by omega) hw hr
    have hm := returned_two_phase_mass_congruence c B A C g0 h0 g1 h1 1 hc hr
    have h := six_step_two_phase_forced_loss _ _ _ hd.1 hd.2.1 hd.2.2 hm
    omega

theorem returned_six_phase_twelve_step_gains (c : Nat) (B A C : Word)
    (g0 h0 g1 h1 : Nat) (hc : SixPhase c) (hg0 : 0 < g0)
    (hw : CanonicalPair (template c B A C g0 h0))
    (hg : g0 ≤ g1) (hh : h0 ≤ h1)
    (hr : orbit (template c B A C g0 h0) 12 = template c B A C g1 h1) :
    g1 = g0+1 ∧ h1 = h0+1 ∧ actualOverflows (template c B A C g0 h0) 12 = 4 := by
  have hd := canonical_template_return_data c B A C g0 h0 g1 h1 12 hg0 (by omega) hw hr
  have hm := returned_template_mass_congruence c B A C g0 h0 g1 h1 2 hc hr
  have h := twelve_step_gains _ _ _ hd.1 hd.2.1 hd.2.2 hm (by omega) (by omega)
  omega

theorem returned_six_phase_eighteen_step_gains (c : Nat) (B A C : Word)
    (g0 h0 g1 h1 : Nat) (hc : SixPhase c) (hg0 : 0 < g0)
    (hw : CanonicalPair (template c B A C g0 h0))
    (hg : g0 ≤ g1) (hh : h0 ≤ h1)
    (hr : orbit (template c B A C g0 h0) 18 = template c B A C g1 h1) :
    g1 = g0+2 ∧ h1 = h0+2 ∧ actualOverflows (template c B A C g0 h0) 18 = 8 := by
  have hd := canonical_template_return_data c B A C g0 h0 g1 h1 18 hg0 (by omega) hw hr
  have hm := returned_template_mass_congruence c B A C g0 h0 g1 h1 3 hc hr
  have h := eighteen_step_gains _ _ _ hd.1 hd.2.1 hd.2.2 hm (by omega) (by omega)
  omega

#print axioms returned_two_phase_mass_congruence
#print axioms six_step_two_phase_forced_loss
#print axioms no_repeatable_six_step_periodic_template_return
#print axioms returned_six_phase_twelve_step_gains
#print axioms returned_six_phase_eighteen_step_gains

end Agent8
