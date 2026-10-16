# Full fresh canonical verification of actual uniform safe returns

**PASS: 20 source modules, 106 new public theorem endpoints, and 1,551 theorems
checked by their defining module.** The original repository verifier rebuilt
the complete selected closure from an empty external directory. All 20 source
compilations and the exhaustive ProjectAudit exited 0.

The root is `Agent105UniformReturn`. Its exact theorem, quantifiers, actual
output indexing, retained assumptions, and dependency reasoning are reviewed
in `SEMANTIC_REVIEW.md`. The actual mathematical authors of all nine Agent105
modules are recorded in `source-pins.json`. In particular, ReturnTimeBound was
authored by `/root/lean_runtime`; the reviewer `/root/ownership_audit` authored
TailSelection and does not claim an independent author review of that component.

## Build and proof checks

The registry is `proofs/Agent105UniformReturn.registry.json`, exact snapshot
SHA-256 `6bee312ba098872841df7416f6b2c77dc39a83325145556e761401a87d9c562c`.
The root source SHA-256 is
`fba98eb095ca439835e82a90315254090ed03935c3d17d9e6ae8ebe5bb7b7fa7`.
The selected project is `agent105-uniform-safe-return`.

The unchanged canonical verifier has SHA-256
`c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`.
Its execution used official Lean 4.19.0, commit `6caaee842e94`, Release, and its
original `-j1 -DElab.async=false` compiler flags. This full canonical stage did
not add `--trust=0`. Individual author and independent component checks that
used that flag retain their own exact commands.

The full theorem-axiom union is exactly
`[Classical.choice, Quot.sound, propext]`. All private/generated theorem
declarations in each selected module are included. The original verifier also
reports 21 unsafe compiler implementation specializations separately; none
appears in a checked theorem's axiom closure. Those entries are retained in the
original report and raw audit log. Forbidden source proof primitives, safe
custom axioms, and disallowed theorem-axiom dependencies were checked by the
unchanged canonical gates.

The complete build took approximately 128.86 seconds. The retained original
`LychrelDigitSums` dependency was genuinely rebuilt in approximately 77.20
seconds. This successful stage did not use the prior author dependency cache.

## Earlier failed check

`failed-normalize-only-attempt-001/` retains an earlier separate canonical
attempt, including its original FAIL report, source snapshots, raw logs and
file inventory. PeriodObstructions, ActualWordBridge and PrefixSemantics
compiled successfully; LychrelDigitSums was terminated with signal 9 after
approximately 129.68 seconds and produced no compiler diagnostic. That attempt
did not reach the new Normalize source and is not counted as a successful
verification of it.

The associated resource snapshot records an 8 GiB cgroup limit and concurrent
memory pressure. It does not establish a per-process cause for the signal.
After resource coordination, the complete 20-module run recorded here succeeded
without changing any source, compiler argument, or acceptance rule. Other
author attempts remain in their respective contribution directories.

## Source identity and retained evidence

`canonical-attempt-001/` preserves the original `verification.json`, original
`FILES.json`, 20 byte-identical source snapshots, generated ProjectAudit, and
all 21 raw compiler/audit logs. All 43 entries of the copied original inventory
were verified after copying. Runtime binaries and `.olean` files are excluded
from the retained contribution tree.

`provenance/` contains independently retrieved exact sources for the Agent1
repeated-block dependency and all five Agent102 dependencies. Their UTF-8 bytes
were compared directly with the pinned local sources and Git blob identities.
The remaining retained original sources use the current SOURCE_MAP entries.

The canonical report records local HEAD
`33474b2b08e445509475aa6cf341a1a8e12977db` and `source_tree_clean: false`.
Per-file membership in that HEAD is recorded in `source-pins.json`; the successful
build certifies the pinned source vector, not the presence of every new source
in that earlier commit. The original script's `agent: Agent #1` field is fixed
inherited metadata. This run's actual executor is `/root/ownership_audit`,
session `agent105-8f1107db019a`, as recorded in the companion receipt.

## Replay

From the repository root, choose a previously nonexistent output path:

```sh
python3 -B proofs/verify_project__214bf7673efe116b.py --lean /tmp/p196-agent105-toolchain/lean-4.19.0-linux/bin/lean --project agent105-uniform-safe-return --registry proofs/Agent105UniformReturn.registry.json --output /tmp/p196-agent105-uniform-safe-return-replay-NEW
```

The separately registered final plain/integer extension is verified in
`../uniform-integer-return/`. It reuses only the exact artifacts of this
successful fresh build, compiles its six additional modules, and audits the
entire final 26-module closure. The first six-module supporting registry and
this 20-module registry remain distinct, exact snapshots.
