import P196.Core.PhysicalWidth

namespace SeamSafety
open BaseReflection ResetNormalization PhysicalWidth SignedDigitUniqueness

/-- With the input coefficients and incoming carry fixed, a nonzero base
makes the raw normalization map injective in the outgoing carry list. -/
theorem raw_carry_injective (b i : Int) (xs ys : List (Int × Int))
    (hb : b ≠ 0) (hq : qs xs = qs ys)
    (hr : raw b i xs = raw b i ys) : xs = ys := by
  induction xs generalizing i ys with
  | nil =>
    cases ys with
    | nil => rfl
    | cons p ys => simp [qs] at hq
  | cons p xs ih =>
    cases ys with
    | nil => simp [qs] at hq
    | cons a ys =>
      rcases p with ⟨q,c⟩
      rcases a with ⟨r,d⟩
      have hhead : q=r ∧ qs xs=qs ys := List.cons.inj hq
      rcases hhead with ⟨rfl,hqs⟩
      have hh : q+i-b*c=q+i-b*d ∧ raw b c xs=raw b d ys := List.cons.inj hr
      have hmul : b*c=b*d := by omega
      have hcd := Int.eq_of_mul_eq_mul_left hb hmul
      subst d
      have htail := ih c ys hqs hh.2
      rw [htail]

/-- Palindromicity at the actual normalization width forces equality of
full raw lists, including the zero terminal slot in the no-overflow case. -/
theorem palindrome_forces_placed (b : Int) (xs : List (Int × Bool))
    (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (hpal : (actualDigits b xs).reverse = actualDigits b xs) :
    placed b 0 xs = ordinary b xs := by
  unfold actualDigits atActualWidth at hpal
  rw [ordinaryTags_idempotent] at hpal
  split at hpal
  · rename_i ht
    have hraw : ordinary b xs = body b 0 (ordinaryTags xs) ++ [0] := by
      rw [ordinary, placed_body_terminal, ht]
    exact ordinary_nooverflow_symmetry_forces_placed b xs _ hb hbound hq hraw hpal
  · exact ordinary_overflow_symmetry_forces_placed b xs hb hbound hq hpal

theorem palindrome_forces_carry_agreement (b : Int) (xs : List (Int × Bool))
    (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (hpal : (actualDigits b xs).reverse = actualDigits b xs) :
    columns b 0 xs = columns b 0 (ordinaryTags xs) := by
  have heq := palindrome_forces_placed b xs hb hbound hq hpal
  unfold ordinary at heq
  rw [placed_eq_raw, placed_eq_raw] at heq
  apply raw_carry_injective b 0 _ _ (by omega) ?_ heq
  rw [columns_qs, columns_qs, ordinary_qs]

theorem carry_list_defect_nonpalindromic (b : Int) (xs : List (Int × Bool))
    (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (hdefect : columns b 0 xs ≠ columns b 0 (ordinaryTags xs)) :
    (actualDigits b xs).reverse ≠ actualDigits b xs := by
  intro hpal
  exact hdefect (palindrome_forces_carry_agreement b xs hb hbound hq hpal)

def outgoing (b : Int) (xs : List (Int × Bool)) (index : Nat) : Int :=
  ((columns b 0 xs).getD index (0,0)).2

/-- A single mismatch of computed outgoing carries certifies safety of
one normalization step in every base at least three. Out-of-range indices
use the same zero default and therefore cannot produce a false witness. -/
theorem outgoing_defect_nonpalindromic (b : Int) (xs : List (Int × Bool))
    (index : Nat) (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (hdefect : outgoing b xs index ≠ outgoing b (ordinaryTags xs) index) :
    (actualDigits b xs).reverse ≠ actualDigits b xs := by
  apply carry_list_defect_nonpalindromic b xs hb hbound hq
  intro heq
  apply hdefect
  unfold outgoing
  rw [heq]

/-- Canonical ordinary-output safety includes actual digit ranges,
positive leading digit, numeric value, and the nonpalindromic conclusion. -/
theorem canonical_outgoing_defect_safety (b : Int) (xs : List (Int × Bool))
    (index : Nat) (hb : 3 ≤ b) (hbound : Bounded b xs)
    (hp : PositiveTerminal xs)
    (hq : (xs.map Prod.fst).reverse = xs.map Prod.fst)
    (hdefect : outgoing b xs index ≠ outgoing b (ordinaryTags xs) index) :
    (∀ d ∈ actualDigits b xs, 0 ≤ d ∧ d < b) ∧
    PositiveLast (actualDigits b xs) ∧
    eval b (actualDigits b xs) = eval b (xs.map Prod.fst) ∧
    (actualDigits b xs).reverse ≠ actualDigits b xs := by
  obtain ⟨hd,hl,_,hv⟩ := canonical_normalization b xs (by omega) hbound hp
  exact ⟨hd,hl,hv,outgoing_defect_nonpalindromic b xs index hb hbound hq hdefect⟩

end SeamSafety
