import P196.UniversalPhasePrefixes.Relay
import P196.StreamNonisolation.Append
import P196.TrimmedStreamObservation.WidthRecovery

/-!
# One canonical word compatible with every nonneutral phase

A final coefficient transfers any alternative phase's incoming carry to
the original phase's carry. Phase padding puts that coefficient beyond
the observed window. The final coefficient is odd, so the same word is
already canonical at every permitted even phase.
-/

namespace Agent5.UniversalPhasePrefixes

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- An odd terminal coefficient that restores the target phase's carry. -/
def relayLetter (c : Nat) : Nat :=
  1 + 10 * (if 10 ≤ c then 1 else 0)

/-- This word is independent of the alternative phase. -/
def universalWord (c : Nat) (B : List Nat) (m : Nat) : List Nat :=
  (B ++ List.replicate m c) ++ [relayLetter c]

private theorem relayLetter_cases (c : Nat) :
    relayLetter c = 1 ∨ relayLetter c = 11 := by
  by_cases h : 10 ≤ c <;> simp [relayLetter, h]

private theorem relayLetter_carry (c d : Nat) :
    (relayLetter c + (if 10 ≤ d then 1 else 0)) / 10 =
      (if 10 ≤ c then 1 else 0) := by
  by_cases hc : 10 ≤ c <;> by_cases hd : 10 ≤ d <;>
    simp [relayLetter, hc, hd]

private theorem relayLetter_ne_phase (c d : Nat) (hd : nonneutralPhase d) :
    relayLetter c ≠ d := by
  have he := relayLetter_cases c
  simp [nonneutralPhase] at hd
  omega

private theorem phase_bounds (c : Nat) (hc : nonneutralPhase c) :
    0 < c ∧ c ≤ 16 := by
  simp [nonneutralPhase] at hc
  omega

