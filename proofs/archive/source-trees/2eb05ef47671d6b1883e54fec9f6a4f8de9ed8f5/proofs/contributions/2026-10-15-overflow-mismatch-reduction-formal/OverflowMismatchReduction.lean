import OverflowMismatch

/-! Exact detection scope of positive-terminal isolated carry mismatch.
For coefficients at most 18, such a certificate exists precisely when
there is both a positive coefficient at most 9 and a coefficient at least 10.
Whenever a certificate exists, singleton intervals already suffice. -/

namespace OverflowMismatchReduction

open DecimalDigits FoldedDecimal OverflowCarryNormalization Lychrel196 OverflowMismatch

def HasIntervalMismatch (q : Nat → Nat) (L : Nat) : Prop :=
  ∃ a m b k, PositiveTerminalInterval q L a m ∧
    PositiveTerminalInterval q L b k ∧ isolatedCarry q a m ≠ isolatedCarry q b k

def MixedCoefficients (q : Nat → Nat) (L : Nat) : Prop :=
  (∃ i, i < L ∧ 0 < q i ∧ q i ≤ 9) ∧ (∃ j, j < L ∧ 10 ≤ q j)

theorem isolatedCarry_le_one (q : Nat → Nat) (L start length : Nat)
    (hbound : ∀ i, i < L → q i ≤ 18) (hinside : start + length ≤ L) :
    isolatedCarry q start length ≤ 1 :=
  carry_bounded (fun i => q (start + i)) length
    (fun i hi => hbound (start + i) (by omega)) length (Nat.le_refl length)

theorem isolatedCarry_zero_terminal_small (q : Nat → Nat) (start length : Nat)
    (hlen : 0 < length) (hzero : isolatedCarry q start length = 0) :
    q (start + (length - 1)) ≤ 9 := by
  have hi : length = (length - 1) + 1 := by omega
  unfold isolatedCarry at hzero
  rw [hi, carry] at hzero
  omega

theorem isolatedCarry_positive_has_high (q : Nat → Nat) (start length : Nat)
    (hpositive : 0 < isolatedCarry q start length) :
    ∃ j, start ≤ j ∧ j < start + length ∧ 10 ≤ q j := by
  apply Classical.byContradiction
  intro hn
  have hsmall : ∀ i, i < length → q (start + i) ≤ 9 := by
    intro i hi
    have hnhi : ¬ 10 ≤ q (start + i) := by
      intro hg
      exact hn ⟨start + i, by omega, by omega, hg⟩
    omega
  have hz := carry_zero_of_small (fun i => q (start + i)) length hsmall
  change 0 < carry (fun i => q (start + i)) length at hpositive
  omega

theorem mismatch_implies_mixed (q : Nat → Nat) (L : Nat)
    (hbound : ∀ i, i < L → q i ≤ 18) (hmismatch : HasIntervalMismatch q L) :
    MixedCoefficients q L := by
  obtain ⟨a, m, b, k, ha, hb, hne⟩ := hmismatch
  have hca := isolatedCarry_le_one q L a m hbound ha.2.1
  have hcb := isolatedCarry_le_one q L b k hbound hb.2.1
  by_cases hzero : isolatedCarry q a m = 0
  · have hsmall := isolatedCarry_zero_terminal_small q a m ha.1 hzero
    obtain ⟨j, _, hj, hhigh⟩ := isolatedCarry_positive_has_high q b k (by omega)
    exact ⟨⟨a + (m - 1), by have := ha.1; have := ha.2.1; omega,
      ha.2.2, hsmall⟩, ⟨j, by have := hb.2.1; omega, hhigh⟩⟩
  · have hzeroB : isolatedCarry q b k = 0 := by omega
    have hsmall := isolatedCarry_zero_terminal_small q b k hb.1 hzeroB
    obtain ⟨j, _, hj, hhigh⟩ := isolatedCarry_positive_has_high q a m (by omega)
    exact ⟨⟨b + (k - 1), by have := hb.1; have := hb.2.1; omega,
      hb.2.2, hsmall⟩, ⟨j, by have := ha.2.1; omega, hhigh⟩⟩

