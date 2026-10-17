import P196.Agent104P620Witness.Agent124PrefixK

/-!
# Prefix-ancestry endpoint for an abstract rank function (Agent #124)

`Agent124.PrefixK` states its endpoint for Agent #104's `RankTree` lookup.
This module repeats the same argument for an arbitrary partial rank function
`R : List Nat → Option Nat`, with the row and short premises stated
semantically.  Concrete certificates may then use any data structure whose
lookups are proved to satisfy these premises (for example the code-keyed
trees of `Agent124CodeCert`, which kernel-reduce much faster).

Row closure is only required for words whose entries are below 19; every
projection of an actual admissible pair word has this property.
-/

namespace Agent124.PrefixR

open DecimalDigits FoldedDecimal Lychrel196 OverflowCarryNormalization
open NormalizationBridge CarryHistory SevenColumnProjection
open SevenColumn.Certificate SevenColumn.ShortBoundary
open SevenColumnKernel.PalindromeBridge Agent124.PrefixK

/-- Row closure of `R` against the complete long inverse at width `k`. -/
def RowsClosed (k : Nat) (R : List Nat → Option Nat) : Prop :=
  ∀ w r, (∀ x ∈ w, x < 19) → R w = some r →
    ∀ q ∈ longPred k w, ∃ s, R q = some s ∧ s < r

/-- Short-transition rank descent for `R`. -/
def ShortClosed (k : Nat) (R : List Nat → Option Nat) : Prop :=
  ∀ s ∈ shortWordsK k, ∀ r, R (nextWord s) = some r → ∃ m, R s = some m ∧ m < r

theorem wordPrefix_lt19 (q : Nat → Nat) (L k : Nat) (ha : Admissible L q) (hk : k ≤ L) :
    ∀ x ∈ wordPrefix q k, x < 19 := by
  intro x hx
  rw [wordPrefix_eq_range_map, List.mem_map] at hx
  obtain ⟨i, hi, rfl⟩ := hx
  have := ha.2.2.1 i (by have := List.mem_range.mp hi; omega)
  omega

/-- Exact semantic rank theorem for an abstract rank function. -/
theorem actual_iterPairs_rank_R {k : Nat} (hk : 0 < k) {R : List Nat → Option Nat}
    (rows : RowsClosed k R) (short : ShortClosed k R)
    (q : Nat → Nat) (L : Nat) (ha : Admissible L q) (t : Nat) {r : Nat}
    (hend : R (projectK k (iterPairs q L t).2 (iterPairs q L t).1) = some r) :
    t ≤ r := by
  induction t generalizing r with
  | zero => omega
  | succ t ih =>
      let v := iterPairs q L t
      have hv : Admissible v.1 v.2 := iterPairs_admissible q L t ha
      have hv' : Admissible (nextWidth v.2 v.1) (nextColumns v.2 v.1) :=
        iterPairs_admissible q L (t + 1) ha
      change R (projectK k (nextColumns v.2 v.1) (nextWidth v.2 v.1)) = some r at hend
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
        obtain ⟨m, hm, hlt⟩ := short _ hmem r hend
        have hprev : R (projectK k v.2 v.1) = some m := by
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
        obtain ⟨s, hs, hsr⟩ := rows _ r
          (wordPrefix_lt19 _ _ k hv' hnext) hend _ hm
        have hprev : R (projectK k v.2 v.1) = some s := by
          rw [projectK_long _ _ _ hlong]
          exact hs
        have ht := ih hprev
        omega

/-- Initial premise for an abstract rank function. -/
def InitialBounded (k a b c bound : Nat) (R : List Nat → Option Nat) : Prop :=
  ∀ w ∈ initialWordsK k a b c, ∃ r, R w = some r ∧ r ≤ bound

theorem ancestry_bound_of_R (k a b c bound : Nat) (hk : 3 ≤ k) (ha2 : 2 ≤ a)
    (R : List Nat → Option Nat) (rows : RowsClosed k R) (short : ShortClosed k R)
    (initial : InitialBounded k a b c bound R) :
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
      obtain ⟨r, hr, hb⟩ := initial _ hm
      have ht := actual_iterPairs_rank_R (by omega) rows short q L hadm t hr
      omega

theorem no_196_of_R (k a b c bound : Nat) (hk : 3 ≤ k) (ha2 : 2 ≤ a)
    (hb : bound + 1 ≤ 100)
    (R : List Nat → Option Nat) (rows : RowsClosed k R) (short : ShortClosed k R)
    (initial : InitialBounded k a b c bound R) :
    ∀ t, ¬ PalStarts3 a b c (orbit 196 t) :=
  no_196_target_of_ancestry_bound (PalStarts3 a b c) (bound + 1) hb
    (fun _ h => h.1) (ancestry_bound_of_R k a b c bound hk ha2 R rows short initial)

end Agent124.PrefixR

#print axioms Agent124.PrefixR.actual_iterPairs_rank_R
#print axioms Agent124.PrefixR.ancestry_bound_of_R
#print axioms Agent124.PrefixR.no_196_of_R
