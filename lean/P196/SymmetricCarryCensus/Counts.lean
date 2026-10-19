import P196.SymmetricCarryCensus.Enumeration

/-!
Exact cardinality of the original symmetric coefficient-word enumeration.
Filtering a product separates the positive head from the remaining half
word. At odd width its final half coefficient has ten even choices; the
other independent coefficients each have nineteen choices. All counting
uses the existing wordChoices product and the original symWords list.
-/

set_option autoImplicit false

namespace SymmetricCarryCensus

open Agent124.PrefixK SevenColumn.ShortBoundary P196.Agent9.Ensemble

/-- Number of admissible symmetric coefficient words of an exact width. -/
def wordCount (L : Nat) : Nat :=
  if L = 0 then 0 else if L = 1 then 9
  else 18 * 19 ^ (L / 2 - 1) * (if L % 2 = 0 then 1 else 10)

private theorem filter_cons_product (as : List Nat) (ws : List (List Nat))
    (p : Nat → Bool) (q : List Nat → Bool) :
    ((as.flatMap fun a => ws.map (a :: ·)).filter
      (fun w => p (w.getD 0 0) && q w.tail)) =
      (as.filter p).flatMap fun a => (ws.filter q).map (a :: ·) := by
  have hfalse : ws.filter (fun _ => false) = [] :=
    List.filter_eq_nil_iff.mpr (by simp)
  induction as with
  | nil => simp
  | cons a as ih =>
    rw [List.flatMap_cons, List.filter_append, ih]
    cases ha : p a <;>
      simp [List.flatMap_cons, List.filter_append, List.filter_cons,
        List.filter_map, Function.comp_def, List.getD_cons_zero, ha, hfalse]

private theorem length_head_filter (r : Nat) (p : Nat → Bool)
    (q : List Nat → Bool) :
    ((wordChoices (List.range 19) (r + 1)).filter
      (fun w => p (w.getD 0 0) && q w.tail)).length =
      ((List.range 19).filter p).length *
        ((wordChoices (List.range 19) r).filter q).length := by
  rw [wordChoices, filter_cons_product, length_flatMap_map]

private theorem length_tail_filter (r : Nat) (q : List Nat → Bool) :
    ((wordChoices (List.range 19) (r + 1)).filter
      (fun w => q w.tail)).length =
      19 * ((wordChoices (List.range 19) r).filter q).length := by
  simpa using length_head_filter r (fun _ => true) q

private theorem positive_alphabet_length :
    ((List.range 19).filter (fun a => decide (0 < a))).length = 18 := by
  decide

private theorem even_last_count (r : Nat) :
    ((wordChoices (List.range 19) (r + 1)).filter
      (fun w => w.getD r 0 % 2 == 0)).length = 10 * 19 ^ r := by
  induction r with
  | zero => decide
  | succ r ih =>
    have h := length_tail_filter (r + 1) (fun w => w.getD r 0 % 2 == 0)
    rw [ih] at h
    have hfactor : 19 * (10 * 19 ^ r) = 10 * 19 ^ (r + 1) := by
      rw [Nat.pow_succ]
      ac_rfl
    rw [hfactor] at h
    simpa only [List.getD_eq_getElem?_getD, List.getElem?_tail] using h

private theorem positive_halves_count (r : Nat) :
    ((wordChoices (List.range 19) (r + 1)).filter
      (fun w => decide (0 < w.getD 0 0))).length = 18 * 19 ^ r := by
  have htrue : (wordChoices (List.range 19) r).filter (fun _ => true) =
      wordChoices (List.range 19) r := List.filter_eq_self.mpr (by simp)
  have h := length_head_filter r (fun a => decide (0 < a)) (fun _ => true)
  simpa [positive_alphabet_length, htrue, length_wordChoices] using h

private theorem odd_halves_count (r : Nat) :
    ((wordChoices (List.range 19) (r + 2)).filter
      (fun w => decide (0 < w.getD 0 0) && (w.getD (r + 1) 0 % 2 == 0))).length =
      18 * 19 ^ r * 10 := by
  have h := length_head_filter (r + 1) (fun a => decide (0 < a))
    (fun w => w.getD r 0 % 2 == 0)
  rw [positive_alphabet_length, even_last_count] at h
  have hfactor : 18 * (10 * 19 ^ r) = 18 * 19 ^ r * 10 := by ac_rfl
  rw [hfactor] at h
  simpa only [List.getD_eq_getElem?_getD, List.getElem?_tail] using h

private theorem symOK_mirror (L : Nat) (hL : 0 < L) (h : List Nat) :
    symOK L (mirror L h) =
      (decide (0 < h.getD 0 0) &&
        (L % 2 == 0 || h.getD (L / 2) 0 % 2 == 0)) := by
  have hzero : (mirror L h).getD 0 0 = h.getD 0 0 := by
    change wordFun (mirror L h) 0 = h.getD 0 0
    simpa using wordFun_mirror L h 0 hL
  unfold symOK
  rw [hzero]
  by_cases he : L % 2 = 0
  · simp [he]
  · have hmin : min (L / 2) (L - 1 - L / 2) = L / 2 := by omega
    have hmid : (mirror L h).getD (L / 2) 0 = h.getD (L / 2) 0 := by
      change wordFun (mirror L h) (L / 2) = h.getD (L / 2) 0
      rw [wordFun_mirror L h (L / 2) (by omega), hmin]
    rw [hmid]

private theorem symWords_length_as_halves (L : Nat) (hL : 0 < L) :
    (symWords L).length =
      ((wordChoices (List.range 19) ((L + 1) / 2)).filter
        (fun h => decide (0 < h.getD 0 0) &&
          (L % 2 == 0 || h.getD (L / 2) 0 % 2 == 0))).length := by
  unfold symWords
  rw [List.filter_map, List.length_map, lists19_eq_wordChoices]
  congr 1
  apply List.filter_congr
  intro h _
  exact symOK_mirror L hL h

/-- The original executable list has the exact all-width coefficient census. -/
theorem symWords_length (L : Nat) : (symWords L).length = wordCount L := by
  by_cases hzero : L = 0
  · subst L
    decide
  by_cases hone : L = 1
  · subst L
    decide
  have hL : 2 ≤ L := by omega
  rw [symWords_length_as_halves L (by omega)]
  simp only [wordCount, hzero, hone, if_false]
  let r := L / 2 - 1
  have hr : L / 2 = r + 1 := by dsimp [r]; omega
  by_cases he : L % 2 = 0
  · have hhalf : (L + 1) / 2 = r + 1 := by dsimp [r]; omega
    simpa [hhalf, hr, he] using positive_halves_count r
  · have hmod : L % 2 = 1 := by omega
    have hhalf : (L + 1) / 2 = r + 2 := by dsimp [r]; omega
    simpa [hhalf, hr, he, hmod] using odd_halves_count r

end SymmetricCarryCensus

#print axioms SymmetricCarryCensus.symWords_length
