import EventualRealization

namespace Agent112.Eventual
open Agent109
open Agent112.Admissibility

/-- A nonzero final carry removes the trailing-zero obstruction to canonical
integer realization. -/
theorem overflow_canonical (w : Word) (hb : Bounded w) (hc : (norm w 0).2 = 1) :
    Canon (normalize w 0) := by
  apply (canon_iff _).mpr
  refine ⟨normalize_digits w hb, ?_⟩
  intro x hx
  rw [normalize_eq_norm, hc] at hx
  simp [carryWord] at hx
  omega

theorem overflow_realized (w : Word) (hb : Bounded w) (hp : 0 < evalL w)
    (hc : (norm w 0).2 = 1) :
    ∃ n, 0 < n ∧ pairWord n = stepWord w := by
  refine ⟨evalL (normalize w 0), ?_, ?_⟩
  · simpa [evalL_norm] using hp
  · unfold pairWord stepWord
    rw [digits_evalL _ (overflow_canonical w hb hc)]

theorem orbitWord_add (w : Word) (a b : Nat) :
    orbitWord w (a + b) = orbitWord (orbitWord w a) b := by
  induction b with
  | zero => rfl
  | succ b ih => simp [orbitWord, ih]

/-- Every positive bounded finite coefficient word eventually coincides, from
then on, with the pair-word trajectory of a positive ordinary integer.
The input need not be symmetric or canonically realizable. -/
theorem eventual_realization (w : Word) (hb : Bounded w) (hp : 0 < evalL w) :
    ∃ t n, 1 ≤ t ∧ t ≤ 2 * 10 ^ w.length ∧ 0 < n ∧
      ∀ k, pairWord (orbit n k) = orbitWord w (t + k) := by
  obtain ⟨j, hj, hc⟩ := overflow_before_bound w hb hp
  obtain ⟨n, hn, he⟩ := overflow_realized (orbitWord w j) (orbitWord_bounded w hb j)
    (orbitWord_value_growth w hp j).1 hc
  refine ⟨j + 1, n, by omega, by omega, hn, ?_⟩
  intro k
  rw [pairWord_orbit, he, orbitWord_add]
  rfl

/-- Time shifts of the ordinary reverse-and-add orbit commute with one step. -/
theorem orbit_step (n k : Nat) : orbit (step n) k = step (orbit n k) := by
  induction k with
  | zero => rfl
  | succ k ih => simp [orbit, ih]

/-- Infinite normalized-word safety of an arbitrary *finite* positive bounded
word transfers to an ordinary positive decimal seed after a finite transient.
This theorem assumes that full infinite safety property; it does not construct it. -/
theorem safe_symbolic_positive_seed (w : Word) (hb : Bounded w) (hp : 0 < evalL w)
    (hs : ∀ k, (normalize (orbitWord w k) 0).reverse ≠ normalize (orbitWord w k) 0) :
    ∃ m, 0 < m ∧ ∀ k, ¬ Palindrome (orbit m k) := by
  obtain ⟨t, n, _, _, hn, he⟩ := eventual_realization w hb hp
  refine ⟨step n, ?_, ?_⟩
  · unfold step; omega
  · intro k
    rw [orbit_step, step_palindrome_iff, he k]
    exact hs (t + k)


end Agent112.Eventual
#print axioms Agent112.Eventual.overflow_canonical
#print axioms Agent112.Eventual.overflow_realized
#print axioms Agent112.Eventual.orbitWord_add
#print axioms Agent112.Eventual.eventual_realization
#print axioms Agent112.Eventual.orbit_step
#print axioms Agent112.Eventual.safe_symbolic_positive_seed
