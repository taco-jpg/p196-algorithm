import Agent107TransducerDefs

/-!
The literal transducer has exactly one complete finite carry path on every
admissible decimal pair word. The old folded-trace theorems determine both
carry directions; the literal transition then also determines the overflow,
started flag, and delayed high digit. No equality of irrelevant infinite
path tails is required or asserted.
-/

namespace Agent107.FoldedTransducer

open DecimalDigits FoldedDecimal

theorem actual_initial (L : Nat) (q : Nat → Nat)
    (hAd : Admissible L q) :
    actualState L q 0 = initial (carry q L) := by
  have hb := carry_bounded q L hAd.2.2.1 L (Nat.le_refl L)
  by_cases hz : carry q L = 0
  · simp [actualState, initial, hz, carry]
  · have ho : carry q L = 1 := by omega
    simp [actualState, initial, ho, extended, carry]

/-- Exact state update, including the signed delay sentinel. -/
theorem actual_nextState (L : Nat) (q : Nat → Nat)
    (hAd : Admissible L q) (i : Nat) (hi : i < L / 2) :
    actualState L q (i + 1) =
      nextState (actualState L q i) (q i) (actualState L q (i + 1)).high := by
  have hiL : i < L := by omega
  have hd := folded_delay_update q L i hiL hAd.2.2.2.1
  have hs : L - 1 - i = L - (i + 1) := by omega
  rw [hs] at hd
  simp only [actualState, nextState]
  rw [hd]
  simp [carry]

theorem actual_transition (L : Nat) (q : Nat → Nat)
    (hAd : Admissible L q) (i : Nat) (hi : i < L / 2) :
    Transition (actualState L q i) (q i) (actualState L q (i + 1)) := by
  have hiL : i < L := by omega
  refine ⟨hAd.2.2.1 i hiL, ?_, ?_, ?_, actual_nextState L q hAd i hi⟩
  · intro hfalse
    have hi0 : i = 0 := by
      by_contra hne
      have hp : 0 < i := by omega
      simp [actualState, hp] at hfalse
    simpa [hi0] using hAd.2.1
  · exact carry_bounded q L hAd.2.2.1 (L - (i + 1)) (by omega)
  · have hh := (folded_carry_transition q L i hiL hAd.2.2.2.1).2
    have hs : L - 1 - i = L - (i + 1) := by omega
    simpa only [actualState, hs] using hh.symm

theorem actual_terminal (L : Nat) (q : Nat → Nat)
    (hAd : Admissible L q) :
    Terminal (actualState L q (L / 2)) (inputCenter L q) := by
  have hL : 0 < L := hAd.1
  have hn : (actualState L q (L / 2)).started = true ∨
      0 < (inputCenter L q).getD 0 := by
    by_cases hk : 0 < L / 2
    · left
      simp [actualState, hk]
    · have he : L = 1 := by omega
      right
      simpa [inputCenter, he] using hAd.2.1
  refine ⟨hn, ?_⟩
  by_cases heven : L % 2 = 0
  · have he : L - L / 2 = L / 2 := by omega
    simp [inputCenter, heven, actualState, he]
  · have hk : L / 2 < L := by omega
    have he : L - 1 - L / 2 = L / 2 := by omega
    have hw : L = 2 * (L / 2) + 1 := by omega
    simp only [inputCenter, heven, if_false, actualState]
    refine ⟨hAd.2.2.1 _ hk, hAd.2.2.2.2 _ hk (by omega), ?_⟩
    have hc := odd_center_carry q (L / 2)
    simpa only [← hw] using hc.symm

/-- Every admissible finite decimal pair word has its actual accepting path. -/
theorem actual_accepts (L : Nat) (q : Nat → Nat)
    (hAd : Admissible L q) : Accepts L q (actualState L q) := by
  refine ⟨⟨carry q L, carry_bounded q L hAd.2.2.1 L (Nat.le_refl L),
    actual_initial L q hAd⟩, actual_transition L q hAd, actual_terminal L q hAd⟩

