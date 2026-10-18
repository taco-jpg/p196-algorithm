import Std

set_option autoImplicit false

/-!
Agent #423: finite, horizon-independent seed ensembles.
Source mathematical contract: Agent #17 PR58 README and Agent #317 PR77.
The explicit List enumeration replaces the unavailable Fintype/Finset interface,
not the mathematical finiteness hypothesis. No decimal-orbit premise is supplied.
-/
namespace Agent423.FiniteEnsemble

universe u
variable {α : Type u}

def PrefixSafe (Safe : α → Nat → Prop) (x : α) (N : Nat) : Prop :=
  ∀ t, t ≤ N → Safe x t

def ForeverSafe (Safe : α → Nat → Prop) (x : α) : Prop :=
  ∀ t, Safe x t

theorem prefixSafe_mono {Safe : α → Nat → Prop} {x : α} {M N : Nat}
    (hMN : M ≤ N) (h : PrefixSafe Safe x N) : PrefixSafe Safe x M := by
  intro t ht
  exact h t (Nat.le_trans ht hMN)

theorem foreverSafe_prefix {Safe : α → Nat → Prop} {x : α}
    (h : ForeverSafe Safe x) (N : Nat) : PrefixSafe Safe x N := by
  intro t _
  exact h t

theorem foreverSafe_iff_all_prefixes (Safe : α → Nat → Prop) (x : α) :
    ForeverSafe Safe x ↔ ∀ N, PrefixSafe Safe x N := by
  constructor
  · exact fun h N => foreverSafe_prefix h N
  · exact fun h t => h t t (Nat.le_refl t)

/-- Constructive finite collection of existential natural-number witnesses.
Duplicates and the empty list are allowed. No choice axiom is needed. -/
theorem finite_bounded_witnesses (K : List α) (R : α → Nat → Prop)
    (h : ∀ x, x ∈ K → ∃ t, R x t) :
    ∃ M, ∀ x, x ∈ K → ∃ t, t ≤ M ∧ R x t := by
  induction K with
  | nil =>
      refine ⟨0, ?_⟩
      intro x hx
      simp at hx
  | cons a K ih =>
      obtain ⟨ta, ha⟩ := h a (by simp)
      obtain ⟨M, hM⟩ := ih (fun x hx => h x (by simp [hx]))
      refine ⟨max ta M, ?_⟩
      intro x hx
      rcases List.mem_cons.mp hx with hxa | hxK
      · subst x
        exact ⟨ta, Nat.le_max_left ta M, ha⟩
      · obtain ⟨t, ht, hR⟩ := hM x hxK
        exact ⟨t, Nat.le_trans ht (Nat.le_max_right ta M), hR⟩

theorem not_forever_iff_exists_failure (Safe : α → Nat → Prop) (x : α) :
    ¬ ForeverSafe Safe x ↔ ∃ t, ¬ Safe x t := by
  constructor
  · intro h
    apply Classical.byContradiction
    intro hn
    apply h
    intro t
    apply Classical.byContradiction
    intro ht
    exact hn ⟨t, ht⟩
  · intro h hf
    obtain ⟨t, ht⟩ := h
    exact ht (hf t)

/-- If each member eventually fails, all failure witnesses have a common
finite bound. This does not assume any numerical bound in advance. -/
theorem uniform_failure_bound (K : List α) (Safe : α → Nat → Prop)
    (h : ∀ x, x ∈ K → ¬ ForeverSafe Safe x) :
    ∃ M, ∀ x, x ∈ K → ∃ t, t ≤ M ∧ ¬ Safe x t := by
  apply finite_bounded_witnesses K (fun x t => ¬ Safe x t)
  intro x hx
  exact (not_forever_iff_exists_failure Safe x).mp (h x hx)

/-- Exact written finite-ensemble extraction claim, with an explicit finite
list rather than an undeclared Fintype interface. -/
theorem finite_uniform_extraction (K : List α) (Safe : α → Nat → Prop)
    (hprefix : ∀ N, ∃ x, x ∈ K ∧ PrefixSafe Safe x N) :
    ∃ x, x ∈ K ∧ ForeverSafe Safe x := by
  apply Classical.byContradiction
  intro hnone
  have hbad : ∀ x, x ∈ K → ¬ ForeverSafe Safe x := by
    intro x hx hf
    exact hnone ⟨x, hx, hf⟩
  obtain ⟨M, hM⟩ := uniform_failure_bound K Safe hbad
  obtain ⟨x, hxK, hx⟩ := hprefix M
  obtain ⟨t, htM, ht⟩ := hM x hxK
  exact ht (hx t htM)

