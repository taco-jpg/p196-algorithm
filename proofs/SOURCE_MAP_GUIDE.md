# Resolving historical paths and replaying the original layout

Use [SOURCE_MAP.json](SOURCE_MAP.json) to locate the exact retained source
behind an old repository path. Use [replay_original_layout.py](replay_original_layout.py)
when a checker needs its original directory structure and relative dependencies.

This guide describes the source-map and wrapper bytes at
[`ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3`][snapshot].
The map's original-layout baseline is
`2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.
Its **9,161 mapped paths** are one baseline's recovery coverage, not a count of
theorems or a census of every later contribution. Newer packages retain their
own source pins, registries, commands, and verification records.

## Identify the document's layout first

| Surface | Interpretation at this snapshot |
|---|---|
| [Current research entry point](README.md) and [status](STATUS.md) | Navigation and explicitly scoped status; read each named checkpoint's date and source commit. |
| [FINDINGS.md](FINDINGS.md), [REPORTS.md](REPORTS.md), and [REPRODUCE.md](REPRODUCE.md) | Exact original-layout documents selected by the map. Their historical nested paths may be absent from the migrated checkout. |
| [RESULTS.md](RESULTS.md) | The migration's source classification, with its stated review limitations. |
| A later contribution's own registry and verification directory | Evidence for that contribution's stated source closure, independently of membership in the original-layout map. |

The three historical documents above remain hash-pinned. A broken current
relative link does not imply that its original source was deleted or that its
mathematical claim was withdrawn. Resolve the original path before drawing
either conclusion. The current guide does not replace their historical evidence
or expand the scope of a recorded proof check.

## Read a source-map entry

Keys in `mapping["paths"]` are **repository-root-relative original paths**.
For a link in an old document, first resolve it relative to that document's
original directory. For example, `research/README.md` in the original
`proofs/FINDINGS.md` refers to the key `proofs/research/README.md`.

The [pinned map][map] and [actual wrapper][wrapper] use these fields:

| Field | Meaning for recovery |
|---|---|
| `base` | Commit used for the reconstructed repository's branch and index. |
| `current` | Preferred local source path when non-null. |
| `preserved` | Historical source path selected when `current` is null or otherwise false. |
| `sha256` | Required hash of the original bytes. |
| `mode` | Git mode; `120000` means a symbolic link, whose link-text bytes are hashed. |
| `oid` | Recorded Git object ID, distinct from the SHA-256 content hash. |
| `english_current`, `english_sha256` | Optional language-only presentation metadata; the replay wrapper does not select these fields. |

The selection rule is exactly `entry.get("current") or entry["preserved"]`.
The wrapper checks the selected bytes against `sha256` and stops on a mismatch.
It does **not** try `preserved` after a non-null `current` fails its hash check.

For example, the historical `proofs/REPRODUCE.md` entry selects the current
path of that same name. The historical `proofs/README.md` entry has
`current: null`, so replay selects its preserved original even though an
English presentation is also recorded. These are different recovery cases.

## Resolve and check one path without reconstructing the tree

Run this read-only example from the repository root. It needs Python 3 and
the map plus the selected file on disk. Change the first argument to another
original path to inspect that entry.

```sh
python3 - proofs/REPRODUCE.md <<'PY'
import hashlib
import json
import os
import sys
from pathlib import Path

mapping = json.loads(Path("proofs/SOURCE_MAP.json").read_text(encoding="utf-8"))
original = sys.argv[1]
entry = mapping["paths"][original]
selected = entry.get("current") or entry["preserved"]
path = Path(selected)
data = os.fsencode(os.readlink(path)) if entry["mode"] == "120000" else path.read_bytes()
actual = hashlib.sha256(data).hexdigest()
print("baseline:", mapping["base"])
print("original:", original)
print("selected:", selected)
print("sha256:", actual)
if actual != entry["sha256"]:
    raise SystemExit("Selected bytes do not match the historical source map")
