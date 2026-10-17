import Agent1PeriodicOuterRank
import Agent1PeriodicQuotientPath
import Agent1PeriodicZeroPath
import CondensationBound

/-!
Necessary restrictions on positive complete-tuple returns of the original
period-four quotient. The component-interval argument is the existing
CondensationBound theorem. The constant-zero component is excluded by the
existing full-interface no-return theorem, while its abstract graph edges
remain present. No return, safety condition, or numeric trajectory is asserted
to exist.
-/

namespace Agent1.Periodic

open Agent8

/-- The retained nonzero component labels of the original outer catalog. -/
def returnCore : List OuterNode :=
  outerCatalog.filter (fun s => decide (outerComponent s ∈ [8,129,130]))

/-- A complete-tuple return has constant projected component throughout the
finite path, including the returned endpoint. Zero steps are allowed here. -/
theorem quotient_return_component_constant (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hmem : (w 0, outside (B 0) (w 0)) ∈ outerCatalog)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    ∀ i, i ≤ N →
      outerComponent (w i, outside (B i) (w i)) =
        outerComponent (w 0, outside (B 0) (w 0)) := by
  let component : Nat → Nat := fun i => outerComponent (w i, outside (B i) (w i))
  have hcert : CondensationBound.RankCertificate component (fun _ => 1)
      componentRank (N+1) := by
    constructor
    · intro i _
      change 1 ≤ componentRank (component i)
      exact componentRank_pos (component i)
    · intro i hi hne
      obtain ⟨e, he, hs, _, _, ht⟩ :=
        quotient_path_outer_edge B H w N hp hv hmem i (by omega)
      have hne' : outerComponent e.source ≠ outerComponent e.target := by
        rw [hs, ht]
        exact hne
      have hd := outerEdge_rank_drop e he hne'
      simpa only [hs, ht] using hd
  have hclose : component 0 = component N := by
    dsimp only [component]
    rw [hreturn.1, hreturn.2.2]
  have hinter := CondensationBound.component_interval component (fun _ => 1)
    componentRank (N+1) 0 N hcert (fun _ _ => Nat.zero_lt_one)
      (Nat.zero_le N) (by omega) hclose
  intro i hi
  exact hinter i (Nat.zero_le i) hi

/-- Every positive complete-tuple return stays in one retained nonzero
component. The endpoint is included; no exponent or safety premise is used. -/
theorem quotient_return_core (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hmem : (w 0, outside (B 0) (w 0)) ∈ outerCatalog)
    (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    ∃ c, c ∈ [8,129,130] ∧ ∀ i, i ≤ N →
      (w i, outside (B i) (w i)) ∈ returnCore ∧
        outerComponent (w i, outside (B i) (w i)) = c := by
  have hconstant := quotient_return_component_constant B H w N hp hv hmem hreturn
  obtain ⟨e, he, hs, _, _, ht⟩ :=
    quotient_path_outer_edge B H w N hp hv hmem 0 hN
  have heq : outerComponent e.source = outerComponent e.target := by
    rw [hs, ht]
    exact (hconstant 1 (by omega)).symm
  have hfour := outerEdge_internal_component e he heq
  rw [hs] at hfour
  have hnonzero : outerComponent (w 0, outside (B 0) (w 0)) ≠ 131 := by
    intro hzero
    have hwzero := outerComponent_zero_phase (w 0, outside (B 0) (w 0)) hmem hzero
    exact quotient_path_zero_no_return B H w N hp hv hwzero hN hreturn
  have hlabel : outerComponent (w 0, outside (B 0) (w 0)) ∈ [8,129,130] := by
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hfour ⊢
    rcases hfour with h8 | h129 | h130 | h131
    · exact Or.inl h8
    · exact Or.inr (Or.inl h129)
    · exact Or.inr (Or.inr h130)
    · exact False.elim (hnonzero h131)
  refine ⟨outerComponent (w 0, outside (B 0) (w 0)), hlabel, ?_⟩
  intro i hi
  have hiMem := (quotient_path_valid_catalog B H w N hp hv hmem i hi).2
  have hiComponent := hconstant i hi
  refine ⟨List.mem_filter.mpr ⟨hiMem, ?_⟩, hiComponent⟩
  simpa only [hiComponent, decide_eq_true_eq] using hlabel

/-- At the original initial phase, a positive complete-tuple return permits
only the physical outside values nine or ten. Initial catalog membership is
supplied by original validity and the checked eighteen initial rows. -/
theorem quotient_return_initial_outside (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hphase : w 0 = [14,14,4,4]) (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    outside (B 0) (w 0) = 9 ∨ outside (B 0) (w 0) = 10 := by
  have hb := outside_bounds (B 0) (H 0) (w 0) hv
  have hfinite : outside (B 0) (w 0) < 19 := by omega
  have hmem : (w 0, outside (B 0) (w 0)) ∈ outerCatalog := by
    have hi := outerCatalog_initial ⟨outside (B 0) (w 0), hfinite⟩ hb.1
    simpa only [hphase] using hi
  obtain ⟨c, hc, hall⟩ := quotient_return_core B H w N hp hv hmem hN hreturn
  have hc0 := (hall 0 (Nat.zero_le N)).2
  exact outerComponent_initial_core (w 0, outside (B 0) (w 0)) hmem hphase
    (by rw [hc0]; exact hc)

end Agent1.Periodic

#print axioms Agent1.Periodic.quotient_return_component_constant
#print axioms Agent1.Periodic.quotient_return_core
#print axioms Agent1.Periodic.quotient_return_initial_outside
