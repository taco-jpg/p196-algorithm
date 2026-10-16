# Agent #101: ordinary integer multiplicity of Agent #3's protected family

## Complete checked mathematical source

`Agent101.Protected.protectedSeeds m k` enumerates every ordinary integer digit
realization of the specific profiles `inputHalf xs k`, over all Boolean lists
`xs` of length `m`. The definitions of that family are reused unchanged from
Agent #3's finite-horizon-overflow contribution; their exact copies and source
pins are under `dependencies/agent3`.

`Agent101ProtectedMultiplicity.lean` proves complete membership, common input
width `2 * (m + k + 1)`, positivity, disjointness between different Boolean
profiles, duplicate freedom, and exact count `5 * 11^m`. Both `m=0` and `k=0`
are included. The local factor is 5 for the outer coefficient 14, while each
Boolean choice contributes 6 or 5 integer digit splittings.

`Agent101ProtectedPalindrome.lean` proves that this entire enumerated family
has exactly one initially palindromic member. It is `palindromeSeed m k`, whose
digit list is `[7] ++ replicate m 7 ++ replicate k 9` followed by its reversal.
Its existence is proved, not assumed. The general initial-palindrome theorem
from the companion Agent101 contribution is reused.

These modules count the realizations of this specified family. They do not
assert that it exhausts every second preimage of the common later target.

## Verification and continuation

Both mathematical source files were authored by the genuine specialist
`/root/numeric_bridge`; their accepted source hashes, Lean 4.19.0 commands,
zero-exit compilation and public-export axiom audits are under `counts/` and
`palindrome/`. Rejected author attempts remain clearly marked. Only the three
standard project axioms occur. Another genuine specialist independently rebuilt
the complete ten-module count dependency closure with `--trust=0`; its review
and the subsequent palindrome and filtered-count reviews all passed and are
retained under `reviews/`.

`Agent101ProtectedNonpalindromic.lean` now proves the filtered count
`5 * 11^m - 1`, complete numerical membership, duplicate freedom, positivity,
the exact input width, and nonemptiness, including `m = k = 0`.
`Agent101ProtectedFamily.lean` combines these results with a common explicit
second ordinary iterate `natValue (target m k)` and nonpalindromicity at every
time `0..k+1` when `0 < k`.

The finite horizon comes from Agent #3's original normalized safety theorems.
`Agent101NormalizationValue.lean` directly uses Agent #3's published
`digitValue_normalize` from `IntegerInterfaces.lean` at
`0be2a5aad6060d052141246d09bf05a8068f7c3e`; the underlying Agent109 proof
retains its attribution. `Agent101ProtectedSafety.lean` transports the first
value and shifts the original horizon by one ordinary reverse-add step.
The earlier independently checked SafeHigh normalization route remains
alternative development evidence, not a new value-preservation claim.

The complete final registry is `proofs/Agent101ProtectedFamily.registry.json`,
with 26 exact source modules. Its existing `verified_embedded_foundation`
adapter compares all 4,444 non-import lines of the original Research source
against the unchanged DigitSums source before building an import facade. This
avoids defining the original decimal arithmetic twice; no mathematical body is
edited. The author freshly built the 21-module arithmetic/safety closure and
then compiled all five additional counting/filter/endpoint modules with
`--trust=0`. The final combined exact-published-source rebuild and separate
review of the safety/endpoint modules have now both passed at the frozen
mathematical source `71691d50497edc83247b3571af276bb0ee438491`. The
21-module development report records a local snapshot, not publication of its
then-untracked files at its recorded base HEAD; the accompanying receipt makes
that limitation explicit.

## Final independent verification

The genuine nonauthor reviewer `/root/research_inventory` independently read
all 26 exact source files from the published commit, verified their registry
hashes and Git blobs, and ran the unchanged canonical verifier once from an
empty output directory. All 26 modules and the generated complete project
audit passed. The exact report and semantic review are retained in
`reviews/final-canonical-verification.json` and
`reviews/final-semantic-review.md`.

The original verifier did not explicitly request trust zero during its module
builds. The reviewer separately reran the unchanged ProjectAudit with explicit
`--trust=0`, covering all **1,783 module-origin theorems**, and performed a
separate explicit-trust-zero audit of **all 94 new public declarations: 85
theorems and 9 definitions**. Every public declaration is safe. The complete
axiom union is `propext`, `Classical.choice`, and `Quot.sound`. Compiler-generated
unsafe implementation axioms are reported separately and occur in none of
these mathematical dependencies. Source, registry, verifier and compiler
hashes were rechecked after the audits and remained unchanged.

The reviewer did not author the normalization, safety, final aggregate, or
three protected-counting modules. Authorship of the older SplitEnumeration
and generic PalindromeFibers dependencies is disclosed; their independent
reviews were supplied by different workers. This is a genuine within-session
review, not external-account approval or repository-wide certification.

Full retained evidence is recoverable from the archives: the runtime author
history in `archives/runtime-development.tar.gz`, the generic seven-module
reviews in the companion contribution archive, and the final canonical and
independent review corpus in `archives/final-independent.tar.gz`.
Manifests retain exact member hashes, failed attempts, and the historical
21-module snapshot limitation. The raw original reports are not rewritten.

Reproduce the final scoped closure from a checkout with Lean 4.19.0:

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent101ProtectedFamily.registry.json \
  --project agent101-protected-family \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/a-new-output-directory
```

Then run the generated `ProjectAudit.lean` using that generated source
directory as `LEAN_PATH` with `lean --trust=0 -j1 -DElab.async=false`.
The public audit source and exact original commands are included in the
independent archive. PR114 awaits the designated integration owner's review;
Agent #101 has not written main.

The final theorem is a family indexed by finite `m,k`. It does not produce one
fixed seed safe for all times or establish a conclusion about 196.

The successfully published task is
`agent101-protected-family-numeric-multiplicity-20261016`, claim commit
`5020db13f2d5dc3bef8a8074248c9873e1404ec5`. Agent #101 does not hold the main
integration slot.
