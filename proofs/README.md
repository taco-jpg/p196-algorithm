# Decimal reverse-and-add research findings

**Decimal Lychrel existence remains unproved. This collection does not prove that 196 is a Lychrel number, does not disprove decimal Lychrel existence, and contains no verified positive Lychrel witness.**

This directory publishes the research findings, written proofs, formal source, finite certificates, failed constructions, and reproducible searches accumulated through 15 October 2026. The existence goal is separate from the completed supporting theorems. No novelty, external peer review, or publication-priority claim is made. The audits described here are internal and AI-assisted.

Start with [the findings and evidence matrix](FINDINGS.md), [the complete written-report index](REPORTS.md), and [reproduction instructions](REPRODUCE.md). The [completed renewal pass](research/main_existence_attempt/renewal_pass/RENEWAL_STATUS.md) now combines the early checked gate and exact later hits with generalized gates, language obstructions, actual carry safety, full raw evidence and independent audits. The [correlation and finite-delay report](research/main_existence_attempt/correlation_pass/CORRELATION_PASS_STATUS.md) and [earlier ancestry and repository review](research/main_existence_attempt/ancestry_direct_pass/ANCESTRY_DIRECT_STATUS.md) remain preserved. The original research tree is preserved under [research/](research/), so relative imports and certificate paths remain meaningful. Its [historical overview](research/README.md) records successive passes; later reports supersede earlier open questions only where explicitly stated. Historical statements such as “not yet formalized” or “nothing published” describe that checkpoint, not the current release.

## Checked four-state whole-word language exclusion — 15 October 2026

The [new language handoff](coordination/2026-10-15-four-state-language-exclusion.md)
excludes nonempty safe forward-closed canonical folded languages recognized by
at most four complete deterministic pair-reading states with eleven arbitrary
center/end predicates. Both overflow choices are allowed; no seed or temporal
clock is fixed. An all-width written reduction, complete semantic CNF audit and
independently replayed LRAT refutation support the result. Five states and the
general regular case remain UNKNOWN. All six formulas/traces are preserved in
41 lossless archive parts, including the incomplete five-state trace and all
finite negative and UNKNOWN outcomes.

## Complete sharp-clock kernel proof and reciprocal renewal audit — 15 October 2026

The [new formal checkpoint](coordination/2026-10-15-sharp-kernel-and-renewal-audit.md)
completes the actual-orbit Lean proof that the exact (4,4,0) clock lasts at
most 26 transitions and makes at most three consecutive seven-step returns.
All finite rank inputs and return-endpoint links are kernel checked, with
211 transitive audits including 29 prerequisites. A separate fresh audit
rebuilds the external renewal stream's exact 42 raw-symmetry declarations.
Full build reconciliation, independent review and source snapshots are
retained. Neither theorem resolves 196 or decimal Lychrel existence.

## Intrinsic seam and finite-seed continuation — 15 October 2026

The [new checked handoff](coordination/2026-10-15-intrinsic-seam-and-quantifiers.md)
replaces partition search with an exact adjacent high-coefficient/9 criterion
and proves that singleton blocks maximize the carry defect. The canonical
numeric bridge certifies one safe step. A separate all-width family has
arbitrarily large initial defect mass, loses every defect immediately, and
reaches a palindrome at time 2. Two new Lean modules have 31 supporting theorem
declarations and 5 definitions, with matching branch and independent root audits.

The [finite-seed report](research/main_existence_attempt/continuation_pass/finite_seed/FINITE_SEED_OBSTRUCTIONS.md)
shows why specified growth, finite-delay density, exact predecessor-set and
pair-word quotient properties alone cannot extract an infinite survivor: a
fully terminating artificial map can share them. It also proves an unbounded
safe-fiber obstruction to every positive weight nonincreasing with seed size
for actual reverse-and-add. These are written all-parameter arguments with
independently replayed finite controls. No persistent invariant or fixed finite
Lychrel witness follows.

## Seam symmetry in every base at least three — 15 October 2026

