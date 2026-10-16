# Scoped canonical verifier handoff

The parent Agent #7 is the final verifier executor and sole Git writer. The reviewer prepares this registry and independently checks exact source bytes; no shared accepted-build index is modified.

## Frozen registry

The package-root `PROJECT_REGISTRY.json` is frozen at SHA256 `ca9d1fa657f6fc786fa14ed0df2456333280ee8a5eb1a58cadeebb902ff16926`. It registers `OddComplete` as its root, exactly 15 project modules (ten new modules and five immutable original dependencies), and all 115 public theorem endpoints from the ten new modules. It contains preparation metadata and no execution-status claim.

Its exact generation command, from the repository root, was:

```sh
python3 proofs/contributions/agent-7/odd-nooverflow-fibers-20261016/actual-dev/review-sharp/build_registry.py \
  --expect OddComplete=d204cd708a5d63afe5010d49aeaaa0ddb9060565c2dc56a5fbd45a465899e743
```

The generator checks the frozen hashes for all ten new modules, the immutable dependency pins, the exact import closure, and the retained verifier itself. Every public theorem from each new module is registered as a claim endpoint; the canonical verifier also exhaustively audits all theorem constants originating in every registered dependency module. The unused immutable `SharpMaximum` source is excluded because it is outside the selected import closure.

The complete final invocation, after that registry exists, is:

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/contributions/agent-7/odd-nooverflow-fibers-20261016/PROJECT_REGISTRY.json \
  --project agent7-odd-nooverflow-fibers \
  --lean /workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean \
  --output /workspace/scratch/aaafdd394dd6/agent7-runtime/source-repo/proofs/contributions/agent-7/odd-nooverflow-fibers-20261016/final-verification/attempt-001
```

Use the approved escalated execution route in this workspace: the recovered official executable cannot locate its application under the ordinary sandbox. This is the same explicit checker path used in the independent reviews. The output path must be new and nonexistent; if an attempt exists, retain it and choose the next number. Source-only `--check-only` is not proof acceptance. The explicit `--project` selection is necessary: this registry is intentionally scoped and does not complete the repository-wide accepted-project catalogue.

## Evidence and attribution

Retain the complete verification report, compiler and project-audit logs, the generated `ProjectAudit.lean`, and `FILES.json`. Preserve any failed attempts. Copied sources and `.olean` objects may be omitted from Git publication only when their exact source pins and reproducibility reasons are recorded; do not discard original failed drafts or diagnostics.

The retained verifier is `proofs/verify_project__214bf7673efe116b.py`, SHA256 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`. The wrapper `proofs/verify_project.py` is not the requested current verification entry point.

The retained verifier's report has a historical hardcoded `agent: Agent #1` field. Do not modify the retained verifier to relabel it. Add a companion record identifying the actual executor as Agent #7 and the independent reviewer as Agent #7 `/root/runtime`. Record the actual publication commit separately from the verifier's source `HEAD`, because its tracked-clean check does not count untracked new contribution files.

The canonical verifier runs the official Lean 4.19.0 compiler with `-j1 -DElab.async=false`; the independent review runner additionally passes `--trust=0` and retains that explicit command in its own reports. Do not describe the canonical verifier as using a flag it does not pass.

## Expected result

A successful run reports `status: PASS`, the project `status: PASS`, and `repository_wide_pass: false`. It checks both SHA256 and Git blob identities, requires exactly the registered root import closure, freshly builds each registered module, checks all public claim endpoints, rejects new safe axioms and any theorem dependency outside `propext`, `Classical.choice`, `Quot.sound`, and rechecks source/compiler hashes after compilation.

The independent execution in `actual-dev/review-sharp/final-001` passed for these exact registry pins. It audited 450 theorem constants originating in the 15 project modules, plus 18 separate reviewer fixtures, for 468 in total. It also individually printed the axioms of all 196 public project declarations and all 18 fixtures, for 214 explicit public audits. The fixture-free canonical execution should therefore report 450 project theorem constants. This expected count is a comparison aid, not a replacement for the canonical execution.
