import P196.Agent105AllPredecessors.Agent101ProfileExtraction
import P196.Drafts.Agent9FiniteEnsembleMarkerCount.Agent9FiniteProducts

/-!
Finite enumeration of symmetric coefficient words whose entries are even
and at most eighteen. Zero coefficients, including outer zeros, are allowed.
Each word occurs once, and the number of words depends only on its width.
-/

namespace OddPredecessorTargetCensus

open Agent101 P196.Agent9.Ensemble

/-- All possible even decimal pair sums, including zero. -/
def evenCoefficients : List Nat := [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

/-- Enumerate symmetric bounded even words by adding equal outer entries. -/
def evenWords : Nat → List (List Nat)
  | 0 => [[]]
  | 1 => evenCoefficients.map (fun s => [s])
  | n + 2 => evenCoefficients.flatMap fun s =>
      (evenWords n).map (wrapDigits s s)

theorem mem_evenCoefficients (s : Nat) :
    s ∈ evenCoefficients ↔ s ≤ 18 ∧ s % 2 = 0 := by
  simp only [evenCoefficients, List.mem_cons, List.mem_singleton,
    List.not_mem_nil, or_false]
  omega

/-- Membership specifies the exact width, symmetry, and allowed entries. -/
theorem mem_evenWords (L : Nat) (qs : List Nat) :
    qs ∈ evenWords L ↔
      qs.length = L ∧ qs.reverse = qs ∧ ∀ s ∈ qs, s ≤ 18 ∧ s % 2 = 0 := by
  induction L using Nat.strongRecOn generalizing qs with
  | ind L ih =>
    cases L with
    | zero => cases qs <;> simp [evenWords]
    | succ L =>
      cases L with
      | zero =>
        rw [evenWords]
        constructor
        · intro hq
          obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hq
          refine ⟨rfl, rfl, ?_⟩
          intro t ht
          simp only [List.mem_singleton] at ht
          subst t
          exact (mem_evenCoefficients s).mp hs
        · rintro ⟨hlen, _, hb⟩
          obtain ⟨s, rfl⟩ := List.length_eq_one_iff.mp hlen
          exact List.mem_map.mpr
            ⟨s, (mem_evenCoefficients s).mpr (hb s (by simp)), rfl⟩
      | succ n =>
        rw [evenWords]
        constructor
        · intro hq
          obtain ⟨s, hs, hq⟩ := List.mem_flatMap.mp hq
          obtain ⟨inner, hi, rfl⟩ := List.mem_map.mp hq
          obtain ⟨hlen, hrev, hb⟩ := (ih n (by omega) inner).mp hi
          have hs' := (mem_evenCoefficients s).mp hs
          refine ⟨by simp only [length_wrapDigits, hlen], ?_, ?_⟩
          · rw [reverse_wrapDigits, hrev]
          · intro t ht
            simp only [wrapDigits, List.mem_cons, List.mem_append,
              List.mem_singleton, List.not_mem_nil, or_false] at ht
            rcases ht with rfl | ht | rfl
            · exact hs'
            · exact hb t ht
            · exact hs'
        · rintro ⟨hlen, hrev, hb⟩
          obtain ⟨a, b, inner, rfl⟩ := exists_wrapDigits qs (by omega)
          rw [reverse_wrapDigits] at hrev
          obtain ⟨hba, _, hinnerrev⟩ := wrapDigits_injective _ _ _ _ _ _ hrev
          subst b
          have hinnerlen : inner.length = n := by
            rw [length_wrapDigits] at hlen
            omega
          apply List.mem_flatMap.mpr
          refine ⟨a, (mem_evenCoefficients a).mpr (hb a (by simp [wrapDigits])),
            List.mem_map.mpr ⟨inner, ?_, rfl⟩⟩
          apply (ih n (by omega) inner).mpr
          exact ⟨hinnerlen, hinnerrev,
            fun s hs => hb s (by simp [wrapDigits, hs])⟩

/-- The recursive enumeration contains no repeated coefficient word. -/
theorem evenWords_nodup (L : Nat) : (evenWords L).Nodup := by
  induction L using Nat.strongRecOn with
  | ind L ih =>
    cases L with
    | zero => simp [evenWords]
    | succ L =>
      cases L with
      | zero => decide
      | succ n =>
        rw [evenWords]
        apply nodup_flatMap_map _ _ _ (by decide) (ih n (by omega))
        intro a _ a' _ inner _ inner' _ heq
        obtain ⟨ha, _, hi⟩ := wrapDigits_injective _ _ _ _ _ _ heq
        exact ⟨ha, hi⟩

/-- There are ten choices at each position in the first half and center. -/
theorem length_evenWords (L : Nat) :
    (evenWords L).length = 10 ^ ((L + 1) / 2) := by
  induction L using Nat.strongRecOn with
  | ind L ih =>
    cases L with
    | zero => rfl
    | succ L =>
      cases L with
      | zero => rfl
      | succ n =>
        rw [evenWords, length_flatMap_map, ih n (by omega)]
        change 10 * 10 ^ ((n + 1) / 2) = 10 ^ ((n + 3) / 2)
        have hexp : (n + 3) / 2 = (n + 1) / 2 + 1 := by omega
        rw [hexp, Nat.pow_succ]
        exact Nat.mul_comm _ _

#print axioms evenCoefficients
#print axioms evenWords
#print axioms mem_evenCoefficients
#print axioms mem_evenWords
#print axioms evenWords_nodup
#print axioms length_evenWords

end OddPredecessorTargetCensus
