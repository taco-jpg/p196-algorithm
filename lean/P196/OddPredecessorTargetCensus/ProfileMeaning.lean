import P196.OddPredecessorTargetCensus.Carry
import P196.OddPredecessorTargetCensus.ProfileStructure
import P196.OddPredecessorTargetCensus.LanguageShape

/-!
# The exact meaning of the two finite coefficient languages

Agent #6: finite word membership is equivalent to admissibility, accepted
profile parity, and the actual terminal carry. Singleton and two-column
boundaries are kept explicit; larger widths use the first two coefficients.
-/

set_option autoImplicit false

namespace OddPredecessorTargetCensus

open DecimalDigits FoldedDecimal Agent101 CompleteFiberParity
open Agent105WordFiber9df76b Agent105DecoderScan9df76b

private theorem symmetric_wrap (qs : List Nat) (hrev : qs.reverse = qs)
    (hlen : 2 ≤ qs.length) :
    ∃ s xs, qs = wrapDigits s s xs ∧ xs.reverse = xs := by
  obtain ⟨a, b, xs, rfl⟩ := exists_wrapDigits qs hlen
  rw [reverse_wrapDigits] at hrev
  obtain ⟨hba, _, hxs⟩ := wrapDigits_injective _ _ _ _ _ _ hrev
  subst b
  exact ⟨a, xs, rfl, hxs⟩

private theorem wrap_profile_meaning (s : Nat) (xs : List Nat) :
    (Admissible (wrapDigits s s xs).length (digitFn (wrapDigits s s xs)) ∧
      oddProfile (half (wrapDigits s s xs)) (center (wrapDigits s s xs)) = true) ↔
    xs.reverse = xs ∧
      ((s ≤ 9 ∧ s % 2 = 1) ∨ (10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0)) ∧
      ∀ t ∈ xs, t ≤ 18 ∧ t % 2 = 0 := by
  constructor
  · rintro ⟨ha, ho⟩
    have hr := reverse_of_admissible (wrapDigits s s xs) ha
    rw [reverse_wrapDigits] at hr
    have hrev := (wrapDigits_injective _ _ _ _ _ _ hr).2.2
    exact ⟨hrev, (oddProfile_wrap_iff s xs hrev).mp ho⟩
  · rintro ⟨hrev, hs, he⟩
    exact ⟨admissible_wrap s xs hrev (by omega) he,
      (oddProfile_wrap_iff s xs hrev).mpr ⟨hs, he⟩⟩

private theorem allowed_outer_carries
    (q : Nat → Nat) (L : Nat) (ha : Admissible L q) (hL : 3 ≤ L)
    (hout : (q 0 ≤ 9 ∧ q 0 % 2 = 1) ∨
      (10 ≤ q 0 ∧ q 0 ≤ 18 ∧ q 0 % 2 = 0))
    (heven : q 1 % 2 = 0) :
    (carry q L = 0 ↔ q 0 ≤ 9 ∧ q 0 % 2 = 1 ∧ (q 0 ≤ 7 ∨ q 1 ≤ 8)) ∧
    (carry q L = 1 ↔
      (10 ≤ q 0 ∧ q 0 ≤ 18 ∧ q 0 % 2 = 0) ∨ (q 0 = 9 ∧ 10 ≤ q 1)) := by
  have hbit := carry_bounded q L ha.2.2.1 L (by omega)
  rcases hout with ⟨hs, ho⟩ | ⟨h10, h18, he⟩
  · have hc := odd_outer_carry_iff q L ha hL hs ho heven
    constructor <;> omega
  · have hc := OverflowNormalizationNine.outer_large_overflow q L ha h10
    constructor <;> omega

