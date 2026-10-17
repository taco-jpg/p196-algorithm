import Std

/-!
# Finite selection of a uniform tail

This module is an abstract logical component of the claimed affine-dynamics
formalization.  It contains no reverse-and-add closure or width-growth claim.
The eventual stability and finite cover premises are explicit and must be
proved for the actual arithmetic predicates in the downstream application.

Author: Agent #105 / ownership_audit, session 8f1107db019a.
-/

namespace Agent105.TailSelection

/-- A predicate holds at every natural parameter beyond some cutoff. -/
def Eventually (P : Nat → Prop) : Prop :=
  ∃ K, ∀ k, K ≤ k → P k

/-- Beyond a cutoff, a predicate has the same truth value as at that cutoff. -/
def TailStable (P : Nat → Prop) : Prop :=
  ∃ K, ∀ k, K ≤ k → (P k ↔ P K)

theorem eventually_of_forall {P : Nat → Prop} (h : ∀ k, P k) :
    Eventually P :=
  ⟨0, fun k _ => h k⟩

theorem eventually_mono {P Q : Nat → Prop} (hP : Eventually P)
    (hPQ : ∀ k, P k → Q k) : Eventually Q := by
  rcases hP with ⟨K, hK⟩
  exact ⟨K, fun k hk => hPQ k (hK k hk)⟩

theorem eventually_and {P Q : Nat → Prop}
    (hP : Eventually P) (hQ : Eventually Q) :
    Eventually (fun k => P k ∧ Q k) := by
  rcases hP with ⟨KP, hKP⟩
  rcases hQ with ⟨KQ, hKQ⟩
  refine ⟨max KP KQ, fun k hk => ?_⟩
  exact ⟨hKP k (Nat.le_trans (Nat.le_max_left KP KQ) hk),
    hKQ k (Nat.le_trans (Nat.le_max_right KP KQ) hk)⟩

theorem eventually_not_contradiction {P : Nat → Prop}
    (hP : Eventually P) (hN : Eventually (fun k => ¬ P k)) : False := by
  rcases eventually_and hP hN with ⟨K, hK⟩
  exact (hK K (Nat.le_refl K)).2 (hK K (Nat.le_refl K)).1

theorem tailStable_const (p : Prop) : TailStable (fun _ => p) :=
  ⟨0, fun _ _ => Iff.rfl⟩

theorem tailStable_congr {P Q : Nat → Prop}
    (hPQ : ∀ k, P k ↔ Q k) (hP : TailStable P) : TailStable Q := by
  rcases hP with ⟨K, hK⟩
  refine ⟨K, fun k hk => ?_⟩
  exact (hPQ k).symm.trans ((hK k hk).trans (hPQ K))

theorem tailStable_of_eventually {P : Nat → Prop}
    (hP : Eventually P) : TailStable P := by
  rcases hP with ⟨K, hK⟩
  exact ⟨K, fun k hk => ⟨fun _ => hK K (Nat.le_refl K), fun _ => hK k hk⟩⟩

theorem tailStable_of_eventually_not {P : Nat → Prop}
    (hP : Eventually (fun k => ¬ P k)) : TailStable P := by
  rcases hP with ⟨K, hK⟩
  refine ⟨K, fun k hk => ⟨?_, ?_⟩⟩
  · intro hp
    exact False.elim (hK k hk hp)
  · intro hp
    exact False.elim (hK K (Nat.le_refl K) hp)

theorem tailStable_not {P : Nat → Prop} (hP : TailStable P) :
    TailStable (fun k => ¬ P k) := by
  rcases hP with ⟨K, hK⟩
  exact ⟨K, fun k hk => not_congr (hK k hk)⟩

theorem tailStable_and {P Q : Nat → Prop}
    (hP : TailStable P) (hQ : TailStable Q) :
    TailStable (fun k => P k ∧ Q k) := by
  rcases hP with ⟨KP, hKP⟩
  rcases hQ with ⟨KQ, hKQ⟩
  let K := max KP KQ
  have hpK : KP ≤ K := Nat.le_max_left KP KQ
  have hqK : KQ ≤ K := Nat.le_max_right KP KQ
  refine ⟨K, fun k hk => ?_⟩
  have hp : P k ↔ P K :=
    (hKP k (Nat.le_trans hpK hk)).trans (hKP K hpK).symm
  have hq : Q k ↔ Q K :=
    (hKQ k (Nat.le_trans hqK hk)).trans (hKQ K hqK).symm
  exact and_congr hp hq

