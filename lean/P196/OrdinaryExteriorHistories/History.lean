import P196.OrdinaryExteriorHistories.Ends

/-!
# Separate ordinary observations along a finite template orbit

The existing actual-template orbit theorem supplies the template at each
time and bounds the loss of both bands. Applying the one-step observation
identity to those templates gives the chronological carry and digit-end
observations of the accepted ordinary integer orbit.

The exterior state at time `t` uses the original `outerNext` iterate. The
observed ordinary digits belong to time `t + 1`, while the observed carry
belongs to the transition starting at time `t`.
-/

namespace Agent5.OrdinaryExteriorHistories

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.FiniteExteriorHistories Agent6.ExteriorCoordinates

/-- A template with enough of both bands realizes every prescribed exterior
observation through the inclusive finite horizon, using the terminal carry
and the separate ends of the actual ordinary successor's canonical digits. -/
theorem ordinary_history_of_template
    (n c cut T : Nat) (B I C : List Nat) (g h : Nat)
    (hc : nonneutralPhase c)
    (hB : Agent109.Bounded B) (hI : Agent109.Bounded I)
    (hC : Agent109.Bounded C)
    (hrep : Agent109.pairWord n = Agent109.template c B I C g h)
    (hg : 2 * T + cut + 2 ≤ g) (hh : 2 * T + cut + 2 ≤ h) :
    ∀ t, t ≤ T →
      ordinaryObservation cut n t =
        observation cut (outerIter t { c := c, B := B }) := by
  intro t ht
  obtain ⟨I', C', G, H, _, hBt, hIt, hCt, hG, hH, hrepT⟩ :=
    Agent109.Outer.actual_outer_orbit n c B I C g h
      (phase_of_nonneutral c hc) hB hI hC hrep t (by omega) (by omega)
  have hiter : outerIter t { c := c, B := B } =
      Agent109.Outer.outerIter t { c := c, B := B } :=
    outerIter_eq_chain
      (fun i => Agent109.Outer.outerIter i { c := c, B := B }) t
      (by intro i hi; rfl)
  have hphase : nonneutralPhase
      (Agent109.Outer.outerIter t { c := c, B := B }).c := by
    rw [← hiter]
    exact outerIter_nonneutral { c := c, B := B } t hc
  have hrepOriginal : Agent109.pairWord (Lychrel196.orbit n t) =
      Agent109.template
        (Agent109.Outer.outerIter t { c := c, B := B }).c
        (Agent109.Outer.outerIter t { c := c, B := B }).B I' C' G H := by
    rw [Agent109.Compat.orbit_eq]
    exact hrepT
  have hpoint := ordinary_step_observation_of_template
    (Lychrel196.orbit n t)
    (Agent109.Outer.outerIter t { c := c, B := B }).c cut
    (Agent109.Outer.outerIter t { c := c, B := B }).B I' C' G H
    hphase hBt hIt hCt hrepOriginal (by omega) (by omega)
  change ordinaryObservation cut n t =
    observation cut (Agent109.Outer.outerIter t { c := c, B := B }) at hpoint
  rw [← hiter] at hpoint
  exact hpoint

#print axioms ordinary_history_of_template

end Agent5.OrdinaryExteriorHistories
