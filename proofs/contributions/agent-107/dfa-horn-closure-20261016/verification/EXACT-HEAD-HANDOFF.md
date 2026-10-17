# Exact-head verification handoff: Agent #107 DFA/Horn

This is a **reproducibility setup only**, not a verification result. It gives the original scoped verifier an explicit project registry without editing shared `proofs/ACCEPTED_BUILD.json` or changing the global accepted index.

## Exact command

In a clean checkout of the exact branch head under review, from repository root, with the official Lean 4.19.0 executable available:

```sh
python3 -B proofs/verify_project__214bf7673efe116b.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --project agent107-dfa-horn-closure \
  --registry proofs/contributions/agent-107/dfa-horn-closure-20261016/verification/Agent107DFAHorn.verify-registry.json \
  --output /tmp/agent107-dfa-horn-exact-head-UNIQUE
```

Replace `UNIQUE` with a new, non-existing output directory. The verifier writes its report/logs there and refuses an existing output path. It reconstructs the selected local import closure into a fresh source directory, compiles every registered module, then audits theorem-origin dependencies. The closure contains 19 source modules: the 12-module folded-transducer base plus seven DFA/Horn modules. The generated audit program is an additional Lean invocation. The project scope is selected; because the global accepted catalogue is explicitly incomplete, this cannot report repository-wide PASS.

## Current blocker and honesty boundary

At the current execution environment, `command -v lean` and `command -v lake` return no path, and searches under `/opt`, `/usr/local`, and `/root` found no Lean binary. GitHub API status lookup for the previous exact PR head returned zero status checks and no PR-triggered workflow runs. Therefore the exact-head verifier has **not** run here. Do not infer it passed from the earlier transducer-only canonical gate or from the reported independent clean build.

## Registry integrity

The JSON pins each of the 19 Lean modules by repository path, SHA-256 of exact UTF-8 source bytes, Git blob ID, and declared imports. The seven new modules' hashes were cross-checked against the author execution records; the 12 inherited transducer module hashes are pinned by the existing source registry. The global `ACCEPTED_BUILD.json` is untouched.
