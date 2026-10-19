import P196.StreamObservationInjectivity.Values

/-!
Agent #5: phase and high-carry decoding from the original finite streams.

For a known exterior width n, the low numerical observation separates the
even phase offsets into blocks of size 2 * 10^n. The remaining low value
and the complete high observation determine a residue modulo nine. That
residue identifies both the missing phase bit and the actual outgoing high
carry. Neither decoder receives the phase or either normalization carry.

The correctness statements use the existing literal streams of bounded
exterior words. Empty, zero-head, and untrimmed words are included. No
ordinary-orbit or palindrome-avoidance conclusion is asserted.
-/

namespace Agent5.PhaseStreamRecovery

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.StreamObservationInjectivity

/-- The even phase offset selected by the complete low observation. -/
def lowOffset (n : Nat) (low : List Nat) : Nat :=
  2 * (lowValue low / (2 * 10 ^ n))

/-- A residue computed from the two observed lists and the known width.
The added nine makes the displayed subtraction exact in natural numbers. -/
def observationResidue (n : Nat) (low high : List Nat) : Nat :=
  (highValue high + 9 -
    (lowValue low - lowOffset n low * 10 ^ n) % 9) % 9

/-- Recover the phase from finite observations; total on arbitrary lists. -/
def decodePhase (n : Nat) (low high : List Nat) : Nat :=
  let u := lowOffset n low
  let d := observationResidue n low high
  u + 10 * (if d ≤ 1 then d else (d - u) / 2)

/-- Recover the actual outgoing high carry without supplying the phase. -/
def decodeHighCarry (n : Nat) (low high : List Nat) : Nat :=
  if observationResidue n low high ≤ 1 then 1 else 0

private theorem phase_decode_facts (c : Nat) (hc : nonneutralPhase c) :
    let k := if 10 ≤ c then 1 else 0
    let u := c - 10 * k
    c = u + 10 * k ∧ 2 * (u / 2) = u ∧
      2 ≤ u + 2 * k ∧ u + 2 * k < 9 ∧ k ≤ 1 := by
  simp only [nonneutralPhase, List.mem_cons, List.not_mem_nil, or_false] at hc
  rcases hc with h | h | h | h | h | h | h | h <;> subst h <;> decide

private theorem lowValue_lt_twice_width (B : List Nat)
    (hB : ∀ x ∈ B, x ≤ 18) : lowValue B < 2 * 10 ^ B.length := by
  have hb : ∀ x ∈ B.reverse, x ≤ 18 := by
    intro x hx
    exact hB x (List.mem_reverse.mp hx)
  have hv := highValue_lt B.reverse hb
  rw [highValue_reverse_word, List.length_reverse] at hv
  omega

private theorem lowOffset_correct (c : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    lowOffset B.length
      (adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int))) =
      c - 10 * (if 10 ≤ c then 1 else 0) := by
  let k : Nat := if 10 ≤ c then 1 else 0
  let u := c - 10 * k
  have hf := phase_decode_facts c hc
  change c = u + 10 * k ∧ 2 * (u / 2) = u ∧
    2 ≤ u + 2 * k ∧ u + 2 * k < 9 ∧ k ≤ 1 at hf
  have heven := hf.2.1
  have hv := lowValue_lt_twice_width B hB
  have hp : 0 < 2 * 10 ^ B.length :=
    Nat.mul_pos (by decide) (Nat.pow_pos (by decide))
  have hmul : u * 10 ^ B.length = (2 * 10 ^ B.length) * (u / 2) := by
    calc
      _ = (2 * (u / 2)) * 10 ^ B.length := by rw [heven]
      _ = _ := by
        rw [Nat.mul_assoc, Nat.mul_comm (u / 2), ← Nat.mul_assoc]
  unfold lowOffset
  rw [low_stream_prefix_value c B hc hB]
  change 2 * ((lowValue B + u * 10 ^ B.length) / (2 * 10 ^ B.length)) = u
  rw [hmul, Nat.add_mul_div_left _ _ hp, Nat.div_eq_of_lt hv, Nat.zero_add]
  exact heven

