import P196.Drafts.Agent421Agent421.Agent421OverflowClock

namespace Agent421Overflow
open SignedDigitUniqueness BaseReflection ResetNormalization PhysicalWidth ReverseAdd Agent11HighBase Agent421NoOverflow

/-- The actual last carry of an ordinary reverse-add step on canonical digits. -/
def finalCarry (b : Int) (d : List Int) : Int := terminal b 0 (tags (pairs d))

theorem stepDigits_length (b : Int) (d : List Int) (hb : 2 ≤ b)
    (hd : DigitBounds b d) (hp : PositiveLast d) :
    (stepDigits b d).length = d.length + (finalCarry b d).toNat := by
  have h := reverse_add_normalization b d (tags (pairs d)) hb hd hp (tags_projection _)
  simpa only [stepDigits, normalize, tags_ordinary, finalCarry] using h.2.2.1

theorem next_carry_exact (b : Int) (q : Nat → Int) (L : Nat)
    (hc : carry b q L = 1) :
    terminal b 0 (tags (nextPairs b (word q L))) = carry b (nextSeq b q L) (L+1) := by
  rw [← nextSeq_word b q L hc, terminal_word]

/-- A same-width, same-carry positive integer representative with its exact
canonical overflow schedule and corresponding actual output widths. This is
not an abstract-clock premise: the digits are explicitly realized, and each
step satisfies the repository's integer reverse-add semantics. -/
theorem same_carries_actual_schedule (b s : Int) (q : Nat → Int) (L : Nat)
    (hb : 3 ≤ b) (hs : 1 ≤ s ∧ s ≤ b-2) (he : (b+s-1)%2 = 0)
    (hL : 0 < L) (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i)) (hc : carry b q L = 1) :
    ∃ d : List Int, d.length = L ∧ DigitBounds b d ∧ PositiveLast d ∧ 0 < eval b d ∧
      (∀ i, i ≤ L → terminal b 0 (tags ((pairs d).take i)) = carry b q i) ∧
      let d1 := stepDigits b d
      let d2 := stepDigits b d1
      let d3 := stepDigits b d2
      DigitBounds b d1 ∧ PositiveLast d1 ∧ DigitBounds b d2 ∧ PositiveLast d2 ∧
      DigitBounds b d3 ∧ PositiveLast d3 ∧
      eval b d1 = eval b d + reversedValue b d ∧
      eval b d2 = eval b d1 + reversedValue b d1 ∧
      eval b d3 = eval b d2 + reversedValue b d2 ∧
      finalCarry b d = 1 ∧ d1.length = L+1 ∧
      ((finalCarry b d1 = 0 ∧ d2.length = L+1) ∨
       (finalCarry b d1 = 1 ∧ finalCarry b d2 = 0 ∧
        d2.length = L+2 ∧ d3.length = L+2)) := by
  obtain ⟨d, hlen, hd, hp, hn, hpair, htrace⟩ :=
    same_carries_realizable b s q L (by omega) (by omega) he hL hq hsym hc
  let r := normalized b s q L
  have hclock := normalized_outer_clock b s q L hb hs hL hq hsym hc
  have hr : carry b r L = 1 := hclock.1
  have h0 : finalCarry b d = 1 := by
    simp only [finalCarry, hpair, terminal_word]
    exact hr
  have h1 := stepDigits_semantics b d (by omega) hd hp
  have h2 := stepDigits_semantics b (stepDigits b d) (by omega) h1.1 h1.2.1
  have h3 := stepDigits_semantics b (stepDigits b (stepDigits b d)) (by omega) h2.1 h2.2.1
  have hl1 := stepDigits_length b d (by omega) hd hp
  rw [hlen,h0] at hl1
  have hl1' : (stepDigits b d).length = L+1 := by simpa using hl1
  have hc1 : finalCarry b (stepDigits b d) = carry b (nextSeq b r L) (L+1) := by
    change terminal b 0 (tags (pairs (normalize b (pairs d)))) = _
    rw [hpair]
    exact next_carry_exact b r L hr
  refine ⟨d, hlen, hd, hp, hn, htrace, h1.1, h1.2.1, h2.1, h2.2.1,
    h3.1, h3.2.1, h1.2.2, h2.2.2, h3.2.2, h0, hl1', ?_⟩
  rcases hclock.2 with ⟨_,_,hn1⟩ | ⟨_,_,ho1,_,hn2⟩
  · have hn1' : finalCarry b (stepDigits b d) = 0 := hc1.trans hn1
    have hl2 := stepDigits_length b (stepDigits b d) (by omega) h1.1 h1.2.1
    rw [hn1', hl1'] at hl2
    exact Or.inl ⟨hn1', by simpa using hl2⟩
  · have ho1' : finalCarry b (stepDigits b d) = 1 := hc1.trans ho1
    have hc2 : finalCarry b (stepDigits b (stepDigits b d)) =
        carry b (nextSeq b (nextSeq b r L) (L+1)) (L+2) := by
      change terminal b 0 (tags (nextPairs b (pairs (stepDigits b d)))) = _
      have hp1 : pairs (stepDigits b d) = word (nextSeq b r L) (L+1) := by
        change nextPairs b (pairs d) = _
        rw [hpair]
        exact (nextSeq_word b r L hr).symm
      rw [hp1]
      exact next_carry_exact b (nextSeq b r L) (L+1) ho1
    have hn2' : finalCarry b (stepDigits b (stepDigits b d)) = 0 := hc2.trans hn2
    have hl2 := stepDigits_length b (stepDigits b d) (by omega) h1.1 h1.2.1
    rw [ho1', hl1'] at hl2
    have hl2' : (stepDigits b (stepDigits b d)).length = L+2 := by simpa [Nat.add_assoc] using hl2
    have hl3 := stepDigits_length b (stepDigits b (stepDigits b d)) (by omega) h2.1 h2.2.1
    rw [hn2', hl2'] at hl3
    exact Or.inr ⟨ho1', hn2', hl2', by simpa using hl3⟩

