import IncomingCarrySensitivity

/-!
Rigidity of a symmetric raw sum of separately normalized blocks.
The auxiliary finite arithmetic argument is distinguished from the actual
reset-carry construction below.  Integer coefficients retain every raw
terminal-carry contribution without truncation.
-/

namespace RawSymmetryObstruction

open DecimalDigits

/-- One backward step of the scaled seam-state obstruction. -/
theorem scaled_local_zero (P C R τ : Int)
    (hR : 0 ≤ R ∧ R ≤ 1) (hτ : 0 ≤ τ ∧ τ ≤ 1)
    (hnext : P + 9 * (C - R) = 0)
    (hrem : 0 ≤ R + P + τ ∧ R + P + τ ≤ 9) :
    P = 0 ∧ C = R := by
  omega

/-- Finite arithmetic core. The terminal boundary is an explicit hypothesis. -/
theorem scaled_finite_zero (L : Nat) (P C R τ : Nat → Int)
    (hend : P L = 0)
    (hR : ∀ i, i < L → 0 ≤ R i ∧ R i ≤ 1)
    (hτ : ∀ i, i < L → 0 ≤ τ i ∧ τ i ≤ 1)
    (hstep : ∀ i, i < L → P (i + 1) = P i + 9 * (C i - R i))
    (hrem : ∀ i, i < L → 0 ≤ R i + P i + τ i ∧ R i + P i + τ i ≤ 9) :
    (∀ i, i ≤ L → P i = 0) ∧ (∀ i, i < L → C i = R i) := by
  have hback : ∀ k, k ≤ L → P (L - k) = 0 := by
    intro k
    induction k with
    | zero => intro _; simpa only [Nat.sub_zero] using hend
    | succ k ih =>
        intro hk
        have hi : L - (k + 1) < L := by omega
        have hp := ih (by omega)
        have hs := hstep (L - (k + 1)) hi
        have hind : L - (k + 1) + 1 = L - k := by omega
        rw [hind, hp] at hs
        exact (scaled_local_zero _ _ _ _ (hR _ hi) (hτ _ hi)
          hs.symm (hrem _ hi)).1
  have hz : ∀ i, i ≤ L → P i = 0 := by
    intro i hi
    have h := hback (L - i) (by omega)
    have hind : L - (L - i) = i := by omega
    simpa only [hind] using h
  refine ⟨hz, ?_⟩
  intro i hi
  have hs := hstep i hi
  rw [hz i (by omega), hz (i + 1) (by omega)] at hs
  omega

/-- The unscaled core in the notation used by the written seam argument. -/
theorem finite_state_rigidity (L : Nat) (S C R τ q : Nat → Int)
    (hend : S L = 0)
    (hR : ∀ i, i < L → 0 ≤ R i ∧ R i ≤ 1)
    (hτ : ∀ i, i < L → 0 ≤ τ i ∧ τ i ≤ 1)
    (hstep : ∀ i, i < L → S (i + 1) = S i + C i - R i)
    (hq : ∀ i, i < L → q i = 10 * C i + R i + 9 * S i)
    (hrem : ∀ i, i < L →
      0 ≤ q i + τ i - 10 * C i ∧ q i + τ i - 10 * C i ≤ 9) :
    (∀ i, i ≤ L → S i = 0) ∧
      (∀ i, i < L → C i = R i ∧ q i = 11 * C i) := by
  have h := scaled_finite_zero L (fun i => 9 * S i) C R τ
    (by rw [hend]; decide) hR hτ
    (by intro i hi; have hs := hstep i hi; omega)
    (by intro i hi; have heq := hq i hi; have hr := hrem i hi; omega)
  refine ⟨?_, ?_⟩
  · intro i hi
    have hz := h.1 i hi
    omega
  · intro i hi
    have hz := h.1 i (by omega)
    have hc := h.2 i hi
    have heq := hq i hi
    constructor <;> omega

/-- Zero extension of a finite coefficient word. -/
def supported (f : Nat → Int) (L i : Nat) : Int := if i < L then f i else 0

/-- Previous coefficient, with zero outside the left boundary. -/
def previous (f : Nat → Int) : Nat → Int
  | 0 => 0
  | i + 1 => f i

/-- Reversed finite carry word, zero at and after the terminal boundary. -/
def reverseCarry (C : Nat → Int) (L i : Nat) : Int :=
  if i < L then C (L - 1 - i) else 0

