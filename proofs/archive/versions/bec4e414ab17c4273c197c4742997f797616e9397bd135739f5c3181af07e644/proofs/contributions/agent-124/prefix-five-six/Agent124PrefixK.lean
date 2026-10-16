import ActualPrefix
import FastRowsBase
import PalindromeBridge
import ShortBoundary

/-!
# Width-generic prefix-ancestry endpoint (Agent #124)

This module generalizes the accepted seven-column 739 endpoint of Agent #104
(`SevenColumnKernel.ActualAncestry`) from the fixed certificate width seven to
an arbitrary certificate width `k ≥ 3`, and from the fixed prefix 739 to any
three leading digits `a, b, c` with `2 ≤ a`.  None of Agent #104's files is
edited; the long-word inverse (`PrefixInverse`, `FastInverse`), the actual
arbitrary-width projection (`ActualPrefix`), the certificate soundness
(`PrefixCertificate`, `LongRowsBase`, `FastRowsBase`) and the last-step bridge
(`PalindromeBridge`) are reused unchanged.

New ingredients:

* `symWords n`: an executable enumeration of all admissible pair words of
  width `n`, generated from their halves, with a completeness proof for every
  `n` (`wordOf_mem_symWords`).  Hence every actual short state of width
  `n < k` occurs in the finite list `shortWordsK k`.
