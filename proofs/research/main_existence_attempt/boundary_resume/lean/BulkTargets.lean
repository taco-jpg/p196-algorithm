import ArithmeticBridge

/-!
Concrete target coverage: the two primitive six-slot cut words and all six
rotations of each. In particular k=1 gives the 12-slot/24-phase exterior.
-/

namespace BoundaryCertificate
open Sofic

def bulkLetters (family : Fin 2) : Array Nat :=
  if family.val = 0 then #[80, 31, 62, 25, 56, 7] else #[56, 25, 62, 31, 80, 7]

def bulkWord (family : Fin 2) (phase : Fin 6) : Word :=
  fun i => (bulkLetters family)[(i + phase.val) % 6]!

def bulkVertex (family : Fin 2) (phase : Fin 6) : Nat → Nat :=
  fun i => family.val * 6 + (i + phase.val) % 6

theorem bulk_edges_checked : ∀ (family : Fin 2) (phase : Fin 6) (i : Fin 6),
    { src := bulkVertex family phase i.val,
      dst := bulkVertex family phase (i.val+1), lab := bulkWord family phase i.val } ∈ graph0 := by
  native_decide

theorem bulk_accepts (family : Fin 2) (phase : Fin 6) (k : Nat) :
    Accepts graph0 (6 * (k+1)) (bulkWord family phase) := by
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

#print axioms bulk_edges_checked
#print axioms no_bulk_exterior
#print axioms no_24_phase_bulk_exterior

end BoundaryCertificate
