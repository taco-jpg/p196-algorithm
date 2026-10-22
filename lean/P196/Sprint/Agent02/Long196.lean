import P196.Agent124ForwardInvariant.Agent124Forward

/-!
# A 196-specific prefix endpoint that needs only long rows (sprint agent 02)

`Agent124.PrefixL.no_196_of_entries` needs a rank function that is closed under the complete long
inverse (`RowsClosed k R`) **and** under the short-source transitions (`ShortClosed k R`), because
its ancestry bound is proved for every positive seed. For the orbit of 196 the short part is not
needed: from time 50 on the orbit has 24 or more digits, so every projection at width `k ≤ 24` is
long. Here:

* `rank_long`: along an actual trajectory that starts with width at least `k`, a `RowsClosed k`
  rank of the projection after `t` steps is at least `t` (no `ShortClosed` premise);
* `no_196_of_entry_long`: if `entryOK k R (pre, b) = true` and `b ≤ 49`, then no iterate of 196
  is a palindrome beginning with `pre` — times up to 100 by `no_palindrome_through_100`, later times
  because a later palindrome would force a rank of at least 50 at a word whose rank is at most `b`.

This removes the width-`(k-1)` short-word check, which is what blocks width-8 certificates on
small machines (one of nineteen chunks of the width-7 short check exceeded 6 GB in a measurement).
-/

namespace Sprint.Agent02

open DecimalDigits FoldedDecimal Lychrel196 OverflowCarryNormalization
open NormalizationBridge CarryHistory SevenColumnProjection
open SevenColumn.Certificate Agent124.PrefixK Agent124.PrefixR Agent124.LeadOne Agent124.PrefixL
open Agent124.Forward

/-- Rank lower bound along a trajectory that is long at width `k` from the start. -/
theorem rank_long {k : Nat} (hk : 0 < k) {R : List Nat → Option Nat} (rows : RowsClosed k R)
    (q : Nat → Nat) (L : Nat) (ha : Admissible L q) (hkL : k ≤ L) :
    ∀ t r, R (wordPrefix (iterPairs q L t).2 k) = some r → t ≤ r := by
  intro t
  induction t with
  | zero => intro r _; omega
  | succ t ih =>
      intro r hend
      let v := iterPairs q L t
      have hv : Admissible v.1 v.2 := iterPairs_admissible q L t ha
      have hlong : k ≤ v.1 := Nat.le_trans hkL (iterPairs_width_ge q L t)
      have hnext : k ≤ nextWidth v.2 v.1 :=
        Nat.le_trans hlong (width_le_nextWidth v.2 v.1)
      have hv' : Admissible (nextWidth v.2 v.1) (nextColumns v.2 v.1) :=
        iterPairs_admissible q L (t + 1) ha
      change R (wordPrefix (nextColumns v.2 v.1) k) = some r at hend
      have hm : wordPrefix v.2 k ∈ longPred k (wordPrefix (nextColumns v.2 v.1) k) := by
        simp only [longPred, prefix_length, if_true]
        exact actual_mem_prefixPredecessors v.2 v.1 k hv hk hlong
      obtain ⟨s, hs, hsr⟩ := rows _ r (wordPrefix_lt19 _ _ k hv' hnext) hend _ hm
      have := ih s hs
      omega

/-- `Lychrel196.orbit 196 50`, a 24-digit number. -/
def N50 : Nat := 925153265399993573340628

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem orbit196_50 : orbit 196 50 = N50 := by decide

def d50 (i : Nat) : Nat := (N50 / 10 ^ i) % 10

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem value50 : value d50 24 = N50 := by decide

theorem canonical50 : Canonical N50 d50 24 := by
  refine ⟨by decide, fun i _ => ?_, by decide, value50⟩
  unfold d50
  omega

/-- The pair word of the 196 orbit at time 50. -/
def q50 : Nat → Nat := columnSum d50 24

/-- All-time exclusion from one entry check at width `k ≤ 24` with bound at most 49, without any
short-source premise. -/
theorem no_196_of_entry_long {k : Nat} (hk1 : 1 ≤ k) (hk : k ≤ 24)
    {R : List Nat → Option Nat} (rows : RowsClosed k R)
    (e : List Nat × Nat) (he : entryOK k R e = true) (hb : e.2 ≤ 49) :
    ∀ T, ¬ PalStartsL e.1 (orbit 196 T) := by
  intro T hP
  unfold entryOK at he
  simp only [Bool.and_eq_true, Nat.ble_eq] at he
  obtain ⟨⟨⟨hm, hlen⟩, hno⟩, hall⟩ := he
  by_cases hT : T ≤ 100
  · exact no_palindrome_through_100 T hT hP.1
  · obtain ⟨s, rfl⟩ : ∃ s, T = 50 + (s + 1) := ⟨T - 51, by omega⟩
    have horb : orbit 196 (50 + (s + 1)) = step (orbit N50 s) := by
      rw [LychrelCertificates.orbit_add, orbit196_50]
      rfl
    rw [horb] at hP
    obtain ⟨d, hd, hrep⟩ :=
      iterPairs_representation N50 d50 q50 24 s canonical50 (fun _ _ => rfl)
    have hmem := canonical_last_step_initialL k e.1 hm hlen hno hd rfl hP
    have hproj := projectK_congr k (columnSum d (iterPairs q50 24 s).1)
      (iterPairs q50 24 s).2 (iterPairs q50 24 s).1 hrep
    rw [hproj] at hmem
    have hW : k ≤ (iterPairs q50 24 s).1 := Nat.le_trans hk (iterPairs_width_ge q50 24 s)
    rw [projectK_long _ _ _ hW] at hmem
    have hw := List.all_eq_true.mp hall _ hmem
    split at hw
    · rename_i r hr
      have hrb : r ≤ e.2 := by simpa [Nat.ble_eq] using hw
      have hadm : Admissible 24 q50 := canonical_admissible N50 d50 24 canonical50
      have := rank_long (by omega) rows q50 24 hadm hk s r hr
      omega
    · contradiction

end Sprint.Agent02

#print axioms Sprint.Agent02.rank_long
#print axioms Sprint.Agent02.orbit196_50
#print axioms Sprint.Agent02.canonical50
#print axioms Sprint.Agent02.no_196_of_entry_long
