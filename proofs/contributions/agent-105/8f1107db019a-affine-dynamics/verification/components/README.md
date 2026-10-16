# Scoped canonical verification: supporting affine-dynamics interfaces

**PASS for `agent105-affine-components`: six modules, three roots, and all 40 new
public theorem endpoints.** This first registry is limited to supporting
interfaces. Its `catalogue_complete` field is false, and its recorded
`repository_wide_pass` is false.

Executor: Agent #105, session `agent105-8f1107db019a`, verification subagent
`/root/ownership_audit`. Execution uses the repository's unchanged canonical
verifier; mathematical independent review of the time-bound file authored by
the independent subagent `/root/lean_runtime`
is recorded separately under `review/time-bound/ownership-audit/`.

## Exact scope

The three roots supply literal expanded affine-run word operations, finite-tail
predicate selection, and explicit-hypothesis return-time/width bounds for the
original Agent8 list orbit. The finite selector requires eventual equality and
safety stability plus eventual cover. The time-bound family endpoint requires
canonicality, an actual return equality, equal endpoint heads, an affine width
gain, and positive time. These are checked theorem hypotheses, not discharged
claims about every affine family.

The complete actual uniform-safe-return theorem, the fixed-time affine closure,
Agent102's eventual equality/palindrome dichotomies, and integer realizability
are outside this registry. Agent102's definitions are reused unchanged; their
ownership is retained in the source and provenance record.

| Module | Role | Public registered endpoints | All origin-matched theorems |
| --- | --- | ---: | ---: |
| PeriodObstructions | Original Agent8 dependency | 0 | 69 |
| ActualWordBridge | Original Agent8 dependency | 0 | 62 |
| Agent102RunDefs | Unchanged Agent102 definition dependency | 0 | 25 |
| Agent105AffineBasics | Root: literal word interfaces | 13 | 19 |
| Agent105TailSelection | Root: finite-tail selection | 18 | 21 |
| Agent105ReturnTimeBound | Root: actual list-return width/time bounds | 9 | 18 |
| **Total** | | **40** | **214** |

The larger right column includes generated/private theorems. It is the result of
iterating the Lean environment and matching each declaration's defining module;
the audit does not select declarations only by a public-name prefix.

## Canonical replay

The script `proofs/verify_project__214bf7673efe116b.py` was restored with
`git show HEAD:proofs/verify_project__214bf7673efe116b.py` and verified byte-equal
to that tracked original. Its SHA-256 is
`c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`.
No acceptance rule or compiler argument was changed.

The actual invocation, from the repository root, was:

```sh
python3 -B proofs/verify_project__214bf7673efe116b.py --lean /tmp/p196-agent105-toolchain/lean-4.19.0-linux/bin/lean --project agent105-affine-components --registry proofs/Agent105AffineDynamics.registry.json --output /tmp/p196-agent105-affine-components-canonical-001
```

Use another previously nonexistent output directory for a replay. The canonical
script compiles with `-j1 -DElab.async=false`; it does not pass `--trust=0`.
The separate independent time-bound review does use `--trust=0`.

All six module compilations and `ProjectAudit` exited 0. The full audit checked
214 theorems and found the exact dependency union
`[Classical.choice, Quot.sound, propext]`. Source-token scanning and theorem
dependency scanning found no forbidden proof primitives. Two unsafe compiler
implementation specializations are reported verbatim by the original checker:

- `Agent102RunDefs` / `List.flatMapTR.go._at.Agent102.word._spec_1`
- `Agent102RunDefs` / `List.mapTR.loop._at.Agent102.runsAt._spec_1`

Neither appears in the collected dependency list of a checked theorem. The
canonical report treats unsafe implementation declarations separately from
safe custom axioms and theorem dependencies; these records are retained rather
than suppressed.

## Source identity and commit status

`source-pins.json` records exact SHA-256, Git blob identity, imports, owner
provenance, and whether each registered file's bytes were present in local HEAD
at pin time. The Agent8 source map is checked against the current tracked
`proofs/SOURCE_MAP.json`. The Agent102 definition file was independently fetched
at owner commit `90b3d63e9d4a560c0a22406215497f583cc1ea5a`, then compared byte for
byte against the local dependency. Its original SHA-256 is
`1544d22e098c659f804e27faab228f4ebb13c8f9d8fc290c6d90f413286cefcf` and Git blob
is `0c2b723a8c21c953f8a51761e752a827ff72a5cc`.

An earlier transport copy of Agent102RunDefs had one extra terminal newline and
was 1791 bytes. Root corrected it to the original 1790 bytes before this
canonical execution. Earlier author attempts retain the bytes and hash actually
used in those attempts; their logs were not rewritten.

The original canonical report records source commit
`ae8bbdfd2a18e8910eebc25fd2a81661c01abc16` and `source_tree_clean: true`. That
script's cleanliness check is `git status --porcelain --untracked-files=no`.
At execution time, Agent102RunDefs and the three new Agent105 roots were
untracked, so those exact bytes were **not contained in the reported commit**.
The PASS certifies the six pinned source snapshots, not inclusion of those
snapshots in that commit. `execution-receipt.json` and `source-pins.json` preserve
this distinction. The original report's inherited `agent: Agent #1` field is
unchanged script metadata; the actual executor is identified above and in the
companion receipt.

The first checkpoint's companion receipt incorrectly called ReturnTimeBound
root-authored. The actual author is `/root/lean_runtime`; Basics was authored by
`/root`, and TailSelection by `/root/ownership_audit`. The corrected companion
receipt records the earlier value explicitly. This attribution correction does
not alter any Lean source, compiler output, axiom report, or canonical inventory.

## Retained evidence

`Agent105AffineDynamics.registry.snapshot.json` is the exact registry used.
`canonical-attempt-001/` contains the unmodified `verification.json`, original
`FILES.json`, all seven raw compiler/audit logs, all six compiled source
snapshots, and the generated `ProjectAudit.lean`. Its file inventory is verified
after copying. `provenance/Agent102RunDefs.remote.json` retains the independently
fetched owner source and immutable reference.

No prior canonical attempt failed. The build output was a fresh external
directory with no project object cache. The copied contribution evidence omits
all `.olean` files and all runtime binaries. Runtime version and executable /
shared-library hashes remain in the original report for reproducibility.
