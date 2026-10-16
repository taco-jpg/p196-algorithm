import Lychrel196Research
import resume_renewal_certificate

namespace OverflowCarryNormalization
open DecimalDigits FoldedDecimal

/-- Overflow normalization uses0,9,10; low2 from the older no-overflow
normalization does not have the same four-step termination property. -/
def normZero (a b : Nat) : Nat := if a = b then if a = 0 then 0 else 10 else 9

theorem normZero_local (x a b : Nat) (hx : x ≤ 18) (ha : a ≤ 1) (hb : b ≤ 1) :
    let u := (x + a) / 10
    let v := (x + b) / 10
    (normZero u v + a) / 10 = u ∧
    (normZero u v + b) / 10 = v := by
  dsimp
  unfold normZero
  split <;> rename_i h
  · split <;> omega
  · omega

theorem normZero_symmetric (a b : Nat) : normZero a b = normZero b a := by
  unfold normZero
  by_cases h : a = b
  · subst b; simp
  · simp [h, Ne.symm h]

theorem normZero_bounded (a b : Nat) : normZero a b ≤ 10 := by
  unfold normZero
  split <;> simp_all
  split <;> omega

def normalizedZero (q : Nat → Nat) (L i : Nat) : Nat :=
  normZero (carry q (i + 1)) (carry q (L - i))

theorem normalizedZero_preserves_carry (q : Nat → Nat) (L : Nat)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i)) :
    ∀ i, i ≤ L → carry (normalizedZero q L) i = carry q i := by
  intro i
  induction i with
  | zero => intro _; rfl
  | succ i ih =>
    intro hi
    have hf : L - 1 - i + 1 = L - i := by omega
    have hlocal := normZero_local (q i) (carry q i) (carry q (L - 1 - i))
      (hq i (by omega))
      (carry_bounded q L hq i (by omega))
      (carry_bounded q L hq (L - 1 - i) (by omega))
    have hout : (q i + carry q (L - 1 - i)) / 10 = carry q (L - i) := by
      rw [hs i (by omega), ← hf]
      rfl
    dsimp at hlocal
    rw [hout] at hlocal
    change (normalizedZero q L i + carry (normalizedZero q L) i) / 10 = carry q (i + 1)
    rw [ih (by omega)]
    exact hlocal.1

theorem normalizedZero_symmetric (q : Nat → Nat) (L i : Nat) (hi : i < L) :
    normalizedZero q L i = normalizedZero q L (L - 1 - i) := by
  have h1 : L - 1 - i + 1 = L - i := by omega
  have h2 : L - (L - 1 - i) = i + 1 := by omega
  simp only [normalizedZero, h1, h2]
  exact normZero_symmetric _ _

theorem normalizedZero_outer (q : Nat → Nat) (L : Nat)
    (hc : carry q L = 1) :
    normalizedZero q L 0 = 9 ∨ normalizedZero q L 0 = 10 := by
  by_cases h : carry q (0+1) = 1
  · simp [normalizedZero,h,hc,normZero]
  · simp [normalizedZero,h,hc,normZero]

theorem normalizedZero_admissible (q : Nat → Nat) (L : Nat)
    (hL : 0 < L) (hc : carry q L = 1) :
    Admissible L (normalizedZero q L) := by
  refine ⟨hL, ?_, ?_, ?_, ?_⟩
  · have := normalizedZero_outer q L hc; omega
  · intro i hi
    exact Nat.le_trans (normZero_bounded _ _) (by decide)
  · exact normalizedZero_symmetric q L
  · intro i hi hm
    have heq : L - i = i + 1 := by omega
    simp only [normalizedZero, heq, normZero, if_true]
    split <;> decide

/-- Every overflowing carryword has a genuine finite normalized integer.
The four-step palindrome claim is proved by the separate graph bridge. -/
theorem normalizedZero_realizable (q : Nat → Nat) (L : Nat)
    (hL : 0 < L)
    (hq : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i))
    (hc : carry q L = 1) :
    ∃ n d, 0 < n ∧ Canonical n d L ∧
      (∀ i, i < L → columnSum d L i = normalizedZero q L i) ∧
      (∀ i, i ≤ L → carry (columnSum d L) i = carry q i) := by
  have had := normalizedZero_admissible q L hL hc
  obtain ⟨n, d, hn, hcan, hrep⟩ := valid_word_realizable (normalizedZero q L) L
    had.1 had.2.1 had.2.2.1 had.2.2.2.1 had.2.2.2.2
  refine ⟨n,d,hn,hcan,hrep,?_⟩
  intro i hi
  exact (carry_congr_upto _ _ L hrep i hi).trans
    (normalizedZero_preserves_carry q L hq hs i hi)