/-- Exact specialization to the original written theorem's base ranges. -/
theorem source_bases_actual_schedule (b : Int) (q : Nat → Int) (L : Nat)
    (hb : (10 ≤ b ∧ b%2 = 0) ∨ (17 ≤ b ∧ b%2 = 1))
    (hL : 0 < L) (hq : ∀ i, i < L → 0 ≤ q i ∧ q i ≤ 2*b-2)
    (hsym : ∀ i, i < L → q i = q (L-1-i)) (hc : carry b q L = 1) :
    ∃ d : List Int, d.length = L ∧ DigitBounds b d ∧ PositiveLast d ∧ 0 < eval b d ∧
      (∀ i, i ≤ L → terminal b 0 (tags ((pairs d).take i)) = carry b q i) ∧
      finalCarry b d = 1 ∧
      (finalCarry b (stepDigits b d) = 0 ∨
       (finalCarry b (stepDigits b d) = 1 ∧ finalCarry b (stepDigits b (stepDigits b d)) = 0)) := by
  have h : ∃ s : Int, 1 ≤ s ∧ s ≤ b-2 ∧ (b+s-1)%2 = 0 := by
    rcases hb with hb | hb
    · exact ⟨1, by omega, by omega, by omega⟩
    · exact ⟨2, by omega, by omega, by omega⟩
  obtain ⟨s,hs1,hs2,he⟩ := h
  obtain ⟨d,hlen,hd,hp,hn,htrace,hrest⟩ :=
    same_carries_actual_schedule b s q L (by omega) ⟨hs1,hs2⟩ he hL hq hsym hc
  dsimp at hrest
  rcases hrest with ⟨_,_,_,_,_,_,_,_,_,h0,_,hschedule⟩
  refine ⟨d,hlen,hd,hp,hn,htrace,h0,?_⟩
  rcases hschedule with ⟨h1,_⟩ | ⟨h1,h2,_,_⟩
  · exact Or.inl h1
  · exact Or.inr ⟨h1,h2⟩

#print axioms same_carries_actual_schedule
#print axioms source_bases_actual_schedule
end Agent421Overflow
