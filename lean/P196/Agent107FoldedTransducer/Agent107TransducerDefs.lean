import P196.Foundations.LychrelDigitSums

/-!
Agent #107: the literal finite folded carry transducer.

The original Python state is `(overflow, low, high, delay, started)`.
The Int delay retains its actual -1 sentinel in the no-overflow branch.
Only the finite prefix through `L / 2` is part of a complete path.
Original algorithms: creative_regular_direct blob
5658e577de22431ee029cf49c2ff640321dc0d8a and
persist_spacetime_weighted blob 8274715ce60ab084b602a08184ed909ee41a1f28.
-/

namespace Agent107.FoldedTransducer

open DecimalDigits FoldedDecimal

structure State where
  overflow : Nat
  low : Nat
  high : Nat
  delay : Int
  started : Bool
  deriving DecidableEq, Repr

def initial (h : Nat) : State :=
  ⟨h, 0, h, if h = 0 then -1 else 1, false⟩

def nextState (s : State) (q b : Nat) : State :=
  ⟨s.overflow, (q + s.low) / 10, b,
    if s.overflow = 0 then -1 else Int.ofNat ((q + b) % 10), true⟩

def emit (s : State) (q b : Nat) : Nat :=
  if s.overflow = 0 then (q + s.low) % 10 + (q + b) % 10
  else (q + s.low) % 10 + s.delay.toNat

def Transition (s : State) (q : Nat) (t : State) : Prop :=
  q ≤ 18 ∧ (s.started = false → 0 < q) ∧ t.high ≤ 1 ∧
    (q + t.high) / 10 = s.high ∧ t = nextState s q t.high

instance (s : State) (q : Nat) (t : State) : Decidable (Transition s q t) := by
  unfold Transition
  infer_instance

def Terminal (s : State) (c : Option Nat) : Prop :=
  (s.started = true ∨ 0 < c.getD 0) ∧
    match c with
    | none => s.low = s.high
    | some v => v ≤ 18 ∧ v % 2 = 0 ∧ (v + s.low) / 10 = s.high

instance (s : State) (c : Option Nat) : Decidable (Terminal s c) := by
  unfold Terminal
  cases c <;> infer_instance

def terminalExtra (s : State) (c : Option Nat) : Option Nat :=
  if s.overflow = 0 then none
  else c.map (fun v => (v + s.low) % 10 + s.delay.toNat)

def terminalCenter (s : State) (c : Option Nat) : Option Nat :=
  if s.overflow = 0 then c.map (fun v => 2 * ((v + s.low) % 10))
  else match c with
    | none => some (2 * s.delay.toNat)
    | some _ => none

def inputCenter (L : Nat) (q : Nat → Nat) : Option Nat :=
  if L % 2 = 0 then none else some (q (L / 2))

def Accepts (L : Nat) (q : Nat → Nat) (p : Nat → State) : Prop :=
  (∃ h, h ≤ 1 ∧ p 0 = initial h) ∧
  (∀ i, i < L / 2 → Transition (p i) (q i) (p (i + 1))) ∧
  Terminal (p (L / 2)) (inputCenter L q)

def actualState (L : Nat) (q : Nat → Nat) (i : Nat) : State :=
  ⟨carry q L, carry q i, carry q (L - i),
    if carry q L = 0 then -1 else Int.ofNat (extended q L (L - i)),
    decide (0 < i)⟩

structure Word where
  pairs : List Nat
  center : Option Nat
  deriving DecidableEq, Repr

def foldPrefix (L : Nat) (q : Nat → Nat) : Word :=
  ⟨List.ofFn (fun i : Fin (L / 2) => q i.val), inputCenter L q⟩

def pathOutput (L : Nat) (q : Nat → Nat) (p : Nat → State) : Word :=
  ⟨List.ofFn (fun i : Fin (L / 2) => emit (p i.val) (q i.val) (p (i.val + 1)).high)
    ++ (terminalExtra (p (L / 2)) (inputCenter L q)).toList,
    terminalCenter (p (L / 2)) (inputCenter L q)⟩

def finitePath (L : Nat) (p : Nat → State) : List State :=
  List.ofFn (fun i : Fin (L / 2 + 1) => p i.val)

end Agent107.FoldedTransducer
