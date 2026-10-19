import P196.OddPredecessorTargetCensus.Profiles

/-!
# Uniform outer-wrapper form of the coefficient census

Agent #6: from source width three onward, either coefficient language is
an allowed outer pair surrounding a nonempty even symmetric inner word.
This isolates the list construction from the decimal carry classification.
-/

set_option autoImplicit false

namespace OddPredecessorTargetCensus

open Agent101

private theorem mem_center_prefixes (ps : List (Nat × Nat))
    (hp : ∀ p ∈ ps, p.2 ∈ evenCoefficients) (qs : List Nat) :
    qs ∈ ps.map (fun p => wrapDigits p.1 p.1 [p.2]) ↔
      ∃ s xs, qs = wrapDigits s s xs ∧ xs ∈ evenWords 1 ∧
        (s, digitFn xs 0) ∈ ps := by
  constructor
  · intro hq
    obtain ⟨p, hp', rfl⟩ := List.mem_map.mp hq
    refine ⟨p.1, [p.2], rfl, ?_, ?_⟩
    · exact List.mem_map.mpr ⟨p.2, hp p hp', rfl⟩
    · simpa only [digitFn, List.getElem?_cons_zero, Option.getD_some] using hp'
  · rintro ⟨s, xs, rfl, hx, hp'⟩
    obtain ⟨t, _, rfl⟩ := List.mem_map.mp hx
    exact List.mem_map.mpr ⟨(s, t), hp', rfl⟩

private theorem mem_wrapped_prefixes (ps : List (Nat × Nat))
    (hp : ∀ p ∈ ps, p.2 ∈ evenCoefficients) (k : Nat) (qs : List Nat) :
    qs ∈ ps.flatMap (fun p => (evenWords k).map
      (fun xs => wrapDigits p.1 p.1 (wrapDigits p.2 p.2 xs))) ↔
      ∃ s xs, qs = wrapDigits s s xs ∧ xs ∈ evenWords (k + 2) ∧
        (s, digitFn xs 0) ∈ ps := by
  constructor
  · intro hq
    obtain ⟨p, hp', hq⟩ := List.mem_flatMap.mp hq
    obtain ⟨inner, hi, rfl⟩ := List.mem_map.mp hq
    refine ⟨p.1, wrapDigits p.2 p.2 inner, rfl, ?_, ?_⟩
    · exact List.mem_flatMap.mpr ⟨p.2, hp p hp',
        List.mem_map.mpr ⟨inner, hi, rfl⟩⟩
    · simpa only [digitFn, wrapDigits, List.getElem?_cons_zero,
        Option.getD_some] using hp'
  · rintro ⟨s, xs, rfl, hx, hp'⟩
    obtain ⟨t, _, hx⟩ := List.mem_flatMap.mp hx
    obtain ⟨inner, hi, rfl⟩ := List.mem_map.mp hx
    exact List.mem_flatMap.mpr ⟨(s, t), hp', List.mem_map.mpr ⟨inner, hi, rfl⟩⟩

/-- At every source width at least three, the no-overflow list has one
uniform outer-wrapper description with an even nonempty inner word. -/
theorem mem_noOverflowWords_large (L : Nat) (qs : List Nat) (hL : 3 ≤ L) :
    qs ∈ noOverflowWords L ↔
      ∃ s xs, qs = wrapDigits s s xs ∧ xs ∈ evenWords (L - 2) ∧
        (s, digitFn xs 0) ∈ noOverflowPrefixes := by
  have hp : ∀ p ∈ noOverflowPrefixes, p.2 ∈ evenCoefficients := by
    intro p hp
    have ht := (mem_noOverflowPrefixes p.1 p.2).mp hp
    exact (mem_evenCoefficients p.2).mpr ⟨ht.2.2.1, ht.2.2.2.1⟩
  match L with
  | 0 => omega
  | 1 => omega
  | 2 => omega
  | 3 => exact mem_center_prefixes noOverflowPrefixes hp qs
  | k + 4 =>
    have hk : k + 4 - 2 = k + 2 := by omega
    simpa only [noOverflowWords, hk] using
      mem_wrapped_prefixes noOverflowPrefixes hp k qs

/-- The same uniform outer-wrapper description holds for overflow,
with its separate fifty-five permitted outer coefficient pairs. -/
theorem mem_overflowWords_large (L : Nat) (qs : List Nat) (hL : 3 ≤ L) :
    qs ∈ overflowWords L ↔
      ∃ s xs, qs = wrapDigits s s xs ∧ xs ∈ evenWords (L - 2) ∧
        (s, digitFn xs 0) ∈ overflowPrefixes := by
  have hp : ∀ p ∈ overflowPrefixes, p.2 ∈ evenCoefficients := by
    intro p hp
    have ht := (mem_overflowPrefixes p.1 p.2).mp hp
    exact (mem_evenCoefficients p.2).mpr ⟨ht.1, ht.2.1⟩
  match L with
  | 0 => omega
  | 1 => omega
  | 2 => omega
  | 3 => exact mem_center_prefixes overflowPrefixes hp qs
  | k + 4 =>
    have hk : k + 4 - 2 = k + 2 := by omega
    simpa only [overflowWords, hk] using
      mem_wrapped_prefixes overflowPrefixes hp k qs

end OddPredecessorTargetCensus

#print axioms OddPredecessorTargetCensus.mem_noOverflowWords_large
#print axioms OddPredecessorTargetCensus.mem_overflowWords_large
