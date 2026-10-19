import P196.MaximalDigitSplitFibers.Equality

/-!
Agent #7. The sharp gap below the digit-splitting maximum.
A positive inner length has submaximum 81 times the remaining power of ten.
The empty inner list has only the separate bound eight and its witnesses.
-/

namespace Agent7.MaximalDigitSplitFibers

open Agent101

theorem pairProduct_gap_nonmax (h : List Nat) (hlen : 0 < h.length)
    (hne : natProduct (h.map (pairCount false)) ≠ 10 ^ h.length) :
    natProduct (h.map (pairCount false)) ≤ 9 * 10 ^ (h.length - 1) := by
  induction h with
  | nil => simp at hlen
  | cons s h ih =>
    by_cases hs : pairCount false s = 10
    · have hhne : natProduct (h.map (pairCount false)) ≠ 10 ^ h.length := by
        intro he
        apply hne
        simp [List.map_cons, natProduct, hs, he, Nat.pow_succ, Nat.mul_comm]
      have hhl : 0 < h.length := by
        cases h with
        | nil => simp [natProduct] at hhne
        | cons t h => simp
      have hb := Nat.mul_le_mul_left 10 (ih hhl hhne)
      have hp : 10 ^ h.length = 10 ^ (h.length - 1) * 10 := by
        have he : (h.length - 1).succ = h.length := by omega
        simpa only [he] using Nat.pow_succ 10 (h.length - 1)
      simpa [List.map_cons, natProduct, hs, hp, Nat.mul_assoc,
        Nat.mul_comm, Nat.mul_left_comm] using hb
    · have hs9 : pairCount false s ≤ 9 := by
        have hb := pairCount_inner_le s
        omega
      have hb := Nat.mul_le_mul hs9 (pairProduct_le h)
      simpa [List.map_cons, natProduct] using hb

theorem profileCount_gap (s : Nat) (h : List Nat) (c : Option Nat)
    (hlen : 0 < h.length)
    (hne : profileCount (s :: h) c ≠ 9 * 10 ^ h.length) :
    profileCount (s :: h) c ≤ 81 * 10 ^ (h.length - 1) := by
  have ha : pairCount true s * centerCount c ≤ 9 := by
    simpa using Nat.mul_le_mul (pairCount_outer_le s) (centerCount_le c)
  change (pairCount true s * centerCount c) *
    natProduct (h.map (pairCount false)) ≤ 81 * 10 ^ (h.length - 1)
  by_cases ha9 : pairCount true s * centerCount c = 9
  · have hpne : natProduct (h.map (pairCount false)) ≠ 10 ^ h.length := by
      intro he
      apply hne
      change (pairCount true s * centerCount c) *
        natProduct (h.map (pairCount false)) = 9 * 10 ^ h.length
      rw [ha9, he]
    have hb := Nat.mul_le_mul_left 9 (pairProduct_gap_nonmax h hlen hpne)
    rw [ha9]
    simpa [← Nat.mul_assoc] using hb
  · have ha8 : pairCount true s * centerCount c ≤ 8 := by omega
    have hb := Nat.mul_le_mul ha8 (pairProduct_le h)
    have hp : 10 ^ h.length = 10 ^ (h.length - 1) * 10 := by
      have he : (h.length - 1).succ = h.length := by omega
      simpa only [he] using Nat.pow_succ 10 (h.length - 1)
    rw [hp] at hb
    omega

theorem profileCount_gap_cons (s t : Nat) (h : List Nat) (c : Option Nat)
    (hne : profileCount (s :: t :: h) c ≠ 9 * 10 ^ (h.length + 1)) :
    profileCount (s :: t :: h) c ≤ 81 * 10 ^ h.length := by
  have hb := profileCount_gap s (t :: h) c (by simp) (by simpa using hne)
  simpa using hb

theorem profileCount_gap_of_length_succ
    (s : Nat) (h : List Nat) (c : Option Nat) (k : Nat)
    (hlen : h.length = k + 1)
    (hne : profileCount (s :: h) c ≠ 9 * 10 ^ (k + 1)) :
    profileCount (s :: h) c ≤ 81 * 10 ^ k := by
  have hb := profileCount_gap s h c (by omega) (by simpa [hlen] using hne)
  simpa [hlen] using hb

theorem profileCount_gap_empty (s : Nat) (c : Option Nat)
    (hne : profileCount [s] c ≠ 9) :
    profileCount [s] c ≤ 8 := by
  have hb := profileCount_cons_le s [] c
  simp only [List.length_nil, Nat.pow_zero, Nat.mul_one] at hb
  omega

theorem profileCount_submax_witness (k : Nat) (c : Option Nat)
    (hc : centerCount c = 1) :
    profileCount (9 :: 8 :: List.replicate k 9) c = 81 * 10 ^ k := by
  simp [profileCount, pairCount, hc, List.map_replicate,
    natProduct, natProduct_replicate, ← Nat.mul_assoc]

theorem profileCount_submax_witness_lt (k : Nat) (c : Option Nat)
    (hc : centerCount c = 1) :
    profileCount (9 :: 8 :: List.replicate k 9) c < 9 * 10 ^ (k + 1) := by
  rw [profileCount_submax_witness k c hc, Nat.pow_succ]
  have hp : 0 < 10 ^ k := Nat.pow_pos (by decide)
  omega

theorem profileCount_submax_empty_witness (c : Option Nat)
    (hc : centerCount c = 1) :
    profileCount [8] c = 8 := by
  simp [profileCount, pairCount, hc, natProduct]

theorem profileCount_submax_empty_witness_lt (c : Option Nat)
    (hc : centerCount c = 1) :
    profileCount [8] c < 9 := by
  rw [profileCount_submax_empty_witness c hc]
  decide

#print axioms pairProduct_gap_nonmax
#print axioms profileCount_gap_cons
#print axioms profileCount_gap
#print axioms profileCount_gap_of_length_succ
#print axioms profileCount_gap_empty
#print axioms profileCount_submax_witness
#print axioms profileCount_submax_witness_lt
#print axioms profileCount_submax_empty_witness
#print axioms profileCount_submax_empty_witness_lt

end Agent7.MaximalDigitSplitFibers
