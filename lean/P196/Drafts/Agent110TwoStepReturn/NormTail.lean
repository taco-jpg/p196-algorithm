import P196.Agent5OrdinaryStreamPrefix.ExteriorCore

/-! Agent #110: exact carry interface for original P196.Agent6.norm.
Proposed source-bridge layer; no all-width nonreturn theorem claimed. -/
namespace Agent110.TwoStepNorm
open P196.Agent6

theorem norm_snoc (xs : Word) (x e : Nat) :
    norm (xs ++ [x]) e =
      ((norm xs e).1 ++ [(x + (norm xs e).2) % 10],
       (x + (norm xs e).2) / 10) := by
  induction xs generalizing e with
  | nil => simp [norm]
  | cons y ys ih => simp [norm, ih]

theorem norm_digits_length (xs : Word) (e : Nat) :
    (norm xs e).1.length = xs.length := by
  induction xs generalizing e with
  | nil => rfl
  | cons x xs ih => simp [norm, ih]

theorem norm_terminal_digit (xs : Word) (x e : Nat) :
    (norm (xs ++ [x]) e).1.getLast? =
      some ((x + (norm xs e).2) % 10) := by
  rw [norm_snoc]
  simp

theorem norm_terminal_carry (xs : Word) (x e : Nat) :
    (norm (xs ++ [x]) e).2 =
      (x + (norm xs e).2) / 10 := by
  rw [norm_snoc]

#print axioms norm_snoc
#print axioms norm_digits_length
#print axioms norm_terminal_digit
#print axioms norm_terminal_carry
end Agent110.TwoStepNorm
