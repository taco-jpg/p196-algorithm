import P196.Agent117P2641.Agent124PrefixL
import P196.Agent117RemainingCycles.Projection
import P196.Agent117RemainingCycles.Cycle112_k8
import P196.Agent117RemainingCycles.Cycle138_k7
import P196.Agent117RemainingCycles.Cycle164_k7
import P196.Agent117RemainingCycles.Cycle198_k7
import P196.Agent117RemainingCycles.Cycle248_k7
import P196.Agent117RemainingCycles.Cycle275_k8
import P196.Agent117RemainingCycles.Cycle398_k7
import P196.Agent117RemainingCycles.Cycle626_k7
import P196.Agent117RemainingCycles.Cycle710_k7
import P196.Agent117RemainingCycles.Cycle716_k7
import P196.Agent117RemainingCycles.Cycle790_k7
import P196.Agent117RemainingCycles.Cycle911_k7
import P196.Agent117RemainingCycles.Cycle936_k7
import P196.Agent117RemainingCycles.Cycle952_k7

/-!
# Agent 19 review: the 14 cycle witnesses also defeat the certificate formats in use

`Agent117RemainingCycles` proves, for each of 14 three-digit prefixes, that no rank tree
whose rows are checked against the full inverse `SevenColumn.prefixPredecessors`
(`CheckedRows tree prefixPredecessors`) contains one initial word `p0`.

The prefix certificates that are actually used check rows only for words of the
certificate width: Agent #118 uses `CheckedRows tree (longPred 7)` and Agent #124 uses the
rank interface `RowsClosed k R` (`Agent124.PrefixR`).  Neither hypothesis is literally the
one in Agent #117's theorem.  This file closes that gap for the same width `k`:

* `none_of_walks`: a verified entry walk plus a verified closed walk from a bounded word
  of length `k` force `R p = none` for every `R` with `RowsClosed k R`;
* `rowsClosed_of_checked`: every `CheckedRows tree (longPred k)` tree gives such an `R`;
* per prefix: `no_rank_*` (any `RowsClosed` rank function misses `p0`),
  `no_tree_*` (Agent #118 / #104 tree format), `no_entry_*` (Agent #124 entry format:
  `entryOK k R (prefix, b) = false` for every bound `b`).

Scope: only the width `k` of each witness (7, or 8 for 112 and 275).  Nothing here says
the method fails at a larger width, and nothing is claimed about 196 or about palindromes.
-/

namespace Sprint.Agent19.CycleFormats

open SevenColumn SevenColumn.Certificate SevenColumnProjection Agent117
open Agent124.PrefixK Agent124.PrefixR Agent124.PrefixL

theorem forwardPrefix_length (s : List Nat) (e : Nat) :
    (forwardPrefix s e).length = s.length := by
  unfold forwardPrefix
  dsimp only
  split <;> simp [List.length_zipWith]

/-- A verified backward edge is a `prefixPredecessors` edge between words of equal
length whose new word has entries below 19. -/
theorem edgeOK_props {p s : List Nat} {e : Nat} (h : edgeOK p s e = true) :
    s ∈ prefixPredecessors p ∧ (∀ x ∈ s, x < 19) ∧ p.length = s.length := by
  refine ⟨edgeOK_sound h, ?_, ?_⟩
  · unfold edgeOK at h
    simp only [Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, beq_iff_eq] at h
    exact h.1.1.2
  · unfold edgeOK at h
    simp only [Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, beq_iff_eq] at h
    rw [← h.2, forwardPrefix_length]

