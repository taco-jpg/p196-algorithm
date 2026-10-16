# Agent 7: complete odd-width no-overflow inverse fibers

Status: **LEAN-CHECKED; final review and canonical replay PASS**. The complete
arbitrary-output theorem passed the separate fresh review build and the
retained canonical verifier at source commit
`af9ddce989030508e9fc2895f2f44fbbfcf2aed9`. The exact scoped registry remains
frozen. No accepted-build integration or main-write slot is claimed.

## Result and exact domain

Let `m >= 0` and let `r` be **any** finite list of natural numbers. The fiber
consists of complete coefficient words `q` satisfying all of the following:

- `q.length = 2*m+1` and `q.reverse = q`;
- every coefficient is in `0..18`, and the outer coefficient is positive;
- the literal central entry `q[m]` is even;
- the actual decimal scan from incoming carry zero has final carry zero;
- the unchanged repository function `Agent8.stepWord q` equals `r`.

`CompleteOddFiber m r q` is precisely this literal predicate.
`universalOddPreimages m r` is a computable finite enumerator. The final
`complete_odd_fiber_theorem` proves duplicate freedom, membership if and only
if that predicate holds, the uniform bound

```
(universalOddPreimages m r).length <= (fib (m+1)+1)/2,
```

and existence of an output attaining the bound at every `m`. Division is
natural-number division; `fib 0 = 0`, `fib 1 = 1`. The sharp maximum is thus
`ceil(F_(m+1)/2)` at complete width `2*m+1`.

These are counts of distinct **coefficient words**, not counts of individual
integer digit splittings having the same pair sums. The theorem concerns
one actual reverse-add update. It does not assert infinite palindrome
avoidance or resolve the orbit of 196.

## Explicit maximizing family

For positive half-width `m`, use target half
`[11] ++ replicate (m-1) 9`. Its target center digit is

```
sharpCenter m = if m % 6 < 3 then 6 else 7.
```

The complete target coefficient word is that half, followed by twice the
center digit, followed by the reversed half. Every enumerated source has
outer coefficient five, so the positive-head filter removes none of them.
For `m=0`, the attaining source family is exactly `[[6]]`, with target `[12]`.
`sharpFamily_exact` proves full membership, duplicate freedom, and length.

The stronger prescribed-center maximum is also established. If `v` is the
central digit in the normalized output, the target's central *coefficient*
is `2*v`. At positive half-width:

| `m % 6` | Even `v` | Odd `v` |
|---|---:|---:|
| 0, 1, 2 | `ceil(F_(m+1)/2)` | `floor(F_(m+1)/2)` |
| 3, 4, 5 | `floor(F_(m+1)/2)` | `ceil(F_(m+1)/2)` |

When the Fibonacci number is even the two values agree. The same leading
11/9 target half attains the formula for **every** prescribed center.
`full_fixed_center_maximum` states this at `m=n+1`. Width one is separate:
the unfiltered zero-source candidate for center zero fails positivity.
All ten width-one centers were checked independently.

## Why the proof covers the full domain

The imported Agent 9 graph has four states carrying the two actual boundary
carry bits. For an odd center `z`, the central column must simultaneously
satisfy its carry equation, output remainder, coefficient bound, and evenness.
`center_iff` proves the exact criterion

```
low p = v.val % 2  and  z = v.val + 10*high p - low p.
```

This determines the center uniquely and preserves the boundary values zero
and eighteen. `OddCenter` proves complete path enumeration and duplicate
freedom. `OddActual` proves both directions of its equivalence to the
original normalizer and `Agent8.stepWord`; the converse reconstructs the
carry states from the actual scan.

For the count, a row vector `(a,b,c,d)` starts at `(1,0,0,0)`. The original
transition table has five exact symbol classes:

| Target coefficient | Next count vector |
|---|---|
| 9 | `(c, a+b, c+d, b)` |
| Other odd value | `(c, a, d, b)` |
| 0 | `(a, 0, b, d)` |
| 18 | `(a, c, 0, d)` |
| Other even value | `(a, c, b, d)` |

The final center accepts `a+b` for even `v`, and `c+d` for odd `v`.
A kernel-reduced 625-case certificate seeds coordinatewise domination by
the all-nine row after four symbols. Explicit growth inequalities propagate
that domination at every greater length; the shorter cases are checked
separately. The all-nine total is `F_(m+1)`, and its two accepted sums differ
by at most one. This proves the ceiling bound. A six-case recurrence for
opposite-coordinate differences gives the prescribed-center formula.

`OddWords` proves every symmetric list of the required odd length has a
unique half/center/reversed-half representation. `OddCanonical` transports
membership to the literal complete-word predicate and checks positivity on
`xs.headD z`, so the empty-half case uses the actual center.

Finally, `OddOutputRange` proves that *every* actual no-overflow output of
an odd-length input has the required target encoding. It needs neither
input symmetry nor a coefficient bound: scan digits are decimal remainders,
and pairing an odd digit list doubles its middle entry. `OddComplete`
computes a candidate encoding from any requested `r` and then checks exact
reconstruction. Its equality guard prevents modulo aliases. The range
lemma proves that a rejected target cannot have an admissible source.
Thus the final theorem quantifies over all output lists, with no assumed
encoding or hidden restriction on the target.

## Source and dependency identity

The ten new modules are `OddWords`, `OddCenter`, `OddActual`, `OddCounts`,
`OddCountsFixedCenter`, `OddCountsPhase`, `OddCanonical`, `OddSharp`,
`OddOutputRange`, and `OddComplete`.

