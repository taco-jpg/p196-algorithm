import P196.CrossWidthTargetRecurrence.Weighted
import P196.CrossWidthTargetRecurrence.Certificate

/-!
# The exact recurrence for ordinary cross-width target counts

The checked cubic transfer identity holds at every last state in the
existing walk census. Summing it and applying the weighted append identity
three times gives the even-family recurrence. The established parity
pairing and initial census controls give one recurrence at every shorter
source width, including zero and one.
-/

set_option autoImplicit false

namespace CrossWidthTargetRecurrence

open CrossWidthCollisionStates FoldedCollisionPrefixes CrossWidthTargetCensus

private theorem fold_cubic {k : Nat} (ps : List (Prefix k))
    (hps : ∀ p ∈ ps, prefixAt p k ∈ productive) :
    ps.foldr (fun p total =>
      transfer (transfer (transfer terminalWeight)) (prefixAt p k) + total) 0 =
    2 * ps.foldr (fun p total =>
      transfer (transfer terminalWeight) (prefixAt p k) + total) 0 +
    3 * ps.foldr (fun p total =>
      transfer terminalWeight (prefixAt p k) + total) 0 +
    ps.foldr (fun p total => terminalWeight (prefixAt p k) + total) 0 := by
  induction ps with
  | nil => rfl
  | cons p ps ih =>
    have hp := transfer_cubic (hps p (by simp))
    have ht := ih (fun q hq => hps q (by simp [hq]))
    simp only [List.foldr_cons, Nat.mul_add]
    omega

/-- The finite certificate remains exact when summed over the existing
productive walk list. -/
theorem weightedWalks_cubic (k : Nat) :
    weightedWalks k (transfer (transfer (transfer terminalWeight))) =
      2 * weightedWalks k (transfer (transfer terminalWeight)) +
      3 * weightedWalks k (transfer terminalWeight) +
      weightedWalks k terminalWeight := by
  apply fold_cubic
  intro p hp
  exact ((mem_walkPrefixes k p).mp hp).2 _

/-- Counts of distinct ordinary common targets at even shorter widths
satisfy the cubic recurrence with coefficients two, three, and one. -/
theorem even_count_recurrence (k : Nat) :
    (targets (2 * (k + 3) + 2)).length =
      2 * (targets (2 * (k + 2) + 2)).length +
      3 * (targets (2 * (k + 1) + 2)).length +
      (targets (2 * k + 2)).length := by
  have h : weightedWalks (k + 3) terminalWeight =
      2 * weightedWalks (k + 2) terminalWeight +
      3 * weightedWalks (k + 1) terminalWeight +
      weightedWalks k terminalWeight := by
    calc
      weightedWalks (k + 3) terminalWeight =
          weightedWalks k (transfer (transfer (transfer terminalWeight))) := by
        rw [weightedWalks_succ (k + 2) terminalWeight,
          weightedWalks_succ (k + 1) (transfer terminalWeight),
          weightedWalks_succ k (transfer (transfer terminalWeight))]
      _ = 2 * weightedWalks k (transfer (transfer terminalWeight)) +
          3 * weightedWalks k (transfer terminalWeight) +
          weightedWalks k terminalWeight := weightedWalks_cubic k
      _ = 2 * weightedWalks (k + 2) terminalWeight +
          3 * weightedWalks (k + 1) terminalWeight +
          weightedWalks k terminalWeight := by
        rw [weightedWalks_succ (k + 1) terminalWeight,
          weightedWalks_succ k (transfer terminalWeight),
          weightedWalks_succ k terminalWeight]
  simpa only [weightedWalks_terminal, targets_even] using h

private theorem odd_count_recurrence (k : Nat) :
    (targets (2 * (k + 3) + 3)).length =
      2 * (targets (2 * (k + 2) + 3)).length +
      3 * (targets (2 * (k + 1) + 3)).length +
      (targets (2 * k + 3)).length := by
  rw [← targets_paired_length (k + 3), ← targets_paired_length (k + 2),
    ← targets_paired_length (k + 1), ← targets_paired_length k]
  exact even_count_recurrence k

private theorem initial_recurrence (L : Nat) (hL : L < 2) :
    (targets (L + 6)).length =
      2 * (targets (L + 4)).length +
      3 * (targets (L + 2)).length + (targets L).length := by
  have h4 := congrArg (fun ns : List Nat => ns[4]!) small_target_counts
  have h6 := congrArg (fun ns : List Nat => ns[6]!) small_target_counts
  change (targets 4).length = 2 at h4
  change (targets 6).length = 7 at h6
  have hcases : L = 0 ∨ L = 1 := by omega
  rcases hcases with rfl | rfl
  · change (targets 6).length =
      2 * (targets 4).length + 3 * (targets 2).length + (targets 0).length
    rw [h6, h4, targets_two, targets_zero]
    rfl
  · have h5 : (targets 5).length = 2 :=
      (targets_paired_length 1).symm.trans h4
    have h7 : (targets 7).length = 7 :=
      (targets_paired_length 2).symm.trans h6
    change (targets 7).length =
      2 * (targets 5).length + 3 * (targets 3).length + (targets 1).length
    rw [h7, h5, targets_three, targets_one]
    rfl

/-- Every shorter source width satisfies one exact recurrence, including
the empty width-zero and width-one families. -/
theorem target_count_recurrence (L : Nat) :
    (targets (L + 6)).length =
      2 * (targets (L + 4)).length +
      3 * (targets (L + 2)).length + (targets L).length := by
  by_cases hsmall : L < 2
  · exact initial_recurrence L hsmall
  · by_cases hmod : L % 2 = 0
    · let k := (L - 2) / 2
      have hL : 2 * k + 2 = L := by dsimp [k]; omega
      have h3 : 2 * (k + 3) + 2 = L + 6 := by omega
      have h2 : 2 * (k + 2) + 2 = L + 4 := by omega
      have h1 : 2 * (k + 1) + 2 = L + 2 := by omega
      simpa only [h3, h2, h1, hL] using even_count_recurrence k
    · let k := (L - 3) / 2
      have hL : 2 * k + 3 = L := by dsimp [k]; omega
      have h3 : 2 * (k + 3) + 3 = L + 6 := by omega
      have h2 : 2 * (k + 2) + 3 = L + 4 := by omega
      have h1 : 2 * (k + 1) + 3 = L + 2 := by omega
      simpa only [h3, h2, h1, hL] using odd_count_recurrence k

end CrossWidthTargetRecurrence

#print axioms CrossWidthTargetRecurrence.weightedWalks_cubic
#print axioms CrossWidthTargetRecurrence.even_count_recurrence
#print axioms CrossWidthTargetRecurrence.target_count_recurrence
