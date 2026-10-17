import Agent101NumericFibers
import IntegerInterfaces

/-!
Agent 101 compatibility between finite decimal evaluation and the existing
Agent 8 list normalizer. The carry value-preservation theorem is reused
from Agent 3's published `digitValue_normalize` interface; the existing
Agent 109 normalization theorem retains its original attribution.
-/

namespace Agent101

theorem natValue_eq_digitValue (ds : List Nat) :
    natValue ds = P196.Agent3.OverflowHorizon.digitValue ds := rfl

/-- Transport the existing all-word, all-carry value-preservation theorem. -/
theorem natValue_normalize (w : List Nat) (e : Nat) :
    natValue (Agent8.normalize w e) = natValue w + e :=
  P196.Agent3.TwoHistory.digitValue_normalize w e

theorem natValue_normalize_zero (w : List Nat) :
    natValue (Agent8.normalize w 0) = natValue w := by
  simpa only [Nat.add_zero] using natValue_normalize w 0

theorem step_eq_normalized_pair_value (ds : List Nat)
    (hd : canonicalDigits ds) :
    Lychrel196.step (natValue ds) =
      natValue (Agent8.normalize (digitPairSums ds) 0) := by
  rw [natValue_normalize_zero, step_natValue ds hd]

/-- Any enumerated predecessor has precisely this normalized first value. -/
theorem numericFiber_first_step (h : List Nat) (c : Option Nat) (n : Nat)
    (hn : n ∈ numericFiber h c) :
    Lychrel196.step n = natValue (Agent8.normalize (coefficientWord h c) 0) := by
  obtain ⟨ds, hd, hp, hv⟩ := (mem_numericFiber_digits h c n).mp hn
  rw [← hv, step_eq_normalized_pair_value ds hd, hp]

#print axioms natValue_eq_digitValue
#print axioms natValue_normalize
#print axioms natValue_normalize_zero
#print axioms step_eq_normalized_pair_value
#print axioms numericFiber_first_step

end Agent101
