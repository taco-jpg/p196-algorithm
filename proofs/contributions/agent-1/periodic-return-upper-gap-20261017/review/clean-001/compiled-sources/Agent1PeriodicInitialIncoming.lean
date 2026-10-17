import Agent1PeriodicQuotientPath

/-!
The unchanged phase catalog has clock one on every edge returning to the
original phase [14,14,4,4]. Transporting that finite certificate through the
literal quotient path identifies the actual last raw overflow. This is a
necessary condition on a positive full-tuple return, not an existence or
ordinary-orbit realization statement.
-/

namespace Agent1.Periodic
open Agent8

private theorem phaseEdges_initial_clock_checked :
    phaseEdges.all (fun e =>
      decide (e.target = [14,14,4,4] → e.clock = 1)) = true := by decide

/-- Every archived phase edge entering the original phase has clock one. -/
theorem phaseEdge_initial_clock (e : PhaseEdge) (he : e ∈ phaseEdges)
    (ht : e.target = [14,14,4,4]) : e.clock = 1 := by
  have h := List.all_eq_true.mp phaseEdges_initial_clock_checked e he
  exact (of_decide_eq_true h) ht

/-- A positive exact full-tuple return at the original phase has actual raw
overflow one on its last transition. Original validity supplies catalog
membership; no catalog hypothesis or exponent trajectory is required. -/
theorem quotient_return_initial_last_clock (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hphase : w 0 = [14,14,4,4]) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    rawGamma (B (N-1)) (H (N-1)) (w (N-1)) = 1 := by
  have hb := outside_bounds (B 0) (H 0) (w 0) hv
  have hfinite : outside (B 0) (w 0) < 19 := by omega
  have hmem : (w 0, outside (B 0) (w 0)) ∈ outerCatalog := by
    have hi := outerCatalog_initial ⟨outside (B 0) (w 0), hfinite⟩ hb.1
    simpa only [hphase] using hi
  have hlast : N-1 < N := by omega
  have hstate := quotient_path_valid_catalog B H w N hp hv hmem (N-1) (by omega)
  have hphaseMem := outerCatalog_phase_mem
    (w (N-1), outside (B (N-1)) (w (N-1))) hstate.2
  obtain ⟨hB, hH, hw, hlen, _, _, hnext⟩ := hp (N-1) hlast
  obtain ⟨e, he, _, hclock, _, htarget⟩ :=
    rawPeriod_catalog_edge (B (N-1)) (H (N-1)) (w (N-1)) hB hH hw hlen hphaseMem
  have hn : N-1+1 = N := by omega
  have ht : e.target = [14,14,4,4] := by
    rw [htarget, ← hnext, hn, hreturn.2.2, hphase]
  rw [← hclock]
  exact phaseEdge_initial_clock e he ht

end Agent1.Periodic

#print axioms Agent1.Periodic.phaseEdge_initial_clock
#print axioms Agent1.Periodic.quotient_return_initial_last_clock
