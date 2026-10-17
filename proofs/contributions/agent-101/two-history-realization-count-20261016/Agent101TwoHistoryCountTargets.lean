import Agent101NumericFibers
import HistoryFamily

/-!
WIP specification for Agent #101's weighted ordinary-integer realization count.
This module is deliberately outside the accepted verifier registry until the
proofs and exact dependency closure are compiled under the pinned Lean runtime.
It does not re-prove the inherited two-history word or finite-safety theorem.
-/ 

namespace Agent101.TwoHistoryCount

open Agent101
open P196.Agent3.OverflowHorizon
open P196.Agent3.TwoHistory

/-- Complete ordinary-integer realization union for the original two-history
initial family. Each profile contributes every digit split, not one witness. -/
def twoHistorySeeds (m k : Nat) : List Nat :=
  (allBits m).flatMap fun xs => numericFiber (historyHalf0 xs k) none

/-- Number of low/high decimal splits emitted by one original transition. -/
def localWeight (b : Bool) (j : Joint) : Nat :=
  pairCount false (emit0 b j).val

/-- Multiplicity of the original state-dependent six-bit correction. -/
def correctionWeight (j : Joint) : Nat :=
  natProduct ((secondLabels j (correction j)).map
    fun s => pairCount false s.val)

/-- Multiplicity of the free Boolean word followed by its original
state-dependent correction, before multiplying the fixed leading outer pair. -/
def profileWeight (xs : List Bool) (j : Joint) : Nat :=
  natProduct ((secondLabels j (xs ++ correction (runStates j xs))).map
    fun s => pairCount false s.val)

/-- One transition contributes its actual emitted low/high split count, then
continues at the exact original joint state. -/
def profileWeightConsTarget (b : Bool) (xs : List Bool) (j : Joint) : Prop :=
  profileWeight (b :: xs) j =
    localWeight b j * profileWeight xs (jointStep b j)

/-- The state recurrence must equal the sum of profile multiplicities over
all Boolean words of the requested length. -/
def stateWeightSumTarget (m : Nat) (j : Joint) : Prop :=
  stateWeight m j = natProduct [] * 0 +
    ((allBits m).map fun xs => profileWeight xs j).foldl (fun acc x => acc + x) 0

/-- Exact weighted recurrence over the original four-by-four joint state.
No state-independent replacement for the six-bit correction is permitted. -/
def stateWeight : Nat → Joint → Nat
  | 0, j => correctionWeight j
  | n + 1, j =>
      localWeight false j * stateWeight n (jointStep false j) +
      localWeight true j * stateWeight n (jointStep true j)

/-- Target: the flattened list is exactly the union of all original ordinary
integer realizations of the initial words, with no omissions or duplicates. -/
def completeRealizationTarget (m k : Nat) : Prop :=
  ∀ n, n ∈ twoHistorySeeds m k ↔
    ∃ xs : List Bool, xs.length = m ∧
      IntegerRealizes n (historyWord0 xs k)

/-- Target: all counted integers are positive and have the exact original
decimal width 2*(m+k+7), inherited from the canonical coefficient words. -/
def realizationWidthTarget (m k : Nat) : Prop :=
  ∀ n, n ∈ twoHistorySeeds m k →
    0 < n ∧ decimalWidth n (2 * (m + k + 7))

/-- Target: the complete integer union has no duplicates, including across
distinct coefficient profiles. Per-profile Nodup alone is insufficient. -/
def realizationNodupTarget (m k : Nat) : Prop :=
  (twoHistorySeeds m k).Nodup

/-- Target: exact ordinary-integer multiplicity. The initial outer pair sum
is 3, giving the factor three; the remaining choices are state-weighted. -/
def exactWeightedCountTarget (m k : Nat) : Prop :=
  (twoHistorySeeds m k).length = 3 * stateWeight m (0, 1)

/-- The original PR91 package already supplies this finite-time property for
each integer realizing each history word. This target only transports it to
the complete counted union; it is not an infinite-time or 196 conclusion. -/
def finiteSafetyTarget (m k : Nat) : Prop :=
  ∀ n, n ∈ twoHistorySeeds m k →
    0 < n ∧
    (∀ t, t ≤ k + 3 → ¬ Palindrome (orbit n t)) ∧
    orbit n 4 = digitValue (target (m + 6) k)

/-- All members share the same original numeric time-four value, as in PR91. -/
def commonTimeFourTarget (m k : Nat) : Prop :=
  ∀ n, n ∈ twoHistorySeeds m k →
    orbit n 4 = digitValue (target (m + 6) k)

end Agent101.TwoHistoryCount
