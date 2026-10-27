import P196.Agent119NeutralCenterUnpadding.Inverse
import P196.Agent1PeriodicNineCenter.Agent1PeriodicCenterWrap
import P196.Agent105NormalizeReview.Agent105AffineNormalize

/-!
# Maximal neutral-center core

The existing generic period stripper, specialized to the singleton neutral
coefficient, supplies the core and removed depth. These lemmas connect that
unchanged algorithm to the A120 padding API; no new stripping loop is introduced.
-/

namespace Agent119.NeutralCenterCanonicalization

open Agent120.Neutral
open Agent119.NeutralCenterPadding Agent119.NeutralCenterUnpadding
open Agent1.Periodic

/-- The center after all paired neutral boundary coefficients are removed. -/
def coreC (b : Nat) (C : List Nat) : List Nat :=
  (stripPeriodCenter [b - 1] C).1

/-- The number of neutral coefficients removed from each side of the center. -/
def depthC (b : Nat) (C : List Nat) : Nat :=
  (stripPeriodCenter [b - 1] C).2

theorem decompose (b : Nat) (C : List Nat) :
    C = padC b (depthC b C) (coreC b C) := by
  have h := stripPeriodCenter_decomposition [b - 1] C
  simpa only [coreC, depthC, padC, List.reverse_cons, List.reverse_nil, List.nil_append,
    Agent105.AffineNormalize.singleton_pow, List.append_assoc] using h

private theorem strip_padC (b a : Nat) (C : List Nat) :
    stripPeriodCenter [b - 1] (padC b a C) = (coreC b C, a + depthC b C) := by
  induction a with
  | zero => simp [padC_zero, coreC, depthC]
  | succ a ih =>
      have hp : padC b (a + 1) C = [b - 1] ++ padC b a C ++ [b - 1] := by
        calc
          padC b (a + 1) C = padC b 1 (padC b a C) := by
            rw [padC_add, Nat.add_comm 1 a]
          _ = [b - 1] ++ padC b a C ++ [b - 1] := by
            simp only [padC, List.replicate_one, List.append_assoc]
      rw [hp]
      have hw := stripPeriodCenter_wrap [b - 1] (padC b a C) (by simp)
      simp only [List.reverse_cons, List.reverse_nil, List.nil_append, ih] at hw
      rw [hw]
      congr 1
      omega

theorem core_padC (b a : Nat) (C : List Nat) :
    coreC b (padC b a C) = coreC b C := by
  have h := congrArg Prod.fst (strip_padC b a C)
  exact h

theorem depth_padC (b a : Nat) (C : List Nat) :
    depthC b (padC b a C) = a + depthC b C := by
  have h := congrArg Prod.snd (strip_padC b a C)
  exact h

theorem core_idempotent (b : Nat) (C : List Nat) :
    coreC b (coreC b C) = coreC b C := by
  have h := congrArg (coreC b) (decompose b C)
  rw [core_padC] at h
  exact h.symm

theorem depth_core (b : Nat) (C : List Nat) :
    depthC b (coreC b C) = 0 := by
  have h := congrArg (depthC b) (decompose b C)
  rw [depth_padC] at h
  omega

theorem core_length_le (b : Nat) (C : List Nat) :
    (coreC b C).length ≤ C.length :=
  stripPeriodCenter_length_le [b - 1] C

theorem core_irreducible (b : Nat) (C : List Nat) :
    ¬ ∃ D, coreC b C = padC b 1 D := by
  rintro ⟨D, hD⟩
  apply stripPeriodCenter_maximal [b - 1] C (by simp)
  refine ⟨D, ?_⟩
  simpa only [coreC, padC, List.replicate_one, List.reverse_cons, List.reverse_nil, List.nil_append,
    List.append_assoc] using hD

/-- The complete source hypotheses are invariant under maximal center stripping. -/
theorem Hyp_core_iff {b : Nat} {B C : List Nat} :
    Hyp b B (coreC b C) ↔ Hyp b B C := by
  have h := Hyp_padC_iff (b := b) (a := depthC b C) (B := B) (C := coreC b C)
  rw [← decompose b C] at h
  exact h.symm

theorem Hyp_core {b : Nat} {B C : List Nat} (h : Hyp b B C) :
    Hyp b B (coreC b C) :=
  Hyp_core_iff.mpr h

end Agent119.NeutralCenterCanonicalization

#print axioms Agent119.NeutralCenterCanonicalization.decompose
#print axioms Agent119.NeutralCenterCanonicalization.core_padC
#print axioms Agent119.NeutralCenterCanonicalization.depth_padC
#print axioms Agent119.NeutralCenterCanonicalization.core_idempotent
#print axioms Agent119.NeutralCenterCanonicalization.depth_core
#print axioms Agent119.NeutralCenterCanonicalization.core_length_le
#print axioms Agent119.NeutralCenterCanonicalization.core_irreducible
#print axioms Agent119.NeutralCenterCanonicalization.Hyp_core_iff
#print axioms Agent119.NeutralCenterCanonicalization.Hyp_core
