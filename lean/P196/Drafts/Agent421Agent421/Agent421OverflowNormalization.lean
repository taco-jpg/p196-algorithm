import P196.Drafts.Agent421Agent421.Agent421NoOverflow

namespace Agent421Overflow
open SignedDigitUniqueness BaseReflection ResetNormalization PhysicalWidth ReverseAdd Agent11HighBase Agent421NoOverflow

/-- The low-zero normalization required in the overflowing branch. -/
def norm (b s u v : Int) : Int :=
  if u = v then if u = 0 then 0 else b+s-1 else b-1

theorem norm_symmetric (b s u v : Int) : norm b s u v = norm b s v u := by
  unfold norm
  by_cases h : u = v
  · subst v; rfl
  · simp [h, Ne.symm h]

theorem norm_local (b s x a c : Int) (hb : 2 ≤ b)
    (hs : 1 ≤ s ∧ s ≤ b-1) (hx : 0 ≤ x ∧ x ≤ 2*b-2)
    (ha : 0 ≤ a ∧ a ≤ 1) (hc : 0 ≤ c ∧ c ≤ 1) :
    let u := (x+a)/b
    let v := (x+c)/b
    (norm b s u v+a)/b = u ∧ (norm b s u v+c)/b = v := by
  dsimp
  have hu := carry_bit b x a hb hx ha
  by_cases he : (x+a)/b = (x+c)/b
  · rcases hu with hu | hu
    · have hv : (x+c)/b = 0 := by omega
      have da := low_divmod b a ha.1 (by omega)
      have dc := low_divmod b c hc.1 (by omega)
      simp only [norm, hu, hv, ↓reduceIte, Int.zero_add, da.1, dc.1, and_self]
    · have hv : (x+c)/b = 1 := by omega
      have da := high_divmod b (b+s-1+a) hb (by omega)
      have dc := high_divmod b (b+s-1+c) hb (by omega)
      simp only [norm, hu, hv, Int.reduceEq, ↓reduceIte, da.1, dc.1, and_self]
  · have hn := unequal_carries b x a c hb hx ha hc he
    have hn' : norm b s ((x+a)/b) ((x+c)/b) = x := by
      simp only [norm, he, ↓reduceIte]; omega
    rw [hn']
    exact ⟨rfl,rfl⟩

theorem norm_range (b s u v : Int) (hb : 2 ≤ b) (hs : 1 ≤ s ∧ s ≤ b-1) :
    0 ≤ norm b s u v ∧ norm b s u v ≤ 2*b-2 := by
  unfold norm; split
  · split <;> omega
  · omega

theorem norm_center_even (b s u : Int) (he : (b+s-1)%2 = 0) :
    norm b s u u % 2 = 0 := by
  simp only [norm, ↓reduceIte]
  split <;> simp_all

def normalized (b s : Int) (q : Nat → Int) (L i : Nat) : Int :=
  norm b s (carry b q (i+1)) (carry b q (L-i))

theorem normalized_symmetric (b s : Int) (q : Nat → Int) (L i : Nat) (hi : i < L) :
    normalized b s q L i = normalized b s q L (L-1-i) := by
  have h1 : L-1-i+1 = L-i := by omega
  have h2 : L-(L-1-i) = i+1 := by omega
  simp only [normalized, h1, h2]
  exact norm_symmetric b s _ _

theorem normalized_center_even (b s : Int) (q : Nat → Int) (L i : Nat)
    (he : (b+s-1)%2 = 0) (hi : i < L) (hc : i = L-1-i) :
    normalized b s q L i % 2 = 0 := by
  have h : L-i = i+1 := by omega
  simp only [normalized,h]
  exact norm_center_even b s _ he

theorem normalized_preserves_carry (b s : Int) (q : Nat → Int) (L : Nat)
    (hb : 2 ≤ b) (hs : 1 ≤ s ∧ s ≤ b-1)
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
      (hq i (by omega)) (carry_bounded b q L hb hq i (by omega))
      (carry_bounded b q L hb hq (L-1-i) (by omega))
    have hout : (q i + carry b q (L-1-i))/b = carry b q (L-i) := by
      rw [hsym i (by omega), ← hf]
      rfl
    dsimp at hl
    rw [hout] at hl
    change (normalized b s q L i + carry b (normalized b s q L) i)/b = carry b q (i+1)
    rw [ih (by omega)]
    exact hl.1

theorem normalized_outer_cases (b s : Int) (q : Nat → Int) (L : Nat)
    (hb : 2 ≤ b) (hL : 0 < L)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hover : carry b q L = 1) :
    normalized b s q L 0 = b+s-1 ∨ normalized b s q L 0 = b-1 := by
  have hc := carry_bounded b q L hb hq 1 (by omega)
  have hc' : carry b q 1 = 0 ∨ carry b q 1 = 1 := by omega
  rcases hc' with hc' | hc'
  · right; simp [normalized, norm, hover, hc']
  · left; simp [normalized, norm, hover, hc']

/-- Positive same-width realization and complete first carry preservation for
all overflowing inputs, without assuming the missing protected-run argument. -/
theorem same_carries_realizable (b s : Int) (q : Nat → Int) (L : Nat)
    (hb : 2 ≤ b) (hs : 1 ≤ s ∧ s ≤ b-1) (he : (b+s-1)%2 = 0)
    (hL : 0 < L) (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i)) (hover : carry b q L = 1) :
    ∃ d : List Int, d.length = L ∧ DigitBounds b d ∧ PositiveLast d ∧
      0 < eval b d ∧ pairs d = word (normalized b s q L) L ∧
      (∀ i, i ≤ L → terminal b 0 (tags ((pairs d).take i)) = carry b q i) := by
  let r := normalized b s q L
  have ho := normalized_outer_cases b s q L hb hL hq hover
  have hr : ∀ i, i < L → 0 ≤ r i ∧ r i ≤ 2*b-2 := by
    intro i _; exact norm_range b s _ _ hb hs
  have hp : 0 < r 0 := by
    change 0 < normalized b s q L 0
    rcases ho with ho | ho <;> rw [ho] <;> omega
  obtain ⟨d, hlen, hd, hpos, hnum, hpair⟩ := valid_word_realizable b r L hb hL hp hr
    (normalized_symmetric b s q L) (fun i hi hc => normalized_center_even b s q L i he hi hc)
  refine ⟨d, hlen, hd, hpos, hnum, hpair, ?_⟩
  intro i hi
  rw [hpair]
  have htake : (word r L).take i = word r i := by
    apply List.ext_getElem (by simp [Nat.min_eq_left hi])
    intro j hj hk
    have hji : j < i := by simpa using hk
    have hjL : j < L := by omega
    simp only [List.getElem_take]
    rw [word_get r L j hjL, word_get r i j hji]
  rw [htake, terminal_word]
  exact normalized_preserves_carry b s q L hb hs hq hsym i hi

#print axioms norm_local
#print axioms normalized_preserves_carry
#print axioms same_carries_realizable
end Agent421Overflow
