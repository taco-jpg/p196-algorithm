# Independent carryfree build and axiom review

**Result: INDEPENDENT_BUILD_AND_AXIOM_PASS.**

Reviewer: genuine Agent #14 `/root/runtime`, a nonauthor specialist separate
from Agent #14/root and the coverage specialist who authored the four
mathematical modules. This review covers exact source identity, actual fresh
execution, module-origin safe declarations, public signatures and transitive
axioms. The separate semantic review is performed by `/root/spectral_semantics`.

The independent process executed once and returned exit code zero. Every
recorded Lean command returned zero. No failed independent build attempt or
retry occurred for this five-source gate. The tool-observed process result is
retained as an explicitly post-exit observation in `EXECUTION.json`.

## Exact publication and source binding

The target source checkpoint is `a883847381cd800b13e511d8ccc8909ba998866c`,
associated with [PR 149](https://github.com/taco-jpg/p196-algorithm/pull/149).
The parent reported reading all 18 published files byte for byte, including
their Git blob identities, and an additive-only diff. This specialist did not
independently fetch or check out that publication commit.

This specialist checked every frozen source below, its registered Git blob
identity and its exact imports before execution and again after the complete
audit. Source snapshots are retained. The later publication binding is in
`PUBLICATION_BINDING.json`; the original execution-time contract and reports
remain unchanged. At execution start the publication commit had not yet been
asserted in that contract.

| Module | Bytes | SHA-256 | Registered Git blob |
|---|---:|---|---|
| LychrelDigitSums | 218799 | ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57 | 8a865176625283648a8a20dd2411ed77670eb0a2 |
| Agent14CarryfreeResidues | 3717 | 7785adc325f7ae100cfcde21238f27d06a558c23d74a3fa03464ea356867ece6 | 52526e5d8c400783bbf03220fd5937bb5153eb60 |
| Agent14CarryfreeDigits | 8127 | ae394c8a19e6fc497c1cf83fdf77943abd3f0b8fd681e59006bc8f7524f4ece9 | 8b7f903a870c772d7c7e329f93931de3e4ab5fac |
| Agent14CarryfreeCoordinates | 6154 | 5c2b5b72f14b8f002719fa77b54b63aef1a2fa644dd379bdb94dec4b3dbfa519 | e06631541818a8ee8bf266193f35637a5a07bd21 |
| Agent14CarryfreeSaturation | 11243 | 2427fcac82b20afe208ae2529b1dc9436217395eef63fcceb707447b0064171a | 856d9a7b95e4b43501c0fb4b07955fc5279b8c26 |

The registry SHA-256 is
`0a8454b8dbcf7ece3c117a3bcb2f7d3cffbf562f7decdefafbb4e72fc842f53c`;
its retained bytes also compute to Git blob `cf974d5d91fb0256cc99107e2a50f80e339d50e2`.
The author source-freeze manifest SHA-256 is
`5f8a120d796e8c765830f31e52939035708c95266ca1574c26cbafec4c7f3f32`.
The mathematical scope contract SHA-256 is
`ac077f99d5c5bbf49e5e5ef8801872178f3082888f03d417279b45a280c01feb`.
Both documents were retained as snapshots and rechecked at completion.

The exact project is `agent14-carryfree-saturation`, with five modules rooted
at `Agent14CarryfreeSaturation` and 22 registered endpoints. The import closure
uses the unchanged original `LychrelDigitSums` foundation.

## Canonical metadata and minimal snapshot

The original canonical verifier was copied without any change. Its SHA-256 is
`c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`.

Its `ROOT` constant derives from its own filename, so the byte-identical copy
was executed inside `run-001/input-snapshot`, containing exact registered
source paths and unchanged registry bytes. This is a minimal source snapshot,
not a complete repository checkout.

The verifier's existing `git rev-parse HEAD` and
`git status --porcelain --untracked-files=no` calls used explicit `GIT_DIR`
and `GIT_WORK_TREE` references to the existing checkout, with
`GIT_OPTIONAL_LOCKS=0`. Its historical report therefore records that checkout's
HEAD, `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`, and its tracked-only clean
status. Those fields do not identify the minimal snapshot or certify the
publication checkpoint. The unchanged verifier's literal `Agent #1` field is
also historical; the current executor is recorded separately as Agent #14/runtime.

The canonical source path behavior, source checks, import checks, compiler
flags and Lean audit were not modified. No Git mutation, proof-source edit or
source publication was performed by this specialist.

## Two separate actual builds

| Gate | Result | Actual compiler flags | Coverage |
|---|---|---|---|
| Unchanged canonical replay | PASS | `-j1 -DElab.async=false` | Five fresh modules, 22 endpoints, all 1204 theorem constants |
| Independent fresh execution | INDEPENDENT_BUILD_AND_AXIOM_PASS | `--trust=0 -j1 -DElab.async=false` | Five fresh modules, all 1358 safe constants, 55 explicit public signatures and literal axiom reports |

The canonical verifier did **not** use `--trust=0`.

The canonical and strict builds had separate newly created output directories.
The strict source directory contained zero compiled project objects before
compilation. Both builds used exact source copies and neither used author
project objects. The strict build also did not reuse canonical project objects.
A stale object in an author development directory is outside these two fresh
build paths.

The canonical replay took 102.104186 seconds, including its audit. The original
`LychrelDigitSums` compilation took 65.759370 seconds in that run and 69.681644
seconds in the strict run. The strict `Digits`, `Coordinates` and `Saturation`
compilations took 8.599029, 1.920246 and 1.772097 seconds respectively. The
strict safe-constant audit took 45.254496 seconds; the public signature and
literal axiom checks took 1.869353 seconds.

All commands, arguments, elapsed times, process return codes, timeout limits
and complete logs are retained in `run-001/verification.json` and
`run-001/logs/`. Every strict module compilation and both strict audits used
`--trust=0 -j1 -DElab.async=false`. The unchanged canonical report and its logs
are retained under `run-001/canonical/`.

## Exhaustive declaration and axiom checks

The strict Lean audit selected declarations by their actual imported module
origin. It checked every safe theorem, definition, opaque, inductive,
constructor and recursor in the five-source closure, rejecting custom safe
axioms and any forbidden transitive axiom. This closure contains no safe
opaque constants.

| Module | Theorem constants | Safe definitions | Other safe constants |
|---|---:|---:|---:|
| LychrelDigitSums | 986 | 131 | 14 |
| Agent14CarryfreeResidues | 30 | 0 | 0 |
| Agent14CarryfreeDigits | 123 | 3 | 0 |
| Agent14CarryfreeCoordinates | 38 | 4 | 0 |
| Agent14CarryfreeSaturation | 27 | 2 | 0 |
| **Total** | **1204** | **140** | **14** |

The 14 other safe constants are four inductives, six constructors and four
recursors from the original foundation. These counts include generated
auxiliaries and are not counts of distinct mathematical claims.

The complete safe axiom union is exactly:

```text
Classical.choice
Quot.sound
propext
```

The separately retained implementation inventory has 784 unsafe and 18 partial
declarations, recorded in `run-001/implementation-inventory.json`. No disallowed
axiom appears in any audited safe declaration's transitive dependencies.

The four new source files declare **55 explicit public names: 49 theorems and
six definitions**. Every name was checked with `#check @name` and literal
`#print axioms name`, including full names, explicit arguments and universe
printing. Every public name has its expected module origin and appears in the
safe audit. Every literal public axiom set agrees with its exhaustive audit
record. All 22 registered endpoints are included.

The complete theorem-name set from the canonical module audit matches the
theorem-name set from the independent safe audit. Full public types and
literal output are in `run-001/logs/public-types-and-axioms.log`; structured
results are in `run-001/public-axioms.json` and `run-001/safe-constants.json`.

Original source bytes, both source snapshots, the source-freeze manifest,
mathematical contract, registry, approved execution contract, verification
infrastructure and runtime identities were all checked at the end.

## Accepted mathematical scope

The retained contract covers the carryfree construction for every odd
canonical width at least five and every pair of residues modulo nine and
eleven, together with the corresponding even-width construction for every
even width at least two and residue modulo nine. The endpoints connect the
actual canonical nonpalindromic ordinary input, original computed carries
through the terminal index, and a canonical palindromic successor at the same
width.

The coordinate endpoints use literal finite integer coefficient evaluation of
the actual column word. They cover the value at one and the signed half of
the value at minus one, including the width-five central collision and
negative integer half. The even-width statement adds no input
divisibility-by-eleven condition.

The registry and execution retain `repository_wide_pass: false`. The
carry-defect ideal, quotient classification, overflow family, U/S or J,
orbit persistence and any conclusion about the 196 orbit remain outside this
gate. Semantic correspondence is separately reviewed by the genuine nonauthor
semantic specialist.

## Runtime provenance

Actual version:

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
```

The actual runtime prefix is
`/workspace/scratch/f8aedc6d7adf/runtime-agent6/lean-4.19.0-linux`.
The executable SHA-256 is
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.

The unmodified official distribution was independently verified earlier in
this session against all 4617 nondirectory members of the official release
archive, with matching member bytes and links and no extra installed files.
The official archive is
`https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst`,
343842845 bytes, SHA-256
`6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.
The earlier complete provenance is in the first evidence archive, SHA-256
`62075e97ae5c8ca9084d5561d07a09b29573639c1c42233e6eb750ac655cc3e0`.

This task reused that distribution without copying, patching or downloading it
again. It rechecked version, prefix, executable and runtime shared-library
identities. Supported execution escalation was used for the verified runtime
and authorized memory-backed workspace.

## Reproduction and preservation

The executed runner SHA-256 is
`b3f21681f2f1513091c75a7300c17d86d8677d891a6d950efd53f55ac0d4091d`.
The audit helper SHA-256 is
`e07e5ef5699c7e297cba66df7b003ed150f5159e6dbadac192d6847a8d22b80e`.
Executed copies and the unchanged canonical verifier are in
`run-001/verification-infrastructure/`. The earlier preparation runner is
preserved under `development/`; `INFRASTRUCTURE_FREEZE.json` records that the
final two source pins and frozen-contract capture were added before any gate
ran. The generated Lean audit program was unchanged from preparation.

The original execution command is preserved exactly in `EXECUTION.json`.
For a new run, use the same official Lean executable and a new output
directory below the recovered independent evidence root:

```sh
python3 -B "$AGENT14_EVIDENCE_ROOT/verify_carryfree.py" \
  --contract "$AGENT14_RECOVERED_CONTRACT" \
  --lean "$AGENT14_LEAN_BIN" \
  --output "$AGENT14_EVIDENCE_ROOT/reproduction-001"
```

On another machine, adjust only location fields in a copy of the approved
execution contract to the recovered identical source and contract snapshots,
plus an available existing checkout for the canonical read-only Git metadata.
Preserve all source and document digests and the full five-module registry.
A reproduction records its own contract digest and actual metadata checkout;
source identity remains explicit.

A subsequent report-writing tool invocation was rejected by the JavaScript
parser before any filesystem command ran. `REPORT_WRITER_FAILURE.json`
preserves that artifact-preparation failure and the quoting correction. No
mathematical gate was repeated and no execution evidence was changed.

`package_evidence.py` packages all preparation and final independent evidence,
including this review, contracts, exact sources, infrastructure and logs. It
checks the execution manifest, then verifies every archive member's
uncompressed byte count and SHA-256 by streaming extraction in memory.
Compiled objects and caches are excluded and inventoried. The generated
package directory is outside its own input selection; the root manifest is
included inside the archive and the final archive descriptor remains external
to avoid a self-digest cycle.
