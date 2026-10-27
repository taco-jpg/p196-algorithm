import P196.Drafts.D20261015Agent2ComplementarySearchAlternatingCharge.AlternatingCharge
import P196.Drafts.Agent120NeutralBandCalibration.A120Certificate

/-!
The decimal neutral-band charge reuses the existing alternating-charge algebra.
This file identifies the two normalization functions and proves invariance under
adding neutral suffixes. It supplies no cycle or Lychrel existence theorem.
-/

namespace Agent108.NeutralCharge

/-- The existing alternating charge with neutral coefficient nine. -/
def charge (B : List Nat) : Int := Agent2Exterior.alternatingCharge 9 B

/-- A120's base-ten normalization is the existing decimal normalization. -/
theorem norm10_eq_normalize (w : List Nat) (c : Nat) :
    Agent120.Neutral.norm 10 w c = Agent2Exterior.normalize w c := by
  induction w generalizing c with
  | nil => rfl
  | cons a w ih =>
      simp only [Agent120.Neutral.norm, Agent2Exterior.normalize, ih]

/-- Reuse the established alternating-sum normalization identity in A120 notation. -/
theorem norm_alternating_mod11 (w : List Nat) (c : Nat) :
    (Agent2Exterior.alternatingSum (Agent120.Neutral.norm 10 w c).1 +
      Agent2Exterior.paritySign w.length *
        ((Agent120.Neutral.norm 10 w c).2 : Int)) % 11 =
      (Agent2Exterior.alternatingSum w + (c : Int)) % 11 := by
  rw [norm10_eq_normalize]
  exact Agent2Exterior.normalize_alternating_mod11 w c

@[simp] theorem charge_nil : charge [] = 9 := by
  exact Agent2Exterior.alternatingCharge_nil 9

/-- A neutral word has the same charge as the empty exterior. -/
@[simp] theorem charge_replicate (u : Nat) :
    charge (List.replicate u 9) = 9 := by
  induction u with
  | zero => exact charge_nil
  | succ u ih =>
      simp only [List.replicate_succ, charge, Agent2Exterior.alternatingCharge_cons]
      change 18 - charge (List.replicate u 9) = 9
      omega

/-- Moving any finite neutral suffix into or out of the band preserves charge. -/
theorem charge_append_neutral (B : List Nat) (u : Nat) :
    charge (B ++ List.replicate u 9) = charge B := by
  induction B with
  | nil => simp
  | cons a B ih =>
      change Agent2Exterior.alternatingCharge 9
        ((a :: B) ++ List.replicate u 9) =
          Agent2Exterior.alternatingCharge 9 (a :: B)
      rw [List.cons_append, Agent2Exterior.alternatingCharge_cons,
        Agent2Exterior.alternatingCharge_cons]
      exact congrArg (fun z : Int => 2 * (a : Int) - z) ih

/-- Zero charge modulo eleven rules out the empty exterior. -/
theorem charge_zero_implies_nonempty (B : List Nat) (h : charge B % 11 = 0) :
    B ≠ [] := by
  intro hB
  simp [hB] at h

end Agent108.NeutralCharge
