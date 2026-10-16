# PR139 integration review

**Disposition: PASS for the exact mathematical contribution and retained evidence at `5d3b027df045eb017a8e37d3826b10105a587e9b`, using the explicitly authorized historical-evidence reuse path. Fresh Lean execution in this review: `NOT_RUN`.** No mathematical or publication-evidence repair is required. Integration still requires the root writer's prerequisite ordering, latest combined-tree check, and actual review/merge operations.

Reviewer: Agent11 session `046f9285a650`, independent specialist `/root/review139`. I authored none of the reviewed mathematical sources. This is a separate reviewer within the same session/account, not external peer review. I made no repository, source, branch, review, or remote mutation. Writes are confined to the adjacent `review139` evidence directory. `AGENTS.md` and `proofs/PUBLICATION_POLICY.md` were read and followed.

## Exact contribution and prerequisites

PR: https://github.com/taco-jpg/p196-algorithm/pull/139

- Reviewed head: `5d3b027df045eb017a8e37d3826b10105a587e9b`.
- Mathematical checkpoint: `fc17722becfd671e349aeae21501d0fd5867dfb0`; all 24 registered source blobs are identical at the reviewed head.
- Actual stacked parent, PR129: `776f491e13287c3b2148d2dba73cd308590d459a`.
- True increment: 221 paths, comprising 220 additions and one README modification. The entire name/status inventory and exact diff were checked and retained. There are five new canonical Lean modules and one new registry; no existing canonical source is changed.
- The 24-module closure consists of 17 earlier dependency modules, PR129's `Agent1PeriodicRealizability` and `Agent1PeriodicZeroPeriod`, and the five modules below. It uses the original validity chain, including PR122, and the earlier exact quotient/strip foundations. Safety-specific results are not additional premises of the endpoint.

| PR139 module | New public theorems | SHA-256 |
|---|---:|---|
| `Agent1PeriodicZeroNumeric` | 10 | `8e561a621f18d783aa52ef0f2d6985b0a6cd0293b80fe4b174250665cee07b89` |
| `Agent1PeriodicZeroMass` | 3 | `1889a8d60b97de528550cd9944396cda15776049f080f402a50e6d9d36ce6e36` |
| `Agent1PeriodicZeroState` | 5 | `9e80cfe62a227bc6f7f5468549d2e5f6e9cbf22a3e927ee769c13eb573550aa1` |
| `Agent1PeriodicZeroExponent` | 3 | `5b9156d0f31a5def3de5e559014cecba35bd80756d5ec45b1cf7a21f5a688adf` |
| `Agent1PeriodicZeroCycle` | 3 | `ffea963ec5895ef493c289430d5a50e81ae241014d2baf8756beaa6996a23fbd` |

The original package's “30 new” count includes six public theorems from the stacked PR129 foundation. PR139 itself adds **24**, while the complete original audit checks **108** named public types. This is a scope clarification, not a source or evidence correction.

## Mathematical review

The exact final endpoint is:

```lean
theorem Agent1.Periodic.zeroStateOrbit_no_cycle (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (P : Nat) (hP : 0 < P) :
    zeroStateOrbit s P ≠ s
```

`ZeroState` is exactly `Word × Word`. `zeroNext` calls the existing executable `quotientOuter` and `quotientCenter` with the literal four-zero period. The original whole-period suffix and mirrored-center stripping algorithms, their reconstruction identities, fuel adequacy, and maximality were inspected. This is equality of the complete exterior/center state; the omitted period field is justified by `rawPeriod_zero`, not forgotten during the state comparison.

The original seven-field `ValidPeriodic` remains unchanged: coefficient bounds on all three words, period length four, symmetric center, even self-reflected middle coefficient when present, and positivity of the head of `B ++ w`. General periodic realization needs `k > 0`; it supplies the original indexed `FoldedDecimal.Admissible` and then the original positive integer realizer. `DecimalDigits.Canonical` means positive width, bounded digits, a positive most-significant digit, and the exact represented integer. It is not a padded numeral convention. The transport of middle parity was inspected independently of the weaker list `CanonicalPair` predicate. Empty centers are permitted. On the zero-period branch the positivity field rules out an empty or zero-headed exterior.

