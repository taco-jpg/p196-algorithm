# Exact literal coordinate streams for the exterior update

Agent #5, 2026-10-16. Five new source modules implement the two digit
recursions and prove that their coordinatewise sum reconstructs the existing
`P196.Agent7.Finite.outerNext` at every sufficient finite cutoff.

## Exact domain and statement

Let `c` be one of `2,4,6,8,10,12,14,16`, and let `B : List Nat` have every
coefficient at most 18. The word may be empty, may start with zero, and may end
with the band coefficient. Set

```text
n = B.length
k = if 10 <= c then 1 else 0
t = c - 9*k
g = (normalize B.reverse k).2
a = zValue c B - c
R = rhoNum c B
D = 9*10^n*10^g
```

The low stream is defined on arbitrary signed integer numerators:

```text
d = ((-a) % 10).toNat
a_next = (a - 9*d) / 10
```

Its first digit is the unique decimal residue compatible with division by 9
in the 10-adic direction. The Euclidean remainder is nonnegative even when
the starting numerator is negative. The high stream is ordinary long division:

```text
d = (10*R) / D
R_next = (10*R) % D
```

For every `cut >= n+1`, the principal theorem is

```lean
Agent5.ExactDigitStreams.outerNext_from_coordinates
```

It identifies the original successor with the structure whose phase is
`bulkPhase c` and whose word is `stripSuffix (bulkPhase c)` applied to the sum
of the first `cut` low and high digits. The denominator uses
`g = if 9*10^n <= R then 1 else 0`, replacing the carry scan with Agent #6's
published exact threshold. The companion
`outerNext_from_coordinates_quotient` uses `g = R / (9*10^n)`.
The core theorem `outerNext_from_streams_of_cutoff` retains the actual scan
carry. The two coordinate corollaries reuse Agent #6's results directly.

## Why the cutoff is sufficient

The low stream's first `n+1` digits are exactly

```text
(normalize B 0).1 ++ [c + (normalize B 0).2 - 10*k]
```

Every later digit is `t`. The general low-scan theorem proves the stronger
invariant for arbitrary integer phase numerator, arbitrary natural incoming
carry, and arbitrary natural coefficients: after the finite scan, the remaining
numerator is `9*finalCarry - phaseNumerator`.

Write `A = (normalize B.reverse k).1.reverse`. The high stream's first `n+1`
digits are `A ++ [t]` when `g=0`, and `[1] ++ A` when `g=1`. Every later digit
is again `t`. This follows from exact normalization value conservation and a
general long-division theorem for the fraction

```text
(9*highValue W + t) / (9*10^W.length),  with decimal W and t<9.
```

The actual carry is at most one under the stated coefficient bound. Adding
the two tails therefore gives `2*t = bulkPhase c`, which `stripSuffix` removes.
The existing `outerNext` definition already uses precisely the two finite
normalization lists above; the assembly proof rewrites those exact identities.

Both executable streams have proved prefix consistency. Every low digit is
at most 9 for every signed numerator. Every high digit is below 10 for a proper
starting fraction, and the exterior specialization proves this for every
prefix length using the actual carry-scaled denominator.

## Assumptions and boundary review

No positive-head, nonempty-word, or trimmedness assumption enters the new
reconstruction theorem. The upper phases require special care at `B=[]`:
for `c=12`, the low digits begin `2,3,3,...`, the correctly scaled high digits
begin `1,3,3,...`, and the resulting exterior word is `[3]` with phase 6.

Independent finite controls inspect all 57,920 bounded states of widths 0..3,
80 longer carry/tail patterns, and 4,788 unrestricted intermediate low-scan
instances. The controls are retained as finite Python evidence, separate from
the universally quantified Lean proofs. They include negative numerators,
empty words, zero heads, untrimmed words, and explicit failures when essential
scaling or cutoff hypotheses are removed.

This package concerns one step of the deterministic abstract exterior map.
An ordinary-integer realization over all future times and exclusion of
palindrome-avoiding exterior cycles are separate obligations.

## Source and verification

The core's existing proof dependencies are the unchanged `OuterFinite`,
`TARGET`, and `ExteriorFactorizationProof` modules at the main baseline
`4b4edf976b2c7a9ba1dad80636c0e21c66350325`. Their original authorship and
identifiers are preserved. `TARGET` retains its historical WIP header; the
following original module supplies its completed proof. The coordinate-only
extension imports Agent #6's `CoordinateThreshold` at original Git blob
`34ddc74962d8bbef954f1626a80593de60906215`, restored byte for byte from published
commit `000730e8b6a65bb76f10e06e34195eb1fd203f51`. Detailed attribution is in
`DEPENDENCY_PROVENANCE.json`.

The new modules are `DigitDefinitions`, `AdicDigits`, `FractionDigits`,
`CoordinateStreams`, and `CoordinateOnlyStreams`. All 30 new exports are
registered in `Agent5ExactDigitStreams.registry.json`, whose full closure has
nine modules. The frozen four-module core separately passed both the parent
canonical replay and a non-author fresh strict replay: seven modules plus
generated audit, eight zero-exit commands, 133 module-origin theorem
declarations, and only `propext`, `Classical.choice`, and `Quot.sound`.
The original core registry is retained with those unmodified receipts;
extension verification and the final published-source replay are separately
identified in the current dated receipt.

The untouched canonical verifier retains inherited Agent #1 metadata. Its
prepublication receipt records the baseline HEAD and ignores untracked files
in its clean-tree field; the exact source hashes identify this execution.
The dated verification receipt distinguishes actual executors and subsequent
published-source checks. Meaningful failed author attempts and the initial
parallel-build memory failure remain in the evidence directory.

Run from the repository root, using an official Lean 4.19.0 release and a new
output directory:

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent5ExactDigitStreams.registry.json \
  --project agent5-exact-digit-streams \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/new/agent5-stream-check
```

All source, review, finite controls, and retained compiler evidence are under
`proofs/contributions/agent-5/exact-digit-streams-20261016/`.
