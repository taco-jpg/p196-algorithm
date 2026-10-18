import Std

/-!
# Agent #120: base-generic reverse-and-add on digit lists

Everything is self-contained and stated for an arbitrary base `b`.
Digit lists are least significant first. No decimal-specific fact is used,
and nothing here concerns 196.

* `val b w` evaluates any coefficient list (entries may exceed `b - 1`).
* `norm b w c` is the carry normalization of `w` with incoming carry `c`.
* `digits b N` is the canonical base-`b` digit list of `N` (fuel-based, so the
  kernel can evaluate it on small literals).
* `step b N = N + rev N`, `orbit`, `IsPal`, `Lychrel` are the ordinary
  base-`b` reverse-and-add notions on natural numbers.
-/

namespace Agent120.Neutral

/-- Value of a least-significant-first coefficient list. -/
def val (b : Nat) : List Nat → Nat
  | [] => 0
  | d :: ds => d + b * val b ds

/-- Carry normalization: digits and the final outgoing carry. -/
def norm (b : Nat) : List Nat → Nat → List Nat × Nat
  | [], c => ([], c)
  | v :: w, c =>
      let r := norm b w ((v + c) / b)
      ((v + c) % b :: r.1, r.2)

/-- Fuel-based canonical digits. -/
def digitsAux (b : Nat) : Nat → Nat → List Nat
  | 0, _ => []
  | fuel + 1, N => if N = 0 then [] else N % b :: digitsAux b fuel (N / b)

/-- Canonical base-`b` digits of `N`, least significant first; `digits b 0 = []`. -/
def digits (b N : Nat) : List Nat := digitsAux b N N

/-- Mirrored digit sums of a digit list. -/
def pairs (D : List Nat) : List Nat := List.zipWith (· + ·) D D.reverse

/-- Ordinary base-`b` reversal of a natural number. -/
def revNat (b N : Nat) : Nat := val b (digits b N).reverse

/-- Ordinary base-`b` reverse-and-add. -/
def step (b N : Nat) : Nat := N + revNat b N

def orbit (b N : Nat) : Nat → Nat
  | 0 => N
  | t + 1 => step b (orbit b N t)

/-- Base-`b` palindrome: the canonical digit list equals its reversal. -/
def IsPal (b N : Nat) : Prop := digits b N = (digits b N).reverse

instance (b N : Nat) : Decidable (IsPal b N) := by
  unfold IsPal; infer_instance

/-- Base-`b` Lychrel property: no orbit element, including the seed, is a palindrome. -/
def Lychrel (b N : Nat) : Prop := ∀ t, ¬ IsPal b (orbit b N t)

/-! ## `val` -/

@[simp] theorem val_nil (b : Nat) : val b [] = 0 := rfl

@[simp] theorem val_cons (b d : Nat) (ds : List Nat) :
    val b (d :: ds) = d + b * val b ds := rfl

theorem val_append (b : Nat) (u w : List Nat) :
    val b (u ++ w) = val b u + b ^ u.length * val b w := by
  induction u with
  | nil => simp
  | cons d ds ih =>
      simp only [List.cons_append, val_cons, ih, List.length_cons, Nat.pow_succ]
      rw [Nat.mul_add, ← Nat.mul_assoc, Nat.mul_comm b (b ^ ds.length)]
      omega

theorem val_zipWith_add (b : Nat) :
    ∀ (u w : List Nat), u.length = w.length →
      val b (List.zipWith (· + ·) u w) = val b u + val b w
  | [], [], _ => by simp [List.zipWith]
  | [], _ :: _, h => by simp at h
  | _ :: _, [], h => by simp at h
  | x :: xs, y :: ys, h => by
      simp only [List.zipWith_cons_cons, val_cons]
      have hl : xs.length = ys.length := by simpa using h
      rw [val_zipWith_add b xs ys hl, Nat.mul_add]
      omega

theorem val_pairs (b : Nat) (D : List Nat) :
    val b (pairs D) = val b D + val b D.reverse := by
  unfold pairs
  exact val_zipWith_add b D D.reverse (by simp)

/-! ## Normalization -/

@[simp] theorem norm_nil (b c : Nat) : norm b [] c = ([], c) := rfl

theorem norm_cons (b v c : Nat) (w : List Nat) :
    norm b (v :: w) c =
      ((v + c) % b :: (norm b w ((v + c) / b)).1, (norm b w ((v + c) / b)).2) := rfl

theorem norm_length (b : Nat) : ∀ (w : List Nat) (c : Nat), (norm b w c).1.length = w.length
  | [], _ => rfl
  | v :: w, c => by
      rw [norm_cons]
      simp [norm_length b w]

