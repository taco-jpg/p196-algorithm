import P196.Sprint.Agent19.ArithTransfer
import P196.Agent124Prefix620.A124Prefix620Final

/-!
# Agent 19 review: plain-arithmetic form of the exclusion of 620

Applies the transfer lemmas of `ArithTransfer.lean` to the exclusion of 620: for every time `t` and every
`k`, if `orbit 196 t` is a palindrome then `orbit 196 t / 10 ^ k` is not the excluded prefix.

-/

namespace Sprint.Agent19.Arith620

open Lychrel196 Sprint.Agent19.Fidelity Sprint.Agent19.ArithTransfer

theorem plain_620 : ∀ t k, Palindrome (orbit 196 t) → orbit 196 t / 10 ^ k ≠ 620 :=
  transfer124 (a := 6) (b := 2) (c := 0) (by decide) (by decide) (by decide) (by decide)
    Agent124.CertPrefix620.no_196_620

end Sprint.Agent19.Arith620

#print axioms Sprint.Agent19.Arith620.plain_620
