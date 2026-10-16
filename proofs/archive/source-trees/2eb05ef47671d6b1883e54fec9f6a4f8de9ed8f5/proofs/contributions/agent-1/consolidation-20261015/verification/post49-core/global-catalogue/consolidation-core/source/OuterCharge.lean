import Lean

/-! All-width alternating-charge algebra for the exact outer list map.
The actual whole-word semiconjugacy is a written dependency, not assumed
as an axiom. This standalone module uses the same explicit list operation
as OuterEscape.lean. No theorem here asserts decimal Lychrel existence. -/
namespace P196.Agent3.Charge

set_option maxRecDepth 100000
set_option maxHeartbeats 2000000

def alt : List Nat → Int
  | [] => 0
  | x :: xs => (x : Int) - alt xs

def sign : List Nat → Int
  | [] => 1
  | _ :: xs => -sign xs

def charge (c : Nat) (w : List Nat) : Int := 2 * alt w + sign w * (c : Int)

def normalize : List Nat → Nat → List Nat × Nat
  | [], e => ([], e)
  | x :: xs, e =>
    let next := normalize xs ((x + e) / 10)
    ((x + e) % 10 :: next.1, next.2)

def trim (c : Nat) (w : List Nat) : List Nat :=
  (w.reverse.dropWhile (fun x => x == c)).reverse

def step (c : Nat) (B : List Nat) : Nat × List Nat :=
  let k := if c < 9 then 0 else 1
  let t := c - 9 * k
  let left := normalize B 0
  let right := normalize B.reverse k
  let u := c + left.2 - 10 * k
  let R := if right.2 = 1 then 1 :: right.1.reverse else right.1.reverse ++ [t]
  let raw := List.zipWith (fun x y => x + y) (left.1 ++ [u]) R
  (2 * t, trim (2 * t) raw)

theorem sign_cases (w : List Nat) : sign w = 1 ∨ sign w = -1 := by
  induction w with
  | nil => simp [sign]
  | cons x xs ih =>
    simp only [sign]
    rcases ih with h | h <;> simp [h]

theorem sign_append (a b : List Nat) : sign (a ++ b) = sign a * sign b := by
  induction a with
  | nil => simp [sign]
  | cons x xs ih => simp [sign, ih, Int.neg_mul]

theorem alt_append (a b : List Nat) : alt (a ++ b) = alt a + sign a * alt b := by
  induction a with
  | nil => simp [alt, sign]
  | cons x xs ih =>
    simp only [List.cons_append, alt, sign, ih, Int.neg_mul]
    omega

theorem sign_reverse (w : List Nat) : sign w.reverse = sign w := by
  induction w with
  | nil => simp [sign]
  | cons x xs ih => simp [List.reverse_cons, sign_append, sign, ih]

theorem alt_reverse (w : List Nat) : alt w.reverse = -sign w * alt w := by
  induction w with
  | nil => simp [alt, sign]
  | cons x xs ih =>
    rw [List.reverse_cons, alt_append, ih, sign_reverse]
    rcases sign_cases xs with h | h <;> simp [alt, sign, h] <;> omega

theorem sign_of_length (a b : List Nat) (h : a.length = b.length) : sign a = sign b := by
  induction a generalizing b with
  | nil =>
    cases b with
    | nil => rfl
    | cons x xs => simp at h
  | cons x xs ih =>
    cases b with
    | nil => simp at h
    | cons y ys =>
      simp only [List.length_cons, Nat.add_right_cancel_iff] at h
      simp only [sign, ih ys h]

theorem normalize_length (w : List Nat) (e : Nat) : (normalize w e).1.length = w.length := by
  induction w generalizing e with
  | nil => rfl
  | cons x xs ih => simp [normalize, ih]

theorem normalize_sign (w : List Nat) (e : Nat) : sign (normalize w e).1 = sign w :=
  sign_of_length _ _ (normalize_length w e)

theorem normalize_carry (w : List Nat) (e : Nat)
    (he : e ≤ 1) (hw : ∀ x ∈ w, x ≤ 18) : (normalize w e).2 ≤ 1 := by
  induction w generalizing e with
  | nil => exact he
  | cons x xs ih =>
    have hx : x ≤ 18 := hw x (by simp)
    exact ih ((x + e) / 10) (by omega) (by intro y hy; exact hw y (by simp [hy]))

