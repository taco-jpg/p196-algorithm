import P196.Agent104NeutralFunctionalSearch.Iteration
import P196.Agent104NeutralJointWidth.Decision

/-!
# Finite functional search refines the complete certificate specification

Each carrier state is followed for at most the proved state bound. A successful
positive-length return reconstructs an original checked cycle. The converse
uses an actual short normalized cycle, not a fixed-driver period assumption.
-/

namespace Agent104.NeutralFunctionalSearch

open Agent120.Neutral
open Agent104.NeutralJointWidth

/-- Search every finite start using the direct partial successor and early stop. -/
def functionalSearch (b M W : Nat) : Bool :=
  (states b M W).any fun s => returns b M W s s (stateBound b M W)

theorem functionalSearch_sound {b M W : Nat}
    (h : functionalSearch b M W = true) : JointRealizable b M W := by
  obtain ⟨s, hs, hr⟩ := List.any_eq_true.mp h
  obtain ⟨es, hc, hn, hp, hl⟩ := returns_cycle_sound hr
  exact ⟨es, s.1, s.2, hc, normalizedEdges_caps hn⟩

theorem functionalSearch_complete {b M W : Nat} (hW : 2 ≤ W)
    (h : JointRealizable b M W) : functionalSearch b M W = true := by
  obtain ⟨es, B, C, hc, hn, hp, hl⟩ :=
    (joint_iff_short_normalized b M W hW).mp h
  have hs := cycle_start_mem hc (cycle_source_states hc hn)
  exact List.any_eq_true.mpr
    ⟨(B, C), hs, returns_cycle_complete hc hn hl⟩

/-- The bounded direct algorithm decides exactly the original capped problem. -/
theorem functionalSearch_iff (b M W : Nat) (hW : 2 ≤ W) :
    functionalSearch b M W = true ↔ JointRealizable b M W :=
  ⟨functionalSearch_sound, functionalSearch_complete hW⟩

theorem functionalSearch_false_iff (b M W : Nat) (hW : 2 ≤ W) :
    functionalSearch b M W = false ↔ ¬ JointRealizable b M W := by
  rw [← functionalSearch_iff b M W hW]
  cases functionalSearch b M W <;> simp

/-- Refinement of the earlier complete but impractical edge-list specification. -/
theorem functionalSearch_eq_normalizedSearch (b M W : Nat) (hW : 2 ≤ W) :
    functionalSearch b M W = normalizedSearch b M W := by
  have hh : (functionalSearch b M W = true) ↔ normalizedSearch b M W = true :=
    (functionalSearch_iff b M W hW).trans (normalizedSearch_iff b M W hW).symm
  exact Bool.eq_iff_iff.mpr hh

/-- Decidability implemented by the direct functional search. -/
def functionalDecidable (b M W : Nat) (hW : 2 ≤ W) :
    Decidable (JointRealizable b M W) :=
  if h : functionalSearch b M W = true then
    isTrue ((functionalSearch_iff b M W hW).mp h)
  else
    isFalse (fun hc => h ((functionalSearch_iff b M W hW).mpr hc))

end Agent104.NeutralFunctionalSearch

#print axioms Agent104.NeutralFunctionalSearch.functionalSearch_sound
#print axioms Agent104.NeutralFunctionalSearch.functionalSearch_complete
#print axioms Agent104.NeutralFunctionalSearch.functionalSearch_iff
#print axioms Agent104.NeutralFunctionalSearch.functionalSearch_false_iff
#print axioms Agent104.NeutralFunctionalSearch.functionalSearch_eq_normalizedSearch
#print axioms Agent104.NeutralFunctionalSearch.functionalDecidable
