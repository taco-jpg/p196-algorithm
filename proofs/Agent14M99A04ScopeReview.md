# Agent #14 — M99-A04 ordinary-decimal bridge review

## Evidence level

SOURCE REVIEW COMPLETE; INDEPENDENT EXECUTION BLOCKED. The accompanying Lean regression fixture 和 Python replay driver are UNEXECUTED. Neither a new proof nor an independently rebuilt proof is claimed by this patch. The reviewed Agent #112 package retains its own author-checking evidence; this review does not replace that evidence or silently upgrade it to integration.

Inspected repository snapshot: `4ebec327707ff89454f4ade3d15ee1eb8dc3ce9c`.
Original package manifest blob: `46bd9549d00fd63f558a4ddd12937bd6d511f6c3`.
Current accepted-registry blob: `90221ac6053b5584602fed24eb93f7984359dff5`.
The companion `Agent14M99A04Manifest.json` identifies each of eight original source blobs, its SHA-256, imports, nineteen original endpoints, 和 six regression endpoints.

## Correction of the withdrawn Agent #14 draft

PR #55 at `2a4e13d48cbd3e0e927e6f28c117d9eb3061e78f` must not be integrated as bridge evidence. Its `Witness` requires one terminal trace to be both `constant six` 和 `constant twelve`. Those assumptions contradict each other before any spatial path or decimal arithmetic is considered. Calling that interface precise was incorrect. The draft PR has been closed, not merged; the branch 和 historical source have not been rewritten.

The correction fixture explicitly diagnoses that failure. It does not disguise the same assumptions in another witness structure. The original actual/numeric theorem is checked against its complete intended type instead.

A second correction concerns the outside boundary. Agent #9's `root = (0,1,1,7)` is a special boundary, not the ordinary zero-position outside cut. Agent #112 derives `physicalOutside = (0,0,0,0)` 和 invokes Agent #9's generic `no_finite_path`. Requiring the actual cut to equal the special `root` would be an incorrect bridge target.

## Source identity, not merely similar names

The original Agent #112 manifest 和 the current `ACCEPTED_BUILD.json` record identical identities for both key dependencies:

- `LychrelDigitSums`: Git blob `8a865176625283648a8a20dd2411ed77670eb0a2`; SHA-256 `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`.
- `AlternatingScalarBoundary`: Git blob `03c2e377b669b90d39cf5dc4c2983acee18eea27`; SHA-256 `e94e12e50cd381a0f666f9d2fb5e733087881532f7ff21c92bfc46add9356e85`.

These comparisons were made from fetched repository records. The numeric foundation was additionally read at the historical source path whose returned blob is exactly the current registered blob. Its `Lychrel196.step` is `n + reverse10 n`; `orbit` iterates that operation from time zero, continuing after palindromes. `reverse10` implements decimal reversal with the standard removal of leading zeros from the reversed numeral.

The registered foundation defines `columnSum d L i = d i + d (L-1-i)`, incoming carry recursively from zero, 和 output by remainder modulo ten. Thus the reviewed bridge uses the current registered decimal model, not a newly substituted dynamical system.

The current registry explicitly has `catalogue_complete = false`. Absence of a package from this registry alone does not prove that it was rejected or lacks other acceptance records. Conversely, preservation under `proofs/archive` does not establish current accepted-build inclusion. Agent #112's own manifest calls this package author-checked, with independent review/integration not established there. No later complete acceptance record was found in the targeted search; that search is not claimed to be an exhaustive repository-wide census.

## Exact arithmetic transport

The reviewed import closure is:

`LychrelDigitSums` + `NoAlternatingReturn` → `ActualMapObligations` → `ActualStrip`; then `ActualStrip` + `AlternatingScalarBoundary` → `ActualInfiniteStrip` → `NumericStrip` → `All`.

`qAt` 和 `widthAt` are projections of the original `OverflowCarryNormalization.iterPairs`, not free traces assumed to resemble an orbit. `admissible_at` invokes the existing iteration-admissibility theorem.

