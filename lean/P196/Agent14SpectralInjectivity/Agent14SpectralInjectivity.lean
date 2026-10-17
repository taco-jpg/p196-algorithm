import P196.Agent14SpectralInjectivity.Agent14SpectralWeights

/-!
Exact finite-width injectivity of the integer spectral coordinate from
creative_global_spectral_notes.md. The recurrence weights are used literally.
This module concerns bounded symmetric coefficient words, not the individual
decimal digits realizing such a word or a real square-root interpretation.
-/

namespace Agent14.Spectral

/-- Equality of finite sums uses only the specified finite indices. -/
theorem prefixSum_congr (f g : Nat → Nat) (n : Nat)
    (h : ∀ i, i < n → f i = g i) : prefixSum f n = prefixSum g n := by
  induction n with
  | zero => rfl
  | succ n ih =>
      simp only [prefixSum]
      rw [ih (fun i hi => h i (by omega)), h n (by omega)]

/-- Separate the first term while shifting all remaining indices. -/
theorem prefixSum_shift (f : Nat → Nat) (n : Nat) :
    prefixSum f (n + 1) = f 0 + prefixSum (fun i => f (i + 1)) n := by
  induction n with
  | zero => simp [prefixSum]
  | succ n ih =>
      simp only [prefixSum] at ih ⊢
      omega

/-- Evaluate a finite low-to-center half word with decreasing weights. -/
def descendingScore (w q : Nat → Nat) (n : Nat) : Nat :=
  prefixSum (fun i => q i * w (n - 1 - i)) n

theorem descendingScore_zero (w q : Nat → Nat) :
    descendingScore w q 0 = 0 := rfl

theorem descendingScore_succ (w q : Nat → Nat) (n : Nat) :
    descendingScore w q (n + 1) =
      q 0 * w n + descendingScore w (fun i => q (i + 1)) n := by
  unfold descendingScore
  rw [prefixSum_shift]
  simp only [Nat.add_sub_cancel, Nat.sub_zero]
  congr 1
  apply prefixSum_congr
  intro i hi
  congr 2
  omega

/-- A bound for all words in the original coefficient alphabet 0..18. -/
theorem descendingScore_le (w q : Nat → Nat) (n : Nat)
    (hq : ∀ i, i < n → q i ≤ 18) :
    descendingScore w q n ≤ 18 * prefixSum w n := by
  induction n generalizing q with
  | zero => simp [descendingScore, prefixSum]
  | succ n ih =>
      rw [descendingScore_succ, prefixSum, Nat.mul_add]
      have hb := ih (fun i => q (i + 1)) (fun i hi => hq (i + 1) (by omega))
      have hzero := Nat.mul_le_mul_right (w n) (hq 0 (by omega))
      omega

/-- A largest differing coefficient cannot be cancelled by all lower weights. -/
theorem descendingScore_injective (w : Nat → Nat)
    (hdom : ∀ k, 18 * prefixSum w k < w k)
    (q r : Nat → Nat) (n : Nat)
    (hq : ∀ i, i < n → q i ≤ 18)
    (hr : ∀ i, i < n → r i ≤ 18)
    (heq : descendingScore w q n = descendingScore w r n) :
    ∀ i, i < n → q i = r i := by
  induction n generalizing q r with
  | zero => intro i hi; omega
  | succ n ih =>
      have hqt : ∀ i, i < n → q (i + 1) ≤ 18 :=
        fun i hi => hq (i + 1) (by omega)
      have hrt : ∀ i, i < n → r (i + 1) ≤ 18 :=
        fun i hi => hr (i + 1) (by omega)
      have hqb := Nat.lt_of_le_of_lt (descendingScore_le w (fun i => q (i + 1)) n hqt) (hdom n)
      have hrb := Nat.lt_of_le_of_lt (descendingScore_le w (fun i => r (i + 1)) n hrt) (hdom n)
      rw [descendingScore_succ, descendingScore_succ] at heq
      have hzero : q 0 = r 0 := by
        by_cases hsame : q 0 = r 0
        · exact hsame
        have hcases : q 0 < r 0 ∨ r 0 < q 0 := by omega
        rcases hcases with hlt | hgt
        · have hm := Nat.mul_le_mul_right (w n) (Nat.succ_le_of_lt hlt)
          simp only [Nat.succ_mul] at hm
          omega
        · have hm := Nat.mul_le_mul_right (w n) (Nat.succ_le_of_lt hgt)
          simp only [Nat.succ_mul] at hm
          omega
      have htail : descendingScore w (fun i => q (i + 1)) n =
          descendingScore w (fun i => r (i + 1)) n := by
        rw [hzero] at heq
        omega
      intro i hi
      cases i with
      | zero => exact hzero
      | succ i => exact ih _ _ hqt hrt htail i (by omega)

/-- The source's exact even-width formula, including its empty-width extension. -/
def evenCoordinate (q : Nat → Nat) (m : Nat) : Nat :=
  prefixSum (fun i => q i * R (m - 1 - i)) m

/-- The source's exact odd-width formula. The center has weight one, not T(0). -/
def oddCoordinate (q : Nat → Nat) (m : Nat) : Nat :=
  q m + prefixSum (fun i => q i * T (m - i)) m

theorem evenCoordinate_eq_descending (q : Nat → Nat) (m : Nat) :
    evenCoordinate q m = descendingScore R q m := rfl