`dependencies/SOURCE_PINS.json` preserves original path, commit, Git blob,
and SHA-256 for every imported source. Agent 9's five stored sources are
byte-identical to coordination checkpoint
`7be455c03d777e5e0ca1d44bea4d1330e3f764c7`. Their original module names and
identifiers are retained. Only four of those five are in the final root's
transitive closure; the stored `SharpMaximum` source is not a new dependency.
The fifth imported closure module is Agent 8's unchanged
`PeriodObstructions.lean`, blob
`a89dda20e9a9b3452f7d0272b4fbd28f7d6ce119`, from source snapshot
`2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.

The contribution began from main
`4b4edf976b2c7a9ba1dad80636c0e21c66350325`. Task ownership was published at
`3c415e96dcc95c28752fd1deaf6ad3185a4690ba`. PR #82 contains incremental
source checkpoints and original failed attempts. Communication uses issue
#61. No other agent's source or owned theorem was changed.

## Verification and replay

Pinned compiler: official Lean 4.19.0 release commit `6caaee842e94`, executable
SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Successful theorem audits contain only `propext`, `Classical.choice`, and
`Quot.sound`. No new axioms, incomplete proofs, or compiler-trusted proof
shortcuts enter the checked import closure. The 625-case base certificate
itself has no axioms.

`PROJECT_REGISTRY.json` pins the exact 15-module closure of `OddComplete`
and all 115 public new-module theorem endpoints. From the repository root,
use the current-layout verifier and a fresh, nonexistent output directory:

```bash
python proofs/verify_project__214bf7673efe116b.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --registry proofs/contributions/agent-7/odd-nooverflow-fibers-20261016/PROJECT_REGISTRY.json \
  --project agent7-odd-nooverflow-fibers \
  --output /absolute/path/to/new-odd-fiber-verification
```

The frozen registry SHA-256 is
`ca9d1fa657f6fc786fa14ed0df2456333280ee8a5eb1a58cadeebb902ff16926`.
It does not mark the repository-wide accepted catalogue complete.

The parent Agent 7 canonical replay completed successfully from
`af9ddce989030508e9fc2895f2f44fbbfcf2aed9`: all 15 modules compiled, all
115 public new-module endpoints were checked, and the module-origin audit
checked 450 theorem constants. Its recorded tracked-source clean flag is
true. A separate evidence inspection confirmed that the recorded commit
contains every registered source, the registry and the verifier at their
exact Git blob identities. The original
[canonical report](verification/canonical-001/verification.json) is retained
unchanged at SHA-256
`73b2589136626623121f50bafff87986b89e6bbf2b08399503edcb1422d76e64`.

The retained verifier initializes a historical report label `Agent #1`.
The [execution receipt](verification/AGENT7_EXECUTION_RECEIPT.json) identifies
the actual executor as parent Agent 7 `/root`, and records that `/root/runtime`
prepared the receipt by inspecting the completed evidence. Exact recorded
compiler commands and the reproducible outer invocation are separated in
[CANONICAL_COMMANDS.json](verification/CANONICAL_COMMANDS.json).

The separate fresh review execution used `--trust=0` in addition to the
canonical compiler's `-j1 -DElab.async=false` options. It checked the same
450 project theorem constants and 18 additional boundary fixtures, and
individually audited all 214 public project/fixture declarations. The
[final review](actual-dev/review-sharp/FINAL_REVIEW.md) records the literal
source-domain, decoder completeness, boundary cases and exact source pins;
its [execution report](actual-dev/review-sharp/final-001/verification.json)
has SHA-256
`2132ab2176dec34039ca22da1f461e5136d318a54e632154ac1458bd340b6d9d`.

Author attempts are retained in `words-dev`, `center-dev`, `actual-dev`,
`counts-dev`, `canonical-dev`, `sharp-dev`, `output-dev`, and `complete-dev`.
Specialists within the same Agent 7 collaboration tree cross-reviewed the
center, arithmetic, counting and complete-word results and ran separate
fresh builds. The final reviewer `/root/runtime` authored the imported
`OddActual` module and reviewed the parent-authored canonical, sharpness and
complete wrappers. This affiliation is explicit in the execution receipt
and suggested formal review comment. Exact reviewed source pins and actual
build commands are recorded in the review manifests. Failed
Lean runs remain visibly failed; compiler-inserted `sorryAx` in those
rejected logs is not part of the successful chain.

Publication manifests retain substantive drafts, discovery outputs, source
snapshots, compiler logs, and execution receipts. Byte-identical dependency
copies and reproducible compiled objects are excluded with source pins and
reasons. Runtime installations and operational publication helpers are
infrastructure. The first historical OddWords shell wrapper reported a
log-reader status; only its subsequent explicit subprocess receipt is
claimed as a successful execution.

The final publication packet is described by
[verification/PUBLICATION.json](verification/PUBLICATION.json), and
[FINAL_STAGE_FILES.json](FINAL_STAGE_FILES.json) is the flat repository-relative
list combining retained review and canonical evidence. Following disk
exhaustion, the parent reclaimed 256 previously hashed untracked compiler
objects, including the 15 canonical outputs. The unchanged
[cleanup receipt](verification/cleanup/COMPILED_OBJECT_CLEANUP.json) preserves
their identities. All Lean sources, original failed attempts, logs, generated
audit sources, reports and Git history remain preserved; publication packet
preparation did not rerun any proof build.
