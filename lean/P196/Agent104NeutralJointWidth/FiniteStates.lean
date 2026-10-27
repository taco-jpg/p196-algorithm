import P196.Drafts.Agent120NeutralBandCalibration.A120Certificate

/-!
# Explicit finite words and joint interface states

This is an enumeration specification, not a claim of practical complexity.
The carrier includes every coefficient word allowed by the original Hyp.
-/

namespace Agent104.NeutralJointWidth

open Agent120.Neutral

abbrev State := List Nat × List Nat

/-- All lists of the given length over a finite alphabet, retaining duplicates. -/
def listsOf {α : Type} (alphabet : List α) : Nat → List (List α)
  | 0 => [[]]
  | n + 1 => alphabet.flatMap fun a => (listsOf alphabet n).map (List.cons a)

private theorem flatMap_length_const {α β : Type} (xs : List α) (f : α → List β)
    (n : Nat) (hf : ∀ a ∈ xs, (f a).length = n) :
    (xs.flatMap f).length = xs.length * n := by
  induction xs with
  | nil => simp
  | cons a xs ih =>
      have ha := hf a List.mem_cons_self
      have ht : ∀ x ∈ xs, (f x).length = n :=
        fun x hx => hf x (List.mem_cons_of_mem a hx)
      simp only [List.flatMap_cons, List.length_append, ha, ih ht, List.length_cons]
      simp [Nat.add_mul, Nat.add_comm]

theorem listsOf_length {α : Type} (alphabet : List α) (n : Nat) :
    (listsOf alphabet n).length = alphabet.length ^ n := by
  induction n with
  | zero => simp [listsOf]
  | succ n ih =>
      rw [listsOf, flatMap_length_const alphabet _ (alphabet.length ^ n)]
      · simp [Nat.pow_succ, Nat.mul_comm]
      · intro a ha
        simpa using ih

theorem mem_listsOf {α : Type} (alphabet : List α) (n : Nat) (xs : List α) :
    xs ∈ listsOf alphabet n ↔ xs.length = n ∧ ∀ x ∈ xs, x ∈ alphabet := by
  induction n generalizing xs with
  | zero =>
      simp only [listsOf, List.mem_singleton, List.length_eq_zero_iff]
      constructor
      · intro h
        subst xs
        simp
      · exact fun h => h.1
  | succ n ih =>
      constructor
      · intro h
        obtain ⟨a, ha, hm⟩ := List.mem_flatMap.mp h
        obtain ⟨tail, ht, heq⟩ := List.mem_map.mp hm
        subst xs
        have hh := (ih tail).mp ht
        refine ⟨by simp [hh.1], ?_⟩
        intro x hx
        rcases List.mem_cons.mp hx with hx | hx
        · simpa [hx] using ha
        · exact hh.2 x hx
      · rintro ⟨hlen, hall⟩
        cases xs with
        | nil => simp at hlen
        | cons a tail =>
            have htlen : tail.length = n := by simpa using hlen
            have ht : tail ∈ listsOf alphabet n :=
              (ih tail).mpr ⟨htlen, fun x hx => hall x (List.mem_cons_of_mem a hx)⟩
            exact List.mem_flatMap.mpr ⟨a, hall a List.mem_cons_self,
              List.mem_map.mpr ⟨tail, ht, rfl⟩⟩

def words (q n : Nat) : List (List Nat) := listsOf (List.range q) n

theorem words_length (q n : Nat) : (words q n).length = q ^ n := by
  simp [words, listsOf_length]

theorem mem_words (q n : Nat) (xs : List Nat) :
    xs ∈ words q n ↔ xs.length = n ∧ ∀ x ∈ xs, x < q := by
  simp [words, mem_listsOf]

/-- An intentionally coarse carrier: every coefficient-bounded word at these widths. -/
def states (b M W : Nat) : List State :=
  (words (2 * b - 1) M).flatMap fun B =>
    (words (2 * b - 1) (W - 1) ++ words (2 * b - 1) W).map fun C => (B, C)

def stateBound (b M W : Nat) : Nat :=
  (2 * b - 1) ^ M * ((2 * b - 1) ^ (W - 1) + (2 * b - 1) ^ W)

theorem states_length (b M W : Nat) : (states b M W).length = stateBound b M W := by
  unfold states stateBound
  rw [flatMap_length_const _ _ ((2 * b - 1) ^ (W - 1) + (2 * b - 1) ^ W)]
  · rw [words_length]
  · intro B hB
    simp [words_length]

theorem mem_states (b M W : Nat) (B C : List Nat) :
    (B, C) ∈ states b M W ↔
      B.length = M ∧ (C.length = W - 1 ∨ C.length = W) ∧
      (∀ x ∈ B, x < 2 * b - 1) ∧ (∀ x ∈ C, x < 2 * b - 1) := by
  simp only [states, List.mem_flatMap, List.mem_map, List.mem_append]
  constructor
  · rintro ⟨B', hB, C', hC, heq⟩
    cases heq
    have hb := (mem_words _ _ _).mp hB
    rcases hC with hC | hC
    · have hc := (mem_words _ _ _).mp hC
      exact ⟨hb.1, Or.inl hc.1, hb.2, hc.2⟩
    · have hc := (mem_words _ _ _).mp hC
      exact ⟨hb.1, Or.inr hc.1, hb.2, hc.2⟩
  · rintro ⟨hB, hC, hb, hc⟩
    refine ⟨B, (mem_words _ _ _).mpr ⟨hB, hb⟩, C, ?_, rfl⟩
    rcases hC with hC | hC
    · exact Or.inl ((mem_words _ _ _).mpr ⟨hC, hc⟩)
    · exact Or.inr ((mem_words _ _ _).mpr ⟨hC, hc⟩)

theorem hyp_mem_states {b M W : Nat} {B C : List Nat}
    (h : Hyp b B C) (hB : B.length = M)
    (hC : C.length = W - 1 ∨ C.length = W) : (B, C) ∈ states b M W := by
  apply (mem_states _ _ _ _ _).mpr
  refine ⟨hB, hC, ?_, ?_⟩
  · intro x hx
    have hb := h.boundB x hx
    have hbase := h.base
    omega
  · intro x hx
    have hc := h.boundC x hx
    have hbase := h.base
    omega

end Agent104.NeutralJointWidth

#print axioms Agent104.NeutralJointWidth.listsOf_length
#print axioms Agent104.NeutralJointWidth.mem_listsOf
#print axioms Agent104.NeutralJointWidth.words_length
#print axioms Agent104.NeutralJointWidth.mem_words
#print axioms Agent104.NeutralJointWidth.states_length
#print axioms Agent104.NeutralJointWidth.mem_states
#print axioms Agent104.NeutralJointWidth.hyp_mem_states