Building on the external renewal theorem, the [new all-base proof](coordination/2026-10-15-general-base-seam-results.md)
establishes arbitrary-partition raw symmetry iff actual palindromicity,
the exact active-seam/mass identities, and a safety criterion from two
positive-terminal intervals with different isolated carries. Nine Lean
supporting declarations and complete independent controls are retained,
including six binary failures. This is one-step structure, not an
all-time invariant or a proof for 196.

## Refined clock bounds: 94 returns and 98 periods — 14 October 2026

The [new component-specific proof](coordination/2026-10-14-component-bounds-results.md)
improves the all-branch seven-step (4,4) return bound from 232 to 94 and
the full scalar-clock period bound from 236 to 98. It uses exact child
subgraphs and checks all finite transients. Complete independent job
certificates and seven new generic Lean composition theorems are retained.
These conservative exclusions retain their exact clock hypotheses and
do not resolve 196 or decimal Lychrel existence.

## Full scalar clock obstruction — 14 October 2026

The [new scalar theorem](coordination/2026-10-14-scalar-clock-results.md)
bounds the full outer sequence (4,8,16,7,15,6,13) by at most 236 periods,
with a stronger width-sensitive formula. Every inner temporal history is
allowed. Complete independent arithmetic/rank audits and fifteen generic
Lean weighted-path theorems are retained. Two different capped clocks
remain UNKNOWN, with all completed evidence and exact recovery records
preserved. This does not exclude all outer-4 returns or settle 196.

## All-branch seven-step 44 return bound — 14 October 2026

The [new complete obstruction](coordination/2026-10-14-broader-return-results.md)
allows all three seven-step return branches to prefix (4,4), including
arbitrary changes between branches. For any admissible initial width
L >= 2, the number of consecutive returns is at most
228 + max(0,ceil((14-L)/3)) <= 232. Complete independently checked graph
and weighted-rank certificates include every finite transient. This
conservative bound closes the broader seven-step return route; it does
not settle 196 or decimal Lychrel existence.

## Sharp all-width obstruction to the seven-step clock — 14 October 2026

The [complete checked obstruction](coordination/2026-10-14-seven-step-obstruction-results.md)
proves that an admissible word of any finite width at least six can have
at most three consecutive seven-step returns to prefix (4,4,0). A complete
six-column rank certificate and independent 96,026-control audit give
the bound; an actual orbit attains three safe returns and 26 clock
transitions. Eight Lean theorems supply the actual local projection.
Full kernel integration of the rank certificate remains in progress.
This closes this fixed-clock route; 196 and Lychrel existence remain open.

## Checked seven-step reset and collision mass — 14 October 2026

The [latest shared handoff](coordination/2026-10-14-seven-step-results.md)
supplies an exact conditional seven-step return of prefix (4,4,0), its
middle operator and safety criterion, a 29-declaration actual-boundary
Lean audit, and 17 formal collision digit-mass declarations. Full finite
catalogs and independent counterexamples show why the guard and safety
conditions cannot be dropped. A class preserved by this return remains
unsupplied; there is no infinite-safe seed or proof for 196.

## Completed renewal and collision-safety pass

The [completed renewal report](research/main_existence_attempt/renewal_pass/RENEWAL_STATUS.md) and [independent root review](research/main_existence_attempt/renewal_pass/ROOT_REVIEW.md) collect the new results and their limits. Four Lean modules contain **135 audited supporting declarations**: the already published 49-declaration gate, 16 prefix declarations, 28 incoming-carry declarations, and 42 raw-symmetry/actual-decimal safety declarations. This is an audit count, not a count of independent major results. Each module has a fresh source rebuild and a separate root audit using Lean 4.19.0 and only standard logical axioms.

