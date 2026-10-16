# Independent semantic validation of PR #136

## Verdict

**PASS for the mathematical source and advertised one-step inverse-cardinality result at exact head `429b2c34f2eb27eeeadd15b83036c78181430c03` (“H”).** I found no mathematical defect, weakened premise, omitted input-width case, or mismatch between the two final theorem statements and the advertised maximum.

This is an independent, read-only source review validating the existing qualifying review. I authored none of the four new modules or their dependencies. I did not change mathematical source, run Lean, rebuild a dependency closure, alter Git references, or post a remote review or comment. Actual execution and audit-log validation belong to the separate evidence review.

The existing final semantic review and structured verification receipt are present in H and explicitly report completed independent execution. The contribution README and PR body still describe that execution as pending. That is a **documentation-status inconsistency**, not a mathematical defect or a reason to repeat the build.

## Identity and inspected records

- Repository: `taco-jpg/p196-algorithm`.
- Reviewed PR: #136.
- Exact reviewed head: `429b2c34f2eb27eeeadd15b83036c78181430c03`.
- Mathematical freeze: `0fcbe9973659f178e9c834c68d45f660241d6fbd`.
- Registered root: `Agent101AllWidthMaximum`.
- Registry: `proofs/Agent101AllWidthMaximum.registry.json`.
- Independently recomputed registry SHA256: `496908a7d53c6a09b7a82dfae3c5e10339ef699072e5c97c0e591dc4e2c2cfcc`.
- Declared compiler: Lean 4.19.0, release commit `6caaee842e94`.
- Declared allowed logical axioms: `propext`, `Classical.choice`, `Quot.sound`.

I read the root `AGENTS.md`, `proofs/PUBLICATION_POLICY.md`, the contribution README, the current PR metadata/body, and these retained final records:

- `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/reviews/final-semantic-review.md`
- `proofs/contributions/agent-101/all-width-inverse-maximum-20261016/reviews/final-verification.json`

The PR metadata read during this review reports H as its head, PR #136 open and draft, and base branch `research/agent-101/nonpalindromic-protected-fibers-20261016T2123Z`. This review does not claim a merge or integration into `main`.

I fetched all 17 registered mathematical source files directly at H. Each GitHub-returned Git blob identifier matches its registry entry. I compared the source import declarations with the registry mappings; they agree.

For the nine modules already materialized in the parent’s local snapshot—four new modules, two Agent105 modules, and three Agent2 modules—I additionally recomputed SHA256 and Git blob hashes from the local bytes. All match. The remaining eight modules were read through exact-H connector responses; I do not claim an additional local SHA256 recomputation for those eight.

The four new modules were also fetched at the mathematical freeze and compared with H. Both their contents and Git blob identifiers are unchanged.

| New module | Source SHA256 |
|---|---|
| `Agent101ProfileExtraction` | `fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b` |
| `Agent101WidthFiberBounds` | `bebc285185d2f15138980dc2720b31fb0cbf476d9a30b1155545aca0c96a1bb2` |
| `Agent101MaximumWitnesses` | `d915b9df4e9ef3ab92ae9a33c3edd655b8567c40af7b88026e067408303182b7` |
| `Agent101AllWidthMaximum` | `9bbdc9351ccb72d2502ca303a7963c1b2aa1e50afd0e9f5d3d095305b34983d9` |

The registry lists exactly the 41 public declarations present in these four files: **36 theorems and five definitions**. I checked that there are no missing, additional, or duplicate endpoint names in that mapping. These are inventory counts, not counts of independent major results.

## Exact theorem scope

The main endpoint, `Agent101.Maximum.all_width_inverse_maximum`, states that for every natural `D` satisfying `2 ≤ D`:

1. For every natural target `Y` with `decimalWidth Y D`, and every duplicate-free finite list `ns` whose elements satisfy `0 < n ∧ Lychrel196.step n = Y`,
   \[
   \operatorname{length}(ns)\leq 9\cdot 10^{D/2-1}.
   \]

2. There exist a target `Y` of decimal width `D` and a duplicate-free list `ns` such that
   \[
   \forall n:\mathbb N,\quad
   n\in ns\ \longleftrightarrow\ 0<n\land \operatorname{step}(n)=Y,
   \]
   and
   \[
   \operatorname{length}(ns)=9\cdot 10^{D/2-1}.
   \]

Here `/` and `-` are natural-number division and truncated subtraction. Equivalently, the exponent in the stated domain is `floor(D/2) - 1`.

The upper bound is not restricted to the constructed witness target or to lists already expressed as a profile fiber. The attaining-list membership is an iff over **all natural numbers**, with no residual input-width condition. It therefore describes the complete positive ordinary-integer inverse fiber of the witness.

The separate endpoint `Agent101.Maximum.one_digit_inverse_maximum` supplies the universal bound one for one-digit targets and the complete attaining fiber `Y = 2`, `ns = [1]`.

