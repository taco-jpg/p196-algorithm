import OuterFinite

/-!
Representation-completeness and existential first-exit wrappers for the
kernel-certified cap-2 graph. The digit and length hypotheses are explicit.
The actual whole-word-to-outer projection remains a separate written bridge.
-/
namespace P196.Agent7.Finite
set_option maxHeartbeats 0

theorem decode_complete (B : List Nat) (hlen : B.length ≤ 2)
    (hdigit : ∀ x ∈ B, x ≤ 18) :
    ∃ k : Fin 381, decodeWord k.val = B := by
  cases B with
  | nil => exact ⟨⟨0, by decide⟩, rfl⟩
  | cons a tail =>
    have ha : a ≤ 18 := hdigit a (by simp)
    cases tail with
    | nil =>
      refine ⟨⟨a + 1, by omega⟩, ?_⟩
      simp [decodeWord, Nat.ne_of_gt (Nat.zero_lt_succ a), show a + 1 ≤ 19 by omega]
    | cons b tail =>
      have hb : b ≤ 18 := hdigit b (by simp)
      cases tail with
      | nil =>
        refine ⟨⟨20 + 19 * a + b, by omega⟩, ?_⟩
        have h0 : 20 + 19 * a + b ≠ 0 := by omega
        have h19 : ¬20 + 19 * a + b ≤ 19 := by omega
        have hsub : 20 + 19 * a + b - 20 = 19 * a + b := by omega
        have hdiv : (19 * a + b) / 19 = a := by omega
        have hmod : (19 * a + b) % 19 = b := by omega
        simp [decodeWord, h0, h19, hsub, hdiv, hmod]
      | cons z zs => simp at hlen

theorem cap2_unencoded (p : Fin 8) (B : List Nat)
    (hlen : B.length ≤ 2) (hdigit : ∀ x ∈ B, x ≤ 18)
    (hvalid : validOuter {c := 2 * (p.val + 1), B := B} = true) :
    staysSmall 7 {c := 2 * (p.val + 1), B := B} = false := by
  obtain ⟨k, hk⟩ := decode_complete B hlen hdigit
  have he : encoded p k = {c := 2 * (p.val + 1), B := B} := by
    simp [encoded, hk]
  have h := cap2_exits_by_seven p k
  rw [he] at h
  exact h hvalid

def outerIterate : Nat → Outer → Outer
  | 0, s => s
  | n + 1, s => outerIterate n (outerNext s)

theorem exit_witness_of_false (n : Nat) (s : Outer)
    (h : staysSmall n s = false) :
    ∃ i, i ≤ n ∧ 2 < (outerIterate i s).B.length := by
  induction n generalizing s with
  | zero =>
    refine ⟨0, Nat.le_refl 0, ?_⟩
    simp [staysSmall] at h
    simpa [outerIterate] using h
  | succ n ih =>
    by_cases hs : s.B.length ≤ 2
    · have hn : staysSmall n (outerNext s) = false := by
        simpa [staysSmall, hs] using h
      obtain ⟨i, hi, he⟩ := ih (outerNext s) hn
      exact ⟨i + 1, by omega, by simpa [outerIterate] using he⟩
    · exact ⟨0, by omega, by simpa [outerIterate] using (show 2 < s.B.length by omega)⟩

theorem cap2_exit_witness (p : Fin 8) (B : List Nat)
    (hlen : B.length ≤ 2) (hdigit : ∀ x ∈ B, x ≤ 18)
    (hvalid : validOuter {c := 2 * (p.val + 1), B := B} = true) :
    ∃ i, i ≤ 7 ∧
      2 < (outerIterate i {c := 2 * (p.val + 1), B := B}).B.length := by
  exact exit_witness_of_false 7 _ (cap2_unencoded p B hlen hdigit hvalid)

#print axioms decode_complete
#print axioms cap2_unencoded
#print axioms exit_witness_of_false
#print axioms cap2_exit_witness
end P196.Agent7.Finite
