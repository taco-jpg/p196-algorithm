import BoundaryData

/-!
Concrete finite checks and unbounded-width exclusion.

TRUST: finite Boolean checks use `native_decide` (Lean 4.19.0). Their
theorems therefore depend on `Lean.ofReduceBool`, in addition to ordinary
logical axioms. No user axiom, external oracle, or `sorry` is declared.
The generic soundness proof in SoficProof.lean does not use native_decide.
-/

namespace BoundaryCertificate
open Sofic

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem fibers_arithmetic_checked :
    ((List.range 88).all fun l =>
      (fiber l).all (fun i => i < 164) &&
      (List.range 164).all (fun i =>
        (fiber l).contains i == permitted l opts[i]!)) = true := by
  native_decide

theorem projection0_checked : checkProjection fiber output graph0 graph1 ranks0 maps0 = true := by
  native_decide
theorem projection1_checked : checkProjection fiber output graph1 graph2 ranks1 maps1 = true := by
  native_decide
theorem projection2_checked : checkProjection fiber output graph2 graph3 ranks2 maps2 = true := by
  native_decide
theorem projection3_checked : checkProjection fiber output graph3 graph4 ranks3 maps3 = true := by
  native_decide
theorem projection4_checked : checkProjection fiber output graph4 graph5 ranks4 maps4 = true := by
  native_decide
theorem projection5_checked : checkProjection fiber output graph5 graph6 ranks5 maps5 = true := by
  native_decide
theorem projection6_checked : checkProjection fiber output graph6 graph7 ranks6 maps6 = true := by
  native_decide
theorem projection7_checked : checkProjection fiber output graph7 graph5 ranks7 maps7 = true := by
  native_decide

theorem root0_checked : checkRoot graph0 41 rootRanks0 = true := by native_decide
theorem root1_checked : checkRoot graph1 41 rootRanks1 = true := by native_decide
theorem root2_checked : checkRoot graph2 41 rootRanks2 = true := by native_decide
theorem root3_checked : checkRoot graph3 41 rootRanks3 = true := by native_decide
theorem root4_checked : checkRoot graph4 41 rootRanks4 = true := by native_decide
theorem root5_checked : checkRoot graph5 41 rootRanks5 = true := by native_decide
theorem root6_checked : checkRoot graph6 41 rootRanks6 = true := by native_decide
theorem root7_checked : checkRoot graph7 41 rootRanks7 = true := by native_decide

def Invariant (n : Nat) (w : Word) : Prop :=
  Accepts graph0 n w ∨ Accepts graph1 n w ∨ Accepts graph2 n w ∨
  Accepts graph3 n w ∨ Accepts graph4 n w ∨ Accepts graph5 n w ∨
  Accepts graph6 n w ∨ Accepts graph7 n w

theorem invariant_preclosed {n : Nat} {old new : Word}
    (hnew : Invariant n new) (hcol : Column fiber output n old new) :
    Invariant n old := by
  rcases hnew with h | h | h | h | h | h | h | h
  · exact Or.inr (Or.inl (projection_sound (checkProjection_sound projection0_checked) h hcol))
  · exact Or.inr (Or.inr (Or.inl (projection_sound (checkProjection_sound projection1_checked) h hcol)))
  · exact Or.inr (Or.inr (Or.inr (Or.inl (projection_sound (checkProjection_sound projection2_checked) h hcol))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl (projection_sound (checkProjection_sound projection3_checked) h hcol)))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl (projection_sound (checkProjection_sound projection4_checked) h hcol))))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl (projection_sound (checkProjection_sound projection5_checked) h hcol)))))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (projection_sound (checkProjection_sound projection6_checked) h hcol)))))))
  · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl (projection_sound (checkProjection_sound projection7_checked) h hcol))))))

theorem root_excluded (n : Nat) : ¬ Invariant n (fun _ => 41) := by
  intro h
  rcases h with h | h | h | h | h | h | h | h
  · exact checkRoot_sound root0_checked n h
  · exact checkRoot_sound root1_checked n h
  · exact checkRoot_sound root2_checked n h
  · exact checkRoot_sound root3_checked n h
  · exact checkRoot_sound root4_checked n h
  · exact checkRoot_sound root5_checked n h
  · exact checkRoot_sound root6_checked n h
  · exact checkRoot_sound root7_checked n h

/-- Every finite width is excluded, simultaneously for every temporal period.
The target language is the two explicitly given primitive six-letter cycles.
-/
theorem no_finite_exterior {n : Nat} {target : Word}
    (ht : Accepts graph0 n target) :
    ¬ ReverseClosure.Path (Column fiber output n) (fun _ => 41) target := by
  apply ReverseClosure.excludes_reachable (root_excluded n) (Or.inl ht)
  intro p s hs hcol
  have hp := invariant_preclosed hs hcol
  refine ⟨?_, Or.inl hp⟩
  intro heq
  subst p
  exact root_excluded n hp

#print axioms fibers_arithmetic_checked
#print axioms invariant_preclosed
#print axioms no_finite_exterior

end BoundaryCertificate