theorem tailStable_iff_eventually_or_not {P : Nat → Prop} :
    TailStable P ↔ Eventually P ∨ Eventually (fun k => ¬ P k) := by
  classical
  constructor
  · rintro ⟨K, hK⟩
    by_cases hp : P K
    · exact Or.inl ⟨K, fun k hk => (hK k hk).mpr hp⟩
    · exact Or.inr ⟨K, fun k hk hp' => hp ((hK k hk).mp hp')⟩
  · intro h
    rcases h with h | h
    · exact tailStable_of_eventually h
    · exact tailStable_of_eventually_not h

theorem eventually_forall_list {α : Type u} (xs : List α)
    {P : α → Nat → Prop} (hP : ∀ a, a ∈ xs → Eventually (P a)) :
    Eventually (fun k => ∀ a, a ∈ xs → P a k) := by
  induction xs with
  | nil =>
      exact eventually_of_forall (by simp)
  | cons a xs ih =>
      have ha : Eventually (P a) := hP a (by simp)
      have hxs : Eventually (fun k => ∀ b, b ∈ xs → P b k) :=
        ih (fun b hb => hP b (by simp [hb]))
      apply eventually_mono (eventually_and ha hxs)
      intro k hk b hb
      rcases List.mem_cons.mp hb with hba | hbx
      · simpa only [hba] using hk.1
      · exact hk.2 b hbx

theorem tailStable_forall_list {α : Type u} (xs : List α)
    {P : α → Nat → Prop} (hP : ∀ a, a ∈ xs → TailStable (P a)) :
    TailStable (fun k => ∀ a, a ∈ xs → P a k) := by
  induction xs with
  | nil =>
      exact tailStable_of_eventually (eventually_of_forall (by simp))
  | cons a xs ih =>
      have ha : TailStable (P a) := hP a (by simp)
      have hxs : TailStable (fun k => ∀ b, b ∈ xs → P b k) :=
        ih (fun b hb => hP b (by simp [hb]))
      apply tailStable_congr (P := fun k => P a k ∧ (∀ b, b ∈ xs → P b k))
      · intro k
        simp
      · exact tailStable_and ha hxs

/-- Stability of a conjunction over all positive times up to a fixed bound. -/
theorem tailStable_forall_pos_le (B : Nat) {R : Nat → Nat → Prop}
    (hR : ∀ t, 1 ≤ t → t ≤ B → TailStable (R t)) :
    TailStable (fun k => ∀ t, 1 ≤ t → t ≤ B → R t k) := by
  have hlist : TailStable (fun k => ∀ j, j ∈ List.range B → R (j + 1) k) := by
    apply tailStable_forall_list
    intro j hj
    have hjB := List.mem_range.mp hj
    exact hR (j + 1) (by omega) (by omega)
  apply tailStable_congr (P := fun k => ∀ j, j ∈ List.range B → R (j + 1) k)
  · intro k
    constructor
    · intro h t ht hB
      have hj : t - 1 ∈ List.range B := List.mem_range.mpr (by omega)
      have he : t - 1 + 1 = t := Nat.sub_add_cancel ht
      simpa only [he] using h (t - 1) hj
    · intro h j hj
      have hjB := List.mem_range.mp hj
      exact h (j + 1) (by omega) (by omega)
  · exact hlist