theorem norm_append (b : Nat) : ∀ (u w : List Nat) (c : Nat),
    norm b (u ++ w) c =
      ((norm b u c).1 ++ (norm b w (norm b u c).2).1, (norm b w (norm b u c).2).2)
  | [], w, c => by simp
  | v :: u, w, c => by
      rw [List.cons_append, norm_cons, norm_cons, norm_append b u w]
      simp

/-- The normalized digits are digits. -/
theorem norm_digit_lt (b : Nat) (hb : 0 < b) :
    ∀ (w : List Nat) (c : Nat), ∀ d ∈ (norm b w c).1, d < b
  | [], _ => by simp
  | v :: w, c => by
      rw [norm_cons]
      intro d hd
      simp only [List.mem_cons] at hd
      rcases hd with rfl | hd
      · exact Nat.mod_lt _ hb
      · exact norm_digit_lt b hb w _ d hd

/-- Value conservation of the normalization. -/
theorem norm_val (b : Nat) :
    ∀ (w : List Nat) (c : Nat),
      val b (norm b w c).1 + b ^ w.length * (norm b w c).2 = val b w + c
  | [], c => by simp
  | v :: w, c => by
      rw [norm_cons]
      have ih := norm_val b w ((v + c) / b)
      simp only [val_cons, List.length_cons, Nat.pow_succ]
      have hdm := Nat.mod_add_div (v + c) b
      have e1 : b * val b (norm b w ((v + c) / b)).1 + b ^ w.length * b * (norm b w ((v + c) / b)).2
          = b * (val b (norm b w ((v + c) / b)).1 + b ^ w.length * (norm b w ((v + c) / b)).2) := by
        rw [Nat.mul_add, Nat.mul_comm (b ^ w.length) b, Nat.mul_assoc]
      rw [ih] at e1
      rw [Nat.mul_add] at e1
      omega

/-- Carries stay at most one for coefficients at most `2(b-1)`. -/
theorem norm_carry_le_one (b : Nat) (hb : 0 < b) :
    ∀ (w : List Nat) (c : Nat), (∀ v ∈ w, v ≤ 2 * (b - 1)) → c ≤ 1 → (norm b w c).2 ≤ 1
  | [], c, _, hc => by simpa using hc
  | v :: w, c, hw, hc => by
      rw [norm_cons]
      apply norm_carry_le_one b hb w
      · intro u hu
        exact hw u (List.mem_cons_of_mem v hu)
      · have hv := hw v List.mem_cons_self
        have hlt : v + c < 2 * b := by omega
        have : (v + c) / b < 2 := (Nat.div_lt_iff_lt_mul hb).mpr (by omega)
        omega

/-- A neutral run transmits its incoming carry and emits a uniform digit. -/
theorem norm_replicate_neutral (b : Nat) (hb : 2 ≤ b) :
    ∀ (g e : Nat), e ≤ 1 →
      norm b (List.replicate g (b - 1)) e = (List.replicate g ((b - 1) * (1 - e)), e)
  | 0, e, _ => by simp
  | g + 1, e, he => by
      rw [List.replicate_succ, norm_cons]
      have hq : (b - 1 + e) / b = e := by
        rcases (by omega : e = 0 ∨ e = 1) with rfl | rfl
        · exact Nat.div_eq_of_lt (by omega)
        · have : b - 1 + 1 = b := by omega
          rw [this, Nat.div_self (by omega)]
      have hr : (b - 1 + e) % b = (b - 1) * (1 - e) := by
        rcases (by omega : e = 0 ∨ e = 1) with rfl | rfl
        · simp only [Nat.add_zero, Nat.sub_zero, Nat.mul_one]
          exact Nat.mod_eq_of_lt (by omega)
        · have : b - 1 + 1 = b := by omega
          rw [this, Nat.mod_self]
          simp
      rw [hq, hr, norm_replicate_neutral b hb g e he, List.replicate_succ]

/-! ## Canonical digits -/

theorem val_digitsAux (b : Nat) (hb : 2 ≤ b) :
    ∀ (fuel N : Nat), N ≤ fuel → val b (digitsAux b fuel N) = N
  | 0, N, h => by
      have : N = 0 := by omega
      simp [digitsAux, this]
  | fuel + 1, N, h => by
      unfold digitsAux
      by_cases hN : N = 0
      · simp [hN]
      · simp only [hN, if_false, val_cons]
        have hdiv : N / b ≤ fuel := by
          have : N / b < N := Nat.div_lt_self (by omega) (by omega)
          omega
        rw [val_digitsAux b hb fuel (N / b) hdiv]
        exact Nat.mod_add_div N b

