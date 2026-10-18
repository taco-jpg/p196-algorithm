import P196.Drafts.Agent112TwoPhaseObstruction.ActualMapObligations

/-!
Agent #112: discharge the two explicit actual-orbit obligations recorded by
Agent #104 for Agent #4's alternating-overflow strip theorem. These theorems
concern the original `iterPairs` dynamics, not an independently postulated
symbolic strip. The alternation, common band cut and prefix-return hypotheses
are explicit; none is asserted for arbitrary return certificates or for 196.
-/
namespace Agent112.TwoPhase

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open P196.Agent4.TemporalStrip
open Agent104.TemporalStripObligations

theorem admissible_at (q : Nat → Nat) (L : Nat) (ha : Admissible L q) (t : Nat) :
    Admissible (widthAt q L t) (qAt q L t) :=
  CarryHistory.iterPairs_admissible q L t ha

/-- Two adjacent constant columns reset both directed carries at the cut.
The delayed reflected digit uses the adjacent column, not the current one. -/
theorem constant_cut_reset (q : Nat → Nat) (L i c : Nat)
    (ha : Admissible L q) (hi : 0 < i) (hiL : i < L)
    (hc : c ≤ 18) (hc9 : c ≠ 9)
    (hprev : q (i-1) = c) (hcur : q i = c) :
    carry q i = c / 10 ∧ carry q (L-i) = c / 10 ∧
      extended q L (L-i) = (c + c / 10) % 10 := by
  have hlow := carry_bounded q L ha.2.2.1 (i-1) (by omega)
  have hhigh := carry_bounded q L ha.2.2.1 (L-1-i) (by omega)
  have ilow : i = (i-1)+1 := by omega
  have ihigh : L-i = (L-1-i)+1 := by omega
  have hsym := ha.2.2.2.1 i hiL
  have hlo : carry q i = c/10 := by
    calc
      carry q i = carry q ((i-1)+1) := congrArg (carry q) ilow
      _ = (q (i-1) + carry q (i-1)) / 10 := rfl
      _ = c/10 := by
        rw [hprev]
        omega
  have hhi : carry q (L-i) = c/10 := by
    calc
      carry q (L-i) = carry q ((L-1-i)+1) := congrArg (carry q) ihigh
      _ = (q (L-1-i) + carry q (L-1-i)) / 10 := rfl
      _ = c/10 := by
        rw [← hsym, hcur]
        omega
  refine ⟨hlo, hhi, ?_⟩
  have hind : L-1-(L-i) = i-1 := by omega
  have hm : L-i < L := by omega
  have hs := ha.2.2.2.1 (L-i) hm
  rw [hind, hprev] at hs
  simp only [extended, if_pos hm, output, hs, hhi]

/-- The exact previously unproved tail contract is now discharged. -/
theorem uniform_band_tail : UniformBandTailObligation := by
  intro q L N width ha hwidth hw ht
  rcases ht with ht | ht
  · left
    intro j
    have he := constant_cut_reset (qAt q L (2*j.val)) (widthAt q L (2*j.val))
      width 6 (admissible_at q L ha _) hwidth (hw j).1 (by decide) (by decide)
      (ht j).1 (ht j).2.1
    have ho := constant_cut_reset (qAt q L (2*j.val+1)) (widthAt q L (2*j.val+1))
      width 12 (admissible_at q L ha _) hwidth (hw j).2 (by decide) (by decide)
      (ht j).2.2.1 (ht j).2.2.2
    change carry _ width = 0 ∧ carry _ (_-width) = 0 ∧
      carry _ (_-width) = 1 ∧ extended _ _ (_-width) + carry _ width = 4
    omega
  · right
    intro j
    have he := constant_cut_reset (qAt q L (2*j.val)) (widthAt q L (2*j.val))
      width 12 (admissible_at q L ha _) hwidth (hw j).1 (by decide) (by decide)
      (ht j).1 (ht j).2.1
    have ho := constant_cut_reset (qAt q L (2*j.val+1)) (widthAt q L (2*j.val+1))
      width 6 (admissible_at q L ha _) hwidth (hw j).2 (by decide) (by decide)
      (ht j).2.2.1 (ht j).2.2.2
    change carry _ width = 1 ∧ carry _ (_-width) = 1 ∧
      carry _ (_-width) = 0 ∧ extended _ _ (_-width) + carry _ width = 6
    omega

/-- Prefix return supplies the one genuinely cyclic time seam. -/
theorem cyclic_even_value (q : Nat → Nat) (L N width : Nat) (hN : 0 < N)
    (hp : ∀ i, i < width → qAt q L (2*N) i = q i)
    (j : Fin N) (i : Nat) (hi : i < width) :
    qAt q L (2*(cycleNext N hN j).val) i = qAt q L (2*j.val+2) i := by
  have hj := j.isLt
  dsimp only [cycleNext]
  by_cases hn : j.val+1 < N
  · rw [Nat.mod_eq_of_lt hn]
    congr 1
  · have hlast : j.val+1 = N := by omega
    rw [hlast, Nat.mod_self]
    have ht : 2*j.val+2 = 2*N := by omega
    rw [ht]
    exact (hp i hi).symm

