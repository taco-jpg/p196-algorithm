import SevenStepOrbit

/-!
Agent #12 / M99-A02.

WIP target: the unconditional preservation of SevenGuards across a
seven-step actual return is false. The computational witness is the
canonical pair word with middle (1,3,16,3,1), realized by 44013800000.
This file intentionally contains no placeholder proof and is not an
accepted theorem until it compiles and receives the required audit.
-/

namespace Agent12M99A02

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
  BoundaryTransducer ActualBoundary Lychrel196 SevenStepOrbit

/-- Concrete middle used by the guard-preservation counterexample. -/
def witnessMiddle : List Nat := [1, 3, 16, 3, 1]

/-- Exact research target: after one guarded return, the next returned
    interface need not satisfy the same seven-step guard. -/
def GuardPreservationTarget : Prop :=
  ¬ (∀ (q : Nat → Nat) (L : Nat),
      6 ≤ L →
      Admissible L q →
      boundary q = initial →
      SevenGuards q L →
      SevenGuards
        (fun i => (iterPairs q L 7).2 i)
        (iterPairs q L 7).1)

-- Proof intentionally omitted: WIP target only.
-- The exact concrete witness is recorded in COUNTEREXAMPLE.md.
-- A completed proof must use the repository's ordinary-decimal semantics,
-- not a freely chosen transducer trajectory.

end Agent12M99A02
