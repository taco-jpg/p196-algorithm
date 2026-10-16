import IncomingCarry

/-!
Exact normalized digit-mass response, including the outgoing carry.
This supplies finite collision arithmetic, not a preserved orbit family.
-/

namespace CarryResponseMass

open IncomingCarry DecimalDigits DecimalMass DecimalUnboundedMass Lychrel196

/-- The sum of all normalized digits, including the outgoing carry. -/
def massIn (q : Nat → Nat) (c L : Nat) : Nat :=
  wordSum (outputIn q c) L + carryIn q c L

theorem wordSum_constant_on (q : Nat → Nat) (c L : Nat)
    (hq : ∀ i, i < L → q i = c) : wordSum q L = L * c := by
  induction L with
  | zero => simp [wordSum]
  | succ L ih =>
    rw [wordSum, hq L (by omega), ih (fun i hi => hq i (by omega)), Nat.succ_mul]

/-- Exact retained-digit response when the initial nine-run stops at j. -/
theorem retained_mass_first_nonNine (q : Nat → Nat) (L j : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) (hj : j < L)
    (hprefix : ∀ i, i < j → q i = 9) (hne : q j ≠ 9) :
    wordSum (outputIn q 1) L + 9 * j = wordSum (outputIn q 0) L + 1 := by
  have hr := first_nonNine_response q L j hq hj hprefix hne
  have hp0 := wordSum_constant_on (outputIn q 0) 9 j (fun i hi => (hr.1 i hi).1)
  have hp1 := wordSum_constant_on (outputIn q 1) 0 j (fun i hi => (hr.1 i hi).2)
  have hs0 := wordSum_split (outputIn q 0) (j + 1) (L - (j + 1))
  have hs1 := wordSum_split (outputIn q 1) (j + 1) (L - (j + 1))
  have hlen : j + 1 + (L - (j + 1)) = L := by omega
  rw [hlen, wordSum] at hs0 hs1
  have ht : wordSum (fun i => outputIn q 1 (j + 1 + i)) (L - (j + 1)) =
      wordSum (fun i => outputIn q 0 (j + 1 + i)) (L - (j + 1)) := by
    apply wordSum_congr
    intro i hi
    exact hr.2.2.1 (j + 1 + i) (by omega) (by omega)
  have hd := hr.2.1
  omega

theorem massIn_first_nonNine (q : Nat → Nat) (L j : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) (hj : j < L)
    (hprefix : ∀ i, i < j → q i = 9) (hne : q j ≠ 9) :
    massIn q 1 L + 9 * j = massIn q 0 L + 1 := by
  have hm := retained_mass_first_nonNine q L j hq hj hprefix hne
  have hc := (first_nonNine_response q L j hq hj hprefix hne).2.2.2
  unfold massIn
  omega

theorem massIn_all_nines (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i = 9) :
    massIn q 1 L + 9 * L = massIn q 0 L + 1 := by
  have hr := all_nines_response q L hq
  have hp0 := wordSum_constant_on (outputIn q 0) 9 L (fun i hi => (hr.1 i hi).1)
  have hp1 := wordSum_constant_on (outputIn q 1) 0 L (fun i hi => (hr.1 i hi).2)
  unfold massIn
  have hc0 := hr.2.1
  have hc1 := hr.2.2
  omega

/-- Exact length of the initial run of neutral coefficients. -/
def InitialNines (q : Nat → Nat) (L k : Nat) : Prop :=
  k ≤ L ∧ (∀ i, i < k → q i = 9) ∧ (k = L ∨ q k ≠ 9)

/-- Computable length of the initial run, with no existential choice. -/
def initialNinesLength (q : Nat → Nat) : Nat → Nat
  | 0 => 0
  | L + 1 => if q 0 = 9 then initialNinesLength (fun i => q (i + 1)) L + 1 else 0

theorem initialNinesLength_spec (q : Nat → Nat) (L : Nat) :
    InitialNines q L (initialNinesLength q L) := by
  induction L generalizing q with
  | zero => simp [InitialNines, initialNinesLength]
  | succ L ih =>
    by_cases hq0 : q 0 = 9
    · simp only [initialNinesLength, hq0, if_true]
      have hp := ih (fun i => q (i + 1))
      refine ⟨by have := hp.1; omega, ?_, ?_⟩
      · intro i hi
        by_cases hz : i = 0
        · simpa only [hz] using hq0
        · have he : i - 1 + 1 = i := by omega
          have hh := hp.2.1 (i - 1) (by omega)
          simpa only [he] using hh
      · rcases hp.2.2 with he | hn
        · exact Or.inl (by omega)
        · exact Or.inr hn
    · simp only [initialNinesLength, hq0, if_false]
      exact ⟨by omega, by intro i hi; omega, Or.inr hq0⟩

