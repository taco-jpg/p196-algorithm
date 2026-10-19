import P196.CarryCountGrowth.CarryCountGrowth

set_option autoImplicit false

/-!
# Recovering digit sums from finite histories of outgoing carry totals

The chronological total carry counts satisfy an exact weighted mass identity.
For a positive seed, the identity recovers its initial digit sum once the
terminal digit sum is at most the corresponding power of two. The existing
actual-width bound supplies a numerical sufficient condition, and
`Nat.log2 L + 6` observations suffice when the initial decimal width is at
most `L`.

Only the total number of outgoing carry positions in each step is observed;
the count includes the terminal carry. Two seeds may have different widths.
The ordinary orbit continues after a palindrome. The results do not recover
the initial integer, assert an optimal observation horizon, or establish
palindrome avoidance.
-/

namespace CarryCountDecoding

open Lychrel196 DecimalDigits DecimalMass DecimalQuantitativeMass CarryCountGrowth

/-- Chronological powers-of-two weighting of the first `N` observations.
Earlier observations receive the larger weights. -/
def weightedCount (c : Nat → Nat) : Nat → Nat
  | 0 => 0
  | t + 1 => 2 * weightedCount c t + c t

private theorem weightedCount_congr (c d : Nat → Nat) (N : Nat) :
    (∀ t, t < N → c t = d t) → weightedCount c N = weightedCount d N := by
  induction N with
  | zero =>
      intro _
      rfl
  | succ N ih =>
      intro h
      simp only [weightedCount]
      rw [ih (fun t ht => h t (by omega)), h N (by omega)]

/-- Exact temporal mass balance, including the zero seed and an empty history. -/
theorem weightedCount_balance (n N : Nat) :
    digitSum (orbit n N) +
        9 * weightedCount (fun t => outgoingCarryCount (orbit n t)) N =
      2 ^ N * digitSum n := by
  induction N with
  | zero =>
      simp [weightedCount, orbit]
  | succ N ih =>
      have hb := outgoingCarryCount_balance (orbit n N)
      change digitSum (orbit n (N + 1)) +
        9 * outgoingCarryCount (orbit n N) = 2 * digitSum (orbit n N) at hb
      calc
        digitSum (orbit n (N + 1)) +
            9 * weightedCount (fun t => outgoingCarryCount (orbit n t)) (N + 1) =
          2 * (digitSum (orbit n N) +
            9 * weightedCount (fun t => outgoingCarryCount (orbit n t)) N) := by
              simp only [weightedCount]
              omega
        _ = 2 * (2 ^ N * digitSum n) := by rw [ih]
        _ = 2 ^ (N + 1) * digitSum n := by
          simp only [Nat.pow_succ, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]

/-- The exact decoder needs a positive terminal digit sum at most `2 ^ N`.
Equality at the upper endpoint is included. -/
theorem digitSum_eq_decode_of_terminal_bound
    (n N : Nat) (hn : 0 < n)
    (hN : digitSum (orbit n N) ≤ 2 ^ N) :
    digitSum n =
      9 * weightedCount (fun t => outgoingCarryCount (orbit n t)) N / 2 ^ N + 1 := by
  have hstart := digitSum_positive n hn
  have hfinish := digitSum_positive (orbit n N) (orbit_positive n hn N)
  have hb := weightedCount_balance n N
  obtain ⟨a, ha⟩ := Nat.exists_eq_add_one_of_ne_zero (by omega : digitSum n ≠ 0)
  rw [ha, Nat.mul_add, Nat.mul_one] at hb
  rw [Nat.mul_comm (2 ^ N) a] at hb
  have hlo : a * 2 ^ N ≤
      9 * weightedCount (fun t => outgoingCarryCount (orbit n t)) N := by
    omega
  have hhi : 9 * weightedCount (fun t => outgoingCarryCount (orbit n t)) N <
      (a + 1) * 2 ^ N := by
    rw [Nat.add_mul, Nat.one_mul]
    omega
  have hdiv := Nat.div_eq_of_lt_le hlo hhi
  rw [ha, hdiv]

/-- A numerical condition using the actual initial decimal width suffices
for exact recovery, without observing the terminal digit sum. -/
theorem digitSum_eq_decode_of_numeric_bound
    (n N : Nat) (hn : 0 < n)
    (hN : 18 * decimalLength n + 9 * N + 27 ≤ 2 ^ (N + 1)) :
    digitSum n =
      9 * weightedCount (fun t => outgoingCarryCount (orbit n t)) N / 2 ^ N + 1 := by
  apply digitSum_eq_decode_of_terminal_bound n N hn
  obtain ⟨d, L, hc⟩ := canonical_exists n hn
  have hmass := digitSum_twice_upper_bound_of_canonical n d L N hc
  rw [decimalLength_of_canonical n d L hc, Nat.pow_succ] at hN
  omega

/-- A sufficient observation length, logarithmic in a bound on decimal width. -/
def observationBound (L : Nat) : Nat := Nat.log2 L + 6

