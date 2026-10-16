import ActualBaseBirths

/-!
The actual overflowing digit word and its shifted mirror positions.
All carries and digits below use the unchanged ordinary normalization APIs.
The width/index identities themselves need only the computed terminal carry;
base and coefficient bounds are supplied by downstream arithmetic classifiers.
-/

namespace P196.Agent7.AllBaseOverflow

open ResetNormalization PhysicalWidth ReverseAdd ActualBaseBirths

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

/-- Extending an ordinary prefix by one coefficient computes its real next carry. -/
theorem ordinary_terminal_take_succ (b e : Int) (xs : List (Int × Bool))
    (k : Nat) (hk : k < xs.length) :
    terminal b e (ordinaryTags (xs.take (k + 1))) =
      (xs[k].1 + terminal b e (ordinaryTags (xs.take k))) / b := by
  induction xs generalizing e k with
  | nil => simp at hk
  | cons p xs ih =>
    cases k with
    | zero => simp [ordinaryTags, terminal]
    | succ k =>
      simpa [ordinaryTags, terminal] using
        ih ((p.1 + e) / b) k (by simpa using hk)

theorem incoming_succ (b : Int) (xs : List (Int × Bool)) (k : Nat)
    (hk : k < xs.length) :
    incoming b xs (k + 1) = (xs[k].1 + incoming b xs k) / b := by
  exact ordinary_terminal_take_succ b 0 xs k hk