theorem finite_uniform_iff (K : List α) (Safe : α → Nat → Prop) :
    (∃ x, x ∈ K ∧ ForeverSafe Safe x) ↔
      (∀ N, ∃ x, x ∈ K ∧ PrefixSafe Safe x N) := by
  constructor
  · intro h N
    obtain ⟨x, hx, hf⟩ := h
    exact ⟨x, hx, foreverSafe_prefix hf N⟩
  · exact finite_uniform_extraction K Safe

/-- Type-level wrapper with an explicit complete enumeration. Nonemptiness
need not be assumed: the horizon-zero premise already supplies a member. -/
theorem enumerated_type_uniform_extraction (enum : List α)
    (complete : ∀ x : α, x ∈ enum) (Safe : α → Nat → Prop)
    (hprefix : ∀ N, ∃ x : α, PrefixSafe Safe x N) :
    ∃ x : α, ForeverSafe Safe x := by
  have h : ∀ N, ∃ x, x ∈ enum ∧ PrefixSafe Safe x N := by
    intro N
    obtain ⟨x, hx⟩ := hprefix N
    exact ⟨x, complete x, hx⟩
  obtain ⟨x, _, hx⟩ := finite_uniform_extraction enum Safe h
  exact ⟨x, hx⟩

/-- Cofinal sampled horizons suffice; the sequence need not be monotone. -/
theorem cofinal_horizons_extraction (K : List α) (Safe : α → Nat → Prop)
    (horizon : Nat → Nat) (cofinal : ∀ N, ∃ i, N ≤ horizon i)
    (hprefix : ∀ i, ∃ x, x ∈ K ∧ PrefixSafe Safe x (horizon i)) :
    ∃ x, x ∈ K ∧ ForeverSafe Safe x := by
  apply finite_uniform_extraction K Safe
  intro N
  obtain ⟨i, hi⟩ := cofinal N
  obtain ⟨x, hxK, hx⟩ := hprefix i
  exact ⟨x, hxK, prefixSafe_mono hi hx⟩

/-- Equivalent finite refutation of every candidate. -/
theorem no_forever_iff_finite_obstruction (K : List α) (Safe : α → Nat → Prop) :
    (¬ ∃ x, x ∈ K ∧ ForeverSafe Safe x) ↔
      (∃ M, ∀ x, x ∈ K → ¬ PrefixSafe Safe x M) := by
  constructor
  · intro hn
    have hbad : ∀ x, x ∈ K → ¬ ForeverSafe Safe x := by
      intro x hx hf
      exact hn ⟨x, hx, hf⟩
    obtain ⟨M, hM⟩ := uniform_failure_bound K Safe hbad
    refine ⟨M, ?_⟩
    intro x hx hp
    obtain ⟨t, htM, ht⟩ := hM x hx
    exact ht (hp t htM)
  · intro h hf
    obtain ⟨M, hM⟩ := h
    obtain ⟨x, hx, hs⟩ := hf
    exact hM x hx (foreverSafe_prefix hs M)

/-- Every fixed finite ensemble has a finite horizon after which its prefix
survivors are exactly its all-time survivors. No effective bound is asserted. -/
theorem finite_survivors_stabilize (K : List α) (Safe : α → Nat → Prop) :
    ∃ M, ∀ N, M ≤ N → ∀ x, x ∈ K →
      (PrefixSafe Safe x N ↔ ForeverSafe Safe x) := by
  have hw : ∀ x, x ∈ K → ∃ t,
      ForeverSafe Safe x ∨ ¬ PrefixSafe Safe x t := by
    intro x _
    by_cases hf : ForeverSafe Safe x
    · exact ⟨0, Or.inl hf⟩
    · obtain ⟨t, ht⟩ := (not_forever_iff_exists_failure Safe x).mp hf
      exact ⟨t, Or.inr (fun hp => ht (hp t (Nat.le_refl t)))⟩
  obtain ⟨M, hM⟩ := finite_bounded_witnesses K
    (fun x t => ForeverSafe Safe x ∨ ¬ PrefixSafe Safe x t) hw
  refine ⟨M, ?_⟩
  intro N hMN x hx
  constructor
  · intro hp
    obtain ⟨t, htM, hf | hfail⟩ := hM x hx
    · exact hf
    · exact False.elim (hfail (prefixSafe_mono (Nat.le_trans htM hMN) hp))
  · exact fun hf => foreverSafe_prefix hf N

