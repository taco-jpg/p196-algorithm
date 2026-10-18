import P196.Drafts.Agent4GeneralBaseNormalization.DigitsBridge

/-!
Agent #4. Exact no-overflow source subclaim: local output bounds, actual width,
and the arithmetic deduction of a palindrome from low mirrored pair sums.
The finite-word bound alone is not claimed to imply an actual orbit theorem;
final overflow and canonical widths are handled explicitly below.
-/
namespace P196.Agent4.GeneralBase

theorem normalized_quotient_carry (b low n : Nat) (q : Nat → Nat)
    (hb : 2 ≤ b) (hlow : low + 1 < b) (hs : Symmetric n q)
    (k : Nat) (hk : k ≤ n) :
    arithmeticCarry b (normalized b low n q) k = carryAt b q k := by
  have hbound : ∀ i < n, normalized b low n q i ≤ 2 * (b - 1) := by
    intro i hi
    have h := normalSum_le_base b low (carryAt b q (i + 1))
      (carryAt b q (n - i)) (by omega)
    change normalSum b low _ _ ≤ 2 * (b - 1)
    omega
  rw [arithmeticCarry_eq_carryAt b n _ hb hbound k hk]
  exact complete_carry_word_preserved b low n q hb hlow hs k hk

theorem arithmeticOutput_congr (b n : Nat) (q r : Nat → Nat)
    (h : ∀ i < n, q i = r i) (i : Nat) (hi : i < n) :
    arithmeticOutput b q i = arithmeticOutput b r i := by
  unfold arithmeticOutput
  rw [h i hi, arithmeticCarry_congr b n q r h i (by omega)]

/-- Unequal outgoing bits force complementary incoming bits on a neutral pair. -/
theorem neutral_output_pair (b q c d : Nat) (hb : 2 ≤ b)
    (hc : c ≤ 1) (hd : d ≤ 1)
    (hne : carryStep b q c ≠ carryStep b q d) :
    (b - 1 + c) % b + (b - 1 + d) % b = b - 1 := by
  have hcd : c ≠ d := by
    intro h
    apply hne
    rw [h]
  have hcases : (c = 0 ∧ d = 1) ∨ (c = 1 ∧ d = 0) := by omega
  have hsum : b - 1 + 1 = b := by omega
  have hlt : b - 1 < b := by omega
  rcases hcases with h | h
  · rcases h with ⟨rfl, rfl⟩
    simp [hsum, Nat.mod_eq_of_lt hlt]
  · rcases h with ⟨rfl, rfl⟩
    simp [hsum, Nat.mod_eq_of_lt hlt]

/-- The source's low/low <=6, high/high <=2, and unequal =b-1 bounds. -/
theorem normalized_pair_output_bound (b q c d : Nat)
    (hb : 8 ≤ b) (hc : c ≤ 1) (hd : d ≤ 1) :
    (normalSum b 2 (carryStep b q c) (carryStep b q d) + c) % b +
      (normalSum b 2 (carryStep b q c) (carryStep b q d) + d) % b ≤ b - 1 := by
  by_cases heq : carryStep b q c = carryStep b q d
  · by_cases hz : carryStep b q c = 0
    · have hs : normalSum b 2 (carryStep b q c) (carryStep b q d) = 2 := by
        unfold normalSum
        rw [if_pos heq, if_pos hz]
      rw [hs, Nat.mod_eq_of_lt (by omega : 2 + c < b),
        Nat.mod_eq_of_lt (by omega : 2 + d < b)]
      omega
    · have hs : normalSum b 2 (carryStep b q c) (carryStep b q d) = b := by
        unfold normalSum
        rw [if_pos heq, if_neg hz]
      have hc' : c < b := by omega
      have hd' : d < b := by omega
      rw [hs]
      simp only [Nat.add_mod, Nat.mod_self, Nat.zero_add,
        Nat.mod_eq_of_lt hc', Nat.mod_eq_of_lt hd']
      omega
  · have hs : normalSum b 2 (carryStep b q c) (carryStep b q d) = b - 1 := by
      unfold normalSum
      rw [if_neg heq]
    rw [hs, neutral_output_pair b q c d (by omega) hc hd heq]
    exact Nat.le_refl _

