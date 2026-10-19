import P196.CrossWidthCollisionStates.StateSpace
import P196.Agent105InverseBoundaries.Agent105CrossWidth9df76b

/-!
The actual carries of two ordinary reverse-and-add sources of different
widths form a closed walk in the finite collision state space.

The bridge uses equality of the normalized output digits. All carry
differences stay in their natural-number encoding, so the local identities
retain every term without signed subtraction.
-/

set_option autoImplicit false

namespace CrossWidthCollisionStates

open Lychrel196 DecimalDigits FoldedDecimal
open Agent105WidthSupport9df76b Agent105CrossWidth9df76b

private theorem collision_data
    {n m L K : Nat} {d e : Nat → Nat}
    (hn : Canonical n d L) (hm : Canonical m e K)
    (hLK : L < K) (hstep : step n = step m) :
    K = L + 1 ∧ columnSum d L 0 = 11 ∧
      carry (columnSum d L) 1 = 1 ∧ carry (columnSum e K) 1 = 0 ∧
      carry (columnSum d L) L = 1 ∧ carry (columnSum e K) L = 0 ∧
      ∀ i, i < L → output (columnSum d L) i = output (columnSum e K) i := by
  have houter := cross_width_outer hn hm hLK hstep
  obtain ⟨hK, hcq, hcr⟩ := cross_width_carries hn hm hLK hstep
  subst K
  let q := columnSum d L
  let r := columnSum e (L + 1)
  have hq0 : q 0 = 11 := houter.1
  have hr0 : r 0 = 1 := houter.2
  have hnout := canonical_next_overflow n d L hn hcq
  have hmout := canonical_next_no_overflow m e (L + 1) hm hcr
  have hmout' : Canonical (step n) (output r) (L + 1) := by
    rw [hstep]
    exact hmout
  have hext : ∀ i, i < L + 1 → extended q L i = output r i :=
    canonical_digits_unique hnout hmout'
  have hlead : output r L = 1 := by
    have h := hext L (by omega)
    simpa [extended, q, hcq] using h.symm
  have hrsym : r 0 = r L := by
    simpa [r] using columnSum_symmetric e (L + 1) 0 (by omega)
  have hrL : r L = 1 := hrsym.symm.trans hr0
  have hlast := column_equation r L
  have hrlast : carry r (L + 1) = 0 := hcr
  have hrcL : carry r L = 0 := by omega
  have hqc1 : carry q 1 = 1 := by simp [carry, hq0]
  have hrc1 : carry r 1 = 0 := by simp [carry, hr0]
  refine ⟨rfl, hq0, hqc1, hrc1, hcq, hrcL, ?_⟩
  intro i hi
  have h := hext i (by omega)
  simpa [extended, hi] using h

private theorem stateAt_bounded
    (q r : Nat → Nat) (L i : Nat)
    (hq : ∀ j, j < L → q j ≤ 18) (hi : 1 ≤ i) (hiL : i ≤ L) :
    (stateAt q r L i).x ≤ 18 ∧
      (stateAt q r L i).u ≤ 2 ∧ (stateAt q r L i).v ≤ 2 := by
  have hx := hq (i - 1) (by omega)
  have hu := carry_bounded q L hq i hiL
  have hv := carry_bounded q L hq (L - i + 1) (by omega)
  dsimp only [stateAt]
  omega