/-- Local input-automaton edge. It justifies the certificate's four-state
recognizer directly from the two physical carry equations. -/
theorem normZero_input_edge (x a bn : Nat)
    (hx : x ≤ 18) (ha : a ≤ 1) (hb : bn ≤ 1) :
    let an := (x+a)/10
    let b := (x+bn)/10
    (normZero an b, an + 2*bn) ∈
      OverflowNormalizationCertificate.normEdges (a+2*b) := by
  have han : (x+a)/10 ≤ 1 := by omega
  have hbo : (x+bn)/10 ≤ 1 := by omega
  have ha' : a=0 ∨ a=1 := by omega
  have hb' : bn=0 ∨ bn=1 := by omega
  have hn' : (x+a)/10=0 ∨ (x+a)/10=1 := by omega
  have ho' : (x+bn)/10=0 ∨ (x+bn)/10=1 := by omega
  dsimp
  rcases ha' with ha'|ha' <;> rcases hb' with hb'|hb' <;>
    rcases hn' with hn'|hn' <;> rcases ho' with ho'|ho' <;>
    simp only [hn',ho',ha',hb',normZero,OverflowNormalizationCertificate.normEdges] <;>
    simp_all <;> omega

/-- A physical normalized folded pair follows exactly an input-automaton edge. -/
theorem normalizedZero_folded_edge (q : Nat → Nat) (L i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18)
    (hs : ∀ j, j < L → q j = q (L - 1 - j))
    (hi : i < L) :
    (normalizedZero q L i,
      carry (normalizedZero q L) (i+1) +
        2*carry (normalizedZero q L) (L-(i+1))) ∈
      OverflowNormalizationCertificate.normEdges
        (carry (normalizedZero q L) i +
          2*carry (normalizedZero q L) (L-i)) := by
  have hf : L - 1 - i + 1 = L - i := by omega
  have hout : (q i + carry q (L-1-i))/10 = carry q (L-i) := by
    rw [hs i hi, ← hf]
    rfl
  have he := normZero_input_edge (q i) (carry q i) (carry q (L-1-i))
    (hq i hi) (carry_bounded q L hq i (by omega))
    (carry_bounded q L hq (L-1-i) (by omega))
  dsimp at he
  rw [hout] at he
  change (normalizedZero q L i, carry q (i+1) + 2*carry q (L-1-i)) ∈
    OverflowNormalizationCertificate.normEdges (carry q i + 2*carry q (L-i)) at he
  rw [normalizedZero_preserves_carry q L hq hs (i+1) (by omega),
    normalizedZero_preserves_carry q L hq hs (L-(i+1)) (by omega),
    normalizedZero_preserves_carry q L hq hs i (by omega),
    normalizedZero_preserves_carry q L hq hs (L-i) (by omega)]
  have hind : L-(i+1)=L-1-i := by omega
  simpa only [hind] using he

/-- The normalized odd center is exactly ten times its high carry. -/
theorem normalizedZero_odd_center (q : Nat → Nat) (k : Nat)
    (hq : ∀ j, j < 2*k+1 → q j ≤ 18)
    (hs : ∀ j, j < 2*k+1 → q j = q (2*k+1-1-j)) :
    normalizedZero q (2*k+1) k =
      10*carry (normalizedZero q (2*k+1)) (2*k+1-k) := by
  have hind : 2*k+1-k=k+1 := by omega
  rw [normalizedZero_preserves_carry q (2*k+1) hq hs _ (by omega)]
  simp only [normalizedZero,hind,normZero,if_true]
  have hc := carry_bounded q (2*k+1) hq (k+1) (by omega)
  split <;> omega


#print axioms normalizedZero_realizable
#print axioms normZero_input_edge
end OverflowCarryNormalization