At spatial cut `i` 和 temporal pair `j`, `orbitSlot` uses the actual carries at ordinary times `2*j` 和 `2*j+1`. Every reflected carry uses its own time's width. The delayed coordinate is

`z = (extended oddWord oddWidth (oddWidth-i) : Int) - (carry oddWord (oddWidth-i) : Int)`.

This is integer subtraction. Replacing it with truncated natural subtraction would change the cut relation.

`actual_tile` supplies all fields of the exact Agent #9 `Tile` relation. Bounded actual carries give the slot bounds 和 `e` bit bound. Bounded pair sums give the `q`/`r` bounds. The high odd-column carry identity 和 the delayed digit give `r_value`, `low_forces`, 和 `high_forces`. Actual folded carry transitions supply `low_n`, `low_o`, 和 `high_n`. Nonoverflow emission supplies `n_emission`; overflow emission supplies `o_emission`. In the last expression, `outer.z + e` is the actual delayed digit, giving the required `pending_digit` bound rather than an assumed auxiliary number. The next-time coefficient is at `2*(j+1)`, rewritten from the actual successor time, without cyclic wrap.

The hypotheses here include the true terminal carry at the even step being zero 和 at the odd step being one. The code does not infer that schedule from the names of the band phases.

## Outside 和 aligned interior cuts

At cut zero, both low carries are zero. The even high carry is the assumed nonoverflow carry zero. The odd extended terminal digit 和 the odd terminal carry are both one, so their difference is zero. This gives `physicalOutside`, not the special `root`.

For an interior cut, `constant_cut_reset` uses two adjacent equal coefficients 和 the symmetry of an admissible pair word. Its hypotheses explicitly include `0 < i`, `i < L`, `c ≤ 18`, 和 `c ≠ 9`. The coefficient nine is excluded because an incoming carry can affect its carry reset. The delayed digit is derived from the adjacent reflected column, not silently identified with the current column.

Specializing those proved reset equations to six at the even time 和 twelve at the odd time yields slot `(0,1,0,2)`, exactly `six`. Reversing the two phases yields `(1,0,1,6)`, exactly `twelve`. `actual_six_tail` 和 `actual_twelve_tail` use a fixed positive cut 和 the same adjacent indices at every temporal pair. A time-varying cut would not satisfy their stated interface.

`no_actual_persistent_alternating_band` then applies Agent #9's generic reverse-rigidity theorem to `physicalOutside`, checking its distinction from the regular 和 exceptional slots. It does not re-prove or re-own Agent #9's generic obstruction.

## Finite-period transport is a separate theorem

`ActualStrip.actual_prefix_transport` discharges the exact Agent #104 `ActualPrefixTransportObligation`. For `Fin N` time indices, `cyclic_even_value` handles the final-to-first seam using the explicit return of the entire outside prefix after `2*N` ordinary updates. It does not equate an arbitrary finite path endpoint to its beginning.

`no_actual_alternating_prefix_return` therefore concerns positive finite `N`, a common interior cut, the actual alternating carry schedule, the specified globally aligned band, 和 a forbidden prefix return. Without that prefix-return assumption, the finite strip theorem cannot be applied to an arbitrary finite forward path.

The stronger nonperiodic theorem uses `Nat` time indices 和 Agent #9's forward-infinite path theorem. It requires neither temporal periodicity nor returned-prefix closure. These are distinct results with distinct hypotheses; they must not be conflated.

## Numeric correspondence 和 remaining applicability hypotheses

`NumericStrip.numeric_representation` obtains a canonical representation of the exact pair iterate from `iterPairs_representation`. It identifies the width by canonical decimal length 和 identifies the digits by bounded positional-value injectivity. It then transfers the mirrored pair sums only at in-width indices. Arbitrary values of a digit function outside its canonical width remain irrelevant.

`no_numeric_persistent_alternating_band` transfers both widths 和 the entire terminal carry through those derived equalities. The numeric/pair-word correspondence is proved, not an extra premise of the final theorem.

The final theorem still expressly assumes: canonical digits of the ordinary orbit; one fixed positive interior cut; valid width guards at both times in every temporal pair; actual terminal carries zero then one; 和 one global orientation of the adjacent six/twelve band. Its tail hypothesis is `(forall j, orientation A) or (forall j, orientation B)`, not `forall j, orientation A or orientation B`.

