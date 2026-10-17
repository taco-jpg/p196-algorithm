# Untouched-source backward-layer compiler replication: FAIL

Agent1 specialist `/root/research_status` performed this genuine independent
compiler replication. I authored none of the 17 mathematical source modules.
This is a separate same-session specialist using the shared account, not an
external peer-review identity. Agent105/session9df76b owns all source fixes and
the unfinished general backward-layer proofs. Agent1 root is sole Git writer
and issue61 relay.

The accepted bounded claim is `52c51e2d64b75f306d706e5fb65b5d39c6f73994`.
The immutable target is source commit
`59091760af8afa25c65561a35701e3963cd1f934`, specifically
`proofs/Agent105BackwardLayers9df76b.lean`, blob
`b72f13fc7235a71bb2328e368ea370f9e9795f32`, SHA256
`b0bd66964e5bc06b685af6fad9daa89bec1076f2894f6070d1c389151cf03b7e`.
The source was not edited before or after compilation.

## Actual first-gate result

One new empty directory was used. All **16 dependency modules** compiled with
exit 0. The new seventeenth module failed with exit 1, without timeout or a
target `.olean`. This is the requested 15-module predecessor package,
including its separate control root, plus TemplateStep, plus the new scaffold.
The minimal target import closure would have 16 modules; the requested extra
control was included deliberately.

The complete first gate took 51.465 seconds; the target command took 0.157
seconds. Each command used the official Lean 4.19.0 release `6caaee842e94`,
explicit `--trust=0`, `-j1`, `-DElab.async=false`, compiler-default stack, an
8 GiB address-space limit and a 600-second timeout. No project objects were
reused. Exact argv, working directory, LEAN_PATH, timing, exit code and
stdout/stderr are retained per module in `fresh-001/`.

The original complete target diagnostic is:

```text
Agent105BackwardLayers9df76b.lean:59:42: error: unsolved goals
Y n : Nat
⊢ n ∈ Nat.rec (if Y = 0 then [] else [Y]) (fun x xs => List.flatMap preimagesNat xs) 0 ↔ 0 < n ∧ n = Y
Agent105BackwardLayers9df76b.lean:64:30: error: unsolved goals
Y : Nat
⊢ (Nat.rec (if Y = 0 then [] else [Y]) (fun x xs => List.flatMap preimagesNat xs) 0).Nodup
'Agent105BackwardLayers9df76b.backwardLayer_zero_spec' depends on axioms: [sorryAx]
'Agent105BackwardLayers9df76b.backwardLayer_zero_nodup' depends on axioms: [sorryAx]
'Agent105BackwardLayers9df76b.preimagesNat_zero' depends on axioms: [propext]
```

The two `sorryAx` prints are elaborator error placeholders in a **failed**
module, not accepted proofs. The third printed axiom set does not turn the
module into a successful verified artifact. The whole-origin/public audit was
not run, and no accepted new-root theorem count or permitted-axiom verdict is
claimed. This diagnostic is not a mathematical refutation of the two base
statements.

No source repair or altered-source trial was attempted. The requested second
fresh build was conditional on first-gate success, so it was **not run**.
Agent105 must provide a corrected immutable source head for any new execution.
This evidence concerns the exact scaffold at 59091760, not the separate PR165
failure and not the unfinished all-depth layer theorem.

## Preserved source meaning

The three public theorem declarations are the zero-depth membership iff,
zero-depth duplicate freedom, and `preimagesNat 0 = []`. The eight source
definitions include four Prop-valued specification predicates; defining those
predicates does not prove their properties. The missing canonical-digit
adapter, arbitrary-target one-step membership, positive-depth membership and
Nodup, and empty-layer persistence remain Agent105's stated obligations.

The scaffold uses Agent109's computed digits and Agent101's finite digit
function, then the existing complete predecessor decoder. Its specifications
name the original Lychrel196 step/orbit. This source-level interpretation is
not substituted for the failed compilation.

## Evidence and exact reproduction

`source-pins.json` records all 17 paths, Git blobs, SHA256 values and imports.
`closure.json` gives both the minimal and requested topological orders.
`original-predecessor-registry.json` is the unchanged 15-module registry.
`fresh-001/compiled-sources/` contains the exact complete compiler inputs under
their logical module names. Those bytes matched the published commit, their
Git blobs and their registry/scout hashes. The original TemplateStep aliases
share a blob; the author-selected `8873883b39064515` path was used. No import
rewrite or replacement mathematical source was needed.

The executed driver and scanner/template/input manifests are snapshotted in
`fresh-001/`. `AuditTemplate.lean.txt` is retained as **unexecuted** audit setup;
it is not an audit result. Compiler outputs remain outside this package.

To reproduce from a checkout containing the exact source commit, choose new,
nonexistent directories and use the preserved driver:

```sh
python3 proofs/contributions/agent-1/backward-layers-verification-20261017/replay.py \
  --source-root /absolute/path/to/checkout \
  --build-dir /absolute/path/to/new-build \
  --evidence-dir /absolute/path/to/new-evidence \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean
```

The driver verifies all source bytes against the exact Git commit, requires
the pinned official compiler hash, masks nested comments/strings for the
auxiliary forbidden-token scan, and refuses preexisting output directories.
Both commands and failure text are preserved without modification.
`final-receipt.json` binds current source bytes, the executed driver, the log,
the absent target object and the actual result. `FILES.json` indexes all
retained source/text evidence except itself. The two original author requests
and accepted claim are included verbatim.
