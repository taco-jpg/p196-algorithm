# PR #123 independent semantic, source, and evidence review

## Verdict and exact scope

**PASS at exact head `0d1eea6c69078111366d9d7235bd47c3e16aadf8`.** No mathematical source correction is requested. This review accepts the complete canonical-integer marker-complement count and its direct finite positive-time palindrome-hit upper bound. It does not accept any infinite-avoidance, probability-limit, initial-palindrome-intersection, or 196 conclusion.

Reviewer: Agent #12, independently delegated reviewer `/root/review123`. Mathematical author: Agent #9. The earlier author gate and Agent #9/horizon-safety review are retained evidence, not substitutes for this review's new compiler run. This reviewer made no remote mutation, source-branch edit, main edit, comment, review submission, merge, or coordination write. The parent integration agent handles current-main combination checks and any public actions.

The reviewed contribution is `proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/`. Its complete diff from merge base `f44c06c4851b26523bcec920d93a52b93fd2a0a6` consists only of added contribution-package files and is preserved as `complete-pr123.diff`. The isolated checkout was clean before and after the kernel gate. Repository `AGENTS.md` and `proofs/PUBLICATION_POLICY.md` were read. This assessment follows their requirements to preserve failures, distinguish evidence classes, and avoid all-time overclaims.

## What is proved

For natural numbers `L > 0` and `r > 0`, define `J = (L / 2 - 1) / r`, using natural-number division and truncated subtraction. Block `j < J` selects the positions `1 + j*r + i` for `i < r`, together with their reflected positions `L - 1 - (1 + j*r + i)`. Positions are indexed from the least significant digit. The numeric marker is literally a universal statement that the corresponding quotient/remainder digits `n / 10^i % 10` equal nine.

The public membership theorem `mem_unmarkedSeeds` is a two-way equivalence between membership of `unmarkedSeeds L r` and the conjunction of the complete interval condition `10^(L-1) <= n < 10^L` with absence of every selected marker. `Agent101.decimalWidth` also explicitly contains `0 < L`. Thus the theorem ranges over every positive ordinary integer of width L. It has neither a fixed digit-pair-sum profile nor an existential construction restriction left over from the intermediate enumeration.

`unmarkedSeeds_nodup` proves that these integers occur exactly once. `length_unmarkedSeeds` proves the exact count

```
9 * 10^(L - 1 - 2*r*J) * (10^(2*r) - 1)^J.
```

The length identity has a slightly broader statement requiring only `L > 0`; the semantic membership theorem supplies `r > 0`, exactly as required by the target contract. No zero-width interpretation is asserted.

For every natural `R`, the unchanged deterministic module defines

```
blockLength R = min (1 + 2*R) (1 + (7*R + 4)/4).
```

The complete canonical interval is enumerated by `widthSeeds`; it is filtered by `positiveHitB`, whose Boolean test ranges over `k = 0,...,R` and evaluates `Palindrome (orbit n (k+1))`. The membership theorem `mem_positiveHits` explicitly restates this as existence of a time `1 <= t <= R+1`. The underlying `Lychrel196` definitions are ordinary decimal reversal, `step n = n + reverse10 n`, and iteration with `orbit n 0 = n`. Decimal reversal consumes ordinary decimal digits and removes leading zeroes in the reversed representation.

`positiveHits_subset_unmarkedSeeds` uses the unmodified `FiniteHorizonBlocks.mirroredNines_safe_prefix` at `k = t-1`. Its time substitution is justified by the positive-time hypothesis, and the required `k <= R` follows from `t <= R+1`. Numeric markers are transported through a proved digit bridge to exactly that theorem's `MirroredNines` predicate. Hence `positiveHits_count_le` is an upper bound for the complete positive-hit event, with the same formula specialized to `r = blockLength R`. It is not an exact count of palindrome hits.

## Enumeration and arithmetic audit

All five new mathematical modules were read in full, along with both published audit modules, the portable replay driver, author driver, finite-control source, contract, provenance registry, and relevant unchanged numeral/dynamics interfaces. The proof structure is sound for the stated scope:

1. `Agent9FiniteProducts` establishes full fixed-length alphabet-product membership, duplicate freedom, and product lengths. Its concatenation injectivity hypothesis fixes the left block length, avoiding variable-length decomposition ambiguities. Its block membership theorem identifies every selected `drop (j*r) | take r` chunk and the final suffix in both directions, including `J = 0`.
2. `Agent9MarkerWords` enumerates all 100 unrestricted inner digit pairs and all 90 outer pairs. The second component of the outer pair is the leading digit and ranges over `1,...,9`; the first is the units digit and ranges over `0,...,9`. A good block removes exactly the single list of r pairs all equal to `(9,9)`. Its factor is therefore `10^(2*r)-1`, not `99^r`. Wrapping is injective at fixed pair count, and the low/high positional theorems identify the actual paired digits.
3. `Agent9MarkerEnumeration` proves both directions of full canonical digit-list membership. It reconstructs every canonical word by repeatedly extracting its two endpoints, so the construction is surjective onto the stated domain. The unmarked-pair block conditions are converted to `WordMarker` using exact list positions. Duplicate freedom is preserved through the wrapping product.
4. `Agent9NumericMarkerCount` proves the quotient/remainder digit bridge by induction on the finite value representation. Canonical finite lists map injectively to ordinary natural numbers by unchanged Agent101 numeral interfaces. Conversely, every ordinary integer in the canonical interval has a canonical representation and a finite list of exactly that width. This completes the all-integer membership equivalence rather than merely counting representable examples.
5. `Agent9FiniteHorizonCount` enumerates the entire interval, proves exact positive-time event semantics, invokes the unchanged deterministic safety theorem, and takes a finite list-cardinality inequality with duplicate freedom.

For `L >= 2`, writing `q = L/2 - 1 - J*r` and `e = L % 2`, the intermediate enumeration has count `90 * (10^(2*r)-1)^J * 100^q * 10^e`. The width decomposition and exponent identity convert it to the displayed source formula. `selected_digits_le` explicitly proves `2*r*J <= L-1`; natural subtraction is not silently treated as subtraction in the integers. The resulting exponent identity is `L-1-2*r*J = 2*q+e+1` in this width range.

### Boundary cases

- **L = 1:** the representation explicitly lists the nine single digits 1 through 9, and J is zero. The count is nine.
- **J = 0, including r larger than available interior pairs:** marker absence is vacuous. The product construction reduces to the free suffix and center, giving the full canonical interval count.
- **Even and odd widths:** `selected_position_geometry` puts every low selected position strictly between zero and `L/2`, and every high reflected position strictly above `(L-1)/2` and below `L-1`. Thus both endpoints and an odd center are excluded, and mirrored selected positions do not overlap.
- **Leading/trailing digits:** only the leading digit is required to be nonzero. Trailing zeroes remain allowed. The actual reversal definition correctly drops leading zeroes of the reversed numeral.
- **R = 0:** `blockLength 0 = 1`, and the hit predicate tests exactly time one. The fresh direct controls cover this case.
- **Initial palindromes:** no initial-nonpalindrome filter occurs anywhere in `widthSeeds`, `positiveHits`, or the public bound. The retained and replayed control explicitly includes 11, whose next iterate is 22. Initial palindromes therefore remain part of the event where appropriate.

No probability distribution or independence assumption is introduced into the formal count. The original manuscript's probability language and analytic consequences remain preserved historical written material; the new accepted endpoint is finite cardinality. The separately active initial-palindrome/marker intersection task corresponding to equations (4)/(5) is not claimed here.

## Fresh Lean verification

The original independent portable driver was replayed without modification. Driver SHA-256 is `c066b91ecf42ccdba0daea5090708bddf3f779f099ee712581317a8986e01cc5`; source-registry SHA-256 is `aa9e35fdc2836f6c7de34f835ecfd14b934f58d19030ade5ab107202491af457`. Its exact command, environment, output paths, elapsed times, exit codes, and every source identity are preserved in `fresh-full-001/verification.json`. The outer driver exited zero after about 120.8 seconds.

The build directory was created new and contained zero preexisting `.olean` files. All 16 selected mathematical modules were compiled from their exact source bytes, followed by a generated full audit. Every Lean invocation included `--trust=0 -j1 -DElab.async=false`. Only the supplied pinned official standard runtime objects were reused. All 45 recorded driver commands exited zero.

| Audit item | Fresh result |
| --- | ---: |
| Mathematical source modules | 16 |
| Declaration-bearing module origins | 15 |
| Import-only compatibility origin | 1 |
| Literal public exports and type reports | 100 |
| Literal public theorems / definitions | 78 / 22 |
| Theorem constants by actual compiled origin | 1,505 |
| Safe definitions by actual compiled origin | 239 |
| New-module theorem constants / safe definitions | 183 / 32 |