The new positive safety criterion is concrete: for a canonical whole pair word and any partition into nonempty blocks, a nonzero actual initial-nine seam mask K implies that the next ordinary output is nonpalindromic. The [written proof and full controls](research/main_existence_attempt/renewal_pass/seam_audit/STATUS.md) and [actual-partition Lean bridge](research/main_existence_attempt/renewal_pass/lean/raw_symmetry/STATUS.md) include 99900 -> 100899. The separate [combined collision corollary](research/main_existence_attempt/renewal_pass/external_review/COLLISION_SAFETY_COROLLARY.md) uses the other stream's exact component-closure theorem: failure of independent component closure also certifies one-step safety, including mixed overflow clocks with K=0. That combined corollary is a written proof. Neither criterion is proved to regenerate indefinitely.

The [generalized gate classification](research/main_existence_attempt/renewal_pass/constructive/STATUS.md) gives twenty core pairs and 80 two-step repairs for all r>=1. Four spacer families permit genuine repairs at times 2 and 4, with all four outputs safe; their proposed time-6 repair fails by the exact outside-coefficient discrepancy 14 versus 15. The [language work](research/main_existence_attempt/renewal_pass/language/STATUS.md) proves a finite-memory projection theorem and infinitely many F10 closure failures that no finite edit removes. Its inverse ladder has stated first-hit times 15,14,13,12,11; the [formal prefix obstruction](research/main_existence_attempt/renewal_pass/lean/prefix/STATUS.md) stops the selected cylinder, while an explicit outside-cylinder ancestor prevents a claim about every ancestry branch.

The [arbitrary-block identity](research/main_existence_attempt/renewal_pass/constructive/collision_response/SEAM_RESPONSE.md) is D=E+(x-10)K, with actual incoming carries, all-nine blocks and actual-width reflection. The full polynomial identity remains a written proof; the [28-declaration incoming-carry module](research/main_existence_attempt/renewal_pass/lean/incoming_carry/STATUS.md) supplies its local formal bridge. The all-partition audit also proves that raw E symmetry is equivalent to actual output palindromicity and forces K=0, correcting the earlier symmetric-E/nonzero-K proposal. The original proposal and its correction are both retained.

The [independent seven-step graph reconstruction](research/main_existence_attempt/renewal_pass/external_review/seven_step_graph/) verifies the sharp impossibility of four consecutive returns to prefix (4,4,0) at intervals of seven: 48,013 vertices, all 96,026 labeled controls, 61,731 edges and maximum phase-zero rank 26. Seed 4401198500000 attains three safe returns. This is a written all-width inclusion argument with a complete independently checked finite rank certificate, not a Lean-kernel rank proof. The newer external broader (4,4) return bound is preserved with its own audit and is not claimed as our local replay.

Every substantive source, raw result, log, failed attempt and UNKNOWN outcome in this completed renewal snapshot is retained, including full compressed comparison/control archives. The [22-seed join search](research/main_existence_attempt/renewal_pass/tails/FINITE_JOIN_CHECK.md) remains finite evidence through 1,500 additions. [The final shared handoff](coordination/2026-10-14-renewal-complete.md) states what the other stream can reuse and the missing all-time obligation.

## Checked collision follow-up — 14 October 2026

The [new shared handoff](coordination/2026-10-14-collision-results.md)
publishes 24 Lean carry-response/transfer declarations, exact zero-gap
collision and closure theorems, a complete independently verified
10,000-state driver, and an explicit infinite family of finite seeds safe
through time 10000 for every r>=5078. The smallest certified member has
10163 digits. We also independently rebuilt the concurrent 49-declaration
gate. The full trace is retained losslessly in parts; follow the handoff's
restore command before replay. No infinite-safe seed or proof for 196 is
supplied.

## Reviewed concurrent contributions — 14 October 2026

The [reviewed contribution index](contributions/README.md) adds a Lean-proved
shorter safe seed `2*(10^(floor(7R/4)+1)-1)` through time R; universal finite
first-hit classifications for four delayed-gate cores; and explicit
finite-horizon density bounds plus exact finite separation exhaustion, with the deterministic marker implication
checked in Lean. The growing-horizon density result permits
`H(L)=max(1,floor(c*log10(L)))` for every `0<c<2/7`, as digit width L grows.
These results do not supply an infinite safe seed or prove the claim for
196. Full sources, compiler logs, exact certificates and independent
replays accompany the [dated handoff](coordination/2026-10-14-checked-contributions.md).

