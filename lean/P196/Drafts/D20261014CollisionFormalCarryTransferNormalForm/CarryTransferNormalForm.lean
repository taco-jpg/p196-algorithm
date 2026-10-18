import P196.Foundations.IncomingCarry

/-!
The incoming-carry transfer class of a finite block is determined by its
rightmost non-nine coefficient. This is an exact three-state summary;
it does not assert preservation of any collision family under iteration.
-/

namespace CarryTransferNormalForm

open IncomingCarry DecimalDigits

theorem column_transfer_nonNine (q c : Nat) (hq : q ≤ 18)
    (hc : c ≤ 1) (hne : q ≠ 9) : (q + c) / 10 = q / 10 := by
  omega

/-- A terminal run of nines preserves the carry produced at its start. -/
theorem carryIn_suffix_nines (q : Nat → Nat) (c a b : Nat)
    (hc : c ≤ 1) (hq : ∀ i, i < a → q i ≤ 18)
    (htail : ∀ i, i < b → q (a + i) = 9) :
    carryIn q c (a + b) = carryIn q c a := by
  rw [carryIn_add]
  exact carryIn_nines _ _ _ (carryIn_bounded q c a hc hq) htail

/-- The last non-nine coefficient determines the outgoing carry,
independently of every preceding coefficient and the incoming carry. -/
theorem carryIn_last_nonNine (q : Nat → Nat) (c L j : Nat)
    (hc : c ≤ 1) (hq : ∀ i, i < L → q i ≤ 18) (hj : j < L)
    (hne : q j ≠ 9) (htail : ∀ i, j < i → i < L → q i = 9) :
    carryIn q c L = q j / 10 := by
  have hlen : j + 1 + (L - (j + 1)) = L := by omega
  have hs := carryIn_suffix_nines q c (j + 1) (L - (j + 1)) hc
    (fun i hi => hq i (by omega))
    (fun i hi => htail (j + 1 + i) (by omega) (by omega))
  rw [hlen] at hs
  rw [hs, carryIn]
  exact column_transfer_nonNine (q j) (carryIn q c j) (hq j hj)
    (carryIn_bounded q c j hc (fun i hi => hq i (by omega))) hne

/-- Explicit normal form: rightmost non-nine below nine gives constant
zero; rightmost non-nine above nine gives constant one. -/
theorem rightmost_nonNine_transfer (q : Nat → Nat) (L j : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) (hj : j < L)
    (hne : q j ≠ 9) (htail : ∀ i, j < i → i < L → q i = 9) :
    (carryIn q 0 L, carryIn q 1 L) =
      if q j ≤ 8 then (0, 0) else (1, 1) := by
  have h0 := carryIn_last_nonNine q 0 L j (by omega) hq hj hne htail
  have h1 := carryIn_last_nonNine q 1 L j (by omega) hq hj hne htail
  have hqj := hq j hj
  rw [h0, h1]
  split
  · have hz : q j / 10 = 0 := by omega
    rw [hz]
  · have ho : q j / 10 = 1 := by omega
    rw [ho]

/-- The normal form holds for any actual interval in the existing decimal
carry computation, with no assumption about the incoming carry's value. -/
theorem actual_interval_last_nonNine (q : Nat → Nat) (L a m j : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) (ha : a + m ≤ L) (hj : j < m)
    (hne : q (a + j) ≠ 9)
    (htail : ∀ i, j < i → i < m → q (a + i) = 9) :
    DecimalDigits.carry q (a + m) = q (a + j) / 10 := by
  rw [← carryIn_actual_interval q a m]
  exact carryIn_last_nonNine (fun i => q (a + i)) (DecimalDigits.carry q a)
    m j (DecimalDigits.carry_bounded q L hq a (by omega))
    (fun i hi => hq (a + i) (by omega)) hj hne htail

#print axioms carryIn_last_nonNine
#print axioms rightmost_nonNine_transfer
#print axioms actual_interval_last_nonNine

end CarryTransferNormalForm
