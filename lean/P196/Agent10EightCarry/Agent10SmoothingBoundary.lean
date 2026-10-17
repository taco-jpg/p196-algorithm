import Std

/-!
Agent #10, 2026-10-16. Sharp coefficient threshold for fourfold binomial
smoothing of zero-extended integer sequences. This is a supporting algebraic
result, not an assertion of actual eight-carry ambiguity or Lychrel existence.

The intended connection is to DifferenceObservability.smoothPow 4. This module
is self-contained: `four` spells out the coefficients of (1 + X)^4. The separate
bridge file identifies it with the repository operator without changing either
operator's boundary convention.
-/
set_option maxHeartbeats 10000000
namespace Agent10SmoothingBoundary

abbrev Series := Nat → Int

def lag (f : Series) (k i : Nat) : Int :=
  if k ≤ i then f (i - k) else 0

def four (f : Series) (i : Nat) : Int :=
  f i + 4 * lag f 1 i + 6 * lag f 2 i + 4 * lag f 3 i + lag f 4 i

/-- Seven leading coefficient inequalities force the leading input to vanish.
All arithmetic is linear over integers. No solver certificate is assumed. -/
theorem prefix_rigidity
    (a0 a1 a2 a3 a4 a5 a6 : Int)
    (b1 : -5 ≤ a1 ∧ a1 ≤ 5)
    (b2 : -5 ≤ a2 ∧ a2 ≤ 5)
    (b3 : -5 ≤ a3 ∧ a3 ≤ 5)
    (b4 : -5 ≤ a4 ∧ a4 ≤ 5)
    (b5 : -5 ≤ a5 ∧ a5 ≤ 5)
    (b6 : -5 ≤ a6 ∧ a6 ≤ 5)
    (h0 : -1 ≤ a0 ∧ a0 ≤ 1)
    (h1 : -1 ≤ a1 + 4*a0 ∧ a1 + 4*a0 ≤ 1)
    (h2 : -1 ≤ a2 + 4*a1 + 6*a0 ∧ a2 + 4*a1 + 6*a0 ≤ 1)
    (h3 : -1 ≤ a3 + 4*a2 + 6*a1 + 4*a0 ∧
                a3 + 4*a2 + 6*a1 + 4*a0 ≤ 1)
    (h4 : -1 ≤ a4 + 4*a3 + 6*a2 + 4*a1 + a0 ∧
                a4 + 4*a3 + 6*a2 + 4*a1 + a0 ≤ 1)
    (h5 : -1 ≤ a5 + 4*a4 + 6*a3 + 4*a2 + a1 ∧
                a5 + 4*a4 + 6*a3 + 4*a2 + a1 ≤ 1)
    (h6 : -1 ≤ a6 + 4*a5 + 6*a4 + 4*a3 + a2 ∧
                a6 + 4*a5 + 6*a4 + 4*a3 + a2 ≤ 1) : a0 = 0 := by
  omega

private theorem lag_shift (f : Series) (m j k : Nat)
    (hz : ∀ i, i < m → f i = 0) :
    lag (fun i => f (m+i)) k j = lag f k (m+j) := by
  unfold lag
  by_cases h : k ≤ j
  · have hh : k ≤ m+j := by omega
    have he : m+j-k = m+(j-k) := by omega
    simp [h, hh, he]
  · by_cases hh : k ≤ m+j
    · have he : m+j-k < m := by omega
      simp [h, hh, hz _ he]
    · simp [h, hh]

private theorem four_shift (f : Series) (m j : Nat)
    (hz : ∀ i, i < m → f i = 0) :
    four (fun i => f (m+i)) j = four f (m+j) := by
  simp only [four, lag_shift f m j 1 hz, lag_shift f m j 2 hz,
    lag_shift f m j 3 hz, lag_shift f m j 4 hz]

