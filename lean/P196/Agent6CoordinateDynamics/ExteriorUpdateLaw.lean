import P196.Agent6CoordinateDynamics.ExteriorObservationInjective

/-!
Agent #115. Explicit update law of the exact exterior map
`P196.Agent7.Finite.outerNext` in value coordinates.

For a word `B` of length `n` put `V = lowValue B`, `H = highValue B`,
`k = [10 ≤ c]`, `t = c − 9k`, `X = H + k`, `u = c + V / 10^n − 10k`, and let
`revN n y` be the value of the reversed `n`-digit representation of `y`.
The untrimmed successor word `rawSucc c B` (length `n + 1`) has

* `lowValue  = V % 10^n + u·10^n + (X < 10^n ? revN n X + t·10^n : 1 + 10·revN n X)`,
* `highValue = 10·revN n V + u + (X < 10^n ? 10·(X % 10^n) + t : 10^n + X % 10^n)`,

and `outerNext (c,B)` is `rawSucc c B` with trailing band coefficients `2t`
removed, so its `zValue` and `ρ` are explicit functions of `(c, V, H, n)`.
This is the written `(β, ρ)` update of `NOTE.md` in integer form: the digit
reversal `revN` is the only nonlinear ingredient. No hypotheses on `B` or `c`
are needed for the value identities. Core Lean only.
-/

namespace Agent115.ExteriorFactorization

open P196.Agent7.Finite

/-- Value of the reversed `n`-digit representation of `y`. -/
def revN (n y : Nat) : Nat := highValue (digitsOf n y)

/-- The successor word before trailing band coefficients are stripped. -/
def rawSucc (c : Nat) (B : List Nat) : List Nat :=
  let k := if 10 ≤ c then 1 else 0
  let t := c - 9 * k
  let left := normalize B 0
  let right := normalize B.reverse k
  let u := c + left.2 - 10 * k
  let other := if right.2 == 0 then right.1.reverse ++ [t] else [1] ++ right.1.reverse
  List.zipWith (fun x y => x + y) (left.1 ++ [u]) other

theorem outerNext_eq_strip (c : Nat) (B : List Nat) :
    outerNext { c := c, B := B } =
      { c := 2 * (c - 9 * (if 10 ≤ c then 1 else 0)),
        B := stripSuffix (2 * (c - 9 * (if 10 ≤ c then 1 else 0))) (rawSucc c B) } := rfl

/-! ### Value arithmetic -/

theorem lowValue_digitsOf (n v : Nat) : lowValue (digitsOf n v) = v % 10 ^ n := by
  induction n generalizing v with
  | zero => simp [digitsOf, lowValue, Nat.mod_one]
  | succ n ih =>
    simp only [digitsOf, lowValue, ih, Nat.pow_succ]
    rw [Nat.mul_comm (10 ^ n) 10, Nat.mod_mul]

theorem lowValue_zipWith (a b : List Nat) (h : a.length = b.length) :
    lowValue (List.zipWith (fun x y => x + y) a b) = lowValue a + lowValue b := by
  induction a generalizing b with
  | nil => cases b with
    | nil => rfl
    | cons _ _ => simp at h
  | cons x xs ih => cases b with
    | nil => simp at h
    | cons y ys =>
      simp only [List.zipWith_cons_cons, lowValue, ih ys (by simpa using h)]
      omega

theorem length_zipWith_eq (a b : List Nat) (h : a.length = b.length) :
    (List.zipWith (fun x y => x + y) a b).length = a.length := by
  simp [List.length_zipWith, h]

