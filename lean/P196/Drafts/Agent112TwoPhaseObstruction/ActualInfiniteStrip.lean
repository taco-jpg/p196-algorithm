import P196.Drafts.Agent112TwoPhaseObstruction.ActualStrip
import P196.Core.AlternatingScalarBoundary

/-!
Agent #112: an actual-arithmetic bridge to Agent #9's nonperiodic spatial
obstruction. The time traces below are genuine iterates of `nextColumns` with
each step's actual width. No temporal period or returned prefix is assumed.
-/
namespace Agent112.TwoPhase

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open Agent104.TemporalStripObligations
open Agent9.AlternatingScalarBoundary

set_option maxHeartbeats 4000000

/-- Exact directed carries and delayed digit, sampled at two successive
ordinary times. The subtraction in `z` is integer subtraction. -/
def orbitSlot (q : Nat → Nat) (L i j : Nat) : Slot where
  a := carry (qAt q L (2*j)) i
  b := carry (qAt q L (2*j+1)) i
  c := carry (qAt q L (2*j)) (widthAt q L (2*j)-i)
  z := (extended (qAt q L (2*j+1)) (widthAt q L (2*j+1))
    (widthAt q L (2*j+1)-i) : Int) -
    (carry (qAt q L (2*j+1)) (widthAt q L (2*j+1)-i) : Int)

/-- The physical outside cut is distinct from both scalar cuts and their
exceptional predecessors. It is not the separately derived 8/17 cut. -/
def physicalOutside : Slot := ⟨0,0,0,0⟩

theorem orbit_slot_valid (q : Nat → Nat) (L i j : Nat) (ha : Admissible L q)
    (he : i ≤ widthAt q L (2*j)) (ho : i ≤ widthAt q L (2*j+1)) :
    Valid (orbitSlot q L i j) := by
  have hae := admissible_at q L ha (2*j)
  have hao := admissible_at q L ha (2*j+1)
  have hle := carry_bounded _ _ hae.2.2.1 i he
  have hlo := carry_bounded _ _ hao.2.2.1 i ho
  have hhe := carry_bounded _ _ hae.2.2.1 (widthAt q L (2*j)-i) (Nat.sub_le _ _)
  have hho := carry_bounded _ _ hao.2.2.1 (widthAt q L (2*j+1)-i) (Nat.sub_le _ _)
  have hd : extended (qAt q L (2*j+1)) (widthAt q L (2*j+1))
      (widthAt q L (2*j+1)-i) ≤ 9 := by
    unfold extended
    split
    · have h := output_bounded (qAt q L (2*j+1)) (widthAt q L (2*j+1)-i)
      omega
    · have h := carry_bounded _ _ hao.2.2.1 (widthAt q L (2*j+1)) (by omega)
      omega
  dsimp only [Valid, orbitSlot]
  omega

