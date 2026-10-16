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
    (hC : 0 ≤ C) (hR : 0 ≤ R ∧ R ≤ 1) (hτ : 0 ≤ τ ∧ τ ≤ 1)
    (hnext : P + 9 * (C - R) = 0)
    (hrem : 0 ≤ R + P + τ ∧ R + P + τ ≤ 9) :
    P = 0 ∧ C = R := by
  omega

/-- Finite arithmetic core. The terminal boundary is an explicit hypothesis. -/
theorem scaled_finite_zero (L : Nat) (P C R τ : Nat → Int)
    (hend : P L = 0)
    (hC : ∀ i, i < L → 0 ≤ C i)
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
        exact (scaled_local_zero _ _ _ _ (hC _ hi) (hR _ hi) (hτ _ hi)
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
    (hC : ∀ i, i < L → 0 ≤ C i)
    (hR : ∀ i, i < L → 0 ≤ R i ∧ R i ≤ 1)
    (hτ : ∀ i, i < L → 0 ≤ τ i ∧ τ i ≤ 1)
    (hstep : ∀ i, i < L → S (i + 1) = S i + C i - R i)
    (hq : ∀ i, i < L → q i = 10 * C i + R i + 9 * S i)
    (hrem : ∀ i, i < L →
      0 ≤ q i + τ i - 10 * C i ∧ q i + τ i - 10 * C i ≤ 9) :
    (∀ i, i ≤ L → S i = 0) ∧
      (∀ i, i < L → C i = R i ∧ q i = 11 * C i) := by
  have h := scaled_finite_zero L (fun i => 9 * S i) C R τ
    (by change 9 * S L = 0; omega) hC hR hτ
    (by
      intro i hi
      change 9 * S (i + 1) = 9 * S i + 9 * (C i - R i)
      have hs := hstep i hi
      omega)
    (by
      intro i hi
      change 0 ≤ R i + 9 * S i + τ i ∧ R i + 9 * S i + τ i ≤ 9
      have heq := hq i hi
      have hr := hrem i hi
      omega)
  refine ⟨?_, ?_⟩
  · intro i hi
    have hz := h.1 i hi
    change 9 * S i = 0 at hz
    omega
  · intro i hi
    have hz := h.1 i (by omega)
    change 9 * S i = 0 at hz
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
  have hz := scaled_finite_zero L P C R τ hend (fun i hi => (hC i hi).1) hR hτ hstep hlocal
  intro i hi
  have hp := hz.1 i (by omega)
  have hc := hz.2 i hi
  have hpdef : P i = q i - 10 * C i - R i := by
    simp only [P, supported_lt q L i hi, supported_lt C L i hi]
  have hrdef : R i = C (L - 1 - i) := reverseCarry_lt C L i hi
  constructor <;> omega

/-- A preceding outgoing carry, with zero before the first column. -/
def prevNat (C : Nat → Nat) : Nat → Nat
  | 0 => 0
  | i + 1 => C i

/-- A true boundary bit resets the isolated block's incoming carry to zero. -/
def incoming (cut : Nat → Bool) (C : Nat → Nat) (i : Nat) : Nat :=
  if cut i then 0 else prevNat C i

/-- The actual outgoing carries obtained by normalizing each block separately.
The boundary bit at zero is immaterial because its preceding carry is zero. -/
def resetOut (q : Nat → Nat) (cut : Nat → Bool) : Nat → Nat
  | 0 => q 0 / 10
  | i + 1 => (q (i + 1) + if cut (i + 1) then 0 else resetOut q cut i) / 10

def resetDigit (q : Nat → Nat) (cut : Nat → Bool) (i : Nat) : Nat :=
  (q i + incoming cut (resetOut q cut) i) % 10

/-- The raw placed sum includes the preceding block's terminal carry at a cut. -/
def rawCoeff (q : Nat → Nat) (cut : Nat → Bool) (i : Nat) : Nat :=
  resetDigit q cut i + (prevNat (resetOut q cut) i - incoming cut (resetOut q cut) i)

/-- Raw finite coefficient polynomial for the explicitly computed block carries. -/
def resetRaw (q : Nat → Nat) (cut : Nat → Bool) (L i : Nat) : Int :=
  raw (fun j => (q j : Int)) (fun j => (resetOut q cut j : Int)) L i

theorem incoming_le_previous (cut : Nat → Bool) (C : Nat → Nat) (i : Nat) :
    incoming cut C i ≤ prevNat C i := by
  simp only [incoming]
  split <;> omega

theorem resetOut_equation (q : Nat → Nat) (cut : Nat → Bool) (i : Nat) :
    resetOut q cut i = (q i + incoming cut (resetOut q cut) i) / 10 := by
  cases i with
  | zero => simp [resetOut, incoming, prevNat]
  | succ i => rfl

theorem reset_column_equation (q : Nat → Nat) (cut : Nat → Bool) (i : Nat) :
    resetDigit q cut i + 10 * resetOut q cut i = q i + incoming cut (resetOut q cut) i := by
  rw [resetOut_equation]
  exact Nat.mod_add_div _ _

theorem resetOut_bounded (q : Nat → Nat) (cut : Nat → Bool) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) :
    ∀ i, i < L → resetOut q cut i ≤ 1 := by
  intro i
  induction i with
  | zero =>
      intro hi
      have hb := hq 0 hi
      simp only [resetOut]
      omega
  | succ i ih =>
      intro hi
      have hb := hq (i + 1) hi
      have hp := ih (by omega)
      have ht := incoming_le_previous cut (resetOut q cut) (i + 1)
      simp only [prevNat] at ht
      rw [resetOut_equation]
      omega