theorem oddCoordinate_eq_descending (q : Nat → Nat) (m : Nat) :
    oddCoordinate q m = descendingScore oddWeight q (m + 1) := by
  unfold oddCoordinate descendingScore
  rw [prefixSum]
  simp only [Nat.add_sub_cancel, Nat.sub_self]
  have hc : prefixSum (fun i => q i * oddWeight (m - i)) m =
      prefixSum (fun i => q i * T (m - i)) m := by
    apply prefixSum_congr
    intro i hi
    have hpos : m - i ≠ 0 := by omega
    simp [oddWeight, hpos]
  rw [hc]
  simp [oddWeight, Nat.add_comm]

theorem even_coordinate_half_injective (q r : Nat → Nat) (m : Nat)
    (hq : ∀ i, i < m → q i ≤ 18)
    (hr : ∀ i, i < m → r i ≤ 18)
    (heq : evenCoordinate q m = evenCoordinate r m) :
    ∀ i, i < m → q i = r i := by
  exact descendingScore_injective R R_dominates q r m hq hr heq

theorem odd_coordinate_half_injective (q r : Nat → Nat) (m : Nat)
    (hq : ∀ i, i < m + 1 → q i ≤ 18)
    (hr : ∀ i, i < m + 1 → r i ≤ 18)
    (heq : oddCoordinate q m = oddCoordinate r m) :
    ∀ i, i < m + 1 → q i = r i := by
  rw [oddCoordinate_eq_descending, oddCoordinate_eq_descending] at heq
  exact descendingScore_injective oddWeight oddWeight_dominates q r (m + 1) hq hr heq

/-- Even-width reciprocal words are recovered on all valid indices. -/
theorem even_coordinate_injective (q r : Nat → Nat) (m : Nat)
    (hq : ∀ i, i < 2 * m → q i ≤ 18)
    (hr : ∀ i, i < 2 * m → r i ≤ 18)
    (hqs : ∀ i, i < 2 * m → q i = q (2 * m - 1 - i))
    (hrs : ∀ i, i < 2 * m → r i = r (2 * m - 1 - i))
    (heq : evenCoordinate q m = evenCoordinate r m) :
    ∀ i, i < 2 * m → q i = r i := by
  have hh := even_coordinate_half_injective q r m
    (fun i hi => hq i (by omega)) (fun i hi => hr i (by omega)) heq
  intro i hi
  by_cases hlo : i < m
  · exact hh i hlo
  · rw [hqs i hi, hrs i hi]
    exact hh (2 * m - 1 - i) (by omega)

/-- Odd-width reciprocal words are recovered without imposing even center parity. -/
theorem odd_coordinate_injective (q r : Nat → Nat) (m : Nat)
    (hq : ∀ i, i < 2 * m + 1 → q i ≤ 18)
    (hr : ∀ i, i < 2 * m + 1 → r i ≤ 18)
    (hqs : ∀ i, i < 2 * m + 1 → q i = q (2 * m + 1 - 1 - i))
    (hrs : ∀ i, i < 2 * m + 1 → r i = r (2 * m + 1 - 1 - i))
    (heq : oddCoordinate q m = oddCoordinate r m) :
    ∀ i, i < 2 * m + 1 → q i = r i := by
  have hh := odd_coordinate_half_injective q r m
    (fun i hi => hq i (by omega)) (fun i hi => hr i (by omega)) heq
  intro i hi
  by_cases hlo : i < m + 1
  · exact hh i hlo
  · rw [hqs i hi, hrs i hi]
    exact hh (2 * m + 1 - 1 - i) (by omega)

/-- Parity selection agrees with the original Python coordinate function. -/
def coordinate (q : Nat → Nat) (L : Nat) : Nat :=
  if L % 2 = 0 then evenCoordinate q (L / 2) else oddCoordinate q (L / 2)

/-- Complete fixed-width source claim for every bounded reciprocal word. -/
theorem coordinate_injective (q r : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hr : ∀ i, i < L → r i ≤ 18)
    (hqs : ∀ i, i < L → q i = q (L - 1 - i))
    (hrs : ∀ i, i < L → r i = r (L - 1 - i))
    (heq : coordinate q L = coordinate r L) :
    ∀ i, i < L → q i = r i := by
  by_cases hp : L % 2 = 0
  · have hL : L = 2 * (L / 2) := by omega
    have he : evenCoordinate q (L / 2) = evenCoordinate r (L / 2) := by
      simpa [coordinate, hp] using heq
    have h := even_coordinate_injective q r (L / 2)
      (fun i hi => hq i (by omega)) (fun i hi => hr i (by omega))
      (by simpa only [← hL] using hqs) (by simpa only [← hL] using hrs) he
    intro i hi
    exact h i (by omega)
  · have hL : L = 2 * (L / 2) + 1 := by omega
    have he : oddCoordinate q (L / 2) = oddCoordinate r (L / 2) := by
      simpa [coordinate, hp] using heq
    have h := odd_coordinate_injective q r (L / 2)
      (fun i hi => hq i (by omega)) (fun i hi => hr i (by omega))
      (by simpa only [← hL] using hqs) (by simpa only [← hL] using hrs) he
    intro i hi
    exact h i (by omega)

theorem coordinate_zero (q : Nat → Nat) : coordinate q 0 = 0 := rfl
theorem coordinate_one (q : Nat → Nat) : coordinate q 1 = q 0 := by
  simp [coordinate, oddCoordinate, prefixSum]
theorem coordinate_two (q : Nat → Nat) : coordinate q 2 = q 0 := by
  simp [coordinate, evenCoordinate, prefixSum, R]

end Agent14.Spectral
