import Std

/-! Exact autonomous exterior map for the decimal complementary-band quotient.
The ordinary reverse-and-add bridge is a separate written proof. -/
namespace P196.Agent6

abbrev Word := List Nat

/-- Normalize a finite coefficient word with a specified incoming carry. -/
def norm : Word → Nat → Word × Nat
  | [], e => ([], e)
  | x :: xs, e =>
      let rest := norm xs ((x + e) / 10)
      ((x + e) % 10 :: rest.1, rest.2)

structure Exterior where
  phase : Nat
  word : Word
  deriving DecidableEq, Repr

/-- Delete the homogeneous phase suffix, leaving the canonical interface. -/
def trim (c : Nat) (w : Word) : Word :=
  (w.reverse.dropWhile (fun x => x == c)).reverse

/-- The actual overflow is computed, not independently selected. -/
def advance (s : Exterior) : Exterior :=
  let c := s.phase
  let k := if 10 ≤ c then 1 else 0
  let t := c - 9 * k
  let left := norm s.word 0
  let right := norm s.word.reverse k
  let u := c + left.2 - 10 * k
  let rhs := if right.2 == 0 then right.1.reverse ++ [t]
             else 1 :: right.1.reverse
  let raw := List.zipWith Nat.add (left.1 ++ [u]) rhs
  ⟨2 * t, trim (2 * t) raw⟩

def iterate : Nat → Exterior → Exterior
  | 0, s => s
  | n + 1, s => iterate n (advance s)

/-- True exactly when the exterior exceeds the cap at some time at most n. -/
def escapes (cap : Nat) : Nat → Exterior → Bool
  | 0, s => decide (cap < s.word.length)
  | n + 1, s => if cap < s.word.length then true else escapes cap n (advance s)

theorem escapes_sound (cap n : Nat) (s : Exterior)
    (h : escapes cap n s = true) :
    ∃ t, t ≤ n ∧ cap < (iterate t s).word.length := by
  induction n generalizing s with
  | zero =>
      have hs : cap < s.word.length := by simpa [escapes] using h
      exact ⟨0, Nat.le_refl 0, hs⟩
  | succ n ih =>
      by_cases hs : cap < s.word.length
      · exact ⟨0, Nat.zero_le _, hs⟩
      · have hn : escapes cap n (advance s) = true := by
          simpa [escapes, hs] using h
        obtain ⟨t, ht, hw⟩ := ih (advance s) hn
        exact ⟨t + 1, Nat.succ_le_succ ht, hw⟩

/-- Fixed-width base-19 digits, least significant first. -/
def digits19 : Nat → Nat → Word
  | 0, _ => []
  | n + 1, z => z % 19 :: digits19 n (z / 19)

/-- All periodic phases, positive first coefficient, then `tailWidth` digits.
Canonical trimming gives a bijection with exteriors of length <=tailWidth+1. -/
def decode (tailWidth phaseIndex firstIndex tailCode : Nat) : Exterior :=
  let c := 2 * (phaseIndex + 1)
  ⟨c, trim c ((firstIndex + 1) :: digits19 tailWidth tailCode)⟩

def checkChunk (tailWidth bound phaseIndex firstIndex : Nat) : Bool :=
  (List.range (19 ^ tailWidth)).all fun z =>
    escapes (tailWidth + 1) bound (decode tailWidth phaseIndex firstIndex z)

theorem checkChunk_sound (tailWidth bound phaseIndex firstIndex z : Nat)
    (hz : z < 19 ^ tailWidth)
    (h : checkChunk tailWidth bound phaseIndex firstIndex = true) :
    ∃ t, t ≤ bound ∧ tailWidth + 1 <
      (iterate t (decode tailWidth phaseIndex firstIndex z)).word.length := by
  apply escapes_sound
  exact List.all_eq_true.mp h z (List.mem_range.mpr hz)

#print axioms escapes_sound
#print axioms checkChunk_sound

end P196.Agent6