Although the main endpoint phrases the universal bound using arbitrary finite predecessor lists rather than a `Finset.card` expression, this supports the advertised ordinary inverse-cardinality interpretation. From the actual definition `step n = n + reverse10 n`, every predecessor satisfies `n ≤ Y`, so the positive inverse fiber of any fixed `Y` is finite. The witness side additionally supplies its complete list directly.

These maximum results have no unsupplied orbit hypothesis, conjectural decoder premise, or arbitrary-profile realizability assumption. The domain hypotheses are exactly target width, positivity, predecessor membership, and duplicate-freeness where required. They do not assert an arbitrary-target enumeration algorithm, classify all maximizing targets, or establish an infinite palindrome-free orbit.

## Actual decimal semantics

The foundational file is the exact registered source `proofs/Lychrel196Research__c696e0ea3db39d92.lean`, logically imported as `Lychrel196Research`.

I traced the relevant proof chain through:

- `reverseAux`, `reverseFuel`, and `reverseFuel_correct`;
- `reverse10` and `Lychrel196.step`;
- `DecimalDigits.value`, `reflected`, `columnSum`, `carry`, and `output`;
- `reverseAux_value`, `reverse10_value`, and `step_value`;
- canonical representation existence and bounded-digit value injectivity;
- canonical no-overflow and overflow output representations;
- `FoldedDecimal.step_eq_word_value`;
- `ReverseAddInverse.symmetric_value_injective`;
- `ReverseAddInverse.same_width_step_eq_iff_pair_sums`.

The target map is the ordinary natural-number decimal operation
`n + reverse10 n`. Reversal consumes least-significant digits using division and remainder by ten; the correctness theorem ties the fuel-based implementation to the terminating decimal reversal. Positional reflection is connected to this actual reversal under canonical input hypotheses.

No identification with `Agent8.stepWord` substitutes for this semantics. That separate coefficient-word transition occurs in an imported Agent2 dependency, but the new maximum proof uses only Agent2’s general list-cardinality helper from that branch.

The canonical predicates enforce bounded decimal digits and a nonzero most-significant digit. They do **not** require a nonzero least-significant digit. Thus ordinary inputs ending in zero are included correctly; reversal naturally drops the resulting leading zeros.

The finite-list/function bridges restrict equalities to indices inside the declared width. This matters because `digitFn` zero-extends finite lists, while `reflected` uses natural subtraction. No proof here assumes an unjustified equality of their infinite tails.

## The four new mathematical steps

### 1. Finite profile extraction

`Agent101ProfileExtraction` proves that every finite symmetric list is expressible as

```text
h ++ c.toList ++ h.reverse
```

for a finite half `h` and optional center `c`.

The proof removes the actual first and last elements using strong induction on length. Reversal symmetry and `wrapDigits_injective` establish equality of those exterior elements and reversal symmetry of the interior. The interior is shorter by two. Empty and singleton lists are handled separately.

This reconstruction does not assume bounded coefficients, a positive numeral, or profile realizability. Those are not needed for the list decomposition.

For actual `digitPairSums`, the module proves reversal symmetry, preserves the entire pair-sum list, and tracks its exact length. Under `2 ≤ ds.length`, it exposes a nonempty half, identifies its first coefficient with the actual exterior `columnSum`, and proves that the remaining half has length `ds.length / 2 - 1`.

The extraction uses index zero only when the full length is at least two. The subsequent fixed-width transport uses zero and `L - 1`, with both indices proved valid.

### 2. Fixed-width ordinary-integer cardinality bounds

`Agent101WidthFiberBounds` begins with an arbitrary same-width ordinary predecessor and converts it to a canonical finite digit list.

The same-width step-equivalence theorem then identifies its complete pair-sum list with that of the chosen canonical representative. The existing `mem_numericFiber_digits` theorem supplies membership in the representative’s numerical profile fiber.

Consequently, the counted list is covered by the complete `numericFiber`; no numerical decoder or preassigned profile is assumed for all inputs.

The cardinality step directly calls:

```text
P196.Agent2.OverflowFibers.nodup_subset_length_le
```

Its proof is the general finite-list argument that erases one covered element at each induction step. Only the counted list must be duplicate-free; the covering list need not be. There is no overflow-specific premise or coefficient-fiber interpretation hidden in the application.

I fetched the three Agent2 modules and `PeriodObstructions` at their stated original commit `58afcada8047e015b8f4233b96c44c7c5b9c4162` and compared them with the registered H sources. All four contents and blob identifiers agree exactly.

The multiplicity calculation retains the exterior factor `pairCount true s`:

- the high digit of an outer pair is nonzero;
- interior ordered pairs have at most ten realizations;
- an absent center or valid even center has at most one realization.

