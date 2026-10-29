import P196.F1Semigroup.F1Tables
import P196.F1Semigroup.F1MinData
/-! Definitions for the minimal-DFA theorem: DFA, certificate accessors, separation / congruence checks. -/
namespace F1

structure DFA (σ : Type) where
  start : σ
  step : σ → Bool → σ
  acc : σ → Bool

def DFA.runFrom {σ : Type} (D : DFA σ) (q : σ) (w : List Bool) : σ := w.foldl D.step q
def DFA.accepts {σ : Type} (D : DFA σ) (w : List Bool) : Bool := D.acc (D.runFrom D.start w)

def nC : Nat := 241
def Rget (c : Nat) : Nat := (RP >>> (9 * c)) % 512
def clsOf (i : Nat) : Nat := (ClsP >>> (9 * i)) % 512

def accQ (i : Nat) : Bool := AccP.testBit i

/-- decode a separating word: little-endian bits below a leading marker bit -/
def decodeWord : Nat → Nat → List Bool
  | 0, _ => []
  | f + 1, v => if v ≤ 1 then [] else (v % 2 == 1) :: decodeWord f (v / 2)

def sepWord (c d : Nat) : List Bool := decodeWord 10 (((SepL.getD d 0) >>> (10 * c)) % 1024)

def irunQ (i : Nat) (w : List Bool) : Bool := accQ (irun i w)

/-- all representatives are states, and every pair `c < d` of representatives is separated by `sepWord c d` -/
def sepOK (d : Nat) : Bool :=
  decide (Rget d < nS) && (List.range d).all fun c =>
    accQ (irun (Rget c) (sepWord c d)) != accQ (irun (Rget d) (sepWord c d))

/-- congruence of the class map -/
def clsOK (i : Nat) : Bool :=
  decide (clsOf i < nC) && decide (Rget (clsOf i) < nS) && (accQ (Rget (clsOf i)) == accQ i) &&
  decide (clsOf (Nget false (Rget (clsOf i))) = clsOf (Nget false i)) &&
  decide (clsOf (Nget true (Rget (clsOf i))) = clsOf (Nget true i))


end F1
