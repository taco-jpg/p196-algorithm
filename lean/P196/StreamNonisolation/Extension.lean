import P196.StreamNonisolation.Append
import P196.TrimmedStreamObservation.WidthRecovery

/-!
# Arbitrarily deep canonical extensions with fixed finite observations

Append phase letters and then one carry-preserving nonphase letter. The
phase letters preserve both complete observations, while the final letter
cannot be seen before its position. The resulting word is already trimmed
and can have arbitrarily large width, even when the initial word is empty.
-/

namespace Agent5.StreamNonisolation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- A phase-padded word terminated by the next natural coefficient. -/
def extendWord (c : Nat) (B : List Nat) (m : Nat) : List Nat :=
  (B ++ List.replicate m c) ++ [c + 1]

theorem extendWord_length (c : Nat) (B : List Nat) (m : Nat) :
    (extendWord c B m).length = B.length + m + 1 := by
  simp [extendWord, Nat.add_assoc]

private theorem nonneutral_bounds (c : Nat) (hc : nonneutralPhase c) :
    0 < c ∧ c ≤ 16 := by
  simp [nonneutralPhase] at hc
  omega

private theorem next_letter_carry (c : Nat) (hc : nonneutralPhase c) :
    (c + 1 + (if 10 ≤ c then 1 else 0)) / 10 =
      (if 10 ≤ c then 1 else 0) := by
  simp [nonneutralPhase] at hc
  rcases hc with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide

