import P196.Foundations.LychrelDigitSums

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

/-- The actual finite normalization, including the terminal carry, adds c. -/
theorem value_outputWith (q : Nat → Nat) (L c : Nat) :
    value (outputWith q c) L + carryWith q c L * 10 ^ L = value q L + c := by
  induction L with
  | zero => simp [value, carryWith]
  | succ L ih =>
      have h := congrArg (fun x => x * 10 ^ L) (column_equation q c L)
      simp only [Nat.add_mul] at h
      simp only [value, Nat.pow_succ]
      have hc : carryWith q c (L + 1) * (10 ^ L * 10) =
          10 * carryWith q c (L + 1) * 10 ^ L := by
        simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
      rw [hc]
      omega

/-- A maximal initial 9-run, possibly the entire finite block. -/
def InitialNineRun (q : Nat → Nat) (L ℓ : Nat) : Prop :=
  ℓ ≤ L ∧ NinePrefix q ℓ ∧ (ℓ < L → q ℓ ≠ 9)

theorem initialNineRun_exists (q : Nat → Nat) (L : Nat) :
    ∃ ℓ, InitialNineRun q L ℓ := by
  induction L with
  | zero => exact ⟨0, by simp only [InitialNineRun]; exact ⟨by omega,
      ninePrefix_zero q, by omega⟩⟩
  | succ L ih =>
      obtain ⟨ℓ, hle, hp, hend⟩ := ih
      by_cases hlt : ℓ < L
      · exact ⟨ℓ, by omega, hp, fun _ => hend hlt⟩
      · have heq : ℓ = L := by omega
        subst ℓ
        by_cases hlast : q L = 9
        · exact ⟨L + 1, by omega, (ninePrefix_succ q L).mpr ⟨hp, hlast⟩,
            by omega⟩
        · exact ⟨L, by omega, hp, fun _ => hlast⟩

theorem nineIndicator_of_run (q : Nat → Nat) (L ℓ i : Nat)
    (hrun : InitialNineRun q L ℓ) (hi : i ≤ L) :
    nineIndicator q i = if i ≤ ℓ then 1 else 0 := by
  classical
  obtain ⟨hle, hp, hend⟩ := hrun
  by_cases hil : i ≤ ℓ
  · have hpi : NinePrefix q i := fun j hj => hp j (by omega)
    simp only [nineIndicator, if_pos hpi, if_pos hil]
  · have hpi : ¬ NinePrefix q i := by
      intro hn
      exact hend (by omega) (hn ℓ (by omega))
    simp only [nineIndicator, if_neg hpi, if_neg hil]

theorem carry_difference_run (q : Nat → Nat) (L ℓ i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18) (hrun : InitialNineRun q L ℓ)
    (hi : i ≤ L) :
    (carryWith q 1 i : Int) - (carryWith q 0 i : Int) =
      if i ≤ ℓ then 1 else 0 := by
  rw [carry_difference q i (fun j hj => hq j (by omega))]
  exact nineIndicator_of_run q L ℓ i hrun hi

/-- -9 on the initial 9-run, +1 at its first non-9, then zero. -/
theorem output_difference_run (q : Nat → Nat) (L ℓ i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18) (hrun : InitialNineRun q L ℓ)
    (hi : i < L) :
    (outputWith q 1 i : Int) - (outputWith q 0 i : Int) =
      if i < ℓ then -9 else if i = ℓ then 1 else 0 := by
  rw [output_difference q i (fun j hj => hq j (by omega))]
  rw [nineIndicator_of_run q L ℓ i hrun (by omega),
    nineIndicator_of_run q L ℓ (i + 1) hrun (by omega)]
  split <;> split <;> split <;> (try split) <;> omega

/-- The terminal carries differ exactly when the whole block consists of 9s. -/
theorem terminal_difference_run (q : Nat → Nat) (L ℓ : Nat)
    (hq : ∀ j, j < L → q j ≤ 18) (hrun : InitialNineRun q L ℓ) :
    (carryWith q 1 L : Int) - (carryWith q 0 L : Int) =
      if ℓ = L then 1 else 0 := by
  rw [carry_difference_run q L ℓ L hq hrun (by omega)]
  have hle := hrun.1
  split <;> split <;> omega