theorem highValue_zipWith (a b : List Nat) (h : a.length = b.length) :
    highValue (List.zipWith (fun x y => x + y) a b) = highValue a + highValue b := by
  induction a generalizing b with
  | nil => cases b with
    | nil => rfl
    | cons _ _ => simp at h
  | cons x xs ih => cases b with
    | nil => simp at h
    | cons y ys =>
      have h' : xs.length = ys.length := by simpa using h
      simp only [List.zipWith_cons_cons]
      rw [highValue_cons, highValue_cons, highValue_cons, ih ys h', length_zipWith_eq _ _ h',
        ← h', Nat.add_mul]
      omega

theorem lowValue_append_single (l : List Nat) (x : Nat) :
    lowValue (l ++ [x]) = lowValue l + 10 ^ l.length * x := by
  rw [lowValue_append]
  simp [lowValue]

theorem highValue_reverse (l : List Nat) : highValue l.reverse = lowValue l := by
  have := lowValue_reverse l.reverse
  rw [List.reverse_reverse] at this
  exact this.symm

/-! ### The law -/

theorem rawSucc_values (c : Nat) (B : List Nat) :
    lowValue (rawSucc c B) =
        lowValue B % 10 ^ B.length +
          (c + lowValue B / 10 ^ B.length - 10 * (if 10 ≤ c then 1 else 0)) * 10 ^ B.length +
          (if (highValue B + (if 10 ≤ c then 1 else 0)) / 10 ^ B.length = 0 then
            revN B.length (highValue B + (if 10 ≤ c then 1 else 0)) +
              (c - 9 * (if 10 ≤ c then 1 else 0)) * 10 ^ B.length
          else 1 + 10 * revN B.length (highValue B + (if 10 ≤ c then 1 else 0))) ∧
    highValue (rawSucc c B) =
        10 * revN B.length (lowValue B) +
          (c + lowValue B / 10 ^ B.length - 10 * (if 10 ≤ c then 1 else 0)) +
          (if (highValue B + (if 10 ≤ c then 1 else 0)) / 10 ^ B.length = 0 then
            10 * ((highValue B + (if 10 ≤ c then 1 else 0)) % 10 ^ B.length) +
              (c - 9 * (if 10 ≤ c then 1 else 0))
          else 10 ^ B.length + (highValue B + (if 10 ≤ c then 1 else 0)) % 10 ^ B.length) := by
  have hL := normalize_eq B 0
  have hR := normalize_eq B.reverse (if 10 ≤ c then 1 else 0)
  rw [List.length_reverse, lowValue_reverse] at hR
  rw [Nat.add_zero] at hL
  unfold rawSucc
  simp only [hL, hR]
  generalize (if 10 ≤ c then 1 else 0) = k
  generalize hn : B.length = n
  generalize lowValue B = V
  generalize highValue B = H
  have hd : ∀ v, (digitsOf n v).length = n := fun v => digitsOf_length n v
  by_cases ho : (H + k) / 10 ^ n = 0
  · have hb : ((H + k) / 10 ^ n == 0) = true := by simp [ho]
    simp only [hb, ↓reduceIte]
    rw [if_pos ho, if_pos ho]
    have hlen : (digitsOf n V ++ [c + V / 10 ^ n - 10 * k]).length =
        ((digitsOf n (H + k)).reverse ++ [c - 9 * k]).length := by simp [hd]
    refine ⟨?_, ?_⟩
    · rw [lowValue_zipWith _ _ hlen, lowValue_append_single, lowValue_append_single,
        lowValue_digitsOf, List.length_reverse, hd, hd, lowValue_reverse]
      unfold revN
      rw [Nat.mul_comm (10 ^ n) (c + V / 10 ^ n - 10 * k), Nat.mul_comm (10 ^ n) (c - 9 * k)]
      all_goals omega
    · rw [highValue_zipWith _ _ hlen, highValue_append_single, highValue_append_single,
        highValue_reverse, lowValue_digitsOf]
      unfold revN
      omega
  · have hb : ((H + k) / 10 ^ n == 0) = false := by simp [ho]
    simp only [hb, Bool.false_eq_true, ↓reduceIte]
    rw [if_neg ho, if_neg ho]
    have hlen : (digitsOf n V ++ [c + V / 10 ^ n - 10 * k]).length =
        ([1] ++ (digitsOf n (H + k)).reverse).length := by simp [hd]
    refine ⟨?_, ?_⟩
    · rw [lowValue_zipWith _ _ hlen, lowValue_append_single, lowValue_digitsOf, hd]
      simp only [List.singleton_append, lowValue]
      rw [lowValue_reverse]
      unfold revN
      rw [Nat.mul_comm (10 ^ n) (c + V / 10 ^ n - 10 * k)]
      all_goals omega
    · rw [highValue_zipWith _ _ hlen, highValue_append_single, List.singleton_append,
        highValue_cons, List.length_reverse, hd, highValue_reverse, lowValue_digitsOf]
      unfold revN
      omega

/-! ### Observation of the successor -/

theorem takeWhile_eq_mem (d : Nat) (l : List Nat) :
    ∀ x ∈ l.takeWhile (fun x => x == d), x = d := by
  induction l with
  | nil => simp
  | cons a l ih =>
    intro x hx
    by_cases h : (a == d) = true
    · rw [List.takeWhile_cons_of_pos (p := fun x => x == d) h] at hx
      rcases List.mem_cons.mp hx with hx | hx
      · subst hx; simpa using h
      · exact ih x hx
    · rw [List.takeWhile_cons_of_neg (p := fun x => x == d) h] at hx
      simp at hx

theorem stripSuffix_spec (d : Nat) (w : List Nat) :
    ∃ m, stripSuffix d w ++ List.replicate m d = w := by
  unfold stripSuffix
  have hall := takeWhile_eq_mem d w.reverse
  have hsplit := List.takeWhile_append_dropWhile (p := fun x => x == d) (l := w.reverse)
  generalize w.reverse.takeWhile (fun x => x == d) = T at hall hsplit ⊢
  generalize w.reverse.dropWhile (fun x => x == d) = D at hsplit ⊢
  refine ⟨T.length, ?_⟩
  have hw : w = D.reverse ++ T.reverse := by
    rw [← List.reverse_append, hsplit, List.reverse_reverse]
  have hT : T.reverse = List.replicate T.length d := by
    apply List.eq_replicate_iff.mpr
    exact ⟨by simp, fun b hb => hall b (List.mem_reverse.mp hb)⟩
  rw [hw, hT]

theorem rawSucc_length (c : Nat) (B : List Nat) : (rawSucc c B).length = B.length + 1 := by
  unfold rawSucc
  dsimp only
  have h1 := normalize_length B 0
  generalize (if 10 ≤ c then 1 else 0) = k
  have h2 := normalize_length B.reverse k
  rw [List.length_reverse] at h2
  generalize normalize B 0 = Lp at h1 ⊢
  generalize normalize B.reverse k = Rp at h2 ⊢
  split <;> simp [List.length_zipWith, h1, h2]

/-- The successor's centered value and real value, in terms of the explicit
values of `rawSucc` (`rawSucc_values`). -/
theorem successor_observation (c : Nat) (B : List Nat) :
    zValue (2 * (c - 9 * (if 10 ≤ c then 1 else 0))) (outerNext { c := c, B := B }).B =
        9 * (lowValue (rawSucc c B) : Int) -
          ((2 * (c - 9 * (if 10 ≤ c then 1 else 0)) : Nat) : Int) * ((10 : Int) ^ (B.length + 1) - 1) ∧
    rhoNum (2 * (c - 9 * (if 10 ≤ c then 1 else 0))) (outerNext { c := c, B := B }).B *
        10 ^ (B.length + 1) =
      (9 * highValue (rawSucc c B) + 2 * (c - 9 * (if 10 ≤ c then 1 else 0))) *
        10 ^ (outerNext { c := c, B := B }).B.length := by
  rw [outerNext_eq_strip]
  generalize hd : 2 * (c - 9 * (if 10 ≤ c then 1 else 0)) = d
  obtain ⟨m, hm⟩ := stripSuffix_spec d (rawSucc c B)
  have hlen := rawSucc_length c B
  generalize stripSuffix d (rawSucc c B) = S at hm ⊢
  rw [← hm] at hlen
  simp only [List.length_append, List.length_replicate] at hlen
  refine ⟨?_, ?_⟩
  · have hz := zValue_append_replicate d S m
    rw [hm] at hz
    dsimp only
    rw [← hz]
    unfold zValue
    rw [rawSucc_length]
  · have hr := rhoNum_append_replicate d S m
    rw [hm] at hr
    unfold rhoNum at hr ⊢
    dsimp only
    rw [← hlen, Nat.pow_add, hr]
    simp only [Nat.mul_comm, Nat.mul_assoc, Nat.mul_left_comm]

end Agent115.ExteriorFactorization