private theorem padded_bound (c : Nat) (B : List Nat) (m : Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    ∀ x ∈ B ++ List.replicate m c, x ≤ 18 := by
  intro x hx
  rcases List.mem_append.mp hx with hx | hx
  · exact hB x hx
  · rw [List.eq_of_mem_replicate hx]
    have := (nonneutral_bounds c hc).2
    omega

/-- The final letter differs from the phase, so maximal phase-suffix removal
does not shorten the extension, for any natural phase. -/
theorem extendWord_canonical (c : Nat) (B : List Nat) (m : Nat) :
    stripSuffix c (extendWord c B m) = extendWord c B m := by
  have hne : c + 1 ≠ c := by omega
  simp [extendWord, stripSuffix, List.reverse_append, List.dropWhile_cons, hne]

/-- The extension is valid under the original validity predicate. Both the
empty starting word and zero padding are included. -/
theorem extendWord_valid (c : Nat) (B : List Nat) (m : Nat)
    (hc : nonneutralPhase c)
    (hv : validOuter { c := c, B := B } = true) :
    validOuter { c := c, B := extendWord c B m } = true := by
  have hcf := nonneutral_bounds c hc
  have hd : c + 1 ≤ 18 := by omega
  have hne : c + 1 ≠ c := by omega
  have hb := padded_bound c B m hc (entries_le_of_valid c B hv)
  have hall : ∀ x ∈ extendWord c B m, x ≤ 18 := by
    intro x hx
    change x ∈ (B ++ List.replicate m c) ++ [c + 1] at hx
    rcases List.mem_append.mp hx with hx | hx
    · exact hb x hx
    · have heq : x = c + 1 := by simpa using hx
      simpa [heq] using hd
  simp only [validOuter, Bool.and_eq_true, List.all_eq_true,
    decide_eq_true_eq]
  refine ⟨⟨hall, ?_⟩, ?_⟩
  · cases B with
    | nil =>
        cases m with
        | zero => simp [extendWord]
        | succ m => simp [extendWord, List.replicate_succ, hcf.1]
    | cons a tail =>
        have ha : 0 < a := by
          simp only [validOuter, Bool.and_eq_true, decide_eq_true_eq] at hv
          exact hv.1.2
        simpa [extendWord] using ha
  · simp [extendWord, List.getLast?_append, hne]

/-- A sufficiently deep extension preserves the calculated high carry and
both original finite observations. -/
theorem extendWord_same_prefixes (c cut m : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18)
    (hcut : cut ≤ B.length + m) :
    (normalize (extendWord c B m).reverse (if 10 ≤ c then 1 else 0)).2 =
        (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 ∧
      adicNumeratorDigits cut (zValue c (extendWord c B m) - (c : Int)) =
        adicNumeratorDigits cut (zValue c B - (c : Int)) ∧
      fractionDigits cut (rhoNum c (extendWord c B m))
          (9 * 10 ^ (extendWord c B m).length *
            10 ^ (normalize (extendWord c B m).reverse
              (if 10 ≤ c then 1 else 0)).2) =
        fractionDigits cut (rhoNum c B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2) := by
  have hlen : cut ≤ (B ++ List.replicate m c).length := by simpa using hcut
  have hcarry := next_letter_carry c hc
  have hd : c + 1 ≤ 18 := by have := (nonneutral_bounds c hc).2; omega
  constructor
  · change (normalize ((B ++ List.replicate m c) ++ [c + 1]).reverse _).2 = _
    rw [append_high_carry c (B ++ List.replicate m c) (c + 1) hcarry]
    exact Agent5.TrimmedStreamObservation.phase_padding_carry c B m hc
  constructor
  · change adicNumeratorDigits cut
      (zValue c ((B ++ List.replicate m c) ++ [c + 1]) - (c : Int)) = _
    rw [append_low_prefix c cut (B ++ List.replicate m c) (c + 1) hlen]
    exact Agent5.TrimmedStreamObservation.phase_padding_low c cut B m
  · change fractionDigits cut (rhoNum c ((B ++ List.replicate m c) ++ [c + 1]))
      (9 * 10 ^ ((B ++ List.replicate m c) ++ [c + 1]).length *
        10 ^ (normalize ((B ++ List.replicate m c) ++ [c + 1]).reverse
          (if 10 ≤ c then 1 else 0)).2) = _
    rw [append_high_prefix c cut (B ++ List.replicate m c) (c + 1)
      hc (padded_bound c B m hc hB) hd hcarry hlen]
    exact Agent5.TrimmedStreamObservation.phase_padding_high c cut B m hc

/-- No finite observation isolates any valid canonical state among
unrestricted widths, even when its phase and outgoing high carry are known.
There is always a strictly longer valid canonical alternative, beyond any
specified lower width, with the same two literal observed prefixes. -/
theorem arbitrarily_wide_valid_same_prefixes
    (c cut W : Nat) (B : List Nat)
    (hc : nonneutralPhase c)
    (hv : validOuter { c := c, B := B } = true) :
    ∃ B' : List Nat,
      validOuter { c := c, B := B' } = true ∧
      stripSuffix c B' = B' ∧
      max B.length W < B'.length ∧
      (normalize B'.reverse (if 10 ≤ c then 1 else 0)).2 =
        (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 ∧
      adicNumeratorDigits cut (zValue c B' - (c : Int)) =
        adicNumeratorDigits cut (zValue c B - (c : Int)) ∧
      fractionDigits cut (rhoNum c B')
          (9 * 10 ^ B'.length *
            10 ^ (normalize B'.reverse (if 10 ≤ c then 1 else 0)).2) =
        fractionDigits cut (rhoNum c B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2) := by
  refine ⟨extendWord c B (max cut W), extendWord_valid c B _ hc hv,
    extendWord_canonical c B _, ?_, ?_⟩
  · rw [extendWord_length]
    have := Nat.le_max_right cut W
    omega
  · apply extendWord_same_prefixes c cut (max cut W) B hc (entries_le_of_valid c B hv)
    have := Nat.le_max_left cut W
    omega

#print axioms extendWord_length
#print axioms extendWord_canonical
#print axioms extendWord_valid
#print axioms extendWord_same_prefixes
#print axioms arbitrarily_wide_valid_same_prefixes

end Agent5.StreamNonisolation
