import LychrelDigitSums

/-! Exact short-word boundary for the seven-column abstraction.
All finite words are connected directly to FoldedDecimal.Admissible and
FoldedDecimal.nextColumns. No external evaluation is used as a proof. -/

namespace SevenColumn.ShortBoundary

open FoldedDecimal

def wordOf (q : Nat → Nat) (L : Nat) : List Nat := (List.range L).map q

def wordFun (s : List Nat) (i : Nat) : Nat := s[i]?.getD 0

def nextWord (s : List Nat) : List Nat :=
  wordOf (nextColumns (wordFun s) s.length) (nextWidth (wordFun s) s.length)

/-- Canonical halves, with positive outer column and even odd-width center. -/
def rawWords : Nat → List (List Nat)
  | 1 => (List.range 9).map (fun a => [2 * (a + 1)])
  | 2 => (List.range 18).map (fun a => [a + 1, a + 1])
  | 3 => (List.range 18).flatMap (fun a =>
      (List.range 10).map (fun c => [a + 1, 2 * c, a + 1]))
  | 4 => (List.range 18).flatMap (fun a =>
      (List.range 19).map (fun b => [a + 1, b, b, a + 1]))
  | 5 => (List.range 18).flatMap (fun a =>
      (List.range 19).flatMap (fun b =>
      (List.range 10).map (fun c => [a + 1, b, 2 * c, b, a + 1])))
  | 6 => (List.range 18).flatMap (fun a =>
      (List.range 19).flatMap (fun b =>
      (List.range 19).map (fun c => [a + 1, b, c, c, b, a + 1])))
  | _ => []

def shortWords : List (List Nat) :=
  rawWords 1 ++ rawWords 2 ++ rawWords 3 ++ rawWords 4 ++ rawWords 5 ++ rawWords 6

theorem wordOf_length (q : Nat → Nat) (L : Nat) : (wordOf q L).length = L := by
  simp [wordOf]

theorem wordOf_get (q : Nat → Nat) (L i : Nat) (hi : i < L) :
    wordFun (wordOf q L) i = q i := by
  simp [wordFun, wordOf, List.getElem?_map, hi]

/-- Every actual admissible word of width below seven occurs in its exact list. -/
theorem rawWords_complete (q : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hL : L < 7) : wordOf q L ∈ rawWords L := by
  rcases hq with ⟨hpos, houter, hbound, hsymm, hcenter⟩
  have hb0 := hbound 0 hpos
  have he : L = 1 ∨ L = 2 ∨ L = 3 ∨ L = 4 ∨ L = 5 ∨ L = 6 := by omega
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl
  · have hc := hcenter 0 (by omega) (by omega)
    have hd : 2 * (q 0 / 2) = q 0 := by omega
    have hz : 0 < q 0 / 2 := by omega
    have hh : q 0 / 2 - 1 < 9 := by omega
    simp only [rawWords, List.mem_map]
    refine ⟨q 0 / 2 - 1, List.mem_range.mpr hh, ?_⟩
    simp [wordOf, List.range_succ, show 2 * (q 0 / 2 - 1 + 1) = q 0 by omega]
  · have h1 := hsymm 1 (by omega)
    simp only [rawWords, List.mem_map]
    refine ⟨q 0 - 1, List.mem_range.mpr (by omega), ?_⟩
    simp [wordOf, List.range_succ, show q 0 - 1 + 1 = q 0 by omega, h1]
  · have h2 := hsymm 2 (by omega)
    have hc := hcenter 1 (by omega) (by omega)
    have hb1 := hbound 1 (by omega)
    simp only [rawWords, List.mem_flatMap, List.mem_map]
    refine ⟨q 0 - 1, List.mem_range.mpr (by omega), q 1 / 2,
      List.mem_range.mpr (by omega), ?_⟩
    simp [wordOf, List.range_succ, show q 0 - 1 + 1 = q 0 by omega,
      show 2 * (q 1 / 2) = q 1 by omega, h2]
  · have h2 := hsymm 2 (by omega)
    have h3 := hsymm 3 (by omega)
    have hb1 := hbound 1 (by omega)
    simp only [rawWords, List.mem_flatMap, List.mem_map]
    refine ⟨q 0 - 1, List.mem_range.mpr (by omega), q 1,
      List.mem_range.mpr (by omega), ?_⟩
    simp [wordOf, List.range_succ, show q 0 - 1 + 1 = q 0 by omega, h2, h3]
  · have h3 := hsymm 3 (by omega)
    have h4 := hsymm 4 (by omega)
    have hb1 := hbound 1 (by omega)
    have hb2 := hbound 2 (by omega)
    have hc := hcenter 2 (by omega) (by omega)
    simp only [rawWords, List.mem_flatMap, List.mem_map]
    refine ⟨q 0 - 1, List.mem_range.mpr (by omega), q 1,
      List.mem_range.mpr (by omega), q 2 / 2, List.mem_range.mpr (by omega), ?_⟩
    simp [wordOf, List.range_succ, show q 0 - 1 + 1 = q 0 by omega,
      show 2 * (q 2 / 2) = q 2 by omega, h3, h4]
  · have h3 := hsymm 3 (by omega)
    have h4 := hsymm 4 (by omega)
    have h5 := hsymm 5 (by omega)
    have hb1 := hbound 1 (by omega)
    have hb2 := hbound 2 (by omega)
    simp only [rawWords, List.mem_flatMap, List.mem_map]
    refine ⟨q 0 - 1, List.mem_range.mpr (by omega), q 1,
      List.mem_range.mpr (by omega), q 2, List.mem_range.mpr (by omega), ?_⟩
    simp [wordOf, List.range_succ, show q 0 - 1 + 1 = q 0 by omega, h3, h4, h5]

