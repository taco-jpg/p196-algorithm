import Std

/-!
General, kernel-checked reverse-closure theorem with no-predecessor pruning.
This file has no computational certificate and makes no claim about Lychrel
existence. The finite instantiation is in BoundaryCertificate.lean.
-/

namespace ReverseClosure

inductive Path {α : Type} (E : α → α → Prop) : α → α → Prop
  | refl (x : α) : Path E x x
  | snoc {x y z : α} : Path E x y → E y z → Path E x z

/-- A root is explicitly protected before states without predecessors are pruned. -/
theorem excludes_reachable {α : Type} {E : α → α → Prop}
    {C : α → Prop} {r t : α}
    (hr : ¬ C r) (ht : C t)
    (closed : ∀ p s, C s → E p s →
      p ≠ r ∧ (C p ∨ ¬ ∃ q, E q p)) :
    ¬ Path E r t := by
  intro path
  have main : ∀ {s}, Path E r s → C s → False := by
    intro s path
    induction path with
    | refl => exact hr
    | @snoc y z path edge ih =>
      intro hz
      obtain ⟨hne, hp | hdead⟩ := closed y z hz edge
      · exact ih hp
      · cases path with
        | refl => exact hne rfl
        | snoc _ prior => exact hdead ⟨_, prior⟩
  exact main path ht

/-- Variant for an executable overapproximation of having a predecessor. -/
theorem excludes_reachable_of_live {α : Type} {E : α → α → Prop}
    {C : α → Prop} {live : α → Bool} {r t : α}
    (hr : ¬ C r) (ht : C t)
    (live_sound : ∀ q p, E q p → live p = true)
    (closed : ∀ p s, C s → E p s →
      p ≠ r ∧ (live p = true → C p)) :
    ¬ Path E r t := by
  apply excludes_reachable hr ht
  intro p s hs edge
  obtain ⟨hne, hclosed⟩ := closed p s hs edge
  refine ⟨hne, ?_⟩
  by_cases hl : live p = true
  · exact Or.inl (hclosed hl)
  · exact Or.inr (fun ⟨q, hq⟩ => hl (live_sound q p hq))

#print axioms excludes_reachable
#print axioms excludes_reachable_of_live

end ReverseClosure
