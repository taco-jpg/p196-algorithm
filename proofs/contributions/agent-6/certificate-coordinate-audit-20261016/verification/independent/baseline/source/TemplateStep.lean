import Std

/-!
Agent #109: kernel-checked actual whole-word bridge for the complementary
two-gap template of
`proofs/contributions/2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md`.

Definitions `Word`, `zipAdd`, `pair`, `normalize`, `stepWord`, `template`
are verbatim copies of Agent #8's `PeriodObstructions.lean`; `reverseAux`,
`reverseFuel`, `reverse10`, `step` are verbatim copies of
`Lychrel196` in `proofs/research/continuation/LychrelDigitSums.lean`.
`Compat.lean` proves the copies equal to the originals.

Core Lean 4.19.0 + Std only; see the token scan in `build.sh` and the axiom report of `Audit.lean`.
No cycle, safe orbit, Lychrel witness or statement about 196 is claimed.
-/

namespace Agent109

abbrev Word := List Nat

/-! ## Verbatim copies of Agent #8 definitions -/

def zipAdd : Word → Word → Word
  | x :: xs, y :: ys => (x + y) :: zipAdd xs ys
  | _, _ => []

def pair (w : Word) : Word := zipAdd w w.reverse

def normalize : Word → Nat → Word
  | [], e => if e = 0 then [] else [e]
  | x :: xs, e => ((x + e) % 10) :: normalize xs ((x + e) / 10)

def stepWord (w : Word) : Word := pair (normalize w 0)

def template (c : Nat) (B A C : Word) (g h : Nat) : Word :=
  B ++ List.replicate g c ++ A ++ List.replicate h (18 - c) ++ C ++
    List.replicate h (18 - c) ++ A.reverse ++ List.replicate g c ++ B.reverse

/-! ## Basic `zipAdd` algebra -/

theorem zipAdd_eq_zipWith (a b : Word) : zipAdd a b = List.zipWith (· + ·) a b := by
  induction a generalizing b with
  | nil => cases b <;> rfl
  | cons x xs ih =>
    cases b with
    | nil => rfl
    | cons y ys => simp [zipAdd, ih]

theorem zipAdd_append (a a' b b' : Word) (h : a.length = b.length) :
    zipAdd (a ++ a') (b ++ b') = zipAdd a b ++ zipAdd a' b' := by
  simp only [zipAdd_eq_zipWith]
  exact List.zipWith_append h

theorem zipAdd_length (a b : Word) (h : a.length = b.length) :
    (zipAdd a b).length = a.length := by
  simp [zipAdd_eq_zipWith, List.length_zipWith, h]

theorem zipAdd_comm (a b : Word) : zipAdd a b = zipAdd b a := by
  induction a generalizing b with
  | nil => cases b <;> rfl
  | cons x xs ih =>
    cases b with
    | nil => rfl
    | cons y ys => simp [zipAdd, ih, Nat.add_comm]

theorem zipAdd_reverse (a b : Word) (h : a.length = b.length) :
    (zipAdd a b).reverse = zipAdd a.reverse b.reverse := by
  induction a generalizing b with
  | nil => cases b <;> rfl
  | cons x xs ih =>
    cases b with
    | nil => simp at h
    | cons y ys =>
      simp only [List.length_cons, Nat.add_right_cancel_iff] at h
      simp only [zipAdd, List.reverse_cons]
      rw [ih ys h, zipAdd_append _ _ _ _ (by simp [h])]
      rfl

theorem zipAdd_replicate (m p q : Nat) :
    zipAdd (List.replicate m p) (List.replicate m q) = List.replicate m (p + q) := by
  induction m with
  | zero => rfl
  | succ m ih => simp [List.replicate_succ, zipAdd, ih]

/-! ## Normalization with an explicit final carry -/

/-- Same-length normalized digit block and final carry. -/
def norm : Word → Nat → Word × Nat
  | [], e => ([], e)
  | x :: xs, e => (((x + e) % 10) :: (norm xs ((x + e) / 10)).1,
                   (norm xs ((x + e) / 10)).2)

def carryWord (e : Nat) : Word := if e = 0 then [] else [e]

theorem normalize_eq_norm (w : Word) (e : Nat) :
    normalize w e = (norm w e).1 ++ carryWord (norm w e).2 := by
  induction w generalizing e with
  | nil => simp [normalize, norm, carryWord]
  | cons x xs ih => simp [normalize, norm, ih]

theorem norm_length (w : Word) (e : Nat) : (norm w e).1.length = w.length := by
  induction w generalizing e with
  | nil => rfl
  | cons x xs ih => simp [norm, ih]

theorem norm_append (a b : Word) (e : Nat) :
    norm (a ++ b) e = ((norm a e).1 ++ (norm b (norm a e).2).1,
                       (norm b (norm a e).2).2) := by
  induction a generalizing e with
  | nil => rfl
  | cons x xs ih => simp [norm, ih]

/-- Coefficients at most 18 with incoming carry at most one. -/
def Bounded (w : Word) : Prop := ∀ x ∈ w, x ≤ 18

