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

`OddCenter.lean` now proves exact parity-sensitive center acceptance and a complete,
duplicate-free path enumerator. `OddActual.lean` proves equivalence to the unchanged
`Agent8.stepWord` with actual normalization and actual final carry zero.
`OddCounts.lean` proves the all-width sharp path count
`oddMax m = (fib (m+1)+1)/2`, an attaining all-nine family, a positive-leading
11/9 family, and equality between path counts and enumerator lengths.
Each specialist preserved a fresh build, exported-theorem axiom output,
failed draft evidence, and publication manifest in its respective development
folder. The reported axiom union is exactly the permitted foundational set
`propext`, `Classical.choice`, `Quot.sound`.

`OddCanonical.lean` now checks the exact literal complete-word domain:
`fullOddPreimages_membership` is an if-and-only-if with `CanonicalOddFiber`,
without assuming a half-word encoding. The list is duplicate-free. Its
incremental build passed using pinned dependency objects from the separately
recorded clean bridge build. The width-one positive witness is `[[2]]` for
empty target half and target center digit 2. The first failed simplification
attempt is preserved. `OddSharp.lean` now proves complete canonical sharpness, an explicit attaining
family at every half-width, and exact prescribed-center maxima for positive
half-width. Its eleven exports compiled with the permitted foundational axioms.

Independent specialists have separately reviewed and rebuilt several
components; their exact source pins and semantic scope are retained in the
review records. This checkpoint is not integrated into the accepted build.

## Fixed-center refinement and arbitrary outputs

`OddCountsFixedCenter.lean` proves all-nine targets maximize each prescribed
center separately. `OddCountsPhase.lean` gives the exact six-phase formula:
when `m % 6 < 3`, even target center digits receive the ceiling of
`fib(m+1)/2` and odd digits the floor; in the other three phases the roles
reverse. At even Fibonacci values these agree. A completely explicit global
maximizer uses center digit 6 in the first three phases and 7 otherwise.
The canonical sharp family has target half `[11] ++ replicate (m-1) 9`
when `m>0`, and the source singleton `[[6]]` when `m=0`.
The source center is even; the target middle coefficient is twice its
prescribed normalized output digit. For fixed-center canonical maxima,
width one is handled separately because its zero-source candidate is removed.

The frozen extension sources have independent fresh rebuild and semantic
review evidence in `center-dev/review-extensions`. Every exported theorem
has an allowed axiom report, including the original counting declarations
which are not all literal print roots in the author file.

`OddComplete.lean` currently checks an explicit decoder and equality-guarded
enumerator for arbitrary output lists, together with its duplicate freedom,
uniform bound, attaining family, and impossible-target controls. Its actual
membership equivalence for arbitrary outputs remains pending the actual
output-range bridge. This checkpoint does not yet claim that final endpoint.

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