private theorem wrapped_carry_criteria (s : Nat) (xs : List Nat)
    (ha : Admissible (wrapDigits s s xs).length (digitFn (wrapDigits s s xs)))
    (hpos : 0 < xs.length)
    (hout : (s ≤ 9 ∧ s % 2 = 1) ∨ (10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0))
    (he : ∀ t ∈ xs, t ≤ 18 ∧ t % 2 = 0) :
    (carry (digitFn (wrapDigits s s xs)) (wrapDigits s s xs).length = 0 ↔
      s ≤ 9 ∧ s % 2 = 1 ∧ (s ≤ 7 ∨ digitFn xs 0 ≤ 8)) ∧
    (carry (digitFn (wrapDigits s s xs)) (wrapDigits s s xs).length = 1 ↔
      (10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0) ∨ (s = 9 ∧ 10 ≤ digitFn xs 0)) := by
  have ht : digitFn xs 0 % 2 = 0 := by
    rw [digitFn_getElem xs 0 hpos]
    exact (he _ (List.getElem_mem hpos)).2
  have hqone := digitFn_wrap_inner s s xs 0 hpos
  have hc := allowed_outer_carries (digitFn (wrapDigits s s xs))
    (wrapDigits s s xs).length ha (by rw [length_wrapDigits]; omega)
    (by simpa only [digitFn_wrap_zero] using hout)
    (by simpa only [hqone] using ht)
  simpa only [digitFn_wrap_zero, hqone] using hc

private theorem wrap_noOverflow_meaning (s : Nat) (xs : List Nat)
    (hpos : 0 < xs.length) :
    (Admissible (wrapDigits s s xs).length (digitFn (wrapDigits s s xs)) ∧
      oddProfile (half (wrapDigits s s xs)) (center (wrapDigits s s xs)) = true ∧
      carry (digitFn (wrapDigits s s xs)) (wrapDigits s s xs).length = 0) ↔
    xs.reverse = xs ∧ (∀ t ∈ xs, t ≤ 18 ∧ t % 2 = 0) ∧
      s ≤ 9 ∧ s % 2 = 1 ∧ (s ≤ 7 ∨ digitFn xs 0 ≤ 8) := by
  constructor
  · rintro ⟨ha, ho, hc⟩
    obtain ⟨hr, hout, he⟩ := (wrap_profile_meaning s xs).mp ⟨ha, ho⟩
    exact ⟨hr, he, ((wrapped_carry_criteria s xs ha hpos hout he).1).mp hc⟩
  · rintro ⟨hr, he, h9, hodd, hnext⟩
    have hout : (s ≤ 9 ∧ s % 2 = 1) ∨ (10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0) :=
      Or.inl ⟨h9, hodd⟩
    obtain ⟨ha, ho⟩ := (wrap_profile_meaning s xs).mpr ⟨hr, hout, he⟩
    exact ⟨ha, ho, ((wrapped_carry_criteria s xs ha hpos hout he).1).mpr
      ⟨h9, hodd, hnext⟩⟩

private theorem wrap_overflow_meaning (s : Nat) (xs : List Nat)
    (hpos : 0 < xs.length) :
    (Admissible (wrapDigits s s xs).length (digitFn (wrapDigits s s xs)) ∧
      oddProfile (half (wrapDigits s s xs)) (center (wrapDigits s s xs)) = true ∧
      carry (digitFn (wrapDigits s s xs)) (wrapDigits s s xs).length = 1) ↔
    xs.reverse = xs ∧ (∀ t ∈ xs, t ≤ 18 ∧ t % 2 = 0) ∧
      ((10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0) ∨ (s = 9 ∧ 10 ≤ digitFn xs 0)) := by
  constructor
  · rintro ⟨ha, ho, hc⟩
    obtain ⟨hr, hout, he⟩ := (wrap_profile_meaning s xs).mp ⟨ha, ho⟩
    exact ⟨hr, he, ((wrapped_carry_criteria s xs ha hpos hout he).2).mp hc⟩
  · rintro ⟨hr, he, hcase⟩
    have hout : (s ≤ 9 ∧ s % 2 = 1) ∨ (10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0) := by
      rcases hcase with hh | ⟨hs, _⟩
      · exact Or.inr hh
      · exact Or.inl (by omega)
    obtain ⟨ha, ho⟩ := (wrap_profile_meaning s xs).mpr ⟨hr, hout, he⟩
    exact ⟨ha, ho, ((wrapped_carry_criteria s xs ha hpos hout he).2).mpr hcase⟩