/-- Strict rank descent along a verified backward walk, for any rank function that is
closed under the width-`k` inverse. -/
theorem walk_rank {k : Nat} {R : List Nat → Option Nat} (rows : RowsClosed k R) :
    ∀ (w : List (List Nat × Nat)) (p : List Nat) (e r : Nat),
      walkOK ((p, e) :: w) = true → (∀ x ∈ p, x < 19) → p.length = k → R p = some r →
      ∃ r', R (w.getLastD (p, e)).1 = some r' ∧ r' + w.length ≤ r ∧
        (∀ x ∈ (w.getLastD (p, e)).1, x < 19) ∧ (w.getLastD (p, e)).1.length = k
  | [], p, e, r, _, hb, hl, hr => ⟨r, by simpa using hr, by simp, by simpa using hb, by simpa using hl⟩
  | (s, es) :: rest, p, e, r, h, hb, hl, hr => by
      simp only [walkOK, Bool.and_eq_true] at h
      obtain ⟨hs, hsb, hlen⟩ := edgeOK_props h.1
      have hq : s ∈ longPred k p := by
        simp only [longPred, hl, if_true]
        exact hs
      obtain ⟨r1, hr1, hlt⟩ := rows p r hb hr s hq
      obtain ⟨r', hr', hle, hb', hl'⟩ := walk_rank rows rest s es r1 h.2 hsb (by omega) hr1
      refine ⟨r', ?_, ?_, ?_, ?_⟩
      · simpa only [List.getLastD_cons] using hr'
      · simp only [List.length_cons]; omega
      · simpa only [List.getLastD_cons] using hb'
      · simpa only [List.getLastD_cons] using hl'

/-- An entry walk to a word on a closed walk of positive length: no rank function closed
under the width-`k` inverse ranks the start word. -/
theorem none_of_walks {k : Nat} {R : List Nat → Option Nat} (rows : RowsClosed k R)
    (entry cycle : List (List Nat × Nat)) (p z : List Nat) (ep ez : Nat)
    (hp : ∀ x ∈ p, x < 19) (hpl : p.length = k)
    (hentry : walkOK ((p, ep) :: entry) = true)
    (hz : (entry.getLastD (p, ep)).1 = z)
    (hcycle : walkOK ((z, ez) :: cycle) = true)
    (hclose : (cycle.getLastD (z, ez)).1 = z)
    (hpos : 0 < cycle.length) : R p = none := by
  cases hR : R p with
  | none => rfl
  | some r =>
      obtain ⟨rz, hrz, _, hzb, hzl⟩ := walk_rank rows entry p ep r hentry hp hpl hR
      rw [hz] at hrz hzb hzl
      obtain ⟨r', hr', hle, _, _⟩ := walk_rank rows cycle z ez rz hcycle hzb hzl hrz
      rw [hclose, hrz] at hr'
      cases hr'
      omega

/-- Agent #104 / #118 tree format: a tree checked against `longPred k` is closed. -/
theorem rowsClosed_of_checked {k : Nat} {tree : RankTree}
    (h : CheckedRows tree (longPred k)) : RowsClosed k (lookup tree) :=
  fun _ _ _ hr _ hq => checkedRows_closed h hr hq

/-- A full-width digit completion of a prefix is one of its initial words. -/
theorem mem_initialWordsL_full (k : Nat) (pre tail : List Nat)
    (hlen : pre.length + tail.length = k) (ht : ∀ x ∈ tail, x ≤ 9) :
    pre ++ tail ∈ initialWordsL k pre := by
  unfold initialWordsL
  rw [List.mem_filter]
  constructor
  · rw [List.mem_flatMap]
    refine ⟨tail.length, List.mem_range.mpr (by omega), ?_⟩
    rw [List.mem_map]
    exact ⟨tail, mem_digitLists tail.length tail rfl ht, rfl⟩
  · unfold initialOK
    simp [hlen]

/-- Agent #124 entry format: an unranked initial word makes the entry check fail,
whatever the claimed bound. -/
theorem entryOK_false_of_none {k : Nat} {R : List Nat → Option Nat} {pre w : List Nat}
    (b : Nat) (hw : w ∈ initialWordsL k pre) (hR : R w = none) :
    entryOK k R (pre, b) = false := by
  apply Bool.eq_false_iff.mpr
  intro h
  unfold entryOK at h
  simp only [Bool.and_eq_true] at h
  have := List.all_eq_true.mp h.2 w hw
  simp [hR] at this

/-! ### Prefix 112, width 8 -/

theorem p0_112 : Agent117.Cycle112_k8.p0 = [1,1,2] ++ [9,9,5,4,1] := rfl