theorem norm_carry_le (w : Word) (e : Nat) (hw : Bounded w) (he : e ≤ 1) :
    (norm w e).2 ≤ 1 := by
  induction w generalizing e with
  | nil => simpa [norm] using he
  | cons x xs ih =>
    simp only [norm]
    apply ih
    · intro y hy; exact hw y (by simp [hy])
    · have := hw x (by simp); omega

theorem norm_digit_lt (w : Word) (e : Nat) :
    ∀ y ∈ (norm w e).1, y < 10 := by
  induction w generalizing e with
  | nil => simp [norm]
  | cons x xs ih =>
    intro y hy
    simp only [norm, List.mem_cons] at hy
    rcases hy with hy | hy
    · subst hy; exact Nat.mod_lt _ (by decide)
    · exact ih _ y hy

/-! ## Constant bands -/

def kOf (x : Nat) : Nat := if 10 ≤ x then 1 else 0
def tOf (x : Nat) : Nat := x - 9 * kOf x

/-- A legal band phase. -/
def Phase (x : Nat) : Prop := 1 ≤ x ∧ x ≤ 17 ∧ x ≠ 9

theorem norm_band_tail (x m : Nat) (hx : x ≤ 18) :
    norm (List.replicate m x) (kOf x) = (List.replicate m (tOf x), kOf x) := by
  induction m with
  | zero => rfl
  | succ m ih =>
    have h1 : (x + kOf x) % 10 = tOf x := by
      unfold tOf kOf; split <;> omega
    have h2 : (x + kOf x) / 10 = kOf x := by
      unfold kOf; split <;> omega
    simp only [List.replicate_succ, norm, h1, h2, ih]

/-- First column of a band: digit `x+e-10k_x`, then the uniform tail. -/
theorem norm_band (x m e : Nat) (hx : x ≤ 18) (hx9 : x ≠ 9) (he : e ≤ 1) :
    norm (List.replicate (m + 1) x) e =
      ((x + e - 10 * kOf x) :: List.replicate m (tOf x), kOf x) := by
  have h1 : (x + e) % 10 = x + e - 10 * kOf x := by
    unfold kOf; split <;> omega
  have h2 : (x + e) / 10 = kOf x := by
    unfold kOf; split <;> omega
  simp only [List.replicate_succ, norm, h1, h2, norm_band_tail x m hx]

theorem complement_k (c : Nat) (hc : Phase c) : kOf c + kOf (18 - c) = 1 := by
  unfold Phase at hc; unfold kOf; split <;> split <;> omega

theorem complement_t (c : Nat) (hc : Phase c) : tOf c + tOf (18 - c) = 9 := by
  unfold Phase at hc; unfold tOf kOf; split <;> split <;> omega

theorem complement_phase (c : Nat) (hc : Phase c) : Phase (18 - c) := by
  simp only [Phase] at *; omega

theorem next_phase (c : Nat) (hc : Phase c) : Phase (tOf c + tOf c) := by
  simp only [Phase] at *
  by_cases h : 10 ≤ c <;> simp [tOf, kOf, h] <;> omega

theorem next_complement (c : Nat) (hc : Phase c) :
    18 - (tOf c + tOf c) = tOf (18 - c) + tOf (18 - c) := by
  have := complement_t c hc; omega

/-! ## The whole template: normalization identity (5) -/

/-- Block data (3) of the method note: normalized blocks and their carries. -/
structure Data where
  DB : Word
  DA : Word
  DC : Word
  DRA : Word
  DRB : Word
  e0 : Nat
  e1 : Nat
  e2 : Nat
  e3 : Nat
  γ : Nat

def data (c : Nat) (B A C : Word) : Data :=
  { DB := (norm B 0).1, e0 := (norm B 0).2,
    DA := (norm A (kOf c)).1, e1 := (norm A (kOf c)).2,
    DC := (norm C (kOf (18 - c))).1, e2 := (norm C (kOf (18 - c))).2,
    DRA := (norm A.reverse (kOf (18 - c))).1, e3 := (norm A.reverse (kOf (18 - c))).2,
    DRB := (norm B.reverse (kOf c)).1, γ := (norm B.reverse (kOf c)).2 }

/-- Entrance digits (4). -/
def u0 (c : Nat) (B A C : Word) : Nat := c + (data c B A C).e0 - 10 * kOf c
def u1 (c : Nat) (B A C : Word) : Nat := (18 - c) + (data c B A C).e1 - 10 * kOf (18 - c)
def u2 (c : Nat) (B A C : Word) : Nat := (18 - c) + (data c B A C).e2 - 10 * kOf (18 - c)
def u3 (c : Nat) (B A C : Word) : Nat := c + (data c B A C).e3 - 10 * kOf c

