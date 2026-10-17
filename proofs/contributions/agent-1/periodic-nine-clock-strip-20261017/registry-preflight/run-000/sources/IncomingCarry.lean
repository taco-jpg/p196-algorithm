import LychrelDigitSums

/-!
Exact finite-block response to either incoming carry.
The first non-nine coefficient synchronizes the two outgoing carries;
the changed digits consist of an initial 9-to-0 run followed by one
incremented digit. Statements are bridged to the actual decimal carry.
No invariant collision family or Lychrel existence is asserted.
-/

namespace IncomingCarry

open DecimalDigits

def carryIn (q : Nat → Nat) (c : Nat) : Nat → Nat
  | 0 => c
  | i + 1 => (q i + carryIn q c i) / 10

def outputIn (q : Nat → Nat) (c i : Nat) : Nat :=
  (q i + carryIn q c i) % 10

theorem carryIn_zero_eq_carry (q : Nat → Nat) (i : Nat) :
    carryIn q 0 i = DecimalDigits.carry q i := by
  induction i with
  | zero => rfl
  | succ i ih => simp only [carryIn, DecimalDigits.carry, ih]

theorem outputIn_zero_eq_output (q : Nat → Nat) (i : Nat) :
    outputIn q 0 i = DecimalDigits.output q i := by
  simp only [outputIn, DecimalDigits.output, carryIn_zero_eq_carry]

/-- Exact concatenation, with the outgoing carry passed to the next block. -/
theorem carryIn_add (q : Nat → Nat) (c a b : Nat) :
    carryIn q c (a + b) = carryIn (fun i => q (a + i)) (carryIn q c a) b := by
  induction b with
  | zero => rfl
  | succ b ih =>
    change (q (a + b) + carryIn q c (a + b)) / 10 =
      (q (a + b) + carryIn (fun i => q (a + i)) (carryIn q c a) b) / 10
    rw [ih]

/-- An arbitrary interval of the actual carry computation is a block
computation initialized by its actual incoming carry. -/
theorem carryIn_actual_interval (q : Nat → Nat) (a k : Nat) :
    carryIn (fun i => q (a + i)) (DecimalDigits.carry q a) k =
      DecimalDigits.carry q (a + k) := by
  rw [← carryIn_zero_eq_carry q a, ← carryIn_add, carryIn_zero_eq_carry]

theorem outputIn_actual_interval (q : Nat → Nat) (a k : Nat) :
    outputIn (fun i => q (a + i)) (DecimalDigits.carry q a) k =
      DecimalDigits.output q (a + k) := by
  simp only [outputIn, DecimalDigits.output, carryIn_actual_interval]

theorem carryIn_congr (q r : Nat → Nat) (c n : Nat)
    (hqr : ∀ i, i < n → q i = r i) : carryIn q c n = carryIn r c n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [carryIn, hqr n (by omega), ih (fun i hi => hqr i (by omega))]

theorem outputIn_congr (q r : Nat → Nat) (c i : Nat)
    (hqr : ∀ k, k ≤ i → q k = r k) : outputIn q c i = outputIn r c i := by
  simp only [outputIn, hqr i (Nat.le_refl i),
    carryIn_congr q r c i (fun k hk => hqr k (by omega))]

theorem carryIn_bounded (q : Nat → Nat) (c n : Nat) (hc : c ≤ 1)
    (hq : ∀ i, i < n → q i ≤ 18) : carryIn q c n ≤ 1 := by
  induction n with
  | zero => exact hc
  | succ n ih =>
    have hp := ih (fun i hi => hq i (by omega))
    have hqn := hq n (by omega)
    simp only [carryIn]
    omega

theorem column_transfer_ne_iff (q a b : Nat)
    (hq : q ≤ 18) (ha : a ≤ 1) (hb : b ≤ 1) :
    (q + a) / 10 ≠ (q + b) / 10 ↔ a ≠ b ∧ q = 9 := by
  omega

