import P196.Agent101ProtectedFamily.FamilyDefinitions

/-!
Agent #3: exact enumeration and cardinality for the finite-horizon overflow
family. Every binary list of the prescribed length appears exactly once.
The construction is injective for each fixed reservoir size, so mapping the
enumeration produces exactly `2 ^ m` distinct canonical coefficient words.

All claims are about the definitions in `FamilyDefinitions`; this module
neither assumes nor changes a reverse-add transition theorem.
-/

namespace P196.Agent3.OverflowHorizon

open Agent8

/-- All binary lists of length `m`, in false-before-true recursive order. -/
def allBits : Nat → List (List Bool)
  | 0 => [[]]
  | m + 1 => (allBits m).map (false :: ·) ++ (allBits m).map (true :: ·)

theorem allBits_length (m : Nat) : (allBits m).length = 2 ^ m := by
  induction m with
  | zero => rfl
  | succ m ih =>
    simp only [allBits, List.length_append, List.length_map, ih, Nat.pow_succ]
    omega

theorem mem_allBits_iff (xs : List Bool) (m : Nat) :
    xs ∈ allBits m ↔ xs.length = m := by
  induction m generalizing xs with
  | zero => simp [allBits]
  | succ m ih =>
    cases xs with
    | nil => simp [allBits]
    | cons b xs => cases b <;> simp [allBits, ih]

/-- Std-only preservation of distinctness under an injective map. -/
private theorem nodup_map_of_injective {α β : Type} (f : α → β)
    (hf : ∀ a b, f a = f b → a = b) (xs : List α) (hxs : xs.Nodup) :
    (xs.map f).Nodup := by
  exact List.Pairwise.map f (fun a b hab heq => hab (hf a b heq)) hxs

theorem allBits_nodup (m : Nat) : (allBits m).Nodup := by
  induction m with
  | zero => simp [allBits]
  | succ m ih =>
    change List.Pairwise (fun a b => a ≠ b)
      ((allBits m).map (false :: ·) ++ (allBits m).map (true :: ·))
    apply List.pairwise_append.mpr
    refine ⟨nodup_map_of_injective (false :: ·) (by
      intro a b h; exact (List.cons.inj h).2) _ ih,
      nodup_map_of_injective (true :: ·) (by
      intro a b h; exact (List.cons.inj h).2) _ ih, ?_⟩
    intro a ha b hb heq
    rcases List.mem_map.mp ha with ⟨xs, _, rfl⟩
    rcases List.mem_map.mp hb with ⟨ys, _, rfl⟩
    cases heq

theorem choice_injective (a b : Bool) (h : choice a = choice b) : a = b := by
  cases a <;> cases b <;> simp_all [choice]

theorem choice_le_eighteen (b : Bool) : choice b ≤ 18 := by
  cases b <;> decide

theorem choice_map_injective (xs ys : List Bool)
    (h : xs.map choice = ys.map choice) : xs = ys := by
  induction xs generalizing ys with
  | nil => cases ys <;> simp_all
  | cons b xs ih =>
    cases ys with
    | nil => simp at h
    | cons c ys =>
      have hparts := List.cons.inj h
      have hbc := choice_injective b c hparts.1
      have hxy := ih ys hparts.2
      simp [hbc, hxy]

theorem inputHalf_length (xs : List Bool) (k : Nat) :
    (inputHalf xs k).length = xs.length + k + 1 := by
  simp only [inputHalf, List.length_append, List.length_map,
    List.length_replicate, List.length_cons, List.length_nil]
  omega

theorem inputWord_length (xs : List Bool) (k : Nat) :
    (inputWord xs k).length = 2 * (xs.length + k + 1) := by
  simp only [inputWord, List.length_append, List.length_reverse, inputHalf_length]
  omega

/-- The mirrored construction does not identify two different binary choices. -/
theorem inputWord_injective (k : Nat) (xs ys : List Bool)
    (h : inputWord xs k = inputWord ys k) : xs = ys := by
  have hlen := congrArg List.length h
  simp only [inputWord, List.length_append, List.length_reverse] at hlen
  have hhalf := (List.append_inj h (by omega)).1
  change 14 :: (xs.map choice ++ List.replicate k 18) =
    14 :: (ys.map choice ++ List.replicate k 18) at hhalf
  have htail := (List.cons.inj hhalf).2
  exact choice_map_injective xs ys (List.append_cancel_right htail)

