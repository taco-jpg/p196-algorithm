import P196.StreamObservationInjectivity.Values

/-!
Agent #5: phase exceptions and recovery of the omitted low carry.

The normalized low digit list records the low coefficient value modulo its
decimal width. Its residue modulo nine, together with the complete high
stream, leaves only two possible ambiguities: phase eight and phase ten.
In either case, the high value relation and the final normalization step
force one original word to end in its phase. Terminal trimming therefore
rules out every ambiguity and recovers the omitted low carry.
Outside phases eight and ten, the same recovery needs no terminal condition.

The argument uses the original normalization and literal fraction stream.
It imposes no positivity condition on the first coefficient and makes no
claim about an infinite ordinary orbit or palindrome avoidance.
-/

namespace Agent5.TrimmedStreamObservation

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams Agent5.StreamObservationInjectivity

private theorem pow_ten_mod_nine (n : Nat) : 10 ^ n % 9 = 1 := by
  induction n with
  | zero => decide
  | succ n ih => simp [Nat.pow_succ, Nat.mul_mod, ih]

private theorem normalized_residue (B : List Nat) :
    (lowValue (normalize B 0).1 + (normalize B 0).2) % 9 =
      highValue B % 9 := by
  have hv := normalize_value_conservation B 0
  simp only [Nat.add_zero] at hv
  calc
    _ = (lowValue (normalize B 0).1 +
        10 ^ B.length * (normalize B 0).2) % 9 := by
      simp [Nat.add_mod, Nat.mul_mod, pow_ten_mod_nine]
    _ = lowValue B % 9 := by rw [hv]
    _ = highValue B % 9 := lowValue_highValue_mod_nine B

private theorem low_carry_eq_of_highValue_eq (A B : List Nat)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hN : (normalize A 0).1 = (normalize B 0).1)
    (hH : highValue A = highValue B) :
    (normalize A 0).2 = (normalize B 0).2 := by
  have hqa := normalize_carry_le A 0 hA (by decide)
  have hqb := normalize_carry_le B 0 hB (by decide)
  have hrA := normalized_residue A
  have hrB := normalized_residue B
  rw [hN, hH] at hrA
  omega

/-- A cross-carry high-value relation is possible only in phases eight and
ten, with the displayed opposite low carries. Equality of the normalized
low lists suffices; no width or terminal-trimming hypothesis is needed. -/
theorem cross_highValue_phase_carries (c : Nat) (A B : List Nat)
    (hc : nonneutralPhase c)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hN : (normalize A 0).1 = (normalize B 0).1)
    (hH : highValue B = 10 * highValue A + c) :
    (c = 8 ∧ (normalize A 0).2 = 1 ∧ (normalize B 0).2 = 0) ∨
      (c = 10 ∧ (normalize A 0).2 = 0 ∧ (normalize B 0).2 = 1) := by
  have hqa := normalize_carry_le A 0 hA (by decide)
  have hqb := normalize_carry_le B 0 hB (by decide)
  have hrA := normalized_residue A
  have hrB := normalized_residue B
  rw [hN] at hrA
  rw [hH] at hrB
  have hres :
      (lowValue (normalize B 0).1 + (normalize B 0).2) % 9 =
        (lowValue (normalize B 0).1 + (normalize A 0).2 + c) % 9 := by
    calc
      _ = (10 * highValue A + c) % 9 := hrB
      _ = (highValue A % 9 + c) % 9 := by
        simp [Nat.add_mod, Nat.mul_mod]
      _ = ((lowValue (normalize B 0).1 + (normalize A 0).2) % 9 + c) % 9 := by
        rw [hrA]
      _ = _ := by simp [Nat.add_mod]
  clear hrA hrB hH
  simp only [nonneutralPhase, List.mem_cons, List.not_mem_nil, or_false] at hc
  omega

/-- The cross-carry numerical relation forces a terminal phase coefficient.
This implication already follows from equality of the normalized low lists;
it needs neither a separate width hypothesis nor a trimming assumption. -/
theorem last_eq_phase_of_cross_highValue (c : Nat) (A B : List Nat)
    (hc : nonneutralPhase c)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hN : (normalize A 0).1 = (normalize B 0).1)
    (hH : highValue B = 10 * highValue A + c) :
    B.getLast? = some c := by
  have hphase := cross_highValue_phase_carries c A B hc hA hB hN hH
  cases hrev : B.reverse with
  | nil =>
    have hnil : B = [] := by
      have hr := congrArg List.reverse hrev
      simpa only [List.reverse_reverse, List.reverse_nil] using hr
    rw [hnil] at hH
    simp only [highValue, List.foldl_nil] at hH
    rcases hphase with ⟨hc8, _, _⟩ | ⟨hc10, _, _⟩ <;> omega
  | cons b ts =>
    have hword : B = ts.reverse ++ [b] := by
      have hr := congrArg List.reverse hrev
      simpa only [List.reverse_reverse, List.reverse_cons] using hr
    have hb : b ≤ 18 := hB b (by simp [hword])
    have hts : ∀ x ∈ ts.reverse, x ≤ 18 := by
      intro x hx
      exact hB x (by simp only [hword, List.mem_append]; exact Or.inl hx)
    have hqt := normalize_carry_le ts.reverse 0 hts (by decide)
    have hlastcarry : (normalize B 0).2 =
        (b + (normalize ts.reverse 0).2) / 10 := by
      rw [hword, normalize_append_single]
    have hlastvalue : 10 * highValue ts.reverse + b =
        10 * highValue A + c := by
      simpa only [hword, highValue_append_single] using hH
    have hbc : b = c := by
      rcases hphase with ⟨hc8, _, hq0⟩ | ⟨hc10, _, hq1⟩ <;> omega
    rw [hword, List.getLast?_append]
    simp [hbc]

