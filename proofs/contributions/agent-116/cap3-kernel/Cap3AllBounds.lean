import Cap3AllFinite
import Cap3Encoding
import Cap3Bounds

/-! Unrestricted outer words, including leading-zero and nontrimmed words. -/
namespace P196.Agent116.Cap3
open P196.Agent7.Finite
set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem cap3_all_unencoded (p : Fin 8) (B : List Nat)
    (hlen : B.length ≤ 3) (hdigit : ∀ x ∈ B, x ≤ 18) :
    staysWithin 3 10 {c := 2 * (p.val + 1), B := B} = false := by
  obtain ⟨k, hk⟩ := decode_complete B hlen hdigit
  have he : encoded3 p k = {c := 2 * (p.val + 1), B := B} := by
    simp [encoded3, encodedAt, hk]
  have h := cap3_all_exits_by_ten p k
  rw [he] at h
  exact h

theorem cap3_all_exit_witness (p : Fin 8) (B : List Nat)
    (hlen : B.length ≤ 3) (hdigit : ∀ x ∈ B, x ≤ 18) :
    ∃ i, i ≤ 10 ∧
      3 < (outerIterate i {c := 2 * (p.val + 1), B := B}).B.length := by
  exact exit_witness_of_false 3 10 _ (cap3_all_unencoded p B hlen hdigit)

def allSharpStart : Outer := {c := 6, B := [0]}

theorem cap3_all_sharp_invalid : validOuter allSharpStart = false := by decide +kernel

theorem cap3_all_sharp_nine : staysWithin 3 9 allSharpStart = true := by decide +kernel

theorem cap3_all_sharp_tenth_state :
    outerIterate 10 allSharpStart = {c := 6, B := [18, 12, 7, 5]} := by decide +kernel

theorem cap3_all_sharp_first_exit :
    (∀ i, i ≤ 9 → (outerIterate i allSharpStart).B.length ≤ 3) ∧
      3 < (outerIterate 10 allSharpStart).B.length := by
  constructor
  · exact fun i hi => length_le_of_staysWithin 3 9 allSharpStart cap3_all_sharp_nine i hi
  · rw [cap3_all_sharp_tenth_state]
    decide

#print axioms cap3_all_unencoded
#print axioms cap3_all_exit_witness
#print axioms cap3_all_sharp_invalid
#print axioms cap3_all_sharp_nine
#print axioms cap3_all_sharp_tenth_state
#print axioms cap3_all_sharp_first_exit
end P196.Agent116.Cap3
