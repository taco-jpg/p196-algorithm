import DelayedOverlapGate

/-!
Agent #12. Concrete all-parameter carry certificates for the source (1,6)
family, including the zero-length boundary at r=5. This module verifies the carry and
width profiles and a generic normalization formula. The proposed q-word
sequence still needs its next-pair identities and ordinary first-hit endpoint
in a separate module; those conclusions are not asserted here.
Source: renewal_pass/tails/STATUS.md and symbolic_tail_certificates.json.
-/
namespace P196.Agent12.FirstHitEleven

set_option maxHeartbeats 16000000
set_option maxRecDepth 4096

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization
  CarryHistory DelayedOverlapGate DecimalDelayBridge

def width (k t : Nat) : Nat :=
  if t < 5 then 2*k+17 else if t < 7 then 2*k+18
  else if t < 9 then 2*k+19 else 2*k+20

def q (k t i : Nat) : Nat :=
  match t with
  | 0 =>
    if i < 2 ∨ (k+6 ≤ i ∧ i < k+7) ∨ (k+10 ≤ i ∧ i < k+11) ∨ (2*k+15 ≤ i ∧ i < 2*k+17) then 1
    else if (k+7 ≤ i ∧ i < k+8) ∨ (k+9 ≤ i ∧ i < k+10) then 7
    else if (k+8 ≤ i ∧ i < k+9) then 12
    else 0
  | 1 =>
    if i < 2 ∨ (k+6 ≤ i ∧ i < k+7) ∨ (k+10 ≤ i ∧ i < k+11) ∨ (2*k+15 ≤ i ∧ i < 2*k+17) then 2
    else if (k+7 ≤ i ∧ i < k+8) ∨ (k+9 ≤ i ∧ i < k+10) then 15
    else if (k+8 ≤ i ∧ i < k+9) then 4
    else 0
  | 2 =>
    if i < 2 ∨ (2*k+15 ≤ i ∧ i < 2*k+17) then 4
    else if (k+6 ≤ i ∧ i < k+7) ∨ (k+10 ≤ i ∧ i < k+11) then 5
    else if (k+7 ≤ i ∧ i < k+10) then 10
    else 0
  | 3 =>
    if i < 2 ∨ (2*k+15 ≤ i ∧ i < 2*k+17) then 8
    else if (k+6 ≤ i ∧ i < k+7) ∨ (k+10 ≤ i ∧ i < k+11) then 11
    else if (k+7 ≤ i ∧ i < k+8) ∨ (k+9 ≤ i ∧ i < k+10) then 1
    else if (k+8 ≤ i ∧ i < k+9) then 2
    else 0
  | 4 =>
    if i < 2 ∨ (2*k+15 ≤ i ∧ i < 2*k+17) then 16
    else if (k+5 ≤ i ∧ i < k+6) ∨ (k+11 ≤ i ∧ i < k+12) then 1
    else if (k+6 ≤ i ∧ i < k+7) ∨ (k+10 ≤ i ∧ i < k+11) then 2
    else if (k+7 ≤ i ∧ i < k+8) ∨ (k+9 ≤ i ∧ i < k+10) then 3
    else if (k+8 ≤ i ∧ i < k+9) then 4
    else 0
  | 5 =>
    if i < 1 ∨ (2 ≤ i ∧ i < 3) ∨ (k+8 ≤ i ∧ i < k+10) ∨ (2*k+15 ≤ i ∧ i < 2*k+16) ∨ (2*k+17 ≤ i ∧ i < 2*k+18) then 7
    else if (1 ≤ i ∧ i < 2) ∨ (2*k+16 ≤ i ∧ i < 2*k+17) then 14
    else if (k+5 ≤ i ∧ i < k+6) ∨ (k+12 ≤ i ∧ i < k+13) then 1
    else if (k+6 ≤ i ∧ i < k+7) ∨ (k+11 ≤ i ∧ i < k+12) then 3
    else if (k+7 ≤ i ∧ i < k+8) ∨ (k+10 ≤ i ∧ i < k+11) then 5
    else 0
  | 6 =>
    if i < 1 ∨ (2 ≤ i ∧ i < 3) ∨ (2*k+15 ≤ i ∧ i < 2*k+16) ∨ (2*k+17 ≤ i ∧ i < 2*k+18) then 15
    else if (1 ≤ i ∧ i < 2) ∨ (2*k+16 ≤ i ∧ i < 2*k+17) then 8
    else if (k+5 ≤ i ∧ i < k+6) ∨ (k+12 ≤ i ∧ i < k+13) then 2
    else if (k+6 ≤ i ∧ i < k+7) ∨ (k+11 ≤ i ∧ i < k+12) then 6
    else if (k+7 ≤ i ∧ i < k+8) ∨ (k+10 ≤ i ∧ i < k+11) then 10
    else if (k+8 ≤ i ∧ i < k+10) then 14
    else 0
  | 7 =>
    if i < 1 ∨ (3 ≤ i ∧ i < 4) ∨ (k+8 ≤ i ∧ i < k+9) ∨ (k+10 ≤ i ∧ i < k+11) ∨ (2*k+15 ≤ i ∧ i < 2*k+16) ∨ (2*k+18 ≤ i ∧ i < 2*k+19) then 6
    else if (1 ≤ i ∧ i < 3) ∨ (2*k+16 ≤ i ∧ i < 2*k+18) then 14
    else if (k+5 ≤ i ∧ i < k+6) ∨ (k+13 ≤ i ∧ i < k+14) then 2
    else if (k+6 ≤ i ∧ i < k+7) ∨ (k+12 ≤ i ∧ i < k+13) then 8
    else if (k+7 ≤ i ∧ i < k+8) ∨ (k+11 ≤ i ∧ i < k+12) then 7
    else if (k+9 ≤ i ∧ i < k+10) then 10
    else 0
  | 8 =>
    if i < 1 ∨ (3 ≤ i ∧ i < 4) ∨ (k+8 ≤ i ∧ i < k+9) ∨ (k+10 ≤ i ∧ i < k+11) ∨ (2*k+15 ≤ i ∧ i < 2*k+16) ∨ (2*k+18 ≤ i ∧ i < 2*k+19) then 13
    else if (1 ≤ i ∧ i < 3) ∨ (2*k+16 ≤ i ∧ i < 2*k+18) then 9
    else if (k+5 ≤ i ∧ i < k+6) ∨ (k+13 ≤ i ∧ i < k+14) then 4
    else if (k+6 ≤ i ∧ i < k+7) ∨ (k+12 ≤ i ∧ i < k+13) then 16
    else if (k+7 ≤ i ∧ i < k+8) ∨ (k+11 ≤ i ∧ i < k+12) then 14
    else 0
  | 9 =>
    if i < 2 ∨ (3 ≤ i ∧ i < 5) ∨ (k+5 ≤ i ∧ i < k+6) ∨ (k+9 ≤ i ∧ i < k+11) ∨ (k+14 ≤ i ∧ i < k+15) ∨ (2*k+15 ≤ i ∧ i < 2*k+17) ∨ (2*k+18 ≤ i ∧ i < 2*k+20) then 4
    else if (k+6 ≤ i ∧ i < k+7) ∨ (k+13 ≤ i ∧ i < k+14) then 11
    else if (k+7 ≤ i ∧ i < k+8) ∨ (k+12 ≤ i ∧ i < k+13) then 12
    else if (k+8 ≤ i ∧ i < k+9) ∨ (k+11 ≤ i ∧ i < k+12) then 9
    else 0
  | 10 =>
    if i < 2 ∨ (3 ≤ i ∧ i < 5) ∨ (2*k+15 ≤ i ∧ i < 2*k+17) ∨ (2*k+18 ≤ i ∧ i < 2*k+20) then 8
    else if (k+5 ≤ i ∧ i < k+6) ∨ (k+8 ≤ i ∧ i < k+12) ∨ (k+14 ≤ i ∧ i < k+15) then 9
    else if (k+6 ≤ i ∧ i < k+7) ∨ (k+13 ≤ i ∧ i < k+14) then 3
    else if (k+7 ≤ i ∧ i < k+8) ∨ (k+12 ≤ i ∧ i < k+13) then 5
    else 0
  | _ => 0

