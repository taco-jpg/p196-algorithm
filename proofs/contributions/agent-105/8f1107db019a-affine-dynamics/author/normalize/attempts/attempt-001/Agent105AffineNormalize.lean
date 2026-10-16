import Agent1RepeatedBlock
import Agent102RunDefs

/-!
Agent #105, session 8f1107db019a: actual decimal normalization of affine run words.

The constant-run identities below specialize Agent #1's exact repeated-block
normalization; all digit and carry operations are the original Agent8 operations.
No arithmetic update is replaced by a model. The shared run representation is
Agent102.RunSpec, whose signed affine lengths are expanded using Int.toNat.
-/

namespace Agent105.AffineNormalize

open Agent8 Agent102

/-- A singleton block power is the ordinary list replicate. -/
theorem singleton_pow (x k : Nat) :
    Agent1.RepeatedBlock.pow [x] k = List.replicate k x := by
  induction k with
  | zero => rfl
  | succ k ih => simp [Agent1.RepeatedBlock.pow, ih, List.replicate_succ]

private theorem bounded_singleton (x : Nat) (hx : x ≤ 18) : Bounded [x] 18 := by
  intro y hy
  simp only [List.mem_singleton] at hy
  simpa only [hy] using hx

/-- Positive constant runs have the outgoing carry of their first column.
The symbol nine and its incoming-carry dependence are included. -/
theorem terminalCarry_replicate_succ (x e k : Nat) (hx : x ≤ 18) (he : e ≤ 1) :
    terminalCarry (List.replicate (k + 1) x) e = (x + e) / 10 := by
  have h := Agent1.RepeatedBlock.terminalCarry_pow_succ [x] e k
    (bounded_singleton x hx) he
  simpa only [singleton_pow, terminalCarry] using h

/-- The actual first digit is retained; the remaining digits use the stabilized
carry, by the existing repeated-block theorem. -/
theorem fixedDigits_replicate_succ (x e k : Nat) (hx : x ≤ 18) (he : e ≤ 1) :
    fixedDigits (List.replicate (k + 1) x) e =
      [(x + e) % 10] ++ List.replicate k ((x + (x + e) / 10) % 10) := by
  have h := Agent1.RepeatedBlock.fixedDigits_pow_succ [x] e k
    (bounded_singleton x hx) he
  simpa only [singleton_pow, fixedDigits, terminalCarry] using h

/-- Exact full constant-run normalization, with the original appended overflow. -/
theorem normalize_replicate_succ (x e k : Nat) (hx : x ≤ 18) (he : e ≤ 1) :
    normalize (List.replicate (k + 1) x) e =
      [(x + e) % 10] ++ List.replicate k ((x + (x + e) / 10) % 10) ++
        (if (x + e) / 10 = 0 then [] else [(x + e) / 10]) := by
  rw [normalize_decompose, fixedDigits_replicate_succ x e k hx he,
    terminalCarry_replicate_succ x e k hx he]

/-- This incoming-carry formula includes zero copies of nine. -/
theorem terminalCarry_replicate_nine (m e : Nat) (he : e ≤ 1) :
    terminalCarry (List.replicate m 9) e = e := by
  cases m with
  | zero => rfl
  | succ m =>
    rw [terminalCarry_replicate_succ 9 e m (by decide) he]
    omega

theorem fixedDigits_replicate_nine (m e : Nat) (he : e ≤ 1) :
    fixedDigits (List.replicate m 9) e = List.replicate m ((9 + e) % 10) := by
  cases m with
  | zero => rfl
  | succ m =>
    rw [fixedDigits_replicate_succ 9 e m (by decide) he]
    have hc : (9 + e) / 10 = e := by omega
    simp only [hc, List.singleton_append, List.replicate_succ]

/-- Empty neutral runs retain the input carry; nonempty neutral runs retain
its digit effect. Neither zero columns nor the final carry are removed. -/
theorem normalize_replicate_nine (m e : Nat) (he : e ≤ 1) :
    normalize (List.replicate m 9) e =
      List.replicate m ((9 + e) % 10) ++ (if e = 0 then [] else [e]) := by
  rw [normalize_decompose, fixedDigits_replicate_nine m e he,
    terminalCarry_replicate_nine m e he]

end Agent105.AffineNormalize

#print axioms Agent105.AffineNormalize.terminalCarry_replicate_succ
#print axioms Agent105.AffineNormalize.fixedDigits_replicate_succ
#print axioms Agent105.AffineNormalize.normalize_replicate_nine
