import P196.OrdinaryImageCensus.Profiles
import P196.OrdinaryImageSparsity.Enumeration
import P196.Agent105InverseBoundaries.Agent105WidthSupport9df76b
import P196.FoldedCollisionPrefixes.Targets

/-!
# Exact output widths and the two source-width classes

The existing ordinary image list supplies a duplicate-free census at each
decimal output width. The actual terminal carry puts every predecessor in
one of two adjacent source widths. Their numerical intersection is exactly
the previously defined ordinary common-target predicate.
-/

set_option autoImplicit false

namespace OrdinaryImageCensus

open DecimalDigits FoldedDecimal Lychrel196 Agent101
open Agent105WidthSupport9df76b FoldedCollisionPrefixes

/-- All distinct positive ordinary reverse-and-add outputs of width W. -/
def widthTargets (W : Nat) : List Nat :=
  (OrdinaryImageSparsity.allBelow (10 ^ W)).filter
    (fun Y => decide (10 ^ (W - 1) ≤ Y))

/-- Restricting the existing ordinary image census preserves duplicate freedom. -/
theorem widthTargets_nodup (W : Nat) : (widthTargets W).Nodup := by
  exact List.Pairwise.filter _ (OrdinaryImageSparsity.allBelow_nodup (10 ^ W))

/-- Membership specifies the exact positive decimal output width and an
ordinary positive predecessor, without any additional source restriction. -/
theorem mem_widthTargets (W Y : Nat) :
    Y ∈ widthTargets W ↔
      decimalWidth Y W ∧ ∃ n : Nat, 0 < n ∧ step n = Y := by
  rw [widthTargets, List.mem_filter, OrdinaryImageSparsity.mem_allBelow]
  simp only [decide_eq_true_eq]
  constructor
  · rintro ⟨⟨hupper, hsource⟩, hlower⟩
    have hW : 0 < W := by
      by_cases hz : W = 0
      · subst W
        simp only [Nat.zero_sub, Nat.pow_zero] at hupper hlower
        omega
      · omega
    exact ⟨⟨hW, hlower, hupper⟩, hsource⟩
  · rintro ⟨⟨_, hlower, hupper⟩, hsource⟩
    exact ⟨⟨hupper, hsource⟩, hlower⟩

private theorem carryValues_width (L c Y : Nat)
    (hY : Y ∈ carryValues L c) :
    decimalWidth Y (L + c) ∧ ∃ n : Nat, 0 < n ∧ step n = Y := by
  obtain ⟨n, d, hn, hs, hc⟩ := (mem_carryValues L c Y).mp hY
  obtain ⟨e, he⟩ := canonical_step_exists hn
  have hcanonical : Canonical Y e (L + c) := by
    simpa only [hs, hc] using he
  have hpositive : 0 < n :=
    Nat.lt_of_lt_of_le (Nat.pow_pos (by decide))
      (canonical_decimalWidth n d L hn).2.1
  exact ⟨canonical_decimalWidth Y e (L + c) hcanonical, n, hpositive, hs⟩

/-- Every output of positive width comes from a same-width source without
overflow or from a source one digit shorter with terminal carry one. -/
theorem mem_widthTargets_iff_carryValues (W Y : Nat) (hW : 0 < W) :
    Y ∈ widthTargets W ↔
      Y ∈ carryValues W 0 ∨ Y ∈ carryValues (W - 1) 1 := by
  constructor
  · intro hY
    obtain ⟨hw, n, hn, hs⟩ := (mem_widthTargets W Y).mp hY
    obtain ⟨d, L, hcanonical⟩ := canonical_exists n hn
    obtain ⟨e, he⟩ := (decimalWidth_iff_canonical Y W).mp hw
    have hstep : Canonical (step n) e W := by
      simpa only [hs] using he
    rcases step_width_cases hcanonical hstep with
      ⟨hwidth, hcarry⟩ | ⟨hwidth, hcarry⟩
    · subst L
      exact Or.inl ((mem_carryValues W 0 Y).mpr
        ⟨n, d, hcanonical, hs, hcarry⟩)
    · have hL : L = W - 1 := by omega
      subst L
      exact Or.inr ((mem_carryValues (W - 1) 1 Y).mpr
        ⟨n, d, hcanonical, hs, hcarry⟩)
  · intro hY
    apply (mem_widthTargets W Y).mpr
    rcases hY with hY | hY
    · simpa only [Nat.add_zero] using carryValues_width W 0 Y hY
    · have hwidth : W - 1 + 1 = W := by omega
      simpa only [hwidth] using carryValues_width (W - 1) 1 Y hY

/-- The two source-width classes overlap exactly at ordinary outputs
shared by canonical sources of the adjacent widths W-1 and W. -/
theorem mem_overlap_iff (W Y : Nat) (hW : 0 < W) :
    (Y ∈ carryValues W 0 ∧ Y ∈ carryValues (W - 1) 1) ↔
      CommonTarget (W - 1) Y := by
  have hwidth : W - 1 + 1 = W := by omega
  constructor
  · rintro ⟨hLong, hShort⟩
    obtain ⟨n, d, hn, hsn, _⟩ := (mem_carryValues (W - 1) 1 Y).mp hShort
    obtain ⟨m, e, hm, hsm, _⟩ := (mem_carryValues W 0 Y).mp hLong
    exact ⟨n, m, d, e, hn, by simpa only [hwidth] using hm, hsn, hsm⟩
  · rintro ⟨n, m, d, e, hn, hm, hsn, hsm⟩
    obtain ⟨_, hshort, hlong⟩ := cross_width_carries hn hm
      (Nat.lt_succ_self (W - 1)) (hsn.trans hsm.symm)
    constructor
    · apply (mem_carryValues W 0 Y).mpr
      exact ⟨m, e, by simpa only [hwidth] using hm, hsm,
        by simpa only [hwidth] using hlong⟩
    · exact (mem_carryValues (W - 1) 1 Y).mpr ⟨n, d, hn, hsn, hshort⟩

end OrdinaryImageCensus

#print axioms OrdinaryImageCensus.widthTargets
#print axioms OrdinaryImageCensus.widthTargets_nodup
#print axioms OrdinaryImageCensus.mem_widthTargets
#print axioms OrdinaryImageCensus.mem_widthTargets_iff_carryValues
#print axioms OrdinaryImageCensus.mem_overlap_iff