/-- The digit word (5), for band lengths `g+1`, `h+1` (without the overflow digit). -/
def digitWord (c : Nat) (B A C : Word) (g h : Nat) : Word :=
  (data c B A C).DB ++ (u0 c B A C :: List.replicate g (tOf c)) ++ (data c B A C).DA ++
    (u1 c B A C :: List.replicate h (tOf (18 - c))) ++ (data c B A C).DC ++
    (u2 c B A C :: List.replicate h (tOf (18 - c))) ++ (data c B A C).DRA ++
    (u3 c B A C :: List.replicate g (tOf c)) ++ (data c B A C).DRB

theorem bounded_reverse (w : Word) (h : Bounded w) : Bounded w.reverse := by
  intro x hx; exact h x (List.mem_reverse.mp hx)

/-- Identity (5): the actual carry normalization of the template, for all band
lengths at least one, with no freely chosen carries. -/
theorem norm_template (c : Nat) (B A C : Word) (g h : Nat) (hc : Phase c)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C) :
    norm (template c B A C (g + 1) (h + 1)) 0 =
      (digitWord c B A C g h, (data c B A C).γ) := by
  have hc' := complement_phase c hc
  unfold Phase at hc hc'
  have kc : kOf c ≤ 1 := by unfold kOf; split <;> omega
  have kd : kOf (18 - c) ≤ 1 := by unfold kOf; split <;> omega
  have b0 := norm_carry_le B 0 hB (by decide)
  have b1 := norm_carry_le A (kOf c) hA kc
  have b2 := norm_carry_le C (kOf (18 - c)) hC kd
  have b3 := norm_carry_le A.reverse (kOf (18 - c)) (bounded_reverse A hA) kd
  simp only [template, norm_append,
    norm_band c g _ (by omega) hc.2.2 b0,
    norm_band (18 - c) h _ (by omega) hc'.2.2 b1,
    norm_band (18 - c) h _ (by omega) hc'.2.2 b2,
    norm_band c g _ (by omega) hc.2.2 b3]
  simp [digitWord, data, u0, u1, u2, u3]

/-- Identity (5) for Agent #8's `normalize`: digit word plus the overflow digit. -/
theorem normalize_template (c : Nat) (B A C : Word) (g h : Nat) (hc : Phase c)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C) :
    normalize (template c B A C (g + 1) (h + 1)) 0 =
      digitWord c B A C g h ++ carryWord (data c B A C).γ := by
  rw [normalize_eq_norm, norm_template c B A C g h hc hB hA hC]

theorem gamma_le (c : Nat) (B A C : Word) (hB : Bounded B) :
    (data c B A C).γ ≤ 1 := by
  exact norm_carry_le B.reverse (kOf c) (bounded_reverse B hB)
    (by unfold kOf; split <;> omega)

/-! ## Pairing a symmetric-shaped digit word -/

theorem pair_split (X1 X2 X3 X4 X5 : Word) (m n p q : Nat)
    (h15 : X1.length = X5.length) (h24 : X2.length = X4.length) :
    pair (X1 ++ List.replicate m p ++ X2 ++ List.replicate n q ++ X3 ++
          List.replicate n q ++ X4 ++ List.replicate m p ++ X5) =
      zipAdd X1 X5.reverse ++ List.replicate m (p + p) ++ zipAdd X2 X4.reverse ++
        List.replicate n (q + q) ++ pair X3 ++ List.replicate n (q + q) ++
        (zipAdd X2 X4.reverse).reverse ++ List.replicate m (p + p) ++
        (zipAdd X1 X5.reverse).reverse := by
  unfold pair
  simp only [List.reverse_append, List.reverse_replicate, List.append_assoc]
  rw [zipAdd_append _ _ _ _ (by simp [h15]),
      zipAdd_append _ _ _ _ (by simp),
      zipAdd_append _ _ _ _ (by simp [h24]),
      zipAdd_append _ _ _ _ (by simp),
      zipAdd_append _ _ _ _ (by simp),
      zipAdd_append _ _ _ _ (by simp),
      zipAdd_append _ _ _ _ (by simp [h24]),
      zipAdd_append _ _ _ _ (by simp)]
  rw [zipAdd_reverse X2 X4.reverse (by simp [h24]),
      zipAdd_reverse X1 X5.reverse (by simp [h15])]
  simp only [List.reverse_reverse, zipAdd_replicate]
  rw [zipAdd_comm X4 X2.reverse, zipAdd_comm X5 X1.reverse]

/-! ## Identity (8): one actual step of the template -/

/-- Returned exterior block `B_r` of (6)/(7). -/
def Br (c : Nat) (B A C : Word) : Word :=
  if (data c B A C).γ = 0 then
    zipAdd ((data c B A C).DB ++ [u0 c B A C]) ((data c B A C).DRB.reverse ++ [tOf c])
  else
    zipAdd ((data c B A C).DB ++ [u0 c B A C]) ([1] ++ (data c B A C).DRB.reverse)

/-- Returned interface block `A_r` of (6)/(7). -/
def Ar (c : Nat) (B A C : Word) : Word :=
  if (data c B A C).γ = 0 then
    zipAdd ([tOf c] ++ (data c B A C).DA ++ [u1 c B A C])
      ([u3 c B A C] ++ (data c B A C).DRA.reverse ++ [tOf (18 - c)])
  else
    zipAdd ((data c B A C).DA ++ [u1 c B A C])
      ([u3 c B A C] ++ (data c B A C).DRA.reverse)

