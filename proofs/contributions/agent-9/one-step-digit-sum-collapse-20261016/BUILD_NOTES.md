# Author build and replay

The packet's `verify.py` is an attributed local adaptation of the stronger
no-overflow horizon verifier. Its original path, hash, and exact adaptations
are recorded in `PROVENANCE.json`. The mathematical input registry is
`verification/source-registry.json`.

The complete original import closure is:

1. `LychrelDigitSums`
2. `IncomingCarrySensitivity`
3. `RawSymmetryObstruction`
4. `IntrinsicSeam`
5. `SeamAnnihilation`

The sixth source module is `Agent9OneStepDigitSumCollapse`. The generated
`CollapseAudit` is a checking module, not an additional mathematical dependency.
All five original sources are copied byte-for-byte to the fresh build source
tree, with hashes and original Git commit/path/blob identities verified before
compilation. Original build-source copies are omitted from archived development
attempts because their exact references are retained. The original-source
provenance command outputs are retained as logs, preserving every actual command
output, including those commands' original source bytes.

The author uses the official Lean 4.19.0 release, commit `6caaee842e94`, at
`/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean`. The compiler executable and the
runtime root object/shared-library files selected by the checker are hashed.
Standard runtime modules are imported from that release; their entire source
closure is not rebuilt. Project dependencies and the new module are rebuilt
from source with `--trust=0 -j1 -DElab.async=false` in a fresh output tree.

Replay command (use a new output directory):

```sh
python3 -B proofs/contributions/agent-9/one-step-digit-sum-collapse-20261016/verify.py \
  --repo /workspace/scratch/8dcaf4a67fa4/p196-agent9 \
  --package-root /workspace/scratch/8dcaf4a67fa4/p196-agent9/proofs/contributions/agent-9/one-step-digit-sum-collapse-20261016 \
  --manifest /workspace/scratch/8dcaf4a67fa4/p196-agent9/proofs/contributions/agent-9/one-step-digit-sum-collapse-20261016/verification/source-registry.json \
  --lean /tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean \
  --output /workspace/scratch/8dcaf4a67fa4/agent9-collapse-author/replay-new \
  --auditor 'Your actual name and review role'
```

The audit prints the types and literal `#print axioms` reports for every new
export. Independently of the export list, it enumerates every theorem and safe
definition/opaque constant by its actual originating project module, including
private/generated declarations, and collects its transitive axioms. Only
`propext`, `Classical.choice`, and `Quot.sound` are allowed. It also rejects custom
safe axioms and banned proof shortcuts, checks the exact import closure, and
checks that source inputs and selected runtime files did not change during the
run. This is a selected-source-closure gate, not a repository-wide theorem check.

Every actual author compiler attempt, successful or failed, is preserved under
`development/`, with the attempted new sources, exact registry and workflow,
commands, logs, and status. Reproducible `.olean` binaries are excluded from the
retained packet. A final packet manifest covers the retained evidence while
leaving root-owned rolling metadata to root's own final publication manifest.