/-- This includes the carry just beyond the final old coefficient. -/
theorem incoming_predecessor (b : Int) (xs : List (Int × Bool)) (i : Nat)
    (hi0 : 0 < i) (hi : i ≤ xs.length) :
    incoming b xs i =
      ((xs[i - 1]'(by omega)).1 + incoming b xs (i - 1)) / b := by
  have h := incoming_succ b xs (i - 1) (by omega)
  simpa only [Nat.sub_add_cancel hi0] using h

/-- At the reflected side, old coefficient symmetry couples the next carry
to the other member of the adjacent pair. -/
theorem incoming_mirror_predecessor (b : Int) (xs : List (Int × Bool)) (i : Nat)
    (hi0 : 0 < i) (hi : i < xs.length)
    (hs : (xs.map Prod.fst).reverse = xs.map Prod.fst) :
    incoming b xs (xs.length - i) =
      (xs[i].1 + incoming b xs (xs.length - i - 1)) / b := by
  have h := incoming_predecessor b xs (xs.length - i) (by omega) (by omega)
  have he : xs.length - i - 1 = xs.length - 1 - i := by omega
  rw [he, symmetric_coefficient_at xs i hi hs] at h
  simpa only [he] using h

/-- The final carry selects the real extended output, without changing tags
or replacing the existing normalization definition. -/
theorem actual_overflow_body (b : Int) (xs : List (Int × Bool))
    (ho : terminal b 0 (ordinaryTags xs) = 1) :
    actualDigits b xs = body b 0 (ordinaryTags xs) ++ [1] := by
  simp [actualDigits, atActualWidth, ordinaryTags_idempotent, ho,
    placed_body_terminal]

theorem actual_overflow_length (b : Int) (xs : List (Int × Bool))
    (ho : terminal b 0 (ordinaryTags xs) = 1) :
    (actualDigits b xs).length = xs.length + 1 := by
  rw [actual_overflow_body b xs ho]
  simp [body_length, ordinaryTags]

theorem overflow_length_pos (b : Int) (xs : List (Int × Bool))
    (ho : terminal b 0 (ordinaryTags xs) = 1) : 0 < xs.length := by
  cases xs with
  | nil => simp [ordinaryTags, terminal] at ho
  | cons p xs => simp

/-- Every old-width output digit is the remainder of its actual incoming carry. -/
theorem actual_overflow_at (b : Int) (xs : List (Int × Bool)) (k : Nat)
    (ho : terminal b 0 (ordinaryTags xs) = 1) (hk : k < xs.length) :
    (actualDigits b xs)[k]'(by rw [actual_overflow_length b xs ho]; omega) =
      (xs[k].1 + incoming b xs k) % b := by
  have hbody : k < (body b 0 (ordinaryTags xs)).length := by
    simpa [body_length, ordinaryTags] using hk
  rw [actual_overflow_body b xs ho, List.getElem_append_left hbody]
  exact ordinary_body_at b 0 xs k hk

/-- The newly appended highest digit is exactly the computed terminal one. -/
theorem actual_overflow_last (b : Int) (xs : List (Int × Bool))
    (ho : terminal b 0 (ordinaryTags xs) = 1) :
    (actualDigits b xs)[xs.length]'(by rw [actual_overflow_length b xs ho]; omega) = 1 := by
  rw [actual_overflow_body b xs ho]
  apply List.getElem_concat_length
  simp [body_length, ordinaryTags]

/-- Overflow shifts the actual mirror index by one, so an interior pair uses
two adjacent old coefficients, with their recursively computed carries. -/
theorem actual_overflow_pair_at (b : Int) (xs : List (Int × Bool)) (i : Nat)
    (ho : terminal b 0 (ordinaryTags xs) = 1) (hi0 : 0 < i) (hi : i < xs.length)
    (hs : (xs.map Prod.fst).reverse = xs.map Prod.fst) :
    (pairs (actualDigits b xs))[i]'(by
      rw [pairs_length, actual_overflow_length b xs ho]; omega) =
      (xs[i].1 + incoming b xs i) % b +
        ((xs[i - 1]'(by omega)).1 + incoming b xs (xs.length - i)) % b := by
  have hlen := actual_overflow_length b xs ho
  have him : xs.length - i < xs.length := by omega
  have hrefl : xs.length - 1 - (xs.length - i) = i - 1 := by omega
  have hsym := symmetric_coefficient_at xs (xs.length - i) him hs
  rw [hrefl] at hsym
  rw [pairs_at]
  simp only [hlen, Nat.add_sub_cancel]
  rw [actual_overflow_at b xs i ho hi,
    actual_overflow_at b xs (xs.length - i) ho him, ← hsym]

/-- Default-zero notation for the same exact interior formula. -/
theorem actual_overflow_pair_getD (b : Int) (xs : List (Int × Bool)) (i : Nat)
    (ho : terminal b 0 (ordinaryTags xs) = 1) (hi0 : 0 < i) (hi : i < xs.length)
    (hs : (xs.map Prod.fst).reverse = xs.map Prod.fst) :
    (pairs (actualDigits b xs)).getD i 0 =
      ((xs.getD i (0, false)).1 + incoming b xs i) % b +
        ((xs.getD (i - 1) (0, false)).1 + incoming b xs (xs.length - i)) % b := by
  have hprev : i - 1 < xs.length := by omega
  have hout : i < (pairs (actualDigits b xs)).length := by
    rw [pairs_length, actual_overflow_length b xs ho]; omega
  simpa only [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hout,
    List.getElem?_eq_getElem hi, List.getElem?_eq_getElem hprev, Option.getD_some] using
      actual_overflow_pair_at b xs i ho hi0 hi hs

/-- Pairing the actual output puts the appended one at both endpoints.
No coefficient symmetry or coefficient bounds are required for this identity. -/
theorem actual_overflow_endpoints (b : Int) (xs : List (Int × Bool))
    (ho : terminal b 0 (ordinaryTags xs) = 1) :
    (pairs (actualDigits b xs)).getD 0 0 = 1 + (xs.getD 0 (0, false)).1 % b ∧
      (pairs (actualDigits b xs)).getD xs.length 0 = 1 + (xs.getD 0 (0, false)).1 % b := by
  have hx0 := overflow_length_pos b xs ho
  have hlen := actual_overflow_length b xs ho
  have hd0 : 0 < (actualDigits b xs).length := by omega
  have hdL : xs.length < (actualDigits b xs).length := by omega
  have hp0 : 0 < (pairs (actualDigits b xs)).length := by simpa [pairs_length] using hd0
  have hpL : xs.length < (pairs (actualDigits b xs)).length := by simpa [pairs_length] using hdL
  have hzero := actual_overflow_at b xs 0 ho hx0
  simp only [incoming, List.take_zero, ordinaryTags, List.map_nil, terminal, Int.add_zero] at hzero
  have hlast := actual_overflow_last b xs ho
  have hleft := pairs_at (actualDigits b xs) 0 hd0
  have hright := pairs_at (actualDigits b xs) xs.length hdL
  simp only [hlen, Nat.add_sub_cancel, Nat.sub_zero, Nat.sub_self] at hleft hright
  rw [hzero, hlast] at hleft hright
  constructor
  · simpa only [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hp0,
      List.getElem?_eq_getElem hx0, Option.getD_some, Int.add_comm] using hleft
  · simpa only [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hpL,
      List.getElem?_eq_getElem hx0, Option.getD_some] using hright

#print axioms ordinary_terminal_take_succ
#print axioms incoming_succ
#print axioms incoming_predecessor
#print axioms incoming_mirror_predecessor
#print axioms actual_overflow_body
#print axioms actual_overflow_length
#print axioms overflow_length_pos
#print axioms actual_overflow_at
#print axioms actual_overflow_last
#print axioms actual_overflow_pair_at
#print axioms actual_overflow_pair_getD
#print axioms actual_overflow_endpoints

end P196.Agent7.AllBaseOverflow
