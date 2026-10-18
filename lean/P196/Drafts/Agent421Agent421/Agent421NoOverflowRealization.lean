import P196.Drafts.Agent421Agent421.Agent421NoOverflowNormalization

namespace Agent421NoOverflow
open SignedDigitUniqueness BaseReflection ResetNormalization PhysicalWidth ReverseAdd Agent11HighBase

/-- The higher-place digit receives as much of each pair sum as a digit can hold. -/
def realizingDigit (b : Int) (q : Nat → Int) (L i : Nat) : Int :=
  if i < L-1-i then max (q i - (b-1)) 0
  else if L-1-i < i then min (q i) (b-1)
  else q i / 2

theorem realizingDigit_bounds (b : Int) (q : Nat → Int) (L : Nat) (hb : 2 ≤ b)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2) :
    ∀ i, i < L → 0 ≤ realizingDigit b q L i ∧ realizingDigit b q L i < b := by
  intro i hi
  have hqi := hq i hi
  unfold realizingDigit
  split
  · omega
  · split <;> omega

theorem realizingDigit_pairs (b : Int) (q : Nat → Int) (L : Nat)
    (hq : ∀ i, i < L → 0 ≤ q i)
    (hsym : ∀ i, i < L → q i = q (L-1-i))
    (hcenter : ∀ i, i < L → i = L-1-i → q i % 2 = 0) :
    ∀ i, i < L → realizingDigit b q L i + realizingDigit b q L (L-1-i) = q i := by
  intro i hi
  have hind : L-1-(L-1-i) = i := by omega
  have hsym' := hsym i hi
  have hqi := hq i hi
  simp only [realizingDigit, hind, ← hsym']
  by_cases hlo : i < L-1-i
  · have hhi : ¬L-1-i < i := by omega
    simp only [hlo, hhi, ↓reduceIte]
    omega
  · by_cases hhi : L-1-i < i
    · simp only [hlo, hhi, ↓reduceIte]
      omega
    · have heven := hcenter i hi (by omega)
      simp only [hlo, hhi, ↓reduceIte]
      omega

theorem realizingDigit_leading_positive (b : Int) (q : Nat → Int) (L : Nat)
    (hb : 2 ≤ b) (hL : 0 < L) (houter : 0 < q 0)
    (hsym : ∀ i, i < L → q i = q (L-1-i))
    (hcenter : ∀ i, i < L → i = L-1-i → q i % 2 = 0) :
    0 < realizingDigit b q L (L-1) := by
  have hind : L-1-(L-1) = 0 := by omega
  have hs0 : q (L-1) = q 0 := by simpa using (hsym 0 hL).symm
  simp only [realizingDigit, hind, hs0]
  by_cases hn : 1 < L
  · have hlo : ¬L-1 < 0 := by omega
    have hhi : 0 < L-1 := by omega
    simp only [hlo, hhi, ↓reduceIte]
    omega
  · have hone : L = 1 := by omega
    have heven := hcenter 0 hL (by omega)
    subst L
    simp only [Nat.sub_self, Nat.lt_irrefl, ↓reduceIte]
    omega

/-- Constructive same-width realization, including the single-digit center case. -/
theorem valid_word_realizable (b : Int) (q : Nat → Int) (L : Nat)
    (hb : 2 ≤ b) (hL : 0 < L) (houter : 0 < q 0)
    (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i))
    (hcenter : ∀ i, i < L → i = L-1-i → q i % 2 = 0) :
    ∃ d : List Int, d.length = L ∧ DigitBounds b d ∧ PositiveLast d ∧
      0 < eval b d ∧ pairs d = word q L := by
  let r := realizingDigit b q L
  have hd : DigitBounds b (word r L) := by
    intro x hx
    obtain ⟨i, hi, rfl⟩ := (word_mem r L x).mp hx
    exact realizingDigit_bounds b q L hb hq i hi
  have hp : PositiveLast (word r L) := word_positiveLast r L hL
    (realizingDigit_leading_positive b q L hb hL houter hsym hcenter)
  refine ⟨word r L, word_length r L, hd, hp, canonical_input_positive b _ hb hd hp, ?_⟩
  rw [pairs_word]
  apply word_ext
  intro i hi
  exact realizingDigit_pairs b q L (fun j hj => (hq j hj).1) hsym hcenter i hi

