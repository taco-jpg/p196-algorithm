# Renewal research: exact gates, inverse obstructions and collision algebra

**Decimal Lychrel existence and the assertion for 196 remain unproved.**
This checkpoint contains supporting theorems, exact certificates,
counterexamples, completed Lean audits, and the unsuccessful attempts that
led to them. It is a reproducible research record, with no novelty or
external peer-review claim.

The target remains a single finite positive integer n such that every
positive reverse-and-add iterate is nonpalindromic. Varying n with a finite
horizon does not establish this target. No accepted invariant or
indefinitely repeatable safe return has been instantiated in this pass.

## Results and their exact verification level

| Result | Scope | Evidence |
|---|---|---|
| Earlier six-core delayed overlap gate | Every spacer r>=1, outside parameter 1<=p<=4; positive outputs 1 and 2 safe | 49 Lean declarations; fresh build and independent root audit in `lean/` |
| Enlarged twenty-core gate | Exactly 80 genuine two-step repairs in the stated complete four-column class, for all r>=1 | Written carry proof, uniform affine certificates, all small boundaries, full 5,204-record comparison archive |
| Two consecutive repairs | Four infinite spacer families repair at times 2 and 4; their proposed time-6 repair fails by outer coefficients 14 versus 15 | Written formulas and exact all-parameter certificates in `constructive/` |
| Exact terminating tails | Five of the original six core families have stated uniform first-hit times 3, 4 or 11 | 26 independently checked symbolic transitions and finite boundary cases in `tails/` |
| Language repair obstruction | Every finite symmetric-difference edit of F10 still fails forward closure | Explicit infinite inverse family and written proof in `language/` |
| Adaptive-mode projection | Universal safe transition coverage over the same saturated word classes projects to a safe closed union of those classes | Written theorem with full quantifiers; no positive instance |
| Forbidden pair prefixes | No one-step output starts (1,6,2); no orbit at time t>=2 starts (2,12,4), at any finite width | 16 Lean declarations, ordinary-decimal bridge and independent root audit in `lean/prefix/` |
| Arbitrary-block seam response | Exact actual normalized digits D=E+(x-10)K, including all-nine blocks and the actual terminal width | Written all-word proof plus 2,737 complete controls in `constructive/collision_response/` |
| Active-seam safety and raw-symmetry obstruction | For every canonical whole pair word and every partition, K nonzero implies the next ordinary output is nonpalindromic; symmetric raw E instead forces K=0 and a palindrome | 42 Lean declarations, actual ordinary-decimal and arbitrary-partition bridges, fresh and independent root audits in `lean/raw_symmetry/`; 2,495 independently replayed active canonical controls |
| Local incoming carry law | Extra carry persists exactly through the initial run of coefficient 9; arbitrary-offset actual-block bridge included | 28 Lean declarations, fresh and independent root audits in `lean/incoming_carry/` |
| Combined collision safety | For canonical B,H, failed independent closure of BHB certifies a nonpalindromic next output; unequal isolated overflow bits can certify this even when K=0 | Written all-length corollary of the other stream's collision theorem, with exact examples in `external_review/COLLISION_SAFETY_COROLLARY.md` |
| Seven-step clock obstruction | A canonical whole word starting (4,4,0) has at most three consecutive returns of that prefix at seven-step intervals; three safe returns occur | Written actual-orbit inclusion at every width >=6, independently reconstructed complete 48,013-vertex necessary graph and rank certificate in `external_review/seven_step_graph/`; rank computation is not a Lean proof |

The four listed Lean modules contain 135 supporting declarations. The
full generalized-gate classification, concatenated seam-polynomial
identity, combined collision-closure corollary, counting limits, and an
accepted infinite invariant are not being
represented as Lean theorems by that count. The last item remains absent.

## Concrete forward construction and its limit

For low-to-high symmetric pair words put

\[
A=p\,0^r(u,v,v,u)0^r p,\qquad Q=(1+x)A.
\]

The twenty central pairs are specified in `constructive/STATUS.md`.
For p=1,...,4 their overlap relation genuinely fails after one update and
is restored after two. Four p=1 branches admit a second genuine restoration
at time four. The original (u,v)=(1,6) branch is among them, showing why the
earlier original-domain non-reuse theorem was not a complete obstruction.

All four returned exteriors become 16. Their next proposed two-step
restoration fails uniformly: the independent component's outer coefficient
becomes 14 while the whole word's becomes 15. This excludes that particular
reuse, not every later return. The original (1,6) branch in fact reaches a
palindrome at step 11 whenever r>=5, as separately certified.

## Inverse construction and its limit

An explicit all-parameter chain has first positive palindrome times
15,14,13,12,11, with the respective parameter minima in the report. Its
middle edge gives infinitely many fresh closure failures of F10, beyond
every finite set of edits.

The selected chain cannot be extended indefinitely: every word in its
(2,12,4) prefix cylinder has no two-step ancestor. An actual ancestor
outside that cylinder is retained, so this obstruction is not promoted to
a bound on every inverse branch of the original gate. Complete finite
trees through depth six and all rejected branches remain in the archive.

## Collaboration and the collision handoff

The concurrent contribution at commit
`b7fa911dc4ca943528f5d28b67f3fbd87c9404ca` improved the finite-prefix seed to

\[
C_R=2\bigl(10^{\lfloor7R/4\rfloor+1}-1\bigr),
\]

safe at every index 0 through R. It also proved a deterministic marker
theorem and wrote a counting bound giving density-one finite-horizon
avoidance for horizons c log10 L with 0<c<2/7 and input width L.
Root freshly rebuilt its six modules and audited all 24 new supporting
declarations. The counting and asymptotic parts remain written proofs.