theorem normalize_alt (w : List Nat) (e : Nat) :
    (alt (normalize w e).1 + sign w * ((normalize w e).2 : Int) - alt w - (e : Int)) % 11 = 0 := by
  induction w generalizing e with
  | nil => simp [normalize, alt, sign]
  | cons x xs ih =>
    have h := ih ((x + e) / 10)
    rcases sign_cases xs with hs | hs
    all_goals
      simp only [normalize, alt, sign, hs, Int.one_mul, Int.neg_one_mul, Int.neg_neg] at *
      omega

theorem alt_zip (a b : List Nat) (h : a.length = b.length) :
    alt (List.zipWith (fun x y => x + y) a b) = alt a + alt b := by
  induction a generalizing b with
  | nil =>
    cases b with
    | nil => simp [alt]
    | cons x xs => simp at h
  | cons x xs ih =>
    cases b with
    | nil => simp at h
    | cons y ys =>
      have hh : xs.length = ys.length := by simpa using h
      simp only [List.zipWith_cons_cons, alt, Int.ofNat_add, ih ys hh]
      omega

theorem charge_append_bulk (c : Nat) (w : List Nat) : charge c (w ++ [c]) = charge c w := by
  rw [charge, alt_append, sign_append]
  rcases sign_cases w with h | h <;> simp [charge, alt, sign, h] <;> omega

theorem charge_trim (c : Nat) (w : List Nat) : charge c (trim c w) = charge c w := by
  have h (v : List Nat) :
      charge c (v.dropWhile (fun x => x == c)).reverse = charge c v.reverse := by
    induction v with
    | nil => simp [charge, alt, sign]
    | cons x xs ih =>
      by_cases hc : x = c
      · subst x
        simpa [List.dropWhile_cons, List.reverse_cons, charge_append_bulk] using ih
      · simp [List.dropWhile_cons_of_neg, hc]
  simpa [trim] using h w.reverse

def rawZero (c k : Nat) (B : List Nat) : List Nat :=
  let D := normalize B 0
  let R := normalize B.reverse k
  List.zipWith (fun x y => x + y)
    (D.1 ++ [c + D.2 - 10 * k]) (R.1.reverse ++ [c - 9 * k])

def rawOne (c k : Nat) (B : List Nat) : List Nat :=
  let D := normalize B 0
  let R := normalize B.reverse k
  List.zipWith (fun x y => x + y)
    (D.1 ++ [c + D.2 - 10 * k]) (1 :: R.1.reverse)

theorem raw_zero_charge (c k : Nat) (B : List Nat) (hc : 10 * k ≤ c)
    (hg : (normalize B.reverse k).2 = 0) :
    (charge (2 * (c - 9 * k)) (rawZero c k B) - 2 * charge c B) % 11 = 0 := by
  let D := (normalize B 0).1
  let e := (normalize B 0).2
  let R := (normalize B.reverse k).1
  have hD := normalize_alt B 0
  have hR := normalize_alt B.reverse k
  have hDL : D.length = B.length := normalize_length B 0
  have hRL : R.length = B.length := by simpa [R] using normalize_length B.reverse k
  have hDS : sign D = sign B := normalize_sign B 0
  have hRS : sign R = sign B := by simpa [R, sign_reverse] using normalize_sign B.reverse k
  have hsraw : sign (rawZero c k B) = -sign B := by
    have hh : (rawZero c k B).length = (B ++ [0]).length := by
      simp [rawZero, normalize_length]
    simpa [sign_append, sign] using sign_of_length _ _ hh
  have ha : alt (rawZero c k B) =
      alt D + sign B * ((c + e - 10 * k : Nat) : Int) - sign B * alt R +
      sign B * ((c - 9 * k : Nat) : Int) := by
    unfold rawZero
    rw [alt_zip _ _ (by simp [normalize_length])]
    simp only [alt_append, alt_reverse, normalize_sign, sign_reverse, alt, Int.sub_zero]
    rcases sign_cases B with hs | hs <;> simp [D, R, e, hs] <;> omega
  simp only [hg, sign_reverse, alt_reverse] at hR
  change (alt D + sign B * (e : Int) - alt B - 0) % 11 = 0 at hD
  change (alt R + sign B * (0 : Int) - (-sign B * alt B) - (k : Int)) % 11 = 0 at hR
  rw [charge, ha, hsraw]
  rcases sign_cases B with hs | hs
  all_goals
    simp only [charge, hs, Int.one_mul, Int.neg_one_mul, Int.neg_neg, Int.zero_mul,
      Int.mul_zero, Int.ofNat_mul] at *
    omega

