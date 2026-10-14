import LychrelDigitSums

/-!
Exact finite-column sensitivity to one incoming decimal carry.

Coefficients may be any natural numbers from 0 through 18; symmetry is
not assumed.  The extra incoming carry survives precisely through an
initial run of coefficients equal to 9.  Integer differences are used
throughout so that the emitted digit difference -9 is represented exactly.
-/

namespace IncomingCarrySensitivity

open DecimalDigits

/-- Decimal carry recurrence with a specified initial incoming carry. -/
def carryWith (q : Nat → Nat) (c : Nat) : Nat → Nat
  | 0 => c
  | i + 1 => (q i + carryWith q c i) / 10

/-- Emitted decimal digit with a specified initial incoming carry. -/
def outputWith (q : Nat → Nat) (c i : Nat) : Nat :=
  (q i + carryWith q c i) % 10

/-- Every coefficient strictly before i is 9. -/
def NinePrefix (q : Nat → Nat) (i : Nat) : Prop :=
  ∀ j, j < i → q j = 9

/-- Indicator of the prefix through which an extra carry still survives. -/
noncomputable def nineIndicator (q : Nat → Nat) (i : Nat) : Int := by
  classical
  exact if NinePrefix q i then 1 else 0

theorem carryWith_zero (q : Nat → Nat) (i : Nat) :
    carryWith q 0 i = carry q i := by
  induction i with
  | zero => rfl
  | succ i ih => simp only [carryWith, carry, ih]

theorem outputWith_zero (q : Nat → Nat) (i : Nat) :
    outputWith q 0 i = output q i := by
  simp only [outputWith, output, carryWith_zero]

theorem carryWith_bounded (q : Nat → Nat) (L c : Nat) (hc : c ≤ 1)
    (hq : ∀ i, i < L → q i ≤ 18) :
    ∀ i, i ≤ L → carryWith q c i ≤ 1 := by
  intro i
  induction i with
  | zero => intro _; exact hc
  | succ i ih =>
      intro hi
      have hp := ih (by omega)
      have hqi := hq i (by omega)
      simp only [carryWith]
      omega

theorem outputWith_bounded (q : Nat → Nat) (c i : Nat) :
    outputWith q c i ≤ 9 := by
  simp only [outputWith]
  omega

theorem column_equation (q : Nat → Nat) (c i : Nat) :
    outputWith q c i + 10 * carryWith q c (i + 1) =
      q i + carryWith q c i := by
  simp only [outputWith, carryWith]
  exact Nat.mod_add_div _ _

theorem ninePrefix_zero (q : Nat → Nat) : NinePrefix q 0 := by
  intro j hj
  omega

theorem ninePrefix_succ (q : Nat → Nat) (i : Nat) :
    NinePrefix q (i + 1) ↔ NinePrefix q i ∧ q i = 9 := by
  constructor
  · intro h
    exact ⟨fun j hj => h j (by omega), h i (by omega)⟩
  · rintro ⟨h, hqi⟩ j hj
    by_cases hji : j < i
    · exact h j hji
    · have : j = i := by omega
      simpa only [this] using hqi

theorem carries_on_nine_prefix (q : Nat → Nat) (i : Nat)
    (h : NinePrefix q i) : carryWith q 0 i = 0 ∧ carryWith q 1 i = 1 := by
  induction i with
  | zero => exact ⟨rfl, rfl⟩
  | succ i ih =>
      obtain ⟨hp, hqi⟩ := (ninePrefix_succ q i).mp h
      obtain ⟨h0, h1⟩ := ih hp
      simp only [carryWith, hqi, h0, h1]
      decide

/-- At a coefficient other than 9 the two incoming bits have equal outgoing carry. -/
theorem nonnine_carry_coalesces (a : Nat) (ha : a ≤ 18) (hne : a ≠ 9) :
    (a + 1) / 10 = a / 10 := by
  omega

theorem carries_after_nine_prefix (q : Nat → Nat) (i : Nat)
    (hq : ∀ j, j < i → q j ≤ 18) (h : ¬ NinePrefix q i) :
    carryWith q 1 i = carryWith q 0 i := by
  induction i with
  | zero => exact False.elim (h (ninePrefix_zero q))
  | succ i ih =>
      by_cases hp : NinePrefix q i
      · have hqi : q i ≠ 9 := by
          intro heq
          exact h ((ninePrefix_succ q i).mpr ⟨hp, heq⟩)
        obtain ⟨h0, h1⟩ := carries_on_nine_prefix q i hp
        simp only [carryWith, h0, h1, Nat.add_zero]
        exact nonnine_carry_coalesces (q i) (hq i (by omega)) hqi
      · have heq := ih (fun j hj => hq j (by omega)) hp
        simp only [carryWith, heq]

/-- Incoming carry difference, including the terminal boundary i=L. -/
theorem carry_difference (q : Nat → Nat) (i : Nat)
    (hq : ∀ j, j < i → q j ≤ 18) :
    (carryWith q 1 i : Int) - (carryWith q 0 i : Int) = nineIndicator q i := by
  classical
  by_cases hp : NinePrefix q i
  · obtain ⟨h0, h1⟩ := carries_on_nine_prefix q i hp
    simp only [h0, h1, nineIndicator, if_pos hp]
    decide
  · have heq := carries_after_nine_prefix q i hq hp
    simp only [heq, Int.sub_self, nineIndicator, if_neg hp]

/-- Exact digit defect, as a discrete carry-boundary difference. -/
theorem output_difference (q : Nat → Nat) (i : Nat)
    (hq : ∀ j, j < i + 1 → q j ≤ 18) :
    (outputWith q 1 i : Int) - (outputWith q 0 i : Int) =
      nineIndicator q i - 10 * nineIndicator q (i + 1) := by
  have h0 := column_equation q 0 i
  have h1 := column_equation q 1 i
  have hc := carry_difference q i (fun j hj => hq j (by omega))
  have hn := carry_difference q (i + 1) hq
  omega

theorem carry_difference_bit (q : Nat → Nat) (c i : Nat) (hc : c ≤ 1)
    (hq : ∀ j, j < i → q j ≤ 18) :
    (carryWith q c i : Int) - (carryWith q 0 i : Int) =
      (c : Int) * nineIndicator q i := by
  have cases : c = 0 ∨ c = 1 := by omega
  rcases cases with rfl | rfl
  · simp
  · simpa only [Int.natCast_one, Int.one_mul] using carry_difference q i hq

theorem output_difference_bit (q : Nat → Nat) (c i : Nat) (hc : c ≤ 1)
    (hq : ∀ j, j < i + 1 → q j ≤ 18) :
    (outputWith q c i : Int) - (outputWith q 0 i : Int) =
      (c : Int) * (nineIndicator q i - 10 * nineIndicator q (i + 1)) := by
  have cases : c = 0 ∨ c = 1 := by omega
  rcases cases with rfl | rfl
  · simp
  · simpa only [Int.natCast_one, Int.one_mul] using output_difference q i hq

end IncomingCarrySensitivity
