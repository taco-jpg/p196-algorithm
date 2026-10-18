import P196.Drafts.Agent421Agent421.Agent421NoOverflowWords

namespace Agent421NoOverflow
open SignedDigitUniqueness BaseReflection ResetNormalization PhysicalWidth ReverseAdd Agent11HighBase

def normalized (b s : Int) (q : Nat → Int) (L i : Nat) : Int :=
  norm b s (carry b q (i+1)) (carry b q (L-i))

theorem normalized_symmetric (b s : Int) (q : Nat → Int) (L i : Nat) (hi : i < L) :
    normalized b s q L i = normalized b s q L (L-1-i) := by
  have h1 : L-1-i+1 = L-i := by omega
  have h2 : L-(L-1-i) = i+1 := by omega
  simp only [normalized, h1, h2]
  exact norm_symmetric b s _ _

theorem normalized_range (b s : Int) (q : Nat → Int) (L i : Nat)
    (hb : 7 ≤ b) (hs : 1 ≤ s ∧ 2*s ≤ b-1) :
    0 < normalized b s q L i ∧ normalized b s q L i ≤ 2*b-2 :=
  norm_range b s _ _ hb hs

theorem normalized_center_even (b s : Int) (q : Nat → Int) (L i : Nat)
    (he : (b+s-1)%2 = 0) (hi : i < L) (hc : i = L-1-i) :
    normalized b s q L i % 2 = 0 := by
  have h : L-i = i+1 := by omega
  simp only [normalized, h]
  exact norm_center_even b s _ he

theorem normalized_preserves_carry (b s : Int) (q : Nat → Int) (L : Nat)
    (hb : 7 ≤ b) (hs : 1 ≤ s ∧ 2*s ≤ b-1)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i)) :
    ∀ i, i ≤ L → carry b (normalized b s q L) i = carry b q i := by
  intro i
  induction i with
  | zero => intro _; rfl
  | succ i ih =>
    intro hi
    have him : L-1-i < L := by omega
    have hf : L-1-i+1 = L-i := by omega
    have hl := norm_local b s (q i) (carry b q i) (carry b q (L-1-i)) hb hs
      (hq i (by omega)) (carry_bounded b q L (by omega) hq i (by omega))
      (carry_bounded b q L (by omega) hq (L-1-i) (by omega))
    have hout : (q i + carry b q (L-1-i))/b = carry b q (L-i) := by
      rw [hsym i (by omega), ← hf]
      rfl
    dsimp at hl
    rw [hout] at hl
    change (normalized b s q L i + carry b (normalized b s q L) i)/b = carry b q (i+1)
    rw [ih (by omega)]
    exact hl.1

theorem normalized_next_low (b s : Int) (q : Nat → Int) (L : Nat)
    (hb : 7 ≤ b) (hs : 1 ≤ s ∧ 2*s ≤ b-1)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i)) :
    ∀ i, i < L → output b (normalized b s q L) i +
      output b (normalized b s q L) (L-1-i) ≤ b-1 := by
  intro i hi
  have him : L-1-i < L := by omega
  have hf : L-1-i+1 = L-i := by omega
  have hl := norm_local b s (q i) (carry b q i) (carry b q (L-1-i)) hb hs
    (hq i hi) (carry_bounded b q L (by omega) hq i (by omega))
    (carry_bounded b q L (by omega) hq (L-1-i) (by omega))
  have hout : (q i + carry b q (L-1-i))/b = carry b q (L-i) := by
    rw [hsym i hi, ← hf]
    rfl
  dsimp at hl
  rw [hout] at hl
  unfold output
  rw [normalized_preserves_carry b s q L hb hs hq hsym i (by omega),
      normalized_preserves_carry b s q L hb hs hq hsym (L-1-i) (by omega),
      ← normalized_symmetric b s q L i hi]
  exact hl.2.2

theorem low_carry_zero (b : Int) (q : Nat → Int) (L : Nat)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i < b) :
    ∀ i, i ≤ L → carry b q i = 0 := by
  intro i
  induction i with
  | zero => intro _; simp [carry]
  | succ i ih =>
    intro hi
    have hr := hq i (by omega)
    simp only [carry, ih (by omega), Int.add_zero]
    exact (low_divmod b (q i) hr.1 hr.2).1

theorem normalize_low (b : Int) (q : Nat → Int) (L : Nat)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i < b) : normalize b (word q L) = word q L := by
  rw [normalize_nooverflow b q L (low_carry_zero b q L hq L (by omega))]
  apply word_ext
  intro i hi
  simp only [output, low_carry_zero b q L hq i (by omega), Int.add_zero]
  exact (low_divmod b (q i) (hq i hi).1 (hq i hi).2).2

/-- The list-level reverse-add operation is the existing canonical normalizer. -/
def stepDigits (b : Int) (d : List Int) : List Int := normalize b (pairs d)

/-- Exact all-width second-output palindrome for the no-overflow normalized word.
This theorem is about the actual digit normalizer, not a merely abstract transition. -/
theorem normalized_two_step_palindrome (b s : Int) (q : Nat → Int) (L : Nat)
    (hb : 7 ≤ b) (hs : 1 ≤ s ∧ 2*s ≤ b-1)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i))
    (hover : carry b q L = 0) :
    (stepDigits b (normalize b (word (normalized b s q L) L))).reverse =
      stepDigits b (normalize b (word (normalized b s q L) L)) := by
  have hc := (normalized_preserves_carry b s q L hb hs hq hsym L (by omega)).trans hover
  rw [normalize_nooverflow b (normalized b s q L) L hc]
  let e := output b (normalized b s q L)
  have low : ∀ i, i < L → 0 ≤ e i + e (L-1-i) ∧ e i + e (L-1-i) < b := by
    intro i hi
    have ha : 0 ≤ e i := Int.emod_nonneg _ (by omega)
    have hb' : 0 ≤ e (L-1-i) := Int.emod_nonneg _ (by omega)
    have hu := normalized_next_low b s q L hb hs hq hsym i hi
    change e i + e (L-1-i) ≤ b-1 at hu
    exact ⟨by omega, by omega⟩
  change (stepDigits b (word e L)).reverse = stepDigits b (word e L)
  simp only [stepDigits, pairs_word, normalize_low b _ L low]
  apply word_symmetric
  intro i hi
  have hm : L-1-(L-1-i) = i := by omega
  simp only [hm, Int.add_comm]

#print axioms normalized_preserves_carry
#print axioms normalized_next_low
#print axioms normalized_center_even
#print axioms normalized_two_step_palindrome
end Agent421NoOverflow