def c (k t i : Nat) : Nat :=
  match t with
  | 0 =>
    if (k+8 < i ∧ i ≤ k+9) then 1
    else 0
  | 1 =>
    if (k+7 < i ∧ i ≤ k+8) ∨ (k+9 < i ∧ i ≤ k+10) then 1
    else 0
  | 2 =>
    if (k+7 < i ∧ i ≤ k+10) then 1
    else 0
  | 3 =>
    if (k+6 < i ∧ i ≤ k+7) ∨ (k+10 < i ∧ i ≤ k+11) then 1
    else 0
  | 4 =>
    if (0 < i ∧ i ≤ 2) ∨ (2*k+15 < i ∧ i ≤ 2*k+17) then 1
    else 0
  | 5 =>
    if (1 < i ∧ i ≤ 2) ∨ (2*k+16 < i ∧ i ≤ 2*k+17) then 1
    else 0
  | 6 =>
    if (0 < i ∧ i ≤ 1) ∨ (2 < i ∧ i ≤ 3) ∨ (k+7 < i ∧ i ≤ k+11) ∨ (2*k+15 < i ∧ i ≤ 2*k+16) ∨ (2*k+17 < i ∧ i ≤ 2*k+18) then 1
    else 0
  | 7 =>
    if (1 < i ∧ i ≤ 3) ∨ (k+9 < i ∧ i ≤ k+10) ∨ (2*k+16 < i ∧ i ≤ 2*k+18) then 1
    else 0
  | 8 =>
    if (0 < i ∧ i ≤ 4) ∨ (k+6 < i ∧ i ≤ k+9) ∨ (k+10 < i ∧ i ≤ k+13) ∨ (2*k+15 < i ∧ i ≤ 2*k+19) then 1
    else 0
  | 9 =>
    if (k+6 < i ∧ i ≤ k+9) ∨ (k+12 < i ∧ i ≤ k+14) then 1
    else 0
  | _ => 0