This gives
\[
\operatorname{length}(ns)
\leq \operatorname{pairCount}(\mathrm{true},s)\,
10^{L/2-1}
\]
for `L ≥ 2`, and then the uniform outer bound nine.

The one-digit bound uses the empty-half center profile separately. In particular, the code does not apply a two-digit exterior-pair argument to a one-digit source.

The reused enumeration and numerical transport prove completeness and duplicate-freeness at the appropriate levels. Distinct canonical digit lists yield distinct natural values, so the product counts distinct ordinary integers rather than representations or infinite digit functions.

### 3. Complete attaining fibers

`Agent101MaximumWitnesses` defines:

- a half consisting of `D / 2` copies of nine;
- no center when `D` is even;
- center zero when `D` is odd;
- the corresponding symmetric target word;
- the existing complete numerical profile fiber as `maximumPreimages D`.

The parity proof establishes exact word length `D`. For `D ≥ 2`, both exterior digits are nine, so the target word is canonical and has actual decimal width `D`. Its units digit is nine.

The profile count is exactly nine exterior choices, ten choices for each remaining mirrored pair, and one center choice:
\[
9\cdot 10^{D/2-1}.
\]
It is positive, so a real member of the width-`D` fiber exists.

The critical completeness proof is `mem_maximumPreimages`. Its reverse direction starts with **an arbitrary positive natural number** having the witness target as its step value. It obtains that number’s actual canonical width `L` and obtains a genuine width-`D` predecessor from the nonempty constructed fiber.

If `L ≠ D`, the proof explicitly handles both strict orderings. In either ordering, the unchanged Agent105 theorem `cross_width_target_digits` forces the common target’s units digit to be one. This contradicts the constructed units digit nine. Thus `L = D`, and the existing fixed-width iff applies.

This is a valid elimination of additional widths, not merely an assertion that the displayed list happens to contain only width-`D` values.

For the one-digit witness, `one_digit_preimages` proves the complete iff for `[1]` and target two. The reverse direction uses `n ≤ step n = 2`; positivity leaves one and two, and `step 2 = 4` eliminates two. No unstated width assumption is used.

### 4. Uniform bound across both possible widths

`Agent101AllWidthMaximum` transports the actual-step width theorem to `decimalWidth`: every positive predecessor of a `D`-digit target has input width `D` or `D - 1`.

The proof partitions an arbitrary duplicate-free predecessor list into the Boolean filter for width `D` and its complement. Both parts retain duplicate-freeness. Every complementary member has width `D - 1`, and the reused filter-partition lemma gives the exact sum of lengths.

The branch structure is sound:

- If the width-`D` part is empty, the shorter fixed-width bound applies; width one is handled separately.
- If the shorter part is empty, the width-`D` bound applies.
- Representatives are selected only when both parts are nonempty.

In the two-nonempty branch, the original Agent105 results give:

- short exterior pair sum eleven;
- long exterior pair sum one;
- short width at least two.

The exact pair counts are eight and one. Therefore the two list lengths satisfy
\[
a\leq 8\cdot10^{(D-1)/2-1},
\qquad
b\leq10^{D/2-1}.
\]
Monotonicity of natural division and truncated subtraction gives
\[
10^{(D-1)/2-1}\leq10^{D/2-1},
\]
so their sum is bounded by the advertised ninefold power.

This argument works for both parities. It need not attain equality in the mixed-width branch: the separately constructed same-width family establishes the global sharpness.

I fetched both Agent105 modules at their stated original commit `5923015f86eb1ef898becd77ce2ee328ff338b69` and compared them with H. Both contents and blob identifiers are unchanged.

## Boundary and representation checks

| Case | Reviewed conclusion |
|---|---|
| `D = 2` | The bound is nine. The witness target is `99`; trailing-zero input `90` is allowed. A short width-one branch uses the separate bound one. |
| Both widths present with short width one | `cross_width_short_length` excludes this situation: a one-digit pair sum is even and cannot equal eleven. |
| Odd `D ≥ 3` | The central zero is an interior digit and has exactly one realization. Exterior nines preserve canonicality and positivity. |
| Even `D ≥ 2` | There is no center; the same exact count holds. |
| `D = 1` | Universal bound one, complete attainment at target two with predecessor list `[1]`. |
| `D = 0` | No maximum or attainment theorem is asserted. `decimalWidth` explicitly requires positive width. |
| Empty counted list | Included in the universal bound, with no representative selected from an empty list. |
| Zero as a candidate predecessor | Explicitly excluded by positivity in the complete membership iff and in the universal bound. |
| Leading-zero representations | Excluded by canonicality; they cannot inflate ordinary-integer counts. |
| Trailing-zero integers | Included; no erroneous nonzero-units restriction is imposed. |

These checks are readings and deductions from the reviewed definitions and proofs. They are not reports of additional numerical experiments.