theorem mixed_implies_singleton_mismatch (q : Nat → Nat) (L : Nat)
    (hmixed : MixedCoefficients q L) :
    ∃ a b, PositiveTerminalInterval q L a 1 ∧
      PositiveTerminalInterval q L b 1 ∧ isolatedCarry q a 1 ≠ isolatedCarry q b 1 := by
  obtain ⟨⟨a, ha, hapos, hasmall⟩, ⟨b, hb, hbhigh⟩⟩ := hmixed
  refine ⟨a, b, ?_, ?_, ?_⟩
  · unfold PositiveTerminalInterval
    simp only [Nat.sub_self, Nat.add_zero]
    exact ⟨by decide, by omega, hapos⟩
  · unfold PositiveTerminalInterval
    simp only [Nat.sub_self, Nat.add_zero]
    exact ⟨by decide, by omega, by omega⟩
  · simp only [isolatedCarry, carry, Nat.add_zero]
    omega

theorem mixed_implies_mismatch (q : Nat → Nat) (L : Nat)
    (hmixed : MixedCoefficients q L) : HasIntervalMismatch q L := by
  obtain ⟨a, b, ha, hb, hne⟩ := mixed_implies_singleton_mismatch q L hmixed
  exact ⟨a, 1, b, 1, ha, hb, hne⟩

theorem interval_mismatch_iff_mixed (q : Nat → Nat) (L : Nat)
    (hbound : ∀ i, i < L → q i ≤ 18) :
    HasIntervalMismatch q L ↔ MixedCoefficients q L :=
  ⟨mismatch_implies_mixed q L hbound, mixed_implies_mismatch q L⟩

theorem interval_mismatch_iff_singletons (q : Nat → Nat) (L : Nat)
    (hbound : ∀ i, i < L → q i ≤ 18) :
    HasIntervalMismatch q L ↔
      ∃ a b, PositiveTerminalInterval q L a 1 ∧
        PositiveTerminalInterval q L b 1 ∧ isolatedCarry q a 1 ≠ isolatedCarry q b 1 := by
  constructor
  · intro h
    exact mixed_implies_singleton_mismatch q L (mismatch_implies_mixed q L hbound h)
  · rintro ⟨a, b, ha, hb, hne⟩
    exact ⟨a, 1, b, 1, ha, hb, hne⟩

theorem mixed_not_badWord (q : Nat → Nat) (L : Nat)
    (hmixed : MixedCoefficients q L) : ¬ BadWord L q := by
  obtain ⟨a, m, b, k, ha, hb, hne⟩ := mixed_implies_mismatch q L hmixed
  exact mismatch_not_badWord q L a m b k ha hb hne

theorem numeric_mixed_safe (n : Nat) (d q : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hmixed : MixedCoefficients q L) : ¬ Palindrome (step n) := by
  obtain ⟨a, m, b, k, ha, hb, hne⟩ := mixed_implies_mismatch q L hmixed
  exact numeric_mismatch_safe n d q L a m b k hc hrep ha hb hne

theorem numeric_orbit_mixed_safe (n : Nat) (d q : Nat → Nat) (L t : Nat)
    (hc : Canonical n d L) (hrep : ∀ i, i < L → columnSum d L i = q i)
    (hmixed : MixedCoefficients (iterPairs q L t).2 (iterPairs q L t).1) :
    ¬ Palindrome (orbit n (t + 1)) := by
  obtain ⟨e, he, her⟩ := iterPairs_representation n d q L t hc hrep
  exact numeric_mixed_safe (orbit n t) e (iterPairs q L t).2
    (iterPairs q L t).1 he her hmixed

/-- This certificate is sufficient but not necessary for one-step safety. -/
theorem detection_is_incomplete :
    ¬ HasIntervalMismatch (fun _ => 14) 2 ∧
    step 77 = 154 ∧ ¬ Palindrome (step 77) := by
  refine ⟨?_, by decide, by decide⟩
  intro h
  obtain ⟨⟨i, _, _, hi⟩, _⟩ := mismatch_implies_mixed (fun _ => 14) 2
    (by intro _ _; exact (by decide : 14 ≤ 18)) h
  change 14 ≤ 9 at hi
  omega

end OverflowMismatchReduction
