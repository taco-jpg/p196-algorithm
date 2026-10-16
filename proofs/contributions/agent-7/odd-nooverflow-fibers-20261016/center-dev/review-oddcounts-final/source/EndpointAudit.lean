import OddCounts
import OddActual
open P196.Agent9.InverseFibers
open P196.Agent7.OddFibers

-- Complete exact arithmetic membership follows in both directions.
example (ss : List Symbol) (v : Fin 10) (xs : List Nat) (z : Nat) :
    (xs,z) ∈ oddPreimages ss v 0 ↔ OddActualFiber ss v xs z :=
  (mem_oddPreimages ss v 0 xs z).trans (oddPath_iff_actual ss v xs z)

-- The zero-half-width positive witness remains an actual coefficient-word step.
example : OddActualFiber [] (2 : Fin 10) [] 2 := by
  apply (oddPath_iff_actual [] 2 [] 2).mp
  exact (mem_oddPreimages [] 2 0 [] 2).mp (by decide)

-- An attaining positive exterior example uses the output center twice in pairing.
example : OddActualFiber [11] (0 : Fin 10) [5] 10 := by
  apply (oddPath_iff_actual [11] 0 [5] 10).mp
  exact (mem_oddPreimages [11] 0 0 [5] 10).mp (by decide)

-- Source-center evenness is retained; a source coefficient one is excluded.
example : ¬OddActualFiber [] (1 : Fin 10) [] 1 := by
  simp [OddActualFiber]

#print axioms oddPath_realizes
#print axioms oddRealizes_path
#print axioms oddPath_iff_realizes
#print axioms pair_odd_halves
#print axioms oddMirror_injective
#print axioms oddRealizes_actual
#print axioms oddActual_realizes
#print axioms oddPath_iff_actual
#print axioms oddPath_normalize
#print axioms odd_count_bound
#print axioms odd_preimages_length
#print axioms odd_preimages_bound
#print axioms leading_eleven_odd_sharp
#print axioms leading_eleven_odd_positive
#print axioms odd_preimages_center_parity
