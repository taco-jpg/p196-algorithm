# Tail-selection author verification

Executor: Agent #105 / `/root/ownership_audit`, session `8f1107db019a`.
Claim: `agent105-8f1107db019a-affine-dynamics`, coordination `c36eb4f841bcf533ffa3d490853fbd5b287940a7`.
This packet records author execution. It is not independent review of its own source.

## Checked source and exact scope

`proofs/Agent105TailSelection.lean`
SHA-256: `6357e5bc0cb38368949f376a7e6b907dfac87ec3c93ab7b8d2114e3f75e007a6`

The source imports only Std and defines Eventually and TailStable for natural parameter predicates.
Its 18 exported theorems prove finite tail combinations and a uniform selector for positive candidate times 1 through B.
The principal endpoint `uniform_safe_return_time` retains three explicit hypotheses:
eventual stability of each return predicate, eventual stability of every relevant positive-output safety predicate, and an eventual cover by bounded positive safe returns.

No actual affine-run normalization closure, arithmetic return-time bound, ordinary integer representation, or unconditional reverse-and-add theorem is established by this file.

## Actual execution

Pinned executable:
`/tmp/p196-agent105-toolchain/lean-4.19.0-linux/bin/lean`
Lean 4.19.0, release commit `6caaee842e94`.
Executable SHA-256: `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.

1. Attempt 001: direct source compile, --trust=0 -j1 -DElab.async=false; exit 0, no diagnostics.
2. Attempt 002: attempted empty-directory rebuild rejected before elaboration because the absolute input source was outside Lean's current root directory. Exit 1 and exact diagnostic are retained. This was an invocation layout error, not a proof failure.
3. Attempt 003: copied byte-identical source and audit into another initially empty directory, set LEAN_PATH to that directory, then compiled source and audit with the same trust/thread flags. Both commands exited 0. Original/source-copy hashes matched before and after.

Every declared theorem received a literal `#print axioms` query. All 18 reports were present, with transitive union exactly `Classical.choice`, `Quot.sound`, `propext`. No excluded axiom appeared. The audit additionally prints the principal bounded-selector and safe-return endpoint types.
Raw stdout/stderr, source snapshots, exact commands, timestamps, exit codes, executable hash and source hashes are retained in the adjacent receipts.

## Mathematical implementation

The finite-list selector eliminates the head of a list only after its eventual stability yields eventual falsity; the cover then passes to the remaining list. Eventual truth instead supplies the required witness immediately. The empty-list cover is contradictory.
The bounded-time corollary uses indices j in List.range B and actual positive times j+1, retaining both endpoint inequalities. The final safety conjunction includes all positive times i<=t, including the output at the return time.

Empty lists, repeated candidates and B=0 require no additional exclusion assumptions. B=0 cannot satisfy the stated cover. The proof does not assume that a single observed successful parameter establishes a uniform tail.

## Reproduction

From an empty working directory containing exact copies of Agent105TailSelection.lean and TailSelectionAxiomAudit.lean:

```sh
LEAN_PATH="$PWD" /path/to/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o Agent105TailSelection.olean Agent105TailSelection.lean
LEAN_PATH="$PWD" /path/to/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o TailSelectionAxiomAudit.olean TailSelectionAxiomAudit.lean
```

Compiled objects and the installed runtime are reproducible infrastructure and are not included in this packet. No substantive failed proof draft exists: the first mathematical source compiled without changes.

