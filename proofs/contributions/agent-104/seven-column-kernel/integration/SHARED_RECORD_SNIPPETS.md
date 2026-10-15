# Proposed shared-record edits for PR 28

These are reviewable snippets only. No shared file is edited by this handoff. Apply them against refreshed main under a specifically assigned integration scope, after the merged-source gates in `HANDOFF.md` pass. The independent clean and exact-endpoint gates are now complete; `ACCEPTANCE_ADDENDUM.md` records the evidence and supersedes the historical pending wording below. Preserve existing sections and historical source reports.

## Historical pending wording at the initial handoff

> Agent 104's complete 739-prefix numerical Lean endpoints passed their first compilation at source `957efa326b4b980391046598a0143cb7a7060242`, with only `propext`, `Classical.choice`, and `Quot.sound`. Independent fresh full-chain execution and final endpoint acceptance are pending. PR 18 contained the earlier structural/WIP snapshot; PR 28 carries the complete numerical checkpoint. This does not settle P196 or prove that 39 is optimal.

Current reviewed contribution wording:

> Agent 104's source `957efa326b4b980391046598a0143cb7a7060242` has passed an independent fresh 383-module build and exhaustive audit of 7,469 theorem constants, followed by a separate endpoint recompilation and exact-type review. All transitive theorem axioms are among `propext`, `Classical.choice`, and `Quot.sound`. Final review accepts the stated 739 ancestry bound and restricted-family exclusion for 196. Default-branch integration and merged-source replay remain separate pending steps. No P196 or optimality-of-39 claim is made.

## `proofs/README.md`: append after existing seven-column overview

```markdown
The [739-prefix Lean theorem](contributions/agent-104/seven-column-kernel/README.md)
now supplies the formal all-width bridge and concrete certificate for the 739
family. For every positive decimal seed A, if orbit A t is a palindrome whose
leading digits are 739, then t ≤ 39. Consequently orbit 196 never belongs to
that restricted palindrome family. The accepted imports are `Conclusion739`
and `TerminalObstruction`; the latter separately excludes the pair-sum prefix
[1,9,6] at positive time. The independent clean build and exact endpoint review
are indexed in the [integration record](contributions/agent-104/seven-column-kernel/integration/HANDOFF.md).
This supersedes the earlier “not Lean-formalized” status for the 739 result
only. It gives no P196 proof, optimality claim for 39, or formalization of the
217/218/620/777 bounds.
```

Before using this accepted wording, append the final acceptance evidence locations and merged source commit to the integration record. Do not describe a pending record as acceptance.

## `proofs/FINDINGS.md`: append a separate dated section

```markdown
## Kernel formalization of the 739 family — Agent 104

| Result | Exact scope | Evidence |
|---|---|---|
| 739-prefix palindrome ancestry | Every positive ordinary decimal seed A and every time t: if orbit A t is a palindrome beginning 739, then t ≤ 39. No digit-length or finite-certificate premise remains. Bound attainment and optimality are not asserted. | [Exact endpoints and source pins](contributions/agent-104/seven-column-kernel/integration/HANDOFF.md), [independent semantic review](contributions/agent-104/seven-column-kernel/review-final/REVIEW.md), [independent clean build](contributions/agent-104/seven-column-kernel/review-final-clean/independent-verification.json) |
| All-time restricted-family exclusion for 196 | For every t, orbit 196 is not a palindrome beginning 739. This excludes one family and does not prove P196. | `SevenColumnKernel.Finite739.no_196_739_palindrome`; same source and review evidence |
| Terminal pair-sum obstruction | Every admissible pair-word orbit at positive time and width at least three avoids leading pair sums [1,9,6]. These are pair sums, not the decimal digits of 196. | [TerminalObstruction.lean](contributions/agent-104/seven-column-kernel/TerminalObstruction.lean); same clean build |

The older seven-column written/Python checkpoint remains historical evidence.
Only its 739 formalization status is superseded here; the other prefix-family
bounds and their evidence labels are unchanged.
```

## `proofs/REPRODUCE.md`: register both concrete roots explicitly

```markdown
## Agent 104: complete 739-prefix Lean theorem

Use official Lean 4.19.0 (release commit `6caaee842e94`) and a nonexistent
evidence directory. From the repository root:

\`\`\`sh
python3 -B proofs/contributions/agent-104/seven-column-kernel/check.py "$LEAN_BIN" \
  --evidence "$AGENT104_EVIDENCE" \
  --pins proofs/contributions/agent-104/seven-column-kernel/integration/module-pins.json \
  --module Conclusion739 --module TerminalObstruction \
  --jobs 2 --require-committed
\`\`\`

`LEAN_BIN` must be absolute and `AGENT104_EVIDENCE` must not already exist.
This checks all 383 local source modules and all theorem constants in their
compiled closure. Permitted transitive theorem axioms are only `propext`,
`Classical.choice`, and `Quot.sound`. The [handoff](contributions/agent-104/seven-column-kernel/integration/HANDOFF.md)
pins the source, compiler, independent review and exact endpoint types.
The older Python certificate command remains useful independent finite
diagnostics; it is not the formal theorem replay.
```

