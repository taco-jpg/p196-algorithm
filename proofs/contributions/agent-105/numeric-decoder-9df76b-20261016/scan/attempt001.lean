import Lychrel196Research
import Agent101NumericFibers
import Agent105DecoderLocal9df76b

/-!
# Complete finite two-ended numerical decoder

The scanner reads ordinary output digits from both ends, retaining the
original decimal column equations. Its public specification uses the
unchanged `FoldedDecimal.Admissible`, `DecimalDigits.output`, and
`DecimalDigits.carry`. Lists are least-significant first.
-/

namespace Agent105DecoderScan9df76b

open DecimalDigits FoldedDecimal Agent101 Agent105DecoderLocal9df76b

/-- Scan all remaining digits. The empty interior meets the two carries;
the singleton interior checks the even source center coefficient. -/
def scan : Nat → (Nat → Nat) → Nat → Nat → Option (List Nat)
  | 0, _, a, b => if a = b then some [] else none
  | 1, e, a, b => (decodeCenter (e 0) a b).map (fun q => [q])
  | L + 2, e, a, b =>
      match decodePair (e 0) (e (L + 1)) a b with
      | none => none
      | some E =>
          (scan L (fun i => e (i + 1)) E.low E.high).map
            (wrapDigits E.coeff E.coeff)

/-- The complete decoder rejects zero width, a non-bit terminal carry,
and a zero exterior coefficient. Inner zero coefficients remain allowed. -/
def decodeAtWidth (e : Nat → Nat) (L h : Nat) : Option (List Nat) :=
  if 0 < L ∧ h ≤ 1 then
    match scan L e 0 h with
    | none => none
    | some qs => if 0 < digitFn qs 0 then some qs else none
  else none

theorem digitFn_wrap_zero (a b : Nat) (qs : List Nat) :
    digitFn (wrapDigits a b qs) 0 = a := by
  rfl

theorem digitFn_wrap_last (a b : Nat) (qs : List Nat) :
    digitFn (wrapDigits a b qs) (qs.length + 1) = b := by
  simp only [digitFn, wrapDigits, List.getElem?_cons_succ,
    List.getElem?_append_right (Nat.le_refl qs.length), Nat.sub_self,
    List.getElem?_cons_zero, Option.getD_some]

theorem digitFn_wrap_inner (a b : Nat) (qs : List Nat) (i : Nat)
    (hi : i < qs.length) :
    digitFn (wrapDigits a b qs) (i + 1) = digitFn qs i := by
  simp only [digitFn, wrapDigits, List.getElem?_cons_succ,
    List.getElem?_append_left hi]

/-- Putting the same bounded coefficient at both ends preserves exactly
the original finite-word bounds, symmetry, and center parity conditions. -/
theorem wrap_word_conditions (q : Nat) (qs : List Nat)
    (hq : q ≤ 18)
    (hbound : ∀ i, i < qs.length → digitFn qs i ≤ 18)
    (hsym : ∀ i, i < qs.length →
      digitFn qs i = digitFn qs (qs.length - 1 - i))
    (hcenter : ∀ i, i < qs.length → i = qs.length - 1 - i →
      digitFn qs i % 2 = 0) :
    (∀ i, i < qs.length + 2 → digitFn (wrapDigits q q qs) i ≤ 18) ∧
    (∀ i, i < qs.length + 2 → digitFn (wrapDigits q q qs) i =
      digitFn (wrapDigits q q qs) (qs.length + 2 - 1 - i)) ∧
    (∀ i, i < qs.length + 2 → i = qs.length + 2 - 1 - i →
      digitFn (wrapDigits q q qs) i % 2 = 0) := by
  have hvalue : ∀ i, i < qs.length + 2 →
      digitFn (wrapDigits q q qs) i =
        if i = 0 ∨ i = qs.length + 1 then q else digitFn qs (i - 1) := by
    intro i hi
    by_cases hzero : i = 0
    · subst i
      simp only [digitFn_wrap_zero, true_or, if_true]
    by_cases hlast : i = qs.length + 1
    · subst i
      simp only [digitFn_wrap_last, or_true, if_true]
    have hiinner : i - 1 < qs.length := by omega
    have hisucc : i = (i - 1) + 1 := by omega
    rw [if_neg (by omega), hisucc, digitFn_wrap_inner q q qs (i - 1) hiinner]
  refine ⟨?_, ?_, ?_⟩
  · intro i hi
    rw [hvalue i hi]
    split
    · exact hq
    · exact hbound (i - 1) (by omega)
  · intro i hi
    rw [hvalue i hi, hvalue (qs.length + 2 - 1 - i) (by omega)]
    by_cases hout : i = 0 ∨ i = qs.length + 1
    · rw [if_pos hout, if_pos (by omega)]
    · rw [if_neg hout, if_neg (by omega)]
      have heq : qs.length + 2 - 1 - i - 1 = qs.length - 1 - (i - 1) := by omega
      rw [heq]
      exact hsym (i - 1) (by omega)
  · intro i hi heq
    have hout : ¬ (i = 0 ∨ i = qs.length + 1) := by omega
    rw [hvalue i hi, if_neg hout]
    exact hcenter (i - 1) (by omega) (by omega)

#print axioms digitFn_wrap_zero
#print axioms digitFn_wrap_last
#print axioms digitFn_wrap_inner
#print axioms wrap_word_conditions

end Agent105DecoderScan9df76b