/-- A finite block transmits dependence on the incoming carry if and
only if every coefficient in that block is the neutral coefficient 9. -/
theorem carryIn_ne_iff (q : Nat → Nat) (a b n : Nat)
    (ha : a ≤ 1) (hb : b ≤ 1) (hq : ∀ i, i < n → q i ≤ 18) :
    carryIn q a n ≠ carryIn q b n ↔ a ≠ b ∧ ∀ i, i < n → q i = 9 := by
  induction n with
  | zero => simp only [carryIn]; constructor <;> intro h
            · exact ⟨h, by intro i hi; omega⟩
            · exact h.1
  | succ n ih =>
    have hqn := hq n (by omega)
    have hqa : ∀ i, i < n → q i ≤ 18 := fun i hi => hq i (by omega)
    have hca := carryIn_bounded q a n ha hqa
    have hcb := carryIn_bounded q b n hb hqa
    rw [carryIn, carryIn, column_transfer_ne_iff _ _ _ hqn hca hcb, ih hqa]
    constructor
    · rintro ⟨⟨hne, hp⟩, hlast⟩
      refine ⟨hne, ?_⟩
      intro i hi
      by_cases hin : i < n
      · exact hp i hin
      · have he : i = n := by omega
        simpa only [he] using hlast
    · rintro ⟨hne, hp⟩
      exact ⟨⟨hne, fun i hi => hp i (by omega)⟩, hp n (by omega)⟩

theorem carryIn_eq_of_nonNine (q : Nat → Nat) (a b n j : Nat)
    (ha : a ≤ 1) (hb : b ≤ 1) (hq : ∀ i, i < n → q i ≤ 18)
    (hj : j < n) (hne : q j ≠ 9) : carryIn q a n = carryIn q b n := by
  apply Classical.byContradiction
  intro h
  exact hne (((carryIn_ne_iff q a b n ha hb hq).mp h).2 j hj)

theorem carryIn_nines (q : Nat → Nat) (c n : Nat) (hc : c ≤ 1)
    (hq : ∀ i, i < n → q i = 9) : carryIn q c n = c := by
  induction n with
  | zero => rfl
  | succ n ih =>
    have hp := ih (fun i hi => hq i (by omega))
    have hn := hq n (by omega)
    simp only [carryIn, hp, hn]
    omega

/-- The neutral-block exception: every digit flips from nine to zero,
and the outgoing carry retains the incoming carry. -/
theorem all_nines_response (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i = 9) :
    (∀ i, i < L → outputIn q 0 i = 9 ∧ outputIn q 1 i = 0) ∧
    carryIn q 0 L = 0 ∧ carryIn q 1 L = 1 := by
  refine ⟨?_, carryIn_nines q 0 L (by omega) hq,
    carryIn_nines q 1 L (by omega) hq⟩
  intro i hi
  have hc0 := carryIn_nines q 0 i (by omega) (fun k hk => hq k (by omega))
  have hc1 := carryIn_nines q 1 i (by omega) (fun k hk => hq k (by omega))
  simp only [outputIn, hq i hi, hc0, hc1]
  decide

/-- Every block transfer is constant zero, the identity, or constant one.
The identity case is exactly the all-nine block, including the empty block. -/
theorem carryIn_transfer_trichotomy (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) :
    (carryIn q 0 L = 0 ∧ carryIn q 1 L = 0) ∨
    ((∀ i, i < L → q i = 9) ∧ carryIn q 0 L = 0 ∧ carryIn q 1 L = 1) ∨
    (carryIn q 0 L = 1 ∧ carryIn q 1 L = 1) := by
  by_cases he : carryIn q 0 L = carryIn q 1 L
  · have hb := carryIn_bounded q 0 L (by omega) hq
    by_cases hz : carryIn q 0 L = 0
    · exact Or.inl ⟨hz, by omega⟩
    · exact Or.inr (Or.inr ⟨by omega, by omega⟩)
  · have hn := ((carryIn_ne_iff q 0 1 L (by omega) (by omega) hq).mp he).2
    exact Or.inr (Or.inl ⟨hn, (all_nines_response q L hn).2⟩)

/-- A prior non-nine coefficient makes the output digit independent of
the incoming carry, even when later coefficients equal nine again. -/
theorem outputIn_eq_after_nonNine (q : Nat → Nat) (a b L j i : Nat)
    (ha : a ≤ 1) (hb : b ≤ 1) (hq : ∀ k, k < L → q k ≤ 18)
    (hji : j < i) (hi : i < L) (hne : q j ≠ 9) :
    outputIn q a i = outputIn q b i := by
  have hc := carryIn_eq_of_nonNine q a b i j ha hb
    (fun k hk => hq k (by omega)) hji hne
  simp only [outputIn, hc]

