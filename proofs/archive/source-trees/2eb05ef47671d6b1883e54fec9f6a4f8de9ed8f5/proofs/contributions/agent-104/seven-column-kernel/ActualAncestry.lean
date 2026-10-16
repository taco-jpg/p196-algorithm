import ActualPrefix
import ShortBoundary
import LongRowsBase
import PalindromeBridge

/-!
# Actual ordinary-integer ancestry from finite seven-column checks

This module connects checked finite rows to the actual changing-width pair
trajectory of a positive ordinary integer. It handles every short source
by the exact short-word enumeration, and every long source by the proved
complete inverse enumeration. No ancestry bound is assumed.

The final theorems retain three concrete finite certificate premises:
all long rows pass, every short-source image is absent from the rank tree,
and every possible 739 last-predecessor projection has rank at most 38.
Supplying those checks yields the integer ancestry bound 39 and then the
all-time exclusion of 739-prefix palindromes from the ordinary 196 orbit.
-/

namespace SevenColumnKernel.ActualAncestry

open DecimalDigits FoldedDecimal Lychrel196 OverflowCarryNormalization
open NormalizationBridge CarryHistory SevenColumnProjection
open SevenColumn.Certificate SevenColumn.ShortBoundary
open SevenColumnKernel.PalindromeBridge

/-- Retain the complete exact short word, or seven columns of a long word. -/
def project (q : Nat → Nat) (L : Nat) : List Nat :=
  wordPrefix q (min L 7)

theorem project_short (q : Nat → Nat) (L : Nat) (hL : L ≤ 7) :
    project q L = wordOf q L := by
  simp only [project, Nat.min_eq_left hL, wordPrefix_eq_range_map, wordOf]

theorem project_long (q : Nat → Nat) (L : Nat) (hL : 7 ≤ L) :
    project q L = wordPrefix q 7 := by
  simp only [project, Nat.min_eq_right hL]

theorem project_congr (q r : Nat → Nat) (L : Nat)
    (h : ∀ i, i < L → q i = r i) : project q L = project r L := by
  simp only [project, wordPrefix_eq_range_map]
  apply List.map_congr_left
  intro i hi
  apply h
  have hh := List.mem_range.mp hi
  omega

theorem width_le_nextWidth (q : Nat → Nat) (L : Nat) :
    L ≤ nextWidth q L := by
  unfold nextWidth
  split <;> omega

/-- Exact semantic rank theorem. The endpoint lies in the checked tree;
short sources are excluded by the complete finite short-word check, while
actual long transitions are covered by `prefixPredecessors`. -/
theorem actual_iterPairs_rank
    {tree : RankTree} (rows : CheckedRows tree (longPred 7))
    (short : ∀ s ∈ shortWords, lookup tree (nextWord s) = none)
    (q : Nat → Nat) (L : Nat) (ha : Admissible L q)
    (t : Nat) {r : Nat}
    (hend : lookup tree (project (iterPairs q L t).2 (iterPairs q L t).1) = some r) :
    t ≤ r := by
  induction t generalizing r with
  | zero => omega
  | succ t ih =>
      let v := iterPairs q L t
      have hv : Admissible v.1 v.2 := iterPairs_admissible q L t ha
      change lookup tree (project (nextColumns v.2 v.1) (nextWidth v.2 v.1)) = some r
        at hend
      by_cases hshort : v.1 < 7
      · have hn := short_lookup_exclusion (lookup tree) short v.2 v.1 hv hshort
        rw [project_short _ _ (short_next_width v.2 v.1 hshort), hn] at hend
        contradiction
      · have hlong : 7 ≤ v.1 := by omega
        have hnext : 7 ≤ nextWidth v.2 v.1 := by
          have hw := width_le_nextWidth v.2 v.1
          omega
        rw [project_long _ _ hnext] at hend
        have hm : wordPrefix v.2 7 ∈ longPred 7 (wordPrefix (nextColumns v.2 v.1) 7) := by
          simp only [longPred, prefix_length, if_true]
          exact actual_mem_prefixPredecessors v.2 v.1 7 hv (by decide) hlong
        obtain ⟨s, hs, hsr⟩ := checkedRows_closed rows hend hm
        have hprev : lookup tree (project v.2 v.1) = some s := by
          rw [project_long _ _ hlong]
          exact hs
        have ht := ih hprev
        omega

