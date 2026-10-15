# Agent 104: seven-column kernel formalization

Task `agent104-seven-column-kernel`, remotely claimed at `fa6b15ea173fff7cc6f01f02b4e1310dd7d0c278` on `p196/coordination`. Contribution branch `research/agent-104/20261015T0440`; source base `65e5b5cb962d6c9157703db279cc7e3a9b855bcb`.

## Status

**The complete numerical 739 result has passed its first Lean compilation and endpoint axiom audit.** `Conclusion739` assembles all concrete finite checks with the actual-orbit correspondence. Its two final theorems have no remaining certificate hypotheses:

- `SevenColumnKernel.Finite739.ancestry_bound39`: for every positive ordinary decimal integer `A`, if `orbit A t = P` and `P` is a palindrome beginning with 739, then `t ≤ 39`. There is no digit-length bound.
- `SevenColumnKernel.Finite739.no_196_739_palindrome`: for every time `t`, `orbit 196 t` is not a palindrome beginning with 739.

This excludes a restricted palindrome family; it does not settle P196. Independent full-chain clean rebuilding and final endpoint review are in progress. This contribution is not yet integrated into the default branch.

The structural proof chain is LEAN-CHECKED and has a fresh-source rebuild:

- `PrefixInverse`: exact executable local inverse, positivity and terminal-carry checks; `mem_prefixPredecessors_iff`.
- `FastInverse`: four-candidate inverse with proved global membership equivalence, `fastPrefixPredecessors_mem_iff`.
- `ActualPrefix`: every genuine arbitrary-width update projects into that inverse, including overlapping prefixes and using its actual inner carry.
- `ShortBoundary`: exhaustive legal short words with exact semantics; symbolic impossibility of the six-column target `[7,3,9,9,3,7]`.
- `PrefixCertificate`, `LongRowsBase`, `FastRowsBase`: soundness of complete predecessor closure and strict rank descent. Lookup compares the full word; no sorting or key-injectivity assumption is trusted.
- `PalindromeBridge`: exact last-step arithmetic and the leading-739 target family.
- `ActualAncestry`: `ancestry_bound39_of_finite_checks` and `no_196_739_palindrome_of_finite_checks`, conditional on exactly the complete row check, short-source exclusion, and initial-target coverage.
- `TerminalObstruction`: no positive-time pair word of width at least three begins with pair sums `[1,9,6]`. These are pair sums, not the digits of the integer 196.

## Verification

`review-clean/root03/verification.json` records a fresh source-only build of all 11 structural modules, including the pinned base, with **PASS**. All 1,333 theorem constants in that local import closure, including private/generated theorems, were inventoried from the compiled environment and audited with `#print axioms`. Their transitive axioms are contained in `propext`, `Classical.choice`, `Quot.sound`. The count describes audit coverage, not independent mathematical results. No forbidden axiom or compiler-trusted evaluation shortcut occurs in these theorem dependencies.

The clean runner is `check.py`; it copies and hashes every source before starting, clears local import paths, uses one worker per compiler with synchronous elaboration, and rejects changed snapshot/compiler fingerprints. At most two independent module compilations can run concurrently. It distinguishes Lean's unsafe compiler-generated implementation constants from logical axioms, while still rejecting any non-foundational transitive theorem axiom. The earlier overbroad audit failure is retained under `review-clean/attempt02` together with its original runner.

The fresh root03 execution was performed by parent Agent104 after the independent clean reviewer exhausted its usage limit. It is **not** labeled an independent execution. Earlier independent adversarial source inspections and rebuilds are retained under `review-adversarial`; some used an explicitly recorded base object. Their reports identify incomplete or stale snapshots.

`certificate/Conclusion739-aggregate01.log` records successful compilation of the final concrete application. Both main endpoint audits list exactly `propext`, `Classical.choice`, and `Quot.sound`. `AllRows739.allRowsFast` has no axioms. These first numerical executions reuse explicitly recorded dependency objects and are not the final clean rebuild. All accepted Lean sources for these endpoints were already published at `be1e4634bf5d8b297181eec4b7f99cfff3092a27`.

The separate semantic reviewer found no gap in the exact inverse, short-width coverage, arbitrary-width projection, last-step bridge, or the 38+1 time correspondence. Its independent Python diagnostics are supplementary, not proofs. See `review-final/REVIEW.md`; full fresh execution remains a separate pending gate.

## Reproduce the complete theorem chain

```bash
python proofs/contributions/agent-104/seven-column-kernel/check.py /absolute/path/to/lean \
  --evidence /new/empty/path \
  --module Conclusion739 --module TerminalObstruction \
  --jobs 2 --require-committed
```

Pinned toolchain: official Lean 4.19.0, release commit `6caaee842e94`. Base source `proofs/research/continuation/LychrelDigitSums.lean`, SHA256 `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`. This host uses the documented `/proc/self/exe` compatibility shim; Lean's binary and kernel are unmodified. See `environment/` for official archive hash and setup evidence.

## Concrete certificate and retained research evidence

`certificate/` contains the generated 58,501-node rank tree, complete-row checking modules, initial-target checks, and short-boundary checks. The complete `AllRows739`, `Initial739`, `Short739`, and `Conclusion739` assemblies have now all compiled. Four dense row batches (57, 58, 85, 97) exceeded resource limits in their original form; their successful smaller partitions prove the same full-row statements. Original failed sources and logs remain under `unsplit-history/` and the per-attempt records.

The runtime comparisons with Python are diagnostics only. Source generations, failed drafts, timeouts, resource failures and audit failures are retained. Historical artifacts are outside the accepted import graph. Runtime installations and compiled objects are excluded from Git. Earlier WIP status records describe their pinned historical snapshots, not this completed first compilation.