theorem no_rank_112 {R : List Nat → Option Nat} (rows : RowsClosed 8 R) :
    R Agent117.Cycle112_k8.p0 = none :=
  none_of_walks rows Agent117.Cycle112_k8.entry Agent117.Cycle112_k8.cycle Agent117.Cycle112_k8.p0 Agent117.Cycle112_k8.z _ _
    (by decide) (by decide) Agent117.Cycle112_k8.entry_ok Agent117.Cycle112_k8.entry_end Agent117.Cycle112_k8.cycle_ok Agent117.Cycle112_k8.cycle_end
    Agent117.Cycle112_k8.cycle_pos

theorem no_tree_112 (tree : RankTree) (h : CheckedRows tree (longPred 8)) :
    lookup tree Agent117.Cycle112_k8.p0 = none :=
  no_rank_112 (rowsClosed_of_checked h)

theorem no_entry_112 {R : List Nat → Option Nat} (rows : RowsClosed 8 R) (b : Nat) :
    entryOK 8 R ([1,1,2], b) = false :=
  entryOK_false_of_none b
    (by rw [p0_112]; exact mem_initialWordsL_full 8 [1,1,2] [9,9,5,4,1] (by decide) (by decide))
    (no_rank_112 rows)

/-! ### Prefix 138, width 7 -/

theorem p0_138 : Agent117.Cycle138_k7.p0 = [1,3,8] ++ [6,6,6,0] := rfl

theorem no_rank_138 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    R Agent117.Cycle138_k7.p0 = none :=
  none_of_walks rows Agent117.Cycle138_k7.entry Agent117.Cycle138_k7.cycle Agent117.Cycle138_k7.p0 Agent117.Cycle138_k7.z _ _
    (by decide) (by decide) Agent117.Cycle138_k7.entry_ok Agent117.Cycle138_k7.entry_end Agent117.Cycle138_k7.cycle_ok Agent117.Cycle138_k7.cycle_end
    Agent117.Cycle138_k7.cycle_pos

theorem no_tree_138 (tree : RankTree) (h : CheckedRows tree (longPred 7)) :
    lookup tree Agent117.Cycle138_k7.p0 = none :=
  no_rank_138 (rowsClosed_of_checked h)

theorem no_entry_138 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (b : Nat) :
    entryOK 7 R ([1,3,8], b) = false :=
  entryOK_false_of_none b
    (by rw [p0_138]; exact mem_initialWordsL_full 7 [1,3,8] [6,6,6,0] (by decide) (by decide))
    (no_rank_138 rows)

/-! ### Prefix 164, width 7 -/

theorem p0_164 : Agent117.Cycle164_k7.p0 = [1,6,4] ++ [9,9,9,9] := rfl

theorem no_rank_164 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    R Agent117.Cycle164_k7.p0 = none :=
  none_of_walks rows Agent117.Cycle164_k7.entry Agent117.Cycle164_k7.cycle Agent117.Cycle164_k7.p0 Agent117.Cycle164_k7.z _ _
    (by decide) (by decide) Agent117.Cycle164_k7.entry_ok Agent117.Cycle164_k7.entry_end Agent117.Cycle164_k7.cycle_ok Agent117.Cycle164_k7.cycle_end
    Agent117.Cycle164_k7.cycle_pos

theorem no_tree_164 (tree : RankTree) (h : CheckedRows tree (longPred 7)) :
    lookup tree Agent117.Cycle164_k7.p0 = none :=
  no_rank_164 (rowsClosed_of_checked h)

theorem no_entry_164 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (b : Nat) :
    entryOK 7 R ([1,6,4], b) = false :=
  entryOK_false_of_none b
    (by rw [p0_164]; exact mem_initialWordsL_full 7 [1,6,4] [9,9,9,9] (by decide) (by decide))
    (no_rank_164 rows)

/-! ### Prefix 198, width 7 -/

theorem p0_198 : Agent117.Cycle198_k7.p0 = [1,9,8] ++ [6,9,4,2] := rfl

theorem no_rank_198 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    R Agent117.Cycle198_k7.p0 = none :=
  none_of_walks rows Agent117.Cycle198_k7.entry Agent117.Cycle198_k7.cycle Agent117.Cycle198_k7.p0 Agent117.Cycle198_k7.z _ _
    (by decide) (by decide) Agent117.Cycle198_k7.entry_ok Agent117.Cycle198_k7.entry_end Agent117.Cycle198_k7.cycle_ok Agent117.Cycle198_k7.cycle_end
    Agent117.Cycle198_k7.cycle_pos

