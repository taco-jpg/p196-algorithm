import DigitDefinitions

/-!
Agent #5: exact ordinary decimal long division for the high exterior stream.
The proof uses the actual outgoing normalization carry and integer arithmetic.
-/

namespace Agent5.ExactDigitStreams

open P196.Agent7.Finite Agent115.ExteriorFactorization

/-- Multiplying numerator and denominator by the same positive integer preserves
all digits produced by long division. -/
theorem fractionDigits_scale (n r D s : Nat) (hs : 0 < s) :
    fractionDigits n (s * r) (s * D) = fractionDigits n r D := by
  induction n generalizing r with
  | zero => rfl
  | succ n ih =>
    simp only [fractionDigits, Nat.mul_left_comm 10 s r,
      Nat.mul_div_mul_left _ _ hs, Nat.mul_mod_mul_left, ih]

/-- The proper fraction `t/9` repeats its single decimal digit. -/
theorem fractionDigits_repeat (q t : Nat) (ht : t < 9) :
    fractionDigits q t 9 = List.replicate q t := by
  induction q with
  | zero => rfl
  | succ q ih =>
    have hd : 10 * t / 9 = t := by omega
    have hm : 10 * t % 9 = t := by omega
    simp [fractionDigits, hd, hm, ih, List.replicate_succ]

theorem highValue_cons_digit (x : Nat) (xs : List Nat) :
    highValue (x :: xs) = x * 10 ^ xs.length + highValue xs := by
  change xs.foldl (fun acc b => 10 * acc + b) (10 * 0 + x) = _
  rw [foldl_high]
  simp

/-- A word of ordinary decimal digits has value below its place-value modulus. -/
theorem highValue_lt_pow (W : List Nat) (hW : ∀ x ∈ W, x < 10) :
    highValue W < 10 ^ W.length := by
  induction W with
  | nil => simp [highValue]
  | cons x xs ih =>
    have hx := hW x List.mem_cons_self
    have hxs : ∀ y ∈ xs, y < 10 := by
      intro y hy
      exact hW y (List.mem_cons_of_mem x hy)
    rw [highValue_cons_digit, List.length_cons]
    calc
      x * 10 ^ xs.length + highValue xs <
          x * 10 ^ xs.length + 10 ^ xs.length := Nat.add_lt_add_left (ih hxs) _
      _ = (x + 1) * 10 ^ xs.length := by rw [Nat.add_mul, Nat.one_mul]
      _ ≤ 10 * 10 ^ xs.length := Nat.mul_le_mul_right _ (by omega)
      _ = 10 ^ (xs.length + 1) := by rw [Nat.pow_succ, Nat.mul_comm]

/-- Exact finite decimal expansion with an eventually repeating tail. -/
theorem fractionDigits_of_highValue (W : List Nat) (t q : Nat)
    (hW : ∀ x ∈ W, x < 10) (ht : t < 9) :
    fractionDigits (W.length + q) (9 * highValue W + t) (9 * 10 ^ W.length) =
      W ++ List.replicate q t := by
  induction W with
  | nil => simpa [highValue] using fractionDigits_repeat q t ht
  | cons x xs ih =>
    have hxs : ∀ y ∈ xs, y < 10 := by
      intro y hy
      exact hW y (List.mem_cons_of_mem x hy)
    have hv := highValue_lt_pow xs hxs
    have hp : 0 < 9 * 10 ^ xs.length := Nat.mul_pos (by decide) (Nat.pow_pos (by decide))
    have hr : 9 * highValue xs + t < 9 * 10 ^ xs.length := by omega
    have hnum : 9 * highValue (x :: xs) + t =
        (9 * highValue xs + t) + (9 * 10 ^ xs.length) * x := by
      rw [highValue_cons_digit, Nat.mul_add]
      ac_rfl
    have hden : 9 * 10 ^ (xs.length + 1) = 10 * (9 * 10 ^ xs.length) := by
      rw [Nat.pow_succ]
      ac_rfl
    have hd : ((9 * highValue xs + t) + (9 * 10 ^ xs.length) * x) /
        (9 * 10 ^ xs.length) = x := by
      rw [Nat.add_mul_div_left _ _ hp, Nat.div_eq_of_lt hr, Nat.zero_add]
    have hm : ((9 * highValue xs + t) + (9 * 10 ^ xs.length) * x) %
        (9 * 10 ^ xs.length) = 9 * highValue xs + t := by
      rw [Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hr]
    simp only [List.length_cons, Nat.succ_add, fractionDigits, hnum, hden,
      Nat.mul_div_mul_left _ _ (by decide : 0 < 10), Nat.mul_mod_mul_left, hd, hm]
    rw [fractionDigits_scale _ _ _ 10 (by decide), ih hxs]
    rfl