print("source hash: MATCH")
PY
```

At the pinned snapshot, the selected path is `proofs/REPRODUCE.md` and the
hash is `aefd7f4ffaabb81f9799c18156d43af763679ebcf85216472b05e6bb67d02e4a`.
The command above was executed for this document and that output was confirmed.
This checks **one source's bytes**; it does not check the entire map or execute
a mathematical checker. See the [bounded validation record][validation].

A missing map key can mean that a path belongs to a later contribution or a
different retained source tree. Consult its own provenance; do not invent an
original-layout mapping or infer a failed mathematical result.

## Reconstruct before running an original-layout command

The wrapper first creates an external temporary shared Git clone, sets its
branch and index to `mapping["base"]`, reconstructs **every mapped path**,
checks the selected source hashes, and then launches the requested command.
The child process starts at the reconstructed **repository root**, regardless
of the directory assumed by an old command example. The wrapper retains the
temporary workspace and propagates the child's exit status.

Before using it, provide:

- Git and Python, a real Git checkout, and the map's baseline commit object.
- Every source selected by the map, including required preserved paths.
  A sparse checkout containing only one checker is insufficient.
- Enough temporary storage for the full mapped layout, plus the selected
  checker's outputs. Even a request for one small check reconstructs the
  complete mapped layout first.
- The chosen checker's own dependencies, toolchain version, and input files.
  A Lean command still requires its documented compiler and project inputs.

A source ZIP alone lacks the Git metadata used here. A shallow clone is
sufficient only if it also contains the required baseline object. The following
read-only preflight checks that object, not the availability of all mapped files:

```sh
git cat-file -e '2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5^{commit}'
```

To inspect a historical document directly from Git without reconstruction:

```sh
git show '2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5:proofs/REPRODUCE.md'
```

Both Git commands were executed in the documentation checkout. Their success
does not imply that a complete original-layout replay has run.

### Existing wrapper entry points

From the current repository root, the [release wrapper][release-wrapper] already
selects the historical release checker:

```sh
python3 -B proofs/verify_release.py
```

The [project wrapper][project-wrapper] forwards its arguments to the historical
project checker. For the explicitly scoped project shown in the current README:

```sh
python3 -B proofs/verify_project.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --project consolidation-core --output /absolute/new/output/directory
```

These two wrapper commands are **COMMAND_INSPECTED** here, not newly executed
project checks. Their results concern the reconstructed original-layout scope.
A byte-release check does not prove mathematics, and a scoped Lean result does
not establish repository-wide verification.

### Commands whose instructions start in a subdirectory

Put the directory change **inside** the child command. For example, the
historical release check written as `python3 -B verify_release.py` from
`proofs/` can be expressed from the current repository root as:

```sh
python3 -B proofs/replay_original_layout.py -- sh -c \
  'cd proofs && python3 -B verify_release.py'
```

This example is **COMMAND_INSPECTED**. It illustrates the actual working-directory
contract; no full reconstruction or release replay was executed for this guide.
Use the original command's prerequisites and evidence boundaries for other
subdirectories. Running a flattened script directly can select the wrong
relative inputs or outputs even when its own source bytes match.

## Diagnose a recovery problem without changing the evidence

| Observation | Check next |
|---|---|
| The lookup key is absent | The original document's directory, normalized original path, and contribution-specific provenance. |
| A selected file is missing | Checkout completeness and the entry's exact selected path. |
| The wrapper reports changed source bytes | Compare the selected file with the pinned original; an archive copy alone does not change the selection rule. |
| The baseline Git object is unavailable | Obtain the required history before retrying; copying text files does not supply that object. |
| Temporary storage is exhausted | Provide enough temporary capacity for the complete mapped layout before launching another replay. |
| Reconstruction succeeds but the child fails | Preserve its command, outputs, exit status, toolchain, and scoped failure; restoration success is not checker success. |

Before editing a file selected by a historical `current` entry, coordinate the
preservation and mapping implications with its owner. Keeping old bytes in an
additional archive does not automatically redirect replay to them. The existing
publication and source-mapping process must keep the original bytes recoverable
and the selected historical hashes valid. Do not hand-adjust generated
inventories merely to make a changed source appear verified.

## Verification boundary of this guide

The [validation record][validation] distinguishes executed source lookups and
Git-object checks from inspected wrapper commands. No new Lean compilation,
finite-certificate replay, complete original-layout recovery, whole-repository
preservation audit, or proof-status upgrade is asserted here. The existing map,
wrappers, historical documents, manifests, and mathematical sources are unchanged.

[snapshot]: https://github.com/taco-jpg/p196-algorithm/commit/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3
[map]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/SOURCE_MAP.json
[wrapper]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/replay_original_layout.py
[release-wrapper]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/verify_release.py
[project-wrapper]: https://github.com/taco-jpg/p196-algorithm/blob/ee508d3ecf07b7e4a6ca9b2272fc72e997cb59a3/proofs/verify_project.py
[validation]: contributions/agent-65/source-map-guide-20261016/VALIDATION.md
