import ArithmeticBridgeK
import BulkTargets

/-! Agent #109 kernel-only replay of `BulkTargets.lean`: identical proofs with
`decide +kernel` in place of the compiler-evaluated decision procedure, over the literal
tables of `BoundaryDataK.lean`. Definitions that do not mention those tables are reused
from the original module. -/

namespace BoundaryCertificateK
open Sofic BoundaryCertificate

set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem bulk_edges_checked : ∀ (family : Fin 2) (phase : Fin 6) (i : Fin 6),
    { src := bulkVertex family phase i.val,
      dst := bulkVertex family phase (i.val+1), lab := bulkWord family phase i.val } ∈ graph0K := by
  decide +kernel

theorem bulk_accepts (family : Fin 2) (phase : Fin 6) (k : Nat) :
    Accepts graph0K (6 * (k+1)) (bulkWord family phase) := by
  refine ⟨by omega, ?_, bulkVertex family phase, ?_, ?_⟩
  · intro i
    simp [bulkWord, Nat.add_mod, Nat.mul_mod]
  · intro i
    simp [bulkVertex, Nat.add_mod, Nat.mul_mod]
  · intro i _
    have h := bulk_edges_checked family phase ⟨i % 6, Nat.mod_lt _ (by decide)⟩
    simpa [bulkVertex, bulkWord, Nat.add_mod, Nat.add_assoc] using h

/-- The finite exterior cannot connect to any of the twelve phase/chirality
targets, for any number of columns and any positive multiple of six temporal
pairs. No arbitrary-width or arbitrary-clock Lychrel conclusion follows. -/

theorem no_bulk_exterior (family : Fin 2) (phase : Fin 6) (k : Nat) :
    ¬ ReverseClosure.Path (ArithmeticColumn (6*(k+1)))
      (fun _ => 41) (bulkWord family phase) :=
  no_arithmetic_exterior (bulk_accepts family phase k)

theorem no_24_phase_bulk_exterior (family : Fin 2) (phase : Fin 6) :
    ¬ ReverseClosure.Path (ArithmeticColumn 12)
      (fun _ => 41) (bulkWord family phase) :=
  no_bulk_exterior family phase 1

theorem exterior_root_encoding : ((0*2+1)*2+1)*11+(7+1) = 41 := by decide

end BoundaryCertificateK
