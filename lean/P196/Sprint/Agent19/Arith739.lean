import P196.Sprint.Agent19.ArithTransfer
import P196.Agent104Prefix739.Conclusion739

/-!
# Agent 19 review: plain-arithmetic form of the exclusion of 739

Applies the transfer lemmas of `ArithTransfer.lean` to the exclusion of 739: for every time `t` and every
`k`, if `orbit 196 t` is a palindrome then `orbit 196 t / 10 ^ k` is not the excluded prefix.

-/

namespace Sprint.Agent19.Arith739

open Lychrel196 Sprint.Agent19.Fidelity Sprint.Agent19.ArithTransfer

theorem plain_739 : ∀ t k, Palindrome (orbit 196 t) → orbit 196 t / 10 ^ k ≠ 739 :=
  transfer739 SevenColumnKernel.Finite739.no_196_739_palindrome

end Sprint.Agent19.Arith739

#print axioms Sprint.Agent19.Arith739.plain_739
