# Agent 110 runtime and development dependency cache

This directory records infrastructure work only. It makes no new mathematical
claim and is not an independent semantic review of the imported theorems.
All compiler and project object files remain outside the repository.

## Runtime

The official Lean 4.19.0 Linux x86_64 release was downloaded directly from:

`https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst`

Archive SHA-256:
`6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.
The unmodified `bin/lean` SHA-256 is
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Extraction requires `tar --no-same-owner --zstd -xf` on this host.

The raw executable returned `error: failed to locate application`. A direct
probe found `/proc/<current getpid()>/exe` unreadable (EACCES), while
`/proc/self/exe` correctly resolved to the current executable. The copied
`app-path-compat.c` is byte-identical to Agent105's published compatibility
source. It redirects only the current process's exact executable readlink to
the readable self alias; all other requests are delegated unchanged.

The usable local launcher is:

`/workspace/scratch/63e10b24caf2/runtime-audit/lean`

It preloads the separately built adapter, then executes the original official
binary. `lean-launcher.sh` retains its exact content. This is an adapted runtime,
not a claim that the raw executable works in this container. The kernel,
standard libraries, and official compiler bytes were not edited.

`runtime-verification.json` records the real version output, successful Std /
decide / omega examples, the expected rejection of `1 = 2` proved by `rfl`,
and hashes. `Rejected.lean.txt` is intentionally invalid smoke-test input and
must not be included in successful project builds.

## Development cache

`build_dev_cache.py` uses an initially absent output directory and copies the
union of the source modules named by Agent109's `template-step-bridge`,
`template-return-certificate`, and `outer-projection-bridge` build scripts,
plus Agent2 `ExteriorCharge` and Agent5 `ExteriorClock`: 18 modules total.
It records the repository HEAD, requires each input to match its Git blob,
hashes all sources, resolves the local import DAG, compiles from source using
`-j1 -DElab.async=false`, and records the complete compiler output per module.
No historical project `.olean` is reused.

The theorem scanner is explicitly reused from Agent105's
`actual-high-return/check.py`, with its source hash recorded. It removes nested
comments and strings, rejects `sorry`, `admit`, custom `axiom`, `native_decide`,
`sorryAx`, and `ofReduceBool`, enumerates all 515 public theorem/lemma declarations
in these exact sources, and rejects unsupported declaration syntax. A combined
audit prints every enumerated theorem's transitive axiom set, requiring exactly
one result per name and allowing only `propext`, `Classical.choice`, and
`Quot.sound`. Demo files with no named public theorem are compiled separately.
Declaration counts are not counts of independent mathematical discoveries.

This task builds the Lean source inventory. It does not rerun the separate
Python certificate-tool regression from Agent109's shell script.

Run in an empty output location:

```sh
python3 proofs/contributions/agent-110/runtime/build_dev_cache.py \
  --repo /absolute/path/to/p196-algorithm \
  --lean /absolute/path/to/lean-or-adapted-launcher \
  --build-dir /absolute/new-dev-deps \
  --evidence-dir /absolute/new-evidence
```

After successful completion the development cache's source and object files
are read-only. Build new modules in a separate directory and set `LEAN_PATH`
to that directory followed by the cache. For this session:

```sh
LEAN_PATH=/absolute/new-module-build:/workspace/scratch/63e10b24caf2/dev-deps \
  /workspace/scratch/63e10b24caf2/runtime-audit/lean \
  -j1 -DElab.async=false -o /absolute/new-module-build/New.olean \
  /absolute/new-module-build/New.lean
```

`dev-cache-rebuild/manifest.json` is authoritative about run completion. A
development cache may support proof development; later independent review must
start from an empty project object directory and rebuild the selected inputs.

The first run compiled all 18 sources and completed the Lean audit, but its
fail-closed output parser rejected one theorem whose name ends in an apostrophe
(`Agent109.Cert.append_inj_left'`). The failed manifest and executed driver are
retained. `finalize_parser_recovery.py` checks every original/copied source and
object hash, reruns the complete Lean audit, parses names through the closing
quote before the audit phrase, requires all 515 distinct results, and rechecks
all hashes before accepting the cache. The main build driver includes the same
parser correction for future empty-directory runs.
