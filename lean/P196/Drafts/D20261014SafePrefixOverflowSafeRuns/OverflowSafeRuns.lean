import P196.Agent1Pr104Repair.DecimalDelayBridge

/-!
Overflow-sensitive persistence of runs of pair coefficient 18.

An overflow erodes only one column of a run; a nonoverflow erodes two.
The exact width-growth potential therefore improves the explicit
all-nines safe-prefix length from 2R+1 to floor(7R/4)+1.
These are finite safety results. They do not imply eventual termination,
an infinite safe orbit, decimal Lychrel existence, or the 196 conjecture.
-/

namespace OverflowSafeRuns

open Lychrel196 DecimalDigits FoldedDecimal OverflowCarryNormalization
  CarryHistory DecimalSafeRuns DecimalWidthGrowth

/-- On overflow only two consecutive 18 columns are needed. -/
theorem next_eighteen_overflow (q : Nat → Nat) (L i : Nat)
    (ha : Admissible L q) (hc : carry q L ≠ 0)
    (hi0 : 0 < i) (hi : i < L)
    (hleft : q (i - 1) = 18) (hmid : q i = 18) :
    nextColumns q L i = 18 := by
  have hlo := output_eighteen_after_eighteen q L i ha hi0 hi hleft hmid
  have hm : q (L - i) = 18 := by
    have hs := (ha.2.2.2.1 (i - 1) (by omega)).symm.trans hleft
    have he : L - 1 - (i - 1) = L - i := by omega
    simpa only [he] using hs
  have hp : q (L - i - 1) = 18 := by
    have hs := (ha.2.2.2.1 i hi).symm.trans hmid
    have he : L - 1 - i = L - i - 1 := by omega
    simpa only [he] using hs
  have hhi := output_eighteen_after_eighteen q L (L - i) ha
    (by omega) (by omega) hp hm
  simp only [nextColumns, hc, if_false, columnSum, reflected,
    Nat.add_sub_cancel, extended, hi, show L - i < L by omega,
    if_true, hlo, hhi]

theorem run18_next_overflow (q : Nat → Nat) (L a m : Nat)
    (ha : Admissible L q) (hc : carry q L ≠ 0)
    (hr : Run18 q L a (m + 1)) :
    Run18 (nextColumns q L) (nextWidth q L) (a + 1) m := by
  constructor
  · simp only [nextWidth, hc, if_false]
    have := hr.1
    omega
  · intro i hia him
    apply next_eighteen_overflow q L i ha hc (by omega) (by have := hr.1; omega)
    · exact hr.2 (i - 1) (by omega) (by omega)
    · exact hr.2 i (by omega) (by omega)

theorem hasRun18_next_overflow (q : Nat → Nat) (L m : Nat)
    (ha : Admissible L q) (hc : carry q L ≠ 0)
    (hr : HasRun18 q L (m + 1)) :
    HasRun18 (nextColumns q L) (nextWidth q L) m := by
  obtain ⟨a, hr⟩ := hr
  exact ⟨a + 1, run18_next_overflow q L a m ha hc hr⟩

/-- One column per step, plus one for each nonoverflow step. -/
def erosionCost (q : Nat → Nat) (L t : Nat) : Nat :=
  t + noOverflowCount (fun k => (iterPairs q L k).2)
    (fun k => (iterPairs q L k).1) t

theorem erosionCost_zero (q : Nat → Nat) (L : Nat) : erosionCost q L 0 = 0 := rfl

theorem erosionCost_succ (q : Nat → Nat) (L t : Nat) :
    erosionCost q L (t + 1) = erosionCost q L t +
      if carry (iterPairs q L t).2 (iterPairs q L t).1 = 0 then 2 else 1 := by
  simp only [erosionCost, noOverflowCount]
  split <;> omega

/-- Exact accounting: every overflow saves one unit of run erosion. -/
theorem erosionCost_width_identity (q : Nat → Nat) (L t : Nat) :
    erosionCost q L t + (iterPairs q L t).1 = L + 2 * t := by
  have h := width_count_identity q L t
  unfold erosionCost
  omega

/-- The bound keeps the initial outer-column potential. -/
theorem erosionCost_bound (q : Nat → Nat) (L t : Nat)
    (ha : Admissible L q) :
    4 * erosionCost q L t ≤ 7 * t + lowerPotential (q 0) := by
  have hw := width_lower_potential q L t ha
  have he := erosionCost_width_identity q L t
  omega

