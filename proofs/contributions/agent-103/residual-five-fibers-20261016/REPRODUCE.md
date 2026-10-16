# Reproduce the residual-five fiber contribution

Requirements: Python **3.11+**, official Lean **4.19.0**, commit **6caaee842e94**, and a Git checkout containing this contribution. `SOURCES.json` pins every source. Each output directory below must **not already exist**.

## Complete fresh build and actual theorem audit

The repository supplied to `--repo` must contain these four immutable dependency commits. Fetch any missing commits from its existing `origin`:

```sh
git fetch --no-tags origin 913441a936a437e5f4b82d03d7e7fae32da877af
git fetch --no-tags origin 6fae6e659e5c08c59666588c71a4ed06760de85e
git fetch --no-tags origin 326645944168ad2b035a1e653b61527d79684156
git fetch --no-tags origin 05e4ac30bb35ef87446d6d12a0733625c254bb0e
```

From the repository root:

```sh
P196_FIBER_PACKAGE=proofs/contributions/agent-103/residual-five-fibers-20261016
P196_LEAN419=/absolute/path/to/lean-4.19.0-linux/bin/lean
python3 "$P196_FIBER_PACKAGE/check.py" \
  --repo . \
  --lean "$P196_LEAN419" \
  --evidence /absolute/path/to/new-fiber-replay
```

The checker restores exact `commit:path` dependency bytes, checks both Git blob and SHA-256 identities, verifies the complete original foundation body before creating the sole import-only forwarder, and copies the seven new sources unchanged. The actual import graph determines the build order. All project objects are rebuilt in the new snapshot using **`--trust=0 -j1 -DElab.async=false`**. Every theorem discovered by actual module origin, including private and generated declarations, receives a literal **`#print axioms`** query. Failures retain their evidence.

The recorded run passed **22 fresh modules** and **1,812 theorem constants: 1,701 inherited + 111 new-module constants**. The seven source files contain **63 written theorem declarations and 8 definitions**. Every theorem's transitive axioms are contained in `{propext, Classical.choice, Quot.sound}`.

The same audit separately retains **33 unsafe compiler implementation declarations: 30 inherited and 3 new helpers for rawCount, residueCount and modularFiber**. All 33 appear in `UNSAFE_IMPLEMENTATIONS.json` and the raw audit log; none appears in any audited theorem's axiom list. Preserve this ledger distinction; unsafe implementation declarations are not absent.

`verification.json` records actual command arguments, environments, exit codes, source/object hashes and all individual theorem results. `snapshot/AuditAllContributionModules.lean` and `logs/AuditAllContributionModules.log` retain the exhaustive query source and raw output. `FILES.json` indexes all non-object output; object hashes remain in `verification.json`.

## Published-path compatibility

The additive registry has the single root `ResidualFiveFilteredConclusion`, reaching all 22 registered modules. To check the published source paths, hashes and imports:

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --lean "$P196_LEAN419" \
  --output /absolute/path/to/new-fiber-registry-check \
  --registry "$P196_FIBER_PACKAGE/BUILD_REGISTRY.json" \
  --project agent103-residual-five-fibers \
  --check-only
```

The inspected verifier SHA-256 is `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`. The recorded command exited **0**, status **`SOURCE_AND_IMPORT_CHECK_ONLY`**. This checks source/import compatibility; the first command supplies the scoped complete mathematical verification. `registry-check-only-invocation.json` stores the full compatibility command, and `registry-source-evidence.json` stores the staged source identities.

See `non-author-final-review.md` and its JSON companion for the non-author semantic assessment. The contribution classifies complete local predecessor fibers and the phase-selected subset; it does not assert that a listed integer is reached by 196 or prove global orbit avoidance. Neither recorded gate claims repository-wide acceptance.