private theorem numeric_residue (c V H g : Nat)
    (hc : nonneutralPhase c) (hmod : V % 9 = H % 9) :
    let k := if 10 ≤ c then 1 else 0
    let u := c - 10 * k
    let R := if g = 0 then 10 * (H + k) + (c - 9 * k) else H + k
    (R + 9 - V % 9) % 9 = if g = 0 then u + 2 * k else k := by
  have hdiv := Nat.mod_add_div H 9
  simp only [nonneutralPhase, List.mem_cons, List.not_mem_nil, or_false] at hc
  rcases hc with h | h | h | h | h | h | h | h <;> subst h <;>
    by_cases hg : g = 0 <;> simp [hg] <;> omega

private theorem observationResidue_correct (c : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    let k := if 10 ≤ c then 1 else 0
    let g := (normalize B.reverse k).2
    observationResidue B.length
      (adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int)))
      (fractionDigits (B.length + 1) (rhoNum c B)
        (9 * 10 ^ B.length * 10 ^ g)) =
      if g = 0 then (c - 10 * k) + 2 * k else k := by
  unfold observationResidue
  rw [lowOffset_correct c B hc hB, low_stream_prefix_value c B hc hB]
  simp only [Nat.add_sub_cancel_right]
  rw [high_stream_prefix_value c B hc hB]
  exact numeric_residue c (lowValue B) (highValue B)
    (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 hc
    (lowValue_highValue_mod_nine B)

private theorem decoders_correct (c : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    let k := if 10 ≤ c then 1 else 0
    let g := (normalize B.reverse k).2
    let low := adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int))
    let high := fractionDigits (B.length + 1) (rhoNum c B)
      (9 * 10 ^ B.length * 10 ^ g)
    decodePhase B.length low high = c ∧
      decodeHighCarry B.length low high = g := by
  let k : Nat := if 10 ≤ c then 1 else 0
  let u := c - 10 * k
  let g := (normalize B.reverse k).2
  let low := adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int))
  let high := fractionDigits (B.length + 1) (rhoNum c B)
    (9 * 10 ^ B.length * 10 ^ g)
  change decodePhase B.length low high = c ∧ decodeHighCarry B.length low high = g
  have hf := phase_decode_facts c hc
  change c = u + 10 * k ∧ 2 * (u / 2) = u ∧
    2 ≤ u + 2 * k ∧ u + 2 * k < 9 ∧ k ≤ 1 at hf
  obtain ⟨hcu, _, hlarge, _, hk⟩ := hf
  have hb : ∀ x ∈ B.reverse, x ≤ 18 := by
    intro x hx
    exact hB x (List.mem_reverse.mp hx)
  have hg : g ≤ 1 := normalize_carry_le B.reverse k hb hk
  have hu : lowOffset B.length low = u := lowOffset_correct c B hc hB
  have hd : observationResidue B.length low high =
      if g = 0 then u + 2 * k else k := observationResidue_correct c B hc hB
  unfold decodePhase decodeHighCarry
  rw [hd, hu]
  by_cases hg0 : g = 0
  · have hnot : ¬u + 2 * k ≤ 1 := by omega
    simp only [if_pos hg0, if_neg hnot]
    constructor
    · have hquot : (u + 2 * k - u) / 2 = k := by omega
      rw [hquot]
      exact hcu.symm
    · exact hg0.symm
  · simp only [if_neg hg0, if_pos hk]
    exact ⟨hcu.symm, by omega⟩

/-- The width and the first n+1 digits of each original stream recover the
nonneutral phase of every bounded exterior word, including the empty word. -/
theorem decodePhase_correct (c : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    decodePhase B.length
      (adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int)))
      (fractionDigits (B.length + 1) (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) = c :=
  (decoders_correct c B hc hB).1

/-- The same finite observations recover the actual outgoing high carry
without supplying the phase to the decoder. -/
theorem decodeHighCarry_correct (c : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    decodeHighCarry B.length
      (adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int)))
      (fractionDigits (B.length + 1) (rhoNum c B)
        (9 * 10 ^ B.length *
          10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) =
      (normalize B.reverse (if 10 ≤ c then 1 else 0)).2 :=
  (decoders_correct c B hc hB).2

#print axioms decodePhase_correct
#print axioms decodeHighCarry_correct

end Agent5.PhaseStreamRecovery