private theorem collision_columns
    {n m L K : Nat} {d e : Nat → Nat}
    (hn : Canonical n d L) (hm : Canonical m e K)
    (hK : K = L + 1)
    (hout : ∀ j, j < L →
      output (columnSum d L) j = output (columnSum e K) j)
    {i : Nat} (hi : 1 ≤ i) (hiL : i < L) :
    columnSum d L i + (stateAt (columnSum d L) (columnSum e K) L i).u + 9 =
        columnSum e K i +
          10 * (stateAt (columnSum d L) (columnSum e K) L (i + 1)).u ∧
      columnSum e K i +
          10 * (stateAt (columnSum d L) (columnSum e K) L i).v =
        (stateAt (columnSum d L) (columnSum e K) L i).x +
          (stateAt (columnSum d L) (columnSum e K) L (i + 1)).v + 9 := by
  subst K
  let q := columnSum d L
  let r := columnSum e (L + 1)
  have hqb := carry_bounded q L (columnSum_bounded d L hn.2.1)
  have hrb := carry_bounded r (L + 1) (columnSum_bounded e (L + 1) hm.2.1)
  constructor
  · have hqcur := hqb i (by omega)
    have hqnext := hqb (i + 1) (by omega)
    have hrcur := hrb i (by omega)
    have hrnext := hrb (i + 1) (by omega)
    have hqcol := column_equation q i
    have hrcol := column_equation r i
    have heq : output q i = output r i := hout i hiL
    change q i + (carry q i + 1 - carry r i) + 9 =
      r i + 10 * (carry q (i + 1) + 1 - carry r (i + 1))
    omega
  · have hj : L - i < L := by omega
    have hqcur := hqb (L - i) (by omega)
    have hqnext := hqb (L - i + 1) (by omega)
    have hrcur := hrb (L - i) (by omega)
    have hrnext := hrb (L - i + 1) (by omega)
    have hqcol := column_equation q (L - i)
    have hrcol := column_equation r (L - i)
    have heq : output q (L - i) = output r (L - i) := hout (L - i) hj
    have hqindex : L - 1 - (L - i) = i - 1 := by omega
    have hrindex : (L + 1) - 1 - (L - i) = i := by omega
    have hqsym : q (L - i) = q (i - 1) := by
      simpa only [hqindex] using columnSum_symmetric d L (L - i) hj
    have hrsym : r (L - i) = r i := by
      simpa only [hrindex] using
        columnSum_symmetric e (L + 1) (L - i) (by omega)
    rw [hqsym] at hqcol
    rw [hrsym] at hrcol
    have hnextindex : L - (i + 1) + 1 = L - i := by omega
    change r i + 10 * (carry q (L - i + 1) + 1 - carry r (L - i + 1)) =
      q (i - 1) +
        (carry q (L - (i + 1) + 1) + 1 - carry r (L - (i + 1) + 1)) + 9
    rw [hnextindex]
    omega

/-- The reflected column determines the longer source coefficient from
two consecutive actual states. -/
theorem cross_width_high_column
    {n m L K : Nat} {d e : Nat → Nat}
    (hn : Canonical n d L) (hm : Canonical m e K)
    (hLK : L < K) (hstep : step n = step m)
    {i : Nat} (hi : 1 ≤ i) (hiL : i < L) :
    columnSum e K i +
        10 * (stateAt (columnSum d L) (columnSum e K) L i).v =
      (stateAt (columnSum d L) (columnSum e K) L i).x +
        (stateAt (columnSum d L) (columnSum e K) L (i + 1)).v + 9 := by
  obtain ⟨hK, _, _, _, _, _, hout⟩ := collision_data hn hm hLK hstep
  exact (collision_columns hn hm hK hout hi hiL).2

/-- Every different-width ordinary collision gives a closed walk from
the initial state, with one transition at each inner source boundary. -/
theorem cross_width_state_closed_walk
    {n m L K : Nat} {d e : Nat → Nat}
    (hn : Canonical n d L) (hm : Canonical m e K)
    (hLK : L < K) (hstep : step n = step m) :
    let f := stateAt (columnSum d L) (columnSum e K) L
    f 1 = initial ∧ f L = initial ∧
      ∀ i, 1 ≤ i → i < L → Edge (f i) (f (i + 1)) := by
  obtain ⟨hK, hq0, hqc1, hrc1, hqcL, hrcL, hout⟩ :=
    collision_data hn hm hLK hstep
  have hL := hn.1
  have hfirstindex : L - 1 + 1 = L := by omega
  have hqlast : columnSum d L (L - 1) = 11 := by
    have h := columnSum_symmetric d L 0 hL
    simpa only [Nat.sub_zero, hq0] using h.symm
  dsimp only
  refine ⟨?_, ?_, ?_⟩
  · simp [stateAt, initial, hfirstindex, hq0, hqc1, hrc1, hqcL, hrcL]
  · simp [stateAt, initial, hqlast, hqc1, hrc1, hqcL, hrcL]
  · intro i hi hiL
    have hb := stateAt_bounded (columnSum d L) (columnSum e K) L i
      (columnSum_bounded d L hn.2.1) hi (by omega)
    have hbnext := stateAt_bounded (columnSum d L) (columnSum e K) L (i + 1)
      (columnSum_bounded d L hn.2.1) (by omega) (by omega)
    obtain ⟨hlow, hhigh⟩ := collision_columns hn hm hK hout hi hiL
    have hrbound := columnSum_bounded e K hm.2.1 i (by omega)
    have hxnext :
        (stateAt (columnSum d L) (columnSum e K) L (i + 1)).x =
          columnSum d L i := by simp [stateAt]
    refine ⟨hb.1, hb.2.1, hb.2.2, hbnext.1, hbnext.2.1, hbnext.2.2,
      ?_, ?_, ?_⟩
    · omega
    · omega
    · omega

#print axioms cross_width_high_column
#print axioms cross_width_state_closed_walk

end CrossWidthCollisionStates
