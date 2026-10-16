import TARGET

/-!
Agent #115. Proof of `Agent115.ExteriorFactorization.Target`: the exact exterior
map `P196.Agent7.Finite.outerNext` depends only on the band phase, Agent #110's
centered value `zValue`, and the real value `rhoNum / (9 * 10^|B|)`.

Route (no digit expansions are needed):
* `normalize B carry` is determined by `B.length` and `lowValue B + carry`;
* appending one band coefficient `c` leaves `outerNext` unchanged;
* after padding both words with `c` to a common length, equal `zValue` and equal
  `ρ` become equal little-endian and big-endian values.
Core Lean only; no `native_decide`.
-/

namespace Agent115.ExteriorFactorization

open P196.Agent7.Finite

/-! ### Digits of a little-endian value -/

/-- The first `n` base-10 digits of `v`, least significant first. -/
def digitsOf : Nat → Nat → List Nat
  | 0, _ => []
  | n + 1, v => v % 10 :: digitsOf n (v / 10)

theorem digitsOf_length (n v : Nat) : (digitsOf n v).length = n := by
  induction n generalizing v with
  | zero => rfl
  | succ n ih => simp [digitsOf, ih]

theorem normalize_eq (B : List Nat) (carry : Nat) :
    normalize B carry =
      (digitsOf B.length (lowValue B + carry), (lowValue B + carry) / 10 ^ B.length) := by
  induction B generalizing carry with
  | nil => simp [normalize, digitsOf, lowValue]
  | cons x xs ih =>
    have h1 : (x + 10 * lowValue xs + carry) % 10 = (x + carry) % 10 := by omega
    have h2 : (x + 10 * lowValue xs + carry) / 10 = lowValue xs + (x + carry) / 10 := by omega
    simp only [normalize, ih, List.length_cons, digitsOf, lowValue, h1, h2]
    rw [Nat.pow_succ, Nat.mul_comm (10 ^ xs.length) 10, ← Nat.div_div_eq_div_mul, h2]

theorem normalize_length (B : List Nat) (carry : Nat) :
    (normalize B carry).1.length = B.length := by
  rw [normalize_eq, digitsOf_length]

theorem lowValue_append (l₁ l₂ : List Nat) :
    lowValue (l₁ ++ l₂) = lowValue l₁ + 10 ^ l₁.length * lowValue l₂ := by
  induction l₁ with
  | nil => simp [lowValue]
  | cons x xs ih =>
    simp only [List.cons_append, lowValue, ih, List.length_cons, Nat.pow_succ]
    rw [Nat.mul_add, Nat.add_assoc, Nat.mul_comm (10 ^ xs.length) 10, Nat.mul_assoc]

theorem highValue_append_single (B : List Nat) (x : Nat) :
    highValue (B ++ [x]) = 10 * highValue B + x := by
  unfold highValue
  rw [List.foldl_append]
  rfl

theorem foldl_high (B : List Nat) (a : Nat) :
    B.foldl (fun acc b => 10 * acc + b) a = a * 10 ^ B.length + highValue B := by
  induction B generalizing a with
  | nil => simp [highValue]
  | cons x xs ih =>
    have hx : highValue (x :: xs) = x * 10 ^ xs.length + highValue xs := by
      show List.foldl (fun acc b => 10 * acc + b) (10 * 0 + x) xs = _
      rw [ih]
      simp
    have e : 10 * a * 10 ^ xs.length = a * (10 ^ xs.length * 10) := by
      rw [Nat.mul_comm 10 a, Nat.mul_assoc, Nat.mul_comm 10]
    rw [hx, List.foldl_cons, ih, List.length_cons, Nat.pow_succ, Nat.add_mul, e, Nat.add_assoc]

theorem lowValue_reverse (B : List Nat) : lowValue B.reverse = highValue B := by
  induction B with
  | nil => rfl
  | cons x xs ih =>
    have hx : highValue (x :: xs) = x * 10 ^ xs.length + highValue xs := by
      show List.foldl (fun acc b => 10 * acc + b) (10 * 0 + x) xs = _
      rw [foldl_high]
      simp
    rw [List.reverse_cons, lowValue_append, ih, hx, List.length_reverse]
    simp only [lowValue, Nat.mul_zero, Nat.add_zero]
    rw [Nat.mul_comm (10 ^ xs.length) x]
    omega

/-! ### Carries stay at most one -/

