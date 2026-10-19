import P196.MaximalDigitSplitFibers.Numeric
import P196.Agent101AllWidthMaximum.Agent101WidthFiberBounds

/-!
Agent #7: the sharp gap for a complete ordinary-integer predecessor fiber
of any target at one prescribed source width. A member determines the
profile; the empty fiber is treated directly. Source widths are not combined.
-/

namespace Agent7.MaximalDigitSplitFibers

open Agent101 DecimalDigits Lychrel196

/-- One actual member determines a profile whose original numerical fiber
has exactly the prescribed complete list's members and cardinality. -/
theorem complete_fixed_width_fiber_profile (Y L : Nat) (xs : List Nat)
    (hL : 2 ≤ L) (hxs : xs.Nodup)
    (hm : ∀ n, n ∈ xs ↔ decimalWidth n L ∧ step n = Y)
    (hne : xs ≠ []) :
    ∃ s h c,
      h.length = L / 2 - 1 ∧
      (coefficientWord (s :: h) c).length = L ∧
      natValue (coefficientWord (s :: h) c) = Y ∧
      (∀ n, n ∈ xs ↔ n ∈ numericFiber (s :: h) c) ∧
      xs.length = (numericFiber (s :: h) c).length := by
  cases xs with
  | nil => exact False.elim (hne rfl)
  | cons n xs =>
      have hn := (hm n).mp (by simp)
      obtain ⟨d, hc⟩ := (decimalWidth_iff_canonical n L).mp hn.1
      obtain ⟨ds, hlen, hd, hv, _⟩ := canonical_to_list n d L hc
      obtain ⟨s, h, c, hp, hh, hwordlen, _⟩ :=
        digitPairSums_profile_cons ds (by omega)
      have htarget : natValue (coefficientWord (s :: h) c) = Y := by
        rw [← hp, ← step_natValue ds hd, hv, hn.2]
      have hleft : ∀ m ∈ n :: xs, m ∈ numericFiber (s :: h) c := by
        intro m hmem
        obtain ⟨hw, hs⟩ := (hm m).mp hmem
        apply mem_numericFiber_of_same_width_step ds (s :: h) c hd hp m
        · simpa only [hlen] using hw
        · simpa only [hv, hn.2] using hs
      have hright : ∀ m ∈ numericFiber (s :: h) c, m ∈ n :: xs := by
        intro m hmem
        obtain ⟨es, hes, hpairs, hvalue⟩ :=
          (mem_numericFiber_digits (s :: h) c m).mp hmem
        have helen : es.length = L := by
          calc
            es.length = (digitPairSums es).length :=
              (numeric_length_digitPairSums es).symm
            _ = (coefficientWord (s :: h) c).length := congrArg List.length hpairs
            _ = L := hwordlen.trans hlen
        apply (hm m).mpr
        refine ⟨?_, ?_⟩
        · have hw := canonical_decimalWidth _ _ _
            ((canonicalDigits_iff es).mp hes)
          simpa only [hvalue, helen] using hw
        · rw [← hvalue, step_natValue es hes, hpairs, htarget]
      refine ⟨s, h, c, ?_, hwordlen.trans hlen, htarget, ?_, ?_⟩
      · simpa only [hlen] using hh
      · intro m
        exact ⟨hleft m, hright m⟩
      · apply Nat.le_antisymm
        · exact P196.Agent2.OverflowFibers.nodup_subset_length_le
            (n :: xs) (numericFiber (s :: h) c) hxs hleft
        · exact P196.Agent2.OverflowFibers.nodup_subset_length_le
            (numericFiber (s :: h) c) (n :: xs) (numericFiber_nodup _ _) hright

/-- Every complete duplicate-free predecessor list at one source width
`L ≥ 4` either attains the established maximum or lies below this sharp
submaximum. The target is arbitrary, and empty fibers are included. -/
theorem fixed_width_preimages_gap (Y L : Nat) (xs : List Nat)
    (hL : 4 ≤ L) (hxs : xs.Nodup)
    (hm : ∀ n, n ∈ xs ↔ decimalWidth n L ∧ step n = Y)
    (hne : xs.length ≠ 9 * 10 ^ (L / 2 - 1)) :
    xs.length ≤ 81 * 10 ^ (L / 2 - 2) := by
  by_cases hempty : xs = []
  · subst xs
    simp
  · obtain ⟨s, h, c, hh, _, _, _, hcount⟩ :=
      complete_fixed_width_fiber_profile Y L xs (by omega) hxs hm hempty
    have hinner : 0 < h.length := by rw [hh]; omega
    have hn : (numericFiber (s :: h) c).length ≠ 9 * 10 ^ h.length := by
      simpa only [hh, hcount] using hne
    have hg := numericFiber_gap s h c hinner hn
    rw [hh, ← hcount] at hg
    have he : L / 2 - 1 - 1 = L / 2 - 2 := by omega
    simpa only [he] using hg

#print axioms complete_fixed_width_fiber_profile
#print axioms fixed_width_preimages_gap

end Agent7.MaximalDigitSplitFibers
