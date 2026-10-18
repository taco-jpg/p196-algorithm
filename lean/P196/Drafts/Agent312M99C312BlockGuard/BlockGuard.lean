import P196.Drafts.D20261014SevenStepFormalSevenStepOrbit.SevenStepOrbit

namespace Agent312M99C312

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory
  BoundaryTransducer ActualBoundary Lychrel196 SevenStepOrbit

/-- The seven-step return guard at an arbitrary actual orbit index.
    Unlike SevenGuards, this does not silently assume the block starts at
    time zero. -/
def BlockGuards (q : Nat → Nat) (L a : Nat) : Prop :=
  controlAt q L a = false ∧
  controlAt q L (a + 1) = false ∧
  controlAt q L (a + 3) = false ∧
  controlAt q L (a + 5) = false ∧
  controlAt q L (a + 6) = true

/-- Exact arbitrary-index form of the seven-step return criterion.
    The only state assumption is that the block starts at the reset
    boundary; no guard-invariance assumption is used. -/
theorem block_return_iff
    (q : Nat → Nat) (L a : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q)
    (hreset : boundaryAt q L a = initial) :
    boundaryAt q L (a + 7) = initial ↔ BlockGuards q L a := by
  have hr := run_actual q L a 7 hL ha
  change run (boundaryAt q L a)
    [controlAt q L a, controlAt q L (a + 1), controlAt q L (a + 2),
      controlAt q L (a + 3), controlAt q L (a + 4), controlAt q L (a + 5),
      controlAt q L (a + 6)] = boundaryAt q L (a + 7) at hr
  rw [hreset] at hr
  rw [← hr]
  exact BoundaryTransducer.seven_return_iff _ _ _ _ _ _ _

/-- Two consecutive guarded blocks are sufficient for a reset at time
    fourteen. The second guard is an independent hypothesis; it is not
    inferred from the first. -/
theorem two_block_return
    (q : Nat → Nat) (L : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q)
    (hreset : boundaryAt q L 0 = initial)
    (hfirst : BlockGuards q L 0)
    (hsecond : BlockGuards q L 7) :
    boundaryAt q L 14 = initial := by
  have h7 : boundaryAt q L 7 = initial :=
    (block_return_iff q L 0 hL ha hreset).mpr hfirst
  exact (block_return_iff q L 7 hL ha h7).mpr hsecond

#print axioms block_return_iff
#print axioms two_block_return

end Agent312M99C312
