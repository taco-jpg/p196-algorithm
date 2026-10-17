# ReturnClock scoped registry preflight

The exact source registry is prepared by `prepare.py` once the author's
canonical `proofs/Agent1PeriodicReturnClock.lean` exists. The preflight reads
actual imports, visits only their transitive project dependencies, verifies
all inherited source hashes and Git blob IDs, and collects public theorem
names from the actual new source. It executes no Lean and changes neither
the accepted global registry nor mathematical sources.

The accepted claim was independently read through the GitHub contents API at
commit `7f1b9680b99484e550322945ae7be029fb5a200e`. The retained `claim.json`
has Git blob `3f6b679892ba36a60ba537f9642e927e8665b1b8`; `claim-read.json`
records the actual command and exit 0. Its intended files include the single
new root, its scoped registry, and this contribution directory.

The actual dependency baseline is
`8f9249c855418eaadf9bb68bd645948d15777b5b`. The existing OuterCatalog and
WidthLift registries have 25 identical overlapping module pins. Traversing
their declared Outer and WidthPath roots yields 20 dependency modules; every
used dependency's current source SHA-256 and Git blob ID agrees with its pin.
`inherited-source-preflight.json` preserves that preliminary check. The final
registry will independently parse the actual imports and include the new
root, rather than assuming the expected count of 21.

From `/workspace/p196-agent1-clock-20261016`, after source materialization:

```
python3 proofs/contributions/agent-1/periodic-return-clock-20261016/registry-preflight/prepare.py run-001
```

Every run uses a new directory and preserves its script, source, registry,
and report snapshots. The default mode labels the output provisional. After
an actual frozen-author confirmation and inspection of its strict compile
and complete new-module axiom-audit receipts, a new run may use
`--author-checked`; the corresponding `author-confirmation.json` binds the
source hash and every inspected receipt hash. That mode still records the
combined fresh build and independent review as pending.

The source scanner masks nested comments and strings, then checks the entire
actual import closure for `sorry`, `admit`, `sorryAx`, `native_decide`,
`axiom`, `implemented_by`, `extern`, `unsafe`, `ofReduceBool`, and
`trustCompiler`. This limited textual check is distinct from executing Lean
and auditing the transitive theorem axioms. No new publication commit is
assumed before the root writer publishes it.
