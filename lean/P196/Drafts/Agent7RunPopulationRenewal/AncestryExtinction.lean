import P196.Agent1PeriodicEighteenReturn.RunAncestry

/-!
# Extinction time of one maximal 0/18-run ancestry along an actual orbit

Agent #102 contribution (task `agent102-ancestry-lean`).

Formalizes `proofs/contributions/2026-10-15-ancestry-potential-bound/ANCESTRY_BOUND.md`:
if the tracked descendant of a maximal run of `0` or `18` of initial length `ell` is still
nonempty at time `t`, then

  `t + lowerPotential(p_t) ≤ 4 (ell - 1) + lowerPotential(p_0)`,

where `p_t` is the actual exterior pair coefficient at time `t`; hence the ancestry is extinct by
time `4 ell - 3 + lowerPotential(p_0) ≤ 4 ell + 1`.

The state at time `t` is `OverflowCarryNormalization.iterPairs q L t`, the exact column-sum word
(and width) of the `t`-th orbit integer (`iterPairs_representation`, restated below as
`tracked_orbit_representation`). Only ONE ancestry is followed: newly born runs are not tracked,
and nothing here asserts that 0/18 coefficients vanish, that a palindrome is reached, or anything
about 196.
-/

namespace RunAncestry

open DecimalDigits FoldedDecimal OverflowCarryNormalization DecimalWidthGrowth Lychrel196

/-- The tracked descendant interval of an initial run `[a,b)` of `c` after `t` actual steps. -/
def track (q : Nat → Nat) (L c a b : Nat) : Nat → Nat × Nat
  | 0 => (a, b)
  | t + 1 =>
    descendant (iterPairs q L t).2 (iterPairs q L t).1 c
      (track q L c a b t).1 (track q L c a b t).2

theorem descendant_sub (q : Nat → Nat) (L c a b : Nat) :
    a ≤ (descendant q L c a b).1 ∧ (descendant q L c a b).2 ≤ b := by
  unfold descendant
  split
  · constructor <;> dsimp only <;> split <;> omega
  · dsimp only; omega

