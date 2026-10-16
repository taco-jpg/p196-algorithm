import SignedDigitUniqueness

namespace BaseReflection
open SignedDigitUniqueness

def raw (b incoming : Int) : List (Int × Int) → List Int
  | [] => [incoming]
  | (q,c) :: xs => (q + incoming - b*c) :: raw b c xs

def high (b : Int) : List Int → Int
  | [] => 0
  | a :: xs => a * b ^ xs.length + high b xs

def qs (xs : List (Int × Int)) := xs.map Prod.fst
def cs (xs : List (Int × Int)) := xs.map Prod.snd

theorem raw_length (b i : Int) (xs : List (Int × Int)) :
    (raw b i xs).length = xs.length + 1 := by
  induction xs generalizing i with
  | nil => simp [raw]
  | cons a xs ih => simp [raw, ih]

theorem raw_eval (b i : Int) (xs : List (Int × Int)) :
    eval b (raw b i xs) = eval b (qs xs) + i := by
  induction xs generalizing i with
  | nil => simp [raw, eval, qs]
  | cons a xs ih =>
    rcases a with ⟨q,c⟩
    simp only [raw, eval, qs, List.map_cons, ih, Int.mul_add]
    omega

theorem raw_high (b i : Int) (xs : List (Int × Int)) :
    high b (raw b i xs) = b * high b (qs xs) +
      (1-b*b) * high b (cs xs) + i * b ^ xs.length := by
  induction xs generalizing i with
  | nil => simp [raw, high, qs, cs]
  | cons a xs ih =>
    rcases a with ⟨q,c⟩
    simp only [raw, high, raw_length, qs, cs, List.map_cons,
      List.length_map, List.length_cons, ih, Int.pow_succ]
    simp only [Int.add_mul, Int.sub_mul, Int.mul_add, Int.mul_sub,
      Int.one_mul, Int.mul_one, Int.mul_assoc, Int.mul_left_comm, Int.mul_comm]
    omega

theorem eval_append (b : Int) (xs ys : List Int) :
    eval b (xs ++ ys) = eval b xs + b ^ xs.length * eval b ys := by
  induction xs with
  | nil => simp [eval]
  | cons a xs ih =>
    simp only [List.cons_append, eval, List.length_cons, ih, Int.pow_succ]
    simp only [Int.mul_add, Int.mul_assoc, Int.mul_left_comm, Int.mul_comm]
    omega

theorem high_eq_reverse_eval (b : Int) (xs : List Int) :
    high b xs = eval b xs.reverse := by
  induction xs with
  | nil => rfl
  | cons a xs ih =>
    simp [high, List.reverse_cons, eval_append, eval, ← ih,
      Int.mul_comm, Int.add_comm]

def residual (b : Int) (xs : List (Int × Int)) :=
  xs.map (fun p => p.1 - (b+1)*p.2)

theorem residual_high (b : Int) (xs : List (Int × Int)) :
    high b (residual b xs) = high b (qs xs) - (b+1)*high b (cs xs) := by
  induction xs with
  | nil => simp [residual, qs, cs, high]
  | cons a xs ih =>
    rcases a with ⟨q,c⟩
    simp only [residual, qs, cs, List.map_cons, high, List.length_map] at *
    rw [ih]
    simp only [Int.sub_mul, Int.mul_sub, Int.mul_add, Int.add_mul, Int.one_mul, Int.mul_one,
      Int.mul_assoc, Int.mul_left_comm, Int.mul_comm]
    omega

