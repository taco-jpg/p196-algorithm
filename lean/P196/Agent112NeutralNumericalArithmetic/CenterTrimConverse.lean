import P196.Agent112NeutralNumericalArithmetic.CenterPeel

/-!
# Literal center recovery from a prescribed signed quotient

Agent 112's PR349 和 PR368 already give the paper argument that divisibility
by a base power forces removable neutral pairs in a bounded symmetric word.
This file iterates the one-pair result to arbitrary prescribed natural trim
counts. It includes zero signed values, empty cores, 和 nonmaximal trims.

The recovered core is unique by literal list cancellation. Agent 119 retains
the forward padding-value identity 和 the accepted-edge/chain arithmetic;
no numerical-cycle realization or new Lychrel result is asserted here.
-/

namespace Agent112.NeutralNumericalArithmetic

/-- A prescribed integral signed quotient determines an actual removal of
that many neutral pairs, retaining all coefficient bounds 和 symmetry. -/
theorem exists_center_trim_of_signedValue (b : Nat) (hb : 2 ≤ b) (C : List Nat)
    (hbound : ∀ d ∈ C, d ≤ 2 * (b - 1)) (hsym : C.reverse = C)
    (v : Nat) (hlen : 2 * v ≤ C.length) (z : Int)
    (hz : signedValue b C = ((b ^ v : Nat) : Int) * z) :
    ∃ D, C = List.replicate v (b - 1) ++ D ++ List.replicate v (b - 1) ∧
      D.length + 2 * v = C.length ∧
      (∀ d ∈ D, d ≤ 2 * (b - 1)) ∧ D.reverse = D ∧ signedValue b D = z := by
  induction v generalizing C z with
  | zero =>
      refine ⟨C, ?_, ?_, hbound, hsym, ?_⟩
      · simp
      · simp
      · simpa only [Nat.pow_zero, Int.ofNat_one, Int.one_mul] using hz
  | succ v ih =>
      have hzpeel : signedValue b C = (b : Int) * (((b ^ v : Nat) : Int) * z) := by
        simpa only [Nat.pow_succ, Int.ofNat_mul, Int.mul_assoc,
          Int.mul_comm, Int.mul_left_comm] using hz
      obtain ⟨D, hC, hlengthD, hboundD, hsymD, hzD⟩ :=
        exists_center_peel_of_signedValue b hb C hbound hsym (by omega)
          (((b ^ v : Nat) : Int) * z) hzpeel
      obtain ⟨E, hD, hlengthE, hboundE, hsymE, hzE⟩ :=
        ih D hboundD hsymD (by omega) z hzD
      refine ⟨E, ?_, by omega, hboundE, hsymE, hzE⟩
      rw [hC, hD]
      have hrep : List.replicate v (b - 1) ++ [b - 1] =
          (b - 1) :: List.replicate v (b - 1) := by
        rw [← List.replicate_succ', List.replicate_succ]
      simp only [List.replicate_succ, List.cons_append, List.append_assoc]
      rw [hrep]

/-- Two literal removals of the same prescribed number of neutral pairs
from the same source have the same core. No arithmetic hypotheses are needed. -/
theorem center_trim_unique (b v : Nat) (C D E : List Nat)
    (hD : C = List.replicate v (b - 1) ++ D ++ List.replicate v (b - 1))
    (hE : C = List.replicate v (b - 1) ++ E ++ List.replicate v (b - 1)) : D = E := by
  exact List.append_cancel_left (List.append_cancel_right (hD.symm.trans hE))

end Agent112.NeutralNumericalArithmetic
