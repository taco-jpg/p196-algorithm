import Agent1PeriodicNines
import Agent1PeriodicQuotient
import Agent1PeriodicCenterWrap

/-!
The exact center produced by a mixed-entry constant-nine period. The pad uses
the actual whole-word terminal carry, and the middle is paired fixed digits,
not a separately normalized center. No center descent or return obstruction
is asserted.
-/

namespace Agent1.Periodic
open Agent8

private theorem nines_bounded : Bounded [9,9,9,9] 18 := by
  intro x hx
  simp only [List.mem_cons, List.not_mem_nil, or_false, or_self] at hx
  subst x
  decide

private theorem nines_carry (e : Nat) (he : e ≤ 1) :
    terminalCarry [9,9,9,9] e = e := by
  have h : e = 0 ∨ e = 1 := by omega
  rcases h with rfl | rfl <;> rfl

private theorem zipperCenter_nines_mixed (D : Word) (e f g : Nat)
    (he : e ≤ 1) (hf : f ≤ 1) (hg : g ≤ 1) (hmix : e + f = 1) :
    zipperCenter (fixedDigits [9,9,9,9] e)
      (D ++ fixedDigits [9,9,9,9] f) (fixedDigits [9,9,9,9] f) g =
      [9,9,9,9] ++ pair (D ++ List.replicate g (9*e)) ++ [9,9,9,9] := by
  have hef : (e = 0 ∧ f = 1) ∨ (e = 1 ∧ f = 0) := by omega
  have hg' : g = 0 ∨ g = 1 := by omega
  rcases hef with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;>
    rcases hg' with rfl | rfl
  · simpa [zipperCenter, fixedDigits, zipAdd, List.append_assoc] using
      pair_three_parts [9,9,9,9] D [0,0,0,0] rfl
  · have h := pair_three_parts [9,9,9,9] (D ++ [0]) [0,0,0,0] rfl
    simp only [List.append_assoc] at h
    simpa [zipperCenter, fixedDigits, zipAdd, List.append_assoc] using h
  · simpa [zipperCenter, fixedDigits, zipAdd, List.append_assoc] using
      pair_three_parts [0,0,0,0] D [9,9,9,9] rfl
  · have h := pair_three_parts [0,0,0,0] (D ++ [9]) [9,9,9,9] rfl
    simp only [List.append_assoc] at h
    simpa [zipperCenter, fixedDigits, zipAdd, List.append_assoc] using h

/-- Mixed actual entries leave one complete nine period on both sides of the
paired center digits, including the actual clock-dependent final pad. -/
theorem rawCenter_nines_mixed (B H : Word)
    (hB : Bounded B 18) (hH : Bounded H 18)
    (hmix : leftEntry B + rightEntry B H [9,9,9,9] = 1) :
    rawCenter B H [9,9,9,9] = [9,9,9,9] ++
      pair (fixedDigits H (leftEntry B) ++
        List.replicate (rawGamma B H [9,9,9,9]) (9 * leftEntry B)) ++ [9,9,9,9] := by
  obtain ⟨he, hf⟩ := nines_entry_bits B H hB hH
  have hl : leftCarry B [9,9,9,9] = leftEntry B := nines_carry _ he
  have hr : rightCarry B H [9,9,9,9] = rightEntry B H [9,9,9,9] := by
    change terminalCarry [9,9,9,9] (rightEntry B H [9,9,9,9]) = _
    exact nines_carry _ hf
  have hg : rawGamma B H [9,9,9,9] ≤ 1 :=
    scan_carry_le_one B H [9,9,9,9] hB hH nines_bounded
  rw [(raw_blocks_eq_zipper B H [9,9,9,9] hB hH nines_bounded rfl).2.2]
  unfold leftPeriodDigits centerGuardDigits rightPeriodDigits
  rw [hl, hr]
  exact zipperCenter_nines_mixed (fixedDigits H (leftEntry B))
    (leftEntry B) (rightEntry B H [9,9,9,9]) (rawGamma B H [9,9,9,9]) he hf hg hmix

private theorem strip_rawCenter_nines_mixed (B H : Word)
    (hB : Bounded B 18) (hH : Bounded H 18)
    (hmix : leftEntry B + rightEntry B H [9,9,9,9] = 1) :
    stripPeriodCenter (rawPeriod B H [9,9,9,9]) (rawCenter B H [9,9,9,9]) =
      ((stripPeriodCenter [9,9,9,9]
        (pair (fixedDigits H (leftEntry B) ++
          List.replicate (rawGamma B H [9,9,9,9]) (9 * leftEntry B)))).1,
       (stripPeriodCenter [9,9,9,9]
        (pair (fixedDigits H (leftEntry B) ++
          List.replicate (rawGamma B H [9,9,9,9]) (9 * leftEntry B)))).2 + 1) := by
  have hw : rawPeriod B H [9,9,9,9] = [9,9,9,9] := by
    rw [rawPeriod_nines B H hB hH, hmix]
    rfl
  rw [hw, rawCenter_nines_mixed B H hB hH hmix]
  exact stripPeriodCenter_wrap [9,9,9,9] _ (by decide)

/-- The quotient center is the literal maximal stripping of the paired fixed
center digits with the actual clock pad. Further inner removals are retained. -/
theorem quotientCenter_nines_mixed (B H : Word)
    (hB : Bounded B 18) (hH : Bounded H 18)
    (hmix : leftEntry B + rightEntry B H [9,9,9,9] = 1) :
    quotientCenter B H [9,9,9,9] =
      (stripPeriodCenter [9,9,9,9]
        (pair (fixedDigits H (leftEntry B) ++
          List.replicate (rawGamma B H [9,9,9,9]) (9 * leftEntry B)))).1 := by
  exact congrArg Prod.fst (strip_rawCenter_nines_mixed B H hB hH hmix)

/-- The removed center-period count is exactly one plus the maximal count
inside the paired fixed center digits; it need not equal one. -/
theorem centerPeriods_nines_mixed (B H : Word)
    (hB : Bounded B 18) (hH : Bounded H 18)
    (hmix : leftEntry B + rightEntry B H [9,9,9,9] = 1) :
    centerPeriods B H [9,9,9,9] =
      (stripPeriodCenter [9,9,9,9]
        (pair (fixedDigits H (leftEntry B) ++
          List.replicate (rawGamma B H [9,9,9,9]) (9 * leftEntry B)))).2 + 1 := by
  exact congrArg Prod.snd (strip_rawCenter_nines_mixed B H hB hH hmix)

end Agent1.Periodic

#print axioms Agent1.Periodic.rawCenter_nines_mixed
#print axioms Agent1.Periodic.quotientCenter_nines_mixed
#print axioms Agent1.Periodic.centerPeriods_nines_mixed
