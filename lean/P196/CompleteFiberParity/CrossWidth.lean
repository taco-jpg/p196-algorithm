import P196.Agent105AllPredecessors.Agent105DecodedFiber9df76b
import P196.Agent105InverseBoundaries.Agent105CrossWidth9df76b

/-!
Agent #6: divisibility of complete ordinary predecessor fibers across distinct
source widths. The existing cross-width collision theorem forces outer pair
sum eleven at the smaller width; the existing exact fiber product then
contributes a factor of eight.
-/

set_option autoImplicit false

namespace CompleteFiberParity

open Lychrel196 DecimalDigits Agent101
open Agent105DecodedFiber9df76b Agent105NumericDecoder9df76b
open Agent105WordFiber9df76b Agent105CrossWidth9df76b

/-- If a canonical target has a predecessor at a larger source width, its
complete predecessor count at any smaller width is divisible by eight.
The smaller fiber is allowed to be empty. -/
theorem shorter_fiber_divisible_by_eight_of_longer_nonempty
    (Y : Nat) (e : Nat → Nat) (W L K : Nat)
    (htarget : Canonical Y e W)
    (hLK : L < K)
    (hlonger : decodedFiber e W K ≠ []) :
    8 ∣ (decodedFiber e W L).length := by
  have hmember : ∃ m, m ∈ decodedFiber e W K := by
    cases hxs : decodedFiber e W K with
    | nil => exact False.elim (hlonger hxs)
    | cons m ms => exact ⟨m, by simp⟩
  obtain ⟨m, hm⟩ := hmember
  obtain ⟨_, f, hmcan, hmstep⟩ :=
    (mem_decodedFiber Y e W K m htarget).mp hm
  unfold decodedFiber
  cases hdec : decodeNumerical e W L with
  | none => simp
  | some qs =>
    obtain ⟨hlen, n, d, _, hncan, hprofile, hnstep⟩ :=
      (decodeNumerical_eq_some_iff Y e W L qs htarget).mp hdec
    have hstep : step n = step m := hnstep.trans hmstep.symm
    have houter := (cross_width_outer hncan hmcan hLK hstep).1
    have hL := cross_width_short_length hncan hmcan hLK hstep
    have hfirst : digitFn qs 0 = 11 :=
      (hprofile 0 hncan.1).symm.trans houter
    cases qs with
    | nil => simp at hlen; omega
    | cons s tail =>
      have hs : s = 11 := by simpa [digitFn] using hfirst
      subst s
      have hhalfpos : 0 < (11 :: tail).length / 2 := by omega
      cases hhalfcount : (11 :: tail).length / 2 with
      | zero => omega
      | succ j =>
        have hhalf : half (11 :: tail) = 11 :: tail.take j := by
          unfold half
          rw [hhalfcount]
          rfl
        change 8 ∣ (numericFiber (half (11 :: tail)) (center (11 :: tail))).length
        rw [hhalf, length_numericFiber_cons]
        change 8 ∣ 8 * centerCount (center (11 :: tail)) *
          natProduct ((tail.take j).map (pairCount false))
        refine ⟨centerCount (center (11 :: tail)) *
          natProduct ((tail.take j).map (pairCount false)), ?_⟩
        simp only [Nat.mul_assoc]

/-- Complete predecessor counts at two distinct source widths cannot both
be odd. -/
theorem not_both_width_fibers_odd
    (Y : Nat) (e : Nat → Nat) (W L K : Nat)
    (htarget : Canonical Y e W)
    (hLK : L < K) :
    ¬ ((decodedFiber e W L).length % 2 = 1 ∧
       (decodedFiber e W K).length % 2 = 1) := by
  rintro ⟨hshort, hlong⟩
  have hnonempty : decodedFiber e W K ≠ [] := by
    intro hempty
    simp only [hempty, List.length_nil, Nat.zero_mod] at hlong
    omega
  have hdiv := shorter_fiber_divisible_by_eight_of_longer_nonempty
    Y e W L K htarget hLK hnonempty
  have heven := Nat.mod_eq_zero_of_dvd
    (Nat.dvd_trans (by decide : 2 ∣ 8) hdiv)
  omega

/-- At the two source widths allowed by a canonical target, a nonempty
width-W fiber forces the width-(W-1) count to vanish modulo eight. -/
theorem short_fiber_mod_eight_of_long_nonempty
    (Y : Nat) (e : Nat → Nat) (W : Nat)
    (htarget : Canonical Y e W)
    (hlonger : decodedFiber e W W ≠ []) :
    (decodedFiber e W (W - 1)).length % 8 = 0 := by
  apply Nat.mod_eq_zero_of_dvd
  exact shorter_fiber_divisible_by_eight_of_longer_nonempty
    Y e W (W - 1) W htarget (by have hW := htarget.1; omega) hlonger

#print axioms shorter_fiber_divisible_by_eight_of_longer_nonempty
#print axioms not_both_width_fibers_odd
#print axioms short_fiber_mod_eight_of_long_nonempty

end CompleteFiberParity
