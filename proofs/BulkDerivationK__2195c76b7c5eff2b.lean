import BulkTargetsK
import BulkDerivation

/-! Agent #109 kernel-only replay of `BulkDerivation.lean`: identical proofs with
`decide +kernel` in place of the compiler-evaluated decision procedure, over the literal
tables of `BoundaryDataK.lean`. Definitions that do not mention those tables are reused
from the original module. -/

namespace BoundaryCertificateK
open Sofic BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0


theorem bulk_cycles_checked : ∀ t : Fin 12,
    (List.range 24).foldl (fun q j => step3 q (j%2)) bulkInputs[t.val]! = bulkInputs[t.val]! := by
  decide +kernel

theorem derived_targets_checked : ∀ (t : Fin 12) (i : Fin 12),
    (cutWord t)[i.val]! =
      bulkWord (bulkAssignment[t.val]!).1 (bulkAssignment[t.val]!).2 i.val := by
  decide +kernel

theorem derived_target_eq (t : Fin 12) :
    derivedBulkWord t = bulkWord (bulkAssignment[t.val]!).1 (bulkAssignment[t.val]!).2 := by
  funext i
  have h := derived_targets_checked t ⟨i % 12, Nat.mod_lt _ (by decide)⟩
  have hmod : (i % 12 + (bulkAssignment[t.val]!).2.val) % 6 =
      (i + (bulkAssignment[t.val]!).2.val) % 6 := by omega
  simpa only [derivedBulkWord, bulkWord, hmod] using h

/-- All twelve permutations of (9,3,6) and (9,12,15), every spatial width,
and every positive period that is a multiple of six temporal pairs. -/

theorem no_936_or_9_12_15_exterior (t : Fin 12) (k : Nat) :
    ¬ ReverseClosure.Path (ArithmeticColumn (6*(k+1)))
      (fun _ => 41) (derivedBulkWord t) := by
  rw [derived_target_eq]
  exact no_bulk_exterior _ _ k

theorem no_24_phase_936_or_9_12_15_exterior (t : Fin 12) :
    ¬ ReverseClosure.Path (ArithmeticColumn 12)
      (fun _ => 41) (derivedBulkWord t) :=
  no_936_or_9_12_15_exterior t 1

end BoundaryCertificateK
