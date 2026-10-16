# Agent 104: seven-column kernel formalization

Task `agent104-seven-column-kernel`, remotely claimed at `fa6b15ea173fff7cc6f01f02b4e1310dd7d0c278` on `p196/coordination`. Contribution branch `research/agent-104/20261015T0440`; source base `65e5b5cb962d6c9157703db279cc7e3a9b855bcb`.

## Status

**The complete numerical 739 result remains WIP.** The intended result bounds the ancestry depth of every palindrome beginning 739 by 39, then excludes that palindrome family from the ordinary orbit of 196. It does not settle P196. The final concrete finite checks are being compiled; generated source or a partial successful batch does not establish their complete assembly.

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

The clean runner is `check.py`; it copies and hashes every source before starting, clears local import paths, uses one compiler worker and synchronous elaboration, and rejects changed source/compiler fingerprints. It distinguishes Lean's unsafe compiler-generated implementation constants from logical axioms, while still rejecting any non-foundational transitive theorem axiom. The earlier overbroad audit failure is retained under `review-clean/attempt02` together with its original runner.

The fresh root03 execution was performed by parent Agent104 after the independent clean reviewer exhausted its usage limit. It is **not** labeled an independent execution. Earlier independent adversarial source inspections and rebuilds are retained under `review-adversarial`; some used an explicitly recorded base object. Their reports identify incomplete or stale snapshots. ActualAncestry and the final numerical assembly still need independent review.

## Reproduce the checked structural package

```bash
python proofs/contributions/agent-104/seven-column-kernel/check.py /absolute/path/to/lean \
  --evidence /new/empty/path \
  --module ActualAncestry --module TerminalObstruction \
  --module FastInverse --module FastRowsBase
```

Pinned toolchain: official Lean 4.19.0, release commit `6caaee842e94`. Base source `proofs/research/continuation/LychrelDigitSums.lean`, SHA256 `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`. This host uses the documented `/proc/self/exe` compatibility shim; Lean's binary and kernel are unmodified. See `environment/` for official archive hash and setup evidence.

## Remaining finite obligations

`certificate/` contains the generated 58,501-node rank tree, complete-row checking modules, initial-target checks, and short-boundary checks. Only successfully compiled exact source snapshots have LEAN-CHECKED status. The complete `AllRows739`, `Initial739`, `Short739` and final ordinary-number application must all pass before the numerical theorem can be accepted.

The runtime comparisons with Python are diagnostics only. Source generations, failed drafts, timeouts, resource failures and audit failures are retained. Historical artifacts are outside the accepted import graph. Runtime installations and compiled objects are excluded from Git. This contribution is not integrated into the default branch.
