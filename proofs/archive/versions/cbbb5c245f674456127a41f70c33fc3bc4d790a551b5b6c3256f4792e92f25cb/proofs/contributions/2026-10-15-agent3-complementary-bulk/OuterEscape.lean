import Lean

/-!
Exact outer factor from Sections 3--6 of the complementary-bulk quotient.
The connection from this list function to decimal whole-word dynamics is
proved in OUTER_FACTOR.md, not in this Lean file. All finite computations
use ordinary `decide`, never `native_decide`. No theorem concerns 196.
-/
namespace P196.Agent3.Outer

set_option maxRecDepth 100000
set_option maxHeartbeats 0

abbrev OuterState := Nat × List Nat

def normalize : List Nat → Nat → List Nat × Nat
  | [], e => ([], e)
  | x :: xs, e =>
    let next := normalize xs ((x + e) / 10)
    ((x + e) % 10 :: next.1, next.2)

def step (s : OuterState) : OuterState :=
  let c := s.1
  let B := s.2
  let k := if c < 9 then 0 else 1
  let t := c - 9 * k
  let left := normalize B 0
  let right := normalize B.reverse k
  let u := c + left.2 - 10 * k
  let R := if right.2 = 1 then 1 :: right.1.reverse else right.1.reverse ++ [t]
  let raw := List.zipWith (fun x y => x + y) (left.1 ++ [u]) R
  (2 * t, (raw.reverse.dropWhile (fun x => x == 2 * t)).reverse)

def iter : Nat → OuterState → OuterState
  | 0, s => s
  | n + 1, s => iter n (step s)

def escapesWithin : Nat → Nat → OuterState → Bool
  | 0, L, s => decide (L < s.2.length)
  | n + 1, L, s => decide (L < s.2.length) || escapesWithin n L (step s)

def evenPhase (i : Fin 8) : Nat := 2 * (i.val + 1)

theorem empty_escape_four : ∀ i : Fin 8,
    escapesWithin 4 0 (evenPhase i, []) = true := by decide

theorem singleton_escape_five : ∀ (i : Fin 8) (a : Fin 18),
    escapesWithin 5 1 (evenPhase i, [a.val + 1]) = true := by decide

theorem empty_escape_seven : ∀ i : Fin 8,
    escapesWithin 7 2 (evenPhase i, []) = true := by decide

theorem singleton_escape_seven : ∀ (i : Fin 8) (a : Fin 18),
    escapesWithin 7 2 (evenPhase i, [a.val + 1]) = true := by decide

theorem pair_escape_seven : ∀ (i : Fin 8) (a : Fin 18) (b : Fin 19),
    escapesWithin 7 2 (evenPhase i, [a.val + 1, b.val]) = true := by decide

theorem escape_implies_exit (n L : Nat) (s : OuterState)
    (h : escapesWithin n L s = true) :
    ∃ t, t ≤ n ∧ L < (iter t s).2.length := by
  induction n generalizing s with
  | zero =>
    have hlen : L < s.2.length := of_decide_eq_true h
    exact ⟨0, Nat.le_refl 0, hlen⟩
  | succ n ih =>
    by_cases hlen : L < s.2.length
    · exact ⟨0, Nat.zero_le _, hlen⟩
    · have hnext : escapesWithin n L (step s) = true := by
        simpa only [escapesWithin, hlen, decide_false, Bool.false_or] using h
      obtain ⟨t, ht, hlarge⟩ := ih (step s) hnext
      exact ⟨t + 1, by omega, hlarge⟩

theorem short_outer_escape (c : Nat) (B : List Nat)
    (hc0 : 2 ≤ c) (hc1 : c ≤ 16) (heven : c % 2 = 0)
    (hdigits : ∀ x ∈ B, x ≤ 18)
    (hhead : ∀ a tail, B = a :: tail → 0 < a)
    (hsize : B.length ≤ 2) :
    escapesWithin 7 2 (c, B) = true := by
  let i : Fin 8 := ⟨c / 2 - 1, by omega⟩
  have hi : evenPhase i = c := by
    unfold evenPhase
    dsimp [i]
    omega
  cases B with
  | nil =>
    rw [← hi]
    exact empty_escape_seven i
  | cons a tail =>
    have ha0 : 0 < a := hhead a tail rfl
    have ha1 : a ≤ 18 := hdigits a (by simp)
    let aa : Fin 18 := ⟨a - 1, by omega⟩
    have haa : aa.val + 1 = a := by dsimp [aa]; omega
    cases tail with
    | nil =>
      rw [← hi, ← haa]
      exact singleton_escape_seven i aa
    | cons b tail2 =>
      have hb : b < 19 := by
        have h := hdigits b (by simp)
        omega
      cases tail2 with
      | nil =>
        rw [← hi, ← haa]
        exact pair_escape_seven i aa ⟨b, hb⟩
      | cons d tail3 =>
        simp only [List.length_cons] at hsize
        omega

theorem short_outer_must_grow (c : Nat) (B : List Nat)
    (hc0 : 2 ≤ c) (hc1 : c ≤ 16) (heven : c % 2 = 0)
    (hdigits : ∀ x ∈ B, x ≤ 18)
    (hhead : ∀ a tail, B = a :: tail → 0 < a)
    (hsize : B.length ≤ 2) :
    ∃ t, t ≤ 7 ∧ 2 < (iter t (c, B)).2.length :=
  escape_implies_exit 7 2 (c, B)
    (short_outer_escape c B hc0 hc1 heven hdigits hhead hsize)

theorem sharp_empty_example :
    escapesWithin 3 0 (2, []) = false ∧ escapesWithin 4 0 (2, []) = true := by decide

theorem sharp_pair_example :
    escapesWithin 6 2 (14, [2, 17]) = false ∧
    escapesWithin 7 2 (14, [2, 17]) = true := by decide

#print axioms empty_escape_four
#print axioms singleton_escape_five
#print axioms empty_escape_seven
#print axioms singleton_escape_seven
#print axioms pair_escape_seven
#print axioms escape_implies_exit
#print axioms short_outer_escape
#print axioms short_outer_must_grow
#print axioms sharp_empty_example
#print axioms sharp_pair_example

end P196.Agent3.Outer