theorem no_tree_198 (tree : RankTree) (h : CheckedRows tree (longPred 7)) :
    lookup tree Agent117.Cycle198_k7.p0 = none :=
  no_rank_198 (rowsClosed_of_checked h)

theorem no_entry_198 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (b : Nat) :
    entryOK 7 R ([1,9,8], b) = false :=
  entryOK_false_of_none b
    (by rw [p0_198]; exact mem_initialWordsL_full 7 [1,9,8] [6,9,4,2] (by decide) (by decide))
    (no_rank_198 rows)

/-! ### Prefix 248, width 7 -/

theorem p0_248 : Agent117.Cycle248_k7.p0 = [2,4,8] ++ [9,2,7,8] := rfl

theorem no_rank_248 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    R Agent117.Cycle248_k7.p0 = none :=
  none_of_walks rows Agent117.Cycle248_k7.entry Agent117.Cycle248_k7.cycle Agent117.Cycle248_k7.p0 Agent117.Cycle248_k7.z _ _
    (by decide) (by decide) Agent117.Cycle248_k7.entry_ok Agent117.Cycle248_k7.entry_end Agent117.Cycle248_k7.cycle_ok Agent117.Cycle248_k7.cycle_end
    Agent117.Cycle248_k7.cycle_pos

theorem no_tree_248 (tree : RankTree) (h : CheckedRows tree (longPred 7)) :
    lookup tree Agent117.Cycle248_k7.p0 = none :=
  no_rank_248 (rowsClosed_of_checked h)

theorem no_entry_248 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (b : Nat) :
    entryOK 7 R ([2,4,8], b) = false :=
  entryOK_false_of_none b
    (by rw [p0_248]; exact mem_initialWordsL_full 7 [2,4,8] [9,2,7,8] (by decide) (by decide))
    (no_rank_248 rows)

/-! ### Prefix 275, width 8 -/

theorem p0_275 : Agent117.Cycle275_k8.p0 = [2,7,5] ++ [0,0,0,0,0] := rfl

theorem no_rank_275 {R : List Nat → Option Nat} (rows : RowsClosed 8 R) :
    R Agent117.Cycle275_k8.p0 = none :=
  none_of_walks rows Agent117.Cycle275_k8.entry Agent117.Cycle275_k8.cycle Agent117.Cycle275_k8.p0 Agent117.Cycle275_k8.z _ _
    (by decide) (by decide) Agent117.Cycle275_k8.entry_ok Agent117.Cycle275_k8.entry_end Agent117.Cycle275_k8.cycle_ok Agent117.Cycle275_k8.cycle_end
    Agent117.Cycle275_k8.cycle_pos

theorem no_tree_275 (tree : RankTree) (h : CheckedRows tree (longPred 8)) :
    lookup tree Agent117.Cycle275_k8.p0 = none :=
  no_rank_275 (rowsClosed_of_checked h)

theorem no_entry_275 {R : List Nat → Option Nat} (rows : RowsClosed 8 R) (b : Nat) :
    entryOK 8 R ([2,7,5], b) = false :=
  entryOK_false_of_none b
    (by rw [p0_275]; exact mem_initialWordsL_full 8 [2,7,5] [0,0,0,0,0] (by decide) (by decide))
    (no_rank_275 rows)

/-! ### Prefix 398, width 7 -/

theorem p0_398 : Agent117.Cycle398_k7.p0 = [3,9,8] ++ [9,6,7,7] := rfl

theorem no_rank_398 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    R Agent117.Cycle398_k7.p0 = none :=
  none_of_walks rows Agent117.Cycle398_k7.entry Agent117.Cycle398_k7.cycle Agent117.Cycle398_k7.p0 Agent117.Cycle398_k7.z _ _
    (by decide) (by decide) Agent117.Cycle398_k7.entry_ok Agent117.Cycle398_k7.entry_end Agent117.Cycle398_k7.cycle_ok Agent117.Cycle398_k7.cycle_end
    Agent117.Cycle398_k7.cycle_pos