theorem normalize_carry_le (B : List Nat) (carry : Nat) (hB : ∀ x ∈ B, x ≤ 18)
    (hc : carry ≤ 1) : (normalize B carry).2 ≤ 1 := by
  induction B generalizing carry with
  | nil => simpa [normalize] using hc
  | cons x xs ih =>
    simp only [normalize]
    apply ih
    · intro y hy; exact hB y (List.mem_cons_of_mem x hy)
    · have := hB x List.mem_cons_self; omega

theorem normalize_append_single (B : List Nat) (x carry : Nat) :
    normalize (B ++ [x]) carry =
      ((normalize B carry).1 ++ [(x + (normalize B carry).2) % 10],
        (x + (normalize B carry).2) / 10) := by
  induction B generalizing carry with
  | nil => simp [normalize]
  | cons y ys ih => simp only [List.cons_append, normalize, ih]

/-! ### `outerNext` as a function of the two scans -/

/-- `outerNext` written as a function of its two `normalize` results. -/
def fromScans (c : Nat) (L R : List Nat × Nat) : Outer :=
  let k := if 10 ≤ c then 1 else 0
  let t := c - 9 * k
  let u := c + L.2 - 10 * k
  let other := if R.2 == 0 then R.1.reverse ++ [t] else [1] ++ R.1.reverse
  { c := 2 * t, B := stripSuffix (2 * t) (List.zipWith (fun x y => x + y) (L.1 ++ [u]) other) }

theorem outerNext_eq_fromScans (c : Nat) (B : List Nat) :
    outerNext { c := c, B := B } =
      fromScans c (normalize B 0) (normalize B.reverse (if 10 ≤ c then 1 else 0)) := rfl

theorem stripSuffix_append_single (d : Nat) (w : List Nat) :
    stripSuffix d (w ++ [d]) = stripSuffix d w := by
  unfold stripSuffix
  simp [List.reverse_append, List.dropWhile_cons]

theorem zipWith_append_single (a b : List Nat) (x y : Nat) (h : a.length = b.length) :
    List.zipWith (fun x y => x + y) (a ++ [x]) (b ++ [y]) =
      List.zipWith (fun x y => x + y) a b ++ [x + y] := by
  induction a generalizing b with
  | nil =>
    cases b with
    | nil => rfl
    | cons _ _ => simp at h
  | cons p ps ih =>
    cases b with
    | nil => simp at h
    | cons q qs =>
      simp only [List.cons_append, List.zipWith_cons_cons]
      rw [ih qs (by simpa using h)]

theorem strip_zip_append (a b : List Nat) (x y d : Nat) (h : a.length = b.length)
    (hd : x + y = d) :
    stripSuffix d (List.zipWith (fun x y => x + y) (a ++ [x]) (b ++ [y])) =
      stripSuffix d (List.zipWith (fun x y => x + y) a b) := by
  rw [zipWith_append_single a b x y h, hd, stripSuffix_append_single]

/-! ### Phase arithmetic -/

theorem phase_facts (c κ : Nat) (hc : nonneutralPhase c) (hκ : κ ≤ 1) :
    (c + κ) / 10 = (if 10 ≤ c then 1 else 0) ∧
    (c + κ) % 10 = c + κ - 10 * (if 10 ≤ c then 1 else 0) ∧
    (c + (if 10 ≤ c then 1 else 0)) % 10 = c - 9 * (if 10 ≤ c then 1 else 0) ∧
    c + (if 10 ≤ c then 1 else 0) - 10 * (if 10 ≤ c then 1 else 0) =
      c - 9 * (if 10 ≤ c then 1 else 0) ∧
    c ≤ 18 := by
  unfold nonneutralPhase at hc
  simp only [List.mem_cons, List.mem_nil_iff, or_false] at hc
  have : κ = 0 ∨ κ = 1 := by omega
  rcases hc with h | h | h | h | h | h | h | h <;> subst h <;>
    rcases this with h | h <;> subst h <;> decide

