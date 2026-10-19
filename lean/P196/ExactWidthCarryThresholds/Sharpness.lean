import P196.ExactWidthCarryThresholds.Definitions
import P196.ExactWidthCarryThresholds.WidthWitnesses
import P196.ExactSmallWidthCarryThresholds.Sharpness
import P196.CarryPrefixThresholds.SevenCarryWitness
import P196.EightCarryWidthBound.Sharpness
import P196.Agent10NineCarrySharp.Agent10SevenCarryCounterexample
import P196.Agent10NineCarrySharp.Agent10EightCarryCounterexample

/-!
Canonical ambiguity at one fewer observation than the threshold for every
exact initial width from one to seventeen. The full small-width result and
the existing width-nine, thirteen, fifteen and seventeen witnesses are
imported unchanged. The five new instances fill precisely the remaining
widths. Every counterexample has both an active pair difference and distinct
next ordinary integers, with the terminal carry included in each observation.
-/

namespace ExactWidthCarryThresholds

open DecimalDigits FoldedDecimal OverflowCarryNormalization
open CarryObservabilityActual

private theorem additional_observation_count :
    ∀ w : Fin 5,
      exactWidthThreshold (Witnesses.width w) - 1 = Witnesses.observations w := by
  decide +kernel

/-- Each classified exact width admits two canonical inputs with one fewer
complete observation, distinct active pair sums, and distinct next integers. -/
theorem exact_width_counterexample (L : Nat) (hpos : 0 < L) (hwidth : L ≤ 17) :
    ∃ (n m : Nat) (d e : Nat → Nat),
      Canonical n d L ∧ Canonical m e L ∧
      (∀ t, t < exactWidthThreshold L - 1 →
        ∀ i, i ≤ (iterPairs (columnSum d L) L t).1 →
          carry (iterPairs (columnSum d L) L t).2 i =
            carry (iterPairs (columnSum e L) L t).2 i) ∧
      (∃ i, i < L ∧ columnSum d L i ≠ columnSum e L i) ∧
      Lychrel196.step n ≠ Lychrel196.step m := by
  by_cases hsmall : L ≤ 8
  · simpa only [exactWidthThreshold, if_pos hsmall] using
      ExactSmallWidthCarryThresholds.exact_width_counterexample L hpos hsmall
  by_cases h9 : L = 9
  · subst L
    rcases CarryPrefixThresholds.SevenCarryWitness.seven_carry_counterexample with
      ⟨hn, hm, _, _, hc, hne, hs⟩
    refine ⟨490039199, 480047399,
      CarryPrefixThresholds.SevenCarryWitness.leftDigits,
      CarryPrefixThresholds.SevenCarryWitness.rightDigits,
      hn, hm, ?_, ⟨1, hne⟩, hs⟩
    simpa only [show exactWidthThreshold 9 - 1 = 7 from rfl] using hc
  by_cases h13 : L = 13
  · subst L
    rcases EightCarryWidthBound.WidthThirteenWitness.seven_carry_counterexample with
      ⟨hn, hm, _, _, hc, hne, hs⟩
    refine ⟨9000004163209, 9000001716109,
      EightCarryWidthBound.WidthThirteenWitness.digits false,
      EightCarryWidthBound.WidthThirteenWitness.digits true,
      hn, hm, ?_, ⟨2, by decide, hne⟩, hs⟩
    simpa only [show exactWidthThreshold 13 - 1 = 7 from rfl] using hc
  by_cases h15 : L = 15
  · subst L
    rcases Agent10SevenCarryCounterexample.seven_carry_counterexample with
      ⟨hn, hm, hc, hne, hs⟩
    refine ⟨900000058163209, 900000082716109,
      Agent10SevenCarryCounterexample.leftDigits,
      Agent10SevenCarryCounterexample.rightDigits,
      hn, hm, ?_, ⟨2, by decide, hne⟩, hs⟩
    simpa only [show exactWidthThreshold 15 - 1 = 7 from rfl] using hc
  by_cases h17 : L = 17
  · subst L
    rcases Agent10EightCarryCounterexample.eight_carry_counterexample with
      ⟨hn, hm, hc, hne, hs⟩
    refine ⟨90000000560706169, 90000000806235169,
      Agent10EightCarryCounterexample.leftDigits,
      Agent10EightCarryCounterexample.rightDigits,
      hn, hm, ?_, ⟨3, by decide, hne⟩, hs⟩
    simpa only [show exactWidthThreshold 17 - 1 = 8 from rfl] using hc
  have hremaining : L = 10 ∨ L = 11 ∨ L = 12 ∨ L = 14 ∨ L = 16 := by omega
  have hinstance : ∃ w : Fin 5, Witnesses.width w = L := by
    rcases hremaining with h | h | h | h | h
    · subst L; exact ⟨⟨0, by decide⟩, rfl⟩
    · subst L; exact ⟨⟨1, by decide⟩, rfl⟩
    · subst L; exact ⟨⟨2, by decide⟩, rfl⟩
    · subst L; exact ⟨⟨3, by decide⟩, rfl⟩
    · subst L; exact ⟨⟨4, by decide⟩, rfl⟩
  obtain ⟨w, hw⟩ := hinstance
  rw [← hw]
  refine ⟨Witnesses.seed w false, Witnesses.seed w true,
    Witnesses.digits w false, Witnesses.digits w true,
    Witnesses.canonical w false, Witnesses.canonical w true, ?_,
    ⟨Witnesses.differenceIndex w, Witnesses.initial_pair_difference_active w⟩,
    Witnesses.next_integers_differ w⟩
  intro t ht i hi
  exact Witnesses.complete_carries w t
    (by simpa only [additional_observation_count] using ht) i hi

#print axioms exact_width_counterexample

end ExactWidthCarryThresholds
