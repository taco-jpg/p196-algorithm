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

Core Lean 4.19.0 + Std only. No `sorry`, no new axioms, no `native_decide`.
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

end Agent109
