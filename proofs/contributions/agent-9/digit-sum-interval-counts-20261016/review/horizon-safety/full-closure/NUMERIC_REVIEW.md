# Independent numeric and complete-closure review

**Verdict: PASS. No mathematical source correction requested.**

Reviewer: Agent #9/horizon-safety, independently of the coverage-census proof
author. This addendum extends the earlier generic interval review to the ordinary
decimal specialization and its complete eleven-module project import closure.
The original generic review remains preserved in `prior-generic-review/`.

## Exact accepted statement

For every positive natural seed `n` and every natural threshold `B`, start `s`,
and length `N`, the pinned theorem proves

```lean
N / (DecimalUniformEscape.sharpDigitSumEscapeBound B + 1) ≤
  ((List.range' s N).filter
    (fun t => decide
      (B < DecimalMass.digitSum (Lychrel196.orbit n t)))).length
```

The endpoint is `P196.Agent9.IntervalCounts.digitSum_interval_count`.
`digitSum_interval_count_196` specializes it to seed 196, discharging positivity
with a checked proof. The numerator division is natural-number division. The
right side counts distinct qualifying times in the half-open interval `[s,s+N)`;
it is a lower bound, not an exact formula for that count.

The exact sources reviewed are:

| Module | SHA-256 | Git blob |
|---|---|---|
| Agent9WindowIntervalCounts | `597bfe85a6d5ee332aeaf96845e2dc7c96631080ec3a9c5c6c97f3ce17247ff9` | `efe4e98e937918b505edfe99e4f6d501be8019f4` |
| Agent9DigitSumIntervalCounts | `0747bb708957e9d3ab8a2f9afbe5e7222a3ca3daedccc2796d644831d9d7dad4` | `035e6ab3fea49810ccb3f50e5f8ebf426a847c15` |

Both sources remained byte-identical throughout the independent replay. Neither
was edited by this review.

## Mathematical inspection

The original `Lychrel196.step` is addition to ordinary base-ten reversal, and
`orbit n 0 = n`; each successor applies another reverse-and-add step. The orbit
has no stopping condition at a palindrome. `DecimalMass.digitSum` is the original
decimal recursion, with value zero at zero. These definitions are imported from
the exact historical `LychrelDigitSums` source; the contribution introduces no
replacement numeric model.

Write `F(B) = sharpDigitSumEscapeBound B`. The original theorem
`DecimalUniformEscape.digitSum_uniform_window_sharp` supplies a time `t` satisfying
`a ≤ t`, `t ≤ a + F(B)`, and the required strict digit-sum inequality. Over natural
times this is a witness strictly before `a + (F(B)+1)`. The new proof therefore
instantiates the generic window length with `F(B)+1`, which is positive for every
natural `B`. The `+1` is necessary because the original endpoint is inclusive.
Adjacent half-open blocks are disjoint, including when a witness lands on a block
boundary. The earlier generic review proves exact membership and absence of
duplicates in the counted list.

The generic proof counts one witness in each of the `N / (F(B)+1)` complete blocks
and then uses monotonicity when appending the remainder. It makes no extra claim
about a final short block. The seed hypothesis is exactly `0 < n`; no hypothesis
about avoiding palindromes or remaining in a symbolic language is hidden in the
numeric specialization. Positivity at shifted starting times is already supplied
by the original `orbit_positive` theorem inside the original window theorem.

### Endpoint and zero checks

The original generic review already covers exact half-open membership, absence
of duplicates, inclusion of the left endpoint, exclusion of the right endpoint,
empty intervals, `H=0`, `H=1`, and short remainders. The six checked declarations
in `Agent9DigitSumIndependentReview.lean` add the following numeric checks:

- `F(0)=0`, so the denominator at threshold zero is exactly one.
- For every positive seed and every `s,N`, the threshold-zero count is exactly
  `N`, including `s=0` and `N=0`.
- Every empty numeric interval has count zero, without requiring seed positivity.
- The orbit of zero stays zero at every time.
- The seed-zero orbit has no positive digit-sum excursions in any finite interval.
- Removing the positive-seed premise makes the asserted bound false already for
  `B=0`, `s=0`, and `N=1`.

These are review-only declarations. They are outside the eleven mathematical
modules and do not change the accepted theorem statements.

## Provenance and author evidence

The delivered author metadata files are `verify.py`, `dependencies.json`, and
`PROVENANCE.json`, together with `README.md`, `CHECKPOINT.md`, the author's audit
module, and `development/full-001/summary.json`. The requested names `check.py`
and `SOURCE_MAP` are not present; the delivered files serve those roles and were
inspected. Their exact snapshots and identities are preserved in
`author-metadata-snapshot/` and `setup-evidence.json`.

Each of the nine original dependencies was checked against both its original
commit/path and the corresponding Git object bytes at source commit
`2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. Their current flattened paths also resolve
to the same Git blobs at pinned main baseline
`4b4edf976b2c7a9ba1dad80636c0e21c66350325`; the read-only commands are recorded in
`main-baseline-pins.json`. The exact dependency graph appears in
`source-registry.json` and the generated run manifest.

The written argument is `proofs/research/continuation/strengthening_notes.txt`,
section 6, at the same source commit. Its Git blob is
`7103ee939d82740b970dd23fb91e9db50db4ea54`; its SHA-256 is
`15e07772d87cc4ee469541f4fb39ce1d0dce28ac5f630b16980c8abb02db258f`.
The commit/path, blob, and exact bytes were checked, and the source is preserved
as `strengthening_notes.source.txt`. The finite block count formalizes the finite
step underlying the written density discussion. No real-valued density limit is
an endpoint of this contribution. The written source initially states `B≥1`;
the imported original Lean theorem already permits `B=0`, and the independent
checks above verify that extra boundary case explicitly.

## Fresh kernel rebuild

The full independent run started at `2026-10-16T21:26:50.691862+00:00` and finished at `2026-10-16T21:28:41.205496+00:00`.
All eleven project modules and the generated audit succeeded on the first full
closure attempt. The output directory was newly created and contained zero
project compiled objects before compilation. Project sources were copied by
exact module name into an isolated source directory; `LEAN_PATH` contained only
the new build directory.

Compiler:

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
```

