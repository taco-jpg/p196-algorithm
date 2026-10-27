import P196.Agent105DriverPeriodDescent.Witness
import P196.Agent105DriverPeriodDescent.ActualBridge
import P196.Agent114NeutralExteriorPadding.ExteriorPadding

/-!
# Failure of existential exterior driver-period descent

The fixed-width obstruction is lifted to arbitrary exterior widths and arbitrary
neutral suffix trim counts using Agent 114's existing padding covariance.
Per-edge center fixtures remain unchanged throughout.  No center cycle or
decimal assertion is made.
-/

namespace Agent105.DriverPeriod

open Agent120.Neutral Agent114.NeutralExteriorPadding

private theorem length_nextB_zero {b : Nat} {B C : List Nat}
    (hg : gam b B C = 0) : (nextB b B C).length = B.length := by
  simp [nextB, hg, length_DB, length_DR]

private theorem length_nextB_one {b : Nat} {B C : List Nat}
    (hg : gam b B C = 1) : (nextB b B C).length = B.length + 1 := by
  simp [nextB, hg, length_DB, length_DR]

/-- Any two-step exterior return with labels `e=g=01` has an equal-width pad.
The two actual center fixtures are preserved, and the padded trims are `0,1`.
-/
theorem common_width_two_step
    (B0 C0 B1 C1 : List Nat) (u0 u1 : Nat)
    (h0 : Hyp 6 B0 C0) (h1 : Hyp 6 B1 C1)
    (he0 : e1 6 B0 = 0) (he1 : e1 6 B1 = 1)
    (hg0 : gam 6 B0 C0 = 0) (hg1 : gam 6 B1 C1 = 1)
    (hn0 : nextB 6 B0 C0 = B1 ++ List.replicate u0 5)
    (hn1 : nextB 6 B1 C1 = B0 ++ List.replicate u1 5) :
    ∃ W0 W1 : List Nat,
      Hyp 6 W0 C0 ∧ Hyp 6 W1 C1 ∧ W0.length = W1.length ∧
      e1 6 W0 = 0 ∧ e1 6 W1 = 1 ∧
      gam 6 W0 C0 = 0 ∧ gam 6 W1 C1 = 1 ∧
      nextB 6 W0 C0 = W1 ∧ nextB 6 W1 C1 = W0 ++ [5] := by
  have hl0 : B0.length = B1.length + u0 := by
    have hh := congrArg List.length hn0
    rw [length_nextB_zero hg0] at hh
    simpa using hh
  have hl1 : B1.length + 1 = B0.length + u1 := by
    have hh := congrArg List.length hn1
    rw [length_nextB_one hg1] at hh
    simpa using hh
  let M := max B0.length B1.length + 1
  have hM0 : B0.length ≤ M := by
    have hm := Nat.le_max_left B0.length B1.length
    dsimp [M]
    omega
  have hM1 : B1.length ≤ M := by
    have hm := Nat.le_max_right B0.length B1.length
    dsimp [M]
    omega
  let a0 := M - B0.length
  let a1 := M - B1.length
  have ha0 : B0.length + a0 = M := by
    dsimp [a0]
    omega
  have ha1 : B1.length + a1 = M := by
    dsimp [a1]
    omega
  have hc0 : u0 + a0 = a1 := by omega
  have hc1 : u1 + a1 = a0 + 1 := by omega
  have hwlen : (suffixPad 6 a0 B0).length = (suffixPad 6 a1 B1).length := by
    simp only [suffixPad, List.length_append, List.length_replicate]
    omega
  have hnext0 : nextB 6 (suffixPad 6 a0 B0) C0 = suffixPad 6 a1 B1 := by
    rw [nextB_suffixPad h0 a0, hn0]
    simp only [suffixPad, List.append_assoc, List.replicate_append_replicate, hc0]
  have hnext1 : nextB 6 (suffixPad 6 a1 B1) C1 = suffixPad 6 a0 B0 ++ [5] := by
    change nextB 6 (suffixPad 6 a1 B1) C1 =
      suffixPad 6 a0 B0 ++ List.replicate 1 (6 - 1)
    rw [nextB_suffixPad h1 a1, hn1]
    simp only [suffixPad, List.append_assoc, List.replicate_append_replicate, hc1]
  exact ⟨suffixPad 6 a0 B0, suffixPad 6 a1 B1,
    hyp_suffixPad h0 a0, hyp_suffixPad h1 a1, hwlen,
    (e1_suffixPad h0 a0).trans he0, (e1_suffixPad h1 a1).trans he1,
    (gam_suffixPad h0 a0).trans hg0, (gam_suffixPad h1 a1).trans hg1,
    hnext0, hnext1⟩

/-- No two-step exterior return realizes `e=g=01`, for any widths or trims. -/
theorem no_two_step_exterior
    (B0 C0 B1 C1 : List Nat) (u0 u1 : Nat)
    (h0 : ExteriorEdge 6 B0 C0 B1 0 0 u0)
    (h1 : ExteriorEdge 6 B1 C1 B0 1 1 u1) : False := by
  obtain ⟨W0, W1, hw0, hw1, hl, he0, he1, hg0, hg1, hn0, hn1⟩ :=
    common_width_two_step B0 C0 B1 C1 u0 u1 h0.hyp h1.hyp
      h0.carry h1.carry h0.overflow h1.overflow h0.next_eq h1.next_eq
  exact no_fixed_width_two_step W0 C0 W1 C1 hw0 hw1 hl he0 he1 hg0 hg1 hn0 hn1

theorem no_two_step_representative :
    ¬ ∃ (B0 C0 B1 C1 : List Nat) (u0 u1 : Nat),
      ExteriorEdge 6 B0 C0 B1 0 0 u0 ∧ ExteriorEdge 6 B1 C1 B0 1 1 u1 := by
  rintro ⟨B0, C0, B1, C1, u0, u1, h0, h1⟩
  exact no_two_step_exterior B0 C0 B1 C1 u0 u1 h0 h1

/-- A four-state return has the two-step joint carry/overflow/trim driver `01`,
but no exterior return at all realizes one copy of its carry/overflow driver.
The negative clause allows arbitrary center fixtures, widths, and trim counts.
-/
theorem exterior_driver_period_descent_counterexample :
    (∃ B0 B1 B2 B3 : List Nat,
      List.Pairwise (fun B B' : List Nat => B ≠ B') [B0, B1, B2, B3] ∧
      ExteriorEdge 6 B0 [10] B1 0 0 0 ∧
      ExteriorEdge 6 B1 [0] B2 1 1 1 ∧
      ExteriorEdge 6 B2 [10] B3 0 0 0 ∧
      ExteriorEdge 6 B3 [0] B0 1 1 1) ∧
    (¬ ∃ (B0 C0 B1 C1 : List Nat) (u0 u1 : Nat),
      ExteriorEdge 6 B0 C0 B1 0 0 u0 ∧ ExteriorEdge 6 B1 C1 B0 1 1 u1) := by
  refine ⟨?_, no_two_step_representative⟩
  exact ⟨padded0, padded1, padded2, padded3, padded_four_distinct,
    padded_four_edges⟩

end Agent105.DriverPeriod
