import P196.BoundaryOrdinaryStreams.History
import P196.BoundaryOrdinaryStreams.Controls

/-!
# Positive ordinary realizations of finite boundary histories

Each requested cutoff and finite horizon has a positive ordinary seed of
the stated exact initial width. The initial pair word, exterior iterates,
terminal carries, and separate canonical digit ends are all identified.
The seed is allowed to depend on the cutoff and horizon.
-/

namespace Agent5.BoundaryOrdinaryStreams

open P196.Agent7.Finite Agent6.ExteriorCoordinates
open Agent115.ExteriorFactorization Agent5.OrdinaryExteriorHistories

/-- Every valid boundary exterior other than the empty zero-phase state
has an ordinary realization of each finite coherent observation history. -/
theorem boundary_history_realized (c cut T : Nat) (B : List Nat)
    (hc : c = 0 ∨ c = 18) (hv : validOuter ⟨c, B⟩ = true)
    (hpos : c ≠ 0 ∨ B ≠ []) :
    ∃ n, 0 < n ∧
      (Agent109.digits n).length =
        2 * B.length + 2 * (2 * T + cut + 2) ∧
      Agent109.pairWord n = P196.Agent6.surrounded B c (2 * T + cut) [] ∧
      ∀ t, t ≤ T →
        ordinaryObservation cut n t =
          coherentObservation cut (outerIter t ⟨c, B⟩) := by
  obtain ⟨n, hn, hlen, hrep⟩ :=
    positive_boundary_surrounded_realized c (2 * T + cut) B hc hv hpos
  refine ⟨n, hn, hlen, hrep, ?_⟩
  exact boundary_history_of_surrounded n c cut T (2 * T + cut) B [] hc
    (entries_le_of_valid c B hv) (by simp [Agent109.Bounded]) hrep (by omega)

#print axioms boundary_history_realized

end Agent5.BoundaryOrdinaryStreams
