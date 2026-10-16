# Final independent review: all-width inverse maximum

## Verdict and exact scope

**PASS.** Independent source review, exact published-byte checks, the single
fresh canonical build, and all explicit trust-zero audits passed. This
review found no mathematical defect in the four new maximum modules.

The endpoints establish the sharp maximum number of positive ordinary
reverse-add predecessors of a target of decimal width `D`: for `D >= 2`
the bound is `9 * 10^(D/2 - 1)`, and for `D = 1` it is one. Division and
subtraction in the Lean statements are natural-number operations. The
upper bound covers every duplicate-free finite list of positive
predecessors of every target at that width. The attainment side supplies
a list whose membership is equivalent, for **every** natural `n`, to
`0 < n ∧ step n = Y`; hence it describes a complete fiber across all
input widths.

The two final endpoints are
`Agent101.Maximum.all_width_inverse_maximum` and
`Agent101.Maximum.one_digit_inverse_maximum`. They are finite one-step
inverse results. Their statements do not supply an arbitrary-target
decoder, classify every maximizing target, or make an infinite-orbit
claim.

The reviewer `/root/research_inventory` authored none of these four new
modules. The reviewer authored the older `Agent101SplitEnumeration` and
`Agent101PalindromeFibers` dependencies; other workers independently
reviewed those dependencies. That earlier authorship is disclosed and is
not represented here as independent authorship review of those two files.
No mathematical source or Git reference/index was changed by this reviewer.

## Published identity and actual checkout state

- Mathematical source commit: `0fcbe9973659f178e9c834c68d45f660241d6fbd`.
- Final source-and-registry commit: `0a746261de31531b3ed1dc3d754cd3093753ff56`.
- Final tree: `a51cfaf14f39cf58d0294a0f71964f8a86724d45`.
- Registry SHA256: `496908a7d53c6a09b7a82dfae3c5e10339ef699072e5c97c0e591dc4e2c2cfcc`.
- Original verifier SHA256: `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`.

Independent `git show` reads matched all **17** registered mathematical
sources byte-for-byte at both commits, including each SHA256 and Git blob
pin. The eight metadata/provenance/checker files matched the final commit.
The prescribed `make_registry.py --check --check-published-commit` command
also exited zero. Its result is recorded as an identity check, separately
from the Lean proof results. All four earlier semantic-review snapshots
were independently checked against the final source pins.

The original canonical report accurately says `source_tree_clean: false`.
Its field checks the repository-wide tracked tree. Two pre-existing PR114
README edits remained in place throughout this review:

- `proofs/contributions/agent-101/nonpalindromic-fibers-20261016/README.md`
- `proofs/contributions/agent-101/protected-numeric-multiplicity-20261016/README.md`

The selected 17 sources and eight metadata paths had empty Git status and
matched the published bytes before and after verification. No repository-wide
clean-tree claim is made, and the original report was preserved unchanged.

The first readback attempt stopped before Lean because this partial clone
lacked a promised Agent105 blob. Both commit trees contained the correct
path and blob identifier. Root fetched the missing objects without changing
refs, index, or worktree. The same unmodified independent readback script
then passed with `GIT_NO_LAZY_FETCH=1`. The failed receipt and script remain
in `final-source-readback-attempt-001.*`; this was object availability,
not a missing source at the published commit or a failed Lean proof.

## The four reviewed mathematical steps

| Module | Accepted source SHA256 | New public declarations |
| --- | --- | ---: |
| `Agent101ProfileExtraction` | `fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b` | 7 theorems |
| `Agent101WidthFiberBounds` | `bebc285185d2f15138980dc2720b31fb0cbf476d9a30b1155545aca0c96a1bb2` | 6 theorems |
| `Agent101MaximumWitnesses` | `d915b9df4e9ef3ab92ae9a33c3edd655b8567c40af7b88026e067408303182b7` | 15 theorems, 5 definitions |
| `Agent101AllWidthMaximum` | `9bbdc9351ccb72d2502ca303a7963c1b2aa1e50afd0e9f5d3d095305b34983d9` | 8 theorems |

### Finite profile reconstruction

`exists_coefficientWord_of_reverse` decomposes every actual finite list
`q` satisfying `q.reverse = q` as `h ++ c.toList ++ h.reverse`. Strong
induction removes the real first and last entries. Wrap injectivity proves
their equality and the interior's reverse symmetry; the interior length
decreases by two. Empty and singleton lists are separate bases. No digit
bound, positivity, or realizability premise is added to arbitrary `q`.

`digitPairSums_profile` preserves equality of the entire finite pair-sum
list and its exact width. For a word of length at least two,
`digitPairSums_profile_cons` exposes the real outer coefficient and an
interior half length of `L/2 - 1`.

The finite/infinite-tail distinction is respected. `digitFn` zero-extends
a list, whereas the original `columnSum` reflects indices using natural
subtraction. The bridges compare them only at `i < L`; outside the width
they need not agree. Profile extraction uses index zero under `L >= 2`.
The refined bound transports only indices zero and `L-1`, both valid.
No unrestricted equality of infinite digit functions is assumed.

### Integer multiplicities from actual profile fibers

`mem_numericFiber_of_same_width_step` converts an arbitrary positive
same-width predecessor into its canonical finite digit list. The existing
same-width step equivalence gives equality of complete pair-sum lists,
and the original complete numeric-fiber membership theorem supplies actual
membership. Thus the fixed-width bounds cover arbitrary integer lists
without assuming a decoder or a preassigned profile for every input.

