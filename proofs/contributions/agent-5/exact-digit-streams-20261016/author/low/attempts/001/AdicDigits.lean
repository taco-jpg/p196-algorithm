import DigitDefinitions

/-!
Agent #5: exact low 10-adic digits of the exterior coordinate.

All statements use the unchanged `Agent115.ExteriorFactorization` coordinate
and `P196.Agent7.Finite.normalize`. The correspondence includes empty and
untrimmed words. No 10-adic library, evaluator axiom, or admitted proof is used.
-/

namespace Agent5.ExactDigitStreams

open P196.Agent7.Finite Agent115.ExteriorFactorization

/-- One normalization column for a numerator whose denominator is nine. -/
theorem adicNumeratorDigits_column (n x : Nat) (z : Int) :
    adicNumeratorDigits (n + 1) (9 * (x : Int) + 10 * z) =
      x % 10 :: adicNumeratorDigits n (9 * ((x / 10 : Nat) : Int) + z) := by
  have hd : ((-(9 * (x : Int) + 10 * z)) % 10).toNat = x % 10 := by omega
  have hr : (9 * (x : Int) + 10 * z - 9 * ((x % 10 : Nat) : Int)) / 10 =
      9 * ((x / 10 : Nat) : Int) + z := by omega
  simp only [adicNumeratorDigits, hd, hr]

/-- The negative numerator `-t` gives a constant low digit stream. -/
theorem adicNumeratorDigits_constant (n t : Nat) (ht : t < 10) :
    adicNumeratorDigits n (-(t : Int)) = List.replicate n t := by
  have hd : ((-(-(t : Int))) % 10).toNat = t := by omega
  have hr : (-(t : Int) - 9 * (t : Int)) / 10 = -(t : Int) := by omega
  induction n with
  | zero => rfl
  | succ n ih => simp only [adicNumeratorDigits, hd, hr, ih, List.replicate_succ]

/-- A finite scan consumes exactly the word's digits, leaving its true carry.
The phase numerator is arbitrary, and no coefficient bounds are needed. -/
theorem adicNumeratorDigits_normalize (B : List Nat) (e q : Nat) (c : Int) :
    adicNumeratorDigits (B.length + q)
      (9 * ((lowValue B + e : Nat) : Int) - c * 10 ^ B.length) =
      (normalize B e).1 ++
        adicNumeratorDigits q (9 * ((normalize B e).2 : Int) - c) := by
  induction B generalizing e with
  | nil => simp [lowValue, normalize]
  | cons x xs ih =>
      have ha :
          9 * ((lowValue (x :: xs) + e : Nat) : Int) - c * 10 ^ (x :: xs).length =
          9 * ((x + e : Nat) : Int) +
            10 * (9 * (lowValue xs : Int) - c * 10 ^ xs.length) := by
        simp only [lowValue, List.length_cons, Int.natCast_add, Int.natCast_mul,
          Int.natCast_ofNat, Int.pow_succ]
        have hm : c * (10 ^ xs.length * 10) = 10 * (c * 10 ^ xs.length) := by
          ac_rfl
        rw [hm]
        omega
      have hn : (x :: xs).length + q = xs.length + q + 1 := by simp; omega
      rw [ha, hn, adicNumeratorDigits_column]
      have hr : 9 * (((x + e) / 10 : Nat) : Int) +
          (9 * (lowValue xs : Int) - c * 10 ^ xs.length) =
          9 * ((lowValue xs + (x + e) / 10 : Nat) : Int) - c * 10 ^ xs.length := by
        simp only [Int.natCast_add]
        omega
      rw [hr, ih]
      rfl

/-- The entrance to a nonneutral phase tail has one boundary digit, then
constant digits. Its incoming carry is the actual scan carry. -/
theorem adicNumeratorDigits_phase (c e q : Nat) (hc : nonneutralPhase c)
    (he : e ≤ 1) :
    adicNumeratorDigits (q + 1) (9 * (e : Int) - (c : Int)) =
      (c + e - 10 * (if 10 ≤ c then 1 else 0)) ::
        List.replicate q (c - 9 * (if 10 ≤ c then 1 else 0)) := by
  have hp := phase_facts c e hc he
  have hd : ((-(9 * (e : Int) - (c : Int))) % 10).toNat =
      c + e - 10 * (if 10 ≤ c then 1 else 0) := by
    split <;> simp_all <;> omega
  have hr :
      (9 * (e : Int) - (c : Int) -
        9 * ((c + e - 10 * (if 10 ≤ c then 1 else 0) : Nat) : Int)) / 10 =
      -((c - 9 * (if 10 ≤ c then 1 else 0) : Nat) : Int) := by
    split <;> simp_all <;> omega
  have ht : c - 9 * (if 10 ≤ c then 1 else 0) < 10 := by
    have hmod : (c + (if 10 ≤ c then 1 else 0)) % 10 < 10 := Nat.mod_lt _ (by decide)
    omega
  simp only [adicNumeratorDigits, hd, hr, adicNumeratorDigits_constant q _ ht]

/-- Exact low stream of the existing centered exterior coordinate, including
every number of constant tail digits and the empty exterior. -/
theorem adicNumeratorDigits_exterior (c : Nat) (B : List Nat) (q : Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    adicNumeratorDigits (B.length + 1 + q) (zValue c B - (c : Int)) =
      (normalize B 0).1 ++
        [c + (normalize B 0).2 - 10 * (if 10 ≤ c then 1 else 0)] ++
        List.replicate q (c - 9 * (if 10 ≤ c then 1 else 0)) := by
  have ha : zValue c B - (c : Int) =
      9 * ((lowValue B + 0 : Nat) : Int) - (c : Int) * 10 ^ B.length := by
    simp only [zValue, Nat.add_zero, Int.mul_sub, Int.mul_one]
    omega
  have he := normalize_carry_le B 0 hB (by decide)
  rw [ha, Nat.add_assoc, Nat.add_comm 1 q, adicNumeratorDigits_normalize,
    adicNumeratorDigits_phase c (normalize B 0).2 q hc he]
  simp only [List.append_assoc, List.singleton_append]

#print axioms adicNumeratorDigits_column
#print axioms adicNumeratorDigits_constant
#print axioms adicNumeratorDigits_normalize
#print axioms adicNumeratorDigits_phase
#print axioms adicNumeratorDigits_exterior

end Agent5.ExactDigitStreams