theorem inputHalf_bounded (xs : List Bool) (k : Nat) :
    Bounded (inputHalf xs k) 18 := by
  intro a ha
  simp only [inputHalf, List.mem_append, List.mem_singleton] at ha
  rcases ha with (hhead | hchoice) | hrep
  · omega
  · rcases List.mem_map.mp hchoice with ⟨b, _, rfl⟩
    exact choice_le_eighteen b
  · have h := List.mem_replicate.mp hrep
    omega

theorem inputWord_bounded (xs : List Bool) (k : Nat) :
    Bounded (inputWord xs k) 18 := by
  intro a ha
  simp only [inputWord, List.mem_append, List.mem_reverse] at ha
  rcases ha with ha | ha <;> exact inputHalf_bounded xs k a ha

theorem inputWord_symmetric (xs : List Bool) (k : Nat) :
    (inputWord xs k).reverse = inputWord xs k := by
  simp [inputWord, List.reverse_append]

theorem inputWord_head (xs : List Bool) (k : Nat) :
    (inputWord xs k).headD 0 = 14 := by
  simp [inputWord, inputHalf]

/-- Canonicality already holds at `k = 0`; transition results may require `k ≥ 1`. -/
theorem inputWord_canonical (xs : List Bool) (k : Nat) :
    CanonicalPair (inputWord xs k) := by
  refine ⟨?_, inputWord_symmetric xs k, inputWord_bounded xs k, ?_⟩
  · intro hnil
    have hlen := inputWord_length xs k
    simp only [hnil, List.length_nil] at hlen
    omega
  · rw [inputWord_head]
    decide

/-- Even width leaves no unpaired central coefficient. -/
theorem inputWord_even_width (xs : List Bool) (k : Nat) :
    (inputWord xs k).length % 2 = 0 := by
  rw [inputWord_length]
  omega

theorem inputWord_canonical_even (xs : List Bool) (k : Nat) :
    CanonicalPair (inputWord xs k) ∧ (inputWord xs k).length % 2 = 0 :=
  ⟨inputWord_canonical xs k, inputWord_even_width xs k⟩

/-- The fully enumerated family at choice width `m` and reservoir size `k`. -/
def familyWords (m k : Nat) : List Word :=
  (allBits m).map (fun xs => inputWord xs k)

theorem familyWords_length (m k : Nat) : (familyWords m k).length = 2 ^ m := by
  simp [familyWords, allBits_length]

theorem familyWords_nodup (m k : Nat) : (familyWords m k).Nodup := by
  exact nodup_map_of_injective (fun xs => inputWord xs k)
    (inputWord_injective k) (allBits m) (allBits_nodup m)

theorem mem_familyWords_iff (w : Word) (m k : Nat) :
    w ∈ familyWords m k ↔ ∃ xs : List Bool, xs.length = m ∧ inputWord xs k = w := by
  simp [familyWords, List.mem_map, mem_allBits_iff]

theorem familyWords_member_properties (m k : Nat) (w : Word)
    (hw : w ∈ familyWords m k) :
    CanonicalPair w ∧ w.length = 2 * (m + k + 1) ∧ w.length % 2 = 0 := by
  rcases (mem_familyWords_iff w m k).mp hw with ⟨xs, hlen, rfl⟩
  exact ⟨inputWord_canonical xs k, by rw [inputWord_length, hlen],
    inputWord_even_width xs k⟩

/-- Exact finite cardinality, distinctness, canonicality, and uniform width. -/
theorem familyWords_exact (m k : Nat) :
    (familyWords m k).length = 2 ^ m ∧
    (familyWords m k).Nodup ∧
    ∀ w ∈ familyWords m k,
      CanonicalPair w ∧ w.length = 2 * (m + k + 1) ∧ w.length % 2 = 0 := by
  exact ⟨familyWords_length m k, familyWords_nodup m k,
    familyWords_member_properties m k⟩

#print axioms allBits
#print axioms allBits_length
#print axioms mem_allBits_iff
#print axioms nodup_map_of_injective
#print axioms allBits_nodup
#print axioms choice_injective
#print axioms choice_le_eighteen
#print axioms choice_map_injective
#print axioms inputHalf_length
#print axioms inputWord_length
#print axioms inputWord_injective
#print axioms inputHalf_bounded
#print axioms inputWord_bounded
#print axioms inputWord_symmetric
#print axioms inputWord_head
#print axioms inputWord_canonical
#print axioms inputWord_even_width
#print axioms inputWord_canonical_even
#print axioms familyWords
#print axioms familyWords_length
#print axioms familyWords_nodup
#print axioms mem_familyWords_iff
#print axioms familyWords_member_properties
#print axioms familyWords_exact

end P196.Agent3.OverflowHorizon