theorem shortWords_complete (q : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hL : L < 7) : wordOf q L ∈ shortWords := by
  have hm := rawWords_complete q L hq hL
  have he : L = 1 ∨ L = 2 ∨ L = 3 ∨ L = 4 ∨ L = 5 ∨ L = 6 := by
    have hp := hq.1
    omega
  rcases he with rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp only [shortWords, List.mem_append] <;> simp [hm]

theorem wordOf_congr (q r : Nat → Nat) (L : Nat)
    (h : ∀ i, i < L → q i = r i) : wordOf q L = wordOf r L := by
  apply List.map_congr_left
  intro i hi
  exact h i (List.mem_range.mp hi)

/-- Reifying an actual finite word and updating it uses exactly the core update. -/
theorem nextWord_wordOf (q : Nat → Nat) (L : Nat) :
    nextWord (wordOf q L) = wordOf (nextColumns q L) (nextWidth q L) := by
  have hr := wordOf_get q L
  have hc := carry_congr_upto (wordFun (wordOf q L)) q L hr L (Nat.le_refl L)
  have hw : nextWidth (wordFun (wordOf q L)) L = nextWidth q L := by
    simp [nextWidth, hc]
  simp only [nextWord, wordOf_length, hw]
  apply wordOf_congr
  intro i hi
  by_cases hz : DecimalDigits.carry q L = 0
  · have hil : i < L := by simpa [nextWidth, hz] using hi
    have him : L - 1 - i < L := by omega
    simp only [nextColumns, hc, hz, if_true, DecimalDigits.columnSum,
      DecimalDigits.reflected]
    rw [output_congr_upto _ _ L hr i hil,
      output_congr_upto _ _ L hr (L - 1 - i) him]
  · simp only [nextColumns, hc, hz, if_false, DecimalDigits.columnSum,
      DecimalDigits.reflected]
    rw [extended_congr_upto _ _ L hr i,
      extended_congr_upto _ _ L hr (L + 1 - 1 - i)]

theorem short_next_width (q : Nat → Nat) (L : Nat) (hL : L < 7) :
    nextWidth q L ≤ 7 := by
  unfold nextWidth
  split <;> omega

/-- The sole short-to-seven crossing is a six-column overflow. -/
theorem short_crossing (q : Nat → Nat) (L : Nat) (hL : L < 7)
    (hnext : 7 ≤ nextWidth q L) :
    L = 6 ∧ nextWidth q L = 7 ∧ DecimalDigits.carry q L ≠ 0 := by
  unfold nextWidth at *
  split at hnext
  · omega
  · rename_i hc
    simp [hc]
    omega

/-- Generic bridge: a checked finite short-word exclusion covers every actual
short admissible source, including six-to-seven crossings. -/
theorem short_lookup_exclusion (rank : List Nat → Option Nat)
    (checked : ∀ s ∈ shortWords, rank (nextWord s) = none)
    (q : Nat → Nat) (L : Nat) (hq : Admissible L q) (hL : L < 7) :
    rank (wordOf (nextColumns q L) (nextWidth q L)) = none := by
  have h := checked (wordOf q L) (shortWords_complete q L hq hL)
  rw [nextWord_wordOf] at h
  exact h

