import InverseFibers

/-!
Agent #3: the finite two-layer inverse certificate from the preserved
astra_counting_safe_image_fibers.txt. Arithmetic validity is expressed
using the unchanged P196.Agent9.InverseFibers.Local relation.

Written source blob: 30f8ed333edb2e11402569c62d50def2451ffef4.
Exact table generator blob: 7d11de894bf492ad4134c591a1929fd1611c49c3.
Original snapshot: 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5.
Agent #9's imported InverseFibers source blob:
cade8ace6359fe8246a29ec781859e3a39b00e11.
The literal tables below are checked against Local by ordinary decide;
the generator is not part of the logical trusted base.
-/
namespace P196.Agent3.TwoHistory

open P196.Agent9.InverseFibers

abbrev Joint := State × State

def symbol (b : Bool) : Symbol := if b then 14 else 5

private def jointData (b : Bool) (j : Joint) : Joint × Symbol × Symbol :=
  match b, j.1.val, j.2.val with
  | false, 0, 0 => ((1, 0), 2, 1)
  | false, 0, 1 => ((1, 2), 2, 11)
  | false, 0, 2 => ((1, 1), 2, 0)
  | false, 0, 3 => ((1, 3), 2, 10)
  | false, 1, 0 => ((3, 0), 12, 6)
  | false, 1, 1 => ((3, 2), 12, 16)
  | false, 1, 2 => ((3, 1), 12, 5)
  | false, 1, 3 => ((3, 3), 12, 15)
  | false, 2, 0 => ((0, 0), 2, 1)
  | false, 2, 1 => ((0, 2), 2, 11)
  | false, 2, 2 => ((0, 1), 2, 0)
  | false, 2, 3 => ((0, 3), 2, 10)
  | false, 3, 0 => ((2, 0), 12, 6)
  | false, 3, 1 => ((2, 2), 12, 16)
  | false, 3, 2 => ((2, 1), 12, 5)
  | false, 3, 3 => ((2, 3), 12, 15)
  | true, 0, 0 => ((0, 1), 7, 3)
  | true, 0, 1 => ((0, 3), 7, 13)
  | true, 0, 2 => ((0, 0), 7, 3)
  | true, 0, 3 => ((0, 2), 7, 13)
  | true, 1, 0 => ((2, 1), 17, 8)
  | true, 1, 1 => ((2, 3), 17, 18)
  | true, 1, 2 => ((2, 0), 17, 8)
  | true, 1, 3 => ((2, 2), 17, 18)
  | true, 2, 0 => ((1, 0), 6, 3)
  | true, 2, 1 => ((1, 2), 6, 13)
  | true, 2, 2 => ((1, 1), 6, 2)
  | true, 2, 3 => ((1, 3), 6, 12)
  | true, 3, 0 => ((3, 0), 16, 8)
  | true, 3, 1 => ((3, 2), 16, 18)
  | true, 3, 2 => ((3, 1), 16, 7)
  | true, 3, 3 => ((3, 3), 16, 17)
  | _, _, _ => ((0, 0), 0, 0)

def jointStep (b : Bool) (j : Joint) : Joint := (jointData b j).1

def emit1 (b : Bool) (j : Joint) : Symbol := (jointData b j).2.1

def emit0 (b : Bool) (j : Joint) : Symbol := (jointData b j).2.2

def runStates : Joint → List Bool → Joint
  | j, [] => j
  | j, b :: bs => runStates (jointStep b j) bs

def firstLabels : Joint → List Bool → List Symbol
  | _, [] => []
  | j, b :: bs => emit1 b j :: firstLabels (jointStep b j) bs

def secondLabels : Joint → List Bool → List Symbol
  | _, [] => []
  | j, b :: bs => emit0 b j :: secondLabels (jointStep b j) bs

def correction (j : Joint) : List Bool :=
  match j.1.val, j.2.val with
  | 0, 0 => [true, true, false, false, true, true]
  | 0, 1 => [true, false, false, true, true, true]
  | 0, 2 => [false, true, true, false, true, true]
  | 0, 3 => [false, false, true, true, true, true]
  | 1, 0 => [true, false, false, true, true, false]
  | 1, 1 => [true, true, false, true, true, true]
  | 1, 2 => [false, false, false, true, false, false]
  | 1, 3 => [false, true, true, true, true, true]
  | 2, 0 => [false, true, true, false, false, true]
  | 2, 1 => [false, false, true, true, false, true]
  | 2, 2 => [false, true, false, false, true, true]
  | 2, 3 => [true, false, true, true, true, true]
  | 3, 0 => [false, false, true, true, false, false]
  | 3, 1 => [false, false, true, false, false, true]
  | 3, 2 => [false, false, false, true, true, false]
  | 3, 3 => [true, true, true, true, true, true]
  | _, _ => [true, true, true, true, true, true]

theorem symbol_false : symbol false = 5 := rfl

theorem symbol_true : symbol true = 14 := rfl

/-- First predecessor layer: every table row satisfies the original
decimal carry equations. The finite proof is reduced by the kernel. -/
theorem local_emit1 : ∀ b : Bool, ∀ j : Joint,
    Local (symbol b) j.1 (jointStep b j).1 (emit1 b j).val := by
  intro b ⟨p, q⟩
  have h : ∀ b : Bool, ∀ p q : State,
      Local (symbol b) p (jointStep b (p, q)).1 (emit1 b (p, q)).val := by decide
  exact h b p q

/-- Second predecessor layer, targeting the first emitted coefficient. -/
theorem local_emit0 : ∀ b : Bool, ∀ j : Joint,
    Local (emit1 b j) j.2 (jointStep b j).2 (emit0 b j).val := by
  intro b ⟨p, q⟩
  have h : ∀ b : Bool, ∀ p q : State,
      Local (emit1 b (p, q)) q (jointStep b (p, q)).2 (emit0 b (p, q)).val := by decide
  exact h b p q

theorem correction_length : ∀ j : Joint, (correction j).length = 6 := by
  intro ⟨p, q⟩
  have h : ∀ p q : State, (correction (p, q)).length = 6 := by decide
  exact h p q

/-- Every six-symbol correction ends with both carry pairs equal to11. -/
theorem correction_closes : ∀ j : Joint,
    runStates j (correction j) = (3, 3) := by
  intro ⟨p, q⟩
  have h : ∀ p q : State, runStates (p, q) (correction (p, q)) = (3, 3) := by decide
  exact h p q

theorem initial_step : jointStep true (0, 0) = (0, 1) := by decide

theorem initial_emit1 : emit1 true (0, 0) = 7 := by decide

theorem initial_emit0 : emit0 true (0, 0) = 3 := by decide

/-- At the matching inner state, a target18 emits18 and stays at11.
The same original Local identity applies independently in both layers. -/
theorem local_eighteen : Local 18 3 3 18 := by decide

#print axioms Joint
#print axioms symbol
#print axioms jointData
#print axioms jointStep
#print axioms emit1
#print axioms emit0
#print axioms runStates
#print axioms firstLabels
#print axioms secondLabels
#print axioms correction
#print axioms symbol_false
#print axioms symbol_true
#print axioms local_emit1
#print axioms local_emit0
#print axioms correction_length
#print axioms correction_closes
#print axioms initial_step
#print axioms initial_emit1
#print axioms initial_emit0
#print axioms local_eighteen

end P196.Agent3.TwoHistory