/-- Symmetry at the padded width L+1 forces the reversed residual to vanish.
This uses integer evaluations, with no reciprocal or division operation. -/
theorem overflow_residual_eval_zero (b : Int) (xs : List (Int × Int))
    (hb : b ≠ 1) (hq : (qs xs).reverse = qs xs)
    (he : (raw b 0 xs).reverse = raw b 0 xs) :
    eval b (residual b xs).reverse = 0 := by
  have hqv : high b (qs xs) = eval b (qs xs) := by
    rw [high_eq_reverse_eval, hq]
  have hev : high b (raw b 0 xs) = eval b (raw b 0 xs) := by
    rw [high_eq_reverse_eval, he]
  rw [raw_high, raw_eval] at hev
  simp only [Int.zero_mul, Int.add_zero] at hev
  have hc : (b-1) * high b (qs xs) =
      (b-1) * ((b+1)*high b (cs xs)) := by
    rw [← hqv] at hev
    simp only [Int.sub_mul, Int.mul_sub, Int.mul_add, Int.add_mul, Int.one_mul, Int.mul_one,
      Int.mul_one, Int.mul_assoc] at *
    omega
  have hz := Int.eq_of_mul_eq_mul_left (show b-1 ≠ 0 by omega) hc
  rw [← high_eq_reverse_eval, residual_high, hz]
  omega

/-- Full coefficientwise overflow rigidity, under the actual residual bounds.
The list raw has the terminal carry slot, so its width is exactly L+1. -/
theorem overflow_coefficient_rigidity (b : Int) (xs : List (Int × Int))
    (hb : 3 ≤ b) (hq : (qs xs).reverse = qs xs)
    (he : (raw b 0 xs).reverse = raw b 0 xs)
    (hbound : CoefficientBounds b (residual b xs)) :
    ∀ p ∈ xs, p.1 = (b+1)*p.2 := by
  have hz := overflow_residual_eval_zero b xs (by omega) hq he
  have hall := all_zero_of_reverse_eval_zero b (residual b xs) hb hbound hz
  intro p hp
  have hm : p.1 - (b+1)*p.2 ∈ residual b xs := by
    exact List.mem_map.mpr ⟨p, hp, rfl⟩
  have hr := hall _ hm
  omega

/-- Local isolated-block normalization data. Incoming bits may be reset
independently at seams; they need not equal the previous pair's carry. -/
def ColumnConditions (b : Int) (xs : List (Int × Int)) : Prop :=
  ∀ p ∈ xs, (p.2 = 0 ∨ p.2 = 1) ∧
    ∃ incoming digit : Int,
      (0 ≤ p.1 ∧ p.1 ≤ 2*b-2) ∧
      (0 ≤ incoming ∧ incoming ≤ 1) ∧
      (0 ≤ digit ∧ digit ≤ b-1) ∧
      p.1 + incoming = digit + b*p.2

theorem residual_bounds_of_columns (b : Int) (xs : List (Int × Int))
    (h : ColumnConditions b xs) : CoefficientBounds b (residual b xs) := by
  intro a ha
  obtain ⟨p, hp, rfl⟩ := List.mem_map.mp ha
  obtain ⟨hc, incoming, digit, hq, hi, hd, he⟩ := h p hp
  exact carry_residual_bounds b p.1 incoming p.2 digit hq hi hc hd he

theorem overflow_classification (b : Int) (xs : List (Int × Int))
    (hb : 3 ≤ b) (hq : (qs xs).reverse = qs xs)
    (he : (raw b 0 xs).reverse = raw b 0 xs)
    (hcolumns : ColumnConditions b xs) :
    ∀ p ∈ xs, p.1 = (b+1)*p.2 ∧ (p.1 = 0 ∨ p.1 = b+1) := by
  have hr := overflow_coefficient_rigidity b xs hb hq he
    (residual_bounds_of_columns b xs hcolumns)
  intro p hp
  have hpq := hr p hp
  constructor
  · exact hpq
  · rcases (hcolumns p hp).1 with hc | hc
    · left; simpa [hc] using hpq
    · right; simpa [hc] using hpq

theorem high_append_zero (b : Int) (xs : List Int) :
    high b (xs ++ [0]) = b * high b xs := by
  simp [high_eq_reverse_eval, List.reverse_append, eval]

