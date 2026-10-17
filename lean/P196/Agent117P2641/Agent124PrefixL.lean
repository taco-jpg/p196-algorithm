import P196.Agent117P2641.Agent124LeadOne

/-!
# Prefix-ancestry endpoints for digit prefixes of any length (Agent #124)

`Agent124.PrefixK`/`PrefixR`/`LeadOne` treat three leading digits.  This
module states the target family and the initial-family coverage for an
arbitrary list `pre` of leading digits (most significant first), with any
certificate width `k ≥ pre.length`.  The final overflow into the target is
excluded when the leading digit is at least two or some prefix digit is at
least three (`noOverflowPre`).  Certificates are consumed through the
abstract rank interface of `Agent124.PrefixR`, so the code-keyed checks of
`Agent124.CodeCert` apply unchanged.  Also included: list-valued endpoints
that cover many prefixes with a single Boolean initial check.
-/

namespace Agent124.PrefixL

open DecimalDigits FoldedDecimal Lychrel196 OverflowCarryNormalization
open NormalizationBridge CarryHistory SevenColumnProjection
open SevenColumn.Certificate SevenColumn.ShortBoundary
open SevenColumnKernel.PalindromeBridge Agent124.PrefixK Agent124.PrefixR Agent124.LeadOne

/-- An ordinary numeral begins with the digit list `pre`, most significant
first. Width is exact; digits are indexed from the units end. -/
def StartsL (pre : List Nat) (P : Nat) : Prop :=
  ∃ e W, Canonical P e W ∧ pre.length ≤ W ∧
    ∀ i, i < pre.length → e (W - 1 - i) = pre.getD i 0

/-- The target family. Palindromicity is explicit. -/
def PalStartsL (pre : List Nat) (P : Nat) : Prop :=
  Palindrome P ∧ StartsL pre P

/-- Statement fidelity: three-digit lists give exactly `PalStarts3`. -/
theorem palStartsL_three_iff (a b c P : Nat) :
    PalStartsL [a, b, c] P ↔ PalStarts3 a b c P := by
  constructor
  · rintro ⟨hp, e, W, hc, hW, h⟩
    refine ⟨hp, e, W, hc, by simpa using hW, ?_, ?_, ?_⟩
    · simpa using h 0 (by simp)
    · simpa using h 1 (by simp)
    · have := h 2 (by simp)
      simpa [Nat.sub_sub] using this
  · rintro ⟨hp, e, W, hc, hW, ha, hb, hcc⟩
    refine ⟨hp, e, W, hc, by simpa using hW, ?_⟩
    intro i hi
    have : i = 0 ∨ i = 1 ∨ i = 2 := by simp at hi; omega
    rcases this with rfl | rfl | rfl
    · simpa using ha
    · simpa using hb
    · simpa [Nat.sub_sub] using hcc

/-- Finite superset of the width-`k` projections of every last predecessor
of a palindrome beginning with `pre`: lengths `pre.length .. k`. -/
def initialWordsL (k : Nat) (pre : List Nat) : List (List Nat) :=
  ((List.range (k + 1 - pre.length)).flatMap fun j =>
    (digitLists j).map (pre ++ ·)).filter (initialOK k)

