import P196.Sprint.Agent19.ArithTransfer
import P196.Agent118PrefixKernel.Conclusion217
import P196.Agent118PrefixKernel.Conclusion218
import P196.Agent118PrefixKernel.Conclusion777

/-!
# Agent 19 review: plain-arithmetic form of the Agent #118 exclusions of 217, 218 and 777

Applies the transfer lemmas of `ArithTransfer.lean` to the Agent #118 exclusions of 217, 218 and 777: for every time `t` and every
`k`, if `orbit 196 t` is a palindrome then `orbit 196 t / 10 ^ k` is not the excluded prefix.

-/

namespace Sprint.Agent19.Arith118

open Lychrel196 Sprint.Agent19.Fidelity Sprint.Agent19.ArithTransfer

theorem plain_217 : ∀ t k, Palindrome (orbit 196 t) → orbit 196 t / 10 ^ k ≠ 217 :=
  transfer118 (a := 2) (b := 1) (c := 7) (by decide) (by decide) (by decide) (by decide)
    Agent118.Finite217.no_196_217_palindrome

theorem plain_218 : ∀ t k, Palindrome (orbit 196 t) → orbit 196 t / 10 ^ k ≠ 218 :=
  transfer118 (a := 2) (b := 1) (c := 8) (by decide) (by decide) (by decide) (by decide)
    Agent118.Finite218.no_196_218_palindrome

theorem plain_777 : ∀ t k, Palindrome (orbit 196 t) → orbit 196 t / 10 ^ k ≠ 777 :=
  transfer118 (a := 7) (b := 7) (c := 7) (by decide) (by decide) (by decide) (by decide)
    Agent118.Finite777.no_196_777_palindrome

end Sprint.Agent19.Arith118

#print axioms Sprint.Agent19.Arith118.plain_217
#print axioms Sprint.Agent19.Arith118.plain_218
#print axioms Sprint.Agent19.Arith118.plain_777
