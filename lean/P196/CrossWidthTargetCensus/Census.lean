import P196.CrossWidthTargetCensus.Families

/-!
# A finite census of ordinary targets shared across source widths

For every shorter source width L, the executable list contains exactly
the ordinary reverse-and-add outputs shared by canonical sources of
widths L and L+1. Every target occurs once. The neighboring shorter
widths 2*k+2 and 2*k+3 have equally many distinct common targets.
-/

set_option autoImplicit false

namespace CrossWidthTargetCensus

open FoldedCollisionPrefixes

/-- All distinct ordinary outputs shared by sources of widths L and L+1. -/
def targets (L : Nat) : List Nat :=
  if L < 2 then []
  else if L % 2 = 0 then evenTargets ((L - 2) / 2)
  else oddTargets ((L - 3) / 2)

/-- Even shorter widths select the even finite-prefix family. -/
theorem targets_even (k : Nat) : targets (2 * k + 2) = evenTargets k := by
  have hsmall : ¬ 2 * k + 2 < 2 := by omega
  have hmod : (2 * k + 2) % 2 = 0 := by omega
  have hindex : (2 * k + 2 - 2) / 2 = k := by omega
  simp only [targets, if_neg hsmall, if_pos hmod, hindex]

/-- Odd shorter widths select the uniquely extended prefix family. -/
theorem targets_odd (k : Nat) : targets (2 * k + 3) = oddTargets k := by
  have hsmall : ¬ 2 * k + 3 < 2 := by omega
  have hmod : ¬ (2 * k + 3) % 2 = 0 := by omega
  have hindex : (2 * k + 3 - 3) / 2 = k := by omega
  simp only [targets, if_neg hsmall, if_neg hmod, hindex]

/-- A zero-width shorter source contributes no common target. -/
theorem targets_zero : targets 0 = [] := rfl

/-- A one-digit shorter source contributes no common target. -/
theorem targets_one : targets 1 = [] := rfl

private theorem commonTarget_length {L Y : Nat} (h : CommonTarget L Y) :
    2 ≤ L := by
  obtain ⟨n, m, d, e, hn, hm, hnY, hmY⟩ := h
  exact Agent105CrossWidth9df76b.cross_width_short_length hn hm (by omega)
    (hnY.trans hmY.symm)

/-- The census is complete and sound for ordinary common integer outputs. -/
theorem mem_targets (L Y : Nat) : Y ∈ targets L ↔ CommonTarget L Y := by
  by_cases hsmall : L < 2
  · rw [targets, if_pos hsmall]
    constructor
    · intro h
      exact False.elim (List.not_mem_nil h)
    · intro h
      have := commonTarget_length h
      omega
  · by_cases hmod : L % 2 = 0
    · have hindex : 2 * ((L - 2) / 2) + 2 = L := by omega
      rw [targets, if_neg hsmall, if_pos hmod, mem_evenTargets, hindex]
    · have hindex : 2 * ((L - 3) / 2) + 3 = L := by omega
      rw [targets, if_neg hsmall, if_neg hmod, mem_oddTargets, hindex]

/-- Every ordinary target in the census occurs exactly once. -/
theorem targets_nodup (L : Nat) : (targets L).Nodup := by
  unfold targets
  split
  · exact List.Pairwise.nil
  · split
    · exact evenTargets_nodup _
    · exact oddTargets_nodup _

/-- Adjacent even and odd shorter source widths have equal target counts. -/
theorem targets_paired_length (k : Nat) :
    (targets (2 * k + 2)).length = (targets (2 * k + 3)).length := by
  rw [targets_even, targets_odd]
  exact paired_target_lengths k

/-- Kernel-checked counts for shorter source widths zero through seven. -/
theorem small_target_counts :
    (List.range 8).map (fun L => (targets L).length) = [0, 0, 1, 1, 2, 2, 7, 7] := by
  decide +kernel

/-- The first nonempty family consists only of the ordinary output 121. -/
theorem targets_two : targets 2 = [121] := by
  decide +kernel

/-- Its odd-parity partner consists only of the ordinary output 1111. -/
theorem targets_three : targets 3 = [1111] := by
  decide +kernel

end CrossWidthTargetCensus

#print axioms CrossWidthTargetCensus.targets
#print axioms CrossWidthTargetCensus.targets_even
#print axioms CrossWidthTargetCensus.targets_odd
#print axioms CrossWidthTargetCensus.targets_zero
#print axioms CrossWidthTargetCensus.targets_one
#print axioms CrossWidthTargetCensus.mem_targets
#print axioms CrossWidthTargetCensus.targets_nodup
#print axioms CrossWidthTargetCensus.targets_paired_length
#print axioms CrossWidthTargetCensus.small_target_counts
#print axioms CrossWidthTargetCensus.targets_two
#print axioms CrossWidthTargetCensus.targets_three
