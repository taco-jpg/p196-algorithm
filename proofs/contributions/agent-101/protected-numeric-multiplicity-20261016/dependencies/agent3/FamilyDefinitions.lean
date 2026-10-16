import ActualWordBridge

/-!
Agent #3: the finite-horizon overflow family from the preserved
`persist_inverse_fibers_proof.txt`, final section. This module only defines
the exact words; subsequent modules establish their properties.

The underlying decimal operation is the unchanged `Agent8.stepWord`.
Coefficients are mirrored digit sums, not individual decimal digits.
-/

namespace P196.Agent3.OverflowHorizon

open Agent8

def choice (b : Bool) : Nat := if b then 14 else 5

def inputHalf (xs : List Bool) (k : Nat) : Word :=
  [14] ++ xs.map choice ++ List.replicate k 18

def inputWord (xs : List Bool) (k : Nat) : Word :=
  inputHalf xs k ++ (inputHalf xs k).reverse

def target (m k : Nat) : Word :=
  [5] ++ List.replicate m 10 ++ [14] ++ List.replicate (2 * k - 1) 18 ++
    [14] ++ List.replicate m 10 ++ [5]

end P196.Agent3.OverflowHorizon
