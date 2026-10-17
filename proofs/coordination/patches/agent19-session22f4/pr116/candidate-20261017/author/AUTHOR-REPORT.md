# PR116 isolated original-map bridge candidate

## Scope and status

The isolated candidate proves the exact requested all-width statement for the original `P196.Agent6.Exterior`, original `P196.Agent6.Canonical`, and original `P196.Agent6.advance` from repository head `51f8f8d523eb8434b6a80ad7dc1e30fe63ab8378`:

```lean
theorem Agent19.TwoStep.canonical_phase_six_not_period_two
    (s : P196.Agent6.Exterior) (hs : P196.Agent6.Canonical s)
    (hphase : s.phase = 6) :
    P196.Agent6.advance (P196.Agent6.advance s) ≠ s
```

The source candidate is complete and passed author elaboration. Independent review remains a separate, pending activity. This report does not claim independent review, merge readiness, accepted main integration, or any broader 196-orbit theorem. Agent110 retains ownership of the original source branch. No remote mutation, comment, claim, or branch operation was performed by this proof author.

## Exact source preservation

The original definitions and original four helper modules are imported unchanged. `RawBridge.lean` adds `rawWord`, a direct projection of the original `advance` body. The equalities `advance_six` and `advance_twelve` are proved by `rfl`, ensuring that its use stays attached to the original state transition.

The final public theorem imports the unchanged original `Canonical` via `ExteriorCoverage`. Its proof extracts the original coefficient bound and the original fixed-trim condition. It invokes a stronger intermediate theorem for arbitrary coefficient-bounded words fixed by `trim 6`; the original predicate is neither weakened nor redefined.

## Proof structure

1. `RawBridge.lean` establishes normalization carry bounds and decimal output-digit bounds by induction on the original `norm` function. It proves raw successor length is exactly input length plus one, without any bound or monotonicity assumption. It proves every raw coefficient is at most 18 at phases 6 and 12.
2. The terminal-column lemma uses the existing `norm_snoc` and `zipWith_add_snoc`. The entering forward carry and reflected overflow are values computed by the original normalizations. For every nonempty input word it decomposes the exact raw output as a prefix followed by its penultimate and last coefficients. In the reflected-overflow case, the remaining reflected digit belongs to the normalized word (or is the leading digit 1), so it lies in 0 through 9.
3. `raw_six_tail` and `raw_twelve_tail` identify these exact terminal columns with the existing `firstLast`, `secondLast`, `firstPenultPossible`, and `secondPenultPossible` definitions from `BoundaryArithmetic.lean`.
4. The separately authored `TrimBridge.lean` proves that every original trim deletes exactly a suffix consisting of copies of the phase, preserves coefficient bounds, and leaves no surviving final phase coefficient. Combining the two exact raw lengths with a hypothesized state return yields `q + r = 2`.
5. For an original input of length at least 2, the first trimmed word remains nonempty: its length equals original length plus one minus `q`, and `q ≤ 2`. The proof obtains its terminal coefficient and bounds from the actual first successor.
6. `boundary_from_suffixes` handles the three possibilities `q = 0, 1, 2`. Exact equalities of last and penultimate coefficients force the already-defined Boolean `boundaryCandidate` to be true. Membership in all seven finite parameter ranges contradicts the existing kernel-proved `no_abstract_two_step_boundary`.
7. Empty and singleton words use the unchanged `ShortWidths.lean` results. The endpoint therefore covers every finite word length.

No width monotonicity is used; arbitrary deep contractions remain compatible with the proof. No alternative arithmetic model, chosen overflow, cap, axiom, admission, native decision procedure, or modified canonicality predicate is introduced in the final chain.

## Author verification

The official pinned executable is:

`/workspace/scratch/8b5152316f75/runtime-agent1/toolchain/lean-4.19.0-linux/bin/lean`

Runtime specialist verified Lean 4.19.0, commit `6caaee842e94`, and prepared exact-head source import objects separately. Final author elaboration used:

```text
--trust=0 -j1 -DElab.async=false -DmaxHeartbeats=2000000 -DmaxRecDepth=100000
```

The command was bounded by a 90-second timeout and completed in approximately one second. `evidence/BoundaryBridge-attempt005.exit` records the actual Lean/timeout exit code 0. The accompanying log prints the transitive axioms for `boundary_from_suffixes`, `bounded_trim_not_period_two`, and `canonical_phase_six_not_period_two`: only `propext`, `Classical.choice`, and `Quot.sound`.

This is an endpoint axiom receipt, not a claim that the author performed an independent exhaustive declaration audit. All earlier candidate source snapshots and logs are retained. Earlier wrappers ending in `cat` did not preserve a separate Lean exit status; `commands.json` records that limitation explicitly rather than inventing exits. Later runs preserve the exit immediately.

Two resource-wrapper failures are retained: BoundaryBridge attempt003 segfaulted when a 1.5 GiB virtual address-space restriction was imposed; attempt004 rejected Lean's `-M 1024` option because the executable reported the `max_memory` configuration unavailable. Neither changes the source candidate. Attempt005 used the already-established strict flags and succeeded. Failed elaboration logs can print `sorryAx` for incomplete candidates; none is present in the successful final endpoint axiom receipts.

## Frozen deliverables

`FINAL-MANIFEST.json` provides the exact SHA256 identities of the three new modules. `commands.json` records all ten author invocations, source snapshots, logs, module roots, import paths, and exit provenance. Source ownership and publication remain with the parent coordinator; this directory is solely the isolated preparation packet.
