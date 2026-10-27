import Std

/-!
# Labelled walks and positive powers of words

The path projection and path lifting statements below keep every edge label.
Lifting requires a matching edge from each individual original vertex over
the quotient source; an edge witnessed by only some member of a fiber does
not supply that condition. No finiteness or cycle conclusion is used here.
-/

namespace Agent108.CyclicQuotientLift

universe u v q

/-- A walk carrying exactly the given list of edge labels. -/
def Walk {V : Type u} {A : Type v} (E : V → A → V → Prop) :
    V → List A → V → Prop
  | x, [], y => x = y
  | x, a :: w, y => ∃ z, E x a z ∧ Walk E z w y

@[simp] theorem walk_nil {V : Type u} {A : Type v}
    {E : V → A → V → Prop} {x y : V} :
    Walk E x [] y ↔ x = y := Iff.rfl

@[simp] theorem walk_cons {V : Type u} {A : Type v}
    {E : V → A → V → Prop} {x y : V} {a : A} {w : List A} :
    Walk E x (a :: w) y ↔ ∃ z, E x a z ∧ Walk E z w y := Iff.rfl

/-- Concatenation preserves the intervening vertex, not merely the labels. -/
theorem walk_append {V : Type u} {A : Type v}
    {E : V → A → V → Prop} {x y : V} (u v : List A) :
    Walk E x (u ++ v) y ↔ ∃ z, Walk E x u z ∧ Walk E z v y := by
  induction u generalizing x with
  | nil => simp
  | cons a u ih =>
      constructor
      · intro h
        obtain ⟨z, hxz, hzy⟩ := h
        obtain ⟨m, hzm, hmy⟩ := ih.mp hzy
        exact ⟨m, ⟨z, hxz, hzm⟩, hmy⟩
      · rintro ⟨m, ⟨z, hxz, hzm⟩, hmy⟩
        exact ⟨z, hxz, ih.mpr ⟨m, hzm, hmy⟩⟩

/-- Repetition of an entire word; the zeroth power is the empty word. -/
def wordPower {A : Type v} (w : List A) : Nat → List A
  | 0 => []
  | n + 1 => w ++ wordPower w n

@[simp] theorem wordPower_zero {A : Type v} (w : List A) :
    wordPower w 0 = [] := rfl

@[simp] theorem wordPower_succ {A : Type v} (w : List A) (n : Nat) :
    wordPower w (n + 1) = w ++ wordPower w n := rfl

@[simp] theorem wordPower_one {A : Type v} (w : List A) :
    wordPower w 1 = w := by
  simp [wordPower]

theorem wordPower_add {A : Type v} (w : List A) (m n : Nat) :
    wordPower w (m + n) = wordPower w m ++ wordPower w n := by
  induction m with
  | zero => simp
  | succ m ih => simp [Nat.succ_add, wordPower, ih, List.append_assoc]

/-- The same repeated word can also be appended at the right end. -/
theorem wordPower_succ_right {A : Type v} (w : List A) (n : Nat) :
    wordPower w (n + 1) = wordPower w n ++ w := by
  simpa only [wordPower_one] using wordPower_add w n 1

/-- Repeating a whole repeated word multiplies its number of copies. -/
theorem wordPower_mul {A : Type v} (w : List A) (m n : Nat) :
    wordPower (wordPower w m) n = wordPower w (m * n) := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [wordPower_succ, ih, Nat.mul_succ, Nat.add_comm (m * n) m, wordPower_add]

@[simp] theorem wordPower_length {A : Type v} (w : List A) (n : Nat) :
    (wordPower w n).length = n * w.length := by
  induction n with
  | zero => simp
  | succ n ih => simp [wordPower, ih, Nat.succ_mul, Nat.add_comm]

/-- A positive power of a nonempty word is nonempty. -/
theorem wordPower_ne_nil {A : Type v} {w : List A} {n : Nat}
    (hw : w ≠ []) (hn : 0 < n) : wordPower w n ≠ [] := by
  cases n with
  | zero => omega
  | succ n =>
      intro h
      exact hw (List.append_eq_nil_iff.mp h).1

/-- An edge homomorphism projects a walk without changing its label word. -/
theorem walk_map {V : Type u} {Q : Type q} {A : Type v}
    {E : V → A → V → Prop} {F : Q → A → Q → Prop}
    (pi : V → Q)
    (hmap : ∀ x a y, E x a y → F (pi x) a (pi y))
    {x y : V} {w : List A} (h : Walk E x w y) :
    Walk F (pi x) w (pi y) := by
  induction w generalizing x with
  | nil => exact congrArg pi h
  | cons a w ih =>
      obtain ⟨z, hxz, hzy⟩ := h
      exact ⟨pi z, hmap x a z hxz, ih hzy⟩

/-- Pointwise edge lifting lifts a complete labelled path from a specified
original source. Its endpoint lies over the specified quotient endpoint. -/
theorem walk_lift {V : Type u} {Q : Type q} {A : Type v}
    {E : V → A → V → Prop} {F : Q → A → Q → Prop}
    (pi : V → Q)
    (hlift : ∀ x a q', F (pi x) a q' → ∃ y, E x a y ∧ pi y = q')
    {x : V} {q' : Q} {w : List A} (h : Walk F (pi x) w q') :
    ∃ y, Walk E x w y ∧ pi y = q' := by
  induction w generalizing x with
  | nil => exact ⟨x, rfl, h⟩
  | cons a w ih =>
      obtain ⟨middle, hfirst, hrest⟩ := h
      obtain ⟨z, hxz, hproject⟩ := hlift x a middle hfirst
      have hz : Walk F (pi z) w q' := by
        simpa only [hproject] using hrest
      obtain ⟨y, hzy, htarget⟩ := ih hz
      exact ⟨y, ⟨z, hxz, hzy⟩, htarget⟩

end Agent108.CyclicQuotientLift
