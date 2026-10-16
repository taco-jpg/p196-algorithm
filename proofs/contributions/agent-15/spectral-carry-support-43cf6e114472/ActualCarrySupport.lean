import SourceFormula
import RawSymmetryObstruction

/-!
The exact outgoing word of the existing decimal carry recurrence.
For bounded symmetric column coefficients, its nonzero spectral charge is
supported precisely by an asymmetric reflected outgoing pair at coefficient 9.
The final outgoing carry is retained at both possible values. The initial
incoming zero is excluded, and no parity or overflow restriction is imposed.
-/

set_option autoImplicit false

namespace P196.Agent15.SpectralSupport

open DecimalDigits
open P196.Agent15.SpectralCarry

/-- The L computed outgoing carries, in their original low-to-high order. -/
def outgoing (q : Nat → Nat) (L : Nat) : List Nat :=
  (List.range L).map (fun i => DecimalDigits.carry q (i + 1))

/-- The existing exact parity-selected integer charge of the actual carry word. -/
def actualCharge (q : Nat → Nat) (L : Nat) : Int :=
  P196.Agent15.SpectralCarry.carryCharge (outgoing q L)

@[simp] theorem outgoing_length (q : Nat → Nat) (L : Nat) :
    (outgoing q L).length = L := by
  simp [outgoing]

/-- Index i records carry q (i+1), with no initial-zero shift or trimming. -/
theorem outgoing_getElem (q : Nat → Nat) (L i : Nat) (hi : i < L) :
    (outgoing q L)[i]'(by simpa only [outgoing_length] using hi) =
      carry q (i + 1) := by
  simp [outgoing]

theorem outgoing_getElem? (q : Nat → Nat) (L i : Nat) (hi : i < L) :
    (outgoing q L)[i]? = some (carry q (i + 1)) := by
  have hlen : i < (outgoing q L).length := by
    simpa only [outgoing_length] using hi
  rw [List.getElem?_eq_getElem hlen]
  congr 1
  exact outgoing_getElem q L i hi

/-- For every positive width, the last word entry is the actual final outgoing carry. -/
theorem outgoing_last (q : Nat → Nat) (L : Nat) (hL : 0 < L) :
    (outgoing q L)[L - 1]'(by simp only [outgoing_length]; omega) = carry q L := by
  have hi : L - 1 < L := by omega
  have hind : L - 1 + 1 = L := by omega
  simpa only [hind] using outgoing_getElem q L (L - 1) hi

/-- Coefficient bounds are needed only within the original width. -/
theorem outgoing_binary (q : Nat → Nat) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18) : Binary (outgoing q L) := by
  intro a ha
  change a ∈ (List.range L).map (fun i => carry q (i + 1)) at ha
  rcases List.mem_map.mp ha with ⟨i, hi, rfl⟩
  have hiL : i < L := List.mem_range.mp hi
  have hc := carry_bounded q L hb (i + 1) (by omega)
  omega

/-- List reflection agrees with the unshifted pair of actual outgoing indices. -/
theorem outgoing_reverse_iff (q : Nat → Nat) (L : Nat) :
    (outgoing q L).reverse = outgoing q L ↔
      ∀ i, i < L → carry q (i + 1) = carry q (L - i) := by
  constructor
  · intro h i hi
    have he := congrArg (fun xs : List Nat => xs[i]?) h
    change (outgoing q L).reverse[i]? = (outgoing q L)[i]? at he
    have hiW : i < (outgoing q L).length := by
      simpa only [outgoing_length] using hi
    rw [List.getElem?_reverse hiW, outgoing_length] at he
    have hj : L - 1 - i < L := by omega
    rw [outgoing_getElem? q L (L - 1 - i) hj,
      outgoing_getElem? q L i hi] at he
    have hind : L - 1 - i + 1 = L - i := by omega
    rw [hind] at he
    exact (Option.some.inj he).symm
  · intro h
    apply List.ext_getElem?
    intro i
    by_cases hi : i < L
    · have hiW : i < (outgoing q L).length := by
        simpa only [outgoing_length] using hi
      rw [List.getElem?_reverse hiW, outgoing_length]
      have hj : L - 1 - i < L := by omega
      rw [outgoing_getElem? q L (L - 1 - i) hj,
        outgoing_getElem? q L i hi]
      have hind : L - 1 - i + 1 = L - i := by omega
      rw [hind, h i hi]
    · have hw : (outgoing q L).length ≤ i := by
        simp only [outgoing_length]
        omega
      have hr : (outgoing q L).reverse.length ≤ i := by simpa using hw
      rw [List.getElem?_eq_none hr, List.getElem?_eq_none hw]