Its exact separated-block theorem takes the remaining (1,7) gate to a
zero spacer by time tau(r)<=4r-3. Our prior arbitrary-motif collision law
and new seam formula now describe the actual next coupled update. The
correction mask K records each actual incoming carry along the affected
initial-nine run. Its mass effect is exact: the paired coefficient mass
loses 18 times the total active run length relative to the placed isolated
components. Mixed overflow clocks must still be aligned to the actual
whole-word width.

A nonzero K is itself a valid one-step safety certificate. A palindromic
output would require either all input coefficients at most 9, which never
generate an incoming carry, or only coefficients 0 and 11, which contain
no initial-nine run. Both possibilities force K=0. For example, the
canonical seed 99900 has pair word (9,9,18,9,9); partitioning it as
(9,9)|(18)|(9,9) gives K=x^3+x^4 and the nonpalindromic output 100899.
This supplies a realizable criterion. No theorem regenerates it at every
future update of one finite seed.

The other stream's later commit
`a3914ba08e5facb59699d066fcb69f1bd37b6e6a` proves a complete collision
closure classification for canonical BHB. The independently updated
blocks give the actual next pair word exactly if and only if K=0 and
the two isolated overflow bits agree. Combining that theorem with the
exact palindrome-predecessor classes gives a further sufficient safety
criterion: failure of this closure forces a nonpalindromic next output.
For B=(2,2), H=(18), the seed 22900 goes to 23822 with K=0 but unequal
isolated overflow bits. This new combined corollary is a written proof,
not one of the 135 Lean declarations.

The same external commit supplies an explicit infinite family of seeds
n_r which, for every r>=5078, avoids palindromes at times 0 through 10000.
Its proof uses an independently audited 10,000-record finite driver trace
and the exact endpoint loss S_9999=5077. Allowing zero gap at the final
state improves the earlier handoff's sufficient threshold 5079. Root
reviewed the written reduction and indexing, but has not independently
downloaded and replayed that complete trace. The external audit and its
lossless trace parts are preserved with their verification scope. This is
a finite-horizon theorem and does not settle time 10001 or infinite
survival for one fixed seed.

The public division of work assigns actual (1,7) post-collision reset
analysis to the other contribution stream, with our reusable seam theorem
and local formal bridge supplied for it. Our stream develops generalized
gates and semantic language obstructions. Their independent replay of our
tail certificate, our independent rebuild of their formal results, and
the explicit repository handoffs are recorded in `ROOT_REVIEW.md`.

The proposed extra shortcut, a symmetric raw isolated-digit sum E with
nonzero correction K, has been proved impossible for every canonical whole
pair word under every partition. In fact, E symmetry is equivalent to
actual output palindromicity and forces K=0. The complete all-width proof
and independent 58,221-partition audit are in `seam_audit/`. The original
proposal remains in its pinned report snapshot. The main seam identity is
independent of this shortcut. The forward raw-symmetry rigidity and
ordinary-palindrome implication, together with the positive nonzero-defect
safety theorem, are now also compiled in `lean/raw_symmetry/`. The written
equivalence is not miscounted as a separately named Lean iff theorem.

## Immediate follow-up to the other stream's seven-step result

While the release was being assembled, commit
`6889b717599343b6773d376e728ca5b03cf68527` published the exact conditional
return of prefix (4,4,0), the padded middle-word operator, and its separate
safety tests. Its next commit `8a42fe14262fee12ce1c8b40bf25e97b94044742`
announced an all-width obstruction to four consecutive returns. We read
both and independently reconstructed the necessary six-column phase
graph from the boundary arithmetic, rather than waiting for its announced
certificate bundle or assuming its numerical conclusions.

There are exactly 48,013 vertices, 96,026 labeled controls and 61,731
accepted edges. A separate verifier based on literal integer evaluation
recomputes every accepted and rejected control and checks every rank.
The maximum rank at phase zero is 26. The complete 128-control
three-column calculation forces the seven intermediate phases between
any two returns. Four consecutive returns would therefore require 28
edges from phase zero, which the rank excludes. The written inclusion
argument covers widths 6 through 11 where the six-column windows overlap,
as well as larger widths. Allowing both deeper carry bits makes the graph
a necessary overapproximation; no converse realization is assumed.

The other stream's example is independently realized by the ordinary
seed 4401198500000. Its prefixes return at times 7,14,21 and follow the
full phase clock for 26 transitions before deviating at state 27. All
28 checked positive outputs are nonpalindromic. Thus three consecutive
safe returns are attained, but leaving this clock does not imply a
palindrome. The full certificate, all labeled outcomes, every rank and
the literal integer trajectory are retained. This independently confirms
the other stream's announced obstruction; it is not a novelty claim or
a Lean-kernel rank proof. Different clocks and variable return times
remain outside its scope.

## Complete retention and remaining obligation

The failed initial affine base, superseded structural-inequality routine,
small-spacer exceptions, the false exploratory time-five subclaim, escaping
inverse branch, finite UNKNOWN trajectories, and all compiler attempts
are retained. Large outcome streams use lossless gzip with checksums and
recovery commands. Infrastructure and duplicate build products are
inventoried separately by the publication manifest.

All 22 remaining tested gate seeds avoided both palindromes and exact joins
to the tested 196 orbit through 1,500 additions. This is finite evidence
only. No absence of an all-time join, and no all-time avoidance, follows.

The unsatisfied proof obligation is still one finite realizable seed in a
nonempty universally safe forward-closed family, or an exact repeatable
safe return construction with every boundary and overflow case discharged.
The current results supply neither. Reproduction commands and verification
levels are given in each branch report; `ROOT_REVIEW.json` records the
final reviewed hashes and completed checks.
