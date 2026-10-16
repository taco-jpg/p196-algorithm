import BulkTargets

/-!
Finite decimal-arithmetic derivation of all twelve bulk cut words. The
nearest-non-nine carries below inspect the three sites of the periodic bulk.
Each of the twelve specified inputs is replayed through all 24 phases.
-/

namespace BoundaryCertificate
open Sofic

def bulkInputs : Array (Array Nat) := #[
  #[9,3,6], #[9,6,3], #[3,9,6], #[3,6,9], #[6,9,3], #[6,3,9],
  #[9,12,15], #[9,15,12], #[12,9,15], #[12,15,9], #[15,9,12], #[15,12,9]]

/-- Direction one is forward; direction two is backward modulo three. -/
def carry3 (q : Array Nat) (i direction : Nat) : Nat :=
  let j := (i + direction) % 3
  let k := (i + 2*direction) % 3
  if q[j]! != 9 then q[j]! / 10
  else if q[k]! != 9 then q[k]! / 10
  else q[i % 3]! / 10

def step3 (q : Array Nat) (overflow : Nat) : Array Nat :=
  (List.range 3).toArray.map fun i =>
    let j := (i + 3 - overflow) % 3
    (q[i]! + carry3 q i 2) % 10 + (q[j]! + carry3 q j 1) % 10

def pairLetter (q : Array Nat) : Nat :=
  let a := carry3 q 0 2
  let c := (q[0]! + carry3 q 0 1) / 10
  let odd := step3 q 0
  let b := carry3 odd 0 2
  let zPlusOne := odd[2]! + 1 - 10 * ((odd[2]! + carry3 odd 2 1) / 10)
  ((a*2+b)*2+c)*11+zPlusOne

def cutAux : Nat → Array Nat → List Nat
  | 0, _ => []
  | k+1, q => pairLetter q :: cutAux k (step3 (step3 q 0) 1)

def cutWord (t : Fin 12) : Array Nat := (cutAux 12 bulkInputs[t.val]!).toArray

def derivedBulkWord (t : Fin 12) : Word := fun i => (cutWord t)[i % 12]!

def bulkAssignment : Array (Fin 2 × Fin 6) :=
  #[(0,3), (1,5), (1,1), (0,1), (0,5), (1,3),
    (0,0), (1,2), (1,4), (0,4), (0,2), (1,0)]

theorem bulk_cycles_checked : ∀ t : Fin 12,
    (List.range 24).foldl (fun q j => step3 q (j%2)) bulkInputs[t.val]! = bulkInputs[t.val]! := by
  native_decide

theorem derived_targets_checked : ∀ (t : Fin 12) (i : Fin 12),
    (cutWord t)[i.val]! =
      bulkWord (bulkAssignment[t.val]!).1 (bulkAssignment[t.val]!).2 i.val := by
  native_decide

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

#print axioms bulk_cycles_checked
#print axioms derived_targets_checked
#print axioms no_936_or_9_12_15_exterior
#print axioms no_24_phase_936_or_9_12_15_exterior

end BoundaryCertificate
