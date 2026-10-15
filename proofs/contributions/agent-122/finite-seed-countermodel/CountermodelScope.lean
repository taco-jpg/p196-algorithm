import CountermapGrowth

/-!
Agent #122. Quantifiers and the exact limit of the countermodel.
The original map does NOT preserve the true upper width clock. This missing
property is exhibited symbolically at time four, not hidden by the word
"countermodel". No statement here establishes a property of the orbit of 196.
-/
namespace Agent122.Countermodel

open Lychrel196 DecimalDigits DecimalQuantitativeMass

theorem no_infinite_safe_seed (ell : Nat → Nat) :
    ¬ ∃ n, 0 < n ∧ ∀ t, ¬ Palindrome (run ell n t) := by
  rintro ⟨n,hn,hs⟩
  obtain ⟨t,ht,hp⟩ := every_positive_seed_terminates ell n hn
  exact hs t hp

/-- The map is fixed before the safe-prefix horizon is chosen. -/
theorem fixed_map_arbitrary_safe_prefixes (R : Nat) :
    ∃ n, 0 < n ∧ ∀ t, t ≤ R → ¬ Palindrome (run (fun a => a) n t) := by
  obtain ⟨n,tau,hn,hR,hfirst⟩ := fixed_map_unbounded_first_hits R
  refine ⟨n,hn,?_⟩
  intro t ht
  exact hfirst.2 t (by omega)

/-- The quantifier interchange fails even on the actual decimal state space
and with the actual palindrome predicate. The update is explicitly F, not T. -/
theorem finite_prefix_extraction_fails :
    ¬ ((∀ R, ∃ n, 0 < n ∧ ∀ t, t ≤ R →
        ¬ Palindrome (run (fun a => a) n t)) →
      ∃ n, 0 < n ∧ ∀ t, ¬ Palindrome (run (fun a => a) n t)) := by
  intro h
  exact no_infinite_safe_seed _ (h fixed_map_arbitrary_safe_prefixes)

/-- Restatement of the repository's already-proved true-orbit upper clock. -/
theorem actual_upper_width_clock (n t : Nat) (hn : 0 < n) :
    2*decimalLength (orbit n t) ≤ 2*decimalLength n+t+3 := by
  obtain ⟨d,L,hc⟩ := canonical_exists n hn
  obtain ⟨e,W,he,_,hu⟩ := DecimalWidthGrowth.numeric_width_bounds n d L t hc
  rw [decimalLength_of_canonical n d L hc,
    decimalLength_of_canonical (orbit n t) e W he]
  exact hu

/-- Every chain a >= 4 of the fixed example breaks that upper clock at t=4. -/
theorem countermap_violates_upper_clock (a : Nat) (ha : 4 ≤ a) :
    2*decimalLength (run (fun x => x) (node a 0) 4) >
      2*decimalLength (node a 0)+4+3 := by
  rw [run_node (fun x => x) a 0 4 (by omega) (by change 0+4 ≤ a; omega),
    node_width a (0+4) (by omega), node_width a 0 (by omega)]
  omega

/-- This discrepancy alone already separates F's trajectory from actual RAA. -/
theorem countermap_fourth_iterate_not_actual (a : Nat) (ha : 4 ≤ a) :
    run (fun x => x) (node a 0) 4 ≠ orbit (node a 0) 4 := by
  intro heq
  have hf := countermap_violates_upper_clock a ha
  have ht := actual_upper_width_clock (node a 0) 4 (node_positive _ _)
  rw [heq] at hf
  omega

/-- Completed clauses of the original written countermodel, with an explicit
fixed unbounded-delay instance. Density and pair-word factoring are NOT clauses
of this theorem; neither is the true upper width clock. -/
theorem quantitative_terminating_countermodel :
    ∃ ell : Nat → Nat,
      (∀ n, B n → F ell n = step n) ∧
      (∀ n, Palindrome (F ell n) ↔ B n) ∧
      (∀ n, 0 < n → n < F ell n ∧ F ell n < 11*n) ∧
      (∀ n, 0 < n → decimalLength n ≤ decimalLength (F ell n) ∧
        decimalLength (F ell n) ≤ decimalLength n+1) ∧
      (∀ n t, 0 < n → decimalLength n+t/5 ≤ decimalLength (run ell n t)) ∧
      (∀ n, 0 < n → Terminates ell n) ∧
      (∀ R, ∃ n tau, 0 < n ∧ R < tau ∧ FirstHit ell n tau) := by
  refine ⟨fun a => a, F_of_B _, F_exact_predecessors _, F_numeric_growth _,
    F_width_bounds _, run_width_five_floor _, every_positive_seed_terminates _,
    fixed_map_unbounded_first_hits⟩

end Agent122.Countermodel
