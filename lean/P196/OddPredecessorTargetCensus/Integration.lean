import P196.OddPredecessorTargetCensus.Targets

/-!
# Exact census of targets with odd predecessor cardinality

Agent #6: combine the two disjoint coefficient families at their actual
target width. The complete target enumeration supplies the counting
semantics; the formulas below evaluate its cardinality at every width.
-/

set_option autoImplicit false

namespace OddPredecessorTargetCensus

/-- The census length is the sum of its two source-width contributions,
including the empty width-zero case. -/
theorem length_targets (W : Nat) :
    (targets W).length =
      (noOverflowWords W).length + (overflowWords (W - 1)).length := by
  cases W with
  | zero => rfl
  | succ W =>
    simp only [targets, Nat.succ_ne_zero, if_false,
      List.length_map, List.length_append]

/-- There is no positive ordinary decimal target of width zero. -/
theorem length_targets_zero : (targets 0).length = 0 := by
  rfl

/-- Exactly four one-digit targets have odd complete predecessor count. -/
theorem length_targets_one : (targets 1).length = 4 := by
  simp [length_targets, length_noOverflowWords, length_overflowWords]

/-- The three-digit boundary contains exactly fifty such targets. -/
theorem length_targets_three : (targets 3).length = 50 := by
  simp [length_targets, length_noOverflowWords, length_overflowWords]

/-- At every positive even width, the census is a single power of ten. -/
theorem length_targets_even (k : Nat) :
    (targets (2 * k + 2)).length = 10 ^ (k + 1) := by
  cases k with
  | zero =>
    simp [length_targets, length_noOverflowWords, length_overflowWords]
  | succ k =>
    have hl : (2 * (k + 1) + 2 - 3) / 2 = k := by omega
    have hr : (2 * (k + 1) + 2 - 1 - 3) / 2 = k := by omega
    simp (disch := omega) only [length_targets, length_noOverflowWords,
      length_overflowWords, if_neg, hl, hr]
    rw [Nat.pow_succ, Nat.pow_succ]
    omega

/-- At each odd width of at least five, the two families contribute
forty-five times the next power of ten and fifty-five times the current one. -/
theorem length_targets_odd (k : Nat) :
    (targets (2 * k + 5)).length = 505 * 10 ^ k := by
  have hl : (2 * k + 5 - 3) / 2 = k + 1 := by omega
  have hr : (2 * k + 5 - 1 - 3) / 2 = k := by omega
  simp (disch := omega) only [length_targets, length_noOverflowWords,
    length_overflowWords, if_neg, hl, hr]
  rw [Nat.pow_succ]
  omega

end OddPredecessorTargetCensus

#print axioms OddPredecessorTargetCensus.length_targets
#print axioms OddPredecessorTargetCensus.length_targets_zero
#print axioms OddPredecessorTargetCensus.length_targets_one
#print axioms OddPredecessorTargetCensus.length_targets_three
#print axioms OddPredecessorTargetCensus.length_targets_even
#print axioms OddPredecessorTargetCensus.length_targets_odd
