import P196.OddTargetPredecessorParity.NumericShift
import P196.OddTargetPredecessorParity.CandidateSimplification

/-!
# A closed form for complete predecessor parity at every odd target

Agent #6: the only source width that can contribute an odd number of
predecessors is selected by the target's boundary digits. Its exact
parity is a palindrome test on a shifted half-target in a stated range.
-/

set_option autoImplicit false

namespace OddTargetPredecessorParity

open DecimalDigits Lychrel196 CompleteFiberParity
open Agent105Predecessors9df76b

/-- An odd canonical target has an odd complete positive predecessor
count exactly when the selected shifted-half palindrome test accepts. -/
theorem odd_target_predecessor_odd_iff
    (Y : Nat) (e : Nat → Nat) (W : Nat)
    (hY : Canonical Y e W) (hodd : Y % 2 = 1) :
    (predecessors e W).length % 2 = 1 ↔
      candidateAccepts Y (selectedWidth e W) := by
  rw [complete_predecessor_odd_iff Y e W hY]
  constructor
  · rintro (ho | ho)
    · have hc := (odd_target_odd_decoded_iff Y e W W hY hodd).mp ho
      have hw := odd_decoded_selected_width Y e W W hY hodd ho
      rw [← hw]
      exact hc
    · have hc := (odd_target_odd_decoded_iff Y e W (W - 1) hY hodd).mp ho
      have hw := odd_decoded_selected_width Y e W (W - 1) hY hodd ho
      rw [← hw]
      exact hc
  · intro hc
    have ho := (odd_target_odd_decoded_iff Y e W (selectedWidth e W) hY hodd).mpr hc
    unfold selectedWidth at ho
    split at ho
    · exact Or.inr ho
    · exact Or.inl ho

/-- The exact complete positive predecessor parity of an odd target,
using only its digits and a directly specified integer palindrome. -/
theorem odd_target_predecessor_parity
    (Y : Nat) (e : Nat → Nat) (W : Nat)
    (hY : Canonical Y e W) (hodd : Y % 2 = 1) :
    (predecessors e W).length % 2 =
      if candidateAccepts Y (selectedWidth e W) then 1 else 0 := by
  have hiff := odd_target_predecessor_odd_iff Y e W hY hodd
  split
  · rename_i h
    exact hiff.mpr h
  · rename_i h
    have hnot : (predecessors e W).length % 2 ≠ 1 := by
      intro ho
      exact h (hiff.mp ho)
    omega

/-- The closed form applies to every duplicate-free list of all positive
ordinary predecessors, independently of its enumeration order. -/
theorem ordinary_complete_odd_target_parity
    (Y : Nat) (e : Nat → Nat) (W : Nat)
    (hY : Canonical Y e W) (hodd : Y % 2 = 1)
    (ns : List Nat) (hnd : ns.Nodup)
    (hcomplete : ∀ n, n ∈ ns ↔ 0 < n ∧ step n = Y) :
    ns.length % 2 =
      if candidateAccepts Y (selectedWidth e W) then 1 else 0 := by
  have hsame : ns.length % 2 = (predecessors e W).length % 2 := by
    rw [ordinary_complete_predecessor_parity Y e W hY ns hnd hcomplete,
      complete_predecessor_parity Y e W hY]
  rw [hsame]
  exact odd_target_predecessor_parity Y e W hY hodd

/-- At the selected source width the numeric range is automatic, so
the complete parity reduces to a width gate and one palindrome test. -/
theorem odd_target_predecessor_parity_simple
    (Y : Nat) (e : Nat → Nat) (W : Nat)
    (hY : Canonical Y e W) (hodd : Y % 2 = 1) :
    (predecessors e W).length % 2 =
      if 2 ≤ selectedWidth e W ∧
        Palindrome (shiftedHalf Y (selectedWidth e W)) then 1 else 0 := by
  simpa only [candidateAccepts_selectedWidth_iff Y e W hY hodd] using
    odd_target_predecessor_parity Y e W hY hodd

/-- The simplified palindrome test is independent of how the complete
positive predecessor list is ordered. -/
theorem ordinary_complete_odd_target_parity_simple
    (Y : Nat) (e : Nat → Nat) (W : Nat)
    (hY : Canonical Y e W) (hodd : Y % 2 = 1)
    (ns : List Nat) (hnd : ns.Nodup)
    (hcomplete : ∀ n, n ∈ ns ↔ 0 < n ∧ step n = Y) :
    ns.length % 2 =
      if 2 ≤ selectedWidth e W ∧
        Palindrome (shiftedHalf Y (selectedWidth e W)) then 1 else 0 := by
  simpa only [candidateAccepts_selectedWidth_iff Y e W hY hodd] using
    ordinary_complete_odd_target_parity Y e W hY hodd ns hnd hcomplete

#print axioms odd_target_predecessor_odd_iff
#print axioms odd_target_predecessor_parity
#print axioms ordinary_complete_odd_target_parity
#print axioms odd_target_predecessor_parity_simple
#print axioms ordinary_complete_odd_target_parity_simple

end OddTargetPredecessorParity
