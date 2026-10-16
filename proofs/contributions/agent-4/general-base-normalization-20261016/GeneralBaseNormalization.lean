import Lean.Elab.Tactic.Omega

/-!
Agent #4. General-base normalization: local carry transport, complete finite
carry words, symmetry, center parity, and canonical digit-word realization.
Original source: 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5,
proofs/research/resume_even_base_normalization_proof.txt, normalization section.
This module does not assert the four-step termination theorem.
-/
namespace P196.Agent4.GeneralBase

def carryStep (b q c : Nat) : Nat := if b ≤ q + c then 1 else 0

def carryAt (b : Nat) (q : Nat → Nat) : Nat → Nat
  | 0 => 0
  | k + 1 => carryStep b (q k) (carryAt b q k)

def normalSum (b low u v : Nat) : Nat :=
  if u = v then (if u = 0 then low else b) else b - 1

def normalized (b low n : Nat) (q : Nat → Nat) (i : Nat) : Nat :=
  normalSum b low (carryAt b q (i + 1)) (carryAt b q (n - i))

def Symmetric (n : Nat) (q : Nat → Nat) : Prop :=
  ∀ i, i < n → q i = q (n - 1 - i)

def EvenCenter (n : Nat) (q : Nat → Nat) : Prop :=
  ∀ i, i < n → i = n - 1 - i → q i % 2 = 0

theorem carryStep_bit (b q c : Nat) : carryStep b q c ≤ 1 := by
  unfold carryStep
  split <;> omega

theorem carryAt_bit (b : Nat) (q : Nat → Nat) (k : Nat) :
    carryAt b q k ≤ 1 := by
  cases k with
  | zero => simp [carryAt]
  | succ k => exact carryStep_bit b (q k) (carryAt b q k)

theorem unequal_carries_force_neutral (b q c d : Nat)
    (hc : c ≤ 1) (hd : d ≤ 1)
    (hne : carryStep b q c ≠ carryStep b q d) : q = b - 1 := by
  unfold carryStep at hne
  split at hne <;> split at hne <;> omega

theorem normalSum_comm (b low u v : Nat) :
    normalSum b low u v = normalSum b low v u := by
  by_cases h : u = v
  · subst v; rfl
  · simp [normalSum, h, Ne.symm h]

theorem normalSum_le_base (b low u v : Nat) (hlow : low ≤ b) :
    normalSum b low u v ≤ b := by
  unfold normalSum
  split
  · split <;> omega
  · omega

/-- Normalization preserves an outgoing carry with the same incoming bit. -/
theorem normalize_column (b low q c d : Nat)
    (hb : 2 ≤ b) (hlow : low + 1 < b) (hc : c ≤ 1) (hd : d ≤ 1) :
    carryStep b (normalSum b low (carryStep b q c) (carryStep b q d)) c =
      carryStep b q c := by
  unfold normalSum
  split
  · next heq =>
      split
      · next hzero =>
          have hh : ¬ b ≤ low + c := by omega
          calc
            carryStep b low c = 0 := by simp [carryStep, hh]
            _ = carryStep b q c := hzero.symm
      · next hnzero =>
          have hbit := carryStep_bit b q c
          have hone : carryStep b q c = 1 := by omega
          rw [hone]
          have hh : b ≤ b + c := by omega
          simp [carryStep, hh]
  · next hne =>
      have hq := unequal_carries_force_neutral b q c d hc hd hne
      rw [← hq]

theorem mirror_index (n i : Nat) (hi : i < n) :
    n - 1 - (n - 1 - i) = i := by omega

/-- Every original boundary carry, including the final overflow, is preserved. -/
theorem complete_carry_word_preserved (b low n : Nat) (q : Nat → Nat)
    (hb : 2 ≤ b) (hlow : low + 1 < b) (hs : Symmetric n q)
    (k : Nat) (hk : k ≤ n) :
    carryAt b (normalized b low n q) k = carryAt b q k := by
  induction k with
  | zero => rfl
  | succ k ih =>
      have hkn : k < n := by omega
      have hm : n - k = (n - 1 - k) + 1 := by omega
      have hmirror : carryAt b q (n - k) =
          carryStep b (q k) (carryAt b q (n - 1 - k)) := by
        rw [hm, carryAt, ← hs k hkn]
      simp only [carryAt]
      rw [ih (by omega)]
      unfold normalized
      rw [carryAt, hmirror]
      exact normalize_column b low (q k) (carryAt b q k)
        (carryAt b q (n - 1 - k)) hb hlow
        (carryAt_bit b q k) (carryAt_bit b q (n - 1 - k))

theorem normalized_symmetric (b low n : Nat) (q : Nat → Nat) :
    Symmetric n (normalized b low n q) := by
  intro i hi
  have h1 : n - (n - 1 - i) = i + 1 := by omega
  have h2 : (n - 1 - i) + 1 = n - i := by omega
  simp only [normalized, h1, h2]
  exact normalSum_comm b low _ _

theorem normalized_even_center (b low n : Nat) (q : Nat → Nat)
    (hb : b % 2 = 0) (hlow : low % 2 = 0) :
    EvenCenter n (normalized b low n q) := by
  intro i hi hfix
  have hm : n - i = i + 1 := by omega
  unfold normalized
  rw [hm]
  unfold normalSum
  simp only [ite_true]
  split <;> assumption

/-- Floor on the low side and ceiling on the high side of each mirrored pair. -/
def splitDigit (n : Nat) (q : Nat → Nat) (i : Nat) : Nat :=
  if i < n - 1 - i then q i / 2 else q i - q i / 2

