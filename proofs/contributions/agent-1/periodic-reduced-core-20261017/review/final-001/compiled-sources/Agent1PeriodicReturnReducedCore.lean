import Agent1PeriodicEighteenLabel
import Agent1PeriodicReturnCore
import Agent1PeriodicEighteenReturn

/-!
Remove the constant-eighteen label from the existing necessary return core.
The original component-constancy and catalog-membership result is reused
unchanged. This strengthens a necessary condition without constructing a
return or excluding either remaining component.
-/

namespace Agent1.Periodic
open Agent8

/-- A positive full quotient return in the original outer catalog has one
constant component label, either 8 or 129, at every state including N.
Initial catalog membership remains an explicit premise. -/
theorem quotient_return_reduced_core (B H w : Nat → Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hmem : (w 0, outside (B 0) (w 0)) ∈ outerCatalog)
    (hN : 0 < N)
    (hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0) :
    ∃ c, c ∈ [8,129] ∧ ∀ i, i ≤ N →
      (w i, outside (B i) (w i)) ∈ returnCore ∧
        outerComponent (w i, outside (B i) (w i)) = c := by
  obtain ⟨c, hc, hall⟩ := quotient_return_core B H w N hp hv hmem hN hreturn
  refine ⟨c, ?_, hall⟩
  simp only [List.mem_cons, List.not_mem_nil, or_false] at hc ⊢
  rcases hc with h8 | h129 | h130
  · exact Or.inl h8
  · exact Or.inr h129
  · have hc0 : outerComponent (w 0, outside (B 0) (w 0)) = 130 :=
      (hall 0 (Nat.zero_le N)).2.trans h130
    have hw := outerComponent_eighteen_phase (w 0, outside (B 0) (w 0)) hc0
    exact False.elim (quotient_path_eighteen_no_return B H w N hp hv hw hN hreturn)

end Agent1.Periodic

#print axioms Agent1.Periodic.quotient_return_reduced_core