/-- Returned central block `C_r` of (6)/(7). -/
def Cr (c : Nat) (B A C : Word) : Word :=
  if (data c B A C).γ = 0 then
    pair ([tOf (18 - c)] ++ (data c B A C).DC ++ [u2 c B A C])
  else
    pair ((data c B A C).DC ++ [u2 c B A C])

/-- **Identity (8).** For every phase `c ∈ {1,…,17}∖{9}`, all blocks with
coefficients at most 18 (no symmetry or positivity needed at word level) and all
band lengths `g+2, h+2 ≥ 2`, one actual step (Agent #8 `stepWord`) of the template
is again a template with phase `2 t_c`, blocks `B_r,A_r,C_r` and band lengths
`g+γ, h+γ`, where `γ` is the actual final carry. -/
theorem stepWord_template (c : Nat) (B A C : Word) (g h : Nat) (hc : Phase c)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C) :
    stepWord (template c B A C (g + 2) (h + 2)) =
      template (tOf c + tOf c) (Br c B A C) (Ar c B A C) (Cr c B A C)
        (g + (data c B A C).γ) (h + (data c B A C).γ) := by
  unfold stepWord
  rw [normalize_template c B A C (g + 1) (h + 1) hc hB hA hC]
  have hlB : (data c B A C).DB.length = B.length := norm_length _ _
  have hlRB : (data c B A C).DRB.length = B.length := by
    simp [data, norm_length]
  have hlA : (data c B A C).DA.length = A.length := norm_length _ _
  have hlRA : (data c B A C).DRA.length = A.length := by
    simp [data, norm_length]
  have hnext := next_complement c hc
  have hγ1 := gamma_le c B A C hB
  rcases (by omega : (data c B A C).γ = 0 ∨ (data c B A C).γ = 1) with hγ | hγ
  · -- no overflow
    have hw : digitWord c B A C (g + 1) (h + 1) ++ carryWord (data c B A C).γ =
        ((data c B A C).DB ++ [u0 c B A C]) ++ List.replicate g (tOf c) ++
        ([tOf c] ++ (data c B A C).DA ++ [u1 c B A C]) ++ List.replicate h (tOf (18 - c)) ++
        ([tOf (18 - c)] ++ (data c B A C).DC ++ [u2 c B A C]) ++
        List.replicate h (tOf (18 - c)) ++
        ([tOf (18 - c)] ++ (data c B A C).DRA ++ [u3 c B A C]) ++
        List.replicate g (tOf c) ++ ([tOf c] ++ (data c B A C).DRB) := by
      simp only [digitWord, carryWord, hγ, if_true, List.append_nil,
        List.replicate_succ', List.append_assoc, List.cons_append, List.singleton_append,
        List.nil_append]
    rw [hw, pair_split _ _ _ _ _ _ _ _ _ (by simp [hlB, hlRB]) (by simp [hlA, hlRA])]
    simp only [template, Br, Ar, Cr, hγ, if_true, Nat.add_zero, hnext,
      List.reverse_append, List.reverse_cons, List.reverse_nil, List.nil_append,
      List.append_assoc, List.singleton_append, List.cons_append]
  · -- overflow: the appended leading one shifts the reflected alignment
    have hw : digitWord c B A C (g + 1) (h + 1) ++ carryWord (data c B A C).γ =
        ((data c B A C).DB ++ [u0 c B A C]) ++ List.replicate (g + 1) (tOf c) ++
        ((data c B A C).DA ++ [u1 c B A C]) ++ List.replicate (h + 1) (tOf (18 - c)) ++
        ((data c B A C).DC ++ [u2 c B A C]) ++
        List.replicate (h + 1) (tOf (18 - c)) ++
        ((data c B A C).DRA ++ [u3 c B A C]) ++
        List.replicate (g + 1) (tOf c) ++ ((data c B A C).DRB ++ [1]) := by
      simp only [digitWord, carryWord, hγ, List.append_assoc, List.cons_append,
        List.singleton_append, List.nil_append]
      simp
    rw [hw, pair_split _ _ _ _ _ _ _ _ _ (by simp [hlB, hlRB]) (by simp [hlA, hlRA])]
    simp only [template, Br, Ar, Cr, hγ, hnext, List.reverse_append, List.reverse_cons,
      List.reverse_nil, List.nil_append, List.append_assoc, List.singleton_append,
      List.cons_append]
    simp

/-! ## Ordinary integers: verbatim copies of the accepted `Lychrel196` semantics -/

/-- Decimal reversal, consuming the least significant digit at each step. -/
def reverseAux (n acc : Nat) : Nat :=
  if h : n = 0 then acc
  else reverseAux (n / 10) (10 * acc + n % 10)
termination_by n
decreasing_by
  exact Nat.div_lt_self (Nat.pos_of_ne_zero h) (by decide)