/-- Raw separately normalized coefficient sum: q + (x-10)C. -/
def raw (q C : Nat → Int) (L i : Nat) : Int :=
  supported q L i + previous (supported C L) i - 10 * supported C L i

theorem supported_lt (f : Nat → Int) (L i : Nat) (hi : i < L) :
    supported f L i = f i := by simp only [supported, if_pos hi]

theorem reverseCarry_lt (C : Nat → Int) (L i : Nat) (hi : i < L) :
    reverseCarry C L i = C (L - 1 - i) := by
  simp only [reverseCarry, if_pos hi]

theorem previous_reverse (C : Nat → Int) (L i : Nat) (hi : i < L) :
    previous (supported C L) (L - 1 - i) = reverseCarry C L (i + 1) := by
  by_cases h : i + 1 < L
  · have hj : L - 1 - i = (L - 2 - i) + 1 := by omega
    have hk : L - 2 - i < L := by omega
    have heq : L - 1 - (i + 1) = L - 2 - i := by omega
    simp only [hj, previous, supported_lt C L _ hk, reverseCarry, if_pos h, heq]
  · have hj : L - 1 - i = 0 := by omega
    simp only [hj, previous, reverseCarry, if_neg h]

/-- The full overflow-width raw palindrome equations derive the state
recurrence and its terminal boundary; neither is an assumed sum identity. -/
theorem raw_overflow_rigidity (L : Nat) (q C τ : Nat → Int)
    (hC : ∀ i, i < L → 0 ≤ C i ∧ C i ≤ 1)
    (hτ : ∀ i, i < L → 0 ≤ τ i ∧ τ i ≤ 1)
    (hq : ∀ i, i < L → q i = q (L - 1 - i))
    (hrem : ∀ i, i < L →
      0 ≤ q i + τ i - 10 * C i ∧ q i + τ i - 10 * C i ≤ 9)
    (hsym : ∀ i, i ≤ L → raw q C L i = raw q C L (L - i)) :
    ∀ i, i < L → C i = C (L - 1 - i) ∧ q i = 11 * C i := by
  let R := reverseCarry C L
  let P := fun i => supported q L i - 10 * supported C L i - R i
  have hend : P L = 0 := by simp [P, R, reverseCarry, supported]
  have hR : ∀ i, i < L → 0 ≤ R i ∧ R i ≤ 1 := by
    intro i hi
    change 0 ≤ reverseCarry C L i ∧ reverseCarry C L i ≤ 1
    rw [reverseCarry_lt C L i hi]
    exact hC (L - 1 - i) (by omega)
  have hstep : ∀ i, i < L → P (i + 1) = P i + 9 * (C i - R i) := by
    intro i hi
    have hj : L - 1 - i < L := by omega
    have hind : L - (i + 1) = L - 1 - i := by omega
    have he := hsym (i + 1) (by omega)
    rw [hind] at he
    have hl : raw q C L (i + 1) =
        supported q L (i + 1) + C i - 10 * supported C L (i + 1) := by
      simp only [raw, previous, supported_lt C L i hi]
    have hr : raw q C L (L - 1 - i) = q i + R (i + 1) - 10 * R i := by
      rw [raw, previous_reverse C L i hi, supported_lt q L _ hj,
        supported_lt C L _ hj, ← hq i hi]
      simp only [R, reverseCarry_lt C L i hi]
    rw [hl, hr] at he
    have hp : P i = q i - 10 * C i - R i := by
      simp only [P, supported_lt q L i hi, supported_lt C L i hi]
    have hn : P (i + 1) = supported q L (i + 1) -
        10 * supported C L (i + 1) - R (i + 1) := rfl
    omega
  have hlocal : ∀ i, i < L → 0 ≤ R i + P i + τ i ∧ R i + P i + τ i ≤ 9 := by
    intro i hi
    have hp : P i = q i - 10 * C i - R i := by
      simp only [P, supported_lt q L i hi, supported_lt C L i hi]
    have hr := hrem i hi
    omega
  have hz := scaled_finite_zero L P C R τ hend hR hτ hstep hlocal
  intro i hi
  have hp := hz.1 i (by omega)
  have hc := hz.2 i hi
  have hpdef : P i = q i - 10 * C i - R i := by
    simp only [P, supported_lt q L i hi, supported_lt C L i hi]
  have hrdef : R i = C (L - 1 - i) := reverseCarry_lt C L i hi
  constructor <;> omega

end RawSymmetryObstruction