private theorem padded_bound (c : Nat) (B : List Nat) (m : Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    ∀ x ∈ B ++ List.replicate m c, x ≤ 18 := by
  intro x hx
  rcases List.mem_append.mp hx with hx | hx
  · exact hB x hx
  · rw [List.eq_of_mem_replicate hx]
    have := (phase_bounds c hc).2
    omega

theorem universalWord_length (c : Nat) (B : List Nat) (m : Nat) :
    (universalWord c B m).length = B.length + m + 1 := by
  simp [universalWord, Nat.add_assoc]

/-- The same word is maximally trimmed at every nonneutral phase. -/
theorem universalWord_canonical (c d : Nat) (B : List Nat) (m : Nat)
    (hd : nonneutralPhase d) :
    stripSuffix d (universalWord c B m) = universalWord c B m := by
  have hne := relayLetter_ne_phase c d hd
  simp [universalWord, stripSuffix, List.reverse_append, List.dropWhile_cons, hne]

/-- The word is valid at every alternative phase, including when the
original valid word is empty and no phase padding is requested. -/
theorem universalWord_valid (c d : Nat) (B : List Nat) (m : Nat)
    (hc : nonneutralPhase c) (hd : nonneutralPhase d)
    (hv : validOuter { c := c, B := B } = true) :
    validOuter { c := d, B := universalWord c B m } = true := by
  have hcf := phase_bounds c hc
  have he := relayLetter_cases c
  have hepos : 0 < relayLetter c := by omega
  have he18 : relayLetter c ≤ 18 := by omega
  have hne := relayLetter_ne_phase c d hd
  have hb := padded_bound c B m hc (entries_le_of_valid c B hv)
  have hall : ∀ x ∈ universalWord c B m, x ≤ 18 := by
    intro x hx
    change x ∈ (B ++ List.replicate m c) ++ [relayLetter c] at hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hb x hx
    · have heq : x = relayLetter c := by simpa using hx
      simpa [heq] using he18
  simp only [validOuter, Bool.and_eq_true, List.all_eq_true, decide_eq_true_eq]
  refine ⟨⟨hall, ?_⟩, ?_⟩
  · cases B with
    | nil =>
        cases m with
        | zero => simp [universalWord, hepos]
        | succ m => simp [universalWord, List.replicate_succ, hcf.1]
    | cons a tail =>
        have ha : 0 < a := by
          simp only [validOuter, Bool.and_eq_true, decide_eq_true_eq] at hv
          exact hv.1.2
        simpa [universalWord] using ha
  · simp [universalWord, List.getLast?_append, hne]

/-- Every alternative nonneutral phase gives the same original observed
prefixes and the same calculated high carry on this one common word. -/
theorem universalWord_same_prefixes (c d cut m : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hd : nonneutralPhase d)
    (hB : ∀ x ∈ B, x ≤ 18) (hcut : cut ≤ B.length + m) :
    (normalize (universalWord c B m).reverse (if 10 ≤ d then 1 else 0)).2 =
        (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 ∧
      adicNumeratorDigits cut (zValue d (universalWord c B m) - (d : Int)) =
        adicNumeratorDigits cut (zValue c B - (c : Int)) ∧
      fractionDigits cut (rhoNum d (universalWord c B m))
          (9 * 10 ^ (universalWord c B m).length *
            10 ^ (normalize (universalWord c B m).reverse
              (if 10 ≤ d then 1 else 0)).2) =
        fractionDigits cut (rhoNum c B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2) := by
  have hlen : cut ≤ (B ++ List.replicate m c).length := by simpa using hcut
  have hrelay := relayLetter_carry c d
  have he : relayLetter c ≤ 18 := by have := relayLetter_cases c; omega
  constructor
  · change (normalize ((B ++ List.replicate m c) ++ [relayLetter c]).reverse _).2 = _
    rw [relay_high_carry c d (B ++ List.replicate m c) (relayLetter c) hrelay]
    exact Agent5.TrimmedStreamObservation.phase_padding_carry c B m hc
  constructor
  · change adicNumeratorDigits cut
      (zValue d ((B ++ List.replicate m c) ++ [relayLetter c]) - (d : Int)) = _
    rw [Agent5.StreamNonisolation.append_low_prefix d cut
      (B ++ List.replicate m c) (relayLetter c) hlen]
    rw [low_prefix_phase_independent d c cut (B ++ List.replicate m c) hlen]
    exact Agent5.TrimmedStreamObservation.phase_padding_low c cut B m
  · change fractionDigits cut (rhoNum d ((B ++ List.replicate m c) ++ [relayLetter c]))
      (9 * 10 ^ ((B ++ List.replicate m c) ++ [relayLetter c]).length *
        10 ^ (normalize ((B ++ List.replicate m c) ++ [relayLetter c]).reverse
          (if 10 ≤ d then 1 else 0)).2) = _
    rw [relay_high_prefix c d cut (B ++ List.replicate m c) (relayLetter c)
      hc hd (padded_bound c B m hc hB) he hrelay hlen]
    exact Agent5.TrimmedStreamObservation.phase_padding_high c cut B m hc

/-- Around every valid target and beyond every lower width there is one
canonical word that reproduces the finite observations at all eight
nonneutral phases simultaneously, including the supplied actual high carry. -/
theorem arbitrarily_wide_all_phase_same_prefixes
    (c cut W : Nat) (B : List Nat)
    (hc : nonneutralPhase c)
    (hv : validOuter { c := c, B := B } = true) :
    ∃ A : List Nat,
      max B.length W < A.length ∧
      ∀ d : Nat, nonneutralPhase d →
        validOuter { c := d, B := A } = true ∧
        stripSuffix d A = A ∧
        (normalize A.reverse (if 10 ≤ d then 1 else 0)).2 =
          (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 ∧
        adicNumeratorDigits cut (zValue d A - (d : Int)) =
          adicNumeratorDigits cut (zValue c B - (c : Int)) ∧
        fractionDigits cut (rhoNum d A)
            (9 * 10 ^ A.length *
              10 ^ (normalize A.reverse (if 10 ≤ d then 1 else 0)).2) =
          fractionDigits cut (rhoNum c B)
            (9 * 10 ^ B.length *
              10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2) := by
  refine ⟨universalWord c B (max cut W), ?_, ?_⟩
  · rw [universalWord_length]
    have := Nat.le_max_right cut W
    omega
  · intro d hd
    refine ⟨universalWord_valid c d B _ hc hd hv,
      universalWord_canonical c d B _ hd, ?_⟩
    apply universalWord_same_prefixes c d cut (max cut W) B hc hd
      (entries_le_of_valid c B hv)
    have := Nat.le_max_left cut W
    omega

#print axioms universalWord_length
#print axioms universalWord_canonical
#print axioms universalWord_valid
#print axioms universalWord_same_prefixes
#print axioms arbitrarily_wide_all_phase_same_prefixes

end Agent5.UniversalPhasePrefixes