/-- Appending one band coefficient does not change the exact exterior successor. -/
theorem outerNext_append_band (c : Nat) (B : List Nat) (hc : nonneutralPhase c)
    (hB : ∀ x ∈ B, x ≤ 18) :
    outerNext { c := c, B := B ++ [c] } = outerNext { c := c, B := B } := by
  have hκ := normalize_carry_le B 0 hB (by decide)
  have hk : (if 10 ≤ c then 1 else 0) ≤ 1 := by split <;> decide
  obtain ⟨hdiv, hmod, -, -, -⟩ := phase_facts c (normalize B 0).2 hc hκ
  obtain ⟨hdiv', -, hmod', ht, -⟩ := phase_facts c (if 10 ≤ c then 1 else 0) hc hk
  have hlen := normalize_length B 0
  have hlenR := normalize_length B.reverse (if 10 ≤ c then 1 else 0)
  rw [List.length_reverse] at hlenR
  rw [outerNext_eq_fromScans, outerNext_eq_fromScans, normalize_append_single, hdiv, hmod,
    List.reverse_append, show [c].reverse = [c] from rfl, List.singleton_append]
  simp only [normalize, hdiv', hmod']
  generalize normalize B 0 = L at *
  generalize normalize B.reverse (if 10 ≤ c then 1 else 0) = R at *
  generalize hK : (if 10 ≤ c then 1 else 0) = k at *
  generalize hT : c - 9 * k = t at *
  simp only [fromScans, hK, hT]
  split
  · try simp only [ht]
    rw [show (t :: R.1).reverse ++ [t] = (R.1.reverse ++ [t]) ++ [t] by simp,
      strip_zip_append _ _ _ _ _ (by simp [hlen, hlenR]) (by omega)]
  · try simp only [ht]
    rw [show [1] ++ (t :: R.1).reverse = ([1] ++ R.1.reverse) ++ [t] by simp,
      strip_zip_append _ _ _ _ _ (by simp [hlen, hlenR]) (by omega)]

