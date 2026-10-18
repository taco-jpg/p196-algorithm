import P196.Agent104Prefix739.ActualAncestry

/-!
# Prefix-parametric seven-column ancestry endpoint (Agent #118)

This module generalizes the accepted 739 endpoint of Agent #104
(`SevenColumnKernel.ActualAncestry`, `SevenColumnKernel.Finite739`) in two
ways, without editing any of Agent #104's files:

* the target family is any palindrome whose canonical numeral begins with
  three given digits `a, b, c` with `2 ≤ a` (a leading digit above one rules
  out a final overflow, exactly as in `PalindromeBridge.canonical_last_step`);
* the short-source premise is weakened from "no exact short image lies in the
  rank tree" to *short-transition rank descent*: whenever the exact image of a
  short admissible source word lies in the tree with rank `r`, the source word
  itself lies in the tree with rank `< r`.  The first premise holds for 739 but
  fails for 218, 777, 217 and 620, whose certificates contain genuine short
  transitions.

The final theorems keep three explicit finite premises (all long rows, short
descent, initial-family coverage).  Concrete instances discharge them by
kernel reduction in separate modules.  Nothing here concerns any particular
prefix, and nothing here asserts that 196 is a Lychrel number.
-/

namespace Agent118.PrefixKernel

open DecimalDigits FoldedDecimal Lychrel196 OverflowCarryNormalization
open NormalizationBridge CarryHistory SevenColumnProjection
open SevenColumn.Certificate SevenColumn.ShortBoundary
open SevenColumnKernel.PalindromeBridge SevenColumnKernel.ActualAncestry

/-! ## Target family -/

/-- An ordinary numeral has leading decimal digits `a, b, c`. Width is exact
and digits are indexed from the units end, as in `PalindromeBridge.Starts739`. -/
def Starts3 (a b c P : Nat) : Prop :=
  ∃ e W, Canonical P e W ∧ 3 ≤ W ∧
    e (W - 1) = a ∧ e (W - 2) = b ∧ e (W - 3) = c

/-- The target family. Palindromicity is explicit. -/
def PalindromeStarts3 (a b c P : Nat) : Prop :=
  Palindrome P ∧ Starts3 a b c P

/-- Statement-fidelity check: at `7, 3, 9` this is definitionally Agent
#104's accepted target family. -/
theorem palindromeStarts3_739_iff (P : Nat) :
    PalindromeStarts3 7 3 9 P ↔ PalindromeStarts739 P := Iff.rfl

/-! ## Short-transition rank descent -/

/-- Executable short-transition check for one exact short source word. -/
def shortDescentOK (tree : RankTree) (s : List Nat) : Bool :=
  match lookup tree (nextWord s) with
  | none => true
  | some r => checkBelow tree r s

/-- Every exact short source whose image is ranked is itself ranked lower. -/
def ShortDescent (tree : RankTree) : Prop :=
  ∀ s ∈ shortWords, shortDescentOK tree s = true

theorem shortDescentOK_sound {tree : RankTree} {s : List Nat} {r : Nat}
    (h : shortDescentOK tree s = true) (hr : lookup tree (nextWord s) = some r) :
    ∃ k, lookup tree s = some k ∧ k < r := by
  unfold shortDescentOK at h
  rw [hr] at h
  exact checkBelow_sound h

/-- The previous exclusion premise is a special case of rank descent. -/
theorem shortDescent_of_exclusion {tree : RankTree}
    (h : ∀ s ∈ shortWords, lookup tree (nextWord s) = none) : ShortDescent tree := by
  intro s hs
  unfold shortDescentOK
  rw [h s hs]

/-- Exact semantic rank theorem with short-transition rank descent. The
endpoint lies in the checked tree; an actual short source is handled by its
exact complete word, and an actual long source by the proved complete inverse. -/
theorem actual_iterPairs_rank_desc
    {tree : RankTree} (rows : CheckedRows tree (longPred 7))
    (short : ShortDescent tree)
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
      · have hmem : wordOf v.2 v.1 ∈ shortWords :=
          shortWords_complete v.2 v.1 hv hshort
        have himg : project (nextColumns v.2 v.1) (nextWidth v.2 v.1) =
            nextWord (wordOf v.2 v.1) := by
          rw [project_short _ _ (short_next_width v.2 v.1 hshort), nextWord_wordOf]
        rw [himg] at hend
        obtain ⟨k, hk, hlt⟩ := shortDescentOK_sound (short _ hmem) hend
        have hprev : lookup tree (project v.2 v.1) = some k := by
          rw [project_short _ _ (by omega)]
          exact hk
        have ht := ih hprev
        omega
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

/-! ## Initial family of possible last-predecessor projections -/

/-- Long initial words: the prefix followed by four free decimal digits. -/
def targetInitialWord (a b c i : Nat) : List Nat :=
  [a, b, c, i / 1000, (i / 100) % 10, (i / 10) % 10, i % 10]