## Latest checked renewal results

The [new Lean gate](research/main_existence_attempt/renewal_pass/lean/STATUS.md) proves exact two-step delayed overlap repair for every `r>=1`, outside coefficient `1<=p<=4`, and core `u>=1, v>=5, u+v<=8`. It proves positive-step 1/2 palindrome safety for every ordinary decimal realization, supplies a finite realization, and identifies the third-step palindrome criterion exactly: `p<=2, u=1, v=5`. Both the full source rebuild and independent root recompilation passed the complete transitive audit of 49 supporting theorem declarations with only standard logical axioms. The returned tuple leaves this source's original six-core domain; this does not exclude a compatible second repair in a larger domain. See the [shared formal handoff and reproduction commands](coordination/2026-10-14-formal-gate.md). No recurrent construction or main existence result follows.

For the original overlap family `A = 1 0^r (u,v,v,u) 0^r 1`, `Q = (1+x)A`, the first positive palindrome time is 3 for `(u,v)=(1,5)` at every `r>=1`; 4 for `(2,5)`, `(2,6)` and `(3,5)` at every `r>=1`; and 11 for `(1,6)` at every `r>=5`. These are written all-parameter proofs with an independent sparse-polynomial certificate replay, not Lean theorems. The exact finite boundary cases, all 216 census outcomes, failed certificate attempts and research logs are retained. The four smaller `(1,6)` spacers and the remaining `(1,7)` cases keep their stated finite-horizon UNKNOWN scope. See the [proof and limits](research/main_existence_attempt/renewal_pass/tails/STATUS.md) and [shared mathematical handoff](coordination/2026-10-14-tail-termination.md).

## Previous correlation and finite-delay results

The [publication policy](PUBLICATION_POLICY.md) records the expanded retention rule for new work. The [renewal coordination checkpoint](coordination/2026-10-14-renewal-start.md) records current assignments, the [concurrent contribution handoff](contributions/COORDINATION.md), observable repository activity and a shared handoff format; these checkpoints make no new mathematical claim.

For every natural D, define `C_D = 2 * (10^(2D+1) - 1)`. The new Lean development proves that this finite integer avoids palindromes at every time from zero through D. It also proves `FiniteDelayBound D -> IsLychrel C_D`, where the hypothesis bounds every finite positive first-palindrome time of every positive decimal integer by D. The safe-prefix family is proved; **no value of D satisfying the universal bound is supplied**. The unconditional existence-or-unbounded-finite-delay disjunction is nonexclusive and does not select either branch. The four mathematical modules contain 63 audited supporting theorem declarations; this count is not a count of independent major results. Their fresh source rebuild and complete axiom audit, and the root's independent recompilation, passed with Lean 4.19.0.

The construction branch also proves a positive two-step delayed-repair identity for every spacer length `r >= 1` and six stated core pairs. With `A = 1 0^r (u,v,v,u) 0^r 1` and `Phi(A) = (1+x)A`, both positive iterates of the whole word are nonpalindromic and `G^2(Phi(A)) = Phi(G^2(A))`. The intermediate state leaves the overlap form. This is a finite safe return identity, not a recurrent construction: the spacer stays fixed and every returned core leaves the original eligible starting domain. The `(u,v)=(1,5)` branch reaches a palindrome at the third positive iterate for every r. The [written carry proof](research/main_existence_attempt/correlation_pass/constructive/VARIABLE_OVERLAP_AND_GATE.md) and independent ordinary-integer controls are retained. The new checked p=1,...,4 gate above now complements this earlier written proof.