theorem target_project_mem_initialWordsL (k : Nat) (pre : List Nat)
    (hk : pre.length ≤ k) (q : Nat → Nat) (L : Nat) (ha : Admissible L q)
    (hL : pre.length ≤ L) (hsmall : ∀ i, i < L → q i ≤ 9)
    (hprefix : ∀ i, i < pre.length → q i = pre.getD i 0) :
    projectK k q L ∈ initialWordsL k pre := by
  rcases ha with ⟨hpos, houter, hbound, hsymm, hcenter⟩
  let n := pre.length
  let m := min L k
  have hnm : n ≤ m := by omega
  have hmL : m ≤ L := by omega
  have hproj : projectK k q L = (List.range m).map q := by
    simp only [projectK, wordPrefix_eq_range_map]
    rfl
  let tail := (List.range (m - n)).map (fun j => q (j + n))
  have hsplit : (List.range m).map q = pre ++ tail := by
    apply List.ext_getElem
    · simp [tail, n]
      omega
    · intro i h1 h2
      simp only [List.getElem_map, List.getElem_range]
      by_cases hi : i < n
      · have hi' : i < pre.length := hi
        rw [List.getElem_append_left hi']
        rw [hprefix i hi']
        simp [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi']
      · rw [List.getElem_append_right (by omega)]
        simp only [tail, List.getElem_map, List.getElem_range]
        congr 1
        omega
  have htail : tail ∈ digitLists (m - n) := by
    apply mem_digitLists
    · simp [tail]
    · intro x hx
      simp only [tail, List.mem_map, List.mem_range] at hx
      obtain ⟨j, hj, rfl⟩ := hx
      exact hsmall (j + n) (by omega)
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
  unfold initialWordsL
  rw [List.mem_filter]
  refine ⟨?_, hok⟩
  rw [List.mem_flatMap]
  refine ⟨m - n, List.mem_range.mpr (by omega), ?_⟩
  rw [List.mem_map]
  exact ⟨tail, htail, hsplit.symm⟩

/-- Boolean sufficient condition excluding a final overflow into the target. -/
def noOverflowPre (pre : List Nat) : Bool :=
  Nat.ble 2 (pre.getD 0 0) || pre.any (fun d => Nat.ble 3 d)

theorem canonical_last_step_initialL (k : Nat) (pre : List Nat)
    (hm : 1 ≤ pre.length) (hk : pre.length ≤ k) (hno : noOverflowPre pre = true)
    {n P L : Nat} {d : Nat → Nat}
    (hsource : Canonical n d L) (hstep : step n = P) (hP : PalStartsL pre P) :
    projectK k (columnSum d L) L ∈ initialWordsL k pre := by
  obtain ⟨hpal, e, W, htarget, hW, hpre⟩ := hP
  have hc : carry (columnSum d L) L = 0 := by
    unfold noOverflowPre at hno
    simp only [Bool.or_eq_true, Nat.ble_eq, List.any_eq_true] at hno
    rcases hno with h | ⟨x, hx, h3⟩
    · have h0 := hpre 0 hm
      have hlead : 1 < e (W - 1) := by simpa using (show 1 < e (W - 1 - 0) by omega)
      exact no_overflow_of_target_leading_gt_one hsource htarget hstep hlead
    · obtain ⟨i, hi, hix⟩ := List.getElem_of_mem hx
      have hei := hpre i hi
      have hge : 2 < e (W - 1 - i) := by
        rw [hei]
        simp [List.getD_eq_getElem?_getD, hi, hix]
        omega
      exact no_overflow_of_digit_gt_two hsource htarget hstep hpal
        (j := W - 1 - i) (by omega) hge
  obtain ⟨hwidth, _, hpair, hsmall⟩ :=
    canonical_last_step_of_no_overflow hsource htarget hstep hpal hc
  have hp : Palindrome (value e W) := by
    rw [htarget.2.2.2]
    exact hpal
  have hsym := (palindrome_value_iff e W htarget.2.1
    (Or.inr htarget.2.2.1)).mp hp
  apply target_project_mem_initialWordsL k pre hk (columnSum d L) L
    (canonical_admissible n d L hsource) (by omega) hsmall
  intro i hi
  rw [hpair i (by omega), hsym i (by omega)]
  exact hpre i hi

theorem ancestry_bound_of_RL (k : Nat) (pre : List Nat) (bound : Nat)
    (hm : 1 ≤ pre.length) (hk : pre.length ≤ k) (hno : noOverflowPre pre = true)
    (R : List Nat → Option Nat) (rows : RowsClosed k R) (short : ShortClosed k R)
    (initial : ∀ w ∈ initialWordsL k pre, ∃ r, R w = some r ∧ r ≤ bound) :
    ∀ A P t, 0 < A → PalStartsL pre P → orbit A t = P → t ≤ bound + 1 := by
  intro A P t hA hP hreach
  cases t with
  | zero => omega
  | succ t =>
      obtain ⟨d, L, hcan⟩ := canonical_exists A hA
      let q := columnSum d L
      have hadm : Admissible L q := canonical_admissible A d L hcan
      obtain ⟨e, he, hrep⟩ := iterPairs_representation A d q L t hcan (fun _ _ => rfl)
      have hlast : step (orbit A t) = P := hreach
      have hmem := canonical_last_step_initialL k pre hm hk hno he hlast hP
      have hproj := projectK_congr k (columnSum e (iterPairs q L t).1)
        (iterPairs q L t).2 (iterPairs q L t).1 hrep
      rw [hproj] at hmem
      obtain ⟨r, hr, hb⟩ := initial _ hmem
      have ht := actual_iterPairs_rank_R (by omega) rows short q L hadm t hr
      omega

/-! ## Many prefixes from one Boolean check -/

/-- Entry `(pre, bound)`: every initial word has rank at most `bound`. -/
def entryOK (k : Nat) (R : List Nat → Option Nat) (e : List Nat × Nat) : Bool :=
  Nat.ble 1 e.1.length && Nat.ble e.1.length k && noOverflowPre e.1 &&
    (initialWordsL k e.1).all (fun w =>
      match R w with
      | some r => Nat.ble r e.2
      | none => false)

theorem ancestry_of_entries (k : Nat) (R : List Nat → Option Nat)
    (rows : RowsClosed k R) (short : ShortClosed k R)
    (entries : List (List Nat × Nat)) (h : entries.all (entryOK k R) = true) :
    ∀ e ∈ entries, ∀ A P t, 0 < A → PalStartsL e.1 P → orbit A t = P → t ≤ e.2 + 1 := by
  intro e he
  have hc := List.all_eq_true.mp h e he
  unfold entryOK at hc
  simp only [Bool.and_eq_true, Nat.ble_eq] at hc
  obtain ⟨⟨⟨hm, hk⟩, hno⟩, hall⟩ := hc
  apply ancestry_bound_of_RL k e.1 e.2 hm hk hno R rows short
  intro w hw
  have hw' := List.all_eq_true.mp hall w hw
  split at hw'
  · rename_i r hr
    exact ⟨r, hr, by simpa [Nat.ble_eq] using hw'⟩
  · contradiction

theorem no_196_of_entries (k : Nat) (R : List Nat → Option Nat)
    (rows : RowsClosed k R) (short : ShortClosed k R)
    (entries : List (List Nat × Nat)) (h : entries.all (entryOK k R) = true)
    (hb : entries.all (fun e => Nat.ble (e.2 + 1) 100) = true) :
    ∀ t, ∀ e ∈ entries, ¬ PalStartsL e.1 (orbit 196 t) := by
  intro t e he
  have hbe : e.2 + 1 ≤ 100 := by
    simpa [Nat.ble_eq] using List.all_eq_true.mp hb e he
  exact no_196_target_of_ancestry_bound (PalStartsL e.1) (e.2 + 1) hbe
    (fun _ h => h.1) (ancestry_of_entries k R rows short entries h e he) t

end Agent124.PrefixL

#print axioms Agent124.PrefixL.palStartsL_three_iff
#print axioms Agent124.PrefixL.target_project_mem_initialWordsL
#print axioms Agent124.PrefixL.canonical_last_step_initialL
#print axioms Agent124.PrefixL.ancestry_bound_of_RL
#print axioms Agent124.PrefixL.ancestry_of_entries
#print axioms Agent124.PrefixL.no_196_of_entries
