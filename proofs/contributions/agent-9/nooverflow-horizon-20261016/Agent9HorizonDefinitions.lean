import SharpMaximum

/-!
Agent #9: the protected no-overflow family in the final section of
persist_inverse_fibers_proof.txt (source 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5).
The existing exact arithmetic inverse enumerator is reused without changes.
-/

namespace P196.Agent9.NoOverflowHorizon

open InverseFibers

/-- Target half: a leading eleven, a freely growing neutral block, then the
finite central reservoir. Parameters count coefficients, not decimal powers. -/
def targetHalf (m k : Nat) : List Symbol :=
  11 :: (List.replicate m 9 ++ List.replicate k 18)

/-- The complete even symmetric target coefficient word. -/
def targetWord (m k : Nat) : List Nat :=
  mirror ((targetHalf m k).map Fin.val)

/-- The complete, duplicate-free actual no-overflow fiber. -/
def inputWords (m k : Nat) : List (List Nat) :=
  fullPreimages (targetHalf m k)

end P196.Agent9.NoOverflowHorizon
