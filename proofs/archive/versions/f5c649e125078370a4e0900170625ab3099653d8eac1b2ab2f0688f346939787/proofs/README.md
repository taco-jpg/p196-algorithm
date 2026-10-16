# Decimal reverse-and-add research findings

**Decimal Lychrel existence remains unproved. This collection does not prove that 196 is a Lychrel number, does not disprove decimal Lychrel existence, and contains no verified positive Lychrel witness.**

This directory publishes the research findings, written proofs, formal source, finite certificates, failed constructions, and reproducible searches accumulated through 14 October 2026. The existence goal is separate from the completed supporting theorems. No novelty, external peer review, or publication-priority claim is made. The audits described here are internal and AI-assisted.

Start with [the findings and evidence matrix](FINDINGS.md), [the complete written-report index](REPORTS.md), and [reproduction instructions](REPRODUCE.md). The [latest consolidated ancestry and repository-review report](research/main_existence_attempt/ancestry_direct_pass/ANCESTRY_DIRECT_STATUS.md) records the final pass. The original research tree is preserved under [research/](research/), so relative imports and certificate paths remain meaningful. Its [historical overview](research/README.md) records successive passes; later reports supersede earlier open questions only where explicitly stated. Historical statements such as “not yet formalized” or “nothing published” describe that checkpoint, not the current release.

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

Every written research finding and original research source file is retained, together with compact outcome records and selected certificates needed for direct replays. Large generated state graphs, incomplete solver states, repeated raw logs, compiled programs, build products, and rendered duplicates are intentionally excluded. Their conclusions and reproduction sources remain present. [PUBLICATION_SCOPE.md](PUBLICATION_SCOPE.md) explains the selection and maps omitted output families to regeneration.

[INVENTORY.tsv](INVENTORY.tsv) and [INVENTORY.json](INVENTORY.json) account for every file in the source snapshot with its original SHA-256, size, publication decision, reason, and report mapping. [FILES.md](FILES.md) lists every published file; [MANIFEST.sha256](MANIFEST.sha256) verifies release contents. These manifests are provenance aids, not mathematical certificates. Repository engines, production checkpoints, and files outside `proofs/` are unchanged by this publication.

No third-party license is invented for the research or for cited sources. Existing repository licensing and any file-specific notices continue to apply.
