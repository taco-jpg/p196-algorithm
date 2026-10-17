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
    simp only [Nat.add_sub_cancel]
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

/-- A successful scan supplies a finite symmetric bounded coefficient
word and a complete bit-valued trace satisfying every original column
equation, with both requested boundary carries. The trace here is an
implementation witness; its root case is later identified with `carry`.
-/
theorem scan_sound (L : Nat) (e : Nat → Nat) (a b : Nat) (qs : List Nat)
    (ha : a ≤ 1) (hb : b ≤ 1) (hscan : scan L e a b = some qs) :
    qs.length = L ∧
    (∀ i, i < L → digitFn qs i ≤ 18) ∧
    (∀ i, i < L → digitFn qs i = digitFn qs (L - 1 - i)) ∧
    (∀ i, i < L → i = L - 1 - i → digitFn qs i % 2 = 0) ∧
    ∃ c : Nat → Nat, c 0 = a ∧ c L = b ∧
      (∀ i, i ≤ L → c i ≤ 1) ∧
      ∀ i, i < L → digitFn qs i + c i = e i + 10 * c (i + 1) := by
  induction L using Nat.strongRecOn generalizing e a b qs with
  | ind L ih =>
    match L with
    | 0 =>
      have hab : a = b := by
        by_cases hn : a = b
        · exact hn
        · simp only [scan, if_neg hn] at hscan
          cases hscan
      have hqs : qs = [] := by simpa only [scan, if_pos hab] using hscan.symm
      subst qs
      refine ⟨rfl, ?_, ?_, ?_, ⟨fun _ => a, rfl, hab, ?_, ?_⟩⟩
      · intro i hi; omega
      · intro i hi; omega
      · intro i hi; omega
      · intro i hi; exact ha
      · intro i hi; omega
    | 1 =>
      cases hc : decodeCenter (e 0) a b with
      | none => simp only [scan, hc, Option.map_none] at hscan; cases hscan
      | some q =>
        have hqs : qs = [q] := by
          simpa only [scan, hc, Option.map_some] using hscan.symm
        subst qs
        have hq := decodeCenter_eq_some_iff.mp hc
        let c : Nat → Nat := fun i => if i = 0 then a else b
        refine ⟨rfl, ?_, ?_, ?_, ⟨c, ?_, ?_, ?_, ?_⟩⟩
        · intro i hi
          have hi0 : i = 0 := by omega
          simpa only [hi0, digitFn, List.getElem?_cons_zero, Option.getD_some] using hq.1
        · intro i hi
          have hi0 : i = 0 := by omega
          simp only [hi0, Nat.sub_self, Nat.sub_zero]
        · intro i hi _
          have hi0 : i = 0 := by omega
          simpa only [hi0, digitFn, List.getElem?_cons_zero, Option.getD_some] using hq.2.1
        · simp only [c, if_pos rfl]
        · simp only [c, Nat.one_ne_zero, if_false]
        · intro i hi
          dsimp [c]
          split
          · exact ha
          · exact hb
        · intro i hi
          have hi0 : i = 0 := by omega
          simpa only [hi0, digitFn, List.getElem?_cons_zero, Option.getD_some,
            c, if_pos rfl, Nat.zero_add, Nat.one_ne_zero, if_false] using hq.2.2
    | L + 2 =>
      cases hE : decodePair (e 0) (e (L + 1)) a b with
      | none => simp only [scan, hE] at hscan; cases hscan
      | some E =>
        cases hs : scan L (fun i => e (i + 1)) E.low E.high with
        | none => simp only [scan, hE, hs, Option.map_none] at hscan; cases hscan
        | some inner =>
          have hqs : qs = wrapDigits E.coeff E.coeff inner := by
            simpa only [scan, hE, hs, Option.map_some] using hscan.symm
          subst qs
          have hv := decodePair_eq_some_iff.mp hE
          obtain ⟨hlen, hbound, hsym, hcenter, c, hc0, hcL, hcb, hcol⟩ :=
            ih L (by omega) (fun i => e (i + 1)) E.low E.high inner
              hv.2.1 hv.2.2.1 hs
          have hw := wrap_word_conditions E.coeff inner hv.1
            (by simpa only [hlen] using hbound)
            (by simpa only [hlen] using hsym)
            (by simpa only [hlen] using hcenter)
          rw [hlen] at hw
          let C : Nat → Nat := fun
            | 0 => a
            | i + 1 => if i ≤ L then c i else b
          have hCmid : ∀ i, i ≤ L → C (i + 1) = c i := by
            intro i hi
            simp only [C, if_pos hi]
          have hCend : C (L + 2) = b := by
            simp only [C, if_neg (show ¬ L + 1 ≤ L by omega)]
          refine ⟨by simp only [length_wrapDigits, hlen], hw.1, hw.2.1,
            hw.2.2, ⟨C, rfl, hCend, ?_, ?_⟩⟩
          · intro i hi
            cases i with
            | zero => exact ha
            | succ i =>
              by_cases hiL : i ≤ L
              · rw [hCmid i hiL]
                exact hcb i hiL
              · simpa only [C, if_neg hiL] using hb
          · intro i hi
            cases i with
            | zero =>
              rw [digitFn_wrap_zero, hCmid 0 (by omega), hc0]
              exact hv.2.2.2.1
            | succ i =>
              by_cases hiL : i = L
              · subst i
                have hdlast : digitFn (wrapDigits E.coeff E.coeff inner) (L + 1) = E.coeff := by
                  simpa only [hlen] using digitFn_wrap_last E.coeff E.coeff inner
                rw [hdlast, hCmid L (Nat.le_refl L), hcL, hCend]
                exact hv.2.2.2.2
              · have hil : i < L := by omega
                rw [digitFn_wrap_inner E.coeff E.coeff inner i (by omega),
                  hCmid i (by omega), hCmid (i + 1) (by omega)]
                exact hcol i hil

#print axioms digitFn_wrap_zero
#print axioms digitFn_wrap_last
#print axioms digitFn_wrap_inner
#print axioms wrap_word_conditions
#print axioms scan_sound

end Agent105DecoderScan9df76b
