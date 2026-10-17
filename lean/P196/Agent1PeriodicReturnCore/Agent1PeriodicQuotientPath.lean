import P196.Foundations.Agent1PeriodicWidthPath
import P196.Agent1PeriodicOuterCatalog.Agent1PeriodicOuterCatalog

/-!
Finite propagation through the original literal maximal quotient. The path
contract supplies all three successor equalities. Initial full validity and
initial catalog membership propagate through the endpoint, including an
empty path. Each used edge retains its actual clock and exceptional carry
labels. No closed path, exponent guard, or ordinary orbit is asserted here.
-/

namespace Agent1.Periodic
open Agent8

/-- Full validity and physical outside/phase catalog membership hold at
every state of an exact finite quotient path, including its final state. -/
theorem quotient_path_valid_catalog (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hs : (w 0, outside (B 0) (w 0)) ∈ outerCatalog)
    (i : Nat) (hi : i ≤ N) :
    ValidPeriodic (B i) (H i) (w i) ∧
      (w i, outside (B i) (w i)) ∈ outerCatalog := by
  revert hi
  induction i with
  | zero => intro _; exact ⟨hv, hs⟩
  | succ i ih =>
    intro hi
    have hprev := ih (by omega)
    obtain ⟨_, _, _, _, hB, hH, hw⟩ := hp i (by omega)
    have hnext := quotient_valid_in_outerCatalog (B i) (H i) (w i)
      hprev.1 hprev.2
    simpa only [hB, hH, hw] using hnext

/-- Every used path transition is the original catalog edge with its actual
raw overflow and actual all-nine entry bits, at the literal next state. -/
theorem quotient_path_outer_edge (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hs : (w 0, outside (B 0) (w 0)) ∈ outerCatalog)
    (i : Nat) (hi : i < N) :
    ∃ e, e ∈ outerEdges ∧ e.source = (w i, outside (B i) (w i)) ∧
      e.clock = rawGamma (B i) (H i) (w i) ∧
      e.carries = (if w i = [9,9,9,9] then
        some (leftEntry (B i), rightEntry (B i) (H i) (w i)) else none) ∧
      e.target = (w (i+1), outside (B (i+1)) (w (i+1))) := by
  have hstate := quotient_path_valid_catalog B H w N hp hv hs i (by omega)
  obtain ⟨_, _, _, _, hB, _, hw⟩ := hp i hi
  obtain ⟨e, he, hsource, hclock, hcarries, htarget⟩ :=
    quotient_outer_catalog_edge (B i) (H i) (w i) hstate.1 hstate.2
  refine ⟨e, he, hsource, hclock, hcarries, ?_⟩
  simpa only [hB, hw] using htarget

end Agent1.Periodic

#print axioms Agent1.Periodic.quotient_path_valid_catalog
#print axioms Agent1.Periodic.quotient_path_outer_edge