/-- Every actual consecutive nonoverflow/overflow pair satisfies every field
of the exact N/O tile relation, including both delayed-digit constraints. -/
theorem actual_tile (q : Nat → Nat) (L i j : Nat) (ha : Admissible L q)
    (he : i < widthAt q L (2*j)) (ho : i < widthAt q L (2*j+1))
    (hge : carry (qAt q L (2*j)) (widthAt q L (2*j)) = 0)
    (hgo : carry (qAt q L (2*j+1)) (widthAt q L (2*j+1)) = 1) :
    Tile (orbitSlot q L i j) (orbitSlot q L (i+1) j)
      (qAt q L (2*j) i) (qAt q L (2*j+1) i)
      (carry (qAt q L (2*j+1)) (widthAt q L (2*j+1)-i))
      (qAt q L (2*(j+1)) i) := by
  have hae := admissible_at q L ha (2*j)
  have hao := admissible_at q L ha (2*j+1)
  have ce := folded_carry_transition _ _ i he hae.2.2.2.1
  have co := folded_carry_transition _ _ i ho hao.2.2.2.1
  have do' := folded_delay_update _ _ i ho hao.2.2.2.1
  have emitE := folded_emission_no_overflow _ _ i he hae.2.2.2.1 hge
  have emitO := folded_emission_overflow _ _ i ho hgo
  have idxE : widthAt q L (2*j)-1-i = widthAt q L (2*j)-(i+1) := by omega
  have idxO : widthAt q L (2*j+1)-1-i = widthAt q L (2*j+1)-(i+1) := by omega
  rw [idxE] at ce emitE
  rw [idxO] at co do'
  have be := hae.2.2.1 i he
  have bo := hao.2.2.1 i ho
  have bcarry := carry_bounded _ _ hao.2.2.1 (widthAt q L (2*j+1)-i) (Nat.sub_le _ _)
  have bin := carry_bounded _ _ hao.2.2.1 (widthAt q L (2*j+1)-(i+1)) (Nat.sub_le _ _)
  have outValid := orbit_slot_valid q L i j ha (by omega) (by omega)
  have inValid := orbit_slot_valid q L (i+1) j ha (by omega) (by omega)
  have nextEq : qAt q L (2*(j+1)) i =
      nextColumns (qAt q L (2*j+1)) (widthAt q L (2*j+1)) i := by
    have ht : 2*(j+1) = (2*j+1)+1 := by omega
    rw [ht]
    rfl
  have bdelay : extended (qAt q L (2*j+1)) (widthAt q L (2*j+1))
      (widthAt q L (2*j+1)-i) ≤ 9 := by
    unfold extended
    split
    · have h := output_bounded (qAt q L (2*j+1)) (widthAt q L (2*j+1)-i)
      omega
    · have h := carry_bounded _ _ hao.2.2.1 (widthAt q L (2*j+1)) (by omega)
      omega
  refine ⟨outValid, inValid, by omega, by omega, by omega, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  all_goals dsimp only [orbitSlot]
  · omega
  · omega
  · omega
  · omega
  · change _ = (nextColumns (qAt q L (2*j)) (widthAt q L (2*j)) i : Int)
    omega
  · omega
  · omega
  · rw [nextEq]
    omega
  · omega

theorem actual_spatial_step (q : Nat → Nat) (L width i : Nat) (ha : Admissible L q)
    (hi : i < width)
    (hw : ∀ j, width ≤ widthAt q L (2*j) ∧ width ≤ widthAt q L (2*j+1))
    (hg : ∀ j, carry (qAt q L (2*j)) (widthAt q L (2*j)) = 0 ∧
      carry (qAt q L (2*j+1)) (widthAt q L (2*j+1)) = 1) :
    Step (orbitSlot q L i) (orbitSlot q L (i+1)) := by
  refine ⟨(fun j => qAt q L (2*j) i), (fun j => qAt q L (2*j+1) i),
    (fun j => carry (qAt q L (2*j+1)) (widthAt q L (2*j+1)-i)), ?_⟩
  intro j
  exact actual_tile q L i j ha (Nat.lt_of_lt_of_le hi (hw j).1)
    (Nat.lt_of_lt_of_le hi (hw j).2) (hg j).1 (hg j).2

theorem actual_outside (q : Nat → Nat) (L : Nat)
    (hg : ∀ j, carry (qAt q L (2*j)) (widthAt q L (2*j)) = 0 ∧
      carry (qAt q L (2*j+1)) (widthAt q L (2*j+1)) = 1) :
    orbitSlot q L 0 = constant physicalOutside := by
  funext j
  apply slot_ext <;> simp only [orbitSlot, constant, physicalOutside, carry,
    Nat.sub_zero, extended, Nat.lt_irrefl, if_false, (hg j).1, (hg j).2] <;> decide