Executable SHA-256:
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Every project compilation used

```text
lean --trust=0 -j1 -DElab.async=false -o <fresh-module-output> <module>.lean
```

The generated audit used the same trust and elaboration flags. All exact command
arrays, working directories, exit codes, elapsed times, compiler records, and
log hashes are in `runs/full-closure-001/verification.json`. The status is
`PASS_SELECTED_SOURCE_CLOSURE`.

## Exhaustive module-origin axiom audit

The audit iterates the entire imported environment constant table, identifies
each declaration's recorded originating module, and selects the eleven project
modules by origin. It covers every theorem and every non-unsafe definition or
opaque constant in those modules, including private and generated declarations.
It rejects any safe custom axiom declaration even if unused, and rejects any
transitive dependency outside `propext`, `Classical.choice`, and `Quot.sound`.
The explicit endpoint list is used for type printing, not as an audit filter.

The exact audit checked **1,451 theorems and 178 safe definitions**:

| Originating module | Theorems | Safe definitions |
|---|---:|---:|
| Agent9WindowIntervalCounts | 10 | 1 |
| LychrelDigitSums | 986 | 148 |
| SharedProfile | 0 | 14 |
| ProfileDynamics | 145 | 1 |
| ProfileIsolation | 117 | 0 |
| UniformEscape | 45 | 5 |
| SharpProfileBounds | 61 | 0 |
| SharpUniformEscape | 39 | 5 |
| DecimalEmbedding | 38 | 3 |
| SharpUniformDecimal | 6 | 1 |
| Agent9DigitSumIntervalCounts | 4 | 0 |
| **Total** | **1451** | **178** |

The union of all collected mathematical axiom dependencies is exactly
`[Classical.choice, Quot.sound, propext]`. The two new modules contribute fourteen
theorem constants, because the seven user-written theorems have generated proof
helpers and an equation theorem; they contribute one safe definition,
`intervalCount`. These are declaration-audit counts, not counts of independent
major mathematical results.

The audit separately reports sixteen unsafe implementation axiom constants and
806 unsafe compiled implementation definitions. These are kept visible in the
log rather than included in the mathematical audit totals. None enters any
audited theorem or safe definition's axiom dependency set. The full literal audit
output is `runs/full-closure-001/logs/IntervalClosureAudit.log`, and the generated
source is `runs/full-closure-001/source/IntervalClosureAudit.lean`.

The checker was copied from the horizon contribution into this independently
owned review directory. Only its default paths, truthful reviewer label, and
audit filename were adapted; its audit logic was not changed. Both the upstream
checker and adapted checker are preserved. A read-only secondary inspection by
`/root/horizon_safety/interval_audit_logic` confirmed the module-origin traversal
and inspected the installed Lean `collectAxioms` implementation; that attributed
review is in `delegated-checker-review.json`.

### Verification scope

The pass concerns exactly the eleven registered project modules. The official
installed `Init`, `Std`, and `Lean` runtime is imported; the standard library was
not rebuilt from source. The checker records hashes of the compiler executable,
three runtime root `.olean` files, and top-level shared libraries. Its
`compiler_snapshot_unchanged` field means those recorded files stayed unchanged;
it is not a hash of every transitive standard-library object. Endpoint types
were printed and semantically compared with the pinned source by this review;
they were not compared to a separate mechanical type oracle. All selected source
files, copied sources, and the registry remained unchanged through the run.
No repository-wide verification claim is made.

## Preserved attempts and replay

`runs/full-closure-001/` preserves all exact selected source snapshots, generated
audit source, successful logs, source manifest, command records, and the original
run file manifest. Reproducible compiled binaries are omitted from this review
package; their original paths, sizes, and hashes remain in each run's
`preservation.json` and original file manifest.

The review-only boundary check had one failed attempt,
`runs/numeric-boundaries-001/`. A simplifier left a reduced zero-seed goal open in
the last review lemma; Lean exited nonzero and reported the temporary failed
proof's `sorryAx`. That attempt was rejected, and its exact source and logs remain
preserved. Replacing the simplifier step with explicit rewrites followed by
kernel `decide` closed the goal. `runs/numeric-boundaries-002/` records the final
success and permitted-axiom output for all six review declarations. No author
mathematical source changed, and this review-only failure did not affect the
already successful eleven-module gate.

To replay the complete gate from this review directory, with new output paths:

```sh
python3 -B verify_closure.py \
  --repo /absolute/path/to/p196-agent9 \
  --package-root /absolute/path/to/p196-agent9/proofs/contributions/agent-9/digit-sum-interval-counts-20261016 \
  --manifest /absolute/path/to/this-review/source-registry.json \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/new/interval-closure-output \
  --auditor 'Independent interval reviewer'
```

Then run the boundary checks against that successful fresh closure:

```sh
python3 -B verify_numeric_boundaries.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --closure /absolute/new/interval-closure-output \
  --output /absolute/new/interval-boundary-output
```

`SHA256SUMS` covers every preserved file in this addendum except itself. The
parent review manifest additionally covers the complete combined review tree.
No Git or external publication writes were performed by this reviewer.
