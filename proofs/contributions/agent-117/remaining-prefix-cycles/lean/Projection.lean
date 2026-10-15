import PrefixCycle

/-!
# Projection of the finite-prefix abstraction (Agent #117, Lemma 2, long states)

Dropping the last column of a `(k+1)`-column forward edge gives a `k`-column
forward edge whose boundary carry is the carry out of the dropped column.
Hence a backward walk of long `(k+1)`-column states projects to a backward
walk of long `k`-column states, and a `(k+1)`-column cycle projects to a
`k`-column closed walk.  The short boundary is not covered here (it is an
exact map on complete short words, handled separately in the written lemma).
-/

namespace Agent117

open SevenColumnProjection SevenColumn

/-- The carry leaving the low scan of `s` started with `c`. -/
def lowCarry : List Nat → Nat → Nat
  | [], c => c
  | a :: s, c => lowCarry s (carry a c)

theorem lowDigits_append (s : List Nat) (x c : Nat) :
    lowDigits (s ++ [x]) c = lowDigits s c ++ [lowDigit x (lowCarry s c)] := by
  induction s generalizing c with
  | nil => rfl
  | cons a s ih => simp only [List.cons_append, lowDigits, lowCarry, ih]; rfl

theorem highDigits_append (s : List Nat) (x e : Nat) :
    highDigits (s ++ [x]) e =
      ((highDigits s (carry x e)).1, (highDigits s (carry x e)).2 ++ [lowDigit x e]) := by
  induction s with
  | nil => rfl
  | cons a s ih => simp only [List.cons_append, highDigits, ih]

@[simp] theorem lowDigits_length (s : List Nat) (c : Nat) :
    (lowDigits s c).length = s.length := by
  induction s generalizing c with
  | nil => rfl
  | cons a s ih => simp [lowDigits, ih]

@[simp] theorem highDigits_length (s : List Nat) (e : Nat) :
    (highDigits s e).2.length = s.length := by
  induction s with
  | nil => rfl
  | cons a s ih => simp [highDigits, ih]

theorem take_zipWith_append {α : Type} (f : α → α → α) :
    ∀ (l₁ l₂ : List α) (a b : α), l₁.length ≤ l₂.length →
      (List.zipWith f (l₁ ++ [a]) (l₂ ++ [b])).take l₁.length = List.zipWith f l₁ l₂
  | [], l₂, a, b, _ => by simp
  | c :: l₁, [], a, b, h => by simp at h
  | c :: l₁, d :: l₂, a, b, h => by
      simp only [List.cons_append, List.zipWith_cons_cons, List.length_cons, List.take_succ_cons]
      rw [take_zipWith_append f l₁ l₂ a b (by simpa using h)]

/-- Lemma 2 (long states): the first `s.length` coefficients of the
`(k+1)`-column forward image of `s ++ [x]` with boundary carry `e` are the
`k`-column forward image of `s` with boundary carry `carry x e`. -/
theorem forwardPrefix_append_take (s : List Nat) (x e : Nat) :
    (forwardPrefix (s ++ [x]) e).take s.length = forwardPrefix s (carry x e) := by
  unfold forwardPrefix
  rw [lowDigits_append, highDigits_append]
  dsimp only
  by_cases hg : (highDigits s (carry x e)).1 = 0
  · simp only [hg, if_true]
    have := take_zipWith_append (· + ·) (lowDigits s 0) (highDigits s (carry x e)).2
      (lowDigit x (lowCarry s 0)) (lowDigit x e) (by simp)
    simpa using this
  · simp only [hg, if_false]
    rw [← List.cons_append]
    have := take_zipWith_append (· + ·) (lowDigits s 0) (1 :: (highDigits s (carry x e)).2)
      (lowDigit x (lowCarry s 0)) (lowDigit x e) (by simp)
    simpa using this

/-- A `(k+1)`-column forward edge projects to a `k`-column forward edge
(the dropped column `x < 19` keeps the projected boundary carry below two). -/
theorem forwardAdmitted_project {s p : List Nat} {x : Nat} (hx : x < 19)
    (h : ForwardAdmitted (s ++ [x]) p) : ForwardAdmitted s (p.take s.length) := by
  obtain ⟨e, he, rfl⟩ := h
  refine ⟨carry x e, ?_, (forwardPrefix_append_take s x e).symm⟩
  unfold carry; omega

/-- Projected forward edges between admissible long states are edges of the
executable inverse at the smaller width. -/
theorem project_mem_prefixPredecessors {s p : List Nat} {x : Nat}
    (hs : ∀ a ∈ s, a < 19) (hpos : 0 < s.headD 0) (hx : x < 19)
    (h : ForwardAdmitted (s ++ [x]) p) : s ∈ prefixPredecessors (p.take s.length) :=
  forwardAdmitted_mem_prefixPredecessors hs hpos (forwardAdmitted_project hx h)

#print axioms forwardPrefix_append_take
#print axioms forwardAdmitted_project
#print axioms project_mem_prefixPredecessors

end Agent117