/-- Complete coefficientwise response at the first non-nine coefficient.
This is the exact finite carry-collision correction profile. -/
theorem first_nonNine_response (q : Nat → Nat) (L j : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) (hj : j < L)
    (hprefix : ∀ i, i < j → q i = 9) (hne : q j ≠ 9) :
    (∀ i, i < j → outputIn q 0 i = 9 ∧ outputIn q 1 i = 0) ∧
    outputIn q 1 j = outputIn q 0 j + 1 ∧
    (∀ i, j < i → i < L → outputIn q 1 i = outputIn q 0 i) ∧
    carryIn q 1 L = carryIn q 0 L := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro i hi
    have hc0 := carryIn_nines q 0 i (by omega) (fun k hk => hprefix k (by omega))
    have hc1 := carryIn_nines q 1 i (by omega) (fun k hk => hprefix k (by omega))
    simp only [outputIn, hprefix i hi, hc0, hc1]
    decide
  · have hc0 := carryIn_nines q 0 j (by omega) hprefix
    have hc1 := carryIn_nines q 1 j (by omega) hprefix
    have hqj := hq j hj
    simp only [outputIn, hc0, hc1]
    omega
  · intro i hji hi
    exact outputIn_eq_after_nonNine q 1 0 L j i (by omega) (by omega) hq hji hi hne
  · exact carryIn_eq_of_nonNine q 1 0 L j (by omega) (by omega) hq hj hne

/-- The normalized polynomial correction, stated exactly coefficientwise. -/
theorem first_nonNine_response_coefficient (q : Nat → Nat) (L j i : Nat)
    (hq : ∀ k, k < L → q k ≤ 18) (hj : j < L) (hi : i < L)
    (hprefix : ∀ k, k < j → q k = 9) (hne : q j ≠ 9) :
    (outputIn q 1 i : Int) - (outputIn q 0 i : Int) =
      if i < j then -9 else if i = j then 1 else 0 := by
  have hr := first_nonNine_response q L j hq hj hprefix hne
  by_cases hlt : i < j
  · rw [if_pos hlt, (hr.1 i hlt).1, (hr.1 i hlt).2]
    decide
  · rw [if_neg hlt]
    by_cases he : i = j
    · rw [if_pos he, he]
      have hinc := hr.2.1
      omega
    · rw [if_neg he, hr.2.2.1 i (by omega) hi]
      omega

/-- Exact outgoing-carry comparison for two identical blocks occurring
inside one actual finite pair-coefficient word. No fresh normalization
or independently chosen incoming carries are assumed. -/
theorem actual_repeated_block_transfer_ne_iff (q : Nat → Nat) (L a b m : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) (ha : a + m ≤ L) (hb : b + m ≤ L)
    (heq : ∀ i, i < m → q (a + i) = q (b + i)) :
    DecimalDigits.carry q (a + m) ≠ DecimalDigits.carry q (b + m) ↔
      DecimalDigits.carry q a ≠ DecimalDigits.carry q b ∧
      ∀ i, i < m → q (a + i) = 9 := by
  rw [← carryIn_actual_interval q a m, ← carryIn_actual_interval q b m]
  have he : carryIn (fun i => q (a + i)) (DecimalDigits.carry q b) m =
      carryIn (fun i => q (b + i)) (DecimalDigits.carry q b) m :=
    carryIn_congr _ _ _ _ heq
  rw [← he]
  exact carryIn_ne_iff _ _ _ _ (DecimalDigits.carry_bounded q L hq a (by omega))
    (DecimalDigits.carry_bounded q L hq b (by omega))
    (fun i hi => hq (a + i) (by omega))

/-- Any non-nine in two repeated blocks blocks all incoming-carry
influence on the later paired output digits. -/
theorem actual_repeated_block_output_locality (q : Nat → Nat) (L a b m j i : Nat)
    (hq : ∀ k, k < L → q k ≤ 18) (ha : a + m ≤ L) (hb : b + m ≤ L)
    (heq : ∀ k, k < m → q (a + k) = q (b + k))
    (hj : j < i) (hi : i < m) (hne : q (a + j) ≠ 9) :
    DecimalDigits.output q (a + i) = DecimalDigits.output q (b + i) := by
  rw [← outputIn_actual_interval q a i, ← outputIn_actual_interval q b i]
  have he := outputIn_congr (fun k => q (a + k)) (fun k => q (b + k))
    (DecimalDigits.carry q b) i (fun k hk => heq k (by omega))
  rw [← he]
  exact outputIn_eq_after_nonNine _ _ _ m j i
    (DecimalDigits.carry_bounded q L hq a (by omega))
    (DecimalDigits.carry_bounded q L hq b (by omega))
    (fun k hk => hq (a + k) (by omega)) hj hi hne

#print axioms carryIn_ne_iff
#print axioms first_nonNine_response
#print axioms carryIn_actual_interval
#print axioms first_nonNine_response_coefficient
#print axioms actual_repeated_block_transfer_ne_iff
#print axioms actual_repeated_block_output_locality
#print axioms carryIn_transfer_trichotomy

end IncomingCarry
