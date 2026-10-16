# Prospective normalized-carry accounting: independent review plan

Status: READ-ONLY PLANNING, 2026-10-16. Prepared by Agent #6's runtime/reproducibility reviewer, separate from the authors within the same project. The proposed claim has not been independently compiled or proved in this planning pass. The work here consists of reading existing exact source, reasoning about its definitions, and specifying future acceptance gates. Only this planning directory was written.

## Main finding and proposed scope

The intended state-level identity appears to need only `Agent109.Bounded s.B`:

`Agent6.ExteriorCoordinates.overflowBit (Agent116.CertificateExterior.stateOuter s) = Agent109.Cert.gam s`.

This is a proposed interface, not a newly verified theorem. Its phase can be any natural number, and `s.A` and `s.C` can be arbitrary. There is no apparent need for `Phase s.c`, `s.c ≤ 18`, `s.c ≠ 9`, a positive head, nonempty exterior, canonical representation, realizability, or an accepted certificate at this state-level interface. A separate checker-facing consumer should take the original `check cert = true` as its sole certificate premise.

The reason to separate these two levels is concrete: the carry identity is local arithmetic on a bounded word, while the existing weighted-balance theorem obtains its closed orbit from the original checker.

## Exact definition chain

The consulted sources are the unchanged snapshots under `/workspace/scratch/f8aedc6d7adf/runtime-agent6/review-certificate/final/source/`, already bound in the preceding independent review to remote source commit `937c33ba3a98b9778bfee45a0bf2f0c0b3765055`. `SOURCE_RECEIPT.json` records the consulted files' observed bytes, SHA256 values, and Git blob hashes. This is a receipt for these local reads, not a new ownership or dependency census.

1. `Agent109.Cert.gam s` projects the `γ` field of `Agent109.data s.c s.B s.A s.C`. That field is exactly `(Agent109.norm s.B.reverse (Agent109.kOf s.c)).2`. Although other fields of `data` use `18 - s.c`, `A`, and `C`, the projected carry does not depend on them. Natural subtraction in those other fields does not impose a phase restriction on `gam`.
2. `Agent116.CertificateExterior.stateOuter s` preserves `s.c` and replaces `s.B` by the actual `P196.Agent7.Finite.stripSuffix s.c s.B`. This is maximal removal of a constant suffix, implemented by reversing, `dropWhile (fun x => x == c)`, and reversing again.
3. `Agent6.ExteriorCoordinates.overflowBit q` is the zero/nonzero indicator of `(highValue q.B + (if 10 ≤ q.c then 1 else 0)) / 10 ^ q.B.length`. It is not defined to equal a numeric final carry.
4. `Agent6.ExteriorCoordinates.overflow_eq_highValue` identifies that quotient with the actual `P196.Agent7.Finite.normalize` high-side final carry, for every phase and every finite natural-coefficient word. `Agent109.Outer.normalize7_eq` identifies this pair-valued normalizer with `Agent109.norm`. Both `phaseCarry c` and `kOf c` are the same `if 10 ≤ c then 1 else 0`.
5. `Agent109.gamma_le` bounds the original numeric carry by one under `Bounded B`, with no phase premise. Equivalently, `overflow_le_one` plus boundedness of the stripped word bounds the normalized numeric carry by one. This is the step that turns the zero/nonzero indicator into the numeric value.

Use the pair-valued `Agent109.norm` and `P196.Agent7.Finite.normalize` at this bridge. `TemplateStep` also has a word-valued `Agent109.normalize`; its name alone is not an adequate module/definition match.

## Suffix invariance and its precise limitations

For `c ≤ 18`, `Agent109.Outer.stripSuffix_spec` supplies an exact decomposition of the original word into its stripped word followed by copies of `c`. Reversing this decomposition places those copies at the beginning of the high-side scan. `Agent109.norm_band_tail` says that this constant prefix, starting with `kOf c`, finishes with the same carry `kOf c`. `Agent109.norm_append` then gives equality of the final carries on the remainder.

The existing `norm_band_tail` premise is only `c ≤ 18`; it covers phases 0, 9, and 18. Its use does not require boundedness of the remainder. The different lemma `norm_band` handles a more general incoming carry and has the additional premise `c ≠ 9`; that stronger interface is unnecessary here.

For `18 < c` and `Bounded B`, the word contains no occurrence of `c`, hence `stripSuffix c B = B`. One can also see this from `stripSuffix_spec`: a nonzero removed suffix would put a coefficient `c > 18` in the bounded original word. This branch supports the unrestricted-phase state identity.

The invariant concerns the final carry, the `.2` component. The full normalized digit lists generally have different lengths. The scan is on `B.reverse`; removing a suffix becomes removing a prefix before the scan. The original and normalized words are therefore not interchangeable in arbitrary low-side formulas.

The incoming carry must stay `kOf c`. A generalization to arbitrary incoming carry would require a different condition: at `c = 2`, word `[2]`, and incoming carry `1`, the original final carry is `0` while stripping to `[]` leaves final carry `1`.

## Empty words, boundaries, and certificate indexing

Both pair-valued normalizers satisfy `norm [] e = ([], e)`. Consequently an empty word at `c ≥ 10` has final carry one. In the quotient definition, its denominator is `10^0 = 1`, which gives the same value. Stripping a nonempty all-phase word to `[]` does not force zero carry. In particular, `c = 18, B = [18]` retains carry one, while `c = 9, B = [9]` retains zero.

The local state bridge can include phase 9, phase 0, and phases greater than 18. The checker's `LocalOK` uses the narrower `Phase` predicate. Those broader state controls therefore exercise the local bridge; they are not accepted-certificate witnesses.