/-- The explicit observation length satisfies the numerical recovery criterion. -/
theorem observationBound_sufficient (L : Nat) :
    18 * L + 9 * observationBound L + 27 ≤ 2 ^ (observationBound L + 1) := by
  have hL : L < 2 ^ L.log2 * 2 := by
    simpa only [Nat.pow_succ] using (Nat.lt_log2_self (n := L))
  have hk : L.log2 < 2 ^ L.log2 := Nat.lt_two_pow_self
  have hp : 0 < 2 ^ L.log2 := Nat.two_pow_pos L.log2
  unfold observationBound
  rw [show L.log2 + 6 + 1 = L.log2 + 7 by omega, Nat.pow_add]
  simp only [show (2 : Nat) ^ 7 = 128 by decide]
  omega

/-- Exact decoding from a known upper bound on the initial decimal width. -/
theorem digitSum_eq_decode_of_width_bound
    (n L : Nat) (hn : 0 < n) (hwidth : decimalLength n ≤ L) :
    digitSum n =
      9 * weightedCount (fun t => outgoingCarryCount (orbit n t))
        (observationBound L) / 2 ^ observationBound L + 1 := by
  apply digitSum_eq_decode_of_numeric_bound n (observationBound L) hn
  have hbound := observationBound_sufficient L
  omega

/-- Every positive seed has a fully numerical finite carry-total decoder. -/
theorem digitSum_eq_decode (n : Nat) (hn : 0 < n) :
    digitSum n =
      9 * weightedCount (fun t => outgoingCarryCount (orbit n t))
        (observationBound (decimalLength n)) /
        2 ^ observationBound (decimalLength n) + 1 :=
  digitSum_eq_decode_of_width_bound n (decimalLength n) hn (Nat.le_refl _)

/-- Equal finite histories of carry totals determine the initial digit sum.
The positive seeds may have different widths below the common upper bound. -/
theorem finite_carryCount_history_determines_digitSum
    (n m L : Nat) (hn : 0 < n) (hm : 0 < m)
    (hnWidth : decimalLength n ≤ L) (hmWidth : decimalLength m ≤ L)
    (hcounts : ∀ t, t < observationBound L →
      outgoingCarryCount (orbit n t) = outgoingCarryCount (orbit m t)) :
    digitSum n = digitSum m := by
  have hw := weightedCount_congr
    (fun t => outgoingCarryCount (orbit n t))
    (fun t => outgoingCarryCount (orbit m t)) (observationBound L) hcounts
  rw [digitSum_eq_decode_of_width_bound n L hn hnWidth,
    digitSum_eq_decode_of_width_bound m L hm hmWidth, hw]

/-- Equality of all outgoing carry totals determines the initial digit sum
without requiring the initial widths to agree. -/
theorem carryCount_history_determines_digitSum
    (n m : Nat) (hn : 0 < n) (hm : 0 < m)
    (hcounts : ∀ t,
      outgoingCarryCount (orbit n t) = outgoingCarryCount (orbit m t)) :
    digitSum n = digitSum m := by
  apply finite_carryCount_history_determines_digitSum n m
    (max (decimalLength n) (decimalLength m)) hn hm
    (Nat.le_max_left _ _) (Nat.le_max_right _ _)
  intro t _
  exact hcounts t

/-- For positive seeds, complete histories of total outgoing carries and
complete histories of digit sums determine each other. -/
theorem carryCount_history_iff_digitSum_history
    (n m : Nat) (hn : 0 < n) (hm : 0 < m) :
    (∀ t, outgoingCarryCount (orbit n t) = outgoingCarryCount (orbit m t)) ↔
      (∀ t, digitSum (orbit n t) = digitSum (orbit m t)) := by
  constructor
  · intro hcounts t
    induction t with
    | zero =>
        simpa only [orbit] using carryCount_history_determines_digitSum n m hn hm hcounts
    | succ t ih =>
        have hleft := outgoingCarryCount_balance (orbit n t)
        have hright := outgoingCarryCount_balance (orbit m t)
        rw [hcounts t, ih] at hleft
        change digitSum (step (orbit n t)) = digitSum (step (orbit m t))
        omega
  · intro hs t
    have hnow := hs t
    have hnext := hs (t + 1)
    change digitSum (step (orbit n t)) = digitSum (step (orbit m t)) at hnext
    unfold outgoingCarryCount
    rw [hnow, hnext]

end CarryCountDecoding

#print axioms CarryCountDecoding.weightedCount_balance
#print axioms CarryCountDecoding.digitSum_eq_decode_of_terminal_bound
#print axioms CarryCountDecoding.digitSum_eq_decode_of_numeric_bound
#print axioms CarryCountDecoding.observationBound_sufficient
#print axioms CarryCountDecoding.digitSum_eq_decode_of_width_bound
#print axioms CarryCountDecoding.digitSum_eq_decode
#print axioms CarryCountDecoding.finite_carryCount_history_determines_digitSum
#print axioms CarryCountDecoding.carryCount_history_determines_digitSum
#print axioms CarryCountDecoding.carryCount_history_iff_digitSum_history
