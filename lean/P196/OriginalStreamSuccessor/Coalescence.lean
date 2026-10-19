import P196.OriginalStreamSuccessor.Decoder
import P196.Agent6CoordinateDynamics.CoordinateCycle

/-!
# Exact future agreement from the original coordinate streams

The corrected decoder determines a unique original successor even when
the initial coefficient words or calculated carries differ. Equality
after the first step then propagates through every later exact exterior
state by determinism. No assumptions about those future states are needed.
-/

namespace Agent5.OriginalStreamSuccessor

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.BoundedStreamCandidates Agent5.CompleteExteriorFibers
open Agent6.ExteriorCoordinates

/-- Sufficiently long common original prefixes force exact equality of
the two exterior successors, with no supplied carry or validity condition. -/
theorem outerNext_eq_of_prefixes (cut : Nat) (s q : Outer)
    (hs : s.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hq : q.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hBs : ∀ x ∈ s.B, x ≤ 18) (hBq : ∀ x ∈ q.B, x ≤ 18)
    (hcut : max s.B.length q.B.length + 2 ≤ cut)
    (hlo : originalLow cut q = originalLow cut s)
    (hhi : originalHigh cut q = originalHigh cut s) :
    outerNext q = outerNext s := by
  have hsCut : s.B.length + 2 ≤ cut := by
    have := Nat.le_max_left s.B.length q.B.length
    omega
  have hqCut : q.B.length + 2 ≤ cut := by
    have := Nat.le_max_right s.B.length q.B.length
    omega
  calc
    outerNext q = successorFromPrefixes cut
        (originalLow cut q) (originalHigh cut q) :=
      (successorFromPrefixes_correct q.c cut q.B hq hBq hqCut).symm
    _ = successorFromPrefixes cut (originalLow cut s) (originalHigh cut s) := by
      rw [hlo, hhi]
    _ = outerNext s := successorFromPrefixes_correct s.c cut s.B hs hBs hsCut

/-- All bounded-coefficient representatives of the same two complete
original streams have exactly the same successor in the ten even phases. -/
theorem outerNext_eq_of_complete_streams (s q : Outer)
    (hs : s.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hq : q.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hBs : ∀ x ∈ s.B, x ≤ 18) (hBq : ∀ x ∈ q.B, x ≤ 18)
    (hstreams : sameStreams s q) :
    outerNext q = outerNext s := by
  exact outerNext_eq_of_prefixes (max s.B.length q.B.length + 2) s q
    hs hq hBs hBq (Nat.le_refl _) (hstreams _).1 (hstreams _).2

/-- Complete original stream equality fixes every exact exterior state
after time zero, even if the initial states and actual carries differ. -/
theorem outerIter_positive_eq_of_complete_streams (s q : Outer)
    (hs : s.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hq : q.c ∈ [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
    (hBs : ∀ x ∈ s.B, x ≤ 18) (hBq : ∀ x ∈ q.B, x ≤ 18)
    (hstreams : sameStreams s q) :
    ∀ t : Nat, outerIter (t + 1) q = outerIter (t + 1) s := by
  intro t
  induction t with
  | zero => exact outerNext_eq_of_complete_streams s q hs hq hBs hBq hstreams
  | succ t ih =>
    change outerNext (outerIter (t + 1) q) = outerNext (outerIter (t + 1) s)
    exact congrArg outerNext ih

#print axioms outerNext_eq_of_prefixes
#print axioms outerNext_eq_of_complete_streams
#print axioms outerIter_positive_eq_of_complete_streams

end Agent5.OriginalStreamSuccessor