theorem stepDigits_semantics (b : Int) (d : List Int) (hb : 2 ≤ b)
    (hd : DigitBounds b d) (hp : PositiveLast d) :
    DigitBounds b (stepDigits b d) ∧ PositiveLast (stepDigits b d) ∧
      eval b (stepDigits b d) = eval b d + reversedValue b d := by
  have h := reverse_add_normalization b d (tags (pairs d)) hb hd hp (tags_projection _)
  exact ⟨h.1, h.2.1, h.2.2.2⟩

/-- Full no-overflow branch: positive same-width representative, complete first
carry trace preserved, and canonical second output palindromic. Arithmetic
identities for both actual reverse-add steps are included in the conclusion. -/
theorem same_carries_two_step_palindrome (b s : Int) (q : Nat → Int) (L : Nat)
    (hb : 7 ≤ b) (hs : 1 ≤ s ∧ 2*s ≤ b-1) (he : (b+s-1)%2 = 0)
    (hL : 0 < L) (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i)) (hover : carry b q L = 0) :
    ∃ d : List Int, d.length = L ∧ DigitBounds b d ∧ PositiveLast d ∧
      0 < eval b d ∧
      (∀ i, i ≤ L → terminal b 0 (tags (d |> pairs |>.take i)) = carry b q i) ∧
      DigitBounds b (stepDigits b d) ∧ PositiveLast (stepDigits b d) ∧
      DigitBounds b (stepDigits b (stepDigits b d)) ∧
      PositiveLast (stepDigits b (stepDigits b d)) ∧
      eval b (stepDigits b d) = eval b d + reversedValue b d ∧
      eval b (stepDigits b (stepDigits b d)) =
        eval b (stepDigits b d) + reversedValue b (stepDigits b d) ∧
      (stepDigits b (stepDigits b d)).reverse = stepDigits b (stepDigits b d) := by
  let r := normalized b s q L
  have hr : ∀ i, i < L → 0 ≤ r i ∧ r i ≤ 2*b-2 := by
    intro i _
    have h := normalized_range b s q L i hb hs
    change 0 ≤ normalized b s q L i ∧ normalized b s q L i ≤ 2*b-2
    exact ⟨by omega, h.2⟩
  obtain ⟨d, hlen, hd, hp, hn, hpair⟩ := valid_word_realizable b r L (by omega) hL
    (normalized_range b s q L 0 hb hs).1 hr
    (normalized_symmetric b s q L) (fun i hi hc => normalized_center_even b s q L i he hi hc)
  have hstep : stepDigits b d = normalize b (word r L) := by
    simp only [stepDigits, hpair]
  have h1 := stepDigits_semantics b d (by omega) hd hp
  have h2 := stepDigits_semantics b (stepDigits b d) (by omega) h1.1 h1.2.1
  refine ⟨d, hlen, hd, hp, hn, ?_, h1.1, h1.2.1, h2.1, h2.2.1, h1.2.2, h2.2.2, ?_⟩
  · intro i hi
    rw [hpair]
    -- Exact prefix/list carry correspondence is proved in the helper below.
    have htake : (word r L).take i = word r i := by
      apply List.ext_getElem (by simp [Nat.min_eq_left hi])
      intro j hj hk
      have hji : j < i := by simpa using hk
      have hjL : j < L := by omega
      simp only [List.getElem_take]
      rw [word_get r L j hjL, word_get r i j hji]
    rw [htake, terminal_word]
    exact normalized_preserves_carry b s q L hb hs hq hsym i hi
  · rw [hstep]
    exact normalized_two_step_palindrome b s q L hb hs hq hsym hover

#print axioms valid_word_realizable
#print axioms stepDigits_semantics
#print axioms same_carries_two_step_palindrome
end Agent421NoOverflow