/-- The no-overflow branch uses width L rather than L+1: raw's extra
terminal slot is explicitly removed before asking for symmetry. -/
theorem nooverflow_carries_zero (b : Int) (xs : List (Int × Int)) (e : List Int)
    (hb : 3 ≤ b) (hq : (qs xs).reverse = qs xs)
    (hraw : raw b 0 xs = e ++ [0]) (he : e.reverse = e)
    (hcolumns : ColumnConditions b xs) :
    ∀ p ∈ xs, p.2 = 0 := by
  have hqv : high b (qs xs) = eval b (qs xs) := by
    rw [high_eq_reverse_eval, hq]
  have hev : high b e = eval b e := by
    rw [high_eq_reverse_eval, he]
  have hval := raw_eval b 0 xs
  rw [hraw, eval_append] at hval
  simp only [eval, Int.mul_zero, Int.add_zero] at hval
  have hr := raw_high b 0 xs
  rw [hraw, high_append_zero, hev, hval, ← hqv] at hr
  simp only [Int.zero_mul, Int.add_zero] at hr
  have hprod : (1-b*b) * high b (cs xs) = 0 := by omega
  have hbb : 1-b*b ≠ 0 := by
    have hh := Int.mul_le_mul_of_nonneg_left (show 3 ≤ b from hb)
      (show 0 ≤ b by omega)
    have hh' : 3*b ≤ b*b := by simpa [Int.mul_comm] using hh
    omega
  have hcz := (Int.mul_eq_zero.mp hprod).resolve_left hbb
  have hbounds : CoefficientBounds b (cs xs) := by
    intro a ha
    obtain ⟨p, hp, rfl⟩ := List.mem_map.mp ha
    rcases (hcolumns p hp).1 with hc | hc <;> simp [hc] <;> omega
  have hall := all_zero_of_reverse_eval_zero b (cs xs) hb hbounds
    (by rwa [← high_eq_reverse_eval])
  intro p hp
  exact hall _ (List.mem_map.mpr ⟨p, hp, rfl⟩)

theorem nooverflow_classification (b : Int) (xs : List (Int × Int)) (e : List Int)
    (hb : 3 ≤ b) (hq : (qs xs).reverse = qs xs)
    (hraw : raw b 0 xs = e ++ [0]) (he : e.reverse = e)
    (hcolumns : ColumnConditions b xs) :
    ∀ p ∈ xs, p.2 = 0 ∧ p.1 ≤ b-1 := by
  have hz := nooverflow_carries_zero b xs e hb hq hraw he hcolumns
  intro p hp
  have hc := hz p hp
  obtain ⟨_, incoming, digit, _, hi, hd, heq⟩ := hcolumns p hp
  rw [hc] at heq
  simp only [Int.mul_zero, Int.add_zero] at heq
  exact ⟨hc, by omega⟩

theorem raw_of_zero_carries (b : Int) (xs : List (Int × Int))
    (hz : ∀ p ∈ xs, p.2 = 0) : raw b 0 xs = qs xs ++ [0] := by
  induction xs with
  | nil => rfl
  | cons p xs ih =>
    have hc := hz p (by simp)
    have ht : ∀ p ∈ xs, p.2 = 0 := by
      intro p hp
      exact hz p (by simp [hp])
    rcases p with ⟨q,c⟩
    simp only [Prod.snd] at hc
    subst c
    simp [raw, qs, ih ht]

theorem nooverflow_raw_equals_input (b : Int) (xs : List (Int × Int)) (e : List Int)
    (hb : 3 ≤ b) (hq : (qs xs).reverse = qs xs)
    (hraw : raw b 0 xs = e ++ [0]) (he : e.reverse = e)
    (hcolumns : ColumnConditions b xs) : e = qs xs := by
  have hz := nooverflow_carries_zero b xs e hb hq hraw he hcolumns
  have hr := raw_of_zero_carries b xs hz
  rw [hraw] at hr
  exact List.append_cancel_right hr

end BaseReflection