theorem all_nine_normalization (q : Nat → Nat) (L : Nat)
    (hq : NinePrefix q L) :
    (∀ i, i < L → outputWith q 0 i = 9 ∧ outputWith q 1 i = 0) ∧
      carryWith q 0 L = 0 ∧ carryWith q 1 L = 1 := by
  refine ⟨?_, carries_on_nine_prefix q L hq⟩
  intro i hi
  obtain ⟨h0, h1⟩ := carries_on_nine_prefix q i (fun j hj => hq j (by omega))
  simp only [outputWith, hq i hi, h0, h1]
  decide

/-- Restarting the recurrence at an actual column preserves every later carry. -/
theorem carryWith_shift (q : Nat → Nat) (c a i : Nat) :
    carryWith (fun j => q (a + j)) (carryWith q c a) i =
      carryWith q c (a + i) := by
  induction i with
  | zero => simp only [carryWith, Nat.add_zero]
  | succ i ih =>
      simp only [carryWith, ih, Nat.add_succ]
      rfl

theorem outputWith_shift (q : Nat → Nat) (c a i : Nat) :
    outputWith (fun j => q (a + j)) (carryWith q c a) i =
      outputWith q c (a + i) := by
  simp only [outputWith, carryWith_shift]

theorem actual_carry_shift (q : Nat → Nat) (a i : Nat) :
    carryWith (fun j => q (a + j)) (carry q a) i = carry q (a + i) := by
  rw [← carryWith_zero q a, carryWith_shift, carryWith_zero]

theorem actual_output_shift (q : Nat → Nat) (a i : Nat) :
    outputWith (fun j => q (a + j)) (carry q a) i = output q (a + i) := by
  rw [← carryWith_zero q a, outputWith_shift, outputWith_zero]

/-- Exact actual-minus-isolated carry for a block at an arbitrary offset. -/
theorem actual_block_carry_defect (q : Nat → Nat) (a L i : Nat)
    (hq : ∀ j, j < a + L → q j ≤ 18) (hi : i ≤ L) :
    (carry q (a + i) : Int) - (carry (fun j => q (a + j)) i : Int) =
      (carry q a : Int) * nineIndicator (fun j => q (a + j)) i := by
  rw [← actual_carry_shift q a i, ← carryWith_zero (fun j => q (a + j)) i]
  apply carry_difference_bit
  · exact carry_bounded q (a + L) hq a (by omega)
  · intro j hj
    exact hq (a + j) (by omega)

/-- Exact actual-minus-isolated emitted digit for a block at an arbitrary offset. -/
theorem actual_block_output_defect (q : Nat → Nat) (a L i : Nat)
    (hq : ∀ j, j < a + L → q j ≤ 18) (hi : i < L) :
    (output q (a + i) : Int) - (output (fun j => q (a + j)) i : Int) =
      (carry q a : Int) * (nineIndicator (fun j => q (a + j)) i -
        10 * nineIndicator (fun j => q (a + j)) (i + 1)) := by
  rw [← actual_output_shift q a i, ← outputWith_zero (fun j => q (a + j)) i]
  apply output_difference_bit
  · exact carry_bounded q (a + L) hq a (by omega)
  · intro j hj
    exact hq (a + j) (by omega)

/-- The outgoing-carry defect is supported exactly on the initial 9-run. -/
theorem actual_block_outgoing_run (q : Nat → Nat) (a L ℓ i : Nat)
    (hq : ∀ j, j < a + L → q j ≤ 18)
    (hrun : InitialNineRun (fun j => q (a + j)) L ℓ) (hi : i < L) :
    (carry q (a + (i + 1)) : Int) -
        (carry (fun j => q (a + j)) (i + 1) : Int) =
      if i < ℓ then (carry q a : Int) else 0 := by
  rw [actual_block_carry_defect q a L (i + 1) hq (by omega),
    nineIndicator_of_run (fun j => q (a + j)) L ℓ (i + 1) hrun (by omega)]
  split <;> split <;> simp_all <;> omega

end IncomingCarrySensitivity
