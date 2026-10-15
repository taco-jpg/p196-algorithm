# Independent review of the six-column Lean rank certificate

The source/table audit passes. This review does not rerun Lean or substitute
for the separate fresh kernel build in
`../2026-10-14-seven-step-extension-formal/`.

## Exact table and complete finite domain

`independent_rank_audit.py` parses the transparent Lean match definitions
without importing their generator. All 233 rows and 52 tables reconstruct
exactly the 48,013 ranks in the frozen `direct_six_graph.bin.gz` certificate.
Regenerating the ten generated Lean modules in a temporary directory also
produces byte-identical sources.

The audit evaluates the six-column recurrence on all 96,026 inputs and
compares every output with the independently preserved literal-integer
normalization controls. Exactly 61,731 inputs satisfy the next-prefix and
overflow conditions. Their ordered edge list matches the binary certificate,
and every accepted edge strictly decreases the parsed Lean rank. Phase rank
maxima are `26,25,24,26,25,28,27`.

Every one of the 133 `(phase, first free coefficient)` check chunks exists,
quantifies both remaining coefficients over `Fin 19` and the control over
`Bool`, and is used in the general `rank_decreases` theorem. All 19
phase-zero bound chunks are present and used. The aggregate imports all seven
phase files. Thus no phase, coefficient, or Boolean input is omitted.

The default branches in the transparent total functions cannot hide a legal
transition: the source phase is below seven, the target phase is reduced
modulo seven, and all six resulting coefficients lie in `0..18` for every
checked input, including rejected inputs. The formal actual-orbit interface
also supplies the three source-tail bounds from admissibility at every time.

## Actual-word interpretation and endpoints

The reviewed `SixPrefix.step` computes ordinary low digits from incoming
carry zero and ordinary high digits from the actual carry at `L-6`. Its
overflow branch shifts the reflected high digits by one and includes the
new leading digit one. The proof of `boundary6_step_exact` uses symmetry
and the actual carry recurrences; it does not assume independent boundary
windows. Consequently the stated width condition `6 ≤ L` suffices even
when the two observed windows overlap.

`ActualRank.actual_clock_edge` connects the computed target to the next
actual word and supplies both accepted-edge conditions. `ClockPaths`
extracts every intermediate boundary and overflow from two successive
seven-step return endpoints. `NoFourReturns.returns_force_clock` covers the
terminal time separately, so a sequence of `K` returns yields all `7K`
strict decreases, not merely `7K-1`. Natural-number descent then gives
`7K ≤ 26`, hence `K ≤ 3`. The canonical-representation corollary obtains
admissibility from the existing bridge. These conclusions concern the
specified boundary recurrence; they do not assert palindrome occurrence.

## Resume provenance issue found and repaired

The initial resume runner checked each module's own source, object, and log
hashes and the fixed external imports. It did not fingerprint dependencies
between `RankData`, the phase-check modules, the aggregate, and the final
rank theorem. A changed rank table could therefore leave a previously
successful phase record eligible for reuse. This was a general cache
provenance gap; discovering it does not establish that any source changed
during the ongoing fresh build.

The runner now records direct-import source/object fingerprints before each
compile, checks them again afterward, and requires them to match before
reuse. Legacy records without these fields are rejected. The collector now
checks recorded dependency object/log hashes and dependency fingerprints
rather than replacing recorded hashes with the current values.

`check_resume_provenance.py` exercises the public runner in temporary
directories using a synthetic dependency-sensitive compiler. An unchanged
resume reuses all ten modules. Changing only the temporary `RankData` source
recompiles all ten modules and reuses no stale dependent. Removing dependency
provenance from one legacy phase record forces that phase to recompile.
No real proof source or build object is modified, and no Lean process is
launched. These fixtures validate the repaired reuse decisions; they do not
retroactively certify the provenance of a legacy manifest. The separate
formal build must record any one-time reconciliation explicitly.

## Reproduction and status

From the repository root:

```sh
python -B proofs/contributions/2026-10-14-rank-review/independent_rank_audit.py
python -B proofs/contributions/2026-10-14-rank-review/check_resume_provenance.py
```

The two JSON reports record exact audited hashes and finite checks. Kernel
compilation, complete axiom collection, and the final numerical theorem count
are reported separately by the formal contribution's checker. This review
claims source/table agreement and repaired cache-reuse behavior, not an
unperformed kernel build.
