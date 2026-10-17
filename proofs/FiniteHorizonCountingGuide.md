# Finite-horizon counting: exact population and positive-time hit bound

This guide explains the finite counting result integrated through [PR #123](https://github.com/taco-jpg/p196-algorithm/pull/123). It connects the exact Lean statements to their retained verification evidence and keeps the marker count separate from the palindrome-hit bound.

**Source snapshot:** [`ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3`](https://github.com/taco-jpg/p196-algorithm/commit/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3). The original contribution and historical evidence retain their own dates and authorship. This guide is a documentation update, not a new Lean execution.

## Population and selected markers

Fix natural numbers $L\ge1$ and $r\ge1$. The population is every ordinary positive integer in the canonical decimal interval

$$
10^{L-1}\le n<10^L.
$$

The leading digit is nonzero; a zero units digit is allowed. Digit position zero is the least significant position, and the intrinsic digit is $d_i(n)=\lfloor n/10^i\rfloor\bmod10$.

Define

$$
J=\left\lfloor\frac{\max(\lfloor L/2\rfloor-1,0)}{r}\right\rfloor,
\qquad a_j=1+jr\quad(0\le j<J).
$$

A selected marker at $a_j$ means that **all** the digits at $a_j+i$ and $L-1-(a_j+i)$, for $0\le i<r$, are nine. These are $J$ prescribed mirrored blocks, not a search over all possible block positions. The selected blocks avoid both outer digits and any odd-width center.

In [`Agent9NumericMarkerCount.lean`][numeric], `markerCount`, `numericDigit`, and `NumericMarker` give these exact definitions. Lean's natural subtraction truncates at zero. `selected_position_geometry` checks the selected positions, and `selected_digits_le` proves $2rJ\le L-1$, so the exponent below is nonnegative.

## The exact marker-complement count

Let $U_{L,r}$ be the integers in that interval with none of the selected markers. The complete count is

$$
|U_{L,r}|=C(L,r):=9\,10^{L-1-2rJ}(10^{2r}-1)^J.
$$

Three declarations work together: `mem_unmarkedSeeds` characterizes membership in the complete ordinary-integer population, `unmarkedSeeds_nodup` excludes repeated integers, and `length_unmarkedSeeds` proves the formula. The guide retains $r>0$ for the marker interpretation; the literal length lemma itself needs only $L>0$.

The factor $10^{2r}-1$ removes exactly one filling of a whole selected block: all its $2r$ digits being nine. An allowed block may still contain an individual pair $(9,9)$. Replacing this factor by $99^r$ would impose a different condition. The construction in [`Agent9MarkerWords.lean`][words] and [`Agent9MarkerEnumeration.lean`][enumeration] accounts for all canonical digit lists and converts them injectively to the integers counted here.

## The finite positive-time consequence

For every natural $R$, the unchanged deterministic marker theorem uses

$$
r(R)=\min\left(1+2R,\ 1+\left\lfloor\frac{7R+4}{4}\right\rfloor\right).
$$

[`FiniteHorizonBlocks.blockLength`][marker-safety] defines this value, and `blockLength_positive` proves it is positive. A selected marker of this length prevents a palindrome at each time $1,\ldots,R+1$ under ordinary decimal reverse-and-add.

Let $H_{L,R}$ contain exactly the width-$L$ seeds whose orbit has a palindrome at some time $1\le t\le R+1$. Then

$$
H_{L,R}\subseteq U_{L,r(R)},
\qquad |H_{L,R}|\le C(L,r(R)).
$$

In [`Agent9FiniteHorizonCount.lean`][horizon], `positiveHitB` checks `orbit n (k + 1)` for `k` in `List.range (R + 1)`. `mem_positiveHits` exposes the exact positive-time interval. `positiveHits_subset_unmarkedSeeds` applies the original `mirroredNines_safe_prefix` theorem, and `positiveHits_count_le` supplies the bound.

**The equality counts the marker complement. The inequality bounds palindrome hits.** Absence of a selected marker does not certify a palindrome hit, so the result does not identify those two sets or give an exact hit probability. No probability model is required.

## Boundaries that affect interpretation

| Case | Meaning of the proved contract |
| --- | --- |
| $L=1$ | The complement consists of the nine canonical one-digit integers. |
| $J=0$ | No marker is selected; the complement is the entire canonical interval, and the hit bound may be the full population bound. |
| Odd width | The center digit is unrestricted and lies outside the selected blocks. |
| Zero units digit | Allowed; only the leading digit must be nonzero. |
| Initially palindromic seed | Eligible. It is counted as a positive-time hit only if a tested positive iterate is palindromic. |
| $R=0$ | The tested interval is the single positive time $1$. |
| $L=0$ or the guide's $r=0$ interpretation | Outside the stated counting contract; the horizon specialization always has $r(R)>0$. |

The theorem is quantified over every permitted natural parameter, while each population and horizon is finite. It does not establish the separate analytic limits, logarithmically growing-horizon claims, time-zero intersection refinements, a single seed safe for all time, decimal Lychrel existence, or a conclusion specific to 196.

## Source, verification, review, and integration

| Evidence layer | Exact retained evidence and scope |
| --- | --- |
| Source publication | PR #123 head [`0d1eea6c69078111366d9d7235bd47c3e16aadf8`](https://github.com/taco-jpg/p196-algorithm/commit/0d1eea6c69078111366d9d7235bd47c3e16aadf8). Five new mathematical modules use eleven unchanged dependencies. The [author freeze][freeze] and [dependency ledger][dependencies] pin the inputs. |
| Retained Lean check | The [independent result][review-result] records one fresh 16-module project-closure build plus its audit, with zero pre-existing objects, official Lean 4.19.0 (`6caaee842e94`), and explicit `--trust=0`. The standard runtime was hashed, not rebuilt from source. |
| Retained independent semantic review | [Agent #9/horizon-safety's review][semantic] identifies Agent #9/coverage_census as the mathematical author and accepts the exact count and positive-time upper bound. They are distinct agents in the same Agent #9 session; this is not an external peer-review claim. |
| Actual integration | [PR #123](https://github.com/taco-jpg/p196-algorithm/pull/123) records a merge into `main` at [`dcde48c2d17729a73ecec64d7df1e2a99e86bdc6`](https://github.com/taco-jpg/p196-algorithm/commit/dcde48c2d17729a73ecec64d7df1e2a99e86bdc6), on 2026-10-16 at 23:39:55 UTC. The guide's pinned snapshot includes that integration. |
| This documentation increment | Source and retained-record inspection only. Its [documentation evidence][doc-evidence] records the actual checks separately from the historical Lean execution. |

The independent run occurred on 2026-10-16, from 22:21:42 to 22:23:42 UTC. Its receipt reports 1,505 theorem constants, 239 safe definitions, and 100 literal exports (78 theorems and 22 definitions). These are different audit units, not counts of independent discoveries. Fifteen module origins contain declarations; the sixteenth is the unchanged import-only `Lychrel196Research` adapter. The recorded mathematical axiom union is `propext`, `Classical.choice`, and `Quot.sound`; compiler implementation constants are reported separately. None of these scoped records is a repository-wide build claim.

## Detailed argument and retained reproduction records

Read the [original written counting argument][original-argument], the [contribution explanation][contribution], and the [publication and archive-recovery instructions][publication] together. Some build snapshots and raw logs are stored only in the contribution's lossless archive; the publication record identifies their recovery and original paths. Package-specific reproduction must retain its dependency pins and distinguish a new run from the saved historical receipts.

[numeric]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/Agent9NumericMarkerCount.lean
[words]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/Agent9MarkerWords.lean
[enumeration]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/Agent9MarkerEnumeration.lean
[horizon]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/Agent9FiniteHorizonCount.lean
[marker-safety]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/FiniteHorizonBlocks__de01e0bf306b4eaa.lean
[freeze]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/AUTHOR_FREEZE.json
[dependencies]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/dependencies.json
[review-result]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/review/horizon-safety/RESULT.json
[semantic]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/review/horizon-safety/SEMANTIC_REVIEW.md
[contribution]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/README.md
[publication]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/PUBLICATION.md
[original-argument]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/source/README.original.md
[doc-evidence]: contributions/agent-64/finite-horizon-count-guide-20261016/README.md
