# Agent 7: odd-width no-overflow inverse fibers

Status: **ACTIVE / WIP**. This source checkpoint is part of ongoing research.

## Exact domain

For every half-width `m >= 0`, count distinct complete symmetric coefficient
words of width `2*m+1`, with coefficients in `0..18`, positive outer
coefficient, even central coefficient, actual final decimal carry zero, and
a prescribed image under the existing `Agent8.stepWord`.

The even-width theorem remains Agent 9's contribution. Final-carry-one fibers
remain Agent 2's scope, and protected overflow families remain Agent 3's scope.
No count here is a count of individual integers with identical pair sums.

## Current checked source

`OddWords.lean` proves that every odd symmetric finite list has the expected
half/center/reflected-half decomposition, that this representation is
injective, and that the central list entry is exactly the encoded center.
Its actual Lean 4.19.0 `--trust=0` build exited zero. The three printed axiom
sets are subsets of `propext` and `Quot.sound`. The complete source, failed
first attempt, successful second attempt, compiler logs, and execution receipt
are retained under `words-dev`.

The odd-center arithmetic, exact inverse enumerator, original-normalizer
bridge, and all-width sharp cardinality theorem are being developed separately.
They are not established by this checkpoint. A bounded exploratory formula
is not promoted to a theorem until the complete source and axiom audit pass.

## Imported source identity

`dependencies/SOURCE_PINS.json` records the original path, commit, Git blob,
and SHA-256 for every immutable imported source. Agent 9's original module
names and declarations are preserved byte-for-byte. Its five modules are
from coordination source checkpoint
`7be455c03d777e5e0ca1d44bea4d1330e3f764c7`. Agent 8's
`PeriodObstructions.lean` is exact blob
`a89dda20e9a9b3452f7d0272b4fbd28f7d6ce119` from source snapshot
`2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.

The new source is based on main
`4b4edf976b2c7a9ba1dad80636c0e21c66350325`. The published task claim is
`3c415e96dcc95c28752fd1deaf6ad3185a4690ba`; discussion and findings use
GitHub issue #61. The parent is the only Git writer. No default-branch
integration slot or accepted-build promotion is claimed.

## Verification scope

Pinned executable: Lean 4.19.0 release commit `6caaee842e94`, executable
SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
The complete contribution will receive a fresh import-closure build and
transitive axiom audit. Compiler-trusted computation shortcuts, new axioms,
and incomplete proofs are excluded from the accepted theorem chain.

The successful `OddWords` command and source/log hashes are in
`words-dev/attempt02.json`. Its first wrapper reported the final log-reader
exit status rather than the compiler status; `attempt01.log` visibly records
the rejected proof. Only the second explicit subprocess receipt is a
successful proof execution claim.

Infrastructure exclusions: runtime installations, copied `.olean` build
outputs, and operational publishing helpers. Research source, substantive
failed attempts, exact discovery outputs, and proof logs are retained.

Neither this finite inverse-fiber task nor a large fiber supplies a single
positive seed avoiding palindromes forever or resolves the orbit of 196.