/-- Charge faithfulness for the computed carries needs no symmetry of q. -/
theorem actualCharge_zero_iff (q : Nat → Nat) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18) :
    actualCharge q L = 0 ↔
      ∀ i, i < L → carry q (i + 1) = carry q (L - i) := by
  unfold actualCharge
  exact (carryCharge_zero_iff (outgoing_binary q L hb)).trans
    (outgoing_reverse_iff q L)

/-- Outside coefficient 9, the existing local division lemma removes sensitivity
of a reflected outgoing pair to its two possibly different incoming bits. -/
theorem outgoing_reflected_eq_of_nonnine (q : Nat → Nat) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i))
    (i : Nat) (hi : i < L) (hne : q i ≠ 9) :
    carry q (i + 1) = carry q (L - i) := by
  have hindex : L - i = (L - 1 - i) + 1 := by omega
  rw [hindex]
  change (q i + carry q i) / 10 =
    (q (L - 1 - i) + carry q (L - 1 - i)) / 10
  rw [← hs i hi]
  exact RawSymmetryObstruction.nonnine_binary_div (q i)
    (carry q i) (carry q (L - 1 - i)) (hb i hi) hne
    (carry_bounded q L hb i (by omega))
    (carry_bounded q L hb (L - 1 - i) (by omega))

/-- Exact support: nonzero charge is equivalent to a computed asymmetric
outgoing pair at a coefficient equal to 9. This asserts no converse from the
mere occurrence of a 9. -/
theorem actualCharge_nonzero_iff_nine_asymmetry (q : Nat → Nat) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i)) :
    actualCharge q L ≠ 0 ↔
      ∃ i, i < L ∧ q i = 9 ∧ carry q (i + 1) ≠ carry q (L - i) := by
  classical
  constructor
  · intro hn
    have hex : ∃ i, i < L ∧ carry q (i + 1) ≠ carry q (L - i) := by
      apply Classical.byContradiction
      intro h
      apply hn
      apply (actualCharge_zero_iff q L hb).2
      intro i hi
      apply Classical.byContradiction
      intro hc
      exact h ⟨i, hi, hc⟩
    rcases hex with ⟨i, hi, ha⟩
    refine ⟨i, hi, ?_, ha⟩
    apply Classical.byContradiction
    intro hnotnine
    exact ha (outgoing_reflected_eq_of_nonnine q L hb hs i hi hnotnine)
  · rintro ⟨i, hi, _, ha⟩ hz
    exact ha ((actualCharge_zero_iff q L hb).1 hz i hi)

/-- The literal one-way no-nine consequence of the original source statement. -/
theorem actualCharge_zero_of_no_nine (q : Nat → Nat) (L : Nat)
    (hb : ∀ i, i < L → q i ≤ 18)
    (hs : ∀ i, i < L → q i = q (L - 1 - i))
    (hn : ∀ i, i < L → q i ≠ 9) : actualCharge q L = 0 := by
  apply (actualCharge_zero_iff q L hb).2
  intro i hi
  exact outgoing_reflected_eq_of_nonnine q L hb hs i hi (hn i hi)

/-- The charge-zero adapter for an existing canonical decimal representation. -/
theorem canonical_actualCharge_zero_iff (n : Nat) (d : Nat → Nat) (L : Nat)
    (hc : DecimalDigits.Canonical n d L) :
    actualCharge (DecimalDigits.columnSum d L) L = 0 ↔
      ∀ i, i < L →
        DecimalDigits.carry (DecimalDigits.columnSum d L) (i + 1) =
          DecimalDigits.carry (DecimalDigits.columnSum d L) (L - i) := by
  exact actualCharge_zero_iff (columnSum d L) L (columnSum_bounded d L hc.2.1)

