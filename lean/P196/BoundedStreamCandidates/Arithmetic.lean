import P196.BoundedStreamCandidates.Definitions

/-!
# Selecting a low positional value from its residue

A value below twice its width scale has only two possible lifts from its
residue. The scale is one modulo nine, so compatibility with the high
positional value distinguishes those lifts. This scalar argument supplies
the executable selection used by each carry guess.
-/

namespace Agent5.BoundedStreamCandidates

open Agent115.ExteriorFactorization

/-- The modulo-nine comparison recovers the unique compatible low value
below twice the width scale, including a zero requested width. -/
theorem restoreLow_correct (M V H : Nat)
    (hV : V < 2 * 10 ^ M) (hmod : V % 9 = H % 9) :
    restoreLow M (V % 10 ^ M) H = V := by
  let P := 10 ^ M
  change V < 2 * P at hV
  unfold restoreLow
  change (if (V % P) % 9 = H % 9 then V % P else V % P + P) = V
  by_cases hsmall : V < P
  · rw [Nat.mod_eq_of_lt hsmall, if_pos hmod]
  · have hlarge : P ≤ V := by omega
    have hresidue : V % P = V - P := by
      rw [Nat.mod_eq_sub_mod hlarge, Nat.mod_eq_of_lt (by omega)]
    have hlift : V % P + P = V := by omega
    have hrepunit : 9 * highValue (List.replicate M 1) + 1 = P := by
      have hr := rhoNum_append_replicate 1 ([] : List Nat) M
      have hz : rhoNum 1 [] = 1 := rfl
      rw [List.nil_append, hz, Nat.mul_one] at hr
      exact hr
    have hPmod : P % 9 = 1 := by omega
    have hne : (V % P) % 9 ≠ H % 9 := by
      intro heq
      have h := congrArg (fun x : Nat => x % 9) hlift
      change (V % P + P) % 9 = V % 9 at h
      rw [Nat.add_mod, hPmod] at h
      omega
    rw [if_neg hne]
    exact hlift

#print axioms restoreLow_correct

end Agent5.BoundedStreamCandidates