private theorem singleton_profile_meaning (s : Nat) :
    (Admissible 1 (digitFn [s]) ∧ oddProfile (half [s]) (center [s]) = true) ↔
      0 < s ∧ s ≤ 18 ∧ s % 2 = 0 := by
  have ho : oddProfile (half [s]) (center [s]) = true ↔
      0 < s ∧ s ≤ 18 ∧ s % 2 = 0 := by
    simp [half, center, oddProfile, centerCount]
  constructor
  · intro h
    exact ho.mp h.2
  · intro hs
    refine ⟨?_, ho.mpr hs⟩
    refine ⟨by decide, ?_, ?_, ?_, ?_⟩
    · simpa only [digitFn, List.getElem?_cons_zero, Option.getD_some] using hs.1
    · intro i hi
      have hz : i = 0 := by omega
      subst i
      simpa only [digitFn, List.getElem?_cons_zero, Option.getD_some] using hs.2.1
    · intro i hi
      have hz : i = 0 := by omega
      subst i
      rfl
    · intro i hi _
      have hz : i = 0 := by omega
      subst i
      simpa only [digitFn, List.getElem?_cons_zero, Option.getD_some] using hs.2.2

private theorem singleton_noOverflow_meaning (s : Nat) :
    (Admissible 1 (digitFn [s]) ∧ oddProfile (half [s]) (center [s]) = true ∧
      carry (digitFn [s]) 1 = 0) ↔ s ∈ [2, 4, 6, 8] := by
  rw [← and_assoc, singleton_profile_meaning]
  change (0 < s ∧ s ≤ 18 ∧ s % 2 = 0) ∧ s / 10 = 0 ↔ _
  simp only [List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false]
  omega

private theorem singleton_overflow_meaning (s : Nat) :
    (Admissible 1 (digitFn [s]) ∧ oddProfile (half [s]) (center [s]) = true ∧
      carry (digitFn [s]) 1 = 1) ↔ s ∈ [10, 12, 14, 16, 18] := by
  rw [← and_assoc, singleton_profile_meaning]
  change (0 < s ∧ s ≤ 18 ∧ s % 2 = 0) ∧ s / 10 = 1 ↔ _
  simp only [List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false]
  omega

private theorem pair_profile_meaning (s : Nat) :
    (Admissible 2 (digitFn [s, s]) ∧
      oddProfile (half [s, s]) (center [s, s]) = true) ↔
      (s ≤ 9 ∧ s % 2 = 1) ∨ (10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0) := by
  simpa [wrapDigits] using wrap_profile_meaning s []

private theorem pair_noOverflow_meaning (s : Nat) :
    (Admissible 2 (digitFn [s, s]) ∧
      oddProfile (half [s, s]) (center [s, s]) = true ∧
      carry (digitFn [s, s]) 2 = 0) ↔ s ∈ [1, 3, 5, 7, 9] := by
  rw [← and_assoc, pair_profile_meaning]
  change (((s ≤ 9 ∧ s % 2 = 1) ∨ (10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0)) ∧
    (s + s / 10) / 10 = 0) ↔ _
  simp only [List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false]
  omega

