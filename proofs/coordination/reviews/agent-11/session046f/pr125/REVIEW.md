# PR #125 independent review — Agent #11/session046f

Reviewed head: `71fa669acdff9ee203ef28d7db7e31e2f9b5b4af`.
Original branch/merge base: `d591ce6d0cbf2bceab219fe915b1cebcc16a5879`.
Reference main supplied for this review: `2bc42391c63b744951f27fde11af8c7d7958077f`.
Reviewer: independent `/root/review125`, author of no PR mathematical source or evidence correction. No remote mutation, source edit, new branch, or Lean process was performed by this reviewer.

**Verdict: mathematics and retained fresh-build evidence are acceptable; an additive correction of the imported-proof typechecking claim is required before exact-head publication approval.** This is an evidence-label correction, not a failed proof or a request for a new build. After that correction, unchanged mathematical sources and retained execution may be reused under the user's exact-source evidence policy. Current-main combination, platform checks, ownership, Ready transition, formal review and merging remain the integration writer's separate gates.

## Reviewed scope and mathematical interpretation

The complete delta contains 87 additions, including five new overflow modules and an unchanged source copy of Agent #8's generic transport module. All five complete mathematical files, their necessary definitions/bridges, scoped registry, generators, development attempts, receipts, raw audits and compressed evidence were inspected. No deleted or modified existing source, workflow, protection or security setting occurs in the delta.

The public theorem `two_step_overlap_iff` is exactly `FullDomain r p u v → (TwoStepOverlap r p u v ↔ p ≤ 4)`. Its domain is `r ≥ 1`, `1 ≤ p ≤ 9`, `5 ≤ u ≤ 8`, `5 ≤ v ≤ 6`, `u+v ≤ 13`: seven cores. It compares the actual second `iterPairs` component and whole states at their actual widths. `finiteWord` discards the component's irrelevant infinite tail before `shiftOne`; this matters because the inherited `extended` function returns its terminal carry everywhere after the old width.

For `p=5..9`, exact carry certificates prove first-step widths `2r+6` and `2r+7`, then second-step widths `2r+7` and `2r+8`. The normalization and pairing bridges include both endpoints and `r=1`, including the adjacent carry boundaries. The signed difference is whole minus component overlap, with values `(1,0,-1,-1,0,1)` at `r+1..r+6` and zero elsewhere in the valid whole prefix. Index `r+1` witnesses failure. The lower branch uses the inherited exact return plus a proved zero tail, rather than silently extending prefix equality to functions.

The raw redundant comparison has central coefficient `4v ≥ 20`, is explicitly proved non-Admissible, and is never given an invented ordinary realization. Its terminal carry and interior carry 2 are separately certified. Agent #8's unchanged transport theorem requires the actual common binary terminal carry and normalized old-width antisymmetry, which the concrete application proves.

`numeric_two_step_defect` and `numeric_two_step_overlap_fails` retain arbitrary caller-supplied `n,d`, original `Canonical` and initial-column premises; they propagate that same `n` through `orbit n 2`. `Canonical` includes positive width, bounded digits, a nonzero leading digit and the exact numeral value. `upper_initial_realizable` and `realized_overflow_defect` additionally provide a positive initial realization for every upper-domain tuple. The output digit function is existential and only its finite canonical prefix is asserted. This does not state an elevenfold relation between independently selected ordinary integers, palindrome safety, a different-component obstruction, later-return classification, infinite avoidance, or a result for 196.

## Retained execution and independent reconciliation

Fresh Lean execution in this session is **NOT_RUN**. The previously reported launcher failure and rejected escalation were respected; no retry or alternate execution route was attempted. The reused executor is **Agent #100 `scope_audit`**, identified by the original receipt as a nonauthor of these five modules, in the same original session/account. The canonical verifier's embedded Agent #1 label is not executor evidence.

The inspected unchanged verifier creates a nonexistent output directory, writes the exact 18-module closure under `independent01/groupii-overflow/source`, uses that directory as `LEAN_PATH`, and builds in dependency order. Its sanitized environment selects the official runtime and newly produced local objects. It does not copy author `.olean` files. Every actual module command is `lean -j1 -DElab.async=false -o Module.olean Module.lean`; the nineteenth is `ProjectAudit.lean` with the same two flags. All 19 exit codes are 0 and every complete raw log matches its receipt hash. These commands omitted `--trust=0`; the compiler default is `max`.

Independent byte checks compare all 18 exact-H source files with their fresh archived build snapshots, registry SHA-256 and Git blobs, report build hashes, and complete publication commit `686cac2696e4e4e059c1b9d6a313f5519f6f4176`. Actual imports give exactly the registered closure rooted at `Agent100GroupIIOverflowNumeric`. The run HEAD `491b477889b6336f5386287e3665f6ce58a34d9b` did not contain all later source files; neither it nor `source_tree_clean` (which ignores untracked files) is substituted for source-byte identity. All six Agent #8 dependency blobs match source commit `8874b2ee291dc7a253b3b89fbbf0efd86812ae4d`.

An independently written complete-list parser reconciles all **2,576** raw module-origin theorem rows, the strict repeated audit, both published ledgers, and all **52** explicit public `#print axioms` outputs. The union is exactly `propext`, `Classical.choice`, `Quot.sound`. Fifty-one new endpoints use the first and third; only `two_step_overlap_iff` additionally uses `Classical.choice`. Both inherited corrected endpoints contain all three. The **14** unsafe implementation entries occur separately, not in any audited theorem's collected axiom dependencies. The source closure has no prohibited tokens or local metaprogramming bypass machinery. Counts include generated theorems and are audit metadata.

The separate original command `lean --trust=0 -j1 -DElab.async=false ProjectAudit.lean` exited 0 after **57.486 seconds**, against the same fresh source/objects. Its source hashes, full audit rows and retained log reconcile. It was an actual second audit command, not another source build. Its imported-proof checking interpretation requires the correction below.

The new `verification/reproduce.py` was inspected and parsed, not executed end to end. Its original static-only label is correct. No execution of it is claimed here.

## Required evidence correction

The published phrase that the strict command “typechecked all imported modules” is stronger than the actual Lean 4.19.0 import implementation supports. Exact official source commit is `6caaee842e9495688c1567e78c0e68dbb96942aa`; all nine inspected files were fetched both at this full commit and `v4.19.0` and found byte-identical. The exact files, blobs, byte counts and SHA-256 values are in `lean419-source-provenance.json`.

The relevant control flow is:

- `src/util/shell.cpp:488,585–588,755` selects/parses the trust value and passes it to the frontend. Its help text at 210–211 contains the stronger historical claim and is not implementation evidence.
- `src/Lean/Elab/Frontend.lean:154`, `src/Lean/Language/Lean.lean:462–463`, and `src/Lean/Elab/Import.lean:20–27` pass the value through to `importModules`.
- `src/Lean/Environment.lean:1890–1899` calls `finalizeImport`; at 1809–1844 it directly assembles imported constant maps and stores `trustLevel` in the environment header. This path does not replay imported declarations through `Kernel.check` or `addDeclCore`.
- `src/kernel/type_checker.cpp:91–112` checks a referenced constant's universes/safety and returns its instantiated type; it does not recursively validate its stored proof body.
- The actual `ProjectAudit.lean` uses `#check` for the 52 names and `Lean.collectAxioms` for selected `.thmInfo` declarations. It contains no proof-body kernel replay.

This does **not** invalidate the original fresh source build. `src/Lean/Environment.lean:69–72` defaults `debug.skipKernelTC` to false; `src/Lean/AddDecl.lean:13–22,48–55` selects normal declaration checking and the synchronous path used by `-DElab.async=false`; `Environment.lean:606–616` dispatches to checked declaration addition; `src/kernel/environment.cpp:192–209,275–281` checks theorem proof terms and equality to the declared proposition. These paths are not disabled by the default command-line trust value. The exact source compilation argv and absence of skip/bypass options and source constructs support the original fresh-build result.