theorem val_digits (b : Nat) (hb : 2 ≤ b) (N : Nat) : val b (digits b N) = N :=
  val_digitsAux b hb N N (Nat.le_refl N)

/-- Canonical digit lists: digits below `b` and a nonzero most significant digit. -/
def Canonical (b : Nat) (D : List Nat) : Prop :=
  (∀ d ∈ D, d < b) ∧ D.getLast? ≠ some 0

theorem getLast?_cons_of_ne_nil {a : Nat} {l : List Nat} (h : l ≠ []) :
    (a :: l).getLast? = l.getLast? := by
  cases l with
  | nil => exact absurd rfl h
  | cons x xs => simp [List.getLast?_cons]

theorem canonical_tail {b d : Nat} {ds : List Nat} (hds : ds ≠ [])
    (hc : Canonical b (d :: ds)) : Canonical b ds :=
  ⟨fun x hx => hc.1 x (List.mem_cons_of_mem d hx), by
    have := hc.2
    rwa [getLast?_cons_of_ne_nil hds] at this⟩

theorem val_pos_of_canonical (b : Nat) (hb : 2 ≤ b) :
    ∀ (D : List Nat), D ≠ [] → Canonical b D → 0 < val b D
  | [], h, _ => absurd rfl h
  | [d], _, hc => by
      have h2 := hc.2
      simp only [List.getLast?_singleton, ne_eq, Option.some.injEq] at h2
      simp only [val_cons, val_nil, Nat.mul_zero, Nat.add_zero]
      omega
  | d :: e :: ds, _, hc => by
      have hc' : Canonical b (e :: ds) := canonical_tail (by simp) hc
      have := val_pos_of_canonical b hb (e :: ds) (by simp) hc'
      simp only [val_cons] at this ⊢
      have : 0 < b * (e + b * val b ds) := Nat.mul_pos (by omega) this
      omega

theorem digitsAux_val (b : Nat) (hb : 2 ≤ b) :
    ∀ (D : List Nat) (fuel : Nat), Canonical b D → val b D ≤ fuel →
      digitsAux b fuel (val b D) = D
  | [], fuel, _, _ => by
      cases fuel <;> simp [digitsAux]
  | d :: ds, fuel, hc, hle => by
      have hpos := val_pos_of_canonical b hb (d :: ds) (by simp) hc
      have hd : d < b := hc.1 d List.mem_cons_self
      have hle' : d + b * val b ds ≤ fuel := by simpa only [val_cons] using hle
      cases fuel with
      | zero => omega
      | succ fuel =>
          unfold digitsAux
          have hne : val b (d :: ds) ≠ 0 := by omega
          simp only [hne, if_false]
          have hmod : val b (d :: ds) % b = d := by
            simp only [val_cons]
            rw [Nat.add_mul_mod_self_left]
            exact Nat.mod_eq_of_lt hd
          have hdiv : val b (d :: ds) / b = val b ds := by
            simp only [val_cons]
            rw [Nat.add_mul_div_left _ _ (by omega), Nat.div_eq_of_lt hd]
            simp
          rw [hmod, hdiv]
          congr 1
          by_cases hds : ds = []
          · subst hds
            cases fuel <;> simp [digitsAux]
          · have hc' : Canonical b ds := canonical_tail hds hc
            apply digitsAux_val b hb ds fuel hc'
            have hpos' := val_pos_of_canonical b hb ds hds hc'
            have h2 : 2 * val b ds ≤ b * val b ds := Nat.mul_le_mul_right _ hb
            omega

/-- Canonical lists are recovered from their values. -/
theorem digits_val (b : Nat) (hb : 2 ≤ b) (D : List Nat) (hc : Canonical b D) :
    digits b (val b D) = D :=
  digitsAux_val b hb D (val b D) hc (Nat.le_refl _)

/-- Reverse-and-add is evaluation of the mirrored digit sums. -/
theorem step_eq_val_pairs (b : Nat) (hb : 2 ≤ b) (N : Nat) :
    step b N = val b (pairs (digits b N)) := by
  rw [val_pairs, val_digits b hb]
  rfl

theorem orbit_succ (b N t : Nat) : orbit b N (t + 1) = step b (orbit b N t) := rfl

theorem orbit_add (b N s t : Nat) : orbit b N (s + t) = orbit b (orbit b N s) t := by
  induction t with
  | zero => rfl
  | succ t ih => rw [← Nat.add_assoc, orbit_succ, ih, orbit_succ]

end Agent120.Neutral

#print axioms Agent120.Neutral.norm_val
#print axioms Agent120.Neutral.norm_replicate_neutral
#print axioms Agent120.Neutral.digits_val
#print axioms Agent120.Neutral.step_eq_val_pairs