theorem short_lookup_exclusion_of_check (rank : List Nat → Option Nat)
    (checked : shortWords.all (fun s => (rank (nextWord s)).isNone) = true)
    (q : Nat → Nat) (L : Nat) (hq : Admissible L q) (hL : L < 7) :
    rank (wordOf (nextColumns q L) (nextWidth q L)) = none := by
  apply short_lookup_exclusion rank _ q L hq hL
  intro s hs
  exact Option.isNone_iff_eq_none.mp (List.all_eq_true.mp checked s hs)

/-- The sole short certificate target has no exact predecessor. The proof uses
only the six column equations and carry bounds; no finite search is needed. -/
theorem short_target_no_predecessor (q : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (_hL : L < 7) :
    wordOf (nextColumns q L) (nextWidth q L) ≠ [7,3,9,9,3,7] := by
  intro heq
  have hw : nextWidth q L = 6 := by
    have h := congrArg List.length heq
    simpa only [wordOf_length, List.length_cons, List.length_nil] using h
  have h0 := congrArg (fun s => wordFun s 0) heq
  have h1 := congrArg (fun s => wordFun s 1) heq
  have h2 := congrArg (fun s => wordFun s 2) heq
  dsimp only at h0 h1 h2
  rw [wordOf_get _ _ 0 (by omega)] at h0
  rw [wordOf_get _ _ 1 (by omega)] at h1
  rw [wordOf_get _ _ 2 (by omega)] at h2
  simp only [wordFun, List.getElem?_cons_zero, List.getElem?_cons_succ,
    Option.getD_some] at h0 h1 h2
  have cb := DecimalDigits.carry_bounded q L hq.2.2.1
  by_cases hz : DecimalDigits.carry q L = 0
  · have hL : L = 6 := by simpa [nextWidth, hz] using hw
    subst L
    have c0 : DecimalDigits.carry q 0 = 0 := rfl
    have c1 := cb 1 (by omega)
    have c2 := cb 2 (by omega)
    have c3 := cb 3 (by omega)
    have c4 := cb 4 (by omega)
    have c5 := cb 5 (by omega)
    have e0 := DecimalDigits.column_equation q 0
    have e1 := DecimalDigits.column_equation q 1
    have e2 := DecimalDigits.column_equation q 2
    have e3 := DecimalDigits.column_equation q 3
    have e4 := DecimalDigits.column_equation q 4
    have e5 := DecimalDigits.column_equation q 5
    have s3 := hq.2.2.2.1 3 (by omega)
    have s4 := hq.2.2.2.1 4 (by omega)
    have s5 := hq.2.2.2.1 5 (by omega)
    simp only [nextColumns, hz, if_true, DecimalDigits.columnSum,
      DecimalDigits.reflected] at h0 h1 h2
    simp only [Nat.reduceSub, Nat.reduceAdd] at *
    omega
  · have hL : L = 5 := by simp [nextWidth, hz] at hw; omega
    subst L
    have c0 : DecimalDigits.carry q 0 = 0 := rfl
    have c1 := cb 1 (by omega)
    have c4 := cb 4 (by omega)
    have c5 : DecimalDigits.carry q 5 = 1 := by have := cb 5 (by omega); omega
    have e0 := DecimalDigits.column_equation q 0
    have e4 := DecimalDigits.column_equation q 4
    have s4 := hq.2.2.2.1 4 (by omega)
    simp only [nextColumns, hz, if_false, DecimalDigits.columnSum,
      DecimalDigits.reflected, Nat.reduceAdd, Nat.reduceSub,
      DecimalDigits.extended, Nat.reduceLT, if_true, if_false] at h0 h1
    omega

theorem shortWords_count : shortWords.length = 10467 := by
  simp [shortWords, rawWords, List.length_flatMap, List.map_const']

end SevenColumn.ShortBoundary

#print axioms SevenColumn.ShortBoundary.rawWords_complete
#print axioms SevenColumn.ShortBoundary.shortWords_complete
#print axioms SevenColumn.ShortBoundary.nextWord_wordOf
#print axioms SevenColumn.ShortBoundary.short_lookup_exclusion
#print axioms SevenColumn.ShortBoundary.shortWords_count
#print axioms SevenColumn.ShortBoundary.short_target_no_predecessor
