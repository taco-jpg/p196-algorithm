import Agent1RepeatedBlockContext

/-!
Spatial guard extraction for a single original decimal pair-word transition.
The structural zipper lemmas use the original `Agent8.zipAdd` and `pair`.
No arithmetic copies, future interface returns, or safety invariants are used.
-/

namespace Agent1.Periodic

open Agent8 Agent1.RepeatedBlock

theorem pow_append (w : Word) (m n : Nat) :
    pow w (m + n) = pow w m ++ pow w n := by
  induction m with
  | zero => simp [pow]
  | succ m ih => simp [Nat.succ_add, pow, ih, List.append_assoc]

theorem pow_succ_right (w : Word) (n : Nat) :
    pow w (n + 1) = pow w n ++ w := by
  rw [pow_append]
  simp [pow]

theorem pow_reverse (w : Word) (n : Nat) :
    (pow w n).reverse = pow w.reverse n := by
  induction n with
  | zero => rfl
  | succ n ih => rw [pow, List.reverse_append, ih, pow_succ_right]

theorem zipAdd_append_eq (a a' b b' : Word) (h : a.length = b.length) :
    zipAdd (a ++ a') (b ++ b') = zipAdd a b ++ zipAdd a' b' := by
  simp only [zipAdd_eq_zipWith]
  exact List.zipWith_append h

theorem zipAdd_length_eq (a b : Word) (h : a.length = b.length) :
    (zipAdd a b).length = a.length := by
  simp [zipAdd_eq_zipWith, List.length_zipWith, h]

theorem zipAdd_comm_eq (a b : Word) : zipAdd a b = zipAdd b a := by
  simp only [zipAdd_eq_zipWith]
  rw [List.zipWith_comm]
  simp only [Nat.add_comm]

theorem zipAdd_reverse_eq (a b : Word) (h : a.length = b.length) :
    (zipAdd a b).reverse = zipAdd a.reverse b.reverse := by
  simp only [zipAdd_eq_zipWith]
  exact List.reverse_zipWith h

theorem zipAdd_pow (a b : Word) (n : Nat) (h : a.length = b.length) :
    zipAdd (pow a n) (pow b n) = pow (zipAdd a b) n := by
  induction n with
  | zero => rfl
  | succ n ih => rw [pow, pow, zipAdd_append_eq _ _ _ _ h, ih, pow]

/-- Moving a fixed prefix past any number of periods rotates that period. -/
theorem pow_rotate_append (p s : Word) (n : Nat) :
    pow (p ++ s) n ++ p = p ++ pow (s ++ p) n := by
  induction n with
  | zero => simp [pow]
  | succ n ih =>
    simp only [pow, List.append_assoc]
    rw [ih]
    simp only [List.append_assoc]

/-- Pairing three pieces with equally long exteriors leaves the middle paired
with itself and makes the right exterior the reverse of the left one. -/
theorem pair_three_parts (l m r : Word) (h : l.length = r.length) :
    pair (l ++ m ++ r) =
      zipAdd l r.reverse ++ pair m ++ (zipAdd l r.reverse).reverse := by
  have hl : l.length = r.reverse.length := by simpa using h
  have hm : m.length = m.reverse.length := by simp
  have hr : zipAdd r l.reverse = (zipAdd l r.reverse).reverse := by
    rw [zipAdd_reverse_eq l r.reverse hl, List.reverse_reverse, zipAdd_comm_eq]
  simp only [pair, List.reverse_append]
  rw [List.append_assoc l m r, List.append_assoc r.reverse m.reverse l.reverse,
    zipAdd_append_eq l (m ++ r) r.reverse (m.reverse ++ l.reverse) hl,
    zipAdd_append_eq m r m.reverse l.reverse hm, hr]
  simp only [List.append_assoc]

end Agent1.Periodic

#print axioms Agent1.Periodic.pow_append
#print axioms Agent1.Periodic.pow_succ_right
#print axioms Agent1.Periodic.pow_reverse
#print axioms Agent1.Periodic.zipAdd_append_eq
#print axioms Agent1.Periodic.zipAdd_length_eq
#print axioms Agent1.Periodic.zipAdd_comm_eq
#print axioms Agent1.Periodic.zipAdd_reverse_eq
#print axioms Agent1.Periodic.zipAdd_pow
#print axioms Agent1.Periodic.pow_rotate_append
#print axioms Agent1.Periodic.pair_three_parts
