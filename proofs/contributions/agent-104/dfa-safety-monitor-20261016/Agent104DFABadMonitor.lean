import Agent107DFABoolean
import Lychrel196Research

/-!
# Original bad-language monitor for the finite Boolean DFA

This is an incremental WIP formalization of the four-state monitor used by
`creative_regular_boolean`.  It does not assert that a safe DFA certificate
exists.  The first-symbol and optional-center boundary restrictions are
kept separate from the transition function.
-/

namespace Agent104.DFASafety

/-- Monitor states: low, exceptional, and whether a first pair was read. -/
inductive MonitorState where
  | m0
  | m1
  | m2
  | m3
  deriving DecidableEq, Repr

/-- The exact four-state update from the original learner. -/
def monitorStep : MonitorState → Nat → MonitorState
  | .m0, q => if q ≤ 9 then .m1 else if q = 11 then .m2 else .m3
  | .m1, q => if q ≤ 9 then .m1 else .m3
  | .m2, q => if q = 0 ∨ q = 11 then .m2 else .m3
  | .m3, _ => .m3

/-- The first folded pair is positive; later pair symbols may be zero. -/
def pairAllowed (first : Bool) (q : Nat) : Bool :=
  if first then decide (1 ≤ q ∧ q ≤ 18) else decide (q ≤ 18)

/-- The original learner's center-slot boundary: before any pair, none and
some zero are excluded. For a nonempty word, all valid centers are handled. -/
def terminalApplicable (m : MonitorState) (c : Option Nat) : Bool :=
  match m, c with
  | .m0, none => false
  | .m0, some 0 => false
  | _, _ => true

/-- Bad terminal condition copied from the original learner, with the
initial empty-pair exclusions represented by `terminalApplicable`. -/
def badTerminal (m : MonitorState) (c : Option Nat) : Bool :=
  terminalApplicable m c &&
    ((match m with
      | .m0 => true
      | .m1 => true
      | .m2 => false
      | .m3 => false) &&
      (match c with
       | none => true
       | some v => decide (v ≤ 9))) ||
    (terminalApplicable m c &&
      (match m with
       | .m0 => false
       | .m1 => false
       | .m2 => true
       | .m3 => false) &&
      (match c with
       | none => true
       | some v => decide (v = 0)))

/-- The original finite alphabet maps none to slot 0 and some 0 to slot 1. -/
def centerCode (c : Option Nat) : Nat :=
  match c with
  | none => 0
  | some v => v / 2 + 1

@[simp] theorem centerCode_none : centerCode none = 0 := rfl
@[simp] theorem centerCode_some_zero : centerCode (some 0) = 1 := rfl

/-- Exact truth-table equations, useful when reflecting the monitor into
finite Boolean certificate rows. -/
theorem monitorStep_m0 (q : Nat) :
    monitorStep .m0 q = (if q ≤ 9 then .m1 else if q = 11 then .m2 else .m3) := rfl

theorem monitorStep_m1 (q : Nat) :
    monitorStep .m1 q = (if q ≤ 9 then .m1 else .m3) := rfl

theorem monitorStep_m2 (q : Nat) :
    monitorStep .m2 q = (if q = 0 ∨ q = 11 then .m2 else .m3) := rfl

theorem monitorStep_m3 (q : Nat) : monitorStep .m3 q = .m3 := rfl

/-- Run the monitor from an arbitrary state over a finite list of pair symbols. -/
def runMonitorFrom (start : MonitorState) (symbols : List Nat) : MonitorState :=
  symbols.foldl monitorStep start

def runMonitor (symbols : List Nat) : MonitorState :=
  runMonitorFrom .m0 symbols

def allLow (symbols : List Nat) : Bool :=
  symbols.all (fun q => decide (q ≤ 9))

def allExceptional (symbols : List Nat) : Bool :=
  symbols.all (fun q => decide (q = 0 ∨ q = 11))

@[simp] theorem runMonitorFrom_nil (m : MonitorState) :
    runMonitorFrom m [] = m := rfl

@[simp] theorem runMonitorFrom_cons (m : MonitorState) (q : Nat) (qs : List Nat) :
    runMonitorFrom m (q :: qs) = runMonitorFrom (monitorStep m q) qs := rfl

theorem runMonitorFrom_append (m : MonitorState) (xs ys : List Nat) :
    runMonitorFrom m (xs ++ ys) = runMonitorFrom (runMonitorFrom m xs) ys := by
  simp [runMonitorFrom, List.foldl_append]

@[simp] theorem runMonitorFrom_m3 (symbols : List Nat) :
    runMonitorFrom .m3 symbols = .m3 := by
  induction symbols with
  | nil => rfl
  | cons q qs ih =>
      simp [runMonitorFrom_cons, monitorStep, ih]

theorem runMonitorFrom_m1_not_m2 (symbols : List Nat) :
    runMonitorFrom .m1 symbols ≠ .m2 := by
  induction symbols with
  | nil => simp [runMonitorFrom]
  | cons q qs ih =>
      by_cases hq : q ≤ 9
      · simpa [runMonitorFrom_cons, monitorStep, hq] using ih
      · simp [runMonitorFrom_cons, monitorStep, hq, runMonitorFrom_m3]

theorem runMonitorFrom_m2_not_m1 (symbols : List Nat) :
    runMonitorFrom .m2 symbols ≠ .m1 := by
  induction symbols with
  | nil => simp [runMonitorFrom]
  | cons q qs ih =>
      by_cases hq : q = 0 ∨ q = 11
      · simpa [runMonitorFrom_cons, monitorStep, hq] using ih
      · simp [runMonitorFrom_cons, monitorStep, hq, runMonitorFrom_m3]