/-- Normalization preserves the integer represented by the digits and outgoing carry. -/
theorem normalize_value_conservation (B : List Nat) (carry : Nat) :
    lowValue (normalize B carry).1 +
        10 ^ B.length * (normalize B carry).2 = lowValue B + carry := by
  induction B generalizing carry with
  | nil => simp [normalize, lowValue]
  | cons x xs ih =>
    have hi := ih ((x + carry) / 10)
    have hm := congrArg (fun v : Nat => 10 * v) hi
    simp only [Nat.mul_add] at hm
    simp only [normalize, lowValue, List.length_cons, Nat.pow_succ]
    have hp : 10 ^ xs.length * 10 * (normalize xs ((x + carry) / 10)).2 =
        10 * (10 ^ xs.length * (normalize xs ((x + carry) / 10)).2) := by ac_rfl
    rw [hp]
    omega

/-- Every emitted normalization coefficient is a decimal digit. -/
theorem normalize_digits_lt_ten (B : List Nat) (carry : Nat) :
    ∀ x ∈ (normalize B carry).1, x < 10 := by
  induction B generalizing carry with
  | nil => simp [normalize]
  | cons a as ih =>
    intro x hx
    simp only [normalize] at hx
    rcases List.mem_cons.mp hx with hx | hx
    · subst x
      exact Nat.mod_lt _ (by decide)
    · exact ih _ x hx

theorem highValue_reverse_word (W : List Nat) : highValue W.reverse = lowValue W := by
  simpa using (lowValue_reverse W.reverse).symm

/-- Nonneutral phases leave a proper, repeating decimal tail after the band carry. -/
theorem phase_tail_digit (c : Nat) (hc : nonneutralPhase c) :
    c = 9 * (if 10 ≤ c then 1 else 0) + (c - 9 * (if 10 ≤ c then 1 else 0)) ∧
      c - 9 * (if 10 ≤ c then 1 else 0) < 9 := by
  unfold nonneutralPhase at hc
  simp only [List.mem_cons, List.mem_nil_iff, or_false] at hc
  rcases hc with h | h | h | h | h | h | h | h <;> subst h <;> decide


