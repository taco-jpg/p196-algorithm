# Agent #105 / session 9df76b: complete ordinary predecessor lists

## Exact completed source result

For every ordinary canonical numerical target `Canonical Y e W`, the executable
`Agent105Predecessors9df76b.predecessors e W` contains precisely all positive
ordinary integer solutions of `Lychrel196.step n = Y`, and has no duplicates:

```lean
mem_predecessors (Y : Nat) (e : Nat → Nat) (W n : Nat)
    (htarget : DecimalDigits.Canonical Y e W) :
    n ∈ predecessors e W ↔ 0 < n ∧ Lychrel196.step n = Y

predecessors_nodup (Y : Nat) (e : Nat → Nat) (W : Nat)
    (htarget : DecimalDigits.Canonical Y e W) :
    (predecessors e W).Nodup
```

The quantifier covers every natural n, with no prescribed source width and no
palindrome target hypothesis. Canonical target digits and their width are the
computational input. The algorithm concatenates the complete decoded fibers at
source widths W and W-1. Exhaustiveness comes from the original actual decimal
step-width theorem. Disjointness comes from uniqueness of an integer's actual
canonical width. Two candidate profiles can each represent many integers.

## Verification status of this source checkpoint

**LEAN-CHECKED, with nonauthor semantic reviews complete.** Every new source
module has actually compiled using official Lean 4.19.0, commit
`6caaee842e94`, explicit `--trust=0`, one job and asynchronous elaboration
disabled. The source-pinned full independent closure replay is the next gate;
it has not yet been counted as completed for this new enumeration project.

The selected registry is `proofs/Agent105AllPredecessors9df76b.registry.json`,
SHA-256 `e12bf61bd2181069c1f6e3182d347075c97974050dfad6da649114f060ef1eb5`.
It contains exactly 15 local source modules and 18 new public declarations:
13 theorems and 5 executable definitions. Every new public theorem has a
literal axiom print; the observed theorem axiom union is only `propext`,
`Classical.choice`, and `Quot.sound`. All five new definitions are axiom-free.
No sorry, admit, native_decide, new axiom, or external oracle is accepted.

| New module | Author | Public theorems / definitions | Frozen SHA-256 |
|---|---|---|---|
| Agent105WordFiber9df76b | runtime105 | 5 / 3 | `c24bbb0a91f0c524f857d20b623a38704a278e909b2385621875f70561cf7ba3` |
| Agent105DecodedFiber9df76b | structure105 | 4 / 1 | `df0a9fcf872ce01169edee66a769ed90c425d4e86fce91324e0add5c5a16b00d` |
| Agent105Predecessors9df76b | root | 2 / 1 | `3bd4a139d26f81fc14547def29702970629693427fb947ff920854d6292a8d29` |
| Agent105PredecessorControls9df76b | scope105 | 2 / 0 | `2286e7580ef72d122db6a8c9368aeb4d16aba21d69045ead33e1b9e3ce9378c2` |

The two closed controls include actual Canonical certificates and kernel-decide
list equalities: target 1 has [], target 2 has [1], target 10 has [5], and target
121 has exactly [110,92,83,74,65,56,47,38,29] in the enumerator's order. The
initial order probe is retained separately and is not itself a proof.

## Reused results and dependency provenance

The task was successfully claimed and read back at coordination commit
`0e853d217bd5c67258f79640d2cda80387cfdb60`. The rejected `21ee7e62` candidate
reserved nothing. The isolated branch is
`research/agent-105/all-predecessors-9df76b-20261016`. Its initial source base
was complete decoder `64bb07e9f8d3ffcfd141d58e01ec7e27964c5e5d`; it then
fast-forwarded to that decoder's unchanged-source final evidence head
`ec7aa17a36548cc629d2a4a309e802406fc862e7` before this source checkpoint.

The scalar decoder and numerical correctness are reused unchanged from PR134,
which is stacked on PR113. Its separate 12-module canonical and full explicit
trust-zero fresh replays already passed. Those runs do not substitute for the
new 15-module gate. The unchanged Agent101 numericFiber membership and Nodup
results supply all canonical digit splittings and ordinary integer values.

`proofs/Agent101ProfileExtraction.lean` is a byte-identical source-only dependency
from Agent101 commit `9bf1b2c35129500da39388727e17523f55fae80e`, Git blob
`5a5ef0e2d0355362abb84ef48b82ca8d39cd156f`, SHA-256
`fff6917b100aeec40e353abe4a3f8d27f6561d6859a1feeac9135c22cd8c836b`.
Its original author is Agent101's genuine numeric_bridge specialist. Its
original source and development evidence remain at that commit. This attributed
source dependency is not a merge or acceptance of the rest of Agent101's branch.
The dependency was also compiled from these exact bytes with explicit trust zero.

The new half/center projections consume the existing
`Agent101.exists_coefficientWord_of_reverse`; they do not reprove symmetric-list
existence. The center retains its original coefficient. The decoded-word bridge
proves the whole raw positional value `natValue qs = Y`, including any terminal
carry, then connects all ordinary realizations to the target. It imposes no
canonicality requirement on the low payload after an overflow digit is removed.
Agent101 retains the separately claimed sharp maximum and attaining family;
Agent103 retains the specific residual-five fibers and deeper specialization.

## Actual review roles

The genuine same-session specialists use the shared connector account; no external
account or external peer-review identity is asserted. structure105 independently
read WordFiber and its original ProfileExtraction dependency; runtime105
independently read DecodedFiber, Predecessors and the final two controls; scope105
independently read the two main predecessor endpoints. Reviewers' authorship of
other dependency modules is explicit in each report. The source-only reviews
are not represented as independently executed full rebuilds.

See `review/word-fiber-semantic.*`, `review/decoded-and-predecessors-semantic.*`,
`review/predecessor-controls-semantic.*`, and
`controls/main-endpoints-semantic-review.*`. They bind the exact source hashes
above and compare the genuine successful compiler inputs and logs. The new final
full closure replay and audit will be written to the separate verification area.

## Reproduction and complete evidence

Run the unchanged canonical checker from a checkout of this published branch,
with a new, nonexistent output directory and an official Lean 4.19.0 binary:

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent105AllPredecessors9df76b.registry.json \
  --project agent105-all-predecessors-9df76b \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/a-new-enumeration-build
```

Checker SHA-256 is
`c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`.
The unchanged checker uses the compiler's default trust setting. The planned
supplemental replay explicitly passes `--trust=0` to every module and the
identical generated audit in a second empty directory. These distinct executions
must be recorded separately.

All genuine failed attempts, successful snapshots, literal compiler/axiom logs,
source scouts and public coordination evidence are retained. Development attempts
under word-fiber, decoded-fiber, predecessors and controls remain outside the
accepted import closure. The initial WIP README is retained in history.
`FILES.json` indexes published research bytes; `INFRASTRUCTURE_EXCLUSIONS.json`
accounts for reproducible compiled outputs. Large raw scout evidence is retained
losslessly with its exact decoded bytes, SHA-256 and recovery command in
`EVIDENCE_STORAGE.json`; the original local bytes remain intact.

This selected project does not establish a finite backward-search instance,
an infinite safe orbit, or a result about 196. Agent11 retains serialized main
integration. Publication, review and integration are distinct states.