theorem no_tree_398 (tree : RankTree) (h : CheckedRows tree (longPred 7)) :
    lookup tree Agent117.Cycle398_k7.p0 = none :=
  no_rank_398 (rowsClosed_of_checked h)

theorem no_entry_398 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (b : Nat) :
    entryOK 7 R ([3,9,8], b) = false :=
  entryOK_false_of_none b
    (by rw [p0_398]; exact mem_initialWordsL_full 7 [3,9,8] [9,6,7,7] (by decide) (by decide))
    (no_rank_398 rows)

/-! ### Prefix 626, width 7 -/

theorem p0_626 : Agent117.Cycle626_k7.p0 = [6,2,6] ++ [9,7,6,6] := rfl

theorem no_rank_626 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    R Agent117.Cycle626_k7.p0 = none :=
  none_of_walks rows Agent117.Cycle626_k7.entry Agent117.Cycle626_k7.cycle Agent117.Cycle626_k7.p0 Agent117.Cycle626_k7.z _ _
    (by decide) (by decide) Agent117.Cycle626_k7.entry_ok Agent117.Cycle626_k7.entry_end Agent117.Cycle626_k7.cycle_ok Agent117.Cycle626_k7.cycle_end
    Agent117.Cycle626_k7.cycle_pos

theorem no_tree_626 (tree : RankTree) (h : CheckedRows tree (longPred 7)) :
    lookup tree Agent117.Cycle626_k7.p0 = none :=
  no_rank_626 (rowsClosed_of_checked h)

theorem no_entry_626 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (b : Nat) :
    entryOK 7 R ([6,2,6], b) = false :=
  entryOK_false_of_none b
    (by rw [p0_626]; exact mem_initialWordsL_full 7 [6,2,6] [9,7,6,6] (by decide) (by decide))
    (no_rank_626 rows)

/-! ### Prefix 710, width 7 -/

theorem p0_710 : Agent117.Cycle710_k7.p0 = [7,1,0] ++ [2,5,9,5] := rfl

theorem no_rank_710 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    R Agent117.Cycle710_k7.p0 = none :=
  none_of_walks rows Agent117.Cycle710_k7.entry Agent117.Cycle710_k7.cycle Agent117.Cycle710_k7.p0 Agent117.Cycle710_k7.z _ _
    (by decide) (by decide) Agent117.Cycle710_k7.entry_ok Agent117.Cycle710_k7.entry_end Agent117.Cycle710_k7.cycle_ok Agent117.Cycle710_k7.cycle_end
    Agent117.Cycle710_k7.cycle_pos

theorem no_tree_710 (tree : RankTree) (h : CheckedRows tree (longPred 7)) :
    lookup tree Agent117.Cycle710_k7.p0 = none :=
  no_rank_710 (rowsClosed_of_checked h)

theorem no_entry_710 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (b : Nat) :
    entryOK 7 R ([7,1,0], b) = false :=
  entryOK_false_of_none b
    (by rw [p0_710]; exact mem_initialWordsL_full 7 [7,1,0] [2,5,9,5] (by decide) (by decide))
    (no_rank_710 rows)

/-! ### Prefix 716, width 7 -/

theorem p0_716 : Agent117.Cycle716_k7.p0 = [7,1,6] ++ [4,4,6,3] := rfl

theorem no_rank_716 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    R Agent117.Cycle716_k7.p0 = none :=
  none_of_walks rows Agent117.Cycle716_k7.entry Agent117.Cycle716_k7.cycle Agent117.Cycle716_k7.p0 Agent117.Cycle716_k7.z _ _
    (by decide) (by decide) Agent117.Cycle716_k7.entry_ok Agent117.Cycle716_k7.entry_end Agent117.Cycle716_k7.cycle_ok Agent117.Cycle716_k7.cycle_end
    Agent117.Cycle716_k7.cycle_pos

theorem no_tree_716 (tree : RankTree) (h : CheckedRows tree (longPred 7)) :
    lookup tree Agent117.Cycle716_k7.p0 = none :=
  no_rank_716 (rowsClosed_of_checked h)

theorem no_entry_716 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (b : Nat) :
    entryOK 7 R ([7,1,6], b) = false :=
  entryOK_false_of_none b
    (by rw [p0_716]; exact mem_initialWordsL_full 7 [7,1,6] [4,4,6,3] (by decide) (by decide))
    (no_rank_716 rows)

