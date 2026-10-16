# Conditional binary block contraction — first checked source

Protected Agent #3 task: `agent3-zero-clock-prefix-contraction-20261016`.
Claim: `b2deb5b97561cc63bce7a65ce3d244623ca4bb4a`.
Base: `8a67ea8204757cc4f80bf5f576e2cc8024bea97b` (Ready PR130).

`BinaryBlockCounts.lean` has passed an actual Lean 4.19.0 `--trust=0`
author compilation and all 17 explicit axiom reports, using the already
checked dependency cache. Its SHA-256 is
`ea504376835afca4d9f53fdaf24ad92a45932b50428f257290db37f199b11c9d`.
Only `Classical.choice`, `Quot.sound`, and `propext` occur. A fresh full
dependency build and independent semantic review remain later gates.

The module reuses the original `OverflowHorizon.allBits` enumeration and
counts the words whose deterministic run differs from an absorbing dead
state. It proves the state-dependent recursion, exact membership and
distinctness, the elementary `2^n` bound, and these conditional results:

* If every state has a rejected word of length `k`, then
  `S(q,n+k) <= (2^k-1) * S(q,n)`.
* Under the same explicit hypothesis,
  `S(q,k*b+r) <= (2^k-1)^b * 2^r`.
* The corresponding quotient/remainder bound holds for every finite `n`.

The rejected word may depend on the current state. The proof uses the
existing binary enumeration's recursion, so it does not assume a single
common forbidden block. The certificate premise has not yet been proved
for the concrete three-layer machine in this checkpoint.

The actual original-Local transition coverage, one-case regenerated
certificate, original three-Path prefix induction, and ActualFiber count
transport are being developed in separate owned files. Center acceptance
is separate from prefix survival. This checkpoint establishes no concrete
nine-column bound, mixed-clock conclusion, or all-time claim.

The first author attempt failed to normalize `k*(b+1)` in an arithmetic
subgoal; its source, compiler output, and rejected axiom report remain in
`development/counting/attempt001/`. The second attempt explicitly uses
distributivity and passes without warnings. All failed elaborations remain
outside the accepted module set.

`ownership/` preserves both read-only source scouts, exact source captures,
the remote claim and concurrent-head retry evidence. The original missing
full certificate is still accurately recorded as omitted metadata. New
witness data will be labeled regenerated and accepted only after kernel
checking. Original arithmetic relations and prior result attribution are
unchanged.