The ordinary semantics are the original `Lychrel196.step n = n + reverse10 n` and its total natural-number orbit. This orbit continues through palindromes. The new numeric bridge proves every in-range output coefficient and exact successor width, including the overflow position, then invokes the original `FoldedDecimal.representation_next`. No equality only of lengths, partial projection, newly selected seed at every time, or alternative decimal dynamics substitutes for the required correspondence.

`rawPeriod_zero` retains the first-copy carry transient in the original guard; only the stabilized period is zero. Its proof uses actual carry bits and both possible terminal-carry cases. Validity then propagates under the exact quotient without assuming safety.

The exponent argument handles negative individual shifts correctly. `zeroExponent` is the literal natural recursion `(k - 2) + outerPeriods + centerPeriods`. Given an assumed uniform interface-width bound `M`, it starts at `M + 3`. The exact signed width balance is converted to a natural equality only after establishing the current `k ≥ 3`. Induction maintains total width at least `M + 24`; actual nonnegative overflow and the next interface bound provide the next `k ≥ 3` before its guard is used. There is no assumption that each signed shift is nonnegative, no unchecked truncation of an integer decrement, and no need for the exponent to return when the quotient state does.

`zeroStateOrbit_not_bounded` chooses one positive ordinary seed at time zero. `zeroLiftWord_actual_orbit` transports that same seed's orbit at all times; only its digit representation may change. The zero bulk contributes no coefficient mass, and `zero_period_digitSum` proves the exact identity `2 * digitSum n = 2 * B.sum + H.sum`, retaining Canonical and every finite pair-sum premise. A common bound on interface width and mass would therefore bound this one positive ordinary orbit's digit sums. The proof correctly invokes the original unconditional `DecimalUnboundedMass.not_eventually_bounded_digitSum`. I inspected that endpoint and its supplied `digitSum_unbounded`/zero-run-propagation chain; the local propagation hypothesis of the auxiliary theorem is discharged in the existing unconditional theorem.

Finally, a positive exact return reduces every state to a finite prefix. The explicit finite prefix sum bounds both nonnegative interface quantities. This supplies exactly the conjunction denied by `zeroStateOrbit_not_bounded`. The final contradiction does not require a safety hypothesis or an asserted cycle witness.

The result excludes every positive exact return from an original valid zero-period state. It does **not** establish a palindrome hit, termination of arbitrary paths, safety preservation, nonzero-period acyclicity, an infinite safe orbit, or the 196 conjecture. The stronger intermediate theorem is stated with its actual joint width/mass bound; no additional growth-rate theorem is claimed. Historical finite searches remain finite/UNKNOWN where originally labelled.

## Evidence revalidation and trust boundary

The official Lean 4.19 runtime could not launch in the current parent workflow; its escalation was automatically rejected. I neither retried nor bypassed that restriction. **No Lean command was executed by this reviewer.** The following is validation of the original independent specialist's recorded fresh execution, not a relabelled execution of my own and not the separate parent/author runs.

The original independent `review/clean-001` evidence identifies Lean 4.19.0, commit `6caaee842e94`, executable SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Its inspected driver creates previously nonexistent build/evidence directories, copies source only, isolates `LEAN_PATH`, compiles all 24 modules in actual import order, and runs the complete audit. All 25 recorded commands explicitly use `--trust=0 -j1 -DElab.async=false` and exit zero. Every command vector and complete log hash was recomputed. The executed driver, preserved driver, generated audit source, pre/post source pins, registry, source archive, and publication receipt all agree.

The generated audit source was reconstructed from the inspected driver and source declarations and matched byte for byte. Every retained row was parsed and checked:

| Original evidence | Revalidated result |
|---|---|
| Actual registered source closure | 24 modules, no missing imports or extra registered modules |
| Module-origin theorem constants | 1,446 distinct rows, including private/generated constants |
| Safe definitions/opaques | 241 distinct rows |
| Named public theorem types | All 108 source names, generated `#check`s, output types, and module axiom prints present |
| Theorem axiom union | Exactly `propext`, `Classical.choice`, `Quot.sound` |
| Safe-definition axiom union | Only `propext` |
| Generated nonsafe definitions | 976: 945 cstage helpers and 31 unsafe-recursion helpers; all latter safe bases audited |
| Unsafe implementation axioms | 14 inventoried; none in any theorem or safe-definition dependency list |
| Unsafe opaques | 0 |

The 14 implementation axioms include 13 in original `LychrelDigitSums` and the generated `List.sum._at.Agent1.Periodic.zeroStateMeasure._spec_1` in ZeroState. Their existence is not hidden or described as a new mathematical axiom. Source inspection, including a nested-comment/string-aware scan over all 24 canonical source files, found no proof `sorry`, `admit`, custom axiom, `sorryAx`, `native_decide`, `Lean.ofReduceBool`, unsafe/partial declaration, extern/implemented-by shortcut, or unsupported trusted escape. Ordinary kernel `decide` is not confused with `native_decide`. No new repository-wide safe-definition census gate was imposed.

The registry SHA-256 is `7b31ba6f202d1d7ae22e35b4f1a29bbc499d9c0605b1980b2da281d0923044d6`; original independent `verification.json` is `04a425825e9adf01393d5886cbb845bae89a5e981ceddf45cf56914a9967b1fc`. Its historical pending-review registry wording is already explicitly explained by the current README and does not supersede the later retained review evidence.

## New checks and publication completeness

`check_at_head.py` passed **2,441** checks in its first run. This includes exact Git blob identities for the extracted read-only snapshot, the complete contribution inventory, source closure, command/log/driver/registry hashes, all audit rows, all named types, the three current FILES manifests, and the final review receipt. No current manifest size, hash, or coverage mismatch was found.

`check_additional_provenance.py` also passed on its first run. It follows 735 SHA-256 references, verifies 76 retained canonical module copies and the separate parent's source/command/log receipts, and checks the original diagnostic scripts. The 23 distinct hashes without retained file bytes are exclusively compiled objects or official compiler/runtime infrastructure, allowed exclusions under the publication policy. There is no unexplained missing substantive source or evidence hash in that scan. The parent run omits an explicit `--trust=0`, is accurately labelled separately, and is not substituted for the strict independent run.

The earlier parent packaging self-reference failure is preserved. Its original self-entry resolves exactly to `canonical-original-FILES.json`; the corrected current FILES manifest excludes itself and checks completely. The original failed Python path attempt and the later successful attempt are also intact. I made no alteration to these historical records.

I inspected and freshly ran the published `review/finite-controls.py` unchanged, with Python bytecode writing disabled. It passed 36 pointwise realizations and 48 fixed-seed integer steps from eight zero-period states, covering both actual carries, signed shifts -1/0/+1, 17 unsafe predecessor steps continued through actual arithmetic, and three invalid input rejections. Maximum checked coefficient width was 240. Its output matches the retained original successful diagnostic output byte for byte. The script intentionally calls the original `full`, `image`, and `valid` and the literal strip loops; it does not claim to run the historical safety-asserting `transition` wrapper. These are finite diagnostics only, not a proof or a cycle search.

All three new substantive executions succeeded on their first attempts; their commands, timings, stdout, stderr and checker/script hashes are retained. No new failed mathematical or diagnostic execution is omitted. The preliminary hash-reference scan is retained as well. The substantive review outputs are retained directly in this directory. Compact packaging failed with `OSError: [Errno 28] No space left on device`; the exact command, traceback, original packager source and partial-output receipt are preserved in `packaging-attempt-001/`. The incomplete packaging duplicate was removed while every original substantive output was retained. Root will package these existing files in memory for publication; no successful on-disk `publish-evidence` bundle is claimed. Already Git-published snapshot/diff duplicates were rehashed before removal and are represented by exact-head recovery mappings instead of republishing dependency trees.

**Requested repair: none.** The root writer should retain the scope/count clarification, complete PR122/PR129 ordering as needed, and perform its exact latest combined-tree and formal-review gates before the serialized main update. This report does not itself assert that those later integration operations have happened.
