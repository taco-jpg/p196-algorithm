import P196.UniformCarryWindows.UniformEscape

set_option autoImplicit false

/-!
# A finite carry-total decoder without an initial width parameter

The existing weighted carry budget forces the digit sum to grow by at most
eight doublings in each block of nine ordinary reverse-and-add operations.
An upper bound on the first twelve outgoing carry totals then supplies a
terminal digit-sum bound at a horizon computed only from that observed bound.
The existing exact decoder applies at that horizon.

Counts include the terminal carry, and the ordinary orbit continues after
a palindrome. These estimates do not assert an optimal observation length
or recover the initial integer.
-/

namespace AdaptiveCarryDecoding

open Lychrel196 DecimalMass CarryCountGrowth CarryCountDecoding

/-- The required observation count, computed from a ceiling on the first
twelve actual outgoing carry totals. -/
def horizon (B : Nat) : Nat :=
  9 * (Nat.log2 (11 * B) + 2)

/-- Every chosen horizon includes all twelve pilot observations. -/
theorem horizon_ge_eighteen (B : Nat) : 18 ≤ horizon B := by
  unfold horizon
  omega

private theorem digitSum_growth_budget (n N : Nat) :
    10 * digitSum (orbit n N) ≤
      (2 ^ N + 162 * (N + 1)) * digitSum n := by
  have hm := UniformCarryWindows.weighted_mass_bound n N
  have hb := weightedCount_balance n N
  have hleft : 2 ^ N * (2 * digitSum n) = 2 * (2 ^ N * digitSum n) := by
    exact Nat.mul_left_comm _ _ _
  have hright : 18 * (N + 1) * (2 * digitSum n) =
      36 * ((N + 1) * digitSum n) := by
    calc
      18 * (N + 1) * (2 * digitSum n) =
          (18 * 2) * ((N + 1) * digitSum n) := by ac_rfl
      _ = 36 * ((N + 1) * digitSum n) := rfl
  rw [hleft, hright] at hm
  have h : 10 * digitSum (orbit n N) ≤
      2 ^ N * digitSum n + 162 * ((N + 1) * digitSum n) := by omega
  simpa only [Nat.add_mul, Nat.mul_assoc] using h

private theorem digitSum_nine (n : Nat) :
    digitSum (orbit n 9) ≤ 2 ^ 8 * digitSum n := by
  have h := digitSum_growth_budget n 9
  change 10 * digitSum (orbit n 9) ≤ 2132 * digitSum n at h
  change digitSum (orbit n 9) ≤ 256 * digitSum n
  omega

/-- Nine actual operations grow the digit sum by at most eight doublings;
the estimate iterates without a width hypothesis and includes the zero seed. -/
theorem digitSum_nine_blocks (n r : Nat) :
    digitSum (orbit n (9 * r)) ≤ 2 ^ (8 * r) * digitSum n := by
  induction r with
  | zero => simp [orbit]
  | succ r ih =>
    have hnine := digitSum_nine (orbit n (9 * r))
    have hmul := Nat.mul_le_mul_left (2 ^ 8) ih
    calc
      digitSum (orbit n (9 * (r + 1))) =
          digitSum (orbit (orbit n (9 * r)) 9) := by
        rw [Nat.mul_succ, LychrelCertificates.orbit_add]
      _ ≤ 2 ^ 8 * digitSum (orbit n (9 * r)) := hnine
      _ ≤ 2 ^ 8 * (2 ^ (8 * r) * digitSum n) := hmul
      _ = 2 ^ (8 * (r + 1)) * digitSum n := by
        rw [← Nat.mul_assoc, ← Nat.pow_add,
          show 8 + 8 * r = 8 * (r + 1) by omega]

private theorem terminal_bound_of_first_twelve (n B : Nat)
    (hC : ∀ t, t < 12 → outgoingCarryCount (orbit n t) ≤ B) :
    digitSum (orbit n (horizon B)) ≤ 2 ^ horizon B := by
  let r := Nat.log2 (11 * B) + 2
  have hsmall := UniformCarryWindows.digitSum_le_of_twelve_carry_ceiling n B hC
  have hlog : 11 * B < 2 ^ (Nat.log2 (11 * B)) * 2 := by
    simpa only [Nat.pow_succ] using (Nat.lt_log2_self (n := 11 * B))
  have hstart : digitSum n ≤ 2 ^ r := by
    dsimp [r]
    rw [Nat.pow_add]
    change digitSum n ≤ 2 ^ (Nat.log2 (11 * B)) * 4
    omega
  have hblocks := digitSum_nine_blocks n r
  have hmul := Nat.mul_le_mul_left (2 ^ (8 * r)) hstart
  calc
    digitSum (orbit n (horizon B)) = digitSum (orbit n (9 * r)) := rfl
    _ ≤ 2 ^ (8 * r) * digitSum n := hblocks
    _ ≤ 2 ^ (8 * r) * 2 ^ r := hmul
    _ = 2 ^ horizon B := by
      rw [← Nat.pow_add]
      change 2 ^ (8 * r + r) = 2 ^ (9 * r)
      congr 1
      omega

/-- A positive seed's initial digit sum is recovered exactly at the horizon
determined by any ceiling on its first twelve actual carry totals. -/
theorem digitSum_eq_decode_of_first_twelve
    (n B : Nat) (hn : 0 < n)
    (hC : ∀ t, t < 12 → outgoingCarryCount (orbit n t) ≤ B) :
    digitSum n =
      9 * weightedCount (fun t => outgoingCarryCount (orbit n t))
        (horizon B) / 2 ^ horizon B + 1 :=
  digitSum_eq_decode_of_terminal_bound n (horizon B) hn
    (terminal_bound_of_first_twelve n B hC)

#print axioms digitSum_nine_blocks
#print axioms digitSum_eq_decode_of_first_twelve

end AdaptiveCarryDecoding