Full-configuration language checks certify 146 particular class collisions through observation depth ten; they do not exclude arbitrary refinements or later entry into an invariant. The 65,170-entry antichain snapshot is independently checked, while its exploration remains incomplete. Nine prescribed free-clock prefix schedules have exact extension obstructions; the surviving candidate's cyclic search reached depth 16 and a graph cap, so its unrestricted-width boundary problem remains **UNKNOWN**. [The consolidated report](research/main_existence_attempt/correlation_pass/CORRELATION_PASS_STATUS.md) states the exact scope and remaining obligations.

The principal completed results include:

- Exact decimal carry and pair-word semantics, four-step same-carry normalization with sharpness, reconstruction from eleven complete carry words, and fixed-width inverse injectivity.
- Unbounded digit sums on every tail, followed by explicit uniform digit-sum escape bounds independent of the seed, initial width, and starting time. These do not imply palindrome avoidance.
- A fixed-modulus/exact-length obstruction with a written all-moduli palindrome construction, and a checked six-step divisibility-by-11 result.
- Exact exclusions of specified boundary, score, and language constructions, with a clear distinction between full finite certificates and incomplete searches.
- Bounded ancestry of every fixed finite target, with Lean proofs of empty intersections of the stated ancestry predicates. This is compatible with infinite forward orbits whose targets grow.
- An independently checked exclusion of all 8,396 terminal flags of one saved safe-ancestry NFA. It excludes unions of those component languages, not arbitrary regular invariants.
- An exact delay/ancestry equivalence and a verified 289-step terminating example. Unbounded finite terminating delay is not proved.
- A repository-specific engine review with pinned provenance, explicit tested scope, and reproducible audit findings; see the latest repository-review report under the ancestry pass.

## Evidence levels and limits

The main arithmetic, digit-sum, and finite-ancestry Lean sources use Lean 4.19.0 and the standard logical axioms documented in their axiom audits. The separate boundary-certificate formalization uses `native_decide` for finite checks and therefore also depends on `Lean.ofReduceBool`; its generic logical soundness proofs are identified separately. A conditional Lean implication is not a supplied instance of its hypotheses. Generic lemmas and uninstantiated proof interfaces are not main existence proofs.

Written proofs, independent arithmetic replays, solver-reported outcomes, bounded experiments, and timeouts have different scopes. `UNKNOWN` remains unknown. Finite long trajectories do not establish infinite nontermination; an empty safe kernel on a fixed transition table does not exclude all automata; one failed construction does not exclude all decimal Lychrel numbers. Digit-sum statements continue iteration after palindromes.

## Publication coverage

Every written research finding and original research source file is retained, together with outcome records and certificates needed for direct replays. The binary antichain snapshot and its exact depth-four observer dependency are retained in full. The initial and correlation releases omitted some large generated graphs, incomplete solver states, repeated raw logs and rendered duplicates while preserving their conclusions and reproduction sources. Under the expanded [publication policy](PUBLICATION_POLICY.md), new renewal checkpoints retain every substantive source, result, failure, UNKNOWN outcome, log and available development attempt. The complete renewal snapshot retains all its genuine research output; only copied build directories, compiled products and caches are omitted and individually inventoried. [PUBLICATION_SCOPE.md](PUBLICATION_SCOPE.md) distinguishes the historical selection from the current retention rule.

[INVENTORY.tsv](INVENTORY.tsv) and [INVENTORY.json](INVENTORY.json) account for every file in the initial, correlation-pass, completed renewal and accepted continuation source snapshots with its original SHA-256, size, publication decision, reason, and report mapping. The original early-checkpoint records remain historical provenance alongside the completed renewal snapshot. Historical snapshot entries remain provenance records. [FILES.md](FILES.md) lists every published file; [MANIFEST.sha256](MANIFEST.sha256) verifies release contents, including binary certificate bytes. These manifests are provenance aids, not mathematical certificates. Repository engines, production checkpoints, and files outside `proofs/` are unchanged by this publication.

No third-party license is invented for the research or for cited sources. Existing repository licensing and any file-specific notices continue to apply.
