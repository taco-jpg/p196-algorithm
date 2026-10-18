import P196.Drafts.Agent7RunPopulationRenewal.HighCarryReduction
import P196.Drafts.Agent7RunPopulationRenewal.HighReturnRank

/-! The three-column relation is necessary for actual two-step high returns.
The control is the actual carry at column `L - 2`, including widths three
and four where the observed prefixes overlap. -/

namespace Agent105.HighReturnPrefix

open DecimalDigits FoldedDecimal HighCarryReduction

def successor (q : Nat → Nat) (L : Nat) : Nat → Nat :=
  nextColumns (nextColumns q L) (L + 1)

def code (q : Nat → Nat) : Nat :=
  100 * (q 0 - 10) + 10 * (q 1 - 9) + (q 2 - 9)

def a (q : Nat → Nat) : Nat := q 0 - 9
def x (q : Nat → Nat) : Nat := q 0 + q 1 - 18
def y (q : Nat → Nat) : Nat := q 1 + q 2 - 18
def lo (q : Nat → Nat) : Nat := x q / 10
def control (q : Nat → Nat) (L : Nat) : Nat :=
  carry (nextColumns q L) (L - 2)
def v (q : Nat → Nat) (L : Nat) : Nat := (y q + control q L) / 10
def z (q : Nat → Nat) (L : Nat) : Nat := (x q + v q L) / 10

theorem successor_actual (q : Nat → Nat) (L : Nat) (hL : 0 < L)
    (hq : HighCarryWord q L) :
    successor q L = nextColumns (nextColumns q L) (nextWidth q L) := by
  rw [HighCarryReduction.nextWidth_eq q L hL hq]
  rfl

theorem first_admissible (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hq : HighCarryWord q L) :
    Admissible (L + 1) (nextColumns q L) := by
  have h := NormalizationBridge.admissible_next q L ha
  rwa [HighCarryReduction.nextWidth_eq q L ha.1 hq] at h

theorem first_prefix (q : Nat → Nat) (L : Nat) (hL : 3 ≤ L)
    (ha : Admissible L q) (hq : HighCarryWord q L) :
    nextColumns q L 0 = a q ∧ nextColumns q L 1 = x q ∧
      nextColumns q L 2 = y q ∧ nextColumns q L L = a q := by
  refine ⟨nextColumns_zero q L (by omega) hq, ?_, ?_,
    nextColumns_last q L (by omega) hq⟩
  · simpa [x] using nextColumns_internal q L 1 hq ha.2.2.2.1 (by omega) (by omega)
  · simpa [y] using nextColumns_internal q L 2 hq ha.2.2.2.1 (by omega) (by omega)

theorem actual_control_lt_two (q : Nat → Nat) (L : Nat)
    (ha : Admissible L q) (hq : HighCarryWord q L) : control q L < 2 := by
  have hp := first_admissible q L ha hq
  have hc := carry_bounded (nextColumns q L) (L + 1) hp.2.2.1 (L - 2) (by omega)
  exact Nat.lt_succ_of_le hc

theorem prefix_carries (q : Nat → Nat) (L : Nat) (hL : 3 ≤ L)
    (ha : Admissible L q) (hq : HighCarryWord q L) :
    carry (nextColumns q L) 1 = 0 ∧
      carry (nextColumns q L) 2 = lo q ∧
      carry (nextColumns q L) (L - 1) = v q L ∧
      carry (nextColumns q L) L = z q L := by
  let p := nextColumns q L
  have hp := first_admissible q L ha hq
  obtain ⟨hp0, hp1, hp2, _⟩ := first_prefix q L hL ha hq
  have ha9 : a q < 10 := by
    have hb := hq.1 0 (by omega)
    simp only [a]
    omega
  have hc1 : carry p 1 = 0 := by
    simp only [carry, Nat.add_zero, p, hp0]
    exact Nat.div_eq_of_lt ha9
  have hc2 : carry p 2 = lo q := by
    change (p 1 + carry p 1) / 10 = lo q
    rw [hc1, Nat.add_zero]
    exact congrArg (fun n => n / 10) hp1
  have hm2 : p (L - 2) = y q := by
    have hs := hp.2.2.2.1 2 (by omega)
    have he : L + 1 - 1 - 2 = L - 2 := by omega
    rw [he] at hs
    exact hs.symm.trans hp2
  have hm1 : p (L - 1) = x q := by
    have hs := hp.2.2.2.1 1 (by omega)
    have he : L + 1 - 1 - 1 = L - 1 := by omega
    rw [he] at hs
    exact hs.symm.trans hp1
  have hcv : carry p (L - 1) = v q L := by
    have he : L - 1 = (L - 2) + 1 := by omega
    rw [he, carry, hm2]
    rfl
  have hcz : carry p L = z q L := by
    have he : L = (L - 1) + 1 := by omega
    calc
      carry p L = (p (L - 1) + carry p (L - 1)) / 10 := by
        exact (congrArg (carry p) he).trans (by rfl)
      _ = z q L := by rw [hm1, hcv]; rfl
  exact ⟨hc1, hc2, hcv, hcz⟩

theorem actual_no_overflow_constraint (q : Nat → Nat) (L : Nat) (hL : 3 ≤ L)
    (ha : Admissible L q) (hq : HighCarryWord q L)
    (hc : carry (nextColumns q L) (L + 1) = 0) : a q + z q L < 10 := by
  have hpL := (first_prefix q L hL ha hq).2.2.2
  have hcz := (prefix_carries q L hL ha hq).2.2.2
  have he : (a q + z q L) / 10 = 0 := by
    simpa only [carry, hpL, hcz] using hc
  omega

