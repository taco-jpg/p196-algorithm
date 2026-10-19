import P196.Agent5ExactDigitStreams.CoordinateStreams
import P196.Agent6CoordinateDynamics.ExteriorObservationInjective

/-!
Agent #5: numeric observations of the existing literal exterior streams.

The complete low prefix recovers the old little-endian coefficient value.
The complete high prefix gives one of two readings of the old high value.
Their residues modulo nine distinguish the actual outgoing carry, so no
separate carry observation is required. All source streams, the original
normalization, and the exterior map remain unchanged.

These statements concern finite exterior observations, not an infinite
ordinary orbit or a palindrome-avoidance conclusion.
-/

namespace Agent5.StreamObservationInjectivity

open P196.Agent7.Finite Agent115.ExteriorFactorization
open Agent5.ExactDigitStreams

/-- The two positional readings of a coefficient word agree modulo nine. -/
theorem lowValue_mod_nine (B : List Nat) :
    lowValue B % 9 = B.sum % 9 := by
  induction B with
  | nil => rfl
  | cons x xs ih =>
    simp [lowValue, Nat.add_mod, Nat.mul_mod, ih]

theorem lowValue_highValue_mod_nine (B : List Nat) :
    lowValue B % 9 = highValue B % 9 := by
  have hp : ∀ n : Nat, 10 ^ n % 9 = 1 := by
    intro n
    induction n with
    | zero => decide
    | succ n ih => simp [Nat.pow_succ, Nat.mul_mod, ih]
  induction B with
  | nil => rfl
  | cons x xs ih =>
    rw [lowValue, highValue_cons]
    simp [Nat.add_mod, Nat.mul_mod, hp, ih]

theorem nonneutralPhase_mod_nine_ne_zero (c : Nat) (hc : nonneutralPhase c) :
    c % 9 ≠ 0 := by
  simp only [nonneutralPhase, List.mem_cons, List.not_mem_nil, or_false] at hc
  omega

/-- Reading the complete low stream prefix as a little-endian value recovers
the old little-endian coefficient value plus a known phase-dependent offset. -/
theorem low_stream_prefix_value (c : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    lowValue (adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int))) =
      lowValue B + (c - 10 * (if 10 ≤ c then 1 else 0)) * 10 ^ B.length := by
  let k : Nat := if 10 ≤ c then 1 else 0
  have hk : 10 * k ≤ c := by
    dsimp [k]
    split <;> omega
  have hu : c + (normalize B 0).2 - 10 * k =
      c - 10 * k + (normalize B 0).2 := by omega
  have hs :
      adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int)) =
        (normalize B 0).1 ++ [c + (normalize B 0).2 - 10 * k] := by
    simpa only [Nat.add_zero, List.replicate_zero, List.append_nil] using
      adicNumeratorDigits_exterior c B 0 hc hB
  have hv := normalize_value_conservation B 0
  simp only [Nat.add_zero] at hv
  change lowValue _ = lowValue B + (c - 10 * k) * 10 ^ B.length
  rw [hs, lowValue_append, normalize_length]
  simp only [lowValue, Nat.mul_zero, Nat.add_zero]
  rw [hu, Nat.mul_add, Nat.mul_comm (10 ^ B.length) (c - 10 * k)]
  omega