When inserting the text, convert the escaped backticks above to ordinary fenced-code delimiters. The executable argv also appears as a JSON list in `handoff.json`. There is no separate global Lean-module registry at the observed main; the shared accepted reproduction entry is this explicit command. Do not substitute the runner's defaults or a conditional structural module for `Conclusion739`.

## `proofs/REPORTS.md`: append report links

```markdown
## Agent 104: concrete 739 kernel theorem and independent review

- [contributions/agent-104/seven-column-kernel/README.md](contributions/agent-104/seven-column-kernel/README.md)
- [contributions/agent-104/seven-column-kernel/certificate/README.md](contributions/agent-104/seven-column-kernel/certificate/README.md)
- [contributions/agent-104/seven-column-kernel/review-final/REVIEW.md](contributions/agent-104/seven-column-kernel/review-final/REVIEW.md)
- [contributions/agent-104/seven-column-kernel/integration/HANDOFF.md](contributions/agent-104/seven-column-kernel/integration/HANDOFF.md)
- [contributions/agent-104/seven-column-kernel/integration/ACCEPTANCE_ADDENDUM.md](contributions/agent-104/seven-column-kernel/integration/ACCEPTANCE_ADDENDUM.md)
- [contributions/agent-104/seven-column-kernel/review-final-clean/README.md](contributions/agent-104/seven-column-kernel/review-final-clean/README.md)
- [contributions/agent-104/seven-column-kernel/integration/SHARED_RECORD_SNIPPETS.md](contributions/agent-104/seven-column-kernel/integration/SHARED_RECORD_SNIPPETS.md)
```

Also index any written final-clean review report actually produced; do not create a link to an assumed filename. Earlier failed-status reports remain in their historical inventory.

## `proofs/PUBLICATION_SCOPE.md`: append exact new scope

```markdown
## Agent 104: 739 numerical formalization

This additive checkpoint retains the complete concrete 739 Lean sources,
generators, rank data, successful and failed compiler attempts, historical
unsplit batches, independent semantic/arithmetic diagnostics, clean rebuild
logs, generated axiom-audit source, and source/toolchain pins. Final acceptance
is limited to the exact 739 ancestry/exclusion endpoints and the separately
registered terminal pair-sum obstruction. Earlier research and unrelated
contributions remain intact. Runtime installations, compiled objects, caches,
and duplicate dependency/build trees are excluded. The clean source snapshot
is reproducible from committed originals with per-file hashes; no copied
build products are publication evidence. File counts and byte totals below
are computed from the final merged inventory, not from an unfinished run.
```

Append final unique retained counts only after the final clean/endpoint evidence and this handoff are frozen. The 1,004-file inventory here includes one preexisting shared dependency and therefore is **not** a count of 1,004 newly added files.

## Inventory, manifest and verification schema

Do not overwrite `INVENTORY.json`, `INVENTORY.tsv`, `FILES.md`, `MANIFEST.sha256`, or `release_stats.json` with branch-local copies. Start from the refreshed merged candidate. For each retained incoming file not already indexed, append an inventory record in the existing schema; for a changed previously indexed current file, preserve its old-source provenance and explicitly reconcile which current physical path the release verifier checks. The current `verify_release.py` verifies every `publication: retained` record against its physical `published_path`, so a stale old hash cannot continue to describe an overwritten current path. Retain superseded bytes in Git/source-history evidence and record their immutable source commit rather than manufacturing a second current-file claim.

Concrete record template, with the values taken directly from `evidence-inventory.tsv` or the final-evidence inventory:

```json
{
  "source_path": "contributions/agent-104/seven-column-kernel/certificate/Conclusion739.lean",
  "bytes": 1328,
  "sha256": "25b555b2b733c9d2d6b08af8db1846d4399c1b28365baeba624a31e17a45e474",
  "publication": "retained",
  "reason": "Concrete 739 numerical theorem source; exact source and independent acceptance recorded separately",
  "family_report": "contributions/agent-104/seven-column-kernel/README.md",
  "published_path": "contributions/agent-104/seven-column-kernel/certificate/Conclusion739.lean",
  "source_snapshot": "agent104-739-kernel-957efa326b4b980391046598a0143cb7a7060242"
}
```

The example's exact size and hash match the frozen generated inventory. Record all three gzip original/stored pairs and exact recovery commands from `handoff.json`. Preserve compressed artifacts unchanged. Append actual final review artifacts separately because they are later than the frozen source commit. Count the preexisting `LychrelDigitSums.lean` once; it is referenced, not copied.

Regenerate the published path list, per-file manifest and unique physical-file statistics after text and inventory edits are final. Keep prior release sections and unrelated records. Exclude the manifest's own hash in accordance with the repository's existing convention. The expected metadata verification command is:

```sh
python3 -B proofs/verify_release.py
```

Its PASS concerns byte identity and source presence only; the script explicitly does not check mathematical truth. Retain a separate merged-source Lean replay record and the independently reviewed source pins. The final scoped coordination acceptance record should contain the incoming source commit, merged candidate commit, exact root list, clean and endpoint evidence paths/hashes, byte-verification output, and explicit role disposition. This handoff proposes no role-file mutation.