/-- Decimal index for the four free digits after 739. -/
def targetInitialWord (i : Nat) : List Nat :=
  [7, 3, 9, i / 1000, (i / 100) % 10, (i / 10) % 10, i % 10]

/-- Exact finite superset of every possible last-predecessor projection.
The short case has width six; long cases permit all four remaining digits. -/
def targetInitialWords : List (List Nat) :=
  [7, 3, 9, 9, 3, 7] :: (List.range 10000).map targetInitialWord

/-- This converts separately checked decimal indices and the sole short
target to the uniform finite initial-family check consumed below. -/
theorem initialWords_checked_of_index_checks (tree : RankTree) (bound : Nat)
    (hshort : checkInitial tree bound [7, 3, 9, 9, 3, 7] = true)
    (hlong : ∀ i, i < 10000 → checkInitial tree bound (targetInitialWord i) = true) :
    ∀ p ∈ targetInitialWords, checkInitial tree bound p = true := by
  intro p hp
  simp only [targetInitialWords, List.mem_cons, List.mem_map, List.mem_range] at hp
  rcases hp with rfl | ⟨i, hi, rfl⟩
  · exact hshort
  · exact hlong i hi

/-- Admissibility removes every short width except six: width three and
four contradict symmetry; width five would have the odd middle column 9. -/
theorem short_target_unique (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 3 ≤ L) (hshort : L < 7)
    (hprefix : q 0 = 7 ∧ q 1 = 3 ∧ q 2 = 9) :
    L = 6 ∧ project q L = [7, 3, 9, 9, 3, 7] := by
  have hcases : L = 3 ∨ L = 4 ∨ L = 5 ∨ L = 6 := by omega
  rcases hcases with rfl | rfl | rfl | rfl
  · have hs : q 0 = q 2 := ha.2.2.2.1 0 (by omega)
    omega
  · have hs : q 1 = q 2 := ha.2.2.2.1 1 (by omega)
    omega
  · have hc := ha.2.2.2.2 2 (by omega) (by omega)
    omega
  · have h3 : q 3 = q 2 := ha.2.2.2.1 3 (by omega)
    have h4 : q 4 = q 1 := ha.2.2.2.1 4 (by omega)
    have h5 : q 5 = q 0 := ha.2.2.2.1 5 (by omega)
    refine ⟨rfl, ?_⟩
    change segment q 0 6 = [7, 3, 9, 9, 3, 7]
    simp [segment, hprefix.1, hprefix.2.1,
      hprefix.2.2, h3, h4, h5]

/-- Every actual admissible low word beginning 739 is in the finite
initial family, without restricting the length or unretained interior. -/
theorem target_project_mem_initialWords (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 3 ≤ L)
    (hsmall : ∀ i, i < L → q i ≤ 9)
    (hprefix : q 0 = 7 ∧ q 1 = 3 ∧ q 2 = 9) :
    project q L ∈ targetInitialWords := by
  by_cases hshort : L < 7
  · have he := (short_target_unique q L ha hL hshort hprefix).2
    simp only [he, targetInitialWords, List.mem_cons, true_or]
  · have hlong : 7 ≤ L := by omega
    have h3 := hsmall 3 (by omega)
    have h4 := hsmall 4 (by omega)
    have h5 := hsmall 5 (by omega)
    have h6 := hsmall 6 (by omega)
    let i := 1000 * q 3 + 100 * q 4 + 10 * q 5 + q 6
    have hi : i < 10000 := by dsimp [i]; omega
    have he : targetInitialWord i = project q L := by
      rw [project_long q L hlong]
      simp only [targetInitialWord, wordPrefix, segment, hprefix.1,
        hprefix.2.1, hprefix.2.2]
      have hdiv3 : i / 1000 = q 3 := by dsimp [i]; omega
      have hdiv4 : (i / 100) % 10 = q 4 := by dsimp [i]; omega
      have hdiv5 : (i / 10) % 10 = q 5 := by dsimp [i]; omega
      have hmod6 : i % 10 = q 6 := by dsimp [i]; omega
      rw [hdiv3, hdiv4, hdiv5, hmod6]
    simp only [targetInitialWords, List.mem_cons, List.mem_map, List.mem_range]
    exact Or.inr ⟨i, hi, he⟩

