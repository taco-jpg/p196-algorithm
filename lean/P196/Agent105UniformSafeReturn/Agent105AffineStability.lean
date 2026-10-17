import P196.Agent102AffineRuns.Agent102AffineRuns
import P196.Agent105AffineComponents.Agent105AffineBasics
import P196.Agent105AffineComponents.Agent105TailSelection

/-!
Agent #105, session 8f1107db019a. Transfer Agent #102's literal-word equality
and palindrome stability to actual word families with eventual affine-run
representations. This module does not assume any new arithmetic dynamics.
-/

namespace Agent105.AffineStability

open Agent102 Agent105.AffineDynamics Agent105.TailSelection

/-- A change of predicate on only finitely many parameters preserves stability. -/
theorem tailStable_of_eventual_iff {P Q : Nat → Prop}
    (hPQ : Eventually (fun k => P k ↔ Q k)) (hP : TailStable P) :
    TailStable Q := by
  obtain ⟨Ke, he⟩ := hPQ
  obtain ⟨Kp, hp⟩ := hP
  let K := max Ke Kp
  have hKe : Ke ≤ K := Nat.le_max_left _ _
  have hKp : Kp ≤ K := Nat.le_max_right _ _
  refine ⟨K, ?_⟩
  intro k hk
  exact (he k (Nat.le_trans hKe hk)).symm.trans
    (((hp k (Nat.le_trans hKp hk)).trans (hp K hKp).symm).trans (he K hKe))

theorem wordAt_equality_tailStable (rs ss : List RunSpec) :
    TailStable (fun k => wordAt rs k = wordAt ss k) :=
  ⟨equalityCutoff rs ss, fun k hk => Agent102.wordAt_eq_stable rs ss k hk⟩

theorem wordAt_palindrome_tailStable (rs : List RunSpec) :
    TailStable (fun k => wordAt rs k = (wordAt rs k).reverse) :=
  ⟨palindromeCutoff rs, fun k hk => Agent102.wordAt_palindrome_stable rs k hk⟩

theorem hasAffineRuns_equality_tailStable (w v : Nat → List Nat) (M N : Nat)
    (hw : HasAffineRuns w M) (hv : HasAffineRuns v N) :
    TailStable (fun k => w k = v k) := by
  obtain ⟨rs, _, Kr, hr⟩ := hw
  obtain ⟨ss, _, Ks, hs⟩ := hv
  apply tailStable_of_eventual_iff (P := fun k => wordAt rs k = wordAt ss k)
  · refine ⟨max Kr Ks, ?_⟩
    intro k hk
    rw [hr k (Nat.le_trans (Nat.le_max_left _ _) hk),
      hs k (Nat.le_trans (Nat.le_max_right _ _) hk)]
  · exact wordAt_equality_tailStable rs ss

theorem hasAffineRuns_palindrome_tailStable (w : Nat → List Nat) (M : Nat)
    (hw : HasAffineRuns w M) :
    TailStable (fun k => (w k).reverse = w k) := by
  obtain ⟨rs, _, Kr, hr⟩ := hw
  apply tailStable_of_eventual_iff
    (P := fun k => wordAt rs k = (wordAt rs k).reverse)
  · refine ⟨Kr, ?_⟩
    intro k hk
    rw [hr k hk]
    exact eq_comm
  · exact wordAt_palindrome_tailStable rs

theorem hasAffineRuns_nonpalindrome_tailStable (w : Nat → List Nat) (M : Nat)
    (hw : HasAffineRuns w M) :
    TailStable (fun k => (w k).reverse ≠ w k) :=
  tailStable_not (hasAffineRuns_palindrome_tailStable w M hw)

end Agent105.AffineStability

#print axioms Agent105.AffineStability.tailStable_of_eventual_iff
#print axioms Agent105.AffineStability.wordAt_equality_tailStable
#print axioms Agent105.AffineStability.wordAt_palindrome_tailStable
#print axioms Agent105.AffineStability.hasAffineRuns_equality_tailStable
#print axioms Agent105.AffineStability.hasAffineRuns_palindrome_tailStable
#print axioms Agent105.AffineStability.hasAffineRuns_nonpalindrome_tailStable