/-! ### Prefix 790, width 7 -/

theorem p0_790 : Agent117.Cycle790_k7.p0 = [7,9,0] ++ [9,0,2,6] := rfl

theorem no_rank_790 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    R Agent117.Cycle790_k7.p0 = none :=
  none_of_walks rows Agent117.Cycle790_k7.entry Agent117.Cycle790_k7.cycle Agent117.Cycle790_k7.p0 Agent117.Cycle790_k7.z _ _
    (by decide) (by decide) Agent117.Cycle790_k7.entry_ok Agent117.Cycle790_k7.entry_end Agent117.Cycle790_k7.cycle_ok Agent117.Cycle790_k7.cycle_end
    Agent117.Cycle790_k7.cycle_pos

theorem no_tree_790 (tree : RankTree) (h : CheckedRows tree (longPred 7)) :
    lookup tree Agent117.Cycle790_k7.p0 = none :=
  no_rank_790 (rowsClosed_of_checked h)

theorem no_entry_790 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (b : Nat) :
    entryOK 7 R ([7,9,0], b) = false :=
  entryOK_false_of_none b
    (by rw [p0_790]; exact mem_initialWordsL_full 7 [7,9,0] [9,0,2,6] (by decide) (by decide))
    (no_rank_790 rows)

/-! ### Prefix 911, width 7 -/

theorem p0_911 : Agent117.Cycle911_k7.p0 = [9,1,1] ++ [9,6,6,0] := rfl

theorem no_rank_911 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    R Agent117.Cycle911_k7.p0 = none :=
  none_of_walks rows Agent117.Cycle911_k7.entry Agent117.Cycle911_k7.cycle Agent117.Cycle911_k7.p0 Agent117.Cycle911_k7.z _ _
    (by decide) (by decide) Agent117.Cycle911_k7.entry_ok Agent117.Cycle911_k7.entry_end Agent117.Cycle911_k7.cycle_ok Agent117.Cycle911_k7.cycle_end
    Agent117.Cycle911_k7.cycle_pos

theorem no_tree_911 (tree : RankTree) (h : CheckedRows tree (longPred 7)) :
    lookup tree Agent117.Cycle911_k7.p0 = none :=
  no_rank_911 (rowsClosed_of_checked h)

theorem no_entry_911 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (b : Nat) :
    entryOK 7 R ([9,1,1], b) = false :=
  entryOK_false_of_none b
    (by rw [p0_911]; exact mem_initialWordsL_full 7 [9,1,1] [9,6,6,0] (by decide) (by decide))
    (no_rank_911 rows)

/-! ### Prefix 936, width 7 -/

theorem p0_936 : Agent117.Cycle936_k7.p0 = [9,3,6] ++ [8,3,7,6] := rfl

theorem no_rank_936 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    R Agent117.Cycle936_k7.p0 = none :=
  none_of_walks rows Agent117.Cycle936_k7.entry Agent117.Cycle936_k7.cycle Agent117.Cycle936_k7.p0 Agent117.Cycle936_k7.z _ _
    (by decide) (by decide) Agent117.Cycle936_k7.entry_ok Agent117.Cycle936_k7.entry_end Agent117.Cycle936_k7.cycle_ok Agent117.Cycle936_k7.cycle_end
    Agent117.Cycle936_k7.cycle_pos

theorem no_tree_936 (tree : RankTree) (h : CheckedRows tree (longPred 7)) :
    lookup tree Agent117.Cycle936_k7.p0 = none :=
  no_rank_936 (rowsClosed_of_checked h)

theorem no_entry_936 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (b : Nat) :
    entryOK 7 R ([9,3,6], b) = false :=
  entryOK_false_of_none b
    (by rw [p0_936]; exact mem_initialWordsL_full 7 [9,3,6] [8,3,7,6] (by decide) (by decide))
    (no_rank_936 rows)

/-! ### Prefix 952, width 7 -/

theorem p0_952 : Agent117.Cycle952_k7.p0 = [9,5,2] ++ [2,8,8,0] := rfl