theorem splitDigit_lt_base (b n : Nat) (q : Nat → Nat)
    (hb : 2 ≤ b) (hq : ∀ i < n, q i ≤ b) (i : Nat) (hi : i < n) :
    splitDigit n q i < b := by
  have h := hq i hi
  unfold splitDigit
  split <;> omega

theorem splitDigit_pair_sum (n : Nat) (q : Nat → Nat)
    (hs : Symmetric n q) (he : EvenCenter n q) (i : Nat) (hi : i < n) :
    splitDigit n q i + splitDigit n q (n - 1 - i) = q i := by
  have hm := mirror_index n i hi
  by_cases hfix : i = n - 1 - i
  · have hpar := he i hi hfix
    unfold splitDigit
    rw [hm, ← hs i hi]
    split <;> split <;> omega
  · unfold splitDigit
    rw [hm, ← hs i hi]
    split <;> split <;> omega

theorem splitDigit_leading_positive (n : Nat) (q : Nat → Nat)
    (hn : 0 < n) (hs : Symmetric n q) (hq : 0 < q 0) :
    0 < splitDigit n q (n - 1) := by
  have h := hs 0 hn
  simp only [Nat.sub_zero] at h
  unfold splitDigit
  simp only [Nat.sub_self, Nat.not_lt_zero, ite_false]
  omega

/-- A genuine canonical digit word, with the original positive width. -/
theorem symmetric_word_realizable (b n : Nat) (q : Nat → Nat)
    (hb : 2 ≤ b) (hn : 0 < n) (hs : Symmetric n q)
    (he : EvenCenter n q) (hq : ∀ i < n, q i ≤ b) (hout : 0 < q 0) :
    ∃ d : Nat → Nat,
      (∀ i < n, d i < b) ∧ 0 < d (n - 1) ∧
      (∀ i < n, d i + d (n - 1 - i) = q i) := by
  refine ⟨splitDigit n q, ?_, ?_, ?_⟩
  · exact splitDigit_lt_base b n q hb hq
  · exact splitDigit_leading_positive n q hn hs hout
  · exact splitDigit_pair_sum n q hs he

def chosenLow (b n : Nat) (q : Nat → Nat) : Nat :=
  if carryAt b q n = 0 then 2 else 0

theorem chosenLow_bound (b n : Nat) (q : Nat → Nat) (hb : 4 ≤ b) :
    chosenLow b n q + 1 < b := by
  unfold chosenLow
  split <;> omega

theorem chosenLow_even (b n : Nat) (q : Nat → Nat) :
    chosenLow b n q % 2 = 0 := by
  unfold chosenLow
  split <;> decide

theorem normalized_outer_positive (b n : Nat) (q : Nat → Nat) (hb : 2 ≤ b) :
    0 < normalized b (chosenLow b n q) n q 0 := by
  unfold normalized chosenLow normalSum
  simp only [Nat.zero_add, Nat.sub_zero]
  split
  · next heq =>
      split
      · next hz =>
          have hv : carryAt b q n = 0 := by omega
          simp [hv]
      · omega
  · omega

/-- Exact finite-word subclaim. Arithmetic quotient correspondence is separate. -/
theorem normalization_has_same_width_representative (b n : Nat) (q : Nat → Nat)
    (hb : 4 ≤ b) (hbe : b % 2 = 0) (hn : 0 < n) (hs : Symmetric n q) :
    ∃ d : Nat → Nat,
      (∀ i < n, d i < b) ∧ 0 < d (n - 1) ∧
      (∀ i < n, d i + d (n - 1 - i) =
        normalized b (chosenLow b n q) n q i) ∧
      (∀ k ≤ n, carryAt b (normalized b (chosenLow b n q) n q) k =
        carryAt b q k) := by
  have hlow := chosenLow_bound b n q hb
  obtain ⟨d, hd, hpos, hpair⟩ := symmetric_word_realizable b n
    (normalized b (chosenLow b n q) n q) (by omega) hn
    (normalized_symmetric b (chosenLow b n q) n q)
    (normalized_even_center b (chosenLow b n q) n q hbe (chosenLow_even b n q))
    (fun i hi => normalSum_le_base b (chosenLow b n q) _ _ (by omega))
    (normalized_outer_positive b n q (by omega))
  refine ⟨d, hd, hpos, hpair, ?_⟩
  intro k hk
  exact complete_carry_word_preserved b (chosenLow b n q) n q
    (by omega) hlow hs k hk

end P196.Agent4.GeneralBase

#print axioms P196.Agent4.GeneralBase.carryStep_bit
#print axioms P196.Agent4.GeneralBase.carryAt_bit
#print axioms P196.Agent4.GeneralBase.unequal_carries_force_neutral
#print axioms P196.Agent4.GeneralBase.normalSum_comm
#print axioms P196.Agent4.GeneralBase.normalSum_le_base
#print axioms P196.Agent4.GeneralBase.normalize_column
#print axioms P196.Agent4.GeneralBase.mirror_index
#print axioms P196.Agent4.GeneralBase.complete_carry_word_preserved
#print axioms P196.Agent4.GeneralBase.normalized_symmetric
#print axioms P196.Agent4.GeneralBase.normalized_even_center
#print axioms P196.Agent4.GeneralBase.splitDigit_lt_base
#print axioms P196.Agent4.GeneralBase.splitDigit_pair_sum
#print axioms P196.Agent4.GeneralBase.splitDigit_leading_positive
#print axioms P196.Agent4.GeneralBase.symmetric_word_realizable
#print axioms P196.Agent4.GeneralBase.chosenLow_bound
#print axioms P196.Agent4.GeneralBase.chosenLow_even
#print axioms P196.Agent4.GeneralBase.normalized_outer_positive
#print axioms P196.Agent4.GeneralBase.normalization_has_same_width_representative
