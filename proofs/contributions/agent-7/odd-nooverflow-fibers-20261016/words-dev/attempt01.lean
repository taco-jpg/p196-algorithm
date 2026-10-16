import Std

/-!
Exact finite-list representation for odd symmetric coefficient words.
These lemmas connect the half-word encoding to the complete-word domain;
they make no assumption about decimal carries or palindrome avoidance.
-/
namespace P196.Agent7.OddFibers

theorem symmetric_odd_decomposition {α : Type} (q : List α) (m : Nat)
    (hlen : q.length = 2*m+1) (hsym : q.reverse = q) :
    ∃ xs z, xs.length = m ∧ q = xs ++ [z] ++ xs.reverse := by
  have hm : m < q.length := by omega
  have ht : (q.take m).reverse = q.drop (m+1) := by
    rw [List.reverse_take, hsym, hlen]
    congr 1
    omega
  refine ⟨q.take m, q[m], ?_, ?_⟩
  · simp only [List.length_take]
    exact Nat.min_eq_left (by omega)
  · calc
      q = q.take (m+1) ++ q.drop (m+1) := (List.take_append_drop _ _).symm
      _ = (q.take m ++ [q[m]]) ++ (q.take m).reverse := by
        rw [List.take_succ_eq_append_getElem hm, ht]

theorem odd_word_encoding_injective {α : Type} (xs ys : List α) (z w : α)
    (h : xs ++ [z] ++ xs.reverse = ys ++ [w] ++ ys.reverse) :
    xs = ys ∧ z = w := by
  have hh := congrArg List.length h
  simp only [List.length_append, List.length_reverse, List.length_singleton] at hh
  have hlen : xs.length = ys.length := by omega
  have hx := congrArg (List.take xs.length) h
  have he : xs = ys := by
    simpa [List.take_append, hlen] using hx
  subst ys
  have hz := List.append_cancel_left h
  have hz' := List.append_cancel_right hz
  simpa using hz'

theorem odd_word_center {α : Type} (xs : List α) (z : α) :
    (xs ++ [z] ++ xs.reverse)[xs.length]? = some z := by
  simp [List.getElem?_append]

#print axioms symmetric_odd_decomposition
#print axioms odd_word_encoding_injective
#print axioms odd_word_center

end P196.Agent7.OddFibers
