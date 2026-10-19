import P196.Agent101ProtectedFamily.Compat

/-!
Finite decimal blocks separated by two equal, arbitrary zero gaps.
Evaluation and reversal reuse the existing canonical-list semantics and its
compatibility theorem for the original ordinary reverse-and-add map.
-/

namespace DigitSumElevenClassification

open Lychrel196

def gapWord (g : Nat) (lo mid hi : List Nat) : List Nat :=
  lo ++ List.replicate g 0 ++ mid ++ List.replicate g 0 ++ hi

theorem evalL_zero_gap (g : Nat) :
    Agent109.evalL (List.replicate g 0) = 0 := by
  induction g with
  | zero => rfl
  | succ g ih => simp [List.replicate_succ, Agent109.evalL, ih]

/-- Only three coefficients depend on the fixed blocks; the gap contributes
the two powers `10^g` and `10^(g+g)`. -/
theorem evalL_gapWord (g : Nat) (lo mid hi : List Nat) :
    Agent109.evalL (gapWord g lo mid hi) =
      Agent109.evalL lo +
        (10 ^ lo.length * Agent109.evalL mid) * 10 ^ g +
        (10 ^ (lo.length + mid.length) * Agent109.evalL hi) * 10 ^ (g + g) := by
  simp only [gapWord, Agent109.evalL_append, evalL_zero_gap,
    List.length_append, List.length_replicate, Nat.pow_add,
    Nat.zero_add, Nat.add_zero, Nat.mul_zero, Nat.mul_add]
  simp only [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]

theorem reverse_gapWord (g : Nat) (lo mid hi : List Nat) :
    (gapWord g lo mid hi).reverse = gapWord g hi.reverse mid.reverse lo.reverse := by
  simp [gapWord, List.reverse_append, List.reverse_replicate, List.append_assoc]

theorem canon_prepend (xs ys : List Nat)
    (hx : ∀ x ∈ xs, x < 10) (hy : Agent109.Canon ys) (hne : ys ≠ []) :
    Agent109.Canon (xs ++ ys) := by
  induction xs with
  | nil => simpa using hy
  | cons x xs ih =>
    have htail := ih (fun z hz => hx z (by simp [hz]))
    have hnot : xs ++ ys ≠ [] := by
      intro he
      exact hne (List.append_eq_nil_iff.mp he).2
    cases he : xs ++ ys with
    | nil => exact False.elim (hnot he)
    | cons y zs =>
      rw [List.cons_append, he]
      exact ⟨hx x (by simp), by simpa only [he] using htail⟩

theorem canon_gapWord (g : Nat) (lo mid hi : List Nat)
    (hl : ∀ x ∈ lo, x < 10) (hm : ∀ x ∈ mid, x < 10)
    (hh : Agent109.Canon hi) (hne : hi ≠ []) :
    Agent109.Canon (gapWord g lo mid hi) := by
  have hz : ∀ x ∈ List.replicate g 0, x < 10 := by simp
  have hprefix : ∀ x ∈ lo ++ List.replicate g 0 ++ mid ++ List.replicate g 0,
      x < 10 := by
    intro x hx
    simp only [List.mem_append, or_assoc] at hx
    rcases hx with hx | hx | hx | hx
    · exact hl x hx
    · exact hz x hx
    · exact hm x hx
    · exact hz x hx
  simpa only [gapWord, List.append_assoc] using
    canon_prepend (lo ++ List.replicate g 0 ++ mid ++ List.replicate g 0) hi
      hprefix hh hne

theorem reverse10_evalL_gapWord (g : Nat) (lo mid hi : List Nat)
    (hc : Agent109.Canon (gapWord g lo mid hi)) :
    reverse10 (Agent109.evalL (gapWord g lo mid hi)) =
      Agent109.evalL (gapWord g hi.reverse mid.reverse lo.reverse) := by
  rw [Agent109.Compat.reverse10_eq, Agent109.reverse10_eq,
    Agent109.digits_evalL _ hc, reverse_gapWord]

/-- A finite block arithmetic identity certifies one actual integer step. -/
theorem step_gapWord (g : Nat) (lo mid hi lo' mid' hi' : List Nat)
    (hc : Agent109.Canon (gapWord g lo mid hi))
    (hv : Agent109.evalL (gapWord g lo mid hi) +
      Agent109.evalL (gapWord g hi.reverse mid.reverse lo.reverse) =
      Agent109.evalL (gapWord g lo' mid' hi')) :
    step (Agent109.evalL (gapWord g lo mid hi)) =
      Agent109.evalL (gapWord g lo' mid' hi') := by
  rw [step, reverse10_evalL_gapWord g lo mid hi hc]
  exact hv

theorem palindrome_gapWord (g : Nat) (lo mid hi : List Nat)
    (hc : Agent109.Canon (gapWord g lo mid hi))
    (hs : (gapWord g lo mid hi).reverse = gapWord g lo mid hi) :
    Palindrome (Agent109.evalL (gapWord g lo mid hi)) := by
  unfold Palindrome
  rw [Agent109.Compat.reverse10_eq, Agent109.reverse10_eq,
    Agent109.digits_evalL _ hc, hs]

end DigitSumElevenClassification