/-- Structurally recursive implementation used by kernel evaluation. -/
def reverseFuel : Nat → Nat → Nat → Nat
  | 0, _, acc => acc
  | fuel + 1, n, acc =>
      if n = 0 then acc else reverseFuel fuel (n / 10) (10 * acc + n % 10)

def reverse10 (n : Nat) : Nat := reverseFuel n n 0

def Palindrome (n : Nat) : Prop := reverse10 n = n

def step (n : Nat) : Nat := n + reverse10 n

/-- Verbatim copy of `Agent8.orbit` (word orbit). -/
def orbitWord (w : Word) : Nat → Word
  | 0 => w
  | n + 1 => stepWord (orbitWord w n)

/-- Verbatim copy of `Lychrel196.orbit` (integer orbit). -/
def orbit (n : Nat) : Nat → Nat
  | 0 => n
  | k + 1 => step (orbit n k)

/-! ## Decimal digit words (least significant digit first) -/

def evalL : Word → Nat
  | [] => 0
  | x :: xs => x + 10 * evalL xs

def digitsFuel : Nat → Nat → Word
  | 0, _ => []
  | fuel + 1, n => if n = 0 then [] else (n % 10) :: digitsFuel fuel (n / 10)

/-- Canonical decimal digits of `n`, least significant first; `digits 0 = []`. -/
def digits (n : Nat) : Word := digitsFuel n n

/-- Mirrored pair word of an ordinary integer: `D + rev D` for its digits `D`. -/
def pairWord (n : Nat) : Word := pair (digits n)

