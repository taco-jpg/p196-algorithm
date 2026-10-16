import CoefficientContraction
import Compat

/-!
Exact original-semantics endpoints. All words are finite List Nat values.
The correspondence theorem is unconditional except for positivity and the
coefficient bound. The Lychrel transfer theorem additionally assumes infinite
normalized-word safety and does not provide a witness of that assumption.
-/
namespace Agent112.Eventual
open Agent109

/-- Original Agent8 symbolic trajectory and original Lychrel196 integer orbit. -/
theorem original_eventual_realization (w : Word) (hb : Bounded w) (hp : 0 < evalL w) :
    ∃ t n, 1 ≤ t ∧ t ≤ 2 * 10 ^ w.length ∧ 0 < n ∧
      ∀ k, pairWord (Lychrel196.orbit n k) = Agent8.orbit w (t + k) := by
  obtain ⟨t, n, ht, hbound, hn, he⟩ := eventual_realization w hb hp
  refine ⟨t, n, ht, hbound, hn, ?_⟩
  intro k
  rw [Compat.orbit_eq, Compat.orbit_word_eq]
  exact he k

/-- The finite symbolic-to-ordinary-integer bridge has no separate canonical
realizability requirement, even if the initial word is asymmetric or zero-headed. -/
theorem original_safe_symbolic_positive_seed (w : Word) (hb : Bounded w) (hp : 0 < evalL w)
    (hs : ∀ k, (Agent8.normalize (Agent8.orbit w k) 0).reverse ≠
      Agent8.normalize (Agent8.orbit w k) 0) :
    ∃ m, 0 < m ∧ Lychrel196.IsLychrel m := by
  have hs' : ∀ k, (normalize (orbitWord w k) 0).reverse ≠ normalize (orbitWord w k) 0 := by
    intro k
    simpa only [Compat.orbit_word_eq, Compat.normalize_eq] using hs k
  obtain ⟨m, hm, hsafety⟩ := safe_symbolic_positive_seed w hb hp hs'
  refine ⟨m, hm, ?_⟩
  intro k
  rw [Compat.palindrome_eq, Compat.orbit_eq]
  exact hsafety k

/-- Every positive finite natural-coefficient word eventually represents an
ordinary decimal orbit. There is no initial coefficient bound or canonicality
premise. The transient bound above is retained for the bounded special case. -/
theorem original_arbitrary_eventual_realization (w : Word) (hp : 0 < evalL w) :
    ∃ t n, 1 ≤ t ∧ 0 < n ∧
      ∀ k, pairWord (Lychrel196.orbit n k) = Agent8.orbit w (t + k) := by
  obtain ⟨t, n, ht, hn, he⟩ := arbitrary_eventual_realization w hp
  refine ⟨t, n, ht, hn, ?_⟩
  intro k
  rw [Compat.orbit_eq, Compat.orbit_word_eq]
  exact he k

/-- Conditional transfer of infinite safety for arbitrary finite coefficients,
not a construction of an infinitely safe symbolic word. -/
theorem original_arbitrary_safe_symbolic_positive_seed (w : Word) (hp : 0 < evalL w)
    (hs : ∀ k, (Agent8.normalize (Agent8.orbit w k) 0).reverse ≠
      Agent8.normalize (Agent8.orbit w k) 0) :
    ∃ m, 0 < m ∧ Lychrel196.IsLychrel m := by
  have hs' : ∀ k, (normalize (orbitWord w k) 0).reverse ≠ normalize (orbitWord w k) 0 := by
    intro k
    simpa only [Compat.orbit_word_eq, Compat.normalize_eq] using hs k
  obtain ⟨m, hm, hsafety⟩ := arbitrary_safe_symbolic_positive_seed w hp hs'
  refine ⟨m, hm, ?_⟩
  intro k
  rw [Compat.palindrome_eq, Compat.orbit_eq]
  exact hsafety k

end Agent112.Eventual
#print axioms Agent112.Eventual.original_eventual_realization
#print axioms Agent112.Eventual.original_safe_symbolic_positive_seed
#print axioms Agent112.Eventual.original_arbitrary_eventual_realization
#print axioms Agent112.Eventual.original_arbitrary_safe_symbolic_positive_seed
