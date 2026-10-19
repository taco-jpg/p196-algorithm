import P196.EightCarryMaximalWidth.BaseCertificate
import P196.EightCarryMaximalWidth.ExtensionCertificate

/-!
Agent #10: actual eight-observation histories exclude the first seven
coefficients of either nonzero short core. Completeness of each finite stage
is imported from the kernel certificates. Actual survival is instantiated
separately at prefix lengths three through seven, so no abstract truncation
or unproved full-word lifting assertion is used.
-/

namespace EightCarryMaximalWidth

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual SevenColumnProjection PrefixHistory Candidates

theorem prefix_succ (q : Nat → Nat) (k : Nat) :
    wordPrefix q (k + 1) = wordPrefix q k ++ [q k] := by
  simp only [wordPrefix_eq_range_map, List.range_succ, List.map_append,
    List.map_cons, List.map_nil]

/-- Actual eight-observation histories with the displayed first five
coefficient differences belong to the complete five-column candidate cover. -/
theorem eight_carries_force_short_core_five_prefix
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (h5L : 5 ≤ L)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i)
    (h0 : q 0 = r 0) (h1 : q 1 = r 1) (h2 : q 2 = r 2 + 1)
    (h3 : r 3 = q 3 + 3) (h4 : q 4 = r 4 + 5) :
    (wordPrefix q 5, wordPrefix r 5) ∈ quintuples := by
  have hqb : ∀ i, i < 5 → q i ≤ 18 := by
    intro i hi
    exact hq.2.2.1 i (by omega)
  have hrb : ∀ i, i < 5 → r i ≤ 18 := by
    intro i hi
    exact hr.2.2.1 i (by omega)
  have hs : ∀ k, 0 < k → k ≤ 5 →
      accepted (wordPrefix q k, wordPrefix r k) = true := by
    intro k hk0 hk
    exact actual_history_survives_encoded q r L k 8 hq hr hk0 (by omega) hc
  have hm3 : (wordPrefix q 3, wordPrefix r 3) ∈ triples := by
    have hp : 1 ≤ q 0 := by have := hq.2.1; omega
    have hinit := startsAt_mem (q 0) (q 1) (r 2)
      (by have := hqb 1 (by decide); omega)
      (by have := hqb 2 (by decide); omega)
    have hsurv := hs 3 (by decide) (by decide)
    change accepted ([q 0, q 1, q 2], [r 0, r 1, r 2]) = true at hsurv
    rw [← h0, ← h1, h2] at hsurv
    have hm := covered_mem _ _ (startsAt_cover (q 0) hp (hqb 0 (by decide)))
      _ hinit hsurv
    have ht := triples_mem_of_mem_at (q 0) hp (hqb 0 (by decide)) _ hm
    change ([q 0, q 1, q 2], [r 0, r 1, r 2]) ∈ triples
    simpa only [← h0, ← h1, h2] using ht
  have hm4 : (wordPrefix q 4, wordPrefix r 4) ∈ quadruples := by
    have he := extensions_mem 0 3 16 triples _ _ hm3 (q 3)
      (by have := hrb 3 (by decide); omega)
    have he' : (wordPrefix q 4, wordPrefix r 4) ∈
        extensions 0 3 16 triples := by
      simpa only [prefix_succ, h3, Nat.add_zero] using he
    exact covered_mem _ _ cover_four _ he' (hs 4 (by decide) (by decide))
  have hm5 : (wordPrefix q 5, wordPrefix r 5) ∈ quintuples := by
    have he := extensions_mem 5 0 14 quadruples _ _ hm4 (r 4)
      (by have := hqb 4 (by decide); omega)
    have he' : (wordPrefix q 5, wordPrefix r 5) ∈
        extensions 5 0 14 quadruples := by
      simpa only [prefix_succ, h4, Nat.add_zero] using he
    exact covered_mem _ _ cover_five _ he' (hs 5 (by decide) (by decide))
  exact hm5

/-- The two possible positive short cores cannot start an actual synchronized
history of eight complete carry observations. Only seven initial coefficients
are used, and the reflected prefixes are allowed to overlap. -/
theorem eight_carries_exclude_positive_short_core_prefix
    (q r : Nat → Nat) (L : Nat)
    (hq : Admissible L q) (hr : Admissible L r) (h7 : 7 ≤ L)
    (hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
      carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i)
    (h0 : q 0 = r 0) (h1 : q 1 = r 1) (h2 : q 2 = r 2 + 1)
    (h3 : r 3 = q 3 + 3) (h4 : q 4 = r 4 + 5)
    (h5 : r 5 = q 5 + 6) (h6 : q 6 = r 6 + 5 ∨ q 6 = r 6 + 6) :
    False := by
  have hqb : ∀ i, i < 7 → q i ≤ 18 := by
    intro i hi
    exact hq.2.2.1 i (by omega)
  have hrb : ∀ i, i < 7 → r i ≤ 18 := by
    intro i hi
    exact hr.2.2.1 i (by omega)
  have hs : ∀ k, 0 < k → k ≤ 7 →
      accepted (wordPrefix q k, wordPrefix r k) = true := by
    intro k hk0 hk
    exact actual_history_survives_encoded q r L k 8 hq hr hk0 (by omega) hc
  have hm5 := eight_carries_force_short_core_five_prefix q r L hq hr
    (by omega) hc h0 h1 h2 h3 h4
  have hm6 : (wordPrefix q 6, wordPrefix r 6) ∈ sextuples := by
    have he := extensions_mem 0 6 13 quintuples _ _ hm5 (q 5)
      (by have := hrb 5 (by decide); omega)
    have he' : (wordPrefix q 6, wordPrefix r 6) ∈
        extensions 0 6 13 quintuples := by
      simpa only [prefix_succ, h5, Nat.add_zero] using he
    exact covered_mem _ _ cover_six _ he' (hs 6 (by decide) (by decide))
  rcases h6 with h6 | h6
  · have he := extensions_mem 5 0 14 sextuples _ _ hm6 (r 6)
      (by have := hqb 6 (by decide); omega)
    have he' : (wordPrefix q 7, wordPrefix r 7) ∈
        extensions 5 0 14 sextuples := by
      simpa only [prefix_succ, h6, Nat.add_zero] using he
    have hm := covered_mem _ _ cover_seven_five _ he'
      (hs 7 (by decide) (by decide))
    exact List.not_mem_nil hm
  · have he := extensions_mem 6 0 13 sextuples _ _ hm6 (r 6)
      (by have := hqb 6 (by decide); omega)
    have he' : (wordPrefix q 7, wordPrefix r 7) ∈
        extensions 6 0 13 sextuples := by
      simpa only [prefix_succ, h6, Nat.add_zero] using he
    have hm := covered_mem _ _ cover_seven_six _ he'
      (hs 7 (by decide) (by decide))
    exact List.not_mem_nil hm

#print axioms eight_carries_force_short_core_five_prefix
#print axioms eight_carries_exclude_positive_short_core_prefix

end EightCarryMaximalWidth