/-- Exact short completion of a palindromic digit word of width 3..6. -/
def shortTarget (a b c : Nat) : Nat → List Nat
  | 3 => [a, b, c]
  | 4 => [a, b, c, a]
  | 5 => [a, b, c, b, a]
  | 6 => [a, b, c, c, b, a]
  | _ => []

/-- Exactly the short widths that admissibility permits for this prefix:
symmetry, and an even center for odd width. -/
def shortTargetAdmitted (a b c : Nat) : Nat → Bool
  | 3 => c == a && b % 2 == 0
  | 4 => c == b
  | 5 => c % 2 == 0
  | 6 => true
  | _ => false

def shortTargets (a b c : Nat) : List (List Nat) :=
  ([3, 4, 5, 6].filter (shortTargetAdmitted a b c)).map (shortTarget a b c)

/-- Finite superset of every possible last-predecessor projection. -/
def targetInitialWords (a b c : Nat) : List (List Nat) :=
  shortTargets a b c ++ (List.range 10000).map (targetInitialWord a b c)

theorem shortTarget_mem {a b c L : Nat} (hL : L = 3 ∨ L = 4 ∨ L = 5 ∨ L = 6)
    (hadm : shortTargetAdmitted a b c L = true) :
    shortTarget a b c L ∈ shortTargets a b c := by
  simp only [shortTargets, List.mem_map, List.mem_filter]
  refine ⟨L, ⟨?_, hadm⟩, rfl⟩
  rcases hL with rfl | rfl | rfl | rfl <;> simp

/-- Admissibility leaves only the admitted short completions. -/
theorem short_target_mem (a b c : Nat) (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 3 ≤ L) (hshort : L < 7)
    (hprefix : q 0 = a ∧ q 1 = b ∧ q 2 = c) :
    project q L ∈ shortTargets a b c := by
  obtain ⟨h0, h1, h2⟩ := hprefix
  have hcases : L = 3 ∨ L = 4 ∨ L = 5 ∨ L = 6 := by omega
  rcases hcases with rfl | rfl | rfl | rfl
  · have hs : q 2 = q 0 := ha.2.2.2.1 2 (by omega)
    have hc := ha.2.2.2.2 1 (by omega) (by omega)
    have he : project q 3 = shortTarget a b c 3 := by
      rw [project_short _ _ (by omega)]
      simp [wordOf, List.range_succ, shortTarget, h0, h1, h2]
    rw [he]
    apply shortTarget_mem (by omega)
    simp only [shortTargetAdmitted, Bool.and_eq_true, beq_iff_eq]
    omega
  · have hs2 : q 2 = q 1 := ha.2.2.2.1 2 (by omega)
    have hs3 : q 3 = q 0 := ha.2.2.2.1 3 (by omega)
    have he : project q 4 = shortTarget a b c 4 := by
      rw [project_short _ _ (by omega)]
      simp [wordOf, List.range_succ, shortTarget, h0, h1, h2, hs3]
    rw [he]
    apply shortTarget_mem (by omega)
    simp only [shortTargetAdmitted, beq_iff_eq]
    omega
  · have hs3 : q 3 = q 1 := ha.2.2.2.1 3 (by omega)
    have hs4 : q 4 = q 0 := ha.2.2.2.1 4 (by omega)
    have hc := ha.2.2.2.2 2 (by omega) (by omega)
    have he : project q 5 = shortTarget a b c 5 := by
      rw [project_short _ _ (by omega)]
      simp [wordOf, List.range_succ, shortTarget, h0, h1, h2, hs3, hs4]
    rw [he]
    apply shortTarget_mem (by omega)
    simp only [shortTargetAdmitted, beq_iff_eq]
    omega
  · have hs3 : q 3 = q 2 := ha.2.2.2.1 3 (by omega)
    have hs4 : q 4 = q 1 := ha.2.2.2.1 4 (by omega)
    have hs5 : q 5 = q 0 := ha.2.2.2.1 5 (by omega)
    have he : project q 6 = shortTarget a b c 6 := by
      rw [project_short _ _ (by omega)]
      simp [wordOf, List.range_succ, shortTarget, h0, h1, h2, hs3, hs4, hs5]
    rw [he]
    exact shortTarget_mem (by omega) rfl

/-- Every actual admissible low word with the prefix `a, b, c` and digit-sized
columns lies in the finite initial family, at every width. -/
theorem target_project_mem_initialWords (a b c : Nat) (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hL : 3 ≤ L)
    (hsmall : ∀ i, i < L → q i ≤ 9)
    (hprefix : q 0 = a ∧ q 1 = b ∧ q 2 = c) :
    project q L ∈ targetInitialWords a b c := by
  by_cases hshort : L < 7
  · exact List.mem_append_left _ (short_target_mem a b c q L ha hL hshort hprefix)
  · have hlong : 7 ≤ L := by omega
    have h3 := hsmall 3 (by omega)
    have h4 := hsmall 4 (by omega)
    have h5 := hsmall 5 (by omega)
    have h6 := hsmall 6 (by omega)
    let i := 1000 * q 3 + 100 * q 4 + 10 * q 5 + q 6
    have hi : i < 10000 := by dsimp [i]; omega
    have he : targetInitialWord a b c i = project q L := by
      rw [project_long q L hlong]
      simp only [targetInitialWord, wordPrefix, segment, hprefix.1,
        hprefix.2.1, hprefix.2.2]
      have hdiv3 : i / 1000 = q 3 := by dsimp [i]; omega
      have hdiv4 : (i / 100) % 10 = q 4 := by dsimp [i]; omega
      have hdiv5 : (i / 10) % 10 = q 5 := by dsimp [i]; omega
      have hmod6 : i % 10 = q 6 := by dsimp [i]; omega
      rw [hdiv3, hdiv4, hdiv5, hmod6]
    apply List.mem_append_right
    simp only [List.mem_map, List.mem_range]
    exact ⟨i, hi, he⟩