/-- A finite eventually stable cover contains a member true on an entire tail.
No assumption that the list is nonempty or duplicate-free is needed: a cover
of an empty list is impossible, and repetitions do not affect the conclusion. -/
theorem uniform_tail_of_finite_cover {α : Type u} (xs : List α)
    {R : α → Nat → Prop}
    (hStable : ∀ t, t ∈ xs → TailStable (R t))
    (hCover : Eventually (fun k => ∃ t, t ∈ xs ∧ R t k)) :
    ∃ t, t ∈ xs ∧ Eventually (R t) := by
  induction xs with
  | nil =>
      rcases hCover with ⟨K, hK⟩
      rcases hK K (Nat.le_refl K) with ⟨t, ht, _⟩
      simp at ht
  | cons a xs ih =>
      have ha := (tailStable_iff_eventually_or_not).mp (hStable a (by simp))
      rcases ha with ha | ha
      · exact ⟨a, by simp, ha⟩
      · have hTailCover : Eventually (fun k => ∃ t, t ∈ xs ∧ R t k) := by
          apply eventually_mono (eventually_and hCover ha)
          intro k hk
          rcases hk.1 with ⟨t, ht, hrt⟩
          rcases List.mem_cons.mp ht with hta | htx
          · subst t
            exact False.elim (hk.2 hrt)
          · exact ⟨t, htx, hrt⟩
        rcases ih (fun t ht => hStable t (by simp [ht])) hTailCover with
          ⟨t, ht, hrt⟩
        exact ⟨t, by simp [ht], hrt⟩

/-- The finite-cover selector for candidate times `1, ..., B`.  The selected
time is positive and bounded.  The parameter cutoff can increase. -/
theorem uniform_bounded_tail_selection (B : Nat) {R : Nat → Nat → Prop}
    (hStable : ∀ t, 1 ≤ t → t ≤ B → TailStable (R t))
    (hCover : Eventually (fun k => ∃ t, 1 ≤ t ∧ t ≤ B ∧ R t k)) :
    ∃ t, 1 ≤ t ∧ t ≤ B ∧ Eventually (R t) := by
  have hListStable : ∀ j, j ∈ List.range B → TailStable (R (j + 1)) := by
    intro j hj
    have hjB := List.mem_range.mp hj
    exact hStable (j + 1) (by omega) (by omega)
  have hListCover : Eventually (fun k => ∃ j, j ∈ List.range B ∧ R (j + 1) k) := by
    apply eventually_mono hCover
    intro k hk
    rcases hk with ⟨t, ht, hB, hRt⟩
    refine ⟨t - 1, List.mem_range.mpr (by omega), ?_⟩
    have he : t - 1 + 1 = t := Nat.sub_add_cancel ht
    simpa only [he] using hRt
  rcases uniform_tail_of_finite_cover (List.range B) hListStable hListCover with
    ⟨j, hj, hRj⟩
  have hjB := List.mem_range.mp hj
  exact ⟨j + 1, by omega, by omega, hRj⟩

/-- Equality of a proposed return and safety at every positive intermediate
output remain jointly stable on a tail. -/
theorem return_and_safety_tailStable (t : Nat)
    {Return : Nat → Nat → Prop} {Safe : Nat → Nat → Prop}
    (hReturn : TailStable (Return t))
    (hSafe : ∀ i, 1 ≤ i → i ≤ t → TailStable (Safe i)) :
    TailStable (fun k => Return t k ∧ ∀ i, 1 ≤ i → i ≤ t → Safe i k) :=
  tailStable_and hReturn (tailStable_forall_pos_le t hSafe)

/-- Abstract final interface: bounded positive safe returns covering a tail
have a single positive safe return time valid on a whole tail.  Actual word
closure, equality/safety stability and the arithmetic time bound must be
supplied by the application; none is inferred in this module. -/
theorem uniform_safe_return_time (B : Nat)
    {Return : Nat → Nat → Prop} {Safe : Nat → Nat → Prop}
    (hReturn : ∀ t, 1 ≤ t → t ≤ B → TailStable (Return t))
    (hSafe : ∀ i, 1 ≤ i → i ≤ B → TailStable (Safe i))
    (hCover : Eventually (fun k =>
      ∃ t, 1 ≤ t ∧ t ≤ B ∧ Return t k ∧ ∀ i, 1 ≤ i → i ≤ t → Safe i k)) :
    ∃ t, 1 ≤ t ∧ t ≤ B ∧ ∃ K, ∀ k, K ≤ k →
      Return t k ∧ ∀ i, 1 ≤ i → i ≤ t → Safe i k := by
  apply uniform_bounded_tail_selection B
  · intro t ht hB
    exact return_and_safety_tailStable t (hReturn t ht hB)
      (fun i hi hit => hSafe i hi (Nat.le_trans hit hB))
  · exact hCover

end Agent105.TailSelection