theorem previous_bounded (q : Nat → Nat) (cut : Nat → Bool) (L i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18) (hi : i ≤ L) :
    prevNat (resetOut q cut) i ≤ 1 := by
  cases i with
  | zero => simp [prevNat]
  | succ i => exact resetOut_bounded q cut L hq i (by omega)

theorem incoming_bounded (q : Nat → Nat) (cut : Nat → Bool) (L i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18) (hi : i ≤ L) :
    incoming cut (resetOut q cut) i ≤ 1 :=
  Nat.le_trans (incoming_le_previous cut _ i) (previous_bounded q cut L i hq hi)

theorem resetDigit_bounded (q : Nat → Nat) (cut : Nat → Bool) (i : Nat) :
    resetDigit q cut i ≤ 9 := by
  simp only [resetDigit]
  omega

theorem raw_column_equation (q : Nat → Nat) (cut : Nat → Bool) (i : Nat) :
    rawCoeff q cut i + 10 * resetOut q cut i = q i + prevNat (resetOut q cut) i := by
  have he := reset_column_equation q cut i
  have ht := incoming_le_previous cut (resetOut q cut) i
  simp only [rawCoeff]
  omega

theorem rawCoeff_bounded (q : Nat → Nat) (cut : Nat → Bool) (L i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18) (hi : i < L) :
    rawCoeff q cut i ≤ 10 := by
  have hd := resetDigit_bounded q cut i
  have hp := previous_bounded q cut L i hq (by omega)
  simp only [rawCoeff]
  omega

theorem resetOut_le_actual (q : Nat → Nat) (cut : Nat → Bool) (i : Nat) :
    resetOut q cut i ≤ carry q (i + 1) := by
  induction i with
  | zero => simp [resetOut, carry]
  | succ i ih =>
      have ht := incoming_le_previous cut (resetOut q cut) (i + 1)
      simp only [prevNat] at ht
      rw [resetOut_equation]
      simp only [carry]
      change resetOut q cut i ≤ (q i + carry q i) / 10 at ih
      omega

theorem previous_le_actual (q : Nat → Nat) (cut : Nat → Bool) (i : Nat) :
    prevNat (resetOut q cut) i ≤ carry q i := by
  cases i with
  | zero => simp [prevNat, carry]
  | succ i => exact resetOut_le_actual q cut i

theorem raw_value (q : Nat → Nat) (cut : Nat → Bool) (L : Nat) :
    value (rawCoeff q cut) L + prevNat (resetOut q cut) L * 10 ^ L = value q L := by
  induction L with
  | zero => simp [value, prevNat]
  | succ L ih =>
      have he := congrArg (fun x => x * 10 ^ L) (raw_column_equation q cut L)
      simp only [Nat.add_mul] at he
      simp only [value, prevNat, Nat.pow_succ]
      have hc : resetOut q cut L * (10 ^ L * 10) =
          10 * resetOut q cut L * 10 ^ L := by
        simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
      rw [hc]
      omega