theorem nextWidth_eq (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    nextWidth q L = L + carry q L := by
  have h := carry_le_one q L ha L (Nat.le_refl L)
  unfold nextWidth
  split <;> omega

/-- Once the tracked ancestry is empty it stays empty. -/
theorem track_empty_succ (q : Nat → Nat) (L c a b t : Nat)
    (he : (track q L c a b t).2 ≤ (track q L c a b t).1) :
    (track q L c a b (t + 1)).2 ≤ (track q L c a b (t + 1)).1 := by
  have := descendant_sub (iterPairs q L t).2 (iterPairs q L t).1 c
    (track q L c a b t).1 (track q L c a b t).2
  show (descendant _ _ c _ _).2 ≤ (descendant _ _ c _ _).1
  omega

theorem track_empty_mono (q : Nat → Nat) (L c a b t s : Nat) (hts : t ≤ s)
    (he : (track q L c a b t).2 ≤ (track q L c a b t).1) :
    (track q L c a b s).2 ≤ (track q L c a b s).1 := by
  induction s with
  | zero =>
    have : t = 0 := by omega
    subst this; exact he
  | succ s ih =>
    rcases Nat.lt_or_ge t (s + 1) with h | h
    · exact track_empty_succ q L c a b s (ih (by omega))
    · have : t = s + 1 := by omega
      subst this; exact he

/-- While the tracked ancestry survives it is a maximal run in the actual word, and every
overflow so far has cost at least one unit of its length. -/
theorem track_invariant (q : Nat → Nat) (L c a b : Nat) (ha : Admissible L q)
    (hc : c = 0 ∨ c = 18) (hr : MaximalRun q L c a b) :
    ∀ t, (track q L c a b t).1 < (track q L c a b t).2 →
      MaximalRun (iterPairs q L t).2 (iterPairs q L t).1 c
          (track q L c a b t).1 (track q L c a b t).2 ∧
        L ≤ (iterPairs q L t).1 ∧
        (track q L c a b t).2 - (track q L c a b t).1 + ((iterPairs q L t).1 - L) ≤ b - a := by
  intro t
  induction t with
  | zero =>
    intro _
    refine ⟨hr, Nat.le_refl L, ?_⟩
    show b - a + (L - L) ≤ b - a
    omega
  | succ t ih =>
    intro hne
    have hsub := descendant_sub (iterPairs q L t).2 (iterPairs q L t).1 c
      (track q L c a b t).1 (track q L c a b t).2
    have hne' : (track q L c a b t).1 < (track q L c a b t).2 := by
      change (descendant _ _ c _ _).1 < (descendant _ _ c _ _).2 at hne
      omega
    obtain ⟨hmr, hwL, hlen⟩ := ih hne'
    have hadm := CarryHistory.iterPairs_admissible q L t ha
    obtain ⟨-, hmax, hbd⟩ := descendant_step _ _ c _ _ hadm hc hmr
    have hw : (iterPairs q L (t + 1)).1 =
        (iterPairs q L t).1 + carry (iterPairs q L t).2 (iterPairs q L t).1 := by
      show nextWidth _ _ = _
      exact nextWidth_eq _ _ hadm
    refine ⟨hmax hne, ?_, ?_⟩
    · omega
    · change (descendant _ _ c _ _).2 - (descendant _ _ c _ _).1 + _ ≤ _
      rw [hw]
      omega

/-- Telescoped actual outer potential, keeping the final potential term. -/
theorem potential_telescope (q : Nat → Nat) (L : Nat) (ha : Admissible L q) :
    ∀ t, t + lowerPotential ((iterPairs q L t).2 0) + 4 * L ≤
      lowerPotential (q 0) + 4 * (iterPairs q L t).1 := by
  intro t
  induction t with
  | zero => show 0 + lowerPotential (q 0) + 4 * L ≤ lowerPotential (q 0) + 4 * L; omega
  | succ t ih =>
    have hadm := CarryHistory.iterPairs_admissible q L t ha
    have hs := lower_potential_step (iterPairs q L t).2 (iterPairs q L t).1 hadm
    show t + 1 + lowerPotential (nextColumns _ _ 0) + 4 * L ≤
      lowerPotential (q 0) + 4 * nextWidth _ _
    omega

/-- **Survival bound.** If the ancestry of a maximal run of `0` or `18` of length
`b - a` survives to time `t`, then `t + ψ(p_t) ≤ 4 (b - a - 1) + ψ(p_0)`. -/
theorem survival_bound (q : Nat → Nat) (L c a b t : Nat) (ha : Admissible L q)
    (hc : c = 0 ∨ c = 18) (hr : MaximalRun q L c a b)
    (hsurv : (track q L c a b t).1 < (track q L c a b t).2) :
    t + lowerPotential ((iterPairs q L t).2 0) ≤ 4 * (b - a - 1) + lowerPotential (q 0) := by
  obtain ⟨-, hwL, hlen⟩ := track_invariant q L c a b ha hc hr t hsurv
  have hp := potential_telescope q L ha t
  have hab := hr.1
  omega

/-- **Extinction.** The tracked ancestry is empty at every time
`t ≥ 4 (b - a) - 3 + ψ(p_0)`. -/
theorem extinct_after (q : Nat → Nat) (L c a b t : Nat) (ha : Admissible L q)
    (hc : c = 0 ∨ c = 18) (hr : MaximalRun q L c a b)
    (ht : 4 * (b - a) - 3 + lowerPotential (q 0) ≤ t) :
    (track q L c a b t).2 ≤ (track q L c a b t).1 := by
  have hab := hr.1
  rcases Nat.lt_or_ge (track q L c a b t).1 (track q L c a b t).2 with h | h
  · have := survival_bound q L c a b t ha hc hr h
    omega
  · exact h

/-- **Uniform extinction.** The tracked ancestry is empty at every time `t ≥ 4 (b - a) + 1`. -/
theorem extinct_uniform (q : Nat → Nat) (L c a b t : Nat) (ha : Admissible L q)
    (hc : c = 0 ∨ c = 18) (hr : MaximalRun q L c a b)
    (ht : 4 * (b - a) + 1 ≤ t) :
    (track q L c a b t).2 ≤ (track q L c a b t).1 := by
  have := lowerPotential_bounded (q 0)
  have hab := hr.1
  exact extinct_after q L c a b t ha hc hr (by omega)

/-- Actual-integer reading: from a canonical decimal `n` of width `L` with column-sum word
`q = columnSum d L`, the tracked words are the exact column-sum words of `orbit n t`, and the
ancestry of any maximal 0/18 run of `q` of length `ell` is empty from time
`4 ell - 3 + ψ(q 0)` on (in particular from `4 ell + 1` on). -/
theorem orbit_ancestry_extinct (n : Nat) (d : Nat → Nat) (L c a b : Nat)
    (hcan : Canonical n d L) (hc : c = 0 ∨ c = 18)
    (hr : MaximalRun (columnSum d L) L c a b) :
    (∀ t, ∃ e, Canonical (orbit n t) e (iterPairs (columnSum d L) L t).1 ∧
        ∀ i, i < (iterPairs (columnSum d L) L t).1 →
          columnSum e (iterPairs (columnSum d L) L t).1 i = (iterPairs (columnSum d L) L t).2 i) ∧
    (∀ t, (track (columnSum d L) L c a b t).1 < (track (columnSum d L) L c a b t).2 →
        MaximalRun (iterPairs (columnSum d L) L t).2 (iterPairs (columnSum d L) L t).1 c
          (track (columnSum d L) L c a b t).1 (track (columnSum d L) L c a b t).2 ∧
        t + lowerPotential ((iterPairs (columnSum d L) L t).2 0) ≤
          4 * (b - a - 1) + lowerPotential (columnSum d L 0)) ∧
    (∀ t, 4 * (b - a) - 3 + lowerPotential (columnSum d L 0) ≤ t →
        (track (columnSum d L) L c a b t).2 ≤ (track (columnSum d L) L c a b t).1) := by
  have ha := NormalizationBridge.canonical_admissible n d L hcan
  refine ⟨fun t => iterPairs_representation n d (columnSum d L) L t hcan (fun _ _ => rfl),
    fun t h => ⟨(track_invariant _ L c a b ha hc hr t h).1, survival_bound _ L c a b t ha hc hr h⟩,
    fun t h => extinct_after _ L c a b t ha hc hr h⟩

end RunAncestry

#print axioms RunAncestry.track_invariant
#print axioms RunAncestry.potential_telescope
#print axioms RunAncestry.survival_bound
#print axioms RunAncestry.extinct_after
#print axioms RunAncestry.extinct_uniform
#print axioms RunAncestry.orbit_ancestry_extinct

namespace RunAncestry
open DecimalDigits FoldedDecimal

/-- **Central run quotient (ABSORBING_CORE.md sec. 3).** For a maximal central run
`[a, L-a)` of `0` or `18` (length `g = L - 2a`), one actual step leaves exactly the central
interval of length `g` (no overflow, boundary carry `= reset c`), `g - 2` (no overflow, other
boundary carry) or `g - 1` (overflow), truncated at zero; the descendant is again a maximal run
whenever nonempty. In particular no step lengthens a tracked central 0/18 band. -/
theorem central_run_step (q : Nat → Nat) (L c a : Nat) (ha : Admissible L q)
    (hc : c = 0 ∨ c = 18) (hr : MaximalRun q L c a (L - a)) :
    (descendant q L c a (L - a)).2 - (descendant q L c a (L - a)).1 =
      (if carry q L = 0 then
        (if carry q a = reset c then L - 2 * a else L - 2 * a - 2)
      else L - 2 * a - 1) ∧
    ((descendant q L c a (L - a)).1 < (descendant q L c a (L - a)).2 →
      MaximalRun (nextColumns q L) (nextWidth q L) c
        (descendant q L c a (L - a)).1 (descendant q L c a (L - a)).2) := by
  refine ⟨?_, (descendant_step q L c a (L - a) ha hc hr).2.1⟩
  have hab := hr.1
  have hb : L - (L - a) = a := by omega
  unfold descendant
  rw [hb]
  by_cases h0 : carry q L = 0
  · simp only [h0, if_true]
    by_cases hx : carry q a = reset c
    · simp only [hx, if_true]; omega
    · simp only [hx, if_false]; omega
  · simp only [h0, if_false]; omega

end RunAncestry

#print axioms RunAncestry.central_run_step