theorem runMonitorFrom_m1_iff_allLow (symbols : List Nat) :
    runMonitorFrom .m1 symbols = .m1 ↔ allLow symbols = true := by
  induction symbols with
  | nil => simp [runMonitorFrom, allLow]
  | cons q qs ih =>
      by_cases hq : q ≤ 9
      · simp [runMonitorFrom_cons, monitorStep, allLow, hq, ih]
      · simp [runMonitorFrom_cons, monitorStep, allLow, hq, runMonitorFrom_m3]

theorem runMonitorFrom_m2_iff_allExceptional (symbols : List Nat) :
    runMonitorFrom .m2 symbols = .m2 ↔ allExceptional symbols = true := by
  induction symbols with
  | nil => simp [runMonitorFrom, allExceptional]
  | cons q qs ih =>
      by_cases hq : q = 0 ∨ q = 11
      · simp [runMonitorFrom_cons, monitorStep, allExceptional, hq, ih]
      · simp [runMonitorFrom_cons, monitorStep, allExceptional, hq, runMonitorFrom_m3]

theorem runMonitor_cons_m1 (q : Nat) (qs : List Nat) :
    runMonitor (q :: qs) = .m1 ↔ q ≤ 9 ∧ allLow qs = true := by
  unfold runMonitor
  rw [runMonitorFrom_cons]
  by_cases hq : q ≤ 9
  · simp [monitorStep, hq, runMonitorFrom_m1_iff_allLow, runMonitorFrom_m1_not_m2]
  · by_cases h11 : q = 11
    · simp [monitorStep, hq, h11, runMonitorFrom_m2_iff_allExceptional, runMonitorFrom_m2_not_m1]
    · simp [monitorStep, hq, h11, runMonitorFrom_m3]

theorem runMonitor_cons_m2 (q : Nat) (qs : List Nat) :
    runMonitor (q :: qs) = .m2 ↔ q = 11 ∧ allExceptional qs = true := by
  unfold runMonitor
  rw [runMonitorFrom_cons]
  by_cases hq : q ≤ 9
  · simp [monitorStep, hq, runMonitorFrom_m1_iff_allLow]
  · by_cases h11 : q = 11
    · simp [monitorStep, hq, h11, runMonitorFrom_m2_iff_allExceptional]
    · simp [monitorStep, hq, h11, runMonitorFrom_m3]

/-- Finite monitor alphabet and all valid optional center symbols. -/
def monitorStates : List MonitorState := [.m0, .m1, .m2, .m3]

def pairSymbols : List (Fin 19) := List.finRange 19

def centerSymbols : List (Option Nat) :=
  none :: (List.range 10).map (fun k => some (2 * k))

/-- Check the initial product state, every monitor/DFA transition implication,
and rejection of every bad terminal center. This is a finite Boolean
certificate predicate; its soundness theorem is a separate WIP obligation. -/
def checkSafetyRows {N : Nat} (B : Agent107.FoldedDFA.Encoding.BooleanDFA N)
    (raw : Fin N → MonitorState → Bool) : Bool :=
  let starts := raw B.zero .m0
  let transitions :=
    (List.finRange N).all fun a =>
      monitorStates.all fun m =>
        pairSymbols.all fun q =>
          if pairAllowed (m == .m0) q.val then
            (List.finRange N).all fun b =>
              Agent107.FoldedDFA.boolImplies
                (raw a m && B.d a q b)
                (raw b (monitorStep m q.val))
          else true
  let terminals :=
    (List.finRange N).all fun a =>
      monitorStates.all fun m =>
        centerSymbols.all fun c =>
          Agent107.FoldedDFA.boolImplies
            (raw a m && badTerminal m c)
            (!(B.toDFA.final a c))
  starts && transitions && terminals

/-- Exact universal target: on admissible symmetric words, the monitor's
terminal rejection predicate agrees with the original two-branch BadWord
definition. This is a target, not yet a proved theorem. -/
def monitorBadWordCorrespondence : Prop :=
  ∀ L (q : Nat → Nat), FoldedDecimal.Admissible L q →
    (badTerminal
      (runMonitor (List.ofFn (fun i : Fin (L / 2) => q i.val)))
      (Agent107.FoldedTransducer.inputCenter L q) = true
      ↔ FoldedDecimal.BadWord L q)

/-- Exact safety target: finite safety rows plus one-hot transition rows
exclude BadWord for every accepted original folded prefix. This proposition
is intentionally left as a target until the reflection and path-induction
proofs are complete. -/
def safetyRowsSound : Prop :=
  ∀ {N : Nat} (B : Agent107.FoldedDFA.Encoding.BooleanDFA N)
      (raw : Fin N → MonitorState → Bool),
    checkSafetyRows B raw = true →
    B.OneHot →
    ∀ L (q : Nat → Nat), FoldedDecimal.Admissible L q →
      B.toDFA.accepts (Agent107.FoldedTransducer.foldPrefix L q) →
      ¬ FoldedDecimal.BadWord L q

end Agent104.DFASafety

#print axioms Agent104.DFASafety.centerCode_none
#print axioms Agent104.DFASafety.centerCode_some_zero
#print axioms Agent104.DFASafety.monitorStep_m0
#print axioms Agent104.DFASafety.monitorStep_m1
#print axioms Agent104.DFASafety.monitorStep_m2
#print axioms Agent104.DFASafety.monitorStep_m3