`Certificate.P` is the length of `states`. `Certificate.st i` and `Certificate.lk i` use `getD i default`. `Valid` supplies `LocalOK` only for `i < cert.P`, and its `Bounded (cert.st i).B` premise is available at exactly those indices. The existing `sumPrefix_congr` has exactly the same in-range premise, so the sum consumer can avoid any assumption about out-of-range states. An all-index row theorem should explicitly handle the default branch if authors choose to expose it; it is not needed for the proposed sum.

The checker definition has no separate `links.length = states.length` conjunct. Its actual `getD`/`LocalOK` behavior should remain the interface, without adding such an equality premise. An empty certificate has `P = 0` and fails the checker's positive-period conjunct. Empty prefix sums themselves still have the ordinary zero value.

## Checker-facing consumer and arithmetic constants

The existing `CertificateCoordinates.rowOuter cert i` is precisely `stateOuter (cert.st i)`. The existing `Agent110.Accounting.totalGam cert` sums `(gam (cert.st i) : Int)` over the listed indices, using the original untrimmed certificate rows.

From `check cert = true`, `check_sound` supplies `Valid cert`; each in-range `LocalOK` supplies the bound on that original row's `B`. Applying the intended state identity and `sumPrefix_congr` should identify the normalized-row indicator sum with this unchanged `totalGam`.

Let `P = cert.P`, and let sums below denote the existing signed `sumPrefix` over `0, ..., P-1`. The planned direct consumer is:

`Σ weightedPhase (rowOuter cert i) = 9 * Σ weightedReverse (rowOuter cert i) + 9 * totalGam cert`.

It rewrites only the final sum in the existing `checked_row_weighted_balance`. The coordinate quantities stay evaluated on the normalized rows. This statement should have only `check cert = true` as its certificate premise.

If the existing `totalGam_eq_twice_gains` is also consumed, its premise is `Valid cert`, available from the same checker result. The final term becomes `18 * (totalG cert + totalH cert)` in `Int`. This is a substitution into an existing accounting identity, not a new source of the width identity or an independently discovered invariant.

These are necessary consequences of acceptance. They do not supply a converse for `check`, an accepted-certificate construction, or an existence result. The existing filter/failed-check controls already distinguish necessary conditions from acceptance.

## Small future control set

The following values are hand reductions of the inspected definitions. They have not been newly run in Lean. Set `A = C = []` where a complete `State` is wanted. A future claimed implementation can check these cases in the same final build as its exported statements.

| Purpose | `c` | Original `B` | `stripSuffix c B` | Original `gam` | Stripped numeric carry | Normalized `overflowBit` |
|---|---:|---|---|---:|---:|---:|
| Empty zero phase | 0 | `[]` | `[]` | 0 | 0 | 0 |
| Phase 9 is allowed locally | 9 | `[9]` | `[]` | 0 | 0 | 0 |
| Empty result keeps incoming one | 18 | `[18]` | `[]` | 1 | 1 | 1 |
| Bounded high phase needs no upper phase bound | 19 | `[18]` | `[18]` | 1 | 1 | 1 |
| Nonempty remainder and scan orientation | 2 | `[10, 2, 2]` | `[10]` | 1 | 1 | 1 |
| Missing boundedness: indicator loses magnitude | 2 | `[20]` | `[20]` | 2 | 2 | 1 |
| Missing both structural branches: raw carry changes | 19 | `[19]` | `[]` | 2 | 1 | 1 |

The last two are the important negative controls. The first unbounded case keeps the word unchanged but separates the numeric carry from its indicator. The second violates both `c ≤ 18` and `Bounded B`, and separates the two numeric carries. Its original indicator and normalized indicator are both one, so checking indicator invariance alone would miss this failure. The arbitrary-incoming-carry example above is only needed as a further negative control if the planned interface is generalized beyond `kOf c`.

## Minimal independent acceptance gates after a guarded claim

1. **Freeze the concrete interfaces and source.** The local state identity uses the actual existing projection and indicator and only the agreed boundedness premise. The check-facing sum/weighted consumer uses the original `check = true`. Inspect the optional gains coefficient and `Nat`-to-`Int` coercions. Take source hashes and the authors' resolved exact dependency registry; source/ownership census remains with landscape and claims.
2. **Review the two carry steps separately.** Check numeric carry invariance, then the bound that makes an indicator equal that carry. Review reversal order, `.2` projection, empty input, phases 0/9/18 and the high-phase branch, and in-range extraction from `LocalOK`. Use the small controls above to check those concrete risks; the two negative cases should remain failures of the deliberately weakened assertions.
3. **Perform one fresh independent final build and closure audit.** After author freeze, compile the exact resolved closure into a fresh object directory with the already verified genuine Lean 4.19.0, `--trust=0 -j1 -DElab.async=false`, through supported execution escalation. Audit module origins, every theorem and safe definition, and every declared public endpoint. Parse complete multiline `#print axioms` output and compare against the standard allowed set `propext`, `Classical.choice`, `Quot.sound`. Preserve actual commands, compiler/source/object hashes, logs, and any failure before revision. Count public statements separately from private helpers, generated constants, definitions, and numerical controls.
4. **Bind the successful frozen review to publication.** Compare the final reviewed source and dependency registry to the actual remote source commit, preserving all earlier receipts. The remote commit identity must be the published one even when a local commit has the same tree. Once the concrete gates pass, finish the evidence package; no extra test expansion is implied by this planning note.

The previous independent certificate review and its exact-source publication receipt remain the provenance for the consulted baseline. Its successful compilation is not a compilation result for these prospective new statements. The historical 25/1991 multiline receipt correction remains a log-parser correction with the same standard axiom union, not a theorem failure.
