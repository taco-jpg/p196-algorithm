import P196.Foundations.Agent1PeriodicGuard

/-!
The exact period-four phase update away from the all-nine exception.
The two stable digit bands lose dependence on their boundary entry carries,
but the original whole word's actual terminal-carry displacement is retained.
No freely chosen clock, interface return, or safe orbit is asserted.
-/

namespace Agent1.Periodic
open Agent8 Agent1.RepeatedBlock

/-- The boundary-independent stable digit bands, paired at a specified clock.
The arithmetic is the existing list normalizer and zipper. -/
def phaseImage (w : Word) (g : Nat) : Word :=
  zipperPeriod (fixedDigits w (terminalCarry w 0))
    (fixedDigits w.reverse (terminalCarry w.reverse 0)) g

/-- A length-four word different from four nines has a non-nine member. -/
theorem mem_nonNine_of_length_four (w : Word) (hlen : w.length = 4)
    (hne : w ≠ [9,9,9,9]) : ∃ x, x ∈ w ∧ x ≠ 9 := by
  by_cases h : ∃ x, x ∈ w ∧ x ≠ 9
  · exact h
  · exfalso
    apply hne
    have hall : ∀ x, x ∈ w → x = 9 := by
      intro x hx
      by_cases hx9 : x = 9
      · exact hx9
      · exact False.elim (h ⟨x, hx, hx9⟩)
    have he := List.eq_replicate_of_mem hall
    simpa only [hlen, List.replicate] using he

/-- Reversal preserves the exclusion of the neutral four-nine block. -/
theorem reverse_ne_nines (w : Word) (hne : w ≠ [9,9,9,9]) :
    w.reverse ≠ [9,9,9,9] := by
  intro h
  apply hne
  have hr := congrArg List.reverse h
  simpa using hr

/-- A bounded list containing a non-nine synchronizes any two bit entries.
This is the original indexed carry-reset theorem through the checked bridge. -/
theorem terminalCarry_eq_of_nonNine (w : Word) (a b : Nat)
    (hw : Bounded w 18) (ha : a ≤ 1) (hb : b ≤ 1)
    (hne : ∃ x, x ∈ w ∧ x ≠ 9) :
    terminalCarry w a = terminalCarry w b := by
  obtain ⟨x, hx, hx9⟩ := hne
  obtain ⟨i, hi, hix⟩ := List.getElem_of_mem hx
  have hq : ∀ j, j < w.length → (w[j]?).getD 0 ≤ 18 := by
    intro j hj
    rw [List.getElem?_eq_getElem hj]
    exact hw _ (List.getElem_mem hj)
  have hi9 : (w[i]?).getD 0 ≠ 9 := by
    simpa only [List.getElem?_eq_getElem hi, Option.getD_some, hix] using hx9
  rw [terminalCarry_eq_carryIn, terminalCarry_eq_carryIn]
  exact IncomingCarry.carryIn_eq_of_nonNine
    (fun j => (w[j]?).getD 0) a b w.length i ha hb hq hi hi9

/-- The actual raw period depends only on the input period and the actual
whole-word overflow bit, except at the all-nine period. No validity or
realizability premise is needed beyond the stated coefficient bounds. -/
theorem rawPeriod_eq_phaseImage (B H w : Word)
    (hB : Bounded B 18) (hH : Bounded H 18) (hw : Bounded w 18)
    (hlen : w.length = 4) (hne : w ≠ [9,9,9,9]) :
    rawPeriod B H w = phaseImage w (rawGamma B H w) := by
  have hb : leftEntry B ≤ 1 := terminalCarry_le_one B 0 hB (by omega)
  have hc : leftCarry B w ≤ 1 := terminalCarry_le_one w (leftEntry B) hw hb
  have hh : rightEntry B H w ≤ 1 :=
    terminalCarry_le_one H (leftCarry B w) hH hc
  have hwr : Bounded w.reverse 18 := fun x hx => hw x (List.mem_reverse.mp hx)
  have hl : leftCarry B w = terminalCarry w 0 :=
    terminalCarry_eq_of_nonNine w (leftEntry B) 0 hw hb (by omega)
      (mem_nonNine_of_length_four w hlen hne)
  have hr : rightCarry B H w = terminalCarry w.reverse 0 :=
    terminalCarry_eq_of_nonNine w.reverse (rightEntry B H w) 0 hwr hh (by omega)
      (mem_nonNine_of_length_four w.reverse
        (by simpa only [List.length_reverse] using hlen) (reverse_ne_nines w hne))
  rw [(raw_blocks_eq_zipper B H w hB hH hw hlen).2.1]
  simp only [leftPeriodDigits, rightPeriodDigits, hl, hr, phaseImage]

end Agent1.Periodic

#print axioms Agent1.Periodic.phaseImage
#print axioms Agent1.Periodic.mem_nonNine_of_length_four
#print axioms Agent1.Periodic.reverse_ne_nines
#print axioms Agent1.Periodic.terminalCarry_eq_of_nonNine
#print axioms Agent1.Periodic.rawPeriod_eq_phaseImage