/-- Reading the complete high stream prefix as a big-endian value gives one
of two explicit readings of the old high value, selected by the actual carry. -/
theorem high_stream_prefix_value (c : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    let k := if 10 ≤ c then 1 else 0
    let g := (normalize B.reverse k).2
    highValue (fractionDigits (B.length + 1) (rhoNum c B)
      (9 * 10 ^ B.length * 10 ^ g)) =
      if g = 0 then
        10 * (highValue B + k) + (c - 9 * k)
      else highValue B + k := by
  let k : Nat := if 10 ≤ c then 1 else 0
  let g : Nat := (normalize B.reverse k).2
  let A := (normalize B.reverse k).1.reverse
  change highValue (fractionDigits (B.length + 1) (rhoNum c B)
    (9 * 10 ^ B.length * 10 ^ g)) =
      if g = 0 then 10 * (highValue B + k) + (c - 9 * k)
      else highValue B + k
  have hk : k ≤ 1 := by
    dsimp [k]
    split <;> decide
  have hb : ∀ x ∈ B.reverse, x ≤ 18 := by
    intro x hx
    exact hB x (List.mem_reverse.mp hx)
  have hg : g ≤ 1 := normalize_carry_le B.reverse k hb hk
  have hlen : A.length = B.length := by
    dsimp [A]
    rw [List.length_reverse, normalize_length, List.length_reverse]
  have hv : highValue A + 10 ^ B.length * g = highValue B + k := by
    dsimp [A, g]
    rw [highValue_reverse_word]
    simpa [lowValue_reverse] using normalize_value_conservation B.reverse k
  have hs : fractionDigits (B.length + 1) (rhoNum c B)
      (9 * 10 ^ B.length * 10 ^ g) =
      if g == 0 then A ++ [c - 9 * k] else [1] ++ A := by
    simpa only [Nat.add_zero, List.replicate_zero, List.append_nil] using
      fractionDigits_exterior c B 0 hc hB
  by_cases hg0 : g = 0
  · rw [if_pos hg0, hs]
    simp only [hg0, beq_self_eq_true, if_true]
    rw [highValue_append_single]
    rw [hg0, Nat.mul_zero, Nat.add_zero] at hv
    rw [hv]
  · have hg1 : g = 1 := by omega
    rw [if_neg hg0, hs]
    simp only [hg1, show (1 == 0) = false by decide, Bool.false_eq_true,
      if_false, List.singleton_append, highValue_cons_digit, hlen, Nat.one_mul]
    rw [hg1, Nat.mul_one] at hv
    omega

/-- The actual outgoing carry is zero exactly when the two finite stream
readings satisfy this residue test. The test uses no separate carry input. -/
theorem no_overflow_iff_stream_residues (c : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    let k := if 10 ≤ c then 1 else 0
    let g := (normalize B.reverse k).2
    g = 0 ↔
      highValue (fractionDigits (B.length + 1) (rhoNum c B)
        (9 * 10 ^ B.length * 10 ^ g)) % 9 =
      (lowValue (adicNumeratorDigits (B.length + 1)
        (zValue c B - (c : Int))) + 2 * k) % 9 := by
  let k : Nat := if 10 ≤ c then 1 else 0
  let g : Nat := (normalize B.reverse k).2
  let L := lowValue (adicNumeratorDigits (B.length + 1)
    (zValue c B - (c : Int)))
  let R := highValue (fractionDigits (B.length + 1) (rhoNum c B)
    (9 * 10 ^ B.length * 10 ^ g))
  change g = 0 ↔ R % 9 = (L + 2 * k) % 9
  have hk : 10 * k ≤ c := by
    dsimp [k]
    split <;> omega
  have ht := phase_tail_digit c hc
  change c = 9 * k + (c - 9 * k) ∧ c - 9 * k < 9 at ht
  have hc9 := nonneutralPhase_mod_nine_ne_zero c hc
  have hmod := lowValue_highValue_mod_nine B
  have hp : 10 ^ B.length % 9 = 1 := by
    have allP : ∀ n : Nat, 10 ^ n % 9 = 1 := by
      intro n
      induction n with
      | zero => decide
      | succ n ih => simp [Nat.pow_succ, Nat.mul_mod, ih]
    exact allP B.length
  have hl : L = lowValue B + (c - 10 * k) * 10 ^ B.length :=
    low_stream_prefix_value c B hc hB
  have hr : R = if g = 0 then
      10 * (highValue B + k) + (c - 9 * k)
      else highValue B + k := high_stream_prefix_value c B hc hB
  have hlmod : (L + 2 * k) % 9 = (lowValue B + c + k) % 9 := by
    rw [hl]
    simp [Nat.add_mod, Nat.mul_mod, hp]
    omega
  by_cases hg0 : g = 0
  · rw [if_pos hg0] at hr
    have hres : R % 9 = (L + 2 * k) % 9 := by
      rw [hr, hlmod]
      omega
    exact ⟨fun _ => hres, fun _ => hg0⟩
  · rw [if_neg hg0] at hr
    have hres : R % 9 ≠ (L + 2 * k) % 9 := by
      intro heq
      rw [hr, hlmod] at heq
      omega
    exact ⟨fun h => False.elim (hg0 h), fun h => False.elim (hres h)⟩

/-- A total decoder on observed lists; correctness is asserted for complete
literal prefixes in `decodeCarry_correct`. -/
def decodeCarry (c : Nat) (low high : List Nat) : Nat :=
  if highValue high % 9 =
      (lowValue low + 2 * (if 10 ≤ c then 1 else 0)) % 9
    then 0 else 1

/-- The residue decoder returns the actual outgoing normalization carry from
the two complete finite streams, including an empty exterior word. -/
theorem decodeCarry_correct (c : Nat) (B : List Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    let k := if 10 ≤ c then 1 else 0
    let g := (normalize B.reverse k).2
    decodeCarry c
      (adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int)))
      (fractionDigits (B.length + 1) (rhoNum c B)
        (9 * 10 ^ B.length * 10 ^ g)) = g := by
  let k : Nat := if 10 ≤ c then 1 else 0
  let g : Nat := (normalize B.reverse k).2
  have hk : k ≤ 1 := by
    dsimp [k]
    split <;> decide
  have hb : ∀ x ∈ B.reverse, x ≤ 18 := by
    intro x hx
    exact hB x (List.mem_reverse.mp hx)
  have hg : g ≤ 1 := normalize_carry_le B.reverse k hb hk
  have he := no_overflow_iff_stream_residues c B hc hB
  change g = 0 ↔ _ at he
  change decodeCarry c
    (adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int)))
    (fractionDigits (B.length + 1) (rhoNum c B)
      (9 * 10 ^ B.length * 10 ^ g)) = g
  unfold decodeCarry
  change (if highValue (fractionDigits (B.length + 1) (rhoNum c B)
      (9 * 10 ^ B.length * 10 ^ g)) % 9 =
    (lowValue (adicNumeratorDigits (B.length + 1)
      (zValue c B - (c : Int))) + 2 * k) % 9 then 0 else 1) = g
  split <;> rename_i htest
  · have hz : g = 0 := he.mpr htest
    exact hz.symm
  · have hn : g ≠ 0 := by
      intro hz
      exact htest (he.mp hz)
    omega

#print axioms lowValue_mod_nine
#print axioms lowValue_highValue_mod_nine
#print axioms nonneutralPhase_mod_nine_ne_zero
#print axioms low_stream_prefix_value
#print axioms high_stream_prefix_value
#print axioms no_overflow_iff_stream_residues
#print axioms decodeCarry_correct

end Agent5.StreamObservationInjectivity
