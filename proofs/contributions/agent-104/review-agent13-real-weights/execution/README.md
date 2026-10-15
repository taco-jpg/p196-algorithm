# Independent hosted execution controls

Status: **READY; the independent real-weight build and audit have not yet run.** The author run `38688269514` is prior author evidence, not this review's execution. A hosted run must return its own complete raw artifact before any independent mathematical acceptance is recorded.

`check.py` rebuilds the six local modules `LychrelDigitSums`, `Family`, `TargetSafety`, `Counting`, `Weights`, and `SqrtBound` from the exact committed bytes at `122367d4935f0b4cd9e0bee19e4121ec66b3164b`. `source-pins.json` independently fixes their SHA256 values and lengths. The original author checker is retained as provenance only; it is not executed by this review.

The exact-type harness is fixed to the separately published semantic checkpoint `ab6768ef000358b5f81c6807db674dc7515819c9` and SHA256 `79ff0637667b95ff4b411a6c9ce57880c325769b39fb44285de9fa4e2563200c`. Its bytes must also match the current review commit. All 15 source exports and all 15 explicit type witnesses are required in the compiled theorem inventory. Human-readable elaborated types and raw Lean expression types are retained for all 15 original exports.

The checker enumerates every compiled theorem constant owned by all six local modules plus the harness, including private and generated constants. Each receives exactly one actual transitive `#print axioms` report. Only `propext`, `Classical.choice`, and `Quot.sound` are accepted. Safe custom axioms are rejected. Compiler-generated unsafe implementation axioms are listed separately and must not occur in any accepted theorem's transitive dependencies. The official collector source is retained and compared with the pinned compiler archive. The six sources and the harness are scanned for proof escapes and native-evaluation shortcuts before compilation.

The compiler is the direct official Lean 4.19.0 binary, commit `6caaee842e94`, SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The archive SHA256 is `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`. The checker independently compares the installed compiler, shared libraries, standard objects, and axiom-collector source with that archive. Hosted execution uses no compatibility shim or inherited dynamic-library override.

Mathlib commit `c44e0c8ee63ca166450922a373c7409c5d26b00b` and manifest SHA256 `5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752` are mandatory. Every package commit must agree with that exact manifest. The official compiled Mathlib dependency cache is explicitly reused; a Mathlib source rebuild is not claimed. All available dependency objects are pinned before local compilation. Lean itself reports the actual imported object paths, which are checked against those pins afterward. Every imported cached Mathlib/package module must have a byte-checked source at its pinned Git commit; missing source provenance fails closed.

The workflow `.github/workflows/agent104-real-weights-review.yml` runs only on pushes to `research/agent-104/20261015-real-weights-review` changing the workflow, checker, source pins, or exact-type harness. Publishing logs, reports, or README updates does not trigger another build. It has only `contents: read`; it supplies no credentials, persists no authentication, performs no writeback, and uses the existing SHA-pinned artifact uploader. It retains complete success and failure logs. The runner uses one compiler worker with `-j1 -DElab.async=false`; the hosted job has a 45-minute ceiling.

The uploaded artifact includes original sources, the initially empty fresh project with every new local object, audit/type harnesses, review controls, full raw logs, and source/compiler/dependency/object pins. Full external toolchain and Mathlib installations are excluded as reproducible infrastructure, with exact provenance retained. `artifact-inventory.json` inventories the checker output; `hosted-artifact-inventory.json` additionally inventories setup logs, even when infrastructure fails before the checker starts. Any eventual repository publication may exclude these reproducible binary objects only with an explicit inventory and reason, preserving all substantive raw logs.

Local `validation/` files verify Python and shell syntax, the compiled-environment collector and actual-path plumbing (including a private theorem), raw expression output, and the archive-comparison implementation. They use small synthetic fixtures and the already retained official compiler. They are **infrastructure smoke evidence only**, not a rebuild of the real-weight contribution. The full Mathlib-dependent execution remains pending.

Canonical invocation after exact source and dependency checkout:

```bash
python3 proofs/contributions/agent-104/review-agent13-real-weights/execution/check.py \
  --repo /path/to/exact-review-checkout \
  --lean /path/to/lean-4.19.0-linux/bin/lean \
  --lean-archive /path/to/lean-4.19.0-linux.tar.zst \
  --mathlib /path/to/pinned-mathlib \
  --out /new/empty/output
```