/-- Unified response, including empty and all-nine blocks. -/
theorem massIn_response (q : Nat → Nat) (L k : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) (hk : InitialNines q L k) :
    massIn q 1 L + 9 * k = massIn q 0 L + 1 := by
  rcases hk.2.2 with he | hn
  · subst k
    exact massIn_all_nines q L hk.2.1
  · by_cases he : k = L
    · subst k
      exact massIn_all_nines q L hk.2.1
    · exact massIn_first_nonNine q L k hq (by have := hk.1; omega) hk.2.1 hn

theorem massIn_binary_response (q : Nat → Nat) (L k c : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) (hk : InitialNines q L k) (hc : c ≤ 1) :
    massIn q c L + 9 * c * k = massIn q 0 L + c := by
  by_cases hz : c = 0
  · subst c
    simp
  · have ho : c = 1 := by omega
    subst c
    simpa only [Nat.mul_one] using massIn_response q L k hq hk

theorem massIn_response_computable (q : Nat → Nat) (L c : Nat)
    (hq : ∀ i, i < L → q i ≤ 18) (hc : c ≤ 1) :
    massIn q c L + 9 * c * initialNinesLength q L = massIn q 0 L + c :=
  massIn_binary_response q L (initialNinesLength q L) c hq
    (initialNinesLength_spec q L) hc

theorem outputIn_add (q : Nat → Nat) (c a i : Nat) :
    outputIn q c (a + i) = outputIn (fun k => q (a + k)) (carryIn q c a) i := by
  simp only [outputIn, carryIn_add]

/-- At concatenation the intermediate carry is counted in both block
masses, so one copy is removed from their sum. -/
theorem massIn_add (q : Nat → Nat) (c a b : Nat) :
    massIn q c (a + b) + carryIn q c a =
      massIn q c a + massIn (fun i => q (a + i)) (carryIn q c a) b := by
  have hs := wordSum_split (outputIn q c) a b
  have ht : wordSum (fun i => outputIn q c (a + i)) b =
      wordSum (outputIn (fun i => q (a + i)) (carryIn q c a)) b := by
    apply wordSum_congr
    intro i hi
    exact outputIn_add q c a i
  have hc := carryIn_add q c a b
  unfold massIn
  omega

theorem massIn_congr (q r : Nat → Nat) (c L : Nat)
    (hqr : ∀ i, i < L → q i = r i) : massIn q c L = massIn r c L := by
  have hc := carryIn_congr q r c L hqr
  have hd : wordSum (outputIn q c) L = wordSum (outputIn r c) L := by
    apply wordSum_congr
    intro i hi
    exact outputIn_congr q r c i (fun k hk => hqr k (by omega))
  unfold massIn
  rw [hc, hd]

/-- The mass is the ordinary digit sum of the actual numeric step. -/
theorem massIn_actual_step (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : Canonical n d L) :
    massIn (columnSum d L) 0 L = digitSum (step n) := by
  have hb := digitSum_step_balance d L hc.2.1 (Or.inr hc.2.2.1)
  have ho := wordSum_output (columnSum d L) L
  have hcols := wordSum_columns d L
  have hv := digitSum_value d L hc.2.1
  have hd : wordSum (outputIn (columnSum d L) 0) L = wordSum (output (columnSum d L)) L := by
    apply wordSum_congr
    intro i hi
    exact outputIn_zero_eq_output _ i
  have hcarry := carryIn_zero_eq_carry (columnSum d L) L
  rw [hc.2.2.2] at hb hv
  unfold massIn
  omega