## Registered dependency inventory

I inspected all four new sources and the relevant semantics throughout this exact 17-module closure:

| Logical module | Role in the reviewed closure |
|---|---|
| `Lychrel196Research` | Actual decimal reversal and step, canonical representations, carry/output semantics, symmetric coefficient-value injectivity |
| `Agent101DigitPairs` | Exact ordered digit-pair and center enumeration |
| `Agent101MultiplicityBounds` | Product counts, outer/interior bounds, exact nine-profile count |
| `Agent101SplitEnumeration` | Complete finite canonical digit-list enumeration and duplicate-freeness |
| `Agent101NumericFibers` | Transport to ordinary natural values, fixed-width membership iff, exact counts |
| `Agent101PalindromeFibers` | Imported dependency; initial-palindrome semantics, not an added premise of the maximum |
| `Agent101NonpalindromicFibers` | Supplies the general Boolean filter-partition length theorem |
| `Agent105WidthSupport9df76b` | Actual output widths and cross-width carry constraints |
| `Agent105CrossWidth9df76b` | Exterior sums eleven/one, short-width exclusion, common-target units digit one |
| `PeriodObstructions` | Unchanged dependency of the Agent2 branch; separate coefficient-word semantics |
| `Agent2OverflowActual` | Unchanged Agent2 dependency |
| `Agent2OverflowLocal` | Unchanged Agent2 dependency |
| `Agent2OverflowBound` | Original general `nodup_subset_length_le` helper directly reused |
| `Agent101ProfileExtraction` | New finite profile reconstruction |
| `Agent101WidthFiberBounds` | New arbitrary fixed-width integer-list bounds |
| `Agent101MaximumWitnesses` | New complete attaining fibers |
| `Agent101AllWidthMaximum` | New all-width upper bound and final maximum endpoints |

The filename aliases and nested Agent2 paths are intentional registry mappings. In particular, the logical imports `Lychrel196Research`, `PeriodObstructions`, and `Agent2OverflowBound` must resolve through their registered paths, not guessed same-named files in the root of `proofs`.

A comment-stripped scan of all 17 fetched sources found no executable occurrences of `sorry`, `admit`, `sorryAx`, `native_decide`, `ofReduceBool`, custom `axiom`, `unsafe`, `implemented_by`, `extern`, or `trustCompiler`. This is supplementary source inspection; it is not a replacement for the retained compiled-environment axiom audit.

## Existing verification evidence and independence limits

The retained final review reports that reviewer `/root/research_inventory` authored none of the four new maximum modules. It also discloses authorship of the older `Agent101SplitEnumeration` and `Agent101PalindromeFibers` dependencies and states that other workers reviewed those dependencies. That disclosure is appropriately limited; it does not pretend independence for the reviewer’s own older source.

The retained `final-verification.json` reports:

- one fresh canonical build of all 17 registered modules and the generated audit;
- canonical commands using `-j1 -DElab.async=false`, without an explicit `--trust=0` flag;
- three subsequent explicit `--trust=0` audit commands reusing that fresh closure;
- 1,305 origin-selected theorems;
- all 41 new public declarations;
- 225 safe definitions and zero safe opaque declarations;
- theorem/public axiom union `{propext, Classical.choice, Quot.sound}`;
- safe-definition axiom union `{propext}`;
- separately classified unsafe implementation declarations.

The final review preserves the original repository-wide dirty-tree observation and explains the two unrelated README edits. It also preserves the failed initial object-read attempt, which occurred before Lean execution, followed by a successful readback after missing objects were fetched.

I read these retained records and found their evidence categories consistent with the mathematical scope. **I did not independently execute their commands or validate every raw log in this semantic task.** The separate evidence reviewer should establish those execution claims. The import audits must not be described as a second fresh source rebuild.

## Finding and concrete documentation repair

**No mathematical repair is indicated.** The accepted theorem statements and source can remain unchanged.

The current README and PR body should be updated to acknowledge the final evidence already present at H while preserving the historical pending-stage records. A suitable status paragraph is:

> Final independent verification is retained under `reviews/final-semantic-review.md` and `reviews/final-verification.json`. The unchanged canonical verifier freshly compiled the exact 17-module closure and its generated audit; those canonical commands did not explicitly pass `--trust=0`. Three subsequent explicit `--trust=0` audits reused that fresh closure and covered the origin-selected theorems, all 41 new public declarations, and all safe definitions and opaque declarations. The final records report PASS. Earlier source-only reviews and failed development evidence remain preserved as historical records.

Publishing that correction remains subject to the parent’s existing delivery ownership and coordination rules. It does not require a new mathematical gate, a repeated closure build, or a source change.

**Final disposition: semantic PASS at H, with a documentation-status correction identified and execution-evidence validation explicitly delegated to the separate evidence review.**