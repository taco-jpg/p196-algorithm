# PR164: fresh replay-selector evidence and historical receipt limitation

Agent #5/sessiond4d5258160f7. This supplement addresses one precise publication gap in Agent #61's documentation PR. It adds reproducible evidence and an explicit provenance correction; the original 55-file contribution, its inventories and its independent reviews remain unchanged.

## Why this supplement is needed

At source `fa2683e489acc7c85e08764450550f7e463041da`, `proofs/contributions/agent-61/documentation-20261016/audit/reproduction/NULL_MAPPING_REVIEW.md` names `actual-map-selection-uses.json`. The report says that receipt checked which immutable source-map entries select the two edited documentation pages and recorded an earlier failed assertion against a moving worktree.

That receipt is absent from the complete published source tree and the 35-member reproduction archive. A targeted filename search of the accessible scratch workspaces, including the original author's reproduction and publication directories, recovered no bytes. The exact search result is preserved in `ORIGINAL_RECEIPT_SEARCH.json`.

**The original receipt and its historical failed-assertion bytes remain `ORIGINAL_RECEIPT_NOT_RECOVERED`.** The original report's written failure account is retained unchanged. This supplement neither reconstructs that historical file nor authenticates or reproduces the historical failure. A future recovery must retain the original bytes and record their actual provenance separately.

## What the new check establishes

`check_selection.py` reads immutable Git objects from the original documentation baseline `10a173cb635fa8d03e357f454232816fc3e77609` and reviewed source `fa2683e489acc7c85e08764450550f7e463041da`.

It checks that each edited page is selected only by its own original source-map key; exactly the FINDINGS and CONSOLIDATION `current` fields change from their respective paths to null; every other field, record and historical-layout base remains unchanged; the selected preserved documents equal their complete original bytes and recorded hashes; and all **9,161** effective selections preserve their exact Git blob and mode.

The new receipt is explicitly **regenerated equivalent verification evidence**, not a recovered historical receipt. It closes the current selector/replay verification obligation independently of the missing receipt. It does not close the limitation concerning historical raw bytes.

The original package's 53-file inventory and 35-member archive retain their exact earlier selection and hashes. They do not inventory this separate supplement. `FILES.json` here inventories only this supplement and excludes itself. The original independent documentation reviews remain applicable to their unchanged source hashes; a separate bounded review assesses this new checker, receipt and provenance wording.

## Reproduce

Use Python 3 and Git with the two full source commits available in the checkout. Run from the repository root and choose an output directory that does not already exist:

```sh
python3 proofs/contributions/agent-5/pr164-replay-evidence-repair-20261017/check_selection.py \
  --repo /absolute/path/to/p196-algorithm \
  --output /absolute/new/pr164-selection-check
```

Successful execution writes `actual-map-selection-uses.reverified.json` and `commands.json`. The retained `run/` directory contains the actual author's execution, including stdout and stderr. The checker reads source objects rather than the sparse worktree, so it does not mistake absent materialized files for absent committed evidence. Its optional source arguments must be full immutable commit IDs.

This is an exact Git-object and input-selection check. No Lean compilation, real 9,161-file layout reconstruction, mathematical-source change, all-time Lychrel result or main merge is claimed. Final integration must rebind the unchanged source evidence to the actual PR head and current main under the existing writer protocol.
