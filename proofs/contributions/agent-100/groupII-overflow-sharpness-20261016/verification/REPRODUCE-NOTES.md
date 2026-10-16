# Future reproduction with explicit trust-zero import checking

`reproduce.py` is an additive future execution path. The historical canonical
19 commands did not specify `--trust=0`; the official Lean help reports a default
trust level of `max`. Those original commands, reports, attribution labels and
the `b371c559...` evidence archive remain unchanged. A separately recorded strict
import check supplements an original run; it does not retroactively change its
command line.

From any clone of this source, run the new entry point with an official Lean
4.19.0 Linux binary and a **nonexistent** output directory:

```sh
python proofs/contributions/agent-100/groupII-overflow-sharpness-20261016/verification/reproduce.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/new-reproduction \
  --executor 'Name or identifier of the actual reproduction operator'
```

The launcher discovers the repository root from its own location, invokes the
unchanged canonical verifier from that root, and verifies the exact registry,
verifier, extractor and official compiler hashes before creating its output.
It never reuses previous project oleans. The frozen registry identifies the
18-module scoped closure and retains its incomplete global-catalogue warning.

After a canonical PASS, the launcher runs the additional argument list
`[lean, '--trust=0', '-j1', '-DElab.async=false', 'ProjectAudit.lean']` in that
fresh build's `canonical/groupii-overflow/source` directory. `LEAN_PATH` points
only to this fresh project source directory, while the compiler supplies its
standard library. The separate `ProjectAudit-trust0.log` and operator receipt
retain the actual argv, cwd, exit status, log hash and source/compiler/olean
snapshots. The complete strict module-origin ledger must agree with the
canonical multiline ledger, including complete axiom sets, final theorem
count and the separately reported unsafe implementation inventory.

`canonical/verification.json` remains the original verifier's report, including
its embedded Agent #1 label. The unchanged extractor writes
`canonical-multiline-ledger.raw.json`, which retains its embedded historical
`scope_audit` executor string. **Neither embedded label identifies the person
running a future reproduction.** Only `reproduction-operator-receipt.json`
records the supplied current `--executor`; its default is explicitly
`local reproduction operator`. This is self-reported attribution and never
asserts independent review merely from a label. Raw reports are not rewritten.

All process commands use subprocess argument lists, without shell execution.
A failed canonical build stops before the strict audit; later failures retain
their logs and a failed operator receipt. Existing output directories are
rejected so that earlier attempts cannot be overwritten.

This launcher was checked here by Python AST parsing, `--help`, and pure command
construction assertions only. No new full Lean build or successful future
reproduction is claimed by that static check. The original `replay.py`,
`extract_axiom_ledger.py`, registry, verifier and historical archive were checked
byte-for-byte unchanged after this addition.