/-- The exact final ordinary reverse-and-add step produces an initial word.
Palindromicity and the leading digit `a ≥ 2` force equal widths and vanishing
carries (`PalindromeBridge.canonical_last_step`). -/
theorem canonical_last_step_initial (a b c : Nat) (ha2 : 2 ≤ a)
    {n P L : Nat} {d : Nat → Nat}
    (hsource : Canonical n d L) (hstep : step n = P)
    (hP : PalindromeStarts3 a b c P) :
    project (columnSum d L) L ∈ targetInitialWords a b c := by
  obtain ⟨hpal, e, W, htarget, hW, ha, hb, hc⟩ := hP
  have hlead : 1 < e (W - 1) := by omega
  obtain ⟨hwidth, _, hpair, hsmall⟩ :=
    canonical_last_step hsource htarget hstep hpal hlead
  have hp : Palindrome (value e W) := by
    rw [htarget.2.2.2]
    exact hpal
  have hsym := (palindrome_value_iff e W htarget.2.1
    (Or.inr htarget.2.2.1)).mp hp
  apply target_project_mem_initialWords a b c (columnSum d L) L
    (canonical_admissible n d L hsource) (by omega) hsmall
  refine ⟨?_, ?_, ?_⟩
  · rw [hpair 0 (by omega), hsym 0 (by omega)]
    simpa using ha
  · rw [hpair 1 (by omega), hsym 1 (by omega)]
    simpa only [Nat.sub_sub] using hb
  · rw [hpair 2 (by omega), hsym 2 (by omega)]
    simpa only [Nat.sub_sub] using hc

/-! ## Endpoints -/

/-- Three finite checks imply the ordinary-integer ancestry bound for the
prefix family, for arbitrary positive sources and arbitrary widths. -/
theorem ancestry_bound_of_finite_checks (a b c bound : Nat) (ha2 : 2 ≤ a)
    (tree : RankTree) (rows : CheckedRows tree (longPred 7))
    (short : ShortDescent tree)
    (initial : ∀ p ∈ targetInitialWords a b c, checkInitial tree bound p = true) :
    ∀ A P t, 0 < A → PalindromeStarts3 a b c P → orbit A t = P → t ≤ bound + 1 := by
  intro A P t hA hP hreach
  cases t with
  | zero => omega
  | succ t =>
      obtain ⟨d, L, hcan⟩ := canonical_exists A hA
      let q := columnSum d L
      have ha : Admissible L q := canonical_admissible A d L hcan
      obtain ⟨e, he, hrep⟩ := iterPairs_representation A d q L t hcan (fun _ _ => rfl)
      have hlast : step (orbit A t) = P := hreach
      have hm := canonical_last_step_initial a b c ha2 he hlast hP
      have hproj := project_congr (columnSum e (iterPairs q L t).1)
        (iterPairs q L t).2 (iterPairs q L t).1 hrep
      rw [hproj] at hm
      obtain ⟨r, hr, hb⟩ := checkInitial_sound (initial _ hm)
      have ht := actual_iterPairs_rank_desc rows short q L ha t hr
      omega

/-- Supplying the three finite checks, with `bound + 1 ≤ 100`, excludes the
prefix family from the ordinary 196 orbit at every time. Not Lychrelness. -/
theorem no_196_of_finite_checks (a b c bound : Nat) (ha2 : 2 ≤ a)
    (hbound : bound + 1 ≤ 100)
    (tree : RankTree) (rows : CheckedRows tree (longPred 7))
    (short : ShortDescent tree)
    (initial : ∀ p ∈ targetInitialWords a b c, checkInitial tree bound p = true) :
    ∀ t, ¬ PalindromeStarts3 a b c (orbit 196 t) :=
  no_196_target_of_ancestry_bound (PalindromeStarts3 a b c) (bound + 1) hbound
    (fun _ h => h.1) (ancestry_bound_of_finite_checks a b c bound ha2 tree rows short initial)

#print axioms palindromeStarts3_739_iff
#print axioms shortDescent_of_exclusion
#print axioms actual_iterPairs_rank_desc
#print axioms short_target_mem
#print axioms target_project_mem_initialWords
#print axioms canonical_last_step_initial
#print axioms ancestry_bound_of_finite_checks
#print axioms no_196_of_finite_checks

end Agent118.PrefixKernel