The canonical representative used by the cover need not itself belong to
the counted list. Empty lists are valid. The corrected bound calls the
original public `P196.Agent2.OverflowFibers.nodup_subset_length_le`
directly; it contains no private replacement proof. Agent2's coefficient
fiber bound is not being used as an integer multiplicity formula.

The refined factor is `pairCount true s`, retaining the high-digit
positivity correction. Centers contribute at most one and each interior
pair at most ten. This yields `pairCount true s * 10^(L/2 - 1)` for
`L >= 2`, then the uniform outer bound nine. The one-digit lemma uses the
empty-half center profile and its bound one separately.

### A complete all-width attaining fiber

The witness half contains `D/2` nines; even width has no center, odd width
has center zero. For `D >= 2`, both exterior digits of the target word are
nine, so it is canonical with actual numerical width `D` and units digit
nine. Its exact original fiber has nine exterior splits, ten choices per
interior pair, and one center choice. Its length is positive and equals
the asserted bound.

The reverse implication of `mem_maximumPreimages` begins with an arbitrary
positive `n` having the target step value. It obtains the actual canonical
width `L` of `n`, and separately obtains a real width-`D` witness member
from positive list length. If their widths differ, the unchanged Agent105
cross-width target-digit theorem forces the common target's units digit
to be one. This contradicts nine. Both width orderings are handled.
Consequently the arbitrary predecessor belongs to the original width-`D`
fiber. The resulting public equivalence leaves no width assumption on `n`.

### Uniform bound over the complete width partition

The actual-step width theorem places any positive predecessor of a
`D`-digit target at width `D` or `D-1`. The root partitions an arbitrary
`Nodup` input list by `decimalWidth n D` and its Boolean complement.
Both parts retain no-duplicates, every complementary member has width
`D-1`, and their lengths sum to the original length.

When one part is empty, the appropriate single-width bound applies; the
short-width-one boundary is handled separately. Only when both parts are
nonempty are actual representatives selected. Agent105 then forces outer
sums eleven and one, and forces the short width to be at least two.
The two integer counts are bounded by
`8 * 10^((D-1)/2 - 1)` and `10^(D/2 - 1)`. Natural division and truncated
subtraction are monotone, so the short power is at most the long power.
Their sum is at most nine times the long power, with no hidden parity
assumption or selection from an empty list.

## Boundary conclusions

| Boundary | Checked consequence |
| --- | --- |
| `D = 2` | Witness target `99` has nine positive predecessors. The permitted trailing-zero input `90` is included. If only width-one inputs occur for another target, the separate bound one applies; the two-nonempty branch cannot pretend that width one is at least two. |
| Odd `D >= 3` | Center zero is an interior digit with one realization. Outer nines preserve positivity and full width. |
| `D = 1` | The universal bound is one. The complete attaining fiber is `Y = 2`, `ns = [1]`; its equivalence quantifies over all positive inputs. |
| `D = 0` | No positive-width maximum or attainment theorem is asserted. |
| Empty counted list | The universal upper bound includes it and selects no fictitious representative. |

These boundary readings follow from the reviewed source definitions and
proofs. No separate unrecorded numerical test is claimed.

## Actual independent verification

The original verifier was invoked once in the previously unused directory
`/workspace/scratch/2a8a87fd78df/agent101-all-width-canonical-review-01`.
It built all 17 modules and its generated ProjectAudit: 18 commands,
all exit zero, total wall time 110.94 seconds. Its module commands and
initial ProjectAudit command used `-j1 -DElab.async=false` and **did not
explicitly pass `--trust=0`**. This original behavior is recorded honestly.

The same fresh closure was then reused for three further commands, each
explicitly passing `--trust=0`:

| Audit | Result | Elapsed seconds |
| --- | --- | ---: |
| Unchanged generated ProjectAudit | 1,305 origin-selected theorems, including dependency and generated helper theorems; PASS | 27.56 |
| Complete new public inventory | 41 declarations: 36 theorems and 5 definitions; names, origin modules, declaration kinds, and safety flags all match; PASS | 4.33 |
| Additional compiled-environment audit | All 225 safe definitions and zero safe opaque declarations from the 17 modules; PASS | 2.39 |

The theorem and public axiom unions are exactly
`{propext, Classical.choice, Quot.sound}`. The additional safe-definition
union is `{propext}`. All custom safe axioms were rejected by the audit
logic. The 931 declarations marked unsafe by `ConstantInfo.isUnsafe` are
separately inventoried implementation declarations, not counted as safe
logical declarations; none is one of the 41 public exports. The compiled
audit adapts the existing independent auditor while preserving its
module-origin and safety separation.

All registered source bytes, metadata, the original verifier, compiler
pins, and original canonical output-manifest members remained unchanged
after the audits. The original `FILES.json` has 37 entries and already
excludes `.olean` files and itself. No second whole-closure build or
additional Lean run is needed.

## Evidence

`final-verification.json` is the structured final receipt.
`final-source-readback.json`, `final-metadata-check.log`, and
`final-pre-review-snapshot-check.json` establish identity.
`final-canonical-command.*`, `final-canonical-verification.json`,
`final-canonical-FILES.json`, and `final-build-logs/` preserve the original
canonical result. The three `final-*-trust0.log` files and corresponding
Lean audit sources preserve every additional audit. The earlier
`pre-review-semantics.md` and `root-bounds-pre-review.md` retain their
historical pending-runtime labels; this final review closes those pending
stages without rewriting the earlier records. The evidence index is
`final-retained-evidence.json`.