theorem actual_prefix_formulas (q : Nat → Nat) (L : Nat) (hL : 3 ≤ L)
    (ha : Admissible L q) (hq : HighCarryWord q L)
    (hc : carry (nextColumns q L) (L + 1) = 0) :
    successor q L 0 = 2 * a q + z q L ∧
      successor q L 1 = x q % 10 + (x q + v q L) % 10 ∧
      successor q L 2 = (y q + lo q) % 10 + (y q + control q L) % 10 := by
  have hp := first_admissible q L ha hq
  obtain ⟨hp0, hp1, hp2, _⟩ := first_prefix q L hL ha hq
  obtain ⟨hc1, hc2, hcv, hcz⟩ := prefix_carries q L hL ha hq
  have he0 : L + 1 - 1 - 0 = L := by omega
  have he1 : L + 1 - 1 - 1 = L - 1 := by omega
  have he2 : L + 1 - 1 - 2 = L - 2 := by omega
  have hsum := actual_no_overflow_constraint q L hL ha hq hc
  have ha9 : a q < 10 := by omega
  refine ⟨?_, ?_, ?_⟩
  · unfold successor
    rw [folded_emission_no_overflow _ _ 0 (by omega) hp.2.2.2.1 hc]
    rw [hp0, carry, Nat.add_zero, he0, hcz,
      Nat.mod_eq_of_lt ha9, Nat.mod_eq_of_lt hsum]
    omega
  · unfold successor
    rw [folded_emission_no_overflow _ _ 1 (by omega) hp.2.2.2.1 hc]
    rw [hp1, hc1, Nat.add_zero, he1, hcv]
  · unfold successor
    rw [folded_emission_no_overflow _ _ 2 (by omega) hp.2.2.2.1 hc]
    rw [hp2, hc2, he2]
    rfl

theorem code_properties (q : Nat → Nat) (L : Nat) (hL : 3 ≤ L)
    (hq : HighCarryWord q L) :
    code q < 900 ∧ code q / 100 + 10 = q 0 ∧
      code q / 10 % 10 + 9 = q 1 ∧ code q % 10 + 9 = q 2 := by
  have h0 := hq.1 0 (by omega)
  have h1 := hq.1 1 (by omega)
  have h2 := hq.1 2 (by omega)
  have hout := hq.2
  unfold code
  omega

/-- Every actual high return gives an edge of the checked finite relation.
The no-overflow hypothesis is discharged separately by the neutral-exterior
obstruction. No graph edge or rank decrease is assumed here. -/
theorem actual_prefix_edge (q : Nat → Nat) (L : Nat) (hL : 3 ≤ L)
    (ha : Admissible L q) (hq : HighCarryWord q L)
    (hc : carry (nextColumns q L) (L + 1) = 0)
    (hret : HighCarryWord (successor q L) (L + 1)) :
    HighReturnRank.next (code q) (control q L) = some (code (successor q L)) := by
  obtain ⟨_, hA, hB, hC⟩ := code_properties q L hL hq
  obtain ⟨hU, hV, hW⟩ := actual_prefix_formulas q L hL ha hq hc
  have hno := actual_no_overflow_constraint q L hL ha hq hc
  have hu := hret.1 0 (by omega)
  have hv := hret.1 1 (by omega)
  have hw := hret.1 2 (by omega)
  have hout := hret.2
  have hcond : a q + z q L < 10 ∧ 10 ≤ 2 * a q + z q L ∧
      2 * a q + z q L ≤ 18 ∧
      9 ≤ x q % 10 + (x q + v q L) % 10 ∧
      x q % 10 + (x q + v q L) % 10 ≤ 18 ∧
      9 ≤ (y q + lo q) % 10 + (y q + control q L) % 10 ∧
      (y q + lo q) % 10 + (y q + control q L) % 10 ≤ 18 := by
    omega
  unfold HighReturnRank.next
  rw [hA, hB, hC]
  change (if a q + z q L < 10 ∧ 10 ≤ 2 * a q + z q L ∧
      2 * a q + z q L ≤ 18 ∧
      9 ≤ x q % 10 + (x q + v q L) % 10 ∧
      x q % 10 + (x q + v q L) % 10 ≤ 18 ∧
      9 ≤ (y q + lo q) % 10 + (y q + control q L) % 10 ∧
      (y q + lo q) % 10 + (y q + control q L) % 10 ≤ 18
    then some (100 * (2 * a q + z q L - 10) +
      10 * (x q % 10 + (x q + v q L) % 10 - 9) +
      ((y q + lo q) % 10 + (y q + control q L) % 10) - 9)
    else none) = some (code (successor q L))
  rw [if_pos hcond]
  unfold code
  rw [hU, hV, hW]
  congr 1
  omega

theorem actual_prefix_rank_decreases (q : Nat → Nat) (L : Nat) (hL : 3 ≤ L)
    (ha : Admissible L q) (hq : HighCarryWord q L)
    (hc : carry (nextColumns q L) (L + 1) = 0)
    (hret : HighCarryWord (successor q L) (L + 1)) :
    HighReturnRank.rank (code (successor q L)) < HighReturnRank.rank (code q) := by
  exact (HighReturnRank.edge_decreases (code q) (control q L)
    (code (successor q L)) (code_properties q L hL hq).1
    (actual_control_lt_two q L ha hq) (actual_prefix_edge q L hL ha hq hc hret)).2

#print axioms actual_prefix_formulas
#print axioms actual_control_lt_two
#print axioms actual_prefix_edge
#print axioms actual_prefix_rank_decreases

end Agent105.HighReturnPrefix
