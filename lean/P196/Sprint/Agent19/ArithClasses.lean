import P196.Sprint.Agent19.ArithTransfer
import P196.Agent124PrefixFiveSix.Agent124PrefixSummary

/-!
# Agent 19 review: plain-arithmetic form of the 33 three-digit classes

Applies the transfer lemmas of `ArithTransfer.lean` to the 33 three-digit classes: for every time `t` and every
`k`, if `orbit 196 t` is a palindrome then `orbit 196 t / 10 ^ k` is not the excluded prefix.
`classes_valid` shows every listed class is a genuine three-digit prefix.
-/

namespace Sprint.Agent19.ArithClasses

open Lychrel196 Sprint.Agent19.Fidelity Sprint.Agent19.ArithTransfer

theorem classes_valid : Agent124.PrefixSummary.classes.all
    (fun e => decide (1 ≤ e.1 ∧ e.1 ≤ 9 ∧ e.2.1 ≤ 9 ∧ e.2.2.1 ≤ 9)) = true := by decide

theorem plain_classes : ∀ t k, Palindrome (orbit 196 t) →
    ∀ e ∈ Agent124.PrefixSummary.classes,
      orbit 196 t / 10 ^ k ≠ 100 * e.1 + 10 * e.2.1 + e.2.2.1 := by
  intro t k hp e he
  have hv := of_decide_eq_true (List.all_eq_true.mp classes_valid e he)
  exact transfer124 hv.1 hv.2.1 hv.2.2.1 hv.2.2.2
    (fun t' => Agent124.PrefixSummary.no_196_all t' e he) t k hp

end Sprint.Agent19.ArithClasses

#print axioms Sprint.Agent19.ArithClasses.plain_classes