/-- Exact high decimal exterior stream, including the empty word. The scale uses
its actual outgoing carry, without any threshold characterization of that carry. -/
theorem fractionDigits_exterior (c : Nat) (B : List Nat) (q : Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    let k := if 10 ≤ c then 1 else 0
    let t := c - 9 * k
    let g := (normalize B.reverse k).2
    fractionDigits (B.length + 1 + q) (rhoNum c B) (9 * 10 ^ B.length * 10 ^ g) =
      (if g == 0 then (normalize B.reverse k).1.reverse ++ [t]
       else [1] ++ (normalize B.reverse k).1.reverse) ++ List.replicate q t := by
  let k := if 10 ≤ c then 1 else 0
  let t := c - 9 * k
  let g := (normalize B.reverse k).2
  let A := (normalize B.reverse k).1.reverse
  change fractionDigits (B.length + 1 + q) (rhoNum c B) (9 * 10 ^ B.length * 10 ^ g) =
    (if g == 0 then A ++ [t] else [1] ++ A) ++ List.replicate q t
  have hlen : A.length = B.length := by
    dsimp [A]
    rw [List.length_reverse, normalize_length, List.length_reverse]
  have ha : ∀ x ∈ A, x < 10 := by
    intro x hx
    exact normalize_digits_lt_ten B.reverse k x (List.mem_reverse.mp hx)
  have hk : k ≤ 1 := by dsimp [k]; split <;> decide
  have hb : ∀ x ∈ B.reverse, x ≤ 18 := by
    intro x hx
    exact hB x (List.mem_reverse.mp hx)
  have hg : g ≤ 1 := normalize_carry_le B.reverse k hb hk
  have ht := phase_tail_digit c hc
  change c = 9 * k + t ∧ t < 9 at ht
  have hv : highValue A + 10 ^ B.length * g = highValue B + k := by
    dsimp [A, g]
    rw [highValue_reverse_word]
    simpa [lowValue_reverse] using normalize_value_conservation B.reverse k
  by_cases hg0 : g = 0
  · have hnum : rhoNum c B = 9 * highValue A + t := by
      rw [hg0, Nat.mul_zero, Nat.add_zero] at hv
      unfold rhoNum
      omega
    have hf := fractionDigits_of_highValue A t (q + 1) ha ht.2
    simpa [hg0, hnum, hlen, List.replicate_succ, List.append_assoc,
      Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using hf
  · have hg1 : g = 1 := by omega
    have ha1 : ∀ x ∈ (1 :: A), x < 10 := by
      intro x hx
      rcases List.mem_cons.mp hx with hx | hx
      · subst x; decide
      · exact ha x hx
    have hnum : rhoNum c B = 9 * highValue (1 :: A) + t := by
      rw [highValue_cons_digit, hlen, Nat.one_mul]
      rw [hg1, Nat.mul_one] at hv
      unfold rhoNum
      omega
    have hf := fractionDigits_of_highValue (1 :: A) t q ha1 ht.2
    simpa [hg1, hnum, hlen, Nat.pow_succ, Nat.mul_assoc] using hf

/-- Asking for more digits preserves every already produced prefix. -/
theorem fractionDigits_prefix (n q r D : Nat) :
    (fractionDigits (n + q) r D).take n = fractionDigits n r D := by
  induction n generalizing r with
  | zero => simp [fractionDigits]
  | succ n ih => simp [fractionDigits, Nat.succ_add, ih]


/-- Long division of a proper fraction emits only decimal digits. -/
theorem fractionDigits_digits_lt_ten (n r D : Nat) (hr : r < D) :
    ∀ d ∈ fractionDigits n r D, d < 10 := by
  have hD : 0 < D := by omega
  induction n generalizing r with
  | zero => simp [fractionDigits]
  | succ n ih =>
    intro d hd
    simp only [fractionDigits] at hd
    rcases List.mem_cons.mp hd with hd | hd
    · subst d
      apply (Nat.div_lt_iff_lt_mul hD).2
      exact Nat.mul_lt_mul_of_pos_left hr (by decide)
    · exact ih _ (Nat.mod_lt _ hD) d hd

/-- Every finite prefix of the exact high exterior stream contains decimal digits.
This follows from the stream formula and prefix consistency, without a separate
floor or threshold theorem for the outgoing carry. -/
theorem fractionDigits_exterior_digits_lt_ten (c : Nat) (B : List Nat) (n : Nat)
    (hc : nonneutralPhase c) (hB : ∀ x ∈ B, x ≤ 18) :
    let k := if 10 ≤ c then 1 else 0
    let g := (normalize B.reverse k).2
    ∀ d ∈ fractionDigits n (rhoNum c B) (9 * 10 ^ B.length * 10 ^ g), d < 10 := by
  let k := if 10 ≤ c then 1 else 0
  let t := c - 9 * k
  let g := (normalize B.reverse k).2
  let A := (normalize B.reverse k).1.reverse
  change ∀ d ∈ fractionDigits n (rhoNum c B) (9 * 10 ^ B.length * 10 ^ g), d < 10
  intro d hd
  have hp := fractionDigits_prefix n (B.length + 1) (rhoNum c B)
    (9 * 10 ^ B.length * 10 ^ g)
  have hlong : d ∈ fractionDigits (B.length + 1 + n) (rhoNum c B)
      (9 * 10 ^ B.length * 10 ^ g) := by
    rw [← hp] at hd
    have hmem := List.mem_of_mem_take hd
    simpa [Nat.add_comm] using hmem
  have he := fractionDigits_exterior c B n hc hB
  change fractionDigits (B.length + 1 + n) (rhoNum c B) (9 * 10 ^ B.length * 10 ^ g) =
    (if g == 0 then A ++ [t] else [1] ++ A) ++ List.replicate n t at he
  rw [he] at hlong
  have ht : t < 9 := (phase_tail_digit c hc).2
  have ha : ∀ x ∈ A, x < 10 := by
    intro x hx
    exact normalize_digits_lt_ten B.reverse k x (List.mem_reverse.mp hx)
  rcases List.mem_append.mp hlong with hfirst | htail
  · split at hfirst
    · rcases List.mem_append.mp hfirst with hA | ht'
      · exact ha d hA
      · have : d = t := by simpa using ht'
        omega
    · rcases List.mem_append.mp hfirst with h1 | hA
      · have : d = 1 := by simpa using h1
        omega
      · exact ha d hA
  · have : d = t := List.eq_of_mem_replicate htail
    omega

end Agent5.ExactDigitStreams