/-- A canonical paired coefficient different from 9 has equal reflected
computed outgoing carries. -/
theorem canonical_outgoing_reflected_eq_of_nonnine
    (n : Nat) (d : Nat → Nat) (L : Nat) (hc : DecimalDigits.Canonical n d L)
    (i : Nat) (hi : i < L) (hne : DecimalDigits.columnSum d L i ≠ 9) :
    DecimalDigits.carry (DecimalDigits.columnSum d L) (i + 1) =
      DecimalDigits.carry (DecimalDigits.columnSum d L) (L - i) := by
  exact outgoing_reflected_eq_of_nonnine (columnSum d L) L
    (columnSum_bounded d L hc.2.1) (columnSum_symmetric d L) i hi hne

/-- The exact support theorem specialized to actual canonical decimal digits. -/
theorem canonical_actualCharge_nonzero_iff_nine_asymmetry
    (n : Nat) (d : Nat → Nat) (L : Nat) (hc : DecimalDigits.Canonical n d L) :
    actualCharge (DecimalDigits.columnSum d L) L ≠ 0 ↔
      ∃ i, i < L ∧ DecimalDigits.columnSum d L i = 9 ∧
        DecimalDigits.carry (DecimalDigits.columnSum d L) (i + 1) ≠
          DecimalDigits.carry (DecimalDigits.columnSum d L) (L - i) := by
  exact actualCharge_nonzero_iff_nine_asymmetry (columnSum d L) L
    (columnSum_bounded d L hc.2.1) (columnSum_symmetric d L)

/-- Absence of paired coefficient 9 forces zero charge for the actual carries
of the given canonical representation. -/
theorem canonical_actualCharge_zero_of_no_nine
    (n : Nat) (d : Nat → Nat) (L : Nat) (hc : DecimalDigits.Canonical n d L)
    (hn : ∀ i, i < L → DecimalDigits.columnSum d L i ≠ 9) :
    actualCharge (DecimalDigits.columnSum d L) L = 0 := by
  exact actualCharge_zero_of_no_nine (columnSum d L) L
    (columnSum_bounded d L hc.2.1) (columnSum_symmetric d L) hn

/-- The general algebraic extension includes width zero. -/
theorem actualCharge_width_zero (q : Nat → Nat) : actualCharge q 0 = 0 := by
  simp [actualCharge, outgoing, carryCharge, evenCharge, halfCharge, weighted]

/-- At width one the sole outgoing carry is the free central entry. -/
theorem actualCharge_width_one (q : Nat → Nat) : actualCharge q 1 = 0 := by
  simp [actualCharge, outgoing, carryCharge, oddCharge, halfCharge, weighted]

namespace Controls

/-- A coefficient 9 can occur while the actual charge is zero. -/
theorem nine_zero_charge :
    outgoing (fun _ => 9) 2 = [0, 0] ∧ actualCharge (fun _ => 9) 2 = 0 ∧
      ∃ i, i < 2 ∧ (fun _ : Nat => 9) i = 9 := by
  exact ⟨by decide, by decide, 0, by decide, rfl⟩

/-- An even word retains the actual final carry 1 and has zero charge. -/
theorem even_overflow_zero_charge :
    outgoing (fun _ => 10) 2 = [1, 1] ∧ actualCharge (fun _ => 10) 2 = 0 := by
  decide

/-- The nonzero odd central carry is free; the final outgoing carry is zero. -/
theorem odd_free_center :
    outgoing (fun i => if i = 1 then 18 else 8) 3 = [0, 1, 0] ∧
      actualCharge (fun i => if i = 1 then 18 else 8) 3 = 0 := by
  decide

/-- A symmetric bounded coefficient word with 9 does realize nonzero charge. -/
theorem odd_nine_asymmetry :
    outgoing (fun i => if i = 1 then 18 else 9) 3 = [0, 1, 1] ∧
      actualCharge (fun i => if i = 1 then 18 else 9) 3 = 1 := by
  decide

end Controls

end P196.Agent15.SpectralSupport
