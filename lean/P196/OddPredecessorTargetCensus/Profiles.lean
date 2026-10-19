import P196.OddPredecessorTargetCensus.PrefixPairs
import P196.Drafts.Agent9FiniteEnsembleMarkerCount.Agent9FiniteProducts

/-!
# Complete finite coefficient families for the odd-multiplicity census

Agent #6: the first three widths retain their exact singleton, pair and
center cases. At every larger width, the two independent outer choices
surround an arbitrary even symmetric coefficient word. Generic finite
products are imported unchanged for duplicate freedom and exact counting.
-/

set_option autoImplicit false

namespace OddPredecessorTargetCensus

open Agent101 P196.Agent9.Ensemble

/-- Odd-multiplicity coefficient words in the no-overflow class. -/
def noOverflowWords : Nat → List (List Nat)
  | 0 => []
  | 1 => [2, 4, 6, 8].map (fun s => [s])
  | 2 => [1, 3, 5, 7, 9].map (fun s => [s, s])
  | 3 => noOverflowPrefixes.map (fun p => wrapDigits p.1 p.1 [p.2])
  | k + 4 => noOverflowPrefixes.flatMap fun p =>
      (evenWords k).map (fun qs => wrapDigits p.1 p.1 (wrapDigits p.2 p.2 qs))

/-- Odd-multiplicity coefficient words in the overflow class. -/
def overflowWords : Nat → List (List Nat)
  | 0 => []
  | 1 => [10, 12, 14, 16, 18].map (fun s => [s])
  | 2 => [10, 12, 14, 16, 18].map (fun s => [s, s])
  | 3 => overflowPrefixes.map (fun p => wrapDigits p.1 p.1 [p.2])
  | k + 4 => overflowPrefixes.flatMap fun p =>
      (evenWords k).map (fun qs => wrapDigits p.1 p.1 (wrapDigits p.2 p.2 qs))

theorem mem_noOverflowWords_shape (L : Nat) (qs : List Nat) :
    qs ∈ noOverflowWords L ↔
      match L with
      | 0 => False
      | 1 => ∃ s, s ∈ [2, 4, 6, 8] ∧ qs = [s]
      | 2 => ∃ s, s ∈ [1, 3, 5, 7, 9] ∧ qs = [s, s]
      | 3 => ∃ p, p ∈ noOverflowPrefixes ∧ qs = wrapDigits p.1 p.1 [p.2]
      | k + 4 => ∃ p, p ∈ noOverflowPrefixes ∧
          ∃ inner, inner ∈ evenWords k ∧
            qs = wrapDigits p.1 p.1 (wrapDigits p.2 p.2 inner) := by
  match L with
  | 0 => simp [noOverflowWords]
  | 1 => simp only [noOverflowWords, List.mem_map, eq_comm]
  | 2 => simp only [noOverflowWords, List.mem_map, eq_comm]
  | 3 => simp only [noOverflowWords, List.mem_map, eq_comm]
  | k + 4 => simp only [noOverflowWords, List.mem_flatMap, List.mem_map, eq_comm]

theorem mem_overflowWords_shape (L : Nat) (qs : List Nat) :
    qs ∈ overflowWords L ↔
      match L with
      | 0 => False
      | 1 => ∃ s, s ∈ [10, 12, 14, 16, 18] ∧ qs = [s]
      | 2 => ∃ s, s ∈ [10, 12, 14, 16, 18] ∧ qs = [s, s]
      | 3 => ∃ p, p ∈ overflowPrefixes ∧ qs = wrapDigits p.1 p.1 [p.2]
      | k + 4 => ∃ p, p ∈ overflowPrefixes ∧
          ∃ inner, inner ∈ evenWords k ∧
            qs = wrapDigits p.1 p.1 (wrapDigits p.2 p.2 inner) := by
  match L with
  | 0 => simp [overflowWords]
  | 1 => simp only [overflowWords, List.mem_map, eq_comm]
  | 2 => simp only [overflowWords, List.mem_map, eq_comm]
  | 3 => simp only [overflowWords, List.mem_map, eq_comm]
  | k + 4 => simp only [overflowWords, List.mem_flatMap, List.mem_map, eq_comm]

