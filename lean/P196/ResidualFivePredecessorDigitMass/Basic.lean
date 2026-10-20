import P196.ResidualFivePredecessorDigitMass.ListMass
import P196.ResidualFivePredecessorDigitMass.ScanMass
import P196.ResidualFivePredecessorDigitMass.Wrapper

set_option autoImplicit false

/-!
# Exact digit sums and carries of residual-five predecessors

The original all-width predecessor enumeration and the forced exterior
target digits identify every ordinary predecessor with a decoded symmetric
coefficient word. The complementary interior has coefficient sum 18*r;
the two outside coefficient pairs add fourteen. Consequently every source
has digit sum 9*r+7, and the original decimal mass balance gives exactly
r outgoing carries in any canonical representation of that source.

These statements concern the existing residual-five fiber. They do not
identify it with an unrestricted fiber of its associated middle integer,
assert arbitrary inverse depth, or establish an orbit statement about 196.
-/

namespace P196.ResidualFivePredecessorDigitMass

open Agent101 Lychrel196
open Agent105DecoderScan9df76b (scan)

/-- Every positive ordinary predecessor of the existing residual-five
fiber has the same digit sum, without a prescribed source-width premise. -/
theorem predecessor_digitSum (r m : Nat)
    (hm : 0 < m)
    (h : step m ∈ Agent103.ResidualFiveFibers.fiber r) :
    DecimalMass.digitSum m = 9 * r + 7 := by
  have htarget : step m ∈ P196.ResidualFivePredecessorCount.survivors r :=
    (P196.ResidualFivePredecessorCount.mem_survivors r (step m)).mpr
      ⟨h, m, hm, rfl⟩
  obtain ⟨target, hword, hvalue⟩ := List.mem_map.mp htarget
  have hcanonical := (canonicalDigits_iff target).mp
    (P196.ResidualFivePredecessorCount.survivorWords_canonical r target hword)
  have hshape := hword
  rw [P196.ResidualFivePredecessorCount.survivorWords_outer_reduction] at hshape
  obtain ⟨ds, hfiltered, rfl⟩ := List.mem_map.mp hshape
  obtain ⟨hraw, haccepted⟩ := List.mem_filter.mp hfiltered
  have hmem := (Agent105Predecessors9df76b.mem_predecessors
    (natValue (wrapDigits 1 1 (wrapDigits 6 6 ds)))
    (digitFn (wrapDigits 1 1 (wrapDigits 6 6 ds)))
    (wrapDigits 1 1 (wrapDigits 6 6 ds)).length m hcanonical).mpr
      ⟨hm, hvalue.symm⟩
  cases hscan : scan ds.length (digitFn ds) 0 0 with
  | none => simp [hscan] at haccepted
  | some qs =>
    rw [predecessors_wrap_one_six ds, hscan] at hmem
    have hdec := decodeNumerical_wrap_one_pair 6 6 6 ds (by decide)
    rw [hscan] at hdec
    have hrev := (Agent105DecodedFiber9df76b.decodeNumerical_word_spec
      _ _ _ _ _ hcanonical hdec).2.1
    have hmass := wordFiber_digitSum_double
      (wrapDigits 1 1 (wrapDigits 6 6 qs)) m hrev hmem
    have hinner := scan_raw_nines_sum r 0 0 ds qs
      (by decide) (by decide) hraw hscan
    simp only [wrapDigits, List.sum_cons, Agent2Exterior.sum_append,
      List.sum_nil, Nat.add_zero] at hmass
    omega

/-- Every canonical representation of an ordinary predecessor has exactly
r outgoing carries in its reverse-and-add step, including the final carry. -/
theorem predecessor_carryCount (r m L : Nat) (d : Nat → Nat)
    (hc : DecimalDigits.Canonical m d L)
    (h : step m ∈ Agent103.ResidualFiveFibers.fiber r) :
    DecimalMass.carryCount (DecimalDigits.columnSum d L) L = r := by
  have hm : 0 < m := by
    rw [← hc.2.2.2]
    exact DecimalDigits.value_positive d L hc.1 hc.2.2.1
  have hbalance := DecimalMass.digitSum_step_balance d L hc.2.1
    (Or.inr hc.2.2.1)
  rw [hc.2.2.2, fiber_digitSum r (step m) h,
    predecessor_digitSum r m hm h] at hbalance
  omega

end P196.ResidualFivePredecessorDigitMass

#print axioms P196.ResidualFivePredecessorDigitMass.predecessor_digitSum
#print axioms P196.ResidualFivePredecessorDigitMass.predecessor_carryCount
