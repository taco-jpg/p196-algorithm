import P196.BoundaryOrdinaryStreams.Propagation
import P196.BoundaryOrdinaryStreams.Windows

/-!
# Boundary histories along actual ordinary orbits

The two surrounding bands lose at most two units of their gap parameter
per step. Their exact ordinary propagation supplies a bounded middle at
each time. The exterior is always the original outerIter, and each
observation reads the canonical digits of the actual ordinary successor.
-/

namespace Agent5.BoundaryOrdinaryStreams

open P196.Agent7.Finite Agent6.ExteriorCoordinates
open Agent5.OrdinaryExteriorHistories

private theorem boundary_outerIter_phase (c t : Nat) (B : List Nat)
    (hc : c = 0 ∨ c = 18) :
    (outerIter t ⟨c, B⟩).c = c := by
  induction t with
  | zero => rfl
  | succ t ih =>
      change bulkPhase (outerIter t ⟨c, B⟩).c = c
      rw [ih]
      rcases hc with rfl | rfl <;> rfl

/-- A sufficiently protected actual boundary pair word keeps the original
exterior iterate and a bounded middle throughout the available finite gap. -/
theorem boundary_surrounded_orbit (n c gap : Nat) (B W : List Nat)
    (hc : c = 0 ∨ c = 18)
    (hB : Agent109.Bounded B) (hW : Agent109.Bounded W)
    (hrep : Agent109.pairWord n = P196.Agent6.surrounded B c gap W) :
    ∀ t, 2 * t ≤ gap →
      ∃ G M, gap ≤ G + 2 * t ∧
        Agent109.Bounded (outerIter t ⟨c, B⟩).B ∧
        Agent109.Bounded M ∧
        Agent109.pairWord (Lychrel196.orbit n t) =
          P196.Agent6.surrounded (outerIter t ⟨c, B⟩).B
            (outerIter t ⟨c, B⟩).c G M := by
  intro t
  induction t with
  | zero =>
      intro _
      exact ⟨gap, W, by omega, hB, hW, hrep⟩
  | succ t ih =>
      intro ht
      obtain ⟨G, M, hG, hBt, hM, hrepT⟩ := ih (by omega)
      have hphase : (outerIter t ⟨c, B⟩).c = 0 ∨
          (outerIter t ⟨c, B⟩).c = 18 := by
        rw [boundary_outerIter_phase c t B hc]
        exact hc
      obtain ⟨g, rfl⟩ : ∃ g, G = g + 2 := ⟨G - 2, by omega⟩
      obtain ⟨G', M', hG', hM', hB', hstep⟩ :=
        boundary_pairWord_propagation (Lychrel196.orbit n t)
          (outerIter t ⟨c, B⟩).c g (outerIter t ⟨c, B⟩).B M
          hphase hBt hM hrepT
      refine ⟨G', M', by omega, ?_, hM', ?_⟩
      · exact hB'
      · exact hstep

/-- The separate ordinary digit ends and actual terminal carry agree with
the coherent boundary observations through the inclusive finite horizon. -/
theorem boundary_history_of_surrounded
    (n c cut T gap : Nat) (B W : List Nat)
    (hc : c = 0 ∨ c = 18)
    (hB : Agent109.Bounded B) (hW : Agent109.Bounded W)
    (hrep : Agent109.pairWord n = P196.Agent6.surrounded B c gap W)
    (hgap : 2 * T + cut ≤ gap) :
    ∀ t, t ≤ T →
      ordinaryObservation cut n t =
        coherentObservation cut (outerIter t ⟨c, B⟩) := by
  intro t ht
  obtain ⟨G, M, hG, hBt, hM, hrepT⟩ :=
    boundary_surrounded_orbit n c gap B W hc hB hW hrep t (by omega)
  have hphase : (outerIter t ⟨c, B⟩).c = 0 ∨
      (outerIter t ⟨c, B⟩).c = 18 := by
    rw [boundary_outerIter_phase c t B hc]
    exact hc
  have hpoint := ordinary_boundary_observation (Lychrel196.orbit n t)
    (outerIter t ⟨c, B⟩).c cut G (outerIter t ⟨c, B⟩).B M
    hphase hBt hM hrepT (by omega)
  exact hpoint

#print axioms boundary_surrounded_orbit
#print axioms boundary_history_of_surrounded

end Agent5.BoundaryOrdinaryStreams
