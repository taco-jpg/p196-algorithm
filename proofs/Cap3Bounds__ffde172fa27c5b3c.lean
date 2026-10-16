import Cap3Finite
import Cap3Encoding

/-! Unencoded cap-three exit theorem and exact sharpness witness. -/
namespace P196.Agent116.Cap3
open P196.Agent7.Finite
set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem cap3_unencoded (p : Fin 8) (B : List Nat)
    (hlen : B.length ≤ 3) (hdigit : ∀ x ∈ B, x ≤ 18)
    (hvalid : validOuter {c := 2 * (p.val + 1), B := B} = true) :
    staysWithin 3 9 {c := 2 * (p.val + 1), B := B} = false := by
  obtain ⟨k, hk⟩ := decode_complete B hlen hdigit
  have he : encoded3 p k = {c := 2 * (p.val + 1), B := B} := by
    simp [encoded3, encodedAt, hk]
  have h := cap3_exits_by_nine p k
  rw [he] at h
  exact h hvalid

theorem cap3_exit_witness (p : Fin 8) (B : List Nat)
    (hlen : B.length ≤ 3) (hdigit : ∀ x ∈ B, x ≤ 18)
    (hvalid : validOuter {c := 2 * (p.val + 1), B := B} = true) :
    ∃ i, i ≤ 9 ∧
      3 < (outerIterate i {c := 2 * (p.val + 1), B := B}).B.length := by
  exact exit_witness_of_false 3 9 _ (cap3_unencoded p B hlen hdigit hvalid)

/-- The known outer-map witness, now checked in the kernel. -/
def sharpStart : Outer := {c := 8, B := [11, 9]}

theorem cap3_sharp_valid : validOuter sharpStart = true := by decide +kernel

theorem cap3_sharp_eight : staysWithin 3 8 sharpStart = true := by decide +kernel

theorem cap3_sharp_nine : staysWithin 3 9 sharpStart = false := by decide +kernel

theorem cap3_sharp_ninth_state :
    outerIterate 9 sharpStart = {c := 10, B := [4, 9, 6, 6]} := by decide +kernel

theorem length_le_of_staysWithin (cap n : Nat) (s : Outer)
    (h : staysWithin cap n s = true) (i : Nat) (hi : i ≤ n) :
    (outerIterate i s).B.length ≤ cap := by
  induction n generalizing s i with
  | zero =>
    have hi0 : i = 0 := by omega
    subst i
    simpa [staysWithin, outerIterate] using h
  | succ n ih =>
    have hb : s.B.length ≤ cap ∧ staysWithin cap n (outerNext s) = true := by
      simpa [staysWithin] using h
    have hs : s.B.length ≤ cap := hb.1
    cases i with
    | zero => simpa [outerIterate] using hs
    | succ i =>
      have hn : staysWithin cap n (outerNext s) = true := hb.2
      exact ih (outerNext s) hn i (by omega)

theorem cap3_sharp_first_exit :
    (∀ i, i ≤ 8 → (outerIterate i sharpStart).B.length ≤ 3) ∧
      3 < (outerIterate 9 sharpStart).B.length := by
  constructor
  · exact fun i hi => length_le_of_staysWithin 3 8 sharpStart cap3_sharp_eight i hi
  · rw [cap3_sharp_ninth_state]
    decide

#print axioms cap3_unencoded
#print axioms cap3_exit_witness
#print axioms cap3_sharp_valid
#print axioms cap3_sharp_eight
#print axioms cap3_sharp_nine
#print axioms cap3_sharp_ninth_state
#print axioms length_le_of_staysWithin
#print axioms cap3_sharp_first_exit
end P196.Agent116.Cap3