/-- The original exact pair dynamics instantiate every local strip equation,
including the final-to-first temporal seam. -/
theorem actual_prefix_transport : ActualPrefixTransportObligation := by
  intro q L N width hN ha hw hg hp
  have hae : ∀ j : Fin N, Admissible (widthAt q L (2*j.val)) (qAt q L (2*j.val)) :=
    fun j => admissible_at q L ha _
  have hao : ∀ j : Fin N, Admissible (widthAt q L (2*j.val+1)) (qAt q L (2*j.val+1)) :=
    fun j => admissible_at q L ha _
  refine ⟨?_, ?_, ?_⟩
  · intro i hi j
    have hce := carry_bounded _ _ (hae j).2.2.1
    have hco := carry_bounded _ _ (hao j).2.2.1
    refine ⟨hce i (Nat.le_trans hi (hw j).1), hco i (Nat.le_trans hi (hw j).2),
      hce _ (Nat.sub_le _ _), hco _ (Nat.sub_le _ _), ?_⟩
    dsimp only [actualCut]
    unfold extended
    split
    · exact output_bounded _ _
    · have hb := hco (widthAt q L (2*j.val+1)) (by omega)
      omega
  · intro i hi j
    have hie : i < widthAt q L (2*j.val) := Nat.lt_of_lt_of_le hi (hw j).1
    have hio : i < widthAt q L (2*j.val+1) := Nat.lt_of_lt_of_le hi (hw j).2
    have he := folded_carry_transition _ _ i hie (hae j).2.2.2.1
    have ho := folded_carry_transition _ _ i hio (hao j).2.2.2.1
    have hd := folded_delay_update _ _ i hio (hao j).2.2.2.1
    have hxy := folded_emission_no_overflow _ _ i hie (hae j).2.2.2.1 (hg j).1
    have hyx := folded_emission_overflow _ _ i hio (hg j).2
    have hidxe : widthAt q L (2*j.val) - 1 - i = widthAt q L (2*j.val) - (i+1) := by omega
    have hidxo : widthAt q L (2*j.val+1) - 1 - i = widthAt q L (2*j.val+1) - (i+1) := by omega
    rw [hidxe] at he hxy
    rw [hidxo] at ho hd
    refine ⟨(hae j).2.2.1 i hie, (hao j).2.2.1 i hio, he.1, ho.1, he.2, ho.2, hd, ?_, ?_⟩
    · exact hxy
    · change qAt q L (2*(cycleNext N hN j).val) i = _
      rw [cyclic_even_value q L N width hN hp j i hi]
      exact hyx
  · intro j
    have he := (hg j).1
    have ho := (hg j).2
    dsimp only [actualCut]
    simp only [Nat.sub_zero, carry, extended, Nat.lt_irrefl, if_false, he, ho]
    decide

/-- All finite widths and temporal periods: an actual alternating-overflow
orbit cannot return its whole outside prefix while these same two columns
remain in the alternating 6/12 band. No symbolic-strip hypothesis remains. -/
theorem no_actual_alternating_prefix_return (q : Nat → Nat) (L N width : Nat)
    (hN : 0 < N) (hwidth : 0 < width) (ha : Admissible L q)
    (hw : ∀ j : Fin N, width < widthAt q L (2*j.val) ∧
      width < widthAt q L (2*j.val+1))
    (hg : ∀ j : Fin N,
      carry (qAt q L (2*j.val)) (widthAt q L (2*j.val)) = 0 ∧
      carry (qAt q L (2*j.val+1)) (widthAt q L (2*j.val+1)) = 1)
    (ht : (∀ j : Fin N,
        qAt q L (2*j.val) (width-1) = 6 ∧ qAt q L (2*j.val) width = 6 ∧
        qAt q L (2*j.val+1) (width-1) = 12 ∧ qAt q L (2*j.val+1) width = 12) ∨
      (∀ j : Fin N,
        qAt q L (2*j.val) (width-1) = 12 ∧ qAt q L (2*j.val) width = 12 ∧
        qAt q L (2*j.val+1) (width-1) = 6 ∧ qAt q L (2*j.val+1) width = 6)) :
    ¬ (∀ i, i < width → qAt q L (2*N) i = q i) := by
  intro hp
  obtain ⟨hv, hc, ho⟩ := actual_prefix_transport q L N width hN ha
    (fun j => ⟨Nat.le_of_lt (hw j).1, Nat.le_of_lt (hw j).2⟩) hg hp
  exact no_finite_alternating_six_twelve_strip N width hN
    (actualCut q L N) (actualEven q L N) (actualOdd q L N) hv hc ho
    (uniform_band_tail q L N width ha hwidth hw ht)

#print axioms admissible_at
#print axioms cyclic_even_value
#print axioms no_actual_alternating_prefix_return
#print axioms constant_cut_reset
#print axioms uniform_band_tail
#print axioms actual_prefix_transport

end Agent112.TwoPhase
