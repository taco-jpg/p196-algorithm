# Agent #102 verification ledger

## Checked source identity

The exact published mathematical source is commit
`cba5dc441289bbed383972aa522a45c473879396`. Its seven module files and dedicated
registry were compared byte for byte with `git show` before the final replay.
The subsequent evidence publication changes no mathematical source file.

The official compiler is Lean 4.19.0, commit `6caaee842e94`. Runtime recovery,
download identity and a portable author replay script are in `runtime-author/`.

## Executed gates

| Gate | Actual result | Evidence |
| --- | --- | --- |
| Root clean seven-module build | Seven exits 0 with `--trust=0 -j1 -DElab.async=false` | `development/root/attempt-006/receipt.json` |
| Every explicit theorem, literal `#print axioms` | 98 of 98 reports checked; only standard three axioms | `audit/LiteralAudit.lean`, `audit/LiteralAudit.log`, `audit/summary-seven.json` |
| Unchanged repository verifier on exact committed source | PASS; source commit `cba5dc44`; `source_tree_clean=true`; all eight commands exit 0 | `author/exact-source-cba5dc44-002/verification.json` |
| Complete module-origin transitive axiom audit | 227 theorem constants, including generated declarations; only standard three axioms | Same replay's `ProjectAudit.lean` and full log |
| Independent five-module core rebuild and source review | PASS; 75 explicit theorems and 106 explicit declarations audited with `--trust=0` | `independent-lean/core-five/` |
| Independent exact endpoint coverage review | PASS; three general coverage/digit/bounds checks and 11 closed controls | `independent-lean/endpoints/` |
| Independent Boundary review | PASS; 55 literal closure theorems and 144 module-origin theorems checked with `--trust=0` | `independent-lean/boundary/` |
| Independent Decision review | PASS; six-module clean `--trust=0` rebuild, 11 new literal theorems, 200 origin theorems | `independent-lean/decision/` |
| Decision computation dependency check and huge-coefficient controls | No expanded word or cutoff evaluation dependency; six `H=10^100` kernel certificates, all axiom-free | Decision review's dependency and example source/logs |
| Separate mathematical interpretation review and Python controls | PASS at the exact saved source hashes; Python is finite evidence only | `independent-semantic/` |

The allowed and actually observed axiom union is
`{propext, Classical.choice, Quot.sound}`. No accepted theorem depends on
`sorryAx`, `Lean.ofReduceBool`, a new axiom, or a compiler-trusted proof oracle.
No `native_decide` is used in the accepted source closure. The origin audit also
records five compiler-generated unsafe List implementation specializations;
they are not presented as mathematical axioms or as theorem proofs.

## Attribution and audit scope

`RunDefs`, `RunEndpoints`, `AffineRuns` and `AffineDecision` were written by the
root Agent #102. `AffineArithmetic` and `AffineBoundary` were written by the
real `lean_runtime` subagent; `RunWord` was written by the real `word_intervals`
subagent. Review files explicitly distinguish review of another author's module
from a reviewer's own dependency. All use the same connected GitHub account;
there is no claim of external peer review or a separately authenticated reviewer.

The original project verifier has a historical hard-coded `agent: Agent #1`
metadata field. Its output is retained unchanged; the actual operator of the
replays in this package is Agent #102. The verifier does not itself pass
`--trust=0`; separate direct and independent builds above do. Its endpoint-name
grammar accepts 96 of the 98 explicit theorem names. The two names containing
`?` remain in every full literal audit and the complete origin audit.

`repository_wide_pass=false` and `catalogue_complete=false` are deliberate:
these gates accept this selected source closure, not the entire P196 repository.
Integration into the shared accepted build is reserved to the serialized owner.

## Preserved unsuccessful attempts

Development attempts and their exact failed sources remain in `development/`
and `runtime-author/`. Failed elaborations can print recovery-generated
`sorryAx`; those outputs are explicitly failed attempts, outside the accepted
source closure. The source statements were not weakened to repair them.

The first seven-module replay directory was named `exact-source-cba5dc44`, but
its preceding ordinary partial-clone reset could not fetch a missing public
blob, leaving local HEAD at `a3329eda`. Its report correctly records that older
HEAD and `source_tree_clean=false`; it is retained as a source-hash-pinned PASS,
not an exact-commit PASS. The authorized Git alignment succeeded, after which
the separate `exact-source-cba5dc44-002` run verified the actual commit. See the
first directory's `RUN_CONTEXT.md` for the full distinction.

A premature literal-audit launch was stopped by its seven-receipt precondition
before Lean ran; the old 75-line log was consequently rejected by the new
98-theorem consistency check. That execution-order failure is retained in
`development/root/attempt-006/literal-preflight-001.md`. Only the later successful
98-line audit is listed as PASS above.

Compiled caches and external runtime binaries are reproducible outputs and are
excluded. Original source, substantive logs, source pins, repairs and review
records are retained. The new all-parameter decision task uses a separate branch
and is outside the mathematical scope of this frozen PR93 package.
