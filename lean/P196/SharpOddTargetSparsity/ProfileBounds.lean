import P196.SharpOddTargetSparsity.Tables
import P196.OddPredecessorTargetCensus.Profiles

/-!
# Positional cutoff bounds for the odd target coefficient families

Agent #6: the first one or two coefficients of a symmetric word give
lower bounds for its value. After restricting the admissible outer
prefixes, the existing finite-product count supplies every inner choice.
The argument applies to raw coefficients through eighteen and does not
require a decimal normalization or a carry computation.
-/

set_option autoImplicit false

namespace SharpOddTargetSparsity

open Agent101 OddPredecessorTargetCensus P196.Agent9.Ensemble

private theorem top_one_le_value (q : Nat → Nat) (L : Nat) (hL : 1 ≤ L) :
    q (L - 1) * 10 ^ (L - 1) ≤ DecimalDigits.value q L := by
  obtain ⟨k, rfl⟩ : ∃ k, L = k + 1 := ⟨L - 1, by omega⟩
  simp only [Nat.add_sub_cancel, DecimalDigits.value]
  omega

private theorem top_two_le_value (q : Nat → Nat) (L : Nat) (hL : 2 ≤ L) :
    (10 * q (L - 1) + q (L - 2)) * 10 ^ (L - 2) ≤
      DecimalDigits.value q L := by
  obtain ⟨k, rfl⟩ : ∃ k, L = k + 2 := ⟨L - 2, by omega⟩
  have h1 : k + 2 - 1 = k + 1 := by omega
  simp only [h1, Nat.add_sub_cancel, DecimalDigits.value, Nat.pow_succ,
    Nat.add_mul, Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
  omega

private theorem first_le_natValue (qs : List Nat) (hs : qs.reverse = qs)
    (hL : 1 ≤ qs.length) :
    digitFn qs 0 * 10 ^ (qs.length - 1) ≤ natValue qs := by
  have hs0 := digitFn_symmetric_of_reverse qs hs 0 (by omega)
  simp only [Nat.sub_zero] at hs0
  simpa only [← hs0, natValue] using
    top_one_le_value (digitFn qs) qs.length hL

private theorem first_two_le_natValue (qs : List Nat) (hs : qs.reverse = qs)
    (hL : 2 ≤ qs.length) :
    (10 * digitFn qs 0 + digitFn qs 1) * 10 ^ (qs.length - 2) ≤
      natValue qs := by
  have hs0 := digitFn_symmetric_of_reverse qs hs 0 (by omega)
  have hs1 := digitFn_symmetric_of_reverse qs hs 1 (by omega)
  have hi : qs.length - 1 - 1 = qs.length - 2 := by omega
  simp only [Nat.sub_zero] at hs0
  rw [hi] at hs1
  simpa only [← hs0, ← hs1, natValue] using
    top_two_le_value (digitFn qs) qs.length hL

private theorem count_doubleWrapped (ps : List (Nat × Nat))
    (inner : List (List Nat)) (f : Nat → Nat → Bool) :
    (ps.flatMap fun p => inner.map
      (fun qs => wrapDigits p.1 p.1 (wrapDigits p.2 p.2 qs))).countP
        (fun qs => f (digitFn qs 0) (digitFn qs 1)) =
      ps.countP (fun p => f p.1 p.2) * inner.length := by
  have hf :
      (ps.flatMap fun p => inner.map
        (fun qs => wrapDigits p.1 p.1 (wrapDigits p.2 p.2 qs))).filter
          (fun qs => f (digitFn qs 0) (digitFn qs 1)) =
        (ps.filter fun p => f p.1 p.2).flatMap fun p => inner.map
          (fun qs => wrapDigits p.1 p.1 (wrapDigits p.2 p.2 qs)) := by
    induction ps with
    | nil => rfl
    | cons p ps ih =>
      simp only [List.flatMap_cons, List.filter_append, ih, List.filter_map]
      cases h : f p.1 p.2 <;>
        simp [Function.comp_def, digitFn, wrapDigits, h]
      rw [List.filter_eq_self.mpr (by intro qs hqs; rfl)]
  rw [List.countP_eq_length_filter, hf, length_flatMap_map,
    ← List.countP_eq_length_filter]

private theorem doubleWrapped_data (p : Nat × Nat) (k : Nat)
    (inner : List Nat) (hi : inner ∈ evenWords k) :
    let qs := wrapDigits p.1 p.1 (wrapDigits p.2 p.2 inner)
    qs.length = k + 4 ∧ qs.reverse = qs ∧
      digitFn qs 0 = p.1 ∧ digitFn qs 1 = p.2 := by
  obtain ⟨hlen, hrev, _⟩ := (mem_evenWords k inner).mp hi
  refine ⟨?_, ?_, ?_, ?_⟩
  · simp only [length_wrapDigits, hlen]
  · simp only [reverse_wrapDigits, hrev]
  · simp [digitFn, wrapDigits]
  · simp [digitFn, wrapDigits]

/-- The first two coefficients restrict every no-overflow value below
a two-digit cutoff to at most the indicated number of outer blocks. -/
theorem count_noOverflow_lt (L N a : Nat) (hL : 4 ≤ L)
    (ha : 10 ≤ a) (ha' : a ≤ 99)
    (hN : N ≤ (a + 1) * 10 ^ (L - 2)) :
    (noOverflowWords L).countP (fun qs => decide (natValue qs < N)) ≤
      lowBlockCount a * 10 ^ ((L - 3) / 2) := by
  obtain ⟨k, rfl⟩ : ∃ k, L = k + 4 := ⟨L - 4, by omega⟩
  have he : (k + 4 - 3) / 2 = (k + 1) / 2 := by omega
  change (noOverflowPrefixes.flatMap fun p => (evenWords k).map
    (fun qs => wrapDigits p.1 p.1 (wrapDigits p.2 p.2 qs))).countP
      (fun qs => decide (natValue qs < N)) ≤ _
  calc
    _ ≤ (noOverflowPrefixes.flatMap fun p => (evenWords k).map
        (fun qs => wrapDigits p.1 p.1 (wrapDigits p.2 p.2 qs))).countP
          (fun qs => decide (10 * digitFn qs 0 + digitFn qs 1 ≤ a)) := by
      apply List.countP_mono_left
      intro qs hqs hv
      obtain ⟨p, _, hp⟩ := List.mem_flatMap.mp hqs
      obtain ⟨inner, hi, rfl⟩ := List.mem_map.mp hp
      obtain ⟨hlen, hsym, h0, h1⟩ := doubleWrapped_data p k inner hi
      have hval := first_two_le_natValue
        (wrapDigits p.1 p.1 (wrapDigits p.2 p.2 inner)) hsym (by omega)
      simp only [decide_eq_true_eq] at hv ⊢
      rw [hlen] at hval
      have hprod := Nat.lt_of_le_of_lt hval (Nat.lt_of_lt_of_le hv hN)
      have hh := Nat.lt_of_mul_lt_mul_right hprod
      omega
    _ = noOverflowPrefixes.countP (fun p => decide (10 * p.1 + p.2 ≤ a)) *
        (evenWords k).length :=
      count_doubleWrapped noOverflowPrefixes (evenWords k)
        (fun s t => decide (10 * s + t ≤ a))
    _ = lowBlockCount a * 10 ^ ((k + 4 - 3) / 2) := by
      rw [count_noOverflowPrefixes a ha ha', length_evenWords, he]

/-- At width at least three, the leading coefficient restricts every
overflow value below a two-digit cutoff to the listed high blocks. -/
theorem count_overflow_lt (L N a : Nat) (hL : 3 ≤ L)
    (ha : 10 ≤ a) (ha' : a ≤ 99)
    (hN : N ≤ (a + 1) * 10 ^ (L - 1)) :
    (overflowWords L).countP (fun qs => decide (natValue qs < N)) ≤
      highBlockCount a * 10 ^ ((L - 3) / 2) := by
  by_cases h3 : L = 3
  · subst L
    simp only [overflowWords, List.countP_map, Function.comp_def]
    calc
      _ ≤ overflowPrefixes.countP (fun p => decide (p.1 ≤ a)) := by
        apply List.countP_mono_left
        intro p _ hv
        have hsym : (wrapDigits p.1 p.1 [p.2]).reverse =
            wrapDigits p.1 p.1 [p.2] := by
          simp only [reverse_wrapDigits]
          rfl
        have hval := first_le_natValue (wrapDigits p.1 p.1 [p.2]) hsym
          (by simp [length_wrapDigits])
        simp only [length_wrapDigits, List.length_singleton] at hval
        have h0 : digitFn (wrapDigits p.1 p.1 [p.2]) 0 = p.1 := by
          simp [digitFn, wrapDigits]
        rw [h0] at hval
        simp only [decide_eq_true_eq] at hv ⊢
        have hprod := Nat.lt_of_le_of_lt hval (Nat.lt_of_lt_of_le hv hN)
        have hh := Nat.lt_of_mul_lt_mul_right hprod
        omega
      _ = highBlockCount a * 10 ^ ((3 - 3) / 2) := by
        simp only [count_overflowPrefixes a ha ha', Nat.sub_self,
          Nat.zero_div, Nat.pow_zero, Nat.mul_one]
  · obtain ⟨k, rfl⟩ : ∃ k, L = k + 4 := ⟨L - 4, by omega⟩
    have he : (k + 4 - 3) / 2 = (k + 1) / 2 := by omega
    change (overflowPrefixes.flatMap fun p => (evenWords k).map
      (fun qs => wrapDigits p.1 p.1 (wrapDigits p.2 p.2 qs))).countP
        (fun qs => decide (natValue qs < N)) ≤ _
    calc
      _ ≤ (overflowPrefixes.flatMap fun p => (evenWords k).map
          (fun qs => wrapDigits p.1 p.1 (wrapDigits p.2 p.2 qs))).countP
            (fun qs => decide (digitFn qs 0 ≤ a)) := by
        apply List.countP_mono_left
        intro qs hqs hv
        obtain ⟨p, _, hp⟩ := List.mem_flatMap.mp hqs
        obtain ⟨inner, hi, rfl⟩ := List.mem_map.mp hp
        obtain ⟨hlen, hsym, h0, _⟩ := doubleWrapped_data p k inner hi
        have hval := first_le_natValue
          (wrapDigits p.1 p.1 (wrapDigits p.2 p.2 inner)) hsym (by omega)
        simp only [decide_eq_true_eq] at hv ⊢
        rw [hlen] at hval
        have hprod := Nat.lt_of_le_of_lt hval (Nat.lt_of_lt_of_le hv hN)
        have hh := Nat.lt_of_mul_lt_mul_right hprod
        omega
      _ = overflowPrefixes.countP (fun p => decide (p.1 ≤ a)) *
          (evenWords k).length :=
        count_doubleWrapped overflowPrefixes (evenWords k)
          (fun s _ => decide (s ≤ a))
      _ = highBlockCount a * 10 ^ ((k + 4 - 3) / 2) := by
        rw [count_overflowPrefixes a ha ha', length_evenWords, he]

end SharpOddTargetSparsity

#print axioms SharpOddTargetSparsity.count_noOverflow_lt
#print axioms SharpOddTargetSparsity.count_overflow_lt