theorem carries (k t : Nat) (ht : t < 10) :
    ∀ i, i ≤ width k t → carry (q k t) i = c k t i := by
  apply carry_certificate _ _ _
  · have cases : t = 0 ∨ t = 1 ∨ t = 2 ∨ t = 3 ∨ t = 4 ∨ t = 5 ∨ t = 6 ∨ t = 7 ∨ t = 8 ∨ t = 9 := by omega
    rcases cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      simp [c] <;> repeat (first | omega | split)
  · intro i hi
    have cases : t = 0 ∨ t = 1 ∨ t = 2 ∨ t = 3 ∨ t = 4 ∨ t = 5 ∨ t = 6 ∨ t = 7 ∨ t = 8 ∨ t = 9 := by omega
    rcases cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
      simp [q, c, width] at * <;> repeat (first | omega | split)

theorem width_transition (k t : Nat) (ht : t < 10) :
    nextWidth (q k t) (width k t) = width k (t+1) := by
  have hc := carries k t ht (width k t) (Nat.le_refl _)
  rw [nextWidth, hc]
  have cases : t = 0 ∨ t = 1 ∨ t = 2 ∨ t = 3 ∨ t = 4 ∨ t = 5 ∨ t = 6 ∨ t = 7 ∨ t = 8 ∨ t = 9 := by omega
  rcases cases with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;>
    simp [c, width] <;> repeat (first | omega | split)

/-- Uniform actual normalization formula, with final-carry and width cases. -/
theorem next_from_carries (p a : Nat → Nat) (L W i : Nat)
    (hc : ∀ j, j ≤ L → carry p j = a j)
    (hw : nextWidth p L = W) (hi : i < W) :
    nextColumns p L i =
      (if i < L then (p i + a i) % 10 else a L) +
      (if W-1-i < L then (p (W-1-i) + a (W-1-i)) % 10 else a L) := by
  have ho : ∀ j, j ≤ L → output p j = (p j + a j) % 10 := by
    intro j hj
    simp only [output, hc j hj]
  have he : ∀ j, extended p L j =
      if j < L then (p j + a j) % 10 else a L := by
    intro j
    by_cases hj : j < L
    · simp only [extended, hj, if_true, ho j (by omega)]
    · simp only [extended, hj, if_false, hc L (Nat.le_refl _)]
  by_cases hz : carry p L = 0
  · have hW : W = L := by simpa [nextWidth, hz] using hw.symm
    rw [hW] at hi ⊢
    have hm : L-1-i < L := by omega
    simp only [nextColumns, hz, if_true, columnSum, reflected,
      ho i (by omega), ho (L-1-i) (by omega), hi, hm]
  · have hW : W = L+1 := by simpa [nextWidth, hz] using hw.symm
    rw [hW] at hi ⊢
    simp only [nextColumns, hz, if_false, columnSum, reflected, he]


end P196.Agent12.FirstHitEleven