theorem previous_supported (f : Nat → Int) (L i : Nat) (hi : i ≤ L) :
    previous (supported f L) i = previous f i := by
  cases i with
  | zero => rfl
  | succ i => simp only [previous, supported_lt f L i (by omega)]

theorem previous_cast (C : Nat → Nat) (i : Nat) :
    previous (fun j => (C j : Int)) i = (prevNat C i : Int) := by
  cases i <;> rfl

theorem resetRaw_lt (q : Nat → Nat) (cut : Nat → Bool) (L i : Nat)
    (hi : i < L) : resetRaw q cut L i = (rawCoeff q cut i : Int) := by
  have he := raw_column_equation q cut i
  simp only [resetRaw, raw, supported_lt _ L i hi,
    previous_supported _ L i (by omega), previous_cast]
  omega

theorem resetRaw_terminal (q : Nat → Nat) (cut : Nat → Bool) (L : Nat) :
    resetRaw q cut L L = (prevNat (resetOut q cut) L : Int) := by
  simp only [resetRaw, raw, previous_supported _ L L (by omega), previous_cast]
  simp [supported]

/-- Overflow-width raw symmetry forces the actual input coefficients to be 0/11. -/
theorem reset_overflow_rigidity (q : Nat → Nat) (cut : Nat → Bool) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18)
    (hq : ∀ i, i < L → q i = q (L - 1 - i))
    (hsym : ∀ i, i ≤ L → resetRaw q cut L i = resetRaw q cut L (L - i)) :
    ∀ i, i < L → q i = 11 * resetOut q cut i ∧ (q i = 0 ∨ q i = 11) := by
  have h := raw_overflow_rigidity L (fun i => (q i : Int))
    (fun i => (resetOut q cut i : Int))
    (fun i => (incoming cut (resetOut q cut) i : Int))
    (by
      intro i hi
      dsimp only
      have hc := resetOut_bounded q cut L hb i hi
      constructor <;> omega)
    (by
      intro i hi
      dsimp only
      have ht := incoming_bounded q cut L i hb (by omega)
      constructor <;> omega)
    (by intro i hi; dsimp only; rw [hq i hi])
    (by
      intro i hi
      dsimp only
      have he := reset_column_equation q cut i
      have hd := resetDigit_bounded q cut i
      constructor <;> omega)
    hsym
  intro i hi
  have he := (h i hi).2
  dsimp only at he
  have hc := resetOut_bounded q cut L hb i hi
  constructor
  · omega
  · have hcases : resetOut q cut i = 0 ∨ resetOut q cut i = 1 := by omega
    rcases hcases with hz | ho
    · left; omega
    · right; omega

/-- No-overflow raw symmetry forces every isolated carry to vanish. -/
theorem reset_no_overflow_rigidity (q : Nat → Nat) (cut : Nat → Bool) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18)
    (hq : ∀ i, i < L → q i = q (L - 1 - i))
    (hc : carry q L = 0)
    (hsym : ∀ i, i < L → resetRaw q cut L i = resetRaw q cut L (L - 1 - i)) :
    ∀ i, i < L → resetOut q cut i = 0 ∧ q i ≤ 9 := by
  have hterm : prevNat (resetOut q cut) L = 0 := by
    have he := previous_le_actual q cut L
    omega
  have hv : value q L = value (rawCoeff q cut) L := by
    have he := raw_value q cut L
    rw [hterm] at he
    omega
  have heq := ReverseAddInverse.symmetric_value_injective q (rawCoeff q cut) L hb
    (by intro i hi; have he := rawCoeff_bounded q cut L i hb hi; omega) hq
    (by
      intro i hi
      have he := hsym i hi
      rw [resetRaw_lt q cut L i hi, resetRaw_lt q cut L _ (by omega)] at he
      omega) hv
  intro i hi
  have hcol := raw_column_equation q cut i
  have he := heq i hi
  have hp := previous_bounded q cut L i hb (by omega)
  have hz : resetOut q cut i = 0 := by omega
  refine ⟨hz, ?_⟩
  have hloc := reset_column_equation q cut i
  have hd := resetDigit_bounded q cut i
  omega

end RawSymmetryObstruction
