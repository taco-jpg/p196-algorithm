import Std
namespace WidthLiftSupport

theorem length_eight_lift {α β : Type} (xs : List α) (f : α → Nat → β) :
    (xs.flatMap (fun x => (List.range 8).map (f x))).length = xs.length * 8 := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
    simp only [List.flatMap_cons, List.length_append, List.length_map,
      List.length_range, List.length_cons, ih]
    omega

def nodes {α : Type} (xs : List α) : List (α × Nat) :=
  xs.flatMap (fun s => (List.range 8).map (fun r => (s, r)))

theorem mem_nodes_iff {α : Type} (xs : List α) (s : α) (r : Nat) :
    (s, r) ∈ nodes xs ↔ s ∈ xs ∧ r < 8 := by
  constructor
  · intro h
    obtain ⟨s', hs', hr⟩ := List.mem_flatMap.mp h
    obtain ⟨r', hr', heq⟩ := List.mem_map.mp hr
    obtain ⟨rfl, rfl⟩ := Prod.mk.inj heq
    exact ⟨hs', List.mem_range.mp hr'⟩
  · rintro ⟨hs, hr⟩
    exact List.mem_flatMap.mpr
      ⟨s, hs, List.mem_map.mpr ⟨r, List.mem_range.mpr hr, rfl⟩⟩
#print axioms length_eight_lift
#print axioms mem_nodes_iff
end WidthLiftSupport
