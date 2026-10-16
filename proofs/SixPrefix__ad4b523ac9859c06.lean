import LychrelDigitSums
import BoundaryTransducer

/-! Exact six-column boundary transition.  The Boolean input in the
whole-word theorem is the actual carry entering the high boundary window.
The windows may overlap: only `6 ≤ L` is assumed. -/

namespace SixPrefix

open DecimalDigits FoldedDecimal OverflowCarryNormalization CarryHistory

structure Prefix6 where
  x0 : Nat
  x1 : Nat
  x2 : Nat
  x3 : Nat
  x4 : Nat
  x5 : Nat
  deriving DecidableEq, Repr

def front (p : Prefix6) : BoundaryTransducer.Prefix := ⟨p.x0, p.x1, p.x2⟩

def boundary6 (q : Nat → Nat) : Prefix6 := ⟨q 0, q 1, q 2, q 3, q 4, q 5⟩

def step (p : Prefix6) (control : Bool) : Prefix6 × Nat :=
  let l0 := p.x0 % 10
  let a1 := p.x0 / 10
  let l1 := (p.x1 + a1) % 10
  let a2 := (p.x1 + a1) / 10
  let l2 := (p.x2 + a2) % 10
  let a3 := (p.x2 + a2) / 10
  let l3 := (p.x3 + a3) % 10
  let a4 := (p.x3 + a3) / 10
  let l4 := (p.x4 + a4) % 10
  let a5 := (p.x4 + a4) / 10
  let l5 := (p.x5 + a5) % 10
  let h5 := (p.x5 + control.toNat) % 10
  let b5 := (p.x5 + control.toNat) / 10
  let h4 := (p.x4 + b5) % 10
  let b4 := (p.x4 + b5) / 10
  let h3 := (p.x3 + b4) % 10
  let b3 := (p.x3 + b4) / 10
  let h2 := (p.x2 + b3) % 10
  let b2 := (p.x2 + b3) / 10
  let h1 := (p.x1 + b2) % 10
  let b1 := (p.x1 + b2) / 10
  let h0 := (p.x0 + b1) % 10
  let e := (p.x0 + b1) / 10
  let p' : Prefix6 := if e = 0 then
    ⟨l0 + h0, l1 + h1, l2 + h2, l3 + h3, l4 + h4, l5 + h5⟩
    else ⟨l0 + 1, l1 + h0, l2 + h1, l3 + h2, l4 + h3, l5 + h4⟩
  (p', e)

def actualControl (q : Nat → Nat) (L : Nat) : Bool :=
  decide (carry q (L - 6) = 1)

theorem actualControl_exact (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) :
    carry q (L - 6) = (actualControl q L).toNat := by
  have hb := carry_bounded q L ha.2.2.1 (L - 6) (by omega)
  by_cases hc : carry q (L - 6) = 1
  · simp [actualControl, hc]
  · have hz : carry q (L - 6) = 0 := by omega
    simp [actualControl, hz]

theorem actualControl_false_iff (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) :
    actualControl q L = false ↔ carry q (L - 6) = 0 := by
  have hb := carry_bounded q L ha.2.2.1 (L - 6) (by omega)
  simp only [actualControl, decide_eq_false_iff_not]
  omega

theorem actualControl_true_iff (q : Nat → Nat) (L : Nat) :
    actualControl q L = true ↔ carry q (L - 6) = 1 := by
  simp [actualControl]

theorem high_boundary_data (q : Nat → Nat) (L : Nat) (c : Bool)
    (hL : 6 ≤ L) (ha : Admissible L q)
    (hc : carry q (L - 6) = c.toNat) :
    output q (L - 6) = (q 5 + c.toNat) % 10 ∧
    output q (L - 5) = (q 4 + (q 5 + c.toNat) / 10) % 10 ∧
    output q (L - 4) = (q 3 + (q 4 + (q 5 + c.toNat) / 10) / 10) % 10 ∧
    output q (L - 3) = (q 2 + (q 3 + (q 4 + (q 5 + c.toNat) / 10) / 10) / 10) % 10 ∧
    output q (L - 2) = (q 1 + (q 2 + (q 3 + (q 4 + (q 5 + c.toNat) / 10) / 10) / 10) / 10) % 10 ∧
    output q (L - 1) = (q 0 + (q 1 + (q 2 + (q 3 + (q 4 + (q 5 + c.toNat) / 10) / 10) / 10) / 10) / 10) % 10 ∧
    carry q L = (q 0 + (q 1 + (q 2 + (q 3 + (q 4 + (q 5 + c.toNat) / 10) / 10) / 10) / 10) / 10) / 10 := by
  have hs0 : q (L - 1) = q 0 := by
    simpa only [Nat.sub_zero] using (ha.2.2.2.1 0 (by omega)).symm
  have hs1 : q (L - 2) = q 1 := by
    have he : L - 1 - 1 = L - 2 := by omega
    simpa only [he] using (ha.2.2.2.1 1 (by omega)).symm
  have hs2 : q (L - 3) = q 2 := by
    have he : L - 1 - 2 = L - 3 := by omega
    simpa only [he] using (ha.2.2.2.1 2 (by omega)).symm
  have hs3 : q (L - 4) = q 3 := by
    have he : L - 1 - 3 = L - 4 := by omega
    simpa only [he] using (ha.2.2.2.1 3 (by omega)).symm
  have hs4 : q (L - 5) = q 4 := by
    have he : L - 1 - 4 = L - 5 := by omega
    simpa only [he] using (ha.2.2.2.1 4 (by omega)).symm
  have hs5 : q (L - 6) = q 5 := by
    have he : L - 1 - 5 = L - 6 := by omega
    simpa only [he] using (ha.2.2.2.1 5 (by omega)).symm
  have hindex1 : L - 5 = (L - 6) + 1 := by omega
  have hk1 : carry q (L - 5) = (q 5 + c.toNat) / 10 := by
    rw [hindex1, carry, hs5, hc]
  have hindex2 : L - 4 = (L - 5) + 1 := by omega
  have hk2 : carry q (L - 4) = (q 4 + (q 5 + c.toNat) / 10) / 10 := by
    rw [hindex2, carry, hs4, hk1]
  have hindex3 : L - 3 = (L - 4) + 1 := by omega
  have hk3 : carry q (L - 3) = (q 3 + (q 4 + (q 5 + c.toNat) / 10) / 10) / 10 := by
    rw [hindex3, carry, hs3, hk2]
  have hindex4 : L - 2 = (L - 3) + 1 := by omega
  have hk4 : carry q (L - 2) = (q 2 + (q 3 + (q 4 + (q 5 + c.toNat) / 10) / 10) / 10) / 10 := by
    rw [hindex4, carry, hs2, hk3]
  have hindex5 : L - 1 = (L - 2) + 1 := by omega
  have hk5 : carry q (L - 1) = (q 1 + (q 2 + (q 3 + (q 4 + (q 5 + c.toNat) / 10) / 10) / 10) / 10) / 10 := by
    rw [hindex5, carry, hs1, hk4]
  have hindex6 : L = (L - 1) + 1 := by omega
  have hk6 : carry q L = (q 0 + (q 1 + (q 2 + (q 3 + (q 4 + (q 5 + c.toNat) / 10) / 10) / 10) / 10) / 10) / 10 := by
    calc
      carry q L = carry q ((L - 1) + 1) := congrArg (carry q) hindex6
      _ = _ := by rw [carry, hs0, hk5]
  exact ⟨by simp only [output, hs5, hc],
    by simp only [output, hs4, hk1],
    by simp only [output, hs3, hk2],
    by simp only [output, hs2, hk3],
    by simp only [output, hs1, hk4],
    by simp only [output, hs0, hk5], hk6⟩

theorem low_boundary_data (q : Nat → Nat) :
    output q 0 = q 0 % 10 ∧
    output q 1 = (q 1 + q 0 / 10) % 10 ∧
    output q 2 = (q 2 + (q 1 + q 0 / 10) / 10) % 10 ∧
    output q 3 = (q 3 + (q 2 + (q 1 + q 0 / 10) / 10) / 10) % 10 ∧
    output q 4 = (q 4 + (q 3 + (q 2 + (q 1 + q 0 / 10) / 10) / 10) / 10) % 10 ∧
    output q 5 = (q 5 + (q 4 + (q 3 + (q 2 + (q 1 + q 0 / 10) / 10) / 10) / 10) / 10) % 10 := by
  simp [output, carry]

/-- Exact six-column transition for any real incoming boundary carry. -/
theorem boundary6_step_exact (q : Nat → Nat) (L : Nat) (c : Bool)
    (hL : 6 ≤ L) (ha : Admissible L q)
    (hc : carry q (L - 6) = c.toNat) :
    (boundary6 (nextColumns q L), carry q L) = step (boundary6 q) c := by
  obtain ⟨hh0, hh1, hh2, hh3, hh4, hh5, he⟩ := high_boundary_data q L c hL ha hc
  obtain ⟨hl0, hl1, hl2, hl3, hl4, hl5⟩ := low_boundary_data q
  simp only [step, boundary6]
  simp only [← hl0, ← hl1, ← hl2, ← hl3, ← hl4, ← hl5,
    ← hh0, ← hh1, ← hh2, ← hh3, ← hh4, ← hh5, ← he]
  by_cases hz : carry q L = 0
  · simp only [hz, if_true, nextColumns, columnSum, reflected, Nat.sub_zero]
    have hi1 : L - 1 - 1 = L - 2 := by omega
    have hi2 : L - 1 - 2 = L - 3 := by omega
    have hi3 : L - 1 - 3 = L - 4 := by omega
    have hi4 : L - 1 - 4 = L - 5 := by omega
    have hi5 : L - 1 - 5 = L - 6 := by omega
    simp only [hi1, hi2, hi3, hi4, hi5]
  · have hone : carry q L = 1 := by
      have hb := carry_bounded q L ha.2.2.1 L (Nat.le_refl L)
      omega
    simp only [hz, if_false, nextColumns, columnSum, reflected,
      Nat.add_sub_cancel, Nat.sub_zero, extended,
      show 0 < L by omega, show 1 < L by omega, show 2 < L by omega,
      show 3 < L by omega, show 4 < L by omega, show 5 < L by omega,
      show L - 1 < L by omega, show L - 2 < L by omega,
      show L - 3 < L by omega, show L - 4 < L by omega,
      show L - 5 < L by omega, Nat.lt_irrefl, if_true, if_false, hone]
    simp

/-- The graph control is the actual carry at `L - 6`, with no independence
assumption on overlapping boundary windows. -/
theorem actual_boundary6_step (q : Nat → Nat) (L : Nat)
    (hL : 6 ≤ L) (ha : Admissible L q) :
    (boundary6 (nextColumns q L), carry q L) =
      step (boundary6 q) (actualControl q L) :=
  boundary6_step_exact q L (actualControl q L) hL ha (actualControl_exact q L ha)

end SixPrefix
