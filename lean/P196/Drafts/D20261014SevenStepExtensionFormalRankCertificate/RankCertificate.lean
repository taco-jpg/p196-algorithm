import P196.Drafts.D20261014SevenStepExtensionFormalNoFourReturns.RankChecks

/-!
Kernel-checked finite descent for all 48,013 vertices and both Boolean
inputs. The hypotheses are precisely the next phase's three-coordinate
prefix and this phase's overflow. Every transition is recomputed using
SixPrefix.step; the candidate graph's listed edges are never assumed.
-/

namespace RankCertificate

set_option maxHeartbeats 0
set_option maxRecDepth 100000

private theorem split19 (n : Nat) (hn : n < 19) :
    n = 0 ∨ n = 1 ∨ n = 2 ∨ n = 3 ∨ n = 4 ∨ n = 5 ∨ n = 6 ∨ n = 7 ∨ n = 8 ∨ n = 9 ∨ n = 10 ∨ n = 11 ∨ n = 12 ∨ n = 13 ∨ n = 14 ∨ n = 15 ∨ n = 16 ∨ n = 17 ∨ n = 18 := by omega

theorem rank_decreases (phase a b c : Nat) (control : Bool)
    (hphase : phase < 7) (ha : a < 19) (hb : b < 19) (hc : c < 19)
    (hfront : first3 (SixPrefix.step (assemble phase a b c) control).1 =
      phasePrefix ((phase + 1) % 7))
    (hoverflow : (SixPrefix.step (assemble phase a b c) control).2 =
      phaseOverflow phase) :
    rank ((phase + 1) % 7)
      (SixPrefix.step (assemble phase a b c) control).1.x3
      (SixPrefix.step (assemble phase a b c) control).1.x4
      (SixPrefix.step (assemble phase a b c) control).1.x5 < rank phase a b c := by
  have hphaseCases : phase = 0 ∨ phase = 1 ∨ phase = 2 ∨ phase = 3 ∨ phase = 4 ∨ phase = 5 ∨ phase = 6 := by omega
  rcases hphaseCases with rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · rcases split19 a ha with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · exact check_0_0 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_1 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_2 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_3 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_4 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_5 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_6 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_7 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_8 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_9 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_10 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_11 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_12 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_13 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_14 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_15 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_16 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_17 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_0_18 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
  · rcases split19 a ha with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · exact check_1_0 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_1 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_2 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_3 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_4 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_5 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_6 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_7 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_8 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_9 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_10 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_11 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_12 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_13 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_14 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_15 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_16 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_17 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_1_18 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
  · rcases split19 a ha with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · exact check_2_0 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_1 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_2 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_3 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_4 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_5 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_6 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_7 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_8 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_9 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_10 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_11 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_12 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_13 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_14 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_15 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_16 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_17 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_2_18 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
  · rcases split19 a ha with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · exact check_3_0 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_1 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_2 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_3 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_4 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_5 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_6 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_7 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_8 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_9 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_10 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_11 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_12 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_13 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_14 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_15 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_16 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_17 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_3_18 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
  · rcases split19 a ha with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · exact check_4_0 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_1 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_2 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_3 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_4 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_5 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_6 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_7 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_8 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_9 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_10 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_11 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_12 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_13 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_14 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_15 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_16 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_17 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_4_18 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
  · rcases split19 a ha with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · exact check_5_0 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_1 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_2 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_3 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_4 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_5 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_6 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_7 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_8 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_9 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_10 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_11 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_12 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_13 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_14 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_15 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_16 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_17 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_5_18 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
  · rcases split19 a ha with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · exact check_6_0 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_1 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_2 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_3 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_4 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_5 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_6 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_7 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_8 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_9 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_10 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_11 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_12 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_13 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_14 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_15 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_16 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_17 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩
    · exact check_6_18 ⟨b, hb⟩ ⟨c, hc⟩ control ⟨hfront, hoverflow⟩

theorem phase0_bound (a b c : Nat) (ha : a < 19) (hb : b < 19) (hc : c < 19) :
    rank 0 a b c ≤ 26 := by
  rcases split19 a ha with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact bound_0_0 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_1 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_2 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_3 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_4 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_5 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_6 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_7 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_8 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_9 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_10 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_11 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_12 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_13 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_14 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_15 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_16 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_17 ⟨b, hb⟩ ⟨c, hc⟩
  · exact bound_0_18 ⟨b, hb⟩ ⟨c, hc⟩

#print axioms rank_decreases
#print axioms phase0_bound

end RankCertificate
