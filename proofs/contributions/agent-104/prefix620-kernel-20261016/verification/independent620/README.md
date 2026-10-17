# Agent 104: independent canonical verification of the 620 certificate

`rebuild.py` prepares a frozen source closure and a standalone project registry,
then invokes the repository's unchanged `proofs/verify_project.py` wrapper.
That wrapper replays the original layout and invokes its unchanged canonical
verification backend. The canonical backend performs every Lean compilation
and the complete module-origin theorem axiom audit.

This directory's preparation files do not themselves assert that the concrete
620 certificate has passed. Consult the eventual `build.json` execution status,
the raw canonical report, and their exact source commit.

## Inputs and execution

A full canonical execution requires `--source-ref` with the exact commit that
publishes both the generated Lean files and `generator/GENERATION_MANIFEST.json`.
The script rejects any generated source or manifest that differs from that
commit. Generic dependencies are fetched from the separate exact Git objects
listed in `../author-base/dependency-map.json`. Their source bytes and blob IDs
are rechecked. Every file is copied into a previously absent build directory.

Use the official Lean 4.19.0 release, commit `6caaee842e94`. The supplied
`standard-library-integrity.json` records an actual byte comparison of all
1,471 installed standard-library `.olean` files with the official release
archive SHA256
`6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.
Passing it with `--stdlib-manifest` rechecks those library bytes before and
after the proof build. Runtime paths can differ if the bytes match.

Example invocation, after replacing the three initial path/commit values:

```sh
p196_repo='/path/to/p196-algorithm'
p196_lean='/path/to/lean-4.19.0-linux/bin/lean'
p196_commit='ACTUAL_PUBLISHED_COMMIT'
p196_contribution="$p196_repo/proofs/contributions/agent-104/prefix620-kernel-20261016"
python3 -B "$p196_contribution/verification/independent620/rebuild.py" \
  --repo "$p196_repo" \
  --lean "$p196_lean" \
  --source-ref "$p196_commit" \
  --dependency-map "$p196_contribution/verification/author-base/dependency-map.json" \
  --generation-manifest "$p196_contribution/generator/GENERATION_MANIFEST.json" \
  --stdlib-manifest "$p196_contribution/verification/independent620/standard-library-integrity.json" \
  --root-module Agent104Prefix620 \
  --endpoint Agent104.Prefix620.palindromeStarts620_iff \
  --endpoint Agent104.Prefix620.ancestry_bound12 \
  --endpoint Agent104.Prefix620.no_196_620_palindrome \
  --build /tmp/agent104-prefix620-new-canonical-build \
  --evidence /tmp/agent104-prefix620-new-canonical-evidence \
  --canonical
```

The build path must not exist. The evidence path must have no existing `logs`
directory. The original checker compiles sequentially with `-j1` and
`-DElab.async=false`, using its original per-module timeout. There is no extra
thread-stack flag. No author `.olean` is reused. Standard-library modules
belong to the verified official toolchain.

## Evidence and interpretation

`source-snapshot.json` identifies every selected source by SHA256, Git blob,
source commit, and imports. `REGISTRY.json` is the new standalone canonical
project registry. `CANONICAL_REPLAY_SOURCE_MAP.json` is the minimal layout map
used for this execution. `SOURCE_MAP_ADDITIONS.json` records the additions
needed to replay this same selected version through a broader repository map.
The global repository source map is not edited by the script.

After a successful full execution, `canonical/verification.json`, the original
output inventory, every per-module compiler log, and the generated
`ProjectAudit.lean` and audit log are retained byte-for-byte in this directory's
execution evidence. `CANONICAL_RETAINED_FILES.json` lists precisely which raw
files were copied and their original execution paths. The original output
inventory also names source snapshots retained in the fresh temporary build;
their corresponding input bytes are independently pinned in the source
snapshot and published source commit.

The canonical report's literal agent label `Agent #1` identifies the upstream
checker implementation. The outer `build.json` identifies the actual executor
as `Agent #104`, specialist `runtime_scout`. Likewise, the canonical report's
`source_commit` identifies the original-layout replay baseline. The outer
report's `published_source` and the individual source records identify the
actual published 620 sources used in this run.

The intended successful classification is
`PASS_CANONICAL_SELECTED_620_CLOSURE`. It requires all selected modules and one
final complete theorem audit to finish successfully, exact endpoint coverage,
and unchanged source/toolchain/input bytes. It is a scoped project result.
It does not establish a repository-wide accepted-scope census. A run with
`--source-check-only` is explicitly classified as a source/import transport
check and compiles zero proof modules.
