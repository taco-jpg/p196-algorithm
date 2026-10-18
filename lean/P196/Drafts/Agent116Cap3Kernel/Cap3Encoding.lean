import P196.Drafts.Agent116Cap3Kernel.Cap3Base

namespace P196.Agent116.Cap3
open P196.Agent7.Finite
set_option maxHeartbeats 0

theorem decode_complete (B : List Nat) (hlen : B.length ≤ 3)
    (hdigit : ∀ x ∈ B, x ≤ 18) :
    ∃ k : Fin 7240, decodeWord3 k.val = B := by
  cases B with
  | nil => exact ⟨⟨0, by decide⟩, rfl⟩
  | cons a tail =>
    have ha : a ≤ 18 := hdigit a (by simp)
    cases tail with
    | nil =>
      refine ⟨⟨a + 1, by omega⟩, ?_⟩
      simp [decodeWord3, Nat.ne_of_gt (Nat.zero_lt_succ a), show a + 1 ≤ 19 by omega]
    | cons b tail =>
      have hb : b ≤ 18 := hdigit b (by simp)
      cases tail with
      | nil =>
        refine ⟨⟨20 + 19 * a + b, by omega⟩, ?_⟩
        have h0 : 20 + 19 * a + b ≠ 0 := by omega
        have h19 : ¬20 + 19 * a + b ≤ 19 := by omega
        have h380 : 20 + 19 * a + b ≤ 380 := by omega
        have hsub : 20 + 19 * a + b - 20 = 19 * a + b := by omega
        have hdiv : (19 * a + b) / 19 = a := by omega
        have hmod : (19 * a + b) % 19 = b := by omega
        simp [decodeWord3, h0, h19, h380, hsub, hdiv, hmod]
      | cons d tail =>
        have hd : d ≤ 18 := hdigit d (by simp)
        cases tail with
        | nil =>
          refine ⟨⟨381 + 361 * a + 19 * b + d, by omega⟩, ?_⟩
          have h0 : 381 + 361 * a + 19 * b + d ≠ 0 := by omega
          have h19 : ¬381 + 361 * a + 19 * b + d ≤ 19 := by omega
          have h380 : ¬381 + 361 * a + 19 * b + d ≤ 380 := by omega
          have hsub : 381 + 361 * a + 19 * b + d - 381 = 361 * a + 19 * b + d := by omega
          have hdiv361 : (361 * a + 19 * b + d) / 361 = a := by omega
          have hdiv19 : (361 * a + 19 * b + d) / 19 = 19 * a + b := by omega
          have hmod19 : (361 * a + 19 * b + d) % 19 = d := by omega
          have hbmod : (19 * a + b) % 19 = b := by omega
          simp [decodeWord3, h0, h19, h380, hsub, hdiv361, hdiv19, hmod19, hbmod]
        | cons z zs => simp at hlen

/-- The base-19 decoder only emits words inside the specified cap. -/
theorem decode_length (k : Fin 7240) : (decodeWord3 k.val).length ≤ 3 := by
  unfold decodeWord3
  split
  · simp
  · split
    · simp
    · split <;> simp

#print axioms decode_complete
#print axioms decode_length
end P196.Agent116.Cap3