/-- Width-free and support-free rigidity, at the sharp integer coefficient
bound five. The corresponding statement at bound six is false below. -/
theorem four_rigidity_at_five (f : Series)
    (hf : ∀ i, -5 ≤ f i ∧ f i ≤ 5)
    (hg : ∀ i, -1 ≤ four f i ∧ four f i ≤ 1) :
    ∀ i, f i = 0 := by
  intro m
  induction m using Nat.strongRecOn with
  | ind m ih =>
    have hs (j : Nat) : -1 ≤ four (fun i => f (m+i)) j ∧
        four (fun i => f (m+i)) j ≤ 1 := by
      rw [four_shift f m j ih]
      exact hg (m+j)
    have h0 := hs 0
    have h1 := hs 1
    have h2 := hs 2
    have h3 := hs 3
    have h4 := hs 4
    have h5 := hs 5
    have h6 := hs 6
    simp [four, lag] at h0 h1 h2 h3 h4 h5 h6
    exact prefix_rigidity (f m) (f (m+1)) (f (m+2)) (f (m+3))
      (f (m+4)) (f (m+5)) (f (m+6))
      (hf (m+1)) (hf (m+2)) (hf (m+3)) (hf (m+4))
      (hf (m+5)) (hf (m+6)) h0 h1 h2 h3 h4 h5 h6

/-- A palindromic, finitely supported witness. -/
def witness : Series
  | 0 => 1
  | 1 => -3
  | 2 => 5
  | 3 => -6
  | 4 => 6
  | 5 => -6
  | 6 => 6
  | 7 => -6
  | 8 => 5
  | 9 => -3
  | 10 => 1
  | _ => 0

theorem witness_zero_after (i : Nat) (hi : 11 ≤ i) : witness i = 0 := by
  have he : i = (i-11)+11 := by omega
  rw [he]
  simp [witness]

theorem witness_symmetric : ∀ i : Fin 11,
    witness i.val = witness (10-i.val) := by decide

theorem witness_bounds (i : Nat) : -6 ≤ witness i ∧ witness i ≤ 6 := by
  have small : ∀ j : Fin 11, -6 ≤ witness j.val ∧ witness j.val ≤ 6 := by decide
  by_cases h : i < 11
  · exact small ⟨i,h⟩
  · rw [witness_zero_after i (by omega)]
    omega

theorem four_witness_zero_after (i : Nat) (hi : 15 ≤ i) :
    four witness i = 0 := by
  have h1 : 1 ≤ i := by omega
  have h2 : 2 ≤ i := by omega
  have h3 : 3 ≤ i := by omega
  have h4 : 4 ≤ i := by omega
  simp only [four, lag, if_pos h1, if_pos h2, if_pos h3, if_pos h4]
  rw [witness_zero_after i (by omega),
    witness_zero_after (i-1) (by omega), witness_zero_after (i-2) (by omega),
    witness_zero_after (i-3) (by omega), witness_zero_after (i-4) (by omega)]
  decide

theorem four_witness_bounds (i : Nat) :
    -1 ≤ four witness i ∧ four witness i ≤ 1 := by
  have small : ∀ j : Fin 15,
      -1 ≤ four witness j.val ∧ four witness j.val ≤ 1 := by decide
  by_cases h : i < 15
  · exact small ⟨i,h⟩
  · rw [four_witness_zero_after i (by omega)]
    omega

theorem six_is_not_rigid :
    ∃ f : Series, (∀ i, -6 ≤ f i ∧ f i ≤ 6) ∧
      (∀ i, -1 ≤ four f i ∧ four f i ≤ 1) ∧ f 0 ≠ 0 := by
  exact ⟨witness, witness_bounds, four_witness_bounds, by decide⟩

theorem sharp_threshold :
    (∀ f : Series, (∀ i, -5 ≤ f i ∧ f i ≤ 5) →
      (∀ i, -1 ≤ four f i ∧ four f i ≤ 1) → ∀ i, f i = 0) ∧
    (∃ f : Series, (∀ i, -6 ≤ f i ∧ f i ≤ 6) ∧
      (∀ i, -1 ≤ four f i ∧ four f i ≤ 1) ∧ f 0 ≠ 0) := by
  exact ⟨four_rigidity_at_five, six_is_not_rigid⟩

#print axioms lag_shift
#print axioms four_shift
#print axioms witness_zero_after
#print axioms four_witness_zero_after
#print axioms prefix_rigidity
#print axioms four_rigidity_at_five
#print axioms witness_symmetric
#print axioms witness_bounds
#print axioms four_witness_bounds
#print axioms six_is_not_rigid
#print axioms sharp_threshold
end Agent10SmoothingBoundary
