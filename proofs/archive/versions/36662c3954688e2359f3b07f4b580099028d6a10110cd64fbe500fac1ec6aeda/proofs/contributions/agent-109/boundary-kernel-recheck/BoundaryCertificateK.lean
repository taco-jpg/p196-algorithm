import BoundaryDataK

/-! Agent #109 kernel-only replay of `BoundaryCertificate.lean`: identical proofs with
`decide +kernel` in place of the compiler-evaluated decision procedure, over the literal
tables of `BoundaryDataK.lean`. Definitions that do not mention those tables are reused
from the original module. -/

namespace BoundaryCertificateK
open Sofic BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0


theorem fibers_arithmetic_checked :
    ((List.range 88).all fun l =>
      (fiber l).all (fun i => i < 164) &&
      (List.range 164).all (fun i =>
        (fiber l).contains i == permitted l opts[i]!)) = true := by
  decide +kernel

theorem projection0_checked : checkProjection fiber output graph0K graph1K ranks0K maps0K = true := by
  decide +kernel

theorem projection1_checked : checkProjection fiber output graph1K graph2K ranks1K maps1K = true := by
  decide +kernel

theorem projection2_checked : checkProjection fiber output graph2K graph3K ranks2K maps2K = true := by
  decide +kernel

theorem projection3_checked : checkProjection fiber output graph3K graph4K ranks3K maps3K = true := by
  decide +kernel

theorem projection4_checked : checkProjection fiber output graph4K graph5K ranks4K maps4K = true := by
  decide +kernel

theorem projection5_checked : checkProjection fiber output graph5K graph6K ranks5K maps5K = true := by
  decide +kernel

theorem projection6_checked : checkProjection fiber output graph6K graph7K ranks6K maps6K = true := by
  decide +kernel

theorem projection7_checked : checkProjection fiber output graph7K graph5K ranks7K maps7K = true := by
  decide +kernel

theorem root0_checked : checkRoot graph0K 41 rootRanks0K = true := by decide +kernel

theorem root1_checked : checkRoot graph1K 41 rootRanks1K = true := by decide +kernel

theorem root2_checked : checkRoot graph2K 41 rootRanks2K = true := by decide +kernel

theorem root3_checked : checkRoot graph3K 41 rootRanks3K = true := by decide +kernel

theorem root4_checked : checkRoot graph4K 41 rootRanks4K = true := by decide +kernel

theorem root5_checked : checkRoot graph5K 41 rootRanks5K = true := by decide +kernel

theorem root6_checked : checkRoot graph6K 41 rootRanks6K = true := by decide +kernel

theorem root7_checked : checkRoot graph7K 41 rootRanks7K = true := by decide +kernel

def Invariant (n : Nat) (w : Word) : Prop :=
  Accepts graph0K n w ∨ Accepts graph1K n w ∨ Accepts graph2K n w ∨
  Accepts graph3K n w ∨ Accepts graph4K n w ∨ Accepts graph5K n w ∨
  Accepts graph6K n w ∨ Accepts graph7K n w

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
    (ht : Accepts graph0K n target) :
    ¬ ReverseClosure.Path (Column fiber output n) (fun _ => 41) target := by
  apply ReverseClosure.excludes_reachable (root_excluded n) (Or.inl ht)
  intro p s hs hcol
  have hp := invariant_preclosed hs hcol
  refine ⟨?_, Or.inl hp⟩
  intro heq
  subst p
  exact root_excluded n hp

end BoundaryCertificateK