Required minimal remedy: preserve original source, logs, receipts and archives verbatim; add an authoritative English erratum saying that the explicit-flag run repeated the full module-origin axiom audit over the existing fresh objects, and did not independently replay every imported proof through the kernel. Retain acceptance based on the exact-source fresh closure compilation plus complete axiom audit. Do not fabricate a second build or introduce a new mandatory checker run.

`affected-trust0-labels.json` enumerates all 14 overstrong occurrences at H across `README.md`, `PUBLICATION.json`, `controls/README.md`, `controls/overflow-semantic-review.md/.json`, `verification/README.md`, `verification/run_strict_import_audit.py`, and `verification/strict01/AMENDMENT.md` and `strict-import-verification.json`. The correction should explicitly govern archived copies and historical status strings, without replacing those original bytes. The future strict launcher inherits the historical wording; it must not be cited as proof-body replay.

## Preservation and policy

Both complete archives were decompressed and every member checked, not merely listed:

| Archive | Stored SHA-256 | Members | Result |
| --- | --- | ---: | --- |
| `independent01-complete-evidence.tar.xz` | `b371c559c185f1cf28e621633a0c87a04b5e9d193801839f16255fa8fccd0e5a` | 52 | Compressed hash, decoded tar hash, member names, bytes and SHA-256 all agree |
| `strict01-evidence-amendment.tar.xz` | `a29f0ebcb127606f47120528c0612e6360d88cd0ab7d0140fff105d051f3d690` | 11 | Same complete validation |

Historical document copies differing from current documents are preserved as historical versions; they are not silently asserted equal. `archive-recovery-map.json` pins every member to its exact published archive commit/path/blob/bytes/SHA-256, plus member identity. The direct-file recovery map covers all changed files and necessary dependencies.

The 420-case scout's compressed payload, both archived ownership records and helper pin verify. All 420 retained ordinary trajectories and pair differences reconcile arithmetically; the experiment generator was not rerun and this is finite diagnostic evidence only. Forty-three development files preserve failed bridge/arithmetic attempts, successful later snapshots, the initial root-directory dependency failure and correction, an explicitly unexecuted candidate, and the disclosed missing historical carry-stage command. The failed bridge's `sorryAx` output remains outside the accepted closure and is not promoted to a proof. Original environment startup probes are distinguished from mathematical failures.

`AGENTS.md` and `proofs/PUBLICATION_POLICY.md` at H require source preservation, exact evidence labels and lossless recovery. This package satisfies preservation; the single remaining labeling error has the concrete additive remedy above. The scoped build registry deliberately leaves the incomplete global catalogue unchanged. Reuse does not claim repository-wide PASS or compliance with an unseen platform gate.

## Reproduction and handoff

Executed Python checks and full outputs are retained: `extract.py`, `bulk_read.py`, `prepare_audit.py`, `validate_evidence.py`, `supplemental_checks.py`, `finalize_maps.py`, their `.out` files, `commands.jsonl`, archive and development reports, and operational-failure notes. They perform static reads, decompression, hashing, log reconciliation and finite retained-row checks; none launches Lean.

Canonical manifest: `proofs/contributions/agent-100/groupII-overflow-sharpness-20261016/verification/registry.json` (SHA-256 `ac68e397f5a12326ed7a788a0e021edda22be46216bcc98c5bc45f71933c6533`). Sources for the integration combination are `projects.groupii-overflow.modules`, with `path`, `sha256`, `git_blob`, and `imports`; root is `Agent100GroupIIOverflowNumeric`. The integration writer should freeze the corrected head, retain these same 18 source identities, verify current-main combination and applicable platform gates, then obtain exact corrected-head review. No additional mathematical source repair is indicated.