/-- Fixed-width first output has only sub-base mirrored pair sums. -/
theorem normalized_output_pairs_low (b n : Nat) (q : Nat → Nat)
    (hb : 8 ≤ b) (hs : Symmetric n q) (i : Nat) (hi : i < n) :
    pairCoeff n (arithmeticOutput b (normalized b 2 n q)) i ≤ b - 1 := by
  have hm : n - i = (n - 1 - i) + 1 := by omega
  have hmirror : carryAt b q (n - i) =
      carryStep b (q i) (carryAt b q (n - 1 - i)) := by
    rw [hm, carryAt, ← hs i hi]
  have hnorm := normalized_symmetric b 2 n q i hi
  unfold pairCoeff arithmeticOutput
  rw [← hnorm,
    normalized_quotient_carry b 2 n q (by omega) (by omega) hs i (by omega),
    normalized_quotient_carry b 2 n q (by omega) (by omega) hs
      (n - 1 - i) (by omega)]
  unfold normalized
  rw [carryAt, hmirror]
  exact normalized_pair_output_bound b (q i) (carryAt b q i)
    (carryAt b q (n - 1 - i)) hb (carryAt_bit b q i)
    (carryAt_bit b q (n - 1 - i))

theorem leading_positive_of_value_lower (b n : Nat) (d : Nat → Nat)
    (hn : 0 < n) (hd : ∀ i < n, d i < b)
    (hlower : b ^ (n - 1) ≤ value b d n) : 0 < d (n - 1) := by
  cases n with
  | zero => omega
  | succ k =>
      simp only [Nat.succ_sub_one] at hlower ⊢
      by_cases hz : d k = 0
      · have hprefix := value_lt_pow b k d (fun i hi => hd i (by omega))
        simp only [value, hz, Nat.zero_mul, Nat.add_zero] at hlower
        omega
      · omega

/-- Without final overflow, the ordinary output keeps the true input width. -/
theorem canonical_output_nooverflow (b n : Nat) (d : Nat → Nat)
    (hb : 0 < b) (hd : CanonicalDigits b n d)
    (hno : arithmeticCarry b (pairCoeff n d) n = 0) :
    CanonicalDigits b n (arithmeticOutput b (pairCoeff n d)) := by
  have hbound : ∀ i < n, arithmeticOutput b (pairCoeff n d) i < b :=
    fun i _ => arithmeticOutput_lt_base b (pairCoeff n d) i hb
  have hvalue := reverse_add_arithmetic b n d
  simp only [hno, Nat.zero_mul, Nat.add_zero] at hvalue
  have hlow := (canonical_value_bounds b n d hd).1
  refine ⟨hd.1, hbound, ?_⟩
  apply leading_positive_of_value_lower b n _ hd.1 hbound
  omega

/-- Arithmetic reverse-add at a width; applications separately prove it canonical. -/
def addAtWidth (b n a : Nat) : Nat := a + reverseAtWidth b n a

/-- Low pair sums yield the true next numeral, with symmetric extracted digits. -/
theorem low_pairs_palindrome (b n : Nat) (d : Nat → Nat)
    (hb : 0 < b) (hd : CanonicalDigits b n d)
    (hlow : ∀ i < n, pairCoeff n d i < b) :
    CanonicalNumeral b n (addAtWidth b n (value b d n)) ∧
      reverseAtWidth b n (addAtWidth b n (value b d n)) =
        addAtWidth b n (value b d n) := by
  have hlead : 0 < pairCoeff n d (n - 1) := by
    have h := hd.2.2
    unfold pairCoeff
    omega
  have hcanon : CanonicalDigits b n (pairCoeff n d) := ⟨hd.1, hlow, hlead⟩
  have hnum := (canonical_extracted_digits b n (pairCoeff n d) hb hcanon).1
  have hsym : reverseAtWidth b n (value b (pairCoeff n d) n) =
      value b (pairCoeff n d) n := by
    rw [reverseAtWidth_value b n (pairCoeff n d) hb hlow]
    apply value_congr
    intro i hi
    exact (pairCoeff_symmetric n d i hi).symm
  have heq : value b (pairCoeff n d) n = addAtWidth b n (value b d n) := by
    unfold addAtWidth
    rw [pair_value, reverseAtWidth_value b n d hb hd.2.1]
  rw [heq] at hnum hsym
  exact ⟨hnum, hsym⟩

end P196.Agent4.GeneralBase

#print axioms P196.Agent4.GeneralBase.normalized_quotient_carry
#print axioms P196.Agent4.GeneralBase.arithmeticOutput_congr
#print axioms P196.Agent4.GeneralBase.neutral_output_pair
#print axioms P196.Agent4.GeneralBase.normalized_pair_output_bound
#print axioms P196.Agent4.GeneralBase.normalized_output_pairs_low
#print axioms P196.Agent4.GeneralBase.leading_positive_of_value_lower
#print axioms P196.Agent4.GeneralBase.canonical_output_nooverflow
#print axioms P196.Agent4.GeneralBase.low_pairs_palindrome