theorem outerNext_append_replicate (c : Nat) (B : List Nat) (hc : nonneutralPhase c)
    (hB : ∀ x ∈ B, x ≤ 18) (m : Nat) :
    outerNext { c := c, B := B ++ List.replicate m c } = outerNext { c := c, B := B } := by
  have hc18 := (phase_facts c 0 hc (by decide)).2.2.2.2
  induction m with
  | zero => simp
  | succ m ih =>
    rw [List.replicate_succ', ← List.append_assoc, outerNext_append_band c _ hc, ih]
    intro x hx
    rcases List.mem_append.mp hx with h | h
    · exact hB x h
    · rw [List.eq_of_mem_replicate h]; exact hc18

/-- Words of equal length with equal little- and big-endian values have the same successor. -/
theorem outerNext_of_values (c : Nat) (B₁ B₂ : List Nat) (hl : B₁.length = B₂.length)
    (hlow : lowValue B₁ = lowValue B₂) (hhigh : highValue B₁ = highValue B₂) :
    outerNext { c := c, B := B₁ } = outerNext { c := c, B := B₂ } := by
  rw [outerNext_eq_fromScans, outerNext_eq_fromScans, normalize_eq B₁, normalize_eq B₂,
    normalize_eq B₁.reverse, normalize_eq B₂.reverse, List.length_reverse, List.length_reverse,
    lowValue_reverse, lowValue_reverse, hl, hlow, hhigh]

/-! ### Padding invariance of the two values -/

theorem zValue_append_band (c : Nat) (B : List Nat) :
    zValue c (B ++ [c]) = zValue c B := by
  unfold zValue
  rw [lowValue_append, List.length_append, List.length_singleton]
  simp only [lowValue, Nat.mul_zero, Nat.add_zero]
  push_cast
  rw [Int.pow_succ]
  generalize (10 : Int) ^ B.length = X
  generalize (lowValue B : Int) = V
  generalize (c : Int) = C
  have e1 : C * (X * 10 - 1) = 10 * (X * C) - C := by
    rw [Int.mul_sub, Int.mul_one, ← Int.mul_assoc, Int.mul_comm C X, Int.mul_comm (X * C) 10]
  have e2 : C * (X - 1) = X * C - C := by
    rw [Int.mul_sub, Int.mul_one, Int.mul_comm]
  rw [e1, e2, Int.mul_add]
  omega

theorem zValue_append_replicate (c : Nat) (B : List Nat) (m : Nat) :
    zValue c (B ++ List.replicate m c) = zValue c B := by
  induction m with
  | zero => simp
  | succ m ih => rw [List.replicate_succ', ← List.append_assoc, zValue_append_band, ih]

theorem rhoNum_append_band (c : Nat) (B : List Nat) :
    rhoNum c (B ++ [c]) = 10 * rhoNum c B := by
  unfold rhoNum
  rw [highValue_append_single]
  omega

theorem rhoNum_append_replicate (c : Nat) (B : List Nat) (m : Nat) :
    rhoNum c (B ++ List.replicate m c) = 10 ^ m * rhoNum c B := by
  induction m with
  | zero => simp
  | succ m ih =>
    rw [List.replicate_succ', ← List.append_assoc, rhoNum_append_band, ih, Nat.pow_succ,
      Nat.mul_comm (10 ^ m) 10, Nat.mul_assoc]

/-- Equal centered values at equal length give equal little-endian values. -/
theorem lowValue_of_zValue (c : Nat) (B₁ B₂ : List Nat) (hl : B₁.length = B₂.length)
    (hz : zValue c B₁ = zValue c B₂) : lowValue B₁ = lowValue B₂ := by
  unfold zValue at hz
  rw [hl] at hz
  generalize (c : Int) * ((10 : Int) ^ B₂.length - 1) = W at hz
  omega

/-! ### The factorization -/

theorem entries_le_of_valid (c : Nat) (B : List Nat) (hv : validOuter { c := c, B := B } = true) :
    ∀ x ∈ B, x ≤ 18 := by
  simp only [validOuter, Bool.and_eq_true, List.all_eq_true, decide_eq_true_eq] at hv
  exact hv.1.1

/-- One-sided form: the shorter word is padded with band coefficients. -/
theorem factorization_le (c : Nat) (B₁ B₂ : List Nat) (hc : nonneutralPhase c)
    (h₁ : ∀ x ∈ B₁, x ≤ 18) (hle : B₁.length ≤ B₂.length)
    (hz : zValue c B₁ = zValue c B₂)
    (hr : rhoNum c B₁ * 10 ^ B₂.length = rhoNum c B₂ * 10 ^ B₁.length) :
    outerNext { c := c, B := B₁ } = outerNext { c := c, B := B₂ } := by
  obtain ⟨m, hm⟩ : ∃ m, B₂.length = B₁.length + m := ⟨B₂.length - B₁.length, by omega⟩
  rw [← outerNext_append_replicate c B₁ hc h₁ m]
  have hl : (B₁ ++ List.replicate m c).length = B₂.length := by simp [hm]
  apply outerNext_of_values c _ _ hl
  · apply lowValue_of_zValue c _ _ hl
    rw [zValue_append_replicate, hz]
  · have hr' : rhoNum c (B₁ ++ List.replicate m c) = rhoNum c B₂ := by
      rw [rhoNum_append_replicate]
      rw [hm, Nat.pow_add] at hr
      apply Nat.eq_of_mul_eq_mul_right (Nat.pow_pos (by decide : 0 < 10) : 0 < 10 ^ B₁.length)
      rw [← hr, Nat.mul_comm (10 ^ m) (rhoNum c B₁), Nat.mul_assoc,
        Nat.mul_comm (10 ^ m) (10 ^ B₁.length)]
    unfold rhoNum at hr'
    omega

/-- **Factorization.** The exact exterior successor depends only on the band phase,
Agent #110's centered value `zValue`, and the real value `rhoNum / (9 * 10^|B|)`. -/
theorem target : Target := by
  intro c B₁ B₂ hc hv₁ hv₂ hz hr
  rcases Nat.le_total B₁.length B₂.length with h | h
  · exact factorization_le c B₁ B₂ hc (entries_le_of_valid c B₁ hv₁) h hz hr
  · exact (factorization_le c B₂ B₁ hc (entries_le_of_valid c B₂ hv₂) h hz.symm hr.symm).symm

/-- The same statement without the canonical head/tail conditions: only coefficient
bounds are used. -/
theorem factorization_general (c : Nat) (B₁ B₂ : List Nat) (hc : nonneutralPhase c)
    (h₁ : ∀ x ∈ B₁, x ≤ 18) (h₂ : ∀ x ∈ B₂, x ≤ 18)
    (hz : zValue c B₁ = zValue c B₂)
    (hr : rhoNum c B₁ * 10 ^ B₂.length = rhoNum c B₂ * 10 ^ B₁.length) :
    outerNext { c := c, B := B₁ } = outerNext { c := c, B := B₂ } := by
  rcases Nat.le_total B₁.length B₂.length with h | h
  · exact factorization_le c B₁ B₂ hc h₁ h hz hr
  · exact (factorization_le c B₂ B₁ hc h₂ h hz.symm hr.symm).symm

end Agent115.ExteriorFactorization
