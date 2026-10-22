import P196.Sprint.Agent19.Fidelity
import P196.Agent124ForwardInvariant.A124W3Summary

/-!
# Agent 19 review: plain-arithmetic restatement of `Agent124ForwardInvariant`

`Agent124.FwdW3.no_196_excluded` says `¬ PalStartsL w (orbit 196 T)` for every word `w` of the
list `excluded` (277 words).  Here: every listed word is a genuine three-digit prefix
(length 3, digits ≤ 9, leading digit ≥ 1), so the exclusion is not vacuous, and it implies the
plain statement that no palindrome iterate of 196 has a truncation `orbit 196 T / 10 ^ k`
equal to the word read as a number.
-/

namespace Sprint.Agent19.ArithLight

open Lychrel196 Sprint.Agent19.Fidelity

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem excluded_valid :
    Agent124.FwdW3.excluded.all (fun w => validPrefix w && w.length == 3) = true := by
  decide +kernel

theorem forward_plain (T k : Nat) (hp : Palindrome (orbit 196 T)) :
    ∀ w ∈ Agent124.FwdW3.excluded, orbit 196 T / 10 ^ k ≠ fromDigits w := by
  intro w hw
  have hv := List.all_eq_true.mp excluded_valid w hw
  simp only [Bool.and_eq_true] at hv
  exact plain_of_valid hv.1 (Agent124.FwdW3.no_196_excluded T w hw) hp k

end Sprint.Agent19.ArithLight

#print axioms Sprint.Agent19.ArithLight.excluded_valid
#print axioms Sprint.Agent19.ArithLight.forward_plain
