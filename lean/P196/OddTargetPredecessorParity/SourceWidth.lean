import P196.OddTargetPredecessorParity.Definitions

/-!
Agent #6: the source width selected by a low outer pair coefficient, and
the odd-target facts that apply this selection to an accepted parity test.
The existing physical decoder payload supplies the actual target digits,
terminal carry, and canonical width choice together.
-/

set_option autoImplicit false

namespace OddTargetPredecessorParity

open Lychrel196 DecimalDigits FoldedDecimal Agent101
open Agent105DecoderTarget9df76b Agent105NumericDecoder9df76b
open Agent105WordFiber9df76b CompleteFiberParity

/-- Every actual canonical predecessor of an odd target has an odd outer
pair coefficient. -/
theorem odd_predecessor_outer
    (n Y L : Nat) (d : Nat → Nat)
    (hn : Canonical n d L) (hstep : step n = Y) (hodd : Y % 2 = 1) :
    columnSum d L 0 % 2 = 1 := by
  have hv : step n = value (columnSum d L) L :=
    step_eq_word_value n d (columnSum d L) L hn (fun _ _ => rfl)
  have hindex : L - 1 + 1 = L := by have hL := hn.1; omega
  have hshift := value_shift (columnSum d L) (L - 1)
  rw [hindex, ← hv, hstep] at hshift
  omega

/-- A one-digit source has an even reverse-and-add output, so every
canonical predecessor of an odd target has at least two digits. -/
theorem odd_predecessor_width_ge_two
    (n Y L : Nat) (d : Nat → Nat)
    (hn : Canonical n d L) (hstep : step n = Y) (hodd : Y % 2 = 1) :
    2 ≤ L := by
  have hL := hn.1
  have houter := odd_predecessor_outer n Y L d hn hstep hodd
  by_cases htwo : 2 ≤ L
  · exact htwo
  · have hone : L = 1 := by omega
    subst L
    have hcenter : columnSum d 1 0 = 2 * d 0 := by
      simpa using odd_center_input d 0
    omega

/-- A source with outer pair sum at most nine has exactly the width
selected by the target's leading and units digits. This statement does
not require the target itself to be odd. -/
theorem low_outer_source_width
    (n Y L W : Nat) (d e : Nat → Nat)
    (hn : Canonical n d L) (hY : Canonical Y e W)
    (hstep : step n = Y) (hsmall : columnSum d L 0 ≤ 9) :
    L = selectedWidth e W := by
  let q := columnSum d L
  change q 0 ≤ 9 at hsmall
  obtain ⟨c, hwidth, ha, hout, hcarry⟩ :=
    canonical_predecessor_payload Y n e d W L hY hn hstep
  have hunit : e 0 = q 0 := by
    have hu := hout 0 hn.1
    change output q 0 = e 0 at hu
    have hlt : q 0 < 10 := by omega
    simpa only [output, carry, Nat.add_zero, Nat.mod_eq_of_lt hlt] using hu.symm
  have hindex : L - 1 + 1 = L := by have hL := hn.1; omega
  have hsym : q (L - 1) = q 0 := by
    have hs := columnSum_symmetric d L 0 hn.1
    simpa only [Nat.sub_zero] using hs.symm
  have hlast := column_equation q (L - 1)
  rw [hindex, hcarry, hout (L - 1) (by have hL := hn.1; omega), hsym] at hlast
  rcases hwidth with ⟨hW, hc⟩ | ⟨hW, hc, htop⟩
  · have hnot : ¬ (e (W - 1) = 1 ∧ e 0 = 9) := by
      rintro ⟨hlead, hunits⟩
      have hlead' : e (L - 1) = 1 := by simpa only [hW] using hlead
      omega
    unfold selectedWidth
    rw [if_neg hnot]
    exact hW.symm
  · have hoverflow : carry q L = 1 := hcarry.trans hc
    have hnine : q 0 = 9 := by
      by_cases hlow : q 0 ≤ 8
      · have hz := NormalizationBridge.outer_small_no_overflow q L ha hlow
        omega
      · omega
    have hcondition : e (W - 1) = 1 ∧ e 0 = 9 := by
      refine ⟨?_, hunit.trans hnine⟩
      have hlastindex : W - 1 = L := by omega
      simpa only [hlastindex] using htop
    unfold selectedWidth
    rw [if_pos hcondition]
    omega

/-- An accepted odd-target profile has a low odd outer coefficient, so
its prescribed source width equals the target's selected width. -/
theorem odd_decoded_selected_width
    (Y : Nat) (e : Nat → Nat) (W L : Nat)
    (hY : Canonical Y e W) (hodd : Y % 2 = 1)
    (ho : oddDecoded e W L = true) :
    L = selectedWidth e W := by
  cases hdec : decodeNumerical e W L with
  | none => simp [oddDecoded, hdec] at ho
  | some qs =>
    have hprof : oddProfile (half qs) (center qs) = true := by
      simpa only [oddDecoded, hdec] using ho
    obtain ⟨hlen, n, d, _, hn, hprofile, hstep⟩ :=
      (decodeNumerical_eq_some_iff Y e W L qs hY).mp hdec
    have htwo := odd_predecessor_width_ge_two n Y L d hn hstep hodd
    have houter := odd_predecessor_outer n Y L d hn hstep hodd
    cases qs with
    | nil => simp at hlen; omega
    | cons s tail =>
      have hfirst : columnSum d L 0 = s := by
        simpa [digitFn] using hprofile 0 hn.1
      have hsodd : s % 2 = 1 := by simpa only [hfirst] using houter
      have hhalfpos : 0 < (s :: tail).length / 2 := by omega
      cases hhalfcount : (s :: tail).length / 2 with
      | zero => omega
      | succ j =>
        have hhalf : half (s :: tail) = s :: tail.take j := by
          unfold half
          rw [hhalfcount]
          rfl
        have hsmall : s ≤ 9 := by
          rw [hhalf] at hprof
          simp only [oddProfile, Bool.and_eq_true, decide_eq_true_eq] at hprof
          omega
        exact low_outer_source_width n Y L W d e hn hY hstep
          (by simpa only [hfirst] using hsmall)

#print axioms odd_predecessor_outer
#print axioms odd_predecessor_width_ge_two
#print axioms low_outer_source_width
#print axioms odd_decoded_selected_width

end OddTargetPredecessorParity
