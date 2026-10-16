import ActualPrefix
import ShortBoundary
import LongRowsBase

/-!
# Four-column actual ancestry with exact short-transition rank descent

Agent #119, task `agent119-four-column-prefix-kernel`.

This module instantiates Agent #104's accepted, width-generic prefix
machinery (`SevenColumn.prefixPredecessors`,
`SevenColumnProjection.actual_mem_prefixPredecessors`,
`SevenColumn.Certificate.checkedRows_closed`) at prefix width four.
None of those modules is modified.

Projection: a pair word of width `L` is represented by its first
`min L 4` low-to-high pair sums.  Long sources (width at least four) are
covered by the proved complete local inverse.  Short sources (widths one to
three) are covered by the exact finite list `shortWords3` of all admissible
short words and an explicit, decidable *short descent* check: whenever the
exact image of a short word lies in the rank tree, the short word itself lies
in the tree with strictly smaller rank.  No assertion that short images avoid
the tree is made.

The main theorem `actual_iterPairs_rank4` is conditional on the two finite
checks; the concrete instance supplies them by kernel reduction elsewhere.
-/

namespace FourColumnKernel

open DecimalDigits FoldedDecimal Lychrel196 OverflowCarryNormalization
open NormalizationBridge CarryHistory SevenColumnProjection
open SevenColumn.Certificate SevenColumn.ShortBoundary

/-- Retain the complete exact word below width four, or its first four
low-to-high pair sums otherwise. -/
def project4 (q : Nat → Nat) (L : Nat) : List Nat :=
  wordPrefix q (min L 4)

theorem project4_short (q : Nat → Nat) (L : Nat) (hL : L ≤ 4) :
    project4 q L = wordOf q L := by
  simp only [project4, Nat.min_eq_left hL, wordPrefix_eq_range_map, wordOf]

theorem project4_long (q : Nat → Nat) (L : Nat) (hL : 4 ≤ L) :
    project4 q L = wordPrefix q 4 := by
  simp only [project4, Nat.min_eq_right hL]

theorem project4_congr (q r : Nat → Nat) (L : Nat)
    (h : ∀ i, i < L → q i = r i) : project4 q L = project4 r L := by
  simp only [project4, wordPrefix_eq_range_map]
  apply List.map_congr_left
  intro i hi
  apply h
  have hh := List.mem_range.mp hi
  omega

theorem width_le_nextWidth (q : Nat → Nat) (L : Nat) :
    L ≤ nextWidth q L := by
  unfold nextWidth
  split <;> omega

theorem nextWidth_le_succ (q : Nat → Nat) (L : Nat) :
    nextWidth q L ≤ L + 1 := by
  unfold nextWidth
  split <;> omega

/-- Every admissible word of width one, two or three. -/
def shortWords3 : List (List Nat) :=
  rawWords 1 ++ rawWords 2 ++ rawWords 3

theorem shortWords3_complete (q : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hL : L < 4) : wordOf q L ∈ shortWords3 := by
  have hm := rawWords_complete q L hq (by omega)
  have he : L = 1 ∨ L = 2 ∨ L = 3 := by
    have hp := hq.1
    omega
  rcases he with rfl | rfl | rfl <;>
    simp only [shortWords3, List.mem_append] <;> simp [hm]

theorem shortWords3_count : shortWords3.length = 207 := by
  simp [shortWords3, rawWords, List.length_flatMap, List.map_const']

/-- One decidable short-descent row: if the exact image of the short word `s`
has a rank `r`, then `s` itself has a rank strictly below `r`. -/
def shortDescentOK (tree : RankTree) (s : List Nat) : Bool :=
  match lookup tree (nextWord s) with
  | none => true
  | some r =>
    match lookup tree s with
    | none => false
    | some k => decide (k < r)

/-- The complete finite short-descent check. -/
def ShortDescent (tree : RankTree) : Prop :=
  ∀ s ∈ shortWords3, shortDescentOK tree s = true

theorem shortDescent_of_all (tree : RankTree)
    (h : shortWords3.all (shortDescentOK tree) = true) : ShortDescent tree := by
  intro s hs
  exact List.all_eq_true.mp h s hs

theorem shortDescentOK_sound {tree : RankTree} {s : List Nat} {r : Nat}
    (h : shortDescentOK tree s = true) (hr : lookup tree (nextWord s) = some r) :
    ∃ k, lookup tree s = some k ∧ k < r := by
  unfold shortDescentOK at h
  rw [hr] at h
  simp only at h
  split at h
  · contradiction
  · rename_i k hk
    exact ⟨k, hk, of_decide_eq_true h⟩

/-- Exact semantic rank theorem at prefix width four.  Every actual time-`t`
pair state whose four-column projection has rank `r` in a checked tree
satisfies `t ≤ r`.  Long transitions use the complete proved inverse; short
transitions use the exact short-descent check. -/
theorem actual_iterPairs_rank4
    {tree : RankTree} (rows : CheckedRows tree (longPred 4))
    (short : ShortDescent tree)
    (q : Nat → Nat) (L : Nat) (ha : Admissible L q)
    (t : Nat) {r : Nat}
    (hend : lookup tree (project4 (iterPairs q L t).2 (iterPairs q L t).1) = some r) :
    t ≤ r := by
  induction t generalizing r with
  | zero => omega
  | succ t ih =>
      let v := iterPairs q L t
      have hv : Admissible v.1 v.2 := iterPairs_admissible q L t ha
      change lookup tree (project4 (nextColumns v.2 v.1) (nextWidth v.2 v.1)) = some r
        at hend
      by_cases hshort : v.1 < 4
      · have hnw : nextWidth v.2 v.1 ≤ 4 := by
          have := nextWidth_le_succ v.2 v.1
          omega
        rw [project4_short _ _ hnw, ← nextWord_wordOf] at hend
        have hs := shortWords3_complete v.2 v.1 hv hshort
        obtain ⟨k, hk, hkr⟩ := shortDescentOK_sound (short _ hs) hend
        have hprev : lookup tree (project4 v.2 v.1) = some k := by
          rw [project4_short _ _ (by omega)]
          exact hk
        have ht := ih hprev
        omega
      · have hlong : 4 ≤ v.1 := by omega
        have hnext : 4 ≤ nextWidth v.2 v.1 := by
          have hw := width_le_nextWidth v.2 v.1
          omega
        rw [project4_long _ _ hnext] at hend
        have hm : wordPrefix v.2 4 ∈ longPred 4 (wordPrefix (nextColumns v.2 v.1) 4) := by
          simp only [longPred, prefix_length, if_true]
          exact actual_mem_prefixPredecessors v.2 v.1 4 hv (by decide) hlong
        obtain ⟨s, hs, hsr⟩ := checkedRows_closed rows hend hm
        have hprev : lookup tree (project4 v.2 v.1) = some s := by
          rw [project4_long _ _ hlong]
          exact hs
        have ht := ih hprev
        omega

#print axioms project4_short
#print axioms shortWords3_complete
#print axioms shortWords3_count
#print axioms shortDescentOK_sound
#print axioms actual_iterPairs_rank4

end FourColumnKernel