/-- The seed bound is fixed before quantifying over horizons. Zero is allowed. -/
theorem bounded_nat_seed_extraction (B : Nat) (Safe : Nat → Nat → Prop)
    (hprefix : ∀ N, ∃ x, x ≤ B ∧ PrefixSafe Safe x N) :
    ∃ x, x ≤ B ∧ ForeverSafe Safe x := by
  have h : ∀ N, ∃ x, x ∈ List.range (B + 1) ∧ PrefixSafe Safe x N := by
    intro N
    obtain ⟨x, hxB, hx⟩ := hprefix N
    exact ⟨x, List.mem_range.mpr (Nat.lt_succ_of_le hxB), hx⟩
  obtain ⟨x, hxK, hx⟩ := finite_uniform_extraction (List.range (B + 1)) Safe h
  exact ⟨x, Nat.le_of_lt_succ (List.mem_range.mp hxK), hx⟩

/-- Positive-seed variant. Positivity is carried from the actual premise. -/
theorem positive_bounded_nat_seed_extraction (B : Nat) (Safe : Nat → Nat → Prop)
    (hprefix : ∀ N, ∃ x, 0 < x ∧ x ≤ B ∧ PrefixSafe Safe x N) :
    ∃ x, 0 < x ∧ x ≤ B ∧ ForeverSafe Safe x := by
  have h : ∀ N, ∃ x, x ≤ B ∧ PrefixSafe (fun x t => 0 < x ∧ Safe x t) x N := by
    intro N
    obtain ⟨x, hxpos, hxB, hx⟩ := hprefix N
    exact ⟨x, hxB, fun t ht => ⟨hxpos, hx t ht⟩⟩
  obtain ⟨x, hxB, hx⟩ := bounded_nat_seed_extraction B (fun x t => 0 < x ∧ Safe x t) h
  exact ⟨x, (hx 0).1, hxB, fun t => (hx t).2⟩

/-- A repaired proof of PR58's exact unrestricted quantifier counterexample. -/
theorem unrestricted_quantifier_swap_counterexample :
    ¬ ((∀ N : Nat, ∃ x : Nat, ∀ t, t ≤ N → t < x) →
       ∃ x : Nat, ∀ t, t < x) := by
  intro h
  have hp : ∀ N : Nat, ∃ x : Nat, ∀ t, t ≤ N → t < x := by
    intro N
    exact ⟨N + 1, fun _ ht => Nat.lt_succ_of_le ht⟩
  obtain ⟨x, hx⟩ := h hp
  exact Nat.lt_irrefl x (hx x)

/-- PR77's exact conjunction, with no extraction-interface changes. -/
theorem moving_seed_counterexample :
    (∀ N : Nat, ∃ x : Nat, ∀ t, t ≤ N → t < x) ∧
    ¬ (∃ x : Nat, ∀ t, t < x) := by
  constructor
  · intro N
    exact ⟨N + 1, fun _ ht => Nat.lt_succ_of_le ht⟩
  · intro h
    obtain ⟨x, hx⟩ := h
    exact Nat.lt_irrefl x (hx x)

/-- Finite candidate universes at each horizon still do not suffice when
their bound is allowed to grow with that horizon. -/
theorem horizon_dependent_bound_counterexample :
    (∀ N : Nat, ∃ x : Nat, x ≤ N + 1 ∧ PrefixSafe (fun x t => t < x) x N) ∧
    ¬ (∃ x : Nat, ForeverSafe (fun x t => t < x) x) := by
  constructor
  · intro N
    exact ⟨N + 1, Nat.le_refl _, fun _ ht => Nat.lt_succ_of_le ht⟩
  · intro h
    obtain ⟨x, hx⟩ := h
    exact Nat.lt_irrefl x (hx x)

#print axioms prefixSafe_mono
#print axioms foreverSafe_prefix
#print axioms foreverSafe_iff_all_prefixes
#print axioms finite_bounded_witnesses
#print axioms not_forever_iff_exists_failure
#print axioms uniform_failure_bound
#print axioms finite_uniform_extraction
#print axioms finite_uniform_iff
#print axioms enumerated_type_uniform_extraction
#print axioms cofinal_horizons_extraction
#print axioms no_forever_iff_finite_obstruction
#print axioms finite_survivors_stabilize
#print axioms bounded_nat_seed_extraction
#print axioms positive_bounded_nat_seed_extraction
#print axioms unrestricted_quantifier_swap_counterexample
#print axioms moving_seed_counterexample
#print axioms horizon_dependent_bound_counterexample

end Agent423.FiniteEnsemble
