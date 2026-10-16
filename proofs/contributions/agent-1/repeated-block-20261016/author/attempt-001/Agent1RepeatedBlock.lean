import PrefixSemantics
import IncomingCarry

/-!
Exact stabilization of the original decimal list normalizer on repeated
bounded coefficient blocks. The first copy retains its actual incoming-carry
transient; every later copy uses the stabilized outgoing carry.

The carry-transfer classification is reused from `IncomingCarry`, and all
digit/carry operations are the original `Agent8` definitions. Empty blocks
and all-nine blocks are included. No safe return or infinite orbit is claimed.
-/

namespace Agent1.RepeatedBlock

open Agent8

/-- Concatenation of a specified number of copies; no arithmetic is redefined. -/
def pow (w : Word) : Nat → Word
  | 0 => []
  | k + 1 => w ++ pow w k

/-- The existing list carry is the existing finite indexed carry computation. -/
theorem terminalCarry_eq_carryIn (w : Word) (e : Nat) :
    terminalCarry w e =
      IncomingCarry.carryIn (fun i => (w[i]?).getD 0) e w.length := by
  induction w generalizing e with
  | nil => rfl
  | cons x xs ih =>
    change terminalCarry xs ((x + e) / 10) =
      IncomingCarry.carryIn (fun i => ((x :: xs)[i]?).getD 0) e (1 + xs.length)
    rw [IncomingCarry.carryIn_add]
    simpa [IncomingCarry.carryIn, Nat.add_comm] using ih ((x + e) / 10)

/-- Every bounded block's carry transfer is idempotent on incoming bit carries.
This includes the all-nine identity transfer, as well as both constant maps. -/
theorem terminalCarry_idempotent (w : Word) (e : Nat)
    (hw : Bounded w 18) (he : e ≤ 1) :
    terminalCarry w (terminalCarry w e) = terminalCarry w e := by
  have hq : ∀ i, i < w.length → (w[i]?).getD 0 ≤ 18 := by
    intro i hi
    rw [List.getElem?_eq_getElem hi]
    exact hw _ (List.getElem_mem hi)
  have ht := IncomingCarry.carryIn_transfer_trichotomy
    (fun i => (w[i]?).getD 0) w.length hq
  rw [← terminalCarry_eq_carryIn w 0, ← terminalCarry_eq_carryIn w 1] at ht
  rcases ht with ⟨h0, h1⟩ | ⟨_, h0, h1⟩ | ⟨h0, h1⟩
  all_goals
    have he' : e = 0 ∨ e = 1 := by omega
    rcases he' with rfl | rfl <;> simp only [h0, h1]

/-- Every positive number of copies has the outgoing carry of the first copy. -/
theorem terminalCarry_pow_succ (w : Word) (e k : Nat)
    (hw : Bounded w 18) (he : e ≤ 1) :
    terminalCarry (pow w (k + 1)) e = terminalCarry w e := by
  induction k generalizing e with
  | zero => simp [pow, terminalCarry_append, terminalCarry]
  | succ k ih =>
    rw [pow, terminalCarry_append,
      ih (terminalCarry w e) (terminalCarry_le_one w e hw he),
      terminalCarry_idempotent w e hw he]

/-- The first normalized block can be transient; subsequent blocks are exact
copies of the block normalized with its stabilized incoming carry. -/
theorem fixedDigits_pow_succ (w : Word) (e k : Nat)
    (hw : Bounded w 18) (he : e ≤ 1) :
    fixedDigits (pow w (k + 1)) e =
      fixedDigits w e ++ pow (fixedDigits w (terminalCarry w e)) k := by
  induction k generalizing e with
  | zero => simp [pow, fixedDigits_append, fixedDigits]
  | succ k ih =>
    rw [pow, fixedDigits_append,
      ih (terminalCarry w e) (terminalCarry_le_one w e hw he),
      terminalCarry_idempotent w e hw he, pow]

/-- Exact original decimal normalization of any positive block power,
including its actual terminal carry and first-copy digit transient. -/
theorem normalize_pow_succ (w : Word) (e k : Nat)
    (hw : Bounded w 18) (he : e ≤ 1) :
    normalize (pow w (k + 1)) e =
      fixedDigits w e ++ pow (fixedDigits w (terminalCarry w e)) k ++
        (if terminalCarry w e = 0 then [] else [terminalCarry w e]) := by
  rw [normalize_decompose, fixedDigits_pow_succ w e k hw he,
    terminalCarry_pow_succ w e k hw he]

end Agent1.RepeatedBlock

#print axioms Agent1.RepeatedBlock.terminalCarry_eq_carryIn
#print axioms Agent1.RepeatedBlock.terminalCarry_idempotent
#print axioms Agent1.RepeatedBlock.terminalCarry_pow_succ
#print axioms Agent1.RepeatedBlock.fixedDigits_pow_succ
#print axioms Agent1.RepeatedBlock.normalize_pow_succ
