# Agent #9: finite interval counts for decimal digit-sum excursions

This contribution formalizes the finite counting consequence of the preserved uniform digit-sum escape argument. It uses the repository's original ordinary-decimal orbit 和 its existing exact uniform escape theorem.

The latest build status, source hashes, exact compiler commands, exit codes, 和 transitive axiom reports are preserved in `development/full-001/summary.json` 和 its accompanying logs. The first generic module compiled successfully in `development/generic-001/`. Independent review 和 integration are separate steps.

## Exact numeric statement

Write `F(B) = DecimalUniformEscape.sharpDigitSumEscapeBound B`, the existing horizon `E(2*B)`. For every positive ordinary decimal integer `n` 和 all natural `B,s,N`,

```lean
N / (DecimalUniformEscape.sharpDigitSumEscapeBound B + 1) ≤
  ((List.range' s N).filter
    (fun t => decide
      (B < DecimalMass.digitSum (Lychrel196.orbit n t)))).length
```

`List.range' s N` enumerates exactly the half-open interval `[s,s+N)`. The statement includes `B=0`, `s=0`, 和 `N=0`. Division is natural-number division, so the lower bound is the number of complete windows that fit into the interval.

The source uniform theorem guarantees a witness in the inclusive interval `[a,a+F(B)]`. That is a block of exactly `F(B)+1` integer times. The denominator includes this `+1`; adjacent blocks share no endpoint.

The two numeric endpoints are:

```lean
P196.Agent9.IntervalCounts.digitSum_interval_count
P196.Agent9.IntervalCounts.digitSum_interval_count_196
```

The first assumes only `0 < n`; the second specializes it to the ordinary orbit of 196. Both use the unchanged definitions `Lychrel196.orbit` 和 `DecimalMass.digitSum`.

## Generic finite counting theorem

`Agent9WindowIntervalCounts.lean` imports only `Std`. For a decidable predicate `P : Nat → Prop`, a positive window length `H`, 和 the hypothesis

```lean
∀ a, ∃ t, a ≤ t ∧ t < a + H ∧ P t
```

it proves:

```lean
P196.Agent9.IntervalCounts.window_property_interval_count
```

with conclusion

```lean
N / H ≤ ((List.range' s N).filter (fun t => decide (P t))).length
```

The proof first derives exact additivity on adjacent intervals from `List.range'_append_1`, `List.filter_append`, 和 list-length additivity. One window witness contributes at least one. Induction then gives at least `J` qualifying times in an interval of length `J*H`. The interval containing the first `N/H` complete blocks is a prefix of `[s,s+N)`; appending the remainder cannot decrease the count.

No global choice of a witness sequence is assumed. The generic theorem's first checked transitive axiom union is `propext` 和 `Quot.sound`. These are permitted logical foundations, not a claim of axiom-free proofs.

## Existing arithmetic dependency

The numeric module applies:

```lean
DecimalUniformEscape.digitSum_uniform_window_sharp
```

from original `SharpUniformDecimal.lean`, selected in the current source tree as `proofs/SharpUniformDecimal__c7370132a3682d7b.lean`. Its existing statement already quantifies over every positive seed, threshold, 和 starting time. No actual-orbit premise is introduced or left uninstantiated here.

`dependencies.json` records the complete nine-module local import closure in build order, with original paths, current flattened paths, SHA-256, Git blob identities, 和 source commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. The files are copied without edits into a fresh build directory under their original module names. No new dynamics or substitute foundation is defined.

## Written source 和 ownership

The source argument is `proofs/research/continuation/strengthening_notes.txt`, section 6, original Git blob `7103ee939d82740b970dd23fb91e9db50db4ea54` at `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. The general counting argument is the finite block-counting step behind its density discussion. This contribution does not formalize the real density limit.

The parent recorded the narrow task claim at coordination commit `110eb82aeb06baaba420e144ecd21f8b21fd2886`, task `agent9-digit-sum-interval-counts-20261016`, with publication branch `formalize/agent-9/digit-sum-interval-counts-20261016`. The delegated proof author made no Git or remote writes. No novelty or external peer-review claim is made.

## Reproduction

Use the official Lean 4.19.0 release, commit `6caaee842e94`. Both build 和 report directories must be new. From this contribution directory:

```sh
python3 -B verify.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --repo-root /absolute/path/to/p196-algorithm \
  --build-dir /absolute/new/interval-build \
  --report-dir /absolute/new/interval-report
```

The checker verifies the release string 和 every source pin, copies no compiled objects, compiles the nine unchanged dependencies 和 all three new modules, then checks literal transitive axiom output for all seven new theorem declarations. It rejects an unexpected axiom, missing export report, failed compiler command, reused output directory, or changed dependency. The final audit also prints the exact three endpoint types.

All substantive source snapshots, successful compiler outputs, 和 any failed build records remain retained under `development/`. The only initial failure was an infrastructure launch against a scratch cwd that had not yet been created; no compiler ran in that failed launch. Its record is preserved. The unchanged generic source then compiled successfully. Compiled objects 和 temporary copied build trees are reproducible infrastructure outside this contribution.

`MANIFEST.sha256` covers this author's files, including `development/`, relative to this directory. Independently supplied files under `review/` carry their own manifests 和 are excluded from the author's manifest.

## Mathematical limits

The result gives a lower count of visits above each fixed digit-sum threshold in each finite interval. It does not prove that digit sums eventually stay above that threshold, that digit sums converge pointwise to infinity, or that average digit sums diverge. It introduces no real density-limit endpoint.

The integer orbit continues after palindromes, exactly as in the original development. No palindrome-avoidance theorem, infinite safe seed, or resolution of the 196 problem follows from this finite count.