/-- The exact final ordinary reverse-and-add step produces an initial
certificate word. This is where palindromicity and the leading digit 7
force equal widths and all actual carries to vanish. -/
theorem canonical_last_step_initial
    {n P L : Nat} {d : Nat → Nat}
    (hsource : Canonical n d L) (hstep : step n = P)
    (hP : PalindromeStarts739 P) :
    project (columnSum d L) L ∈ targetInitialWords := by
  obtain ⟨hpal, e, W, htarget, hW, h7, h3, h9⟩ := hP
  have hlead : 1 < e (W - 1) := by omega
  obtain ⟨hwidth, _, hpair, hsmall⟩ :=
    canonical_last_step hsource htarget hstep hpal hlead
  have hp : Palindrome (value e W) := by
    rw [htarget.2.2.2]
    exact hpal
  have hsym := (palindrome_value_iff e W htarget.2.1
    (Or.inr htarget.2.2.1)).mp hp
  apply target_project_mem_initialWords (columnSum d L) L
    (canonical_admissible n d L hsource) (by omega) hsmall
  refine ⟨?_, ?_, ?_⟩
  · rw [hpair 0 (by omega), hsym 0 (by omega)]
    simpa using h7
  · rw [hpair 1 (by omega), hsym 1 (by omega)]
    simpa only [Nat.sub_sub] using h3
  · rw [hpair 2 (by omega), hsym 2 (by omega)]
    simpa only [Nat.sub_sub] using h9

/-- Three finite certificate checks imply the genuine ordinary-integer
ancestry bound, including arbitrary positive sources and arbitrary widths. -/
theorem ancestry_bound39_of_finite_checks
    (tree : RankTree) (rows : CheckedRows tree (longPred 7))
    (short : ∀ s ∈ shortWords, lookup tree (nextWord s) = none)
    (initial : ∀ p ∈ targetInitialWords, checkInitial tree 38 p = true) :
    ∀ A P t, 0 < A → PalindromeStarts739 P → orbit A t = P → t ≤ 39 := by
  intro A P t hA hP hreach
  cases t with
  | zero => omega
  | succ t =>
      obtain ⟨d, L, hcan⟩ := canonical_exists A hA
      let q := columnSum d L
      have ha : Admissible L q := canonical_admissible A d L hcan
      obtain ⟨e, he, hrep⟩ := iterPairs_representation A d q L t hcan (fun _ _ => rfl)
      have hlast : step (orbit A t) = P := hreach
      have hm := canonical_last_step_initial he hlast hP
      have hproj := project_congr (columnSum e (iterPairs q L t).1)
        (iterPairs q L t).2 (iterPairs q L t).1 hrep
      rw [hproj] at hm
      obtain ⟨r, hr, hb⟩ := checkInitial_sound (initial _ hm)
      have ht := actual_iterPairs_rank rows short q L ha t hr
      omega

/-- Supplying the three explicit finite checks proves all-time ordinary
196 avoidance of the 739-palindrome family. This is not full Lychrelness. -/
theorem no_196_739_palindrome_of_finite_checks
    (tree : RankTree) (rows : CheckedRows tree (longPred 7))
    (short : ∀ s ∈ shortWords, lookup tree (nextWord s) = none)
    (initial : ∀ p ∈ targetInitialWords, checkInitial tree 38 p = true) :
    ∀ t, ¬ PalindromeStarts739 (orbit 196 t) := by
  exact no_196_739_palindrome_of_ancestry_bound39
    (ancestry_bound39_of_finite_checks tree rows short initial)

#print axioms actual_iterPairs_rank
#print axioms short_target_unique
#print axioms target_project_mem_initialWords
#print axioms canonical_last_step_initial
#print axioms ancestry_bound39_of_finite_checks
#print axioms no_196_739_palindrome_of_finite_checks

end SevenColumnKernel.ActualAncestry
