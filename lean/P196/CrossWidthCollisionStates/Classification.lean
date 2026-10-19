import P196.CrossWidthCollisionStates.ActualTrace
import P196.CrossWidthCollisionStates.Witnesses

/-!
# Exact state catalogue for ordinary cross-width collisions

Agent #6: every actual trace lies in the eleven-state catalogue, and each
catalogue state occurs in a canonical ordinary collision of longer width
at most nine. The first transition gives exactly four possible second
coefficient pairs across all widths and three possible output residues
modulo one hundred. No converse for arbitrary graph walks or exact
collision-count formula is asserted.
-/

set_option autoImplicit false

namespace CrossWidthCollisionStates

open DecimalDigits FoldedDecimal Lychrel196 Agent105CrossWidth9df76b

/-- Every position of an actual cross-width collision belongs to the
eleven-state catalogue, including the reflected half of the trace. -/
theorem cross_width_state_productive
    {n m L K i : Nat} {d e : Nat → Nat}
    (hn : Canonical n d L) (hm : Canonical m e K)
    (hLK : L < K) (hstep : step n = step m)
    (hi : 1 ≤ i) (hiL : i ≤ L) :
    stateAt (columnSum d L) (columnSum e K) L i ∈ productive := by
  obtain ⟨hfirst, hlast, hedges⟩ :=
    cross_width_state_closed_walk hn hm hLK hstep
  exact closed_walk_mem_productive _ hn.1 hfirst hlast hedges hi hiL

/-- A state is attained somewhere in a positive ordinary cross-width
collision exactly when it belongs to the explicit catalogue. -/
theorem state_realized_iff (s : State) :
    (∃ (n m L K i : Nat) (d e : Nat → Nat),
      Canonical n d L ∧ Canonical m e K ∧ L < K ∧
      step n = step m ∧ 1 ≤ i ∧ i ≤ L ∧
      stateAt (columnSum d L) (columnSum e K) L i = s) ↔
    s ∈ productive := by
  constructor
  · rintro ⟨n, m, L, K, i, d, e, hn, hm, hLK, hstep, hi, hiL, hs⟩
    rw [← hs]
    exact cross_width_state_productive hn hm hLK hstep hi hiL
  · intro hs
    obtain ⟨n, m, L, K, i, d, e, hn, hm, hLK, hstep, hi, hiL, _, heq⟩ :=
      productive_realized_small s hs
    exact ⟨n, m, L, K, i, d, e, hn, hm, hLK, hstep, hi, hiL, heq⟩

/-- The second pair coefficients of the short and long source are
confined to four explicitly listed possibilities at every width. -/
theorem cross_width_second_coefficients
    {n m L K : Nat} {d e : Nat → Nat}
    (hn : Canonical n d L) (hm : Canonical m e K)
    (hLK : L < K) (hstep : step n = step m) :
    (columnSum d L 1, columnSum e K 1) ∈ secondPairs := by
  let f := stateAt (columnSum d L) (columnSum e K) L
  have hL := cross_width_short_length hn hm hLK hstep
  obtain ⟨hfirst, _, hedges⟩ :=
    cross_width_state_closed_walk hn hm hLK hstep
  have ht : f 2 ∈ productive :=
    cross_width_state_productive hn hm hLK hstep (by decide) hL
  have hedge : Edge initial (f 2) := by
    have he := hedges 1 (by decide) (by omega)
    rw [hfirst] at he
    exact he
  have hhigh := cross_width_high_column hn hm hLK hstep
    (i := 1) (by decide) (by omega)
  change columnSum e K 1 + 10 * (f 1).v =
    (f 1).x + (f 2).v + 9 at hhigh
  have hf1 : f 1 = initial := hfirst
  rw [hf1] at hhigh
  change columnSum e K 1 + 10 * 2 = 11 + (f 2).v + 9 at hhigh
  have hr : columnSum e K 1 = (f 2).v := by omega
  have hx : (f 2).x = columnSum d L 1 := rfl
  have hcases := initial_edge_cases ht hedge
  rw [hx, ← hr] at hcases
  exact hcases

/-- All four second-coefficient pairs occur in ordinary collisions.
Attainment is existential across widths, not at every fixed width. -/
theorem second_pair_realized_iff (a b : Nat) :
    (∃ (n m L K : Nat) (d e : Nat → Nat),
      Canonical n d L ∧ Canonical m e K ∧ L < K ∧
      step n = step m ∧ columnSum d L 1 = a ∧
      columnSum e K 1 = b) ↔ (a, b) ∈ secondPairs := by
  constructor
  · rintro ⟨n, m, L, K, d, e, hn, hm, hLK, hstep, ha, hb⟩
    rw [← ha, ← hb]
    exact cross_width_second_coefficients hn hm hLK hstep
  · exact second_pair_realized a b

private theorem value_two_low (q : Nat → Nat) (L : Nat) (hL : 2 ≤ L) :
    ∃ t, value q L = q 0 + 10 * q 1 + 100 * t := by
  refine ⟨value (fun i => q (i + 2)) (L - 2), ?_⟩
  calc
    value q L = value q ((L - 2 + 1) + 1) :=
      congrArg (value q) (by omega)
    _ = q 0 + 10 * (q 1 +
        10 * value (fun i => q ((i + 1) + 1)) (L - 2)) := by
      rw [value_shift, value_shift]
    _ = q 0 + 10 * q 1 +
        100 * value (fun i => q (i + 2)) (L - 2) := by
      simp only [Nat.add_assoc, show (1 : Nat) + 1 = 2 from rfl, Nat.mul_add]
      omega

/-- The common ordinary target ends in 01, 11 or 21 in every
different-width collision, regardless of the source widths. -/
theorem cross_width_output_mod100
    {n m L K : Nat} {d e : Nat → Nat}
    (hn : Canonical n d L) (hm : Canonical m e K)
    (hLK : L < K) (hstep : step n = step m) :
    step n % 100 = 1 ∨ step n % 100 = 11 ∨ step n % 100 = 21 := by
  have hL := cross_width_short_length hn hm hLK hstep
  have houter := (cross_width_outer hn hm hLK hstep).1
  have hsecond := cross_width_second_coefficients hn hm hLK hstep
  simp only [secondPairs, List.mem_cons, List.not_mem_nil, or_false,
    Prod.mk.injEq] at hsecond
  have hvalue := step_eq_word_value n d (columnSum d L) L hn
    (fun _ _ => rfl)
  obtain ⟨t, ht⟩ := value_two_low (columnSum d L) L hL
  rw [← hvalue, houter] at ht
  rcases hsecond with ⟨hq1, _⟩ | ⟨hq1, _⟩ | ⟨hq1, _⟩ | ⟨hq1, _⟩ <;>
    rw [hq1] at ht <;> omega

end CrossWidthCollisionStates

#print axioms CrossWidthCollisionStates.cross_width_state_productive
#print axioms CrossWidthCollisionStates.state_realized_iff
#print axioms CrossWidthCollisionStates.cross_width_second_coefficients
#print axioms CrossWidthCollisionStates.second_pair_realized_iff
#print axioms CrossWidthCollisionStates.cross_width_output_mod100