`Lychrel196Research` is the exact preserved import-only adapter that imports `LychrelDigitSums`; it contributes no duplicate arithmetic foundation or declarations. All 15 nonempty origins occur in the fresh audit, and the sixteenth adapter was actually compiled. The supplemental `postcheck.py` independently parses all 1,744 complete bracketed axiom lists across line breaks, validates every one of the 100 literal type and axiom reports, checks exact endpoint coverage against the actual new source declarations, and compares all fresh source snapshots with the exact-head files.

The complete transitive mathematical axiom union is exactly `propext`, `Classical.choice`, and `Quot.sound`. No accepted-chain `sorry`, `admit`, `sorryAx`, `native_decide`, `ofReduceBool`, skipped kernel check, or custom safe axiom was accepted. The 39 unsafe compiler implementation axiom declarations and 924 unsafe implementation definitions are separately reported; none is an extra mathematical axiom dependency of an audited theorem or safe definition.

The compiler reports Lean 4.19.0, release commit `6caaee842e94`. Executable SHA-256 is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The supplied install record identifies the official release download. The executable, root Init/Std/Lean objects, and runtime shared libraries were hashed before and after replay and remained unchanged. The old download archive is no longer present, so its historical hash in the install record was not independently rehashed here. The supplied runtime was not rebuilt from source; this limitation is recorded explicitly and does not imply reuse of author project objects.

## Evidence preservation and finite controls

The compressed evidence file was independently checked against its compressed size/hash and decompressed tar size/hash. Every member was required to be a unique regular file with a relative path and no traversal. Links, devices, duplicate names, and overwrites were rejected by the extraction procedure. All **317 original files**, totaling **2,817,227 payload bytes**, match their manifest sizes and SHA-256 values. Every directly published duplicate is byte-identical to its archived counterpart.

The compressed SHA-256 is `f6311264b4335c320e5763a868f61059d27bee26c7d81ddc1d682f255a39c562`. The decompressed tar SHA-256 is `b8acefbdd47c46e9d36fb9f8efaefe05f0777d4509866cf3c823b267544b7518`. Eight subordinate manifests/checksum lists yielded **750 successful entry checks**. Historical omitted `.olean` objects are explicitly classified as reproducible infrastructure; historical redundant source-copy omissions were followed through their explicit retention aliases and checked against exact retained bytes. No substantive missing source or log was waived.

All 23 author development attempts remain intact, including the six genuine compiler failures. Their source hashes and stdout/stderr presence were validated. The earlier independent review's Git-object availability failure and multiline-axiom packaging parser failure remain separately classified. The original generic checkpoint at `cf7935d24ce8180d6181de01d1050fc02b66802c` was checked by exact Git blob identity: all 24 checkpoint files are preserved unchanged. The original manuscript was also checked against its historical commit/path/blob and retained bytes.

This review reran the unmodified finite ordinary-arithmetic controls in a separate fresh output directory. They passed **1,999,008 seed/case visits** across the published parameter rows. In particular, L=6,r=2 has exact unmarked count **899,910**, whereas the incorrect per-pair exclusion expression gives **882,090**. The controls also cover single digits, zero selected blocks, both width parities, trailing zeroes, two selected blocks, and the one-positive-step implication for r=1. These are supplemental finite implementation checks, not substitutes for the universal Lean proof.

This review's first subordinate-manifest checker stopped on a historical source-copy omission before following `RETENTION.json`. Its original checker and failure classification are retained in `review-development/manifest-audit-attempt-001/`. The corrected checker validates the recorded aliases and all original hashes. This was a reviewer evidence-parser issue; no mathematical source, prior evidence, or kernel run was altered.

## Acceptance boundaries and handoff

The exact head is acceptable for the task contract with no mathematical patch. The source closure, all exact-head paths/hashes, full commands and logs, prior evidence, independent postcheck, finite controls, and this review are available in the review packet. `RECEIPT.json` is the machine-readable handoff.

The parent must tie this fixed-head result to its chosen current-main combination by exact source identities and its own integration process. This review does not claim that unrelated repository files were rebuilt or that a merge was performed. It makes no novelty or external peer-review claim, and does not prove any fixed seed, including 196, avoids palindromes forever.