/-- Two actual adjacent constant columns provide the scalar cut; no infinite
symbolic realization hypothesis is introduced. -/
theorem actual_six_tail (q : Nat → Nat) (L width : Nat) (ha : Admissible L q)
    (hp : 0 < width)
    (hw : ∀ j, width < widthAt q L (2*j) ∧ width < widthAt q L (2*j+1))
    (ht : ∀ j, qAt q L (2*j) (width-1) = 6 ∧ qAt q L (2*j) width = 6 ∧
      qAt q L (2*j+1) (width-1) = 12 ∧ qAt q L (2*j+1) width = 12) :
    orbitSlot q L width = constant six := by
  funext j
  have he := constant_cut_reset _ _ width 6 (admissible_at q L ha _) hp (hw j).1
    (by decide) (by decide) (ht j).1 (ht j).2.1
  have ho := constant_cut_reset _ _ width 12 (admissible_at q L ha _) hp (hw j).2
    (by decide) (by decide) (ht j).2.2.1 (ht j).2.2.2
  apply slot_ext <;> dsimp only [orbitSlot, constant, six] <;> omega

theorem actual_twelve_tail (q : Nat → Nat) (L width : Nat) (ha : Admissible L q)
    (hp : 0 < width)
    (hw : ∀ j, width < widthAt q L (2*j) ∧ width < widthAt q L (2*j+1))
    (ht : ∀ j, qAt q L (2*j) (width-1) = 12 ∧ qAt q L (2*j) width = 12 ∧
      qAt q L (2*j+1) (width-1) = 6 ∧ qAt q L (2*j+1) width = 6) :
    orbitSlot q L width = constant twelve := by
  funext j
  have he := constant_cut_reset _ _ width 12 (admissible_at q L ha _) hp (hw j).1
    (by decide) (by decide) (ht j).1 (ht j).2.1
  have ho := constant_cut_reset _ _ width 6 (admissible_at q L ha _) hp (hw j).2
    (by decide) (by decide) (ht j).2.2.1 (ht j).2.2.2
  apply slot_ext <;> dsimp only [orbitSlot, constant, twelve] <;> omega

/-- No actual orbit with indefinitely alternating 0/1 overflows can retain
an alternating 6/12 band at one fixed positive finite cut. This does not
assume temporal periodicity, an exterior return, or a repeated prefix. -/
theorem no_actual_persistent_alternating_band (q : Nat → Nat) (L width : Nat)
    (ha : Admissible L q) (hp : 0 < width)
    (hw : ∀ j, width < widthAt q L (2*j) ∧ width < widthAt q L (2*j+1))
    (hg : ∀ j, carry (qAt q L (2*j)) (widthAt q L (2*j)) = 0 ∧
      carry (qAt q L (2*j+1)) (widthAt q L (2*j+1)) = 1)
    (ht : (∀ j, qAt q L (2*j) (width-1) = 6 ∧ qAt q L (2*j) width = 6 ∧
        qAt q L (2*j+1) (width-1) = 12 ∧ qAt q L (2*j+1) width = 12) ∨
      (∀ j, qAt q L (2*j) (width-1) = 12 ∧ qAt q L (2*j) width = 12 ∧
        qAt q L (2*j+1) (width-1) = 6 ∧ qAt q L (2*j+1) width = 6)) : False := by
  have path := fun i hi => actual_spatial_step q L width i ha hi
    (fun j => ⟨Nat.le_of_lt (hw j).1, Nat.le_of_lt (hw j).2⟩) hg
  have hout := actual_outside q L hg
  rcases ht with ht | ht
  · exact no_finite_path six sixBad physicalOutside (by decide)
      predecessor_six viable_predecessor_six width (orbitSlot q L) hout
      (actual_six_tail q L width ha hp hw ht) path
  · exact no_finite_path twelve twelveBad physicalOutside (by decide)
      predecessor_twelve viable_predecessor_twelve width (orbitSlot q L) hout
      (actual_twelve_tail q L width ha hp hw ht) path

#print axioms orbit_slot_valid
#print axioms actual_tile
#print axioms actual_spatial_step
#print axioms actual_outside
#print axioms actual_six_tail
#print axioms actual_twelve_tail
#print axioms no_actual_persistent_alternating_band

end Agent112.TwoPhase