theorem noOverflowWords_nodup (L : Nat) : (noOverflowWords L).Nodup := by
  match L with
  | 0 => decide
  | 1 => decide
  | 2 => decide
  | 3 => decide
  | k + 4 =>
    apply nodup_flatMap_map noOverflowPrefixes (evenWords k)
      (fun p qs => wrapDigits p.1 p.1 (wrapDigits p.2 p.2 qs))
      noOverflowPrefixes_nodup (evenWords_nodup k)
    intro p _ p' _ xs _ ys _ heq
    have houter := wrapDigits_injective p.1 p.1 p'.1 p'.1
      (wrapDigits p.2 p.2 xs) (wrapDigits p'.2 p'.2 ys) heq
    have hinner := wrapDigits_injective p.2 p.2 p'.2 p'.2 xs ys houter.2.2
    exact ⟨Prod.ext houter.1 hinner.1, hinner.2.2⟩

theorem overflowWords_nodup (L : Nat) : (overflowWords L).Nodup := by
  match L with
  | 0 => decide
  | 1 => decide
  | 2 => decide
  | 3 => decide
  | k + 4 =>
    apply nodup_flatMap_map overflowPrefixes (evenWords k)
      (fun p qs => wrapDigits p.1 p.1 (wrapDigits p.2 p.2 qs))
      overflowPrefixes_nodup (evenWords_nodup k)
    intro p _ p' _ xs _ ys _ heq
    have houter := wrapDigits_injective p.1 p.1 p'.1 p'.1
      (wrapDigits p.2 p.2 xs) (wrapDigits p'.2 p'.2 ys) heq
    have hinner := wrapDigits_injective p.2 p.2 p'.2 p'.2 xs ys houter.2.2
    exact ⟨Prod.ext houter.1 hinner.1, hinner.2.2⟩

/-- The exact count includes all three small-width boundaries. -/
theorem length_noOverflowWords (L : Nat) :
    (noOverflowWords L).length =
      if L = 0 then 0 else if L = 1 then 4 else if L = 2 then 5
      else 45 * 10 ^ ((L - 3) / 2) := by
  match L with
  | 0 => rfl
  | 1 => rfl
  | 2 => rfl
  | 3 =>
    simpa only [noOverflowWords, List.length_map] using length_noOverflowPrefixes
  | k + 4 =>
    have h0 : k + 4 ≠ 0 := by omega
    have h1 : k + 4 ≠ 1 := by omega
    have h2 : k + 4 ≠ 2 := by omega
    have he : (k + 4 - 3) / 2 = (k + 1) / 2 := by omega
    simp only [noOverflowWords, length_flatMap_map, length_noOverflowPrefixes,
      length_evenWords, if_neg h0, if_neg h1, if_neg h2, he]

/-- The overflow count has five singleton profiles and five two-column
profiles; every larger width has fifty-five outer choices. -/
theorem length_overflowWords (L : Nat) :
    (overflowWords L).length =
      if L = 0 then 0 else if L = 1 then 5 else if L = 2 then 5
      else 55 * 10 ^ ((L - 3) / 2) := by
  match L with
  | 0 => rfl
  | 1 => rfl
  | 2 => rfl
  | 3 =>
    simpa only [overflowWords, List.length_map] using length_overflowPrefixes
  | k + 4 =>
    have h0 : k + 4 ≠ 0 := by omega
    have h1 : k + 4 ≠ 1 := by omega
    have h2 : k + 4 ≠ 2 := by omega
    have he : (k + 4 - 3) / 2 = (k + 1) / 2 := by omega
    simp only [overflowWords, length_flatMap_map, length_overflowPrefixes,
      length_evenWords, if_neg h0, if_neg h1, if_neg h2, he]

#print axioms noOverflowWords
#print axioms overflowWords
#print axioms mem_noOverflowWords_shape
#print axioms mem_overflowWords_shape
#print axioms noOverflowWords_nodup
#print axioms overflowWords_nodup
#print axioms length_noOverflowWords
#print axioms length_overflowWords

end OddPredecessorTargetCensus