/-- Exact finite persistence, depending on the actual overflow schedule. -/
theorem hasRun18_iter_cost (q : Nat → Nat) (L m t : Nat)
    (ha : Admissible L q) (hr : HasRun18 q L (m + erosionCost q L t)) :
    HasRun18 (iterPairs q L t).2 (iterPairs q L t).1 m := by
  induction t generalizing m with
  | zero => simpa only [erosionCost_zero, Nat.add_zero, iterPairs] using hr
  | succ t ih =>
    have he := erosionCost_succ q L t
    by_cases hc : carry (iterPairs q L t).2 (iterPairs q L t).1 = 0
    · simp only [hc, if_true] at he
      have he' : m + 2 + erosionCost q L t = m + erosionCost q L (t + 1) := by omega
      have hp := ih (m + 2) (by simpa only [he'] using hr)
      exact hasRun18_next _ _ m (iterPairs_admissible q L t ha) hp
    · simp only [hc, if_false] at he
      have he' : m + 1 + erosionCost q L t = m + erosionCost q L (t + 1) := by omega
      have hp := ih (m + 1) (by simpa only [he'] using hr)
      exact hasRun18_next_overflow _ _ m (iterPairs_admissible q L t ha) hc hp

theorem iter_not_palindrome_of_run_cost (n : Nat) (d q : Nat → Nat) (L t : Nat)
    (hc : Canonical n d L) (hr : ∀ i, i < L → columnSum d L i = q i)
    (ha : Admissible L q) (h18 : HasRun18 q L (1 + erosionCost q L t)) :
    ¬ Palindrome (orbit n (t + 1)) := by
  obtain ⟨e, he, hrep⟩ := iterPairs_representation n d q L t hc hr
  exact next_not_palindrome_of_not_bad _ e _ _ he hrep
    (hasRun18_not_bad _ _ (hasRun18_iter_cost q L 1 t ha h18))

theorem hasRun18_mono (q : Nat → Nat) (L m M : Nat)
    (hm : m ≤ M) (hr : HasRun18 q L M) : HasRun18 q L m := by
  obtain ⟨a, hb, hq⟩ := hr
  exact ⟨a, by omega, fun i hi hit => hq i hi (by omega)⟩

/-- A numeric run-length criterion retaining the initial outer potential. -/
theorem iter_not_palindrome_of_run_bound (n : Nat) (d q : Nat → Nat) (L t : Nat)
    (hc : Canonical n d L) (hr : ∀ i, i < L → columnSum d L i = q i)
    (ha : Admissible L q)
    (h18 : HasRun18 q L (1 + (7 * t + lowerPotential (q 0)) / 4)) :
    ¬ Palindrome (orbit n (t + 1)) := by
  have hb := erosionCost_bound q L t ha
  exact iter_not_palindrome_of_run_cost n d q L t hc hr ha
    (hasRun18_mono q L _ _ (by omega) h18)

/-- A uniform initial run certifies every positive time through R+1. -/
theorem safe_prefix_of_uniform_run (n : Nat) (d q : Nat → Nat) (L R k : Nat)
    (hc : Canonical n d L) (hr : ∀ i, i < L → columnSum d L i = q i)
    (ha : Admissible L q) (hk : k ≤ R)
    (h18 : HasRun18 q L (1 + (7 * R + 4) / 4)) :
    ¬ Palindrome (orbit n (k + 1)) := by
  have hb := erosionCost_bound q L k ha
  have hp := lowerPotential_bounded (q 0)
  exact iter_not_palindrome_of_run_cost n d q L k hc hr ha
    (hasRun18_mono q L _ _ (by omega) h18)

/-- Shorter explicit input length; division is floor division. -/
def safeLength (R : Nat) : Nat := 7 * R / 4 + 1

theorem safeLength_le_previous (R : Nat) : safeLength R ≤ 2 * R + 1 := by
  unfold safeLength
  omega

theorem safeLength_lt_previous (R : Nat) (hR : 0 < R) : safeLength R < 2 * R + 1 := by
  unfold safeLength
  omega

/-- Unconditional safety of every positive time through R+1. -/
theorem nines_safe_prefix_sharper (R k : Nat) (hk : k ≤ R) :
    ¬ Palindrome (orbit (nines (safeLength R)) (k + 1)) := by
  let d : Nat → Nat := fun _ => 9
  let q : Nat → Nat := fun _ => 18
  let L := safeLength R
  have hL : 0 < L := by dsimp [L, safeLength]; omega
  have hc : Canonical (nines L) d L := nines_canonical L hL
  have hrep : ∀ i, i < L → columnSum d L i = q i := by intro i hi; rfl
  have ha : Admissible L q := NormalizationBridge.admissible_congr _ _ _
    (NormalizationBridge.canonical_admissible _ _ _ hc) hrep
  have hb := erosionCost_bound q L k ha
  have hpot : lowerPotential (q 0) = 0 := rfl
  rw [hpot] at hb
  have hcost : 1 + erosionCost q L k ≤ L := by
    dsimp [L, safeLength] at hb ⊢
    omega
  exact iter_not_palindrome_of_run_cost (nines L) d q L k hc hrep ha
    ⟨0, by omega, by intro i hi hlt; rfl⟩

/-- A finite ordinary integer whose initial state is also safe. -/
def shorterCandidate (R : Nat) : Nat := 2 * (10 ^ safeLength R - 1)

theorem shorterCandidate_eq_step_nines (R : Nat) :
    shorterCandidate R = step (nines (safeLength R)) := by
  have hn := DecimalDelayBridge.nines_add_one (safeLength R)
  have hp := DecimalDelayBridge.nines_palindrome (safeLength R)
  change reverse10 (nines (safeLength R)) = nines (safeLength R) at hp
  unfold shorterCandidate step
  rw [hp]
  omega

theorem shorterCandidate_positive (R : Nat) : 0 < shorterCandidate R := by
  rw [shorterCandidate_eq_step_nines]
  exact DecimalDelayBridge.step_positive _ (nines_positive _ (by unfold safeLength; omega))

/-- Safety includes time zero, unlike the palindromic all-nines seed. -/
theorem shorterCandidate_safe_prefix (R k : Nat) (hk : k ≤ R) :
    ¬ Palindrome (orbit (shorterCandidate R) k) := by
  rw [shorterCandidate_eq_step_nines, DecimalDelayBridge.orbit_step]
  exact nines_safe_prefix_sharper R k hk

/-- If this candidate eventually terminates, its positive delay exceeds R.
No eventual-termination hypothesis is discharged here. -/
theorem shorterCandidate_first_hit_gt (R d : Nat)
    (hf : DecimalDelayBridge.FirstPositiveHit (shorterCandidate R) d) : R < d := by
  apply Classical.byContradiction
  intro h
  exact shorterCandidate_safe_prefix R d (by omega) hf.2.1

/-- The improved candidate works under the same unproved finite-delay bound. -/
theorem shorterCandidate_lychrel_of_finiteDelayBound (R : Nat)
    (hbound : DecimalDelayBridge.FiniteDelayBound R) : IsLychrel (shorterCandidate R) := by
  have hn : 0 < nines (safeLength R) := nines_positive _ (by unfold safeLength; omega)
  have hs : SafeImageDynamics.SafePrefix step DecimalDelayBridge.Bad
      (nines (safeLength R)) R := by
    intro k hk hb
    exact nines_safe_prefix_sharper R k (by omega)
      ((DecimalDelayBridge.bad_iter_iff _ k).mp hb)
  have ha := SafeImageDynamics.avoids_of_finite_bound step (fun n => 0 < n)
    DecimalDelayBridge.Bad R ((DecimalDelayBridge.finiteDelayBound_iff R).mp hbound)
    _ hn hs
  intro k
  rw [shorterCandidate_eq_step_nines, DecimalDelayBridge.orbit_step]
  intro hp
  exact ha k ((DecimalDelayBridge.bad_iter_iff _ k).mpr hp)

#print axioms next_eighteen_overflow
#print axioms erosionCost_width_identity
#print axioms hasRun18_iter_cost
#print axioms erosionCost_bound
#print axioms nines_safe_prefix_sharper
#print axioms safe_prefix_of_uniform_run
#print axioms shorterCandidate_safe_prefix
#print axioms shorterCandidate_first_hit_gt
#print axioms shorterCandidate_lychrel_of_finiteDelayBound

end OverflowSafeRuns
