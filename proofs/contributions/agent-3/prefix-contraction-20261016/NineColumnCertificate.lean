import PrefixMachine
import BinaryBlockCounts

/-!
WIP formalization of the regenerated clock=(0,0,0), y=5 rejecting-block
certificate. The table is generated from the preserved local transition
algorithm and computationally cross-checked against PrefixMachine's
nextCarry/emitted/machineStep equations. This source has NOT been compiled
in this environment. Do not treat it as an accepted theorem until a pinned
Lean 4.19.0 --trust=0 build and axiom audit pass.
-/

namespace P196.Agent3.PrefixContraction

open P196.Agent9.InverseFibers

set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

/-- For each original carry triple, a Boolean continuation that rejects it.
false encodes coefficient 5 and true encodes coefficient 14. -/
def regeneratedRejectingWords : List (Triple × List Bool) := [
  ((0, 1, 1), [true, true, false]),
  ((1, 2, 3), [false, true, false, false, false]),
  ((0, 3, 3), [true, false]),
  ((3, 1, 2), [true, false, false, false]),
  ((2, 0, 3), [true, false, false, false, true, true, true, false]),
  ((1, 3, 3), [true, false, true, false, true]),
  ((0, 2, 2), [false]),
  ((2, 2, 1), [false, false, false, true]),
  ((3, 2, 1), [false, false, false]),
  ((0, 0, 2), [true, false, true, false, true, true, true, false]),
  ((1, 0, 2), [false, false, false, true, true, true, false]),
  ((3, 3, 2), [true, false, false, false, true]),
  ((2, 2, 3), [false, true, false, true]),
  ((0, 0, 0), [true, true, true, false]),
  ((0, 1, 2), [false, false, true]),
  ((1, 1, 2), [false, false, false, false]),
  ((2, 1, 3), [false, false]),
  ((3, 1, 3), [true, false, true, false, true]),
  ((1, 0, 0), [true, false, false, false, false, false, false]),
  ((0, 1, 0), [false, true, false, true, true, true, false]),
  ((3, 0, 1), [false, false, true, true, true, false]),
  ((2, 1, 1), [false, false, true, false, true, false]),
  ((2, 3, 0), [true, false, false, false, true, false]),
  ((3, 3, 0), [false, false, false, true]),
  ((0, 1, 3), [true, false, true]),
  ((1, 1, 3), [true, false, true, false]),
  ((1, 0, 1), [true, true, false, true]),
  ((1, 2, 0), [false, true]),
  ((0, 3, 0), [false, false, false, false, true, false]),
  ((2, 3, 1), [false, false, true]),
  ((1, 2, 2), [false, true, true, true]),
  ((3, 2, 3), [false, true, false, true]),
  ((3, 0, 0), [false, false, false, true, false, false]),
  ((2, 1, 0), [false, false, false, false, false, false]),
  ((1, 2, 1), [true, false, true, true, true, false]),
  ((0, 3, 1), [true, false, true, false, true, false]),
  ((2, 0, 2), [false, true, true, true, false]),
  ((3, 0, 2), [false, true, true, false, false]),
  ((0, 2, 3), [false, true, false, true, false]),
  ((1, 3, 0), [false, false, false, true, false]),
  ((3, 3, 1), [false, false, true, false]),
  ((0, 3, 2), [false, true]),
  ((2, 3, 3), [false, true, false]),
  ((2, 1, 2), [true, false, true]),
  ((3, 1, 1), [true]),
  ((2, 0, 0), [false, false, true, false, false]),
  ((0, 2, 1), [false, false, false, false, false]),
  ((1, 3, 2), [true, false, false, false, true]),
  ((3, 1, 0), [true, true, true]),
  ((2, 0, 1), [true, true, false, false]),
  ((2, 2, 0), [true, false, true, true]),
  ((3, 3, 3), [false, true, true]),
  ((1, 3, 1), [true]),
  ((0, 2, 0), [false, false, true, true]),
  ((2, 2, 2), [false]),
  ((0, 0, 1), [false, true, false, false]),
  ((0, 0, 3), [true, false, false, true]),
  ((3, 2, 0), [true, true]),
  ((1, 0, 3), [true, false, false]),
  ((1, 1, 0), [false, true, true]),
  ((2, 3, 2), [true, true]),
  ((1, 1, 1), [true]),
  ((3, 0, 3), [false, true, false, false, false, true, true, true, false]),
  ((3, 2, 2), [true, true, true, true])
]