/-- Exact collision mass for a finite word B H B. Both occurrences of B
are normalized with the incoming carries produced by the actual word.
The only correction is nine times the two incoming-carry/run products. -/
theorem three_block_collision_mass (q : Nat → Nat) (b m : Nat)
    (hq : ∀ i, i < 2 * b + m → q i ≤ 18)
    (hblocks : ∀ i, i < b → q (b + m + i) = q i) :
    massIn q 0 (2 * b + m) +
      9 * (carryIn q 0 b * initialNinesLength (fun i => q (b + i)) m +
        carryIn q 0 (b + m) * initialNinesLength q b) =
      2 * massIn q 0 b + massIn (fun i => q (b + i)) 0 m := by
  have hfirst := massIn_add q 0 b m
  have hlast := massIn_add q 0 (b + m) b
  have hlen : b + m + b = 2 * b + m := by omega
  rw [hlen] at hlast
  have hrepeat := massIn_congr (fun i => q (b + m + i)) q
    (carryIn q 0 (b + m)) b hblocks
  rw [hrepeat] at hlast
  have hmiddle := massIn_response_computable (fun i => q (b + i)) m
    (carryIn q 0 b) (fun i hi => hq (b + i) (by omega))
    (carryIn_bounded q 0 b (by omega) (fun i hi => hq i (by omega)))
  have houter := massIn_response_computable q b (carryIn q 0 (b + m))
    (fun i hi => hq i (by omega))
    (carryIn_bounded q 0 (b + m) (by omega) (fun i hi => hq i (by omega)))
  simp only [Nat.mul_add, ← Nat.mul_assoc]
  omega

/-- Independent zero-carry block masses give an upper bound, with the
entire deficit described by the preceding exact identity. -/
theorem three_block_collision_mass_le (q : Nat → Nat) (b m : Nat)
    (hq : ∀ i, i < 2 * b + m → q i ≤ 18)
    (hblocks : ∀ i, i < b → q (b + m + i) = q i) :
    massIn q 0 (2 * b + m) ≤ 2 * massIn q 0 b + massIn (fun i => q (b + i)) 0 m := by
  have h := three_block_collision_mass q b m hq hblocks
  omega

/-- Zero mass correction is characterized exactly by vanishing of both
incoming-carry/initial-nine-run products. -/
theorem three_block_collision_mass_eq_iff (q : Nat → Nat) (b m : Nat)
    (hq : ∀ i, i < 2 * b + m → q i ≤ 18)
    (hblocks : ∀ i, i < b → q (b + m + i) = q i) :
    massIn q 0 (2 * b + m) = 2 * massIn q 0 b + massIn (fun i => q (b + i)) 0 m ↔
      carryIn q 0 b * initialNinesLength (fun i => q (b + i)) m = 0 ∧
      carryIn q 0 (b + m) * initialNinesLength q b = 0 := by
  have h := three_block_collision_mass q b m hq hblocks
  omega

/-- The collision identity for the digit sum of an actual integer step. -/
theorem actual_step_three_block_collision_mass (n : Nat) (d : Nat → Nat) (b m : Nat)
    (hc : Canonical n d (2 * b + m))
    (hblocks : ∀ i, i < b → columnSum d (2 * b + m) (b + m + i) =
      columnSum d (2 * b + m) i) :
    digitSum (step n) +
      9 * (carryIn (columnSum d (2 * b + m)) 0 b *
          initialNinesLength (fun i => columnSum d (2 * b + m) (b + i)) m +
        carryIn (columnSum d (2 * b + m)) 0 (b + m) *
          initialNinesLength (columnSum d (2 * b + m)) b) =
      2 * massIn (columnSum d (2 * b + m)) 0 b +
        massIn (fun i => columnSum d (2 * b + m) (b + i)) 0 m := by
  have h := three_block_collision_mass (columnSum d (2 * b + m)) b m
    (columnSum_bounded d (2 * b + m) hc.2.1) hblocks
  rw [massIn_actual_step n d (2 * b + m) hc] at h
  exact h

/-- A concrete canonical collision: B=(10,10), H=(9,9), seed 555455.
Separate normalization predicts mass 22; the actual step has mass four. -/
theorem concrete_collision_mass_loss :
    step 555455 = 1110010 ∧ digitSum (step 555455) = 4 ∧
    2 * massIn (fun _ => 10) 0 2 + massIn (fun _ => 9) 0 2 = 22 := by
  have hs : step 555455 = 1110010 := by decide
  refine ⟨hs, ?_, by decide⟩
  rw [hs]
  simp [digitSum]

#print axioms massIn_response
#print axioms massIn_binary_response
#print axioms massIn_add
#print axioms massIn_actual_step
#print axioms massIn_response_computable
#print axioms three_block_collision_mass
#print axioms three_block_collision_mass_eq_iff
#print axioms actual_step_three_block_collision_mass
#print axioms concrete_collision_mass_loss

end CarryResponseMass
