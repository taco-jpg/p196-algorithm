import Std

/-!
Agent #7: finite rank certificates for the autonomous outer-boundary quotient.
These generic lemmas do not assert that a particular graph has a rank.
No theorem about P196 follows without the separately stated actual-map bridge.
-/
namespace P196.Agent7

theorem strict_rank_path_bound {α : Type} (rank : α → Nat)
    (path : Nat → α) (n : Nat) :
    (∀ i, i < n → rank (path (i + 1)) < rank (path i)) →
    rank (path n) + n ≤ rank (path 0) := by
  induction n with
  | zero =>
      intro _
      simp
  | succ n ih =>
      intro h
      have hp := ih (by
        intro i hi
        exact h i (Nat.lt_trans hi (Nat.lt_succ_self n)))
      have hl := h n (Nat.lt_succ_self n)
      omega

theorem strict_rank_no_return {α : Type} (rank : α → Nat)
    (path : Nat → α) (n : Nat) (hn : 0 < n)
    (h : ∀ i, i < n → rank (path (i + 1)) < rank (path i)) :
    path n ≠ path 0 := by
  intro heq
  have hb := strict_rank_path_bound rank path n h
  rw [heq] at hb
  omega

theorem strict_rank_bounded_duration {α : Type} (rank : α → Nat)
    (path : Nat → α) (n cap : Nat)
    (h : ∀ i, i < n → rank (path (i + 1)) < rank (path i))
    (hc : rank (path 0) ≤ cap) : n ≤ cap := by
  have hb := strict_rank_path_bound rank path n h
  omega

-- Returning physical width imposes an even, positive overflow count.
theorem cycle_overflow_even (dg dh overflows : Int)
    (h : 2 * (dg + dh) = overflows) : overflows % 2 = 0 := by
  omega

theorem cycle_total_gain_positive (dg dh overflows : Int)
    (h : 2 * (dg + dh) = overflows) (hp : 0 < overflows) :
    0 < dg + dh := by
  omega

#print axioms strict_rank_path_bound
#print axioms strict_rank_no_return
#print axioms strict_rank_bounded_duration
#print axioms cycle_overflow_even
#print axioms cycle_total_gain_positive
end P196.Agent7