/-- Look up the finite witness for a carry triple. -/
def regeneratedWitness (p : Triple) : List Bool :=
  ((regeneratedRejectingWords.find? (fun e => decide (e.1 = p))).map Prod.snd).getD []

/-- The table covers every one of the 64 original carry triples exactly once. -/
theorem regeneratedRejectingWords_nodup :
    regeneratedRejectingWords.Nodup := by
  decide

/-- Every triple has a listed continuation of length at most nine that reaches
the absorbing empty state of the exact original-local prefix machine. -/
theorem regeneratedWitness_rejects_all :
    ∀ a b c : State,
      (regeneratedWitness (a, b, c)).length ≤ 9 ∧
        prefixRun (some (a, b, c)) (regeneratedWitness (a, b, c)) = none := by
  decide

theorem regeneratedWitness_rejects (p : Triple) :
    (regeneratedWitness p).length ≤ 9 ∧
      prefixRun (some p) (regeneratedWitness p) = none := by
  rcases p with ⟨a, b, c⟩
  exact regeneratedWitness_rejects_all a b c

#print axioms regeneratedRejectingWords_nodup
#print axioms regeneratedWitness_rejects_all
#print axioms regeneratedWitness_rejects

/-- Extend every finite rejecting witness to a common block length nine.
The absorbing state remains rejecting under every padding symbol. -/
def paddedRejectingWitness (q : Option Triple) : List Bool :=
  match q with
  | none => List.replicate 9 false
  | some p =>
      regeneratedWitness p ++ List.replicate (9 - (regeneratedWitness p).length) false

theorem paddedRejectingWitness_length (q : Option Triple) :
    (paddedRejectingWitness q).length = 9 := by
  cases q with
  | none => simp [paddedRejectingWitness]
  | some p =>
      obtain ⟨hlen, _⟩ := regeneratedWitness_rejects p
      simp [paddedRejectingWitness, List.length_append]
      omega

theorem paddedRejectingWitness_rejects (q : Option Triple) :
    prefixRun q (paddedRejectingWitness q) = none := by
  cases q with
  | none => simp [paddedRejectingWitness, prefixRun, advance_none]
  | some p =>
      obtain ⟨_, hrun⟩ := regeneratedWitness_rejects p
      simp [paddedRejectingWitness, prefixRun, List.foldl_append, hrun, advance_none]

/-- The regenerated certificate supplies the exact uniform nine-symbol
rejection premise required by the generic binary block-count theorem. -/
theorem paddedRejectingWitness_uniform :
    ∀ q : Option Triple,
      ∃ bits : List Bool,
        bits.length = 9 ∧
          BinaryCount.runBits advance q bits = none := by
  intro q
  refine ⟨paddedRejectingWitness q, paddedRejectingWitness_length q, ?_⟩
  simpa [BinaryCount.runBits, prefixRun] using paddedRejectingWitness_rejects q

/-- Conditional-to-concrete count specialization: at most 511 survivors per
nine-symbol block, once the finite certificate checks in Lean. -/
theorem survivorCount_div_mod_511 (q : Option Triple) (n : Nat) :
    BinaryCount.survivorCount advance none q n ≤
      511 ^ (n / 9) * 2 ^ (n % 9) := by
  have h := BinaryCount.survivorCount_div_mod advance none
    (fun b => advance_none b) 9 paddedRejectingWitness_uniform q n
  simpa only [show 2 ^ 9 - 1 = 511 by decide] using h

#print axioms paddedRejectingWitness_length
#print axioms paddedRejectingWitness_rejects
#print axioms paddedRejectingWitness_uniform
#print axioms survivorCount_div_mod_511

end P196.Agent3.PrefixContraction