* Short-transition rank descent: whenever the exact image of a short source
  word lies in the rank tree with rank `r`, the source word lies in the tree
  with rank `< r`.  (The analogous k = 7 lemma is independently written by
  Agent #118 for its own instances; the k = 4 instance is Agent #119's.)
* `initialWordsK k a b c`: an executable finite superset of every possible
  width-`k` projection of the last predecessor of a palindrome beginning
  `a, b, c`, with a proof of coverage for every width.

The final theorems keep three explicit finite premises: all long rows pass,
short descent holds, and every initial word has rank at most `bound`.
Concrete instances discharge them by kernel reduction in separate modules.
Nothing here asserts that 196 is a Lychrel number.
-/

namespace Agent124.PrefixK

open DecimalDigits FoldedDecimal Lychrel196 OverflowCarryNormalization
open NormalizationBridge CarryHistory SevenColumnProjection
open SevenColumn.Certificate SevenColumn.ShortBoundary
open SevenColumnKernel.PalindromeBridge

/-! ## Generic enumeration of admissible short words -/

/-- All lists of length `m` with entries below 19. -/
def lists19 : Nat → List (List Nat)
  | 0 => [[]]
  | m + 1 => (List.range 19).flatMap fun a => (lists19 m).map (a :: ·)

theorem mem_lists19 : ∀ (m : Nat) (h : List Nat), h.length = m →
    (∀ x ∈ h, x < 19) → h ∈ lists19 m
  | 0, h, hl, _ => by
      have : h = [] := List.eq_nil_of_length_eq_zero hl
      subst h
      simp [lists19]
  | m + 1, h, hl, hb => by
      cases h with
      | nil => simp at hl
      | cons x t =>
          simp only [lists19, List.mem_flatMap, List.mem_range, List.mem_map]
          refine ⟨x, hb x (by simp), t, ?_, rfl⟩
          apply mem_lists19 m t (by simpa using hl)
          intro y hy
          exact hb y (by simp [hy])

/-- Mirror a half word to a symmetric word of width `n`. -/
def mirror (n : Nat) (h : List Nat) : List Nat :=
  (List.range n).map fun i => h.getD (min i (n - 1 - i)) 0

/-- Positive outer column, and an even center for odd width. -/
def symOK (n : Nat) (w : List Nat) : Bool :=
  decide (0 < w.getD 0 0) && (n % 2 == 0 || (w.getD (n / 2) 0) % 2 == 0)

/-- Every admissible pair word of width `n` (proved in `wordOf_mem_symWords`). -/
def symWords (n : Nat) : List (List Nat) :=
  ((lists19 ((n + 1) / 2)).map (mirror n)).filter (symOK n)

/-- All admissible short words of widths below `k`. -/
def shortWordsK (k : Nat) : List (List Nat) :=
  (List.range k).flatMap symWords

theorem getD_range_map (f : Nat → Nat) (n i : Nat) (hi : i < n) :
    ((List.range n).map f).getD i 0 = f i := by
  simp [List.getD_eq_getElem?_getD, List.getElem?_map, hi]

theorem wordOf_mem_symWords (q : Nat → Nat) (n : Nat) (ha : Admissible n q) :
    wordOf q n ∈ symWords n := by
  rcases ha with ⟨hpos, houter, hbound, hsymm, hcenter⟩
  let h := (List.range ((n + 1) / 2)).map q
  have hmem : h ∈ lists19 ((n + 1) / 2) := by
    apply mem_lists19
    · simp [h]
    · intro x hx
      simp only [h, List.mem_map, List.mem_range] at hx
      obtain ⟨i, hi, rfl⟩ := hx
      have := hbound i (by omega)
      omega
  have hmirror : mirror n h = wordOf q n := by
    unfold mirror wordOf
    apply List.map_congr_left
    intro i hi
    have hi' := List.mem_range.mp hi
    have hmin : min i (n - 1 - i) < (n + 1) / 2 := by omega
    rw [getD_range_map q _ _ hmin]
    by_cases hc : i ≤ n - 1 - i
    · rw [Nat.min_eq_left hc]
    · rw [Nat.min_eq_right (by omega)]
      exact (hsymm i hi').symm
  have hok : symOK n (wordOf q n) = true := by
    unfold symOK wordOf
    rw [getD_range_map q n 0 hpos]
    simp only [Bool.and_eq_true, decide_eq_true_eq, Bool.or_eq_true, beq_iff_eq]
    refine ⟨houter, ?_⟩
    by_cases he : n % 2 = 0
    · exact Or.inl he
    · right
      rw [getD_range_map q n (n / 2) (by omega)]
      exact hcenter (n / 2) (by omega) (by omega)
  unfold symWords
  rw [List.mem_filter]
  refine ⟨?_, hok⟩
  rw [List.mem_map]
  exact ⟨h, hmem, hmirror⟩

theorem wordOf_mem_shortWordsK (q : Nat → Nat) (L k : Nat) (ha : Admissible L q)
    (hL : L < k) : wordOf q L ∈ shortWordsK k := by
  unfold shortWordsK
  rw [List.mem_flatMap]
  exact ⟨L, List.mem_range.mpr hL, wordOf_mem_symWords q L ha⟩

/-! ## Width-`k` projection and the actual rank theorem -/

/-- Retain the complete exact short word, or `k` columns of a long word. -/
def projectK (k : Nat) (q : Nat → Nat) (L : Nat) : List Nat :=
  wordPrefix q (min L k)

theorem projectK_short (k : Nat) (q : Nat → Nat) (L : Nat) (hL : L ≤ k) :
    projectK k q L = wordOf q L := by
  simp only [projectK, Nat.min_eq_left hL, wordPrefix_eq_range_map, wordOf]

theorem projectK_long (k : Nat) (q : Nat → Nat) (L : Nat) (hL : k ≤ L) :
    projectK k q L = wordPrefix q k := by
  simp only [projectK, Nat.min_eq_right hL]

theorem projectK_congr (k : Nat) (q r : Nat → Nat) (L : Nat)
    (h : ∀ i, i < L → q i = r i) : projectK k q L = projectK k r L := by
  simp only [projectK, wordPrefix_eq_range_map]
  apply List.map_congr_left
  intro i hi
  apply h
  have hh := List.mem_range.mp hi
  omega

theorem width_le_nextWidth (q : Nat → Nat) (L : Nat) : L ≤ nextWidth q L := by
  unfold nextWidth
  split <;> omega

theorem nextWidth_le_succ (q : Nat → Nat) (L : Nat) : nextWidth q L ≤ L + 1 := by
  unfold nextWidth
  split <;> omega

/-- Executable short-transition check for one exact short source word. -/
def shortDescentOK (tree : RankTree) (s : List Nat) : Bool :=
  match lookup tree (nextWord s) with
  | none => true
  | some r => checkBelow tree r s

/-- Every exact short source whose image is ranked is itself ranked lower. -/
def ShortDescentK (k : Nat) (tree : RankTree) : Prop :=
  ∀ s ∈ shortWordsK k, shortDescentOK tree s = true

theorem shortDescentOK_sound {tree : RankTree} {s : List Nat} {r : Nat}
    (h : shortDescentOK tree s = true) (hr : lookup tree (nextWord s) = some r) :
    ∃ m, lookup tree s = some m ∧ m < r := by
  unfold shortDescentOK at h
  rw [hr] at h
  exact checkBelow_sound h

theorem shortDescentK_of_all {k : Nat} {tree : RankTree}
    (h : (shortWordsK k).all (shortDescentOK tree) = true) : ShortDescentK k tree :=
  fun s hs => List.all_eq_true.mp h s hs

/-- Exact semantic rank theorem for every certificate width `k > 0`.
An actual short source (width below `k`) is handled by its exact complete
word and short descent; an actual long source by the proved complete
inverse of `prefixPredecessors`. -/
theorem actual_iterPairs_rank_k {k : Nat} (hk : 0 < k) {tree : RankTree}
    (rows : CheckedRows tree (longPred k)) (short : ShortDescentK k tree)
    (q : Nat → Nat) (L : Nat) (ha : Admissible L q) (t : Nat) {r : Nat}
    (hend : lookup tree (projectK k (iterPairs q L t).2 (iterPairs q L t).1) = some r) :
    t ≤ r := by
  induction t generalizing r with
  | zero => omega
  | succ t ih =>
      let v := iterPairs q L t
      have hv : Admissible v.1 v.2 := iterPairs_admissible q L t ha
      change lookup tree (projectK k (nextColumns v.2 v.1) (nextWidth v.2 v.1)) = some r
        at hend
      by_cases hshort : v.1 < k
      · have hmem : wordOf v.2 v.1 ∈ shortWordsK k :=
          wordOf_mem_shortWordsK v.2 v.1 k hv hshort
        have hw : nextWidth v.2 v.1 ≤ k := by
          have := nextWidth_le_succ v.2 v.1
          omega
        have himg : projectK k (nextColumns v.2 v.1) (nextWidth v.2 v.1) =
            nextWord (wordOf v.2 v.1) := by
          rw [projectK_short _ _ _ hw, nextWord_wordOf]
        rw [himg] at hend
        obtain ⟨m, hm, hlt⟩ := shortDescentOK_sound (short _ hmem) hend
        have hprev : lookup tree (projectK k v.2 v.1) = some m := by
          rw [projectK_short _ _ _ (by omega)]
          exact hm
        have ht := ih hprev
        omega
      · have hlong : k ≤ v.1 := by omega
        have hnext : k ≤ nextWidth v.2 v.1 := by
          have hw := width_le_nextWidth v.2 v.1
          omega
        rw [projectK_long _ _ _ hnext] at hend
        have hm : wordPrefix v.2 k ∈ longPred k (wordPrefix (nextColumns v.2 v.1) k) := by
          simp only [longPred, prefix_length, if_true]
          exact actual_mem_prefixPredecessors v.2 v.1 k hv hk hlong
        obtain ⟨s, hs, hsr⟩ := checkedRows_closed rows hend hm
        have hprev : lookup tree (projectK k v.2 v.1) = some s := by
          rw [projectK_long _ _ _ hlong]
          exact hs
        have ht := ih hprev
        omega

/-! ## Target family -/

/-- An ordinary numeral has leading decimal digits `a, b, c`. Width is exact
and digits are indexed from the units end, as in `PalindromeBridge.Starts739`. -/
def Starts3 (a b c P : Nat) : Prop :=
  ∃ e W, Canonical P e W ∧ 3 ≤ W ∧
    e (W - 1) = a ∧ e (W - 2) = b ∧ e (W - 3) = c

/-- The target family. Palindromicity is explicit. -/
def PalStarts3 (a b c P : Nat) : Prop :=
  Palindrome P ∧ Starts3 a b c P

/-- Statement-fidelity check against Agent #104's accepted 739 family. -/
theorem palStarts3_739_iff (P : Nat) :
    PalStarts3 7 3 9 P ↔ PalindromeStarts739 P := Iff.rfl

/-! ## Initial family of possible last-predecessor projections -/

/-- All lists of length `m` with decimal-digit entries. -/
def digitLists : Nat → List (List Nat)
  | 0 => [[]]
  | m + 1 => (List.range 10).flatMap fun a => (digitLists m).map (a :: ·)

theorem mem_digitLists : ∀ (m : Nat) (h : List Nat), h.length = m →
    (∀ x ∈ h, x ≤ 9) → h ∈ digitLists m
  | 0, h, hl, _ => by
      have : h = [] := List.eq_nil_of_length_eq_zero hl
      subst h
      simp [digitLists]
  | m + 1, h, hl, hb => by
      cases h with
      | nil => simp at hl
      | cons x t =>
          simp only [digitLists, List.mem_flatMap, List.mem_range, List.mem_map]
          refine ⟨x, by have := hb x (by simp); omega, t, ?_, rfl⟩
          apply mem_digitLists m t (by simpa using hl)
          intro y hy
          exact hb y (by simp [hy])

/-- Index symmetry of a finite word. -/
def symB (w : List Nat) : Bool :=
  (List.range w.length).all fun i => w.getD i 0 == w.getD (w.length - 1 - i) 0

/-- Even center for odd width. -/
def centerB (w : List Nat) : Bool :=
  w.length % 2 == 0 || (w.getD (w.length / 2) 0) % 2 == 0

/-- A full-width word, or a symmetric short word with even odd center. -/
def initialOK (k : Nat) (w : List Nat) : Bool :=
  w.length == k || (symB w && centerB w)

/-- Finite superset of the width-`k` projections of every last predecessor of
a palindrome beginning `a, b, c`: lengths 3 .. k, digit entries. -/
def initialWordsK (k a b c : Nat) : List (List Nat) :=
  ((List.range (k - 2)).flatMap fun j =>
    (digitLists j).map ([a, b, c] ++ ·)).filter (initialOK k)

/-- Every actual admissible low word of digits beginning `a, b, c` projects
into the finite initial family, for every width at least three. -/
theorem target_project_mem_initialWordsK (k a b c : Nat) (hk : 3 ≤ k)
    (q : Nat → Nat) (L : Nat) (ha : Admissible L q) (hL : 3 ≤ L)
    (hsmall : ∀ i, i < L → q i ≤ 9)
    (hprefix : q 0 = a ∧ q 1 = b ∧ q 2 = c) :
    projectK k q L ∈ initialWordsK k a b c := by
  rcases ha with ⟨hpos, houter, hbound, hsymm, hcenter⟩
  let m := min L k
  have hm3 : 3 ≤ m := by omega
  have hmL : m ≤ L := by omega
  have hproj : projectK k q L = (List.range m).map q := by
    simp only [projectK, wordPrefix_eq_range_map]
    rfl
  -- split the range into the three prefix columns and the tail
  let tail := (List.range (m - 3)).map (fun j => q (j + 3))
  have hsplit : (List.range m).map q = [a, b, c] ++ tail := by
    apply List.ext_getElem
    · simp [tail]
      omega
    · intro i h1 h2
      simp only [List.getElem_map, List.getElem_range]
      by_cases hi : i < 3
      · have : i = 0 ∨ i = 1 ∨ i = 2 := by omega
        rcases this with rfl | rfl | rfl
        · simp [hprefix.1]
        · simp [hprefix.2.1]
        · simp [hprefix.2.2]
      · rw [List.getElem_append_right (by simp; omega)]
        simp only [List.length_cons, List.length_nil, tail, List.getElem_map,
          List.getElem_range]
        congr 1
        simp
        omega
  have htail : tail ∈ digitLists (m - 3) := by
    apply mem_digitLists
    · simp [tail]
    · intro x hx
      simp only [tail, List.mem_map, List.mem_range] at hx
      obtain ⟨j, hj, rfl⟩ := hx
      exact hsmall (j + 3) (by omega)
  have hok : initialOK k ((List.range m).map q) = true := by
    unfold initialOK
    simp only [Bool.or_eq_true, beq_iff_eq, Bool.and_eq_true, List.length_map,
      List.length_range]
    by_cases hlong : k ≤ L
    · left
      simp [m]
      omega
    · right
      have hmeq : m = L := by simp [m]; omega
      rw [hmeq]
      constructor
      · unfold symB
        simp only [List.length_map, List.length_range]
        apply List.all_eq_true.mpr
        intro i hi
        have hi' := List.mem_range.mp hi
        rw [getD_range_map q L i hi', getD_range_map q L (L - 1 - i) (by omega)]
        simpa using hsymm i hi'
      · unfold centerB
        simp only [List.length_map, List.length_range, Bool.or_eq_true, beq_iff_eq]
        by_cases he : L % 2 = 0
        · exact Or.inl he
        · right
          rw [getD_range_map q L (L / 2) (by omega)]
          exact hcenter (L / 2) (by omega) (by omega)
  rw [hproj]
  unfold initialWordsK
  rw [List.mem_filter]
  refine ⟨?_, hok⟩
  rw [List.mem_flatMap]
  refine ⟨m - 3, List.mem_range.mpr (by omega), ?_⟩
  rw [List.mem_map]
  exact ⟨tail, htail, hsplit.symm⟩

/-- The exact final ordinary reverse-and-add step produces an initial word.
A leading target digit at least two rules out a final overflow, so widths
agree and all carries vanish (Agent #104's `canonical_last_step`). -/
theorem canonical_last_step_initialK (k a b c : Nat) (hk : 3 ≤ k) (ha2 : 2 ≤ a)
    {n P L : Nat} {d : Nat → Nat}
    (hsource : Canonical n d L) (hstep : step n = P) (hP : PalStarts3 a b c P) :
    projectK k (columnSum d L) L ∈ initialWordsK k a b c := by
  obtain ⟨hpal, e, W, htarget, hW, hea, heb, hec⟩ := hP
  have hlead : 1 < e (W - 1) := by omega
  obtain ⟨hwidth, _, hpair, hsmall⟩ :=
    canonical_last_step hsource htarget hstep hpal hlead
  have hp : Palindrome (value e W) := by
    rw [htarget.2.2.2]
    exact hpal
  have hsym := (palindrome_value_iff e W htarget.2.1
    (Or.inr htarget.2.2.1)).mp hp
  apply target_project_mem_initialWordsK k a b c hk (columnSum d L) L
    (canonical_admissible n d L hsource) (by omega) hsmall
  refine ⟨?_, ?_, ?_⟩
  · rw [hpair 0 (by omega), hsym 0 (by omega)]
    simpa using hea
  · rw [hpair 1 (by omega), hsym 1 (by omega)]
    simpa only [Nat.sub_sub] using heb
  · rw [hpair 2 (by omega), hsym 2 (by omega)]
    simpa only [Nat.sub_sub] using hec

/-! ## Endpoints conditional on explicit finite checks -/

/-- Three finite certificate checks at width `k` imply the genuine
ordinary-integer ancestry bound `bound + 1` for every positive source and
every target width. -/
theorem ancestry_bound_of_checks (k a b c bound : Nat) (hk : 3 ≤ k) (ha2 : 2 ≤ a)
    (tree : RankTree) (rows : CheckedRows tree (longPred k))
    (short : ShortDescentK k tree)
    (initial : ∀ w ∈ initialWordsK k a b c, checkInitial tree bound w = true) :
    ∀ A P t, 0 < A → PalStarts3 a b c P → orbit A t = P → t ≤ bound + 1 := by
  intro A P t hA hP hreach
  cases t with
  | zero => omega
  | succ t =>
      obtain ⟨d, L, hcan⟩ := canonical_exists A hA
      let q := columnSum d L
      have hadm : Admissible L q := canonical_admissible A d L hcan
      obtain ⟨e, he, hrep⟩ := iterPairs_representation A d q L t hcan (fun _ _ => rfl)
      have hlast : step (orbit A t) = P := hreach
      have hm := canonical_last_step_initialK k a b c hk ha2 he hlast hP
      have hproj := projectK_congr k (columnSum e (iterPairs q L t).1)
        (iterPairs q L t).2 (iterPairs q L t).1 hrep
      rw [hproj] at hm
      obtain ⟨r, hr, hb⟩ := checkInitial_sound (initial _ hm)
      have ht := actual_iterPairs_rank_k (by omega) rows short q L hadm t hr
      omega

/-- All-time exclusion of the target family from the ordinary 196 orbit,
from the same finite checks, whenever the resulting bound is within the
kernel-checked first 100 iterates. -/
theorem no_196_of_checks (k a b c bound : Nat) (hk : 3 ≤ k) (ha2 : 2 ≤ a)
    (hb : bound + 1 ≤ 100)
    (tree : RankTree) (rows : CheckedRows tree (longPred k))
    (short : ShortDescentK k tree)
    (initial : ∀ w ∈ initialWordsK k a b c, checkInitial tree bound w = true) :
    ∀ t, ¬ PalStarts3 a b c (orbit 196 t) :=
  no_196_target_of_ancestry_bound (PalStarts3 a b c) (bound + 1) hb
    (fun _ h => h.1) (ancestry_bound_of_checks k a b c bound hk ha2 tree rows short initial)

/-- Boolean form of the initial premise, convenient for kernel reduction. -/
theorem initial_of_all {k a b c bound : Nat} {tree : RankTree}
    (h : (initialWordsK k a b c).all (checkInitial tree bound) = true) :
    ∀ w ∈ initialWordsK k a b c, checkInitial tree bound w = true :=
  fun w hw => List.all_eq_true.mp h w hw

end Agent124.PrefixK

#print axioms Agent124.PrefixK.mem_lists19
#print axioms Agent124.PrefixK.wordOf_mem_symWords
#print axioms Agent124.PrefixK.wordOf_mem_shortWordsK
#print axioms Agent124.PrefixK.actual_iterPairs_rank_k
#print axioms Agent124.PrefixK.target_project_mem_initialWordsK
#print axioms Agent124.PrefixK.canonical_last_step_initialK
#print axioms Agent124.PrefixK.ancestry_bound_of_checks
#print axioms Agent124.PrefixK.no_196_of_checks