/-- Accepting the center forces both directional traces to be the actual
ones. This reuses the existing unrestricted even/odd folded-trace theorem. -/
theorem accepting_carries (L : Nat) (q : Nat → Nat) (p : Nat → State)
    (hAd : Admissible L q) (hp : Accepts L q p) :
    (∀ i, i ≤ L / 2 → (p i).low = carry q i) ∧
    (∀ i, i ≤ L / 2 → (p i).high = carry q (L - i)) := by
  obtain ⟨h, _, hstart⟩ := hp.1
  have hz : (p 0).low = 0 := by simp [hstart, initial]
  have hl : ∀ i, i < L / 2 →
      (p (i + 1)).low = (q i + (p i).low) / 10 := by
    intro i hi
    have he := congrArg State.low (hp.2.1 i hi).2.2.2.2
    simpa only [nextState] using he
  have hh : ∀ i, i < L / 2 →
      (p i).high = (q i + (p (i + 1)).high) / 10 := by
    intro i hi
    exact (hp.2.1 i hi).2.2.2.1.symm
  have ht := hp.2.2
  by_cases heven : L % 2 = 0
  · have hw : L = 2 * (L / 2) := by omega
    have hs : ∀ j, j < 2 * (L / 2) →
        q j = q (2 * (L / 2) - 1 - j) := by
      simpa only [← hw] using hAd.2.2.2.1
    simp only [Terminal, inputCenter, heven, if_true] at ht
    have hc := even_folded_trace_sound q (fun i => (p i).low)
      (fun i => (p i).high) (L / 2) hs hz hl hh ht.2
    exact ⟨hc.1, by simpa only [← hw] using hc.2.1⟩
  · have hw : L = 2 * (L / 2) + 1 := by omega
    have hs : ∀ j, j < 2 * (L / 2) + 1 →
        q j = q (2 * (L / 2) + 1 - 1 - j) := by
      simpa only [← hw] using hAd.2.2.2.1
    simp only [Terminal, inputCenter, heven, if_false] at ht
    have hc := odd_folded_trace_sound q (fun i => (p i).low)
      (fun i => (p i).high) (L / 2) hs hz hl hh ht.2.2.2.symm
    exact ⟨hc.1, by simpa only [← hw] using hc.2.1⟩

/-- Uniqueness is exactly on the consumed finite prefix, including its
terminal state. The unused tails of functions `p` remain unconstrained. -/
theorem accepting_state_eq_actual (L : Nat) (q : Nat → Nat)
    (p : Nat → State) (hAd : Admissible L q) (hp : Accepts L q p) :
    ∀ i, i ≤ L / 2 → p i = actualState L q i := by
  have hc := accepting_carries L q p hAd hp
  obtain ⟨h, _, hstart⟩ := hp.1
  have hh : h = carry q L := by
    have he := hc.2 0 (by omega)
    simpa only [hstart, initial, Nat.sub_zero] using he
  intro i
  induction i with
  | zero =>
      intro _
      rw [hstart, hh]
      exact (actual_initial L q hAd).symm
  | succ i ih =>
      intro hi
      have he := (hp.2.1 i (by omega)).2.2.2.2
      rw [he, ih (by omega)]
      have hh' : (p (i + 1)).high = (actualState L q (i + 1)).high :=
        hc.2 (i + 1) hi
      rw [hh']
      exact (actual_nextState L q hAd i (by omega)).symm

theorem accepting_finitePath_eq_actual (L : Nat) (q : Nat → Nat)
    (p : Nat → State) (hAd : Admissible L q) (hp : Accepts L q p) :
    finitePath L p = finitePath L (actualState L q) := by
  unfold finitePath
  congr 1
  funext i
  exact accepting_state_eq_actual L q p hAd hp i.val (by have := i.isLt; omega)

theorem accepting_finitePath_unique (L : Nat) (q : Nat → Nat)
    (p r : Nat → State) (hAd : Admissible L q)
    (hp : Accepts L q p) (hr : Accepts L q r) :
    finitePath L p = finitePath L r := by
  rw [accepting_finitePath_eq_actual L q p hAd hp,
    accepting_finitePath_eq_actual L q r hAd hr]

/-- There is exactly one actual finite trace, not one infinite extension. -/
theorem exists_unique_finitePath (L : Nat) (q : Nat → Nat)
    (hAd : Admissible L q) :
    ∃! xs : List State, ∃ p : Nat → State,
      Accepts L q p ∧ finitePath L p = xs := by
  refine ⟨finitePath L (actualState L q),
    ⟨actualState L q, actual_accepts L q hAd, rfl⟩, ?_⟩
  intro xs hx
  obtain ⟨p, hp, he⟩ := hx
  rw [← he]
  exact accepting_finitePath_eq_actual L q p hAd hp

#print axioms actual_accepts
#print axioms accepting_carries
#print axioms accepting_state_eq_actual
#print axioms accepting_finitePath_unique
#print axioms exists_unique_finitePath

end Agent107.FoldedTransducer