theorem digitsFuel_stable (f f' n : Nat) (hf : n ≤ f) (hf' : n ≤ f') :
    digitsFuel f n = digitsFuel f' n := by
  induction f generalizing f' n with
  | zero =>
    have : n = 0 := by omega
    subst this; cases f' <;> simp [digitsFuel]
  | succ f ih =>
    cases f' with
    | zero => have : n = 0 := by omega
              subst this; simp [digitsFuel]
    | succ f' =>
      by_cases hn : n = 0
      · subst hn; simp [digitsFuel]
      · simp only [digitsFuel, hn, if_false]
        have hd := Nat.div_lt_self (Nat.pos_of_ne_zero hn) (by decide : 1 < 10)
        rw [ih f' (n / 10) (by omega) (by omega)]

theorem digits_zero : digits 0 = [] := by simp [digits, digitsFuel]

theorem digits_pos (n : Nat) (hn : n ≠ 0) : digits n = (n % 10) :: digits (n / 10) := by
  obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
  simp only [digits, digitsFuel, hn, if_false]
  have hd := Nat.div_lt_self (Nat.pos_of_ne_zero hn) (by decide : 1 < 10)
  rw [digitsFuel_stable m ((m + 1) / 10) ((m + 1) / 10) (by omega) (by omega)]

theorem evalL_digits (n : Nat) : evalL (digits n) = n := by
  induction n using Nat.strongRecOn with
  | ind n ih =>
    by_cases hn : n = 0
    · subst hn; simp [digits_zero, evalL]
    · rw [digits_pos n hn, evalL]
      have hd := Nat.div_lt_self (Nat.pos_of_ne_zero hn) (by decide : 1 < 10)
      rw [ih (n / 10) hd]; omega

theorem evalL_append (a b : Word) :
    evalL (a ++ b) = evalL a + 10 ^ a.length * evalL b := by
  induction a with
  | nil => simp [evalL]
  | cons x xs ih =>
    simp only [List.cons_append, evalL, ih, List.length_cons, Nat.pow_succ]
    rw [Nat.mul_add, ← Nat.mul_assoc, Nat.mul_comm 10 (10 ^ xs.length)]
    omega

theorem evalL_zipAdd (a b : Word) (h : a.length = b.length) :
    evalL (zipAdd a b) = evalL a + evalL b := by
  induction a generalizing b with
  | nil => cases b <;> simp_all [zipAdd, evalL]
  | cons x xs ih =>
    cases b with
    | nil => simp at h
    | cons y ys =>
      simp only [List.length_cons, Nat.add_right_cancel_iff] at h
      simp only [zipAdd, evalL, ih ys h]; omega

theorem reverseFuel_digits (fuel n acc : Nat) (h : n ≤ fuel) :
    reverseFuel fuel n acc =
      acc * 10 ^ (digits n).length + evalL (digits n).reverse := by
  induction fuel generalizing n acc with
  | zero =>
    have : n = 0 := by omega
    subst this; simp [reverseFuel, digits_zero, evalL]
  | succ fuel ih =>
    by_cases hn : n = 0
    · subst hn; simp [reverseFuel, digits_zero, evalL]
    · have hd := Nat.div_lt_self (Nat.pos_of_ne_zero hn) (by decide : 1 < 10)
      simp only [reverseFuel, hn, if_false]
      rw [ih (n / 10) _ (by omega), digits_pos n hn, List.reverse_cons, evalL_append]
      simp only [List.length_cons, List.length_reverse, evalL, Nat.pow_succ, Nat.mul_zero,
        Nat.add_zero]
      generalize 10 ^ List.length (digits (n / 10)) = P
      have e1 : acc * (P * 10) = 10 * (acc * P) := by
        rw [Nat.mul_comm P 10, Nat.mul_left_comm]
      have e2 : n % 10 * P = P * (n % 10) := Nat.mul_comm _ _
      have e3 : (10 * acc + n % 10) * P = 10 * (acc * P) + P * (n % 10) := by
        rw [Nat.add_mul, Nat.mul_assoc, e2]
      omega

theorem reverse10_eq (n : Nat) : reverse10 n = evalL (digits n).reverse := by
  rw [reverse10, reverseFuel_digits n n 0 (Nat.le_refl n)]; simp

theorem step_eq_evalL_pair (n : Nat) : step n = evalL (pairWord n) := by
  rw [step, reverse10_eq, pairWord, pair, evalL_zipAdd _ _ (by simp), evalL_digits]

/-! ## Canonical digit words -/

/-- All digits below ten and, if nonempty, the most significant digit is positive. -/
def Canon : Word → Prop
  | [] => True
  | [x] => 0 < x ∧ x < 10
  | x :: y :: ys => x < 10 ∧ Canon (y :: ys)

theorem evalL_pos_of_canon (x : Nat) (xs : Word) (h : Canon (x :: xs)) :
    0 < evalL (x :: xs) := by
  induction xs generalizing x with
  | nil => simp [Canon] at h; simp [evalL]; omega
  | cons y ys ih =>
    have := ih y h.2
    simp only [evalL] at *; omega

theorem digits_evalL (D : Word) (h : Canon D) : digits (evalL D) = D := by
  induction D with
  | nil => simp [evalL, digits_zero]
  | cons x xs ih =>
    cases xs with
    | nil =>
      simp only [Canon] at h
      rw [digits_pos _ (by simp [evalL]; omega)]
      simp [evalL]
      have : x % 10 = x := Nat.mod_eq_of_lt h.2
      have : x / 10 = 0 := Nat.div_eq_of_lt h.2
      simp_all [digits_zero]
    | cons y ys =>
      have hpos := evalL_pos_of_canon y ys h.2
      have hx : x < 10 := h.1
      rw [digits_pos _ (by simp only [evalL] at *; omega)]
      have h1 : evalL (x :: y :: ys) % 10 = x := by simp only [evalL]; omega
      have h2 : evalL (x :: y :: ys) / 10 = evalL (y :: ys) := by simp only [evalL]; omega
      rw [h1, h2, ih h.2]

theorem evalL_norm (w : Word) (e : Nat) :
    evalL (normalize w e) = evalL w + e := by
  induction w generalizing e with
  | nil => by_cases he : e = 0 <;> simp [normalize, evalL, he]
  | cons x xs ih =>
    simp only [normalize, evalL, ih]; omega

/-- Last coefficient positive (the exterior of a nonempty word). -/
def LastPos (w : Word) : Prop := ∀ x, w.getLast? = some x → 0 < x

theorem canon_normalize (w : Word) (e : Nat) (hw : Bounded w) (he : e ≤ 1)
    (hlast : LastPos w) : Canon (normalize w e) := by
  induction w generalizing e with
  | nil =>
    by_cases h0 : e = 0
    · simp [normalize, h0, Canon]
    · simp [normalize, h0, Canon]; omega
  | cons x xs ih =>
    have hx := hw x (by simp)
    cases xs with
    | nil =>
      have hxp : 0 < x := hlast x (by simp)
      by_cases hc : (x + e) / 10 = 0
      · simp [normalize, hc, Canon]; omega
      · simp [normalize, hc, Canon]; omega
    | cons y ys =>
      have hb : Bounded (y :: ys) := fun z hz => hw z (by simp_all)
      have hl : LastPos (y :: ys) := by
        intro z hz; apply hlast z; simpa [List.getLast?_cons_cons] using hz
      have ht := ih ((x + e) / 10) hb (by omega) hl
      simp only [normalize] at ht ⊢
      exact ⟨Nat.mod_lt _ (by decide), ht⟩

theorem bounded_pair_digits (n : Nat) : Bounded (pairWord n) := by
  have hd : ∀ y ∈ digits n, y < 10 := by
    intro y hy
    induction n using Nat.strongRecOn with
    | ind n ih =>
      by_cases hn : n = 0
      · subst hn; simp [digits_zero] at hy
      · rw [digits_pos n hn] at hy
        rcases List.mem_cons.mp hy with h | h
        · subst h; exact Nat.mod_lt _ (by decide)
        · exact ih (n / 10) (Nat.div_lt_self (Nat.pos_of_ne_zero hn) (by decide)) h
  have key : ∀ a b : Word, (∀ y ∈ a, y < 10) → (∀ y ∈ b, y < 10) → Bounded (zipAdd a b) := by
    intro a; induction a with
    | nil => intro b _ _ z hz; cases b <;> simp [zipAdd] at hz
    | cons x xs ih =>
      intro b ha hb z hz
      cases b with
      | nil => simp [zipAdd] at hz
      | cons y ys =>
        simp only [zipAdd, List.mem_cons] at hz
        rcases hz with hz | hz
        · have := ha x (by simp); have := hb y (by simp); omega
        · exact ih ys (fun t ht => ha t (by simp [ht])) (fun t ht => hb t (by simp [ht])) z hz
  exact key _ _ hd (fun y hy => hd y (List.mem_reverse.mp hy))

theorem canon_digits (n : Nat) : Canon (digits n) := by
  induction n using Nat.strongRecOn with
  | ind n ih =>
    by_cases hn : n = 0
    · subst hn; simp [digits_zero, Canon]
    · rw [digits_pos n hn]
      by_cases hq : n / 10 = 0
      · rw [hq, digits_zero]; simp only [Canon]; omega
      · have := ih (n / 10) (Nat.div_lt_self (Nat.pos_of_ne_zero hn) (by decide))
        rw [digits_pos (n / 10) hq] at this ⊢
        exact ⟨Nat.mod_lt _ (by decide), this⟩

theorem canon_last_pos (E : Word) (z : Nat) (h : Canon (E ++ [z])) : 0 < z := by
  induction E with
  | nil => simp [Canon] at h; exact h.1
  | cons a F ih =>
    cases F with
    | nil => simp [Canon] at h; exact h.2.1
    | cons b F => exact ih h.2

theorem pair_last (E : Word) (z : Nat) (hz : 0 < z) :
    LastPos (pair (E ++ [z])) := by
  intro x hx
  cases E with
  | nil => simp [pair, zipAdd] at hx; omega
  | cons z0 E' =>
    have hw : pair (z0 :: E' ++ [z]) =
        (z0 + z) :: (zipAdd E' E'.reverse ++ [z + z0]) := by
      have : (z0 :: E' ++ [z]).reverse = z :: (E'.reverse ++ [z0]) := by simp
      rw [pair, this, List.cons_append, zipAdd,
        zipAdd_append _ _ _ _ (by simp : E'.length = E'.reverse.length)]
      rfl
    rw [hw] at hx
    simp [List.getLast?_cons, List.getLast?_append] at hx
    omega

theorem lastPos_pairWord (n : Nat) : LastPos (pairWord n) := by
  by_cases hn : n = 0
  · subst hn; intro x hx; simp [pairWord, digits_zero, pair, zipAdd] at hx
  · have hc := canon_digits n
    have hne : digits n ≠ [] := by rw [digits_pos n hn]; simp
    obtain ⟨E, z, hEz⟩ : ∃ E z, digits n = E ++ [z] := by
      cases hdec : (digits n).reverse with
      | nil => simp at hdec; exact absurd hdec hne
      | cons z E => exact ⟨E.reverse, z, by
          have := congrArg List.reverse hdec; simpa using this⟩
    rw [hEz] at hc
    unfold pairWord; rw [hEz]
    exact pair_last E z (canon_last_pos E z hc)

/-- **Integer bridge.** For every natural `n`, the mirrored pair word of the
accepted reverse-and-add `step n = n + reverse10 n` is Agent #8's `stepWord`
of the mirrored pair word of `n`. -/
theorem pairWord_step (n : Nat) : pairWord (step n) = stepWord (pairWord n) := by
  have hcan := canon_normalize (pairWord n) 0 (bounded_pair_digits n) (by decide)
    (lastPos_pairWord n)
  have hval : step n = evalL (normalize (pairWord n) 0) := by
    rw [evalL_norm, step_eq_evalL_pair]; rfl
  rw [stepWord, pairWord, hval, digits_evalL _ hcan]

/-- The word orbit is the actual integer orbit, at every time. -/
theorem pairWord_orbit (n k : Nat) : pairWord (orbit n k) = orbitWord (pairWord n) k := by
  induction k with
  | zero => rfl
  | succ k ih => rw [orbit, orbitWord, pairWord_step, ih]

/-- Every later integer of the orbit is the value of the corresponding word. -/
theorem orbit_succ_value (n k : Nat) :
    orbit n (k + 1) = evalL (orbitWord (pairWord n) k) := by
  rw [orbit, step_eq_evalL_pair, pairWord_orbit]

/-! ## Actual integers in template form, and palindromes -/

/-- **Actual-orbit template step.** If an ordinary integer `n` has mirrored pair
word equal to a template, then `n + reverse10 n` has the explicit returned
template as its mirrored pair word. -/
theorem actual_template_step (n c : Nat) (B A C : Word) (g h : Nat) (hc : Phase c)
    (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hn : pairWord n = template c B A C (g + 2) (h + 2)) :
    pairWord (step n) =
      template (tOf c + tOf c) (Br c B A C) (Ar c B A C) (Cr c B A C)
        (g + (data c B A C).γ) (h + (data c B A C).γ) := by
  rw [pairWord_step, hn, stepWord_template c B A C g h hc hB hA hC]

theorem canon_iff (D : Word) : Canon D ↔ (∀ y ∈ D, y < 10) ∧ LastPos D := by
  induction D with
  | nil => simp [Canon, LastPos]
  | cons x xs ih =>
    cases xs with
    | nil =>
      simp only [Canon, LastPos, List.mem_singleton, forall_eq, List.getLast?_singleton,
        Option.some.injEq, forall_eq']
      constructor <;> intro h <;> exact ⟨h.2, h.1⟩
    | cons y ys =>
      have hl : LastPos (x :: y :: ys) ↔ LastPos (y :: ys) := by
        simp [LastPos, List.getLast?_cons_cons]
      simp only [Canon, ih, hl, List.mem_cons]
      constructor
      · rintro ⟨hx, hall, hlp⟩
        refine ⟨?_, hlp⟩
        intro z hz
        rcases hz with hz | hz
        · omega
        · exact hall z (by simp_all)
      · rintro ⟨hall, hlp⟩
        exact ⟨hall x (Or.inl rfl), fun z hz => hall z (Or.inr hz), hlp⟩

theorem evalL_lt (W : Word) (h : ∀ y ∈ W, y < 10) : evalL W < 10 ^ W.length := by
  induction W with
  | nil => simp [evalL]
  | cons x xs ih =>
    have hx := h x (by simp)
    have := ih (fun y hy => h y (by simp [hy]))
    simp only [evalL, List.length_cons, Nat.pow_succ]
    have : 10 * evalL xs + 10 ≤ 10 ^ xs.length * 10 := by
      rw [Nat.mul_comm (10 ^ xs.length) 10]; omega
    omega

theorem evalL_ge (x : Nat) (xs : Word) (h : Canon (x :: xs)) :
    10 ^ xs.length ≤ evalL (x :: xs) := by
  induction xs generalizing x with
  | nil => simp [Canon] at h; simp [evalL]; omega
  | cons y ys ih =>
    have := ih y h.2
    simp only [evalL, List.length_cons, Nat.pow_succ] at *
    rw [Nat.mul_comm (10 ^ ys.length) 10]; omega

/-- Palindromes of the accepted semantics are exactly integers whose canonical
digit word is a list palindrome. -/
theorem palindrome_iff (m : Nat) : Palindrome m ↔ (digits m).reverse = digits m := by
  constructor
  · intro hp
    unfold Palindrome at hp
    rw [reverse10_eq] at hp
    have hc := canon_digits m
    rcases hD : digits m with _ | ⟨d0, F⟩
    · rfl
    · rw [hD] at hp hc
      have hall := ((canon_iff _).mp hc).1
      by_cases hd0 : d0 = 0
      · exfalso
        subst hd0
        have hlt : evalL (0 :: F).reverse < 10 ^ F.length := by
          rw [List.reverse_cons, evalL_append]
          simp only [List.length_reverse, evalL, Nat.mul_zero, Nat.add_zero]
          have := evalL_lt F.reverse
            (fun y hy => hall y (List.mem_cons_of_mem _ (List.mem_reverse.mp hy)))
          simpa using this
        have hge := evalL_ge _ F hc
        have hm : evalL (digits m) = m := evalL_digits m
        rw [hD] at hm
        omega
      · have hcr : Canon (d0 :: F).reverse := by
          rw [canon_iff]
          refine ⟨fun y hy => hall y (List.mem_reverse.mp hy), ?_⟩
          intro x hx
          simp [List.getLast?_reverse] at hx
          omega
        have h1 := digits_evalL _ hcr
        rw [hp, hD] at h1
        exact h1.symm
  · intro h
    unfold Palindrome
    rw [reverse10_eq, h, evalL_digits]

/-- Safety of the next integer is a property of the normalized word:
`step n` is a palindrome iff `normalize (pairWord n) 0` is a list palindrome. -/
theorem step_palindrome_iff (n : Nat) :
    Palindrome (step n) ↔
      (normalize (pairWord n) 0).reverse = normalize (pairWord n) 0 := by
  have hcan := canon_normalize (pairWord n) 0 (bounded_pair_digits n) (by decide)
    (lastPos_pairWord n)
  have hval : step n = evalL (normalize (pairWord n) 0) := by
    rw [evalL_norm, step_eq_evalL_pair]; rfl
  rw [palindrome_iff, hval, digits_evalL _ hcan]

/-- Template form of the safety test: for `n` realizing the template, `step n`
is a palindrome iff the explicit digit word (5) (with its overflow digit) is a
list palindrome. -/
theorem actual_template_palindrome_iff (n c : Nat) (B A C : Word) (g h : Nat)
    (hc : Phase c) (hB : Bounded B) (hA : Bounded A) (hC : Bounded C)
    (hn : pairWord n = template c B A C (g + 1) (h + 1)) :
    Palindrome (step n) ↔
      (digitWord c B A C g h ++ carryWord (data c B A C).γ).reverse =
        digitWord c B A C g h ++ carryWord (data c B A C).γ := by
  rw [step_palindrome_iff, hn, normalize_template c B A C g h hc hB hA hC]

end Agent109