theorem raw_one_charge (c k : Nat) (B : List Nat) (hc : 10 * k ≤ c)
    (hg : (normalize B.reverse k).2 = 1) :
    charge (2 * (c - 9 * k)) (rawOne c k B) % 11 = 0 := by
  let D := (normalize B 0).1
  let e := (normalize B 0).2
  let R := (normalize B.reverse k).1
  have hD := normalize_alt B 0
  have hR := normalize_alt B.reverse k
  have hsraw : sign (rawOne c k B) = -sign B := by
    have hh : (rawOne c k B).length = (B ++ [0]).length := by
      simp [rawOne, normalize_length]
    simpa [sign_append, sign] using sign_of_length _ _ hh
  have ha : alt (rawOne c k B) =
      alt D + sign B * ((c + e - 10 * k : Nat) : Int) + 1 + sign B * alt R := by
    unfold rawOne
    rw [alt_zip _ _ (by simp [normalize_length])]
    simp only [alt_append, alt, alt_reverse, normalize_sign, sign_reverse, Int.sub_zero]
    rcases sign_cases B with hs | hs <;> simp [D, R, e, hs] <;> omega
  simp only [hg, sign_reverse, alt_reverse] at hR
  change (alt D + sign B * (e : Int) - alt B - 0) % 11 = 0 at hD
  change (alt R + sign B * (1 : Int) - (-sign B * alt B) - (k : Int)) % 11 = 0 at hR
  rw [charge, ha, hsraw]
  rcases sign_cases B with hs | hs
  all_goals
    simp only [charge, hs, Int.one_mul, Int.neg_one_mul, Int.neg_neg, Int.zero_mul,
      Int.mul_zero, Int.ofNat_mul] at *
    omega

theorem step_charge_nonoverflow (c : Nat) (B : List Nat)
    (hc0 : 1 ≤ c) (hc1 : c ≤ 17) (hc9 : c ≠ 9)
    (hg : (normalize B.reverse (if c < 9 then 0 else 1)).2 = 0) :
    (charge (step c B).1 (step c B).2 - 2 * charge c B) % 11 = 0 := by
  let k := if c < 9 then 0 else 1
  have hck : 10 * k ≤ c := by dsimp [k]; split <;> omega
  have h := raw_zero_charge c k B hck hg
  simpa [step, hg, rawZero, charge_trim, k] using h

theorem step_charge_overflow (c : Nat) (B : List Nat)
    (hc0 : 1 ≤ c) (hc1 : c ≤ 17) (hc9 : c ≠ 9)
    (hg : (normalize B.reverse (if c < 9 then 0 else 1)).2 = 1) :
    charge (step c B).1 (step c B).2 % 11 = 0 := by
  let k := if c < 9 then 0 else 1
  have hck : 10 * k ≤ c := by dsimp [k]; split <;> omega
  have h := raw_one_charge c k B hck hg
  simpa [step, hg, rawOne, charge_trim, k] using h

theorem step_charge_preserves_zero (c : Nat) (B : List Nat)
    (hc0 : 1 ≤ c) (hc1 : c ≤ 17) (hc9 : c ≠ 9)
    (hB : ∀ x ∈ B, x ≤ 18) (hz : charge c B % 11 = 0) :
    charge (step c B).1 (step c B).2 % 11 = 0 := by
  have hg : (normalize B.reverse (if c < 9 then 0 else 1)).2 ≤ 1 := by
    apply normalize_carry
    · split <;> omega
    · intro x hx
      exact hB x (by simpa using hx)
  by_cases hzero : (normalize B.reverse (if c < 9 then 0 else 1)).2 = 0
  · have h := step_charge_nonoverflow c B hc0 hc1 hc9 hzero
    omega
  · have hone : (normalize B.reverse (if c < 9 then 0 else 1)).2 = 1 := by omega
    exact step_charge_overflow c B hc0 hc1 hc9 hone

#print axioms sign_cases
#print axioms sign_append
#print axioms alt_append
#print axioms sign_reverse
#print axioms alt_reverse
#print axioms sign_of_length
#print axioms normalize_length
#print axioms normalize_sign
#print axioms normalize_carry
#print axioms normalize_alt
#print axioms alt_zip
#print axioms charge_append_bulk
#print axioms charge_trim
#print axioms raw_zero_charge
#print axioms raw_one_charge
#print axioms step_charge_nonoverflow
#print axioms step_charge_overflow
#print axioms step_charge_preserves_zero

end P196.Agent3.Charge
