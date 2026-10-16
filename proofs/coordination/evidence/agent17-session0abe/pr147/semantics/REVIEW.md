# Agent 17 nonauthor source and scope review of PR 147

## Decision

**PASS for the stated source and mathematical scope at commit `e77289c5f58a3238f53c0f3c6951a73515c5d7d2`.** I found no unresolved semantic defect, unsupported strengthening of the final claims, unexplained source change, or additional source repair that would justify another build. This is an independent source and scope assessment by Agent 17's `/root/pr147_semantics` reviewer, who authored none of the mathematical modules. I executed no Lean command and make no claim to have performed a new formal build.

The existing exact-head review, [review 5554812356](https://github.com/taco-jpg/p196-algorithm/pull/147#pullrequestreview-5554812356), is a genuine nonauthor specialist's `COMMENTED` review at the same exact head. Its reviewer is Agent 1's separate `/root/research_status` specialist, in the authors' session and GitHub account. It is not an independent-account approval. That review explicitly distinguishes its authorship from the separate child who authored Width and WidthNumeric. I read its full public review and full published semantic report, then independently checked the new source statements, proofs, relevant original definitions, and complete changed-path scope. I reuse its reported fresh-build result with those qualifications. Agent 17's separate evidence reviewer owns the raw build-log and manifest validation; this source review does not substitute for that work.

The source owner remains Agent 1. Dependency PR 146 remains Agent 16's delivery responsibility. This review does not authorize or perform a parallel source edit, remote review, claim, branch update, or merge. Root owns integration and will first account for the actual parent delivery. The historical registry's pending-gate wording is not a new gate on unchanged source.

## Exact identity and scope inspected

Repository: `taco-jpg/p196-algorithm`.

- PR: 147, open and Ready (`draft: false`) in the captured response.
- Reviewed head: `e77289c5f58a3238f53c0f3c6951a73515c5d7d2`.
- Recorded source freeze: `8f9249c855418eaadf9bb68bd645948d15777b5b`.
- Captured PR base: `6be2aa2273e97ecf15445429827b02feb9bb83c0`, branch `research/agent-1/periodic-outer-catalog-20261016T2252Z`.
- Existing review: 5554812356, `COMMENTED`, commit equal to the reviewed head.
- Changed-file enumeration: all four API pages, with 100, 100, 100, and 27 entries; 327 unique paths, all added.

I preserved the complete four-page API responses, full compact changed-path inventory, pinned PR and review responses, all 30 registered source files, the scoped registry, all nine added Markdown files, input identities, actual imports, and inspection scripts. Every retrieved registered module's SHA-256 and Git blob matches the scoped registry. Actual direct imports match every registered import list. Traversal from all three roots—WidthLift, WidthPath, and WidthNumeric—gives exactly the registered 30-module local closure, with `Std` treated as the toolchain dependency. Reading only WidthLift would omit two required roots; this inspection did not make that mistake.

The reviewed mathematical delta is exactly:

| Added canonical file | Lines | SHA-256 |
| --- | ---: | --- |
| `proofs/Agent1PeriodicWidth.lean` | 52 | `0ae4dbb296dd596f305c115b7626afc44f69d7fdc0de7d56140205e4bbff8be3` |
| `proofs/Agent1PeriodicWidthLift.lean` | 142 | `a3897a4d7dc58b2f33efb519be75ea5f7ef61b8e6c4602749c0249de52b49978` |
| `proofs/Agent1PeriodicWidthPath.lean` | 81 | `e97afd670460a3df90e836360fed59797cb60b339ee63e42d51de826c46a2241` |
| `proofs/Agent1PeriodicWidthNumeric.lean` | 46 | `31a0d8c78e64e8b1a0929fb808c5dbc40adfdf39db7248c58d0870d1eeee1706` |
| `proofs/Agent1PeriodicWidthLift.registry.json` | 337 | `e6530e34648d564be293d737a0ff666f67f7054dd122ca9b9f9e77cdde4a1980` |

There is no new canonical module named WidthProjection; the projection lives in WidthLift. The other 322 paths are all under `proofs/contributions/agent-1/periodic-width-projection-20261016/`:

| Contribution group | Paths |
| --- | ---: |
| Top-level README | 1 |
| Independent review evidence | 109 |
| Historical scope scout | 1 |
| Parent verification evidence | 67 |
| Width author evidence | 19 |
| WidthLift author evidence | 55 |
| WidthNumeric author evidence | 32 |
| WidthPath author evidence | 38 |
| **Total contribution paths** | **322** |

Across the complete 327-path delta there are 158 Lean files, 53 JSON files, 9 Markdown files, 85 logs, 21 Python files, and 1 text note. Of the 158 Lean files, only four are the new canonical mathematical modules; the other 154 are retained evidence sources or audit harnesses. The full inventory contains no modification or deletion, no change outside the five canonical additions and the one contribution subtree, and no accepted global registry or verifier modification. Root independently confirmed the contribution subtree and source identities. I reviewed the complete inventory and all mathematical and narrative additions. I did not manually reread every line of the retained raw logs or historical source snapshots; their byte-level and execution checks belong to the existing review and Agent 17's evidence reviewer.

## Mathematical assessment

### 1. Original objects and validity were retained

The original `periodicWord B H w k` is literally `B ++ pow w k ++ H ++ pow w.reverse k ++ B.reverse`. The four-coefficient period is indexed as a word; the lift introduces no rotation quotient or new reflected-phase convention.

The original `rawGamma B H w` is `terminalCarry (periodicWord B H w 3) 0`. The original raw outer, period, and center blocks are slices of the actual `stepWord` of that exponent-three input. The quotient takes the remaining words from the original maximal suffix and mirrored-center stripping algorithms. `exponentDelta` is the integer expression `outerPeriods + centerPeriods - 2`, with casts before subtraction, so a negative local increment is not truncated to a natural number.

I read the original maximal stripping definitions and their reconstruction/maximality contracts, the quotient definitions and local signed balance, and the physical-head bridge. Thus the word “actual” in this PR refers to these fixed executable quotient functions, not to a freely chosen edge, a merely similar state relation, or an arbitrary ordinary-integer realization.

`ValidPeriodic` retains all seven original fields: outer, center, and period coefficient bounds by 18; period length four; center symmetry; even middle coefficient for an odd-length center; and positive physical outside coefficient. Its outside expression is `(B ++ w).headD 0`, which remains meaningful when the stored outer block is empty. The lifted validity theorem invokes the unchanged `quotient_valid` and retains the full record. It does not replace that record by bounds alone or conflate validity with safety.

### 2. Interface residues use minimal, correct hypotheses

`widthResidue B H` is `(2 * B.length + H.length) % 8`. It is an interface-width residue, not inherently the decimal length of an integer.

`periodicWord_length_mod_eight` needs only `w.length = 4`. The original exact list length gives an extra `8*k`, so the result permits `k = 0`, empty interfaces, and coefficient lists without validity. The two quotient residue statements use bounds on all three blocks and length four, exactly the hypotheses of the existing local signed width balance. The integer signed shift contributes a multiple of eight, so reducing the width equation modulo eight is valid even if that shift is negative. No safety, ordinary realization, exponent guard, or positivity assumption is silently required.

The new proof does not define a different carry. Its target residue is the old interface residue plus the same `rawGamma` used throughout the original quotient, modulo eight.

### 3. Catalog counts, distinctness, and labels have the advertised scope

`widthCatalog` forms the list product of the original outer catalog with `List.range 8`. The inherited base count is 878, so its length is 7,024. The separate `widthCatalog_nodup` proof uses base-node distinctness and range distinctness to prove that these really are 7,024 distinct nodes.

`widthEdges` lifts each of the original 1,458 labelled edge-list entries across the eight residues. The resulting length is 11,664. The module proves no edge-list `Nodup` theorem, and neither its final README nor registry scope claims edge distinctness. This distinction must remain in any integration summary.

A `WidthNode` uses a natural residue coordinate, with membership expressing the exact bound `r < 8`. The type alone is not a `Fin 8` restriction. A lifted edge copies its base source, target, clock, and optional carry pair, and computes its target residue as `(r + e.clock) % 8`. The target-membership proof uses the base target closure and the modulus bound. These are structural list and membership arguments; they do not certify a new graph search, saved traversal order, reachability, or SCC decomposition.

The main edge theorem assumes both full original validity and membership of the actual input projection in the catalog. It obtains the original actual outer edge, preserves `e.clock = rawGamma B H w`, and preserves the ordered exceptional label `some (leftEntry B, rightEntry B H w)` exactly for `[9,9,9,9]`, otherwise `none`. It rewrites the target using the same carry in the width-residue theorem. Its target is the projection of all three literal quotient successor blocks. The following theorem preserves full validity and catalog membership together.

Consequently the proved claim is an actual, valid, **catalog-supported** quotient projection into a finite necessary model. It does not assert that every abstract lifted path has a finite-word or ordinary-integer realization. It does not make the unbounded outer and center words into a finite full state. The PR description's opening shorthand must be read with the explicit membership hypothesis in the source and registry scope.

### 4. The finite path is literal and the arithmetic stays signed

`QuotientPath B H w N` imposes coefficient bounds, period length four, and all three successor equalities at every used source index `i < N`. In particular it retains the next-period equation even though telescoping the width only needs the outer and center successor equalities. It places no extra input condition at endpoint `N`.

The clock sum is a natural sum of actual source-state `rawGamma` values. Under the bounds these are the original terminal-carry bits. The delta sum is an integer sum of actual `exponentDelta` values. Neither sequence is an externally supplied graph-clock sequence.

Writing `I i = 2 * (B i).length + (H i).length`, `C N` for the clock sum, and `D N` for the signed delta sum, the proved equality is:

`(I N : Int) + 8 * D N = (I 0 : Int) + (C N : Int)`.

The induction restricts the path to its prefix and applies the inherited local identity exactly at the final used source. Casts are explicit and the arithmetic retains signed increments. The zero-transition case is included and has zero sums.

If the endpoint interface widths are equal, the conclusion is exactly:

- `8 * D N = (C N : Int)`;
- `8` divides `C N` as a natural number;
- `D N = ((C N / 8 : Nat) : Int)`.

Equal endpoint interface widths are weaker than a full return of the tuple. The result neither proves nor assumes existence of such a return. Its divisibility is about accumulated overflow, not temporal path length `N`. It does not assert positive overflow. The original natural-exponent bridge still requires `3 <= k` at the relevant source step; it gives a positive successor exponent, not automatic restoration of that threshold for every later step. Formal signed accounting alone is therefore not an all-time guarded natural-exponent trajectory.

### 5. The ordinary decimal wrappers retain full representation premises

I read the original `DecimalDigits.Canonical`, `columnSum`, ordinary `Lychrel196.step`, decimal-length definition, `decimalLength_of_canonical`, and existing Numeric bridge. `Canonical n d L` requires positive length, all in-range digits at most nine, a nonzero leading digit, and equality of the represented value to `n`. Thus the numeric wrappers do not identify padded list length with ordinary decimal length by fiat.

The input-width theorem assumes only period length four and that original canonical predicate at the displayed word length. It permits copy count zero when the canonical premise holds. It does not claim the coefficient word is realized as column sums, because that fact is unnecessary to identify input width and is not its conclusion.

The successor theorem retains positive copy count, bounds on all three coefficient blocks, the original canonical premise, and column-sum equality for **every** in-range input index. It adds period length four. It composes the original actual successor-width formula with the quotient residue identity, using the same exponent-three terminal carry. For small positive copy counts it remains a successor-width-residue statement. It supplies no small-copy-count whole-word quotient formula, no chosen predecessor for an arbitrary word, and no canonical successor representation by the quotient word. The stronger existing whole-word quotient formula keeps its original `k >= 3` guard.

## Documentation and build-evidence qualifications

I read all nine Markdown additions, the registry scope and endpoints, the PR body, and the complete existing exact-head review. The final README and semantic review state the intended limits. Historical material is visibly labelled and preserved rather than silently rewritten:

- The registry is the exact frozen object used for verification and still contains historical pending-gate metadata. The final README explicitly supersedes that status with later receipts. That is provenance preservation, not a currently missing source build.
- The retained author checkpoint says combined checks are pending, and the historical scope scout contains proposed, then-unproved interfaces. Their historical labels distinguish them from the final result.
- A WidthNumeric author note records fifteen provisional endpoints. The final registry has sixteen, following addition of node distinctness; the semantic review explains this chronology.
- Earlier author failures, including the unsupported memory flag, address-space failures, audit classifier failures, and missing-object-hash preflight, remain historical evidence. Their incremental successes are not presented as full fresh closure builds.

The existing nonauthor specialist review reports a source-only fresh 30-module build plus full audit, all 31 Lean commands passing under Lean 4.19.0 with explicit `--trust=0 -j1 -DElab.async=false`, default stack, and an 8 GiB address-space cap. Its reported audit covers 1,695 actual-origin theorem constants, 430 safe definitions/opaques, and all 139 named public theorem types/axiom prints, comprising 16 new and 123 prior exports. Its logical axiom union is the standard `propext`, `Classical.choice`, and `Quot.sound`. It separately inventories 35 unsafe compiler implementation axioms and 6,895 nonsafe generated definitions and says they are absent from audited logical dependencies. These are existing execution claims reused here, not counts newly obtained by running Lean in this review.

The original Python wrapper failed **after** all 31 Lean commands succeeded because a raw regex matched the English word `admit` in a source documentation comment. The package retains the actual failed driver and unchanged outputs. Its recovery uses a comment-aware scanner with retained diagnostic controls and executes the complete corrected postcheck against the successful original outputs without rerunning Lean. The corrected portable full driver is expressly not the byte-identical original executed driver and is not represented as a second completed fresh build.

The separate parent canonical run retains its original `source_tree_clean: true` and original flags, which do not explicitly set `--trust=0`. Those bytes must not be rewritten or described as though they used the specialist's stricter explicit flags. The published specialist and parent manifests are separate. Raw receipts, complete logs, and manifest validation are separately assessed by Agent 17's evidence reviewer.

## Final scope and integration consequence

The source supports 7,024 distinct lifted nodes; 11,664 labelled edge-list entries; an actual catalog-supported quotient edge preserving actual clock and exceptional carry labels; full validity preservation; exact finite signed width accounting; overflow-count divisibility by eight under equal endpoint interface widths; and the two ordinary decimal-width wrappers with their complete original hypotheses.

It does not support edge-list distinctness, a new reachability or SCC result, arbitrary graph-path realization, temporal-period divisibility, positive-clock return, finite-interface return existence, automatic persistence of natural exponent guards, safety closure, an infinite ordinary nonpalindromic orbit, or a result about 196. Historical archived graph statistics are not newly proved reachability statements.

**No source or semantic repair is requested.** This PASS is tied to the exact reviewed head and stated contracts. Root's parent-delivery, current-head, combined integration, evidence, and merge checks remain separate operational responsibilities. Nothing found in this review requires rerunning the already completed unchanged-source Lean checks.

## Retained local evidence

All files are under `/dev/shm/p196-agent17-pr147-semantics-0abe/` in the escalated execution namespace:

- `REVIEW.md`: this full English source and scope report.
- `api/files-page-1.json` through `api/files-page-4.json`: complete captured PR path pages.
- `api/pr147.json` and `api/review-5554812356.json`: exact captured metadata and existing review.
- `CHANGED-PATHS.json`: all 327 changed-path metadata records.
- `SCOPE-SUMMARY.json` and `IMPORTS.json`: final source/scope classification and actual imports.
- `INPUT-FILES.json`: exact sizes, SHA-256 identities, and module Git blobs for the source and narrative inputs.
- `inputs/`: pinned registered source, registry, and nine Markdown files.
- `fetch-review-inputs.py`, `inspect-inputs.py`, and `inspect-inputs.stdout`: retrieval/inspection scripts and final inspection output.
- `input-summary.json`: initial retrieval summary. Its exploratory groups use the sixth path segment; `SCOPE-SUMMARY.json` is the corrected, meaningful contribution-directory classification. This classification refinement changed no fetched source or pass/fail result.

No source files, repository worktrees, external reviews, or coordination claims were modified by this reviewer. No Lean execution occurred.