private theorem highValue_cases_of_high_prefix_eq (c : Nat) (A B : List Nat)
    (hc : nonneutralPhase c)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (hhi :
      fractionDigits (A.length + 1) (rhoNum c A)
          (9 * 10 ^ A.length *
            10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
        fractionDigits (B.length + 1) (rhoNum c B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) :
    highValue A = highValue B ∨
      highValue B = 10 * highValue A + c ∨
      highValue A = 10 * highValue B + c := by
  let k : Nat := if 10 ≤ c then 1 else 0
  let ga := (normalize A.reverse k).2
  let gb := (normalize B.reverse k).2
  have ht := phase_tail_digit c hc
  change c = 9 * k + (c - 9 * k) ∧ c - 9 * k < 9 at ht
  have hobs :
      (if ga = 0 then 10 * (highValue A + k) + (c - 9 * k)
        else highValue A + k) =
      (if gb = 0 then 10 * (highValue B + k) + (c - 9 * k)
        else highValue B + k) :=
    (high_stream_prefix_value c A hc hA).symm.trans
      ((congrArg highValue hhi).trans (high_stream_prefix_value c B hc hB))
  by_cases hga : ga = 0 <;> by_cases hgb : gb = 0
  · rw [if_pos hga, if_pos hgb] at hobs
    exact Or.inl (by omega)
  · rw [if_pos hga, if_neg hgb] at hobs
    exact Or.inr (Or.inl (by omega))
  · rw [if_neg hga, if_pos hgb] at hobs
    exact Or.inr (Or.inr (by omega))
  · rw [if_neg hga, if_neg hgb] at hobs
    exact Or.inl (by omega)

/-- A complete high literal prefix recovers the omitted low normalization
carry when both original words are terminal-trimmed and their normalized
low digit lists agree. No separately observed high carry is required. -/
theorem low_carry_eq_of_trimmed_high (c : Nat) (A B : List Nat)
    (hc : nonneutralPhase c)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (_hlen : A.length = B.length)
    (htA : A.getLast? ≠ some c) (htB : B.getLast? ≠ some c)
    (hN : (normalize A 0).1 = (normalize B 0).1)
    (hhi :
      fractionDigits (A.length + 1) (rhoNum c A)
          (9 * 10 ^ A.length *
            10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
        fractionDigits (B.length + 1) (rhoNum c B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) :
    (normalize A 0).2 = (normalize B 0).2 := by
  rcases highValue_cases_of_high_prefix_eq c A B hc hA hB hhi with
    hsame | hcross | hcross
  · exact low_carry_eq_of_highValue_eq A B hA hB hN hsame
  · exact False.elim (htB (last_eq_phase_of_cross_highValue c A B hc hA hB hN hcross))
  · exact False.elim (htA (last_eq_phase_of_cross_highValue c B A hc hB hA hN.symm hcross))

/-- Away from the two exceptional phases, the complete high prefix and the
normalized low list recover the low carry without terminal trimming. -/
theorem low_carry_eq_of_regular_high (c : Nat) (A B : List Nat)
    (hc : nonneutralPhase c) (hc8 : c ≠ 8) (hc10 : c ≠ 10)
    (hA : ∀ x ∈ A, x ≤ 18) (hB : ∀ x ∈ B, x ≤ 18)
    (_hlen : A.length = B.length)
    (hN : (normalize A 0).1 = (normalize B 0).1)
    (hhi :
      fractionDigits (A.length + 1) (rhoNum c A)
          (9 * 10 ^ A.length *
            10 ^ (normalize A.reverse (if 10 ≤ c then 1 else 0)).2) =
        fractionDigits (B.length + 1) (rhoNum c B)
          (9 * 10 ^ B.length *
            10 ^ (normalize B.reverse (if 10 ≤ c then 1 else 0)).2)) :
    (normalize A 0).2 = (normalize B 0).2 := by
  rcases highValue_cases_of_high_prefix_eq c A B hc hA hB hhi with
    hsame | hcross | hcross
  · exact low_carry_eq_of_highValue_eq A B hA hB hN hsame
  · have hphase := cross_highValue_phase_carries c A B hc hA hB hN hcross
    exact False.elim (hphase.elim (fun h => hc8 h.1) (fun h => hc10 h.1))
  · have hphase := cross_highValue_phase_carries c B A hc hB hA hN.symm hcross
    exact False.elim (hphase.elim (fun h => hc8 h.1) (fun h => hc10 h.1))

#print axioms cross_highValue_phase_carries
#print axioms last_eq_phase_of_cross_highValue
#print axioms low_carry_eq_of_trimmed_high
#print axioms low_carry_eq_of_regular_high

end Agent5.TrimmedStreamObservation