theorem no_rank_952 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) :
    R Agent117.Cycle952_k7.p0 = none :=
  none_of_walks rows Agent117.Cycle952_k7.entry Agent117.Cycle952_k7.cycle Agent117.Cycle952_k7.p0 Agent117.Cycle952_k7.z _ _
    (by decide) (by decide) Agent117.Cycle952_k7.entry_ok Agent117.Cycle952_k7.entry_end Agent117.Cycle952_k7.cycle_ok Agent117.Cycle952_k7.cycle_end
    Agent117.Cycle952_k7.cycle_pos

theorem no_tree_952 (tree : RankTree) (h : CheckedRows tree (longPred 7)) :
    lookup tree Agent117.Cycle952_k7.p0 = none :=
  no_rank_952 (rowsClosed_of_checked h)

theorem no_entry_952 {R : List Nat → Option Nat} (rows : RowsClosed 7 R) (b : Nat) :
    entryOK 7 R ([9,5,2], b) = false :=
  entryOK_false_of_none b
    (by rw [p0_952]; exact mem_initialWordsL_full 7 [9,5,2] [2,8,8,0] (by decide) (by decide))
    (no_rank_952 rows)

end Sprint.Agent19.CycleFormats

#print axioms Sprint.Agent19.CycleFormats.no_rank_112
#print axioms Sprint.Agent19.CycleFormats.no_tree_112
#print axioms Sprint.Agent19.CycleFormats.no_entry_112
#print axioms Sprint.Agent19.CycleFormats.no_rank_138
#print axioms Sprint.Agent19.CycleFormats.no_tree_138
#print axioms Sprint.Agent19.CycleFormats.no_entry_138
#print axioms Sprint.Agent19.CycleFormats.no_rank_164
#print axioms Sprint.Agent19.CycleFormats.no_tree_164
#print axioms Sprint.Agent19.CycleFormats.no_entry_164
#print axioms Sprint.Agent19.CycleFormats.no_rank_198
#print axioms Sprint.Agent19.CycleFormats.no_tree_198
#print axioms Sprint.Agent19.CycleFormats.no_entry_198
#print axioms Sprint.Agent19.CycleFormats.no_rank_248
#print axioms Sprint.Agent19.CycleFormats.no_tree_248
#print axioms Sprint.Agent19.CycleFormats.no_entry_248
#print axioms Sprint.Agent19.CycleFormats.no_rank_275
#print axioms Sprint.Agent19.CycleFormats.no_tree_275
#print axioms Sprint.Agent19.CycleFormats.no_entry_275
#print axioms Sprint.Agent19.CycleFormats.no_rank_398
#print axioms Sprint.Agent19.CycleFormats.no_tree_398
#print axioms Sprint.Agent19.CycleFormats.no_entry_398
#print axioms Sprint.Agent19.CycleFormats.no_rank_626
#print axioms Sprint.Agent19.CycleFormats.no_tree_626
#print axioms Sprint.Agent19.CycleFormats.no_entry_626
#print axioms Sprint.Agent19.CycleFormats.no_rank_710
#print axioms Sprint.Agent19.CycleFormats.no_tree_710
#print axioms Sprint.Agent19.CycleFormats.no_entry_710
#print axioms Sprint.Agent19.CycleFormats.no_rank_716
#print axioms Sprint.Agent19.CycleFormats.no_tree_716
#print axioms Sprint.Agent19.CycleFormats.no_entry_716
#print axioms Sprint.Agent19.CycleFormats.no_rank_790
#print axioms Sprint.Agent19.CycleFormats.no_tree_790
#print axioms Sprint.Agent19.CycleFormats.no_entry_790
#print axioms Sprint.Agent19.CycleFormats.no_rank_911
#print axioms Sprint.Agent19.CycleFormats.no_tree_911
#print axioms Sprint.Agent19.CycleFormats.no_entry_911
#print axioms Sprint.Agent19.CycleFormats.no_rank_936
#print axioms Sprint.Agent19.CycleFormats.no_tree_936
#print axioms Sprint.Agent19.CycleFormats.no_entry_936
#print axioms Sprint.Agent19.CycleFormats.no_rank_952
#print axioms Sprint.Agent19.CycleFormats.no_tree_952
#print axioms Sprint.Agent19.CycleFormats.no_entry_952