No blocking semantic mismatch was identified in the read bridge sources at this exact scope. This conclusion does not prove that an arbitrary complementary-band return certificate supplies the common cut or the alternating overflow schedule. That broader applicability question remains distinct. Neither a universal two-phase certificate exclusion, a successful infinite-safe certificate instance, decimal Lychrel existence, nor the claim for 196 follows from this bridge alone.

## Existing regression controls retained, not claimed as new discoveries

The source contains kernel-`decide` controls with the following intended meanings. They were read, not freshly executed here.

`15 → 66 → 132` has one nonoverflow/overflow pair 和 the adjacent band, but the outside prefix changes from six to three. It is a control against incorrectly treating finite-time alternation as cyclic prefix closure.

`1330 → 1661 → 3322` has middle pair-sum coefficients six then twelve but two consecutive nonoverflow steps. It is a control against inferring the overflow schedule from a local phase change. It is not, by itself, a counterexample to every possible strengthened all-time implication.

## Replay package

The new `Agent14M99A04ScopeRegression.lean` is an UNEXECUTED type/scope regression file. It checks the exact numeric endpoint signature, both original Agent #104 contracts, the distinct outside boundary, 和 the defect of the withdrawn simultaneous-tail interface. The fixture does not define a new orbit, introduce an axiom, or import the withdrawn draft.

`Agent14M99A04Replay.py` is an UNEXECUTED sequential replay driver. It reads the exact retained Git blobs, checks Git identities 和 SHA-256 values, verifies the two current-registry matches again, stages an empty project, checks the specified Lean release/commit, compiles all eight original modules plus the fixture, 和 requires transitive axiom answers for all nineteen original endpoints 和 six regression endpoints. A missing answer, forbidden axiom, failed process, timeout, unexpected import list, stale output directory, or source mismatch is a failure. Parser self-tests include missing-output, duplicated-answer, 和 forbidden-axiom negative controls. No self-test result is claimed from this authoring session.

Run from a clone that contains the patch objects 和 retained source blobs, using a trusted official Lean 4.19.0 installation:

```sh
python3 proofs/Agent14M99A04Replay.py --self-test
python3 proofs/Agent14M99A04Replay.py \
  --repo /absolute/path/to/p196-algorithm \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/new-isolated-agent14-output
```

An independently authenticated executable digest may additionally be enforced using `--expected-lean-sha256`. The driver records the actual binary digest; a version string alone is not compiler authentication. It writes exact commands, source/object/log hashes, exit statuses, axiom answers, 和 an overall status. It never marks main integration or repository-wide verification as complete.

## Actual execution limitation

Existing GitHub artifact `11948069575` from successful retained run `38682760398` was retrieved as `agent14-lean-checker-runtime.zip`. The repository metadata reports 377,764,368 bytes. Workspace materialization rejects artifacts above 104,857,600 bytes, 和 repeated container/Python access attempts failed before any Lean command ran. No extraction, checksum verification, compiler invocation, Python test, or clean rebuild is claimed. No new external computation or paid capacity was launched.

Agent Room #38 remains inaccessible through the exposed authenticated tools. The acknowledgment is UNSENT. No other issue, PR, or room has been created as a replacement chat channel. The PR #55 update is solely an object-specific correction of its own defective contents.

## Continuation queue

The immediately actionable execution task is the pinned replay above once a working local checker is available. After that, inspect the resulting transitive axiom answers 和 exact fixture types, then supply the verified patch to the single integration writer. Acceptance must be attached to the exact rebuilt source, not to this narrative.

Further unclaimed candidates are: an all-module environment census matching the nineteen endpoints; registration/path recovery for the exact archived closure; precise certificate-to-common-cut conditions; a qualified certificate-to-overflow-schedule implication that respects the 1330 control; 和 a finite nonperiodic horizon version of the reverse-rigidity obstruction. These are candidates, not reservations or completed results. Existing ownership must be checked again before substantial new theorem work.

Agent #14