private theorem pair_overflow_meaning (s : Nat) :
    (Admissible 2 (digitFn [s, s]) ∧
      oddProfile (half [s, s]) (center [s, s]) = true ∧
      carry (digitFn [s, s]) 2 = 1) ↔ s ∈ [10, 12, 14, 16, 18] := by
  rw [← and_assoc, pair_profile_meaning]
  change (((s ≤ 9 ∧ s % 2 = 1) ∨ (10 ≤ s ∧ s ≤ 18 ∧ s % 2 = 0)) ∧
    (s + s / 10) / 10 = 1) ↔ _
  simp only [List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false]
  omega

/-- The first finite language consists exactly of admissible accepted
coefficient words whose actual terminal carry is zero. -/
theorem mem_noOverflowWords (L : Nat) (qs : List Nat) :
    qs ∈ noOverflowWords L ↔ qs.length = L ∧
      Admissible L (digitFn qs) ∧ oddProfile (half qs) (center qs) = true ∧
      carry (digitFn qs) L = 0 := by
  by_cases hlarge : 3 ≤ L
  · rw [mem_noOverflowWords_large L qs hlarge]
    constructor
    · rintro ⟨s, xs, rfl, hxs, hp⟩
      obtain ⟨hlen, hr, he⟩ := (mem_evenWords (L - 2) xs).mp hxs
      have hpos : 0 < xs.length := by omega
      have hlen' : (wrapDigits s s xs).length = L := by
        rw [length_wrapDigits]
        omega
      have hh := (mem_noOverflowPrefixes s (digitFn xs 0)).mp hp
      have hm := (wrap_noOverflow_meaning s xs hpos).mpr
        ⟨hr, he, hh.1, hh.2.1, hh.2.2.2.2⟩
      exact ⟨hlen', by simpa only [hlen'] using hm⟩
    · rintro ⟨hlen, ha, ho, hc⟩
      have ha' : Admissible qs.length (digitFn qs) := by
        simpa only [hlen] using ha
      obtain ⟨s, xs, rfl, _⟩ := symmetric_wrap qs (reverse_of_admissible qs ha') (by omega)
      have hxslen : xs.length = L - 2 := by
        rw [length_wrapDigits] at hlen
        omega
      have hpos : 0 < xs.length := by omega
      have hm := (wrap_noOverflow_meaning s xs hpos).mp
        ⟨ha', ho, by simpa only [hlen] using hc⟩
      have ht : digitFn xs 0 ≤ 18 ∧ digitFn xs 0 % 2 = 0 := by
        rw [digitFn_getElem xs 0 hpos]
        exact hm.2.1 _ (List.getElem_mem hpos)
      refine ⟨s, xs, rfl, (mem_evenWords (L - 2) xs).mpr ⟨hxslen, hm.1, hm.2.1⟩, ?_⟩
      exact (mem_noOverflowPrefixes s (digitFn xs 0)).mpr
        ⟨hm.2.2.1, hm.2.2.2.1, ht.1, ht.2, hm.2.2.2.2⟩
  · match L with
    | 0 => simp [noOverflowWords, Admissible]
    | 1 =>
      rw [mem_noOverflowWords_shape]
      constructor
      · rintro ⟨s, hs, rfl⟩
        exact ⟨rfl, (singleton_noOverflow_meaning s).mpr hs⟩
      · rintro ⟨hlen, hm⟩
        obtain ⟨s, rfl⟩ := List.length_eq_one_iff.mp hlen
        exact ⟨s, (singleton_noOverflow_meaning s).mp hm, rfl⟩
    | 2 =>
      rw [mem_noOverflowWords_shape]
      constructor
      · rintro ⟨s, hs, rfl⟩
        exact ⟨rfl, (pair_noOverflow_meaning s).mpr hs⟩
      · rintro ⟨hlen, ha, ho, hc⟩
        have ha' : Admissible qs.length (digitFn qs) := by simpa only [hlen] using ha
        obtain ⟨s, xs, rfl, _⟩ := symmetric_wrap qs (reverse_of_admissible qs ha') (by omega)
        have hx : xs = [] := List.eq_nil_of_length_eq_zero (by
          rw [length_wrapDigits] at hlen
          omega)
        subst xs
        exact ⟨s, (pair_noOverflow_meaning s).mp ⟨ha, ho, hc⟩, rfl⟩
    | n + 3 => omega

/-- The second finite language consists exactly of admissible accepted
coefficient words whose actual terminal carry is one. -/
theorem mem_overflowWords (L : Nat) (qs : List Nat) :
    qs ∈ overflowWords L ↔ qs.length = L ∧
      Admissible L (digitFn qs) ∧ oddProfile (half qs) (center qs) = true ∧
      carry (digitFn qs) L = 1 := by
  by_cases hlarge : 3 ≤ L
  · rw [mem_overflowWords_large L qs hlarge]
    constructor
    · rintro ⟨s, xs, rfl, hxs, hp⟩
      obtain ⟨hlen, hr, he⟩ := (mem_evenWords (L - 2) xs).mp hxs
      have hpos : 0 < xs.length := by omega
      have hlen' : (wrapDigits s s xs).length = L := by
        rw [length_wrapDigits]
        omega
      have hh := (mem_overflowPrefixes s (digitFn xs 0)).mp hp
      have hm := (wrap_overflow_meaning s xs hpos).mpr ⟨hr, he, hh.2.2⟩
      exact ⟨hlen', by simpa only [hlen'] using hm⟩
    · rintro ⟨hlen, ha, ho, hc⟩
      have ha' : Admissible qs.length (digitFn qs) := by
        simpa only [hlen] using ha
      obtain ⟨s, xs, rfl, _⟩ := symmetric_wrap qs (reverse_of_admissible qs ha') (by omega)
      have hxslen : xs.length = L - 2 := by
        rw [length_wrapDigits] at hlen
        omega
      have hpos : 0 < xs.length := by omega
      have hm := (wrap_overflow_meaning s xs hpos).mp
        ⟨ha', ho, by simpa only [hlen] using hc⟩
      have ht : digitFn xs 0 ≤ 18 ∧ digitFn xs 0 % 2 = 0 := by
        rw [digitFn_getElem xs 0 hpos]
        exact hm.2.1 _ (List.getElem_mem hpos)
      refine ⟨s, xs, rfl, (mem_evenWords (L - 2) xs).mpr ⟨hxslen, hm.1, hm.2.1⟩, ?_⟩
      exact (mem_overflowPrefixes s (digitFn xs 0)).mpr ⟨ht.1, ht.2, hm.2.2⟩
  · match L with
    | 0 => simp [overflowWords, Admissible]
    | 1 =>
      rw [mem_overflowWords_shape]
      constructor
      · rintro ⟨s, hs, rfl⟩
        exact ⟨rfl, (singleton_overflow_meaning s).mpr hs⟩
      · rintro ⟨hlen, hm⟩
        obtain ⟨s, rfl⟩ := List.length_eq_one_iff.mp hlen
        exact ⟨s, (singleton_overflow_meaning s).mp hm, rfl⟩
    | 2 =>
      rw [mem_overflowWords_shape]
      constructor
      · rintro ⟨s, hs, rfl⟩
        exact ⟨rfl, (pair_overflow_meaning s).mpr hs⟩
      · rintro ⟨hlen, ha, ho, hc⟩
        have ha' : Admissible qs.length (digitFn qs) := by simpa only [hlen] using ha
        obtain ⟨s, xs, rfl, _⟩ := symmetric_wrap qs (reverse_of_admissible qs ha') (by omega)
        have hx : xs = [] := List.eq_nil_of_length_eq_zero (by
          rw [length_wrapDigits] at hlen
          omega)
        subst xs
        exact ⟨s, (pair_overflow_meaning s).mp ⟨ha, ho, hc⟩, rfl⟩
    | n + 3 => omega

#print axioms mem_noOverflowWords
#print axioms mem_overflowWords

end OddPredecessorTargetCensus
