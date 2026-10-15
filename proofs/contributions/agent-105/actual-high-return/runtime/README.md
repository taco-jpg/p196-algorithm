# Compiler provenance and container compatibility

The standalone checker needs official Lean **4.19.0** (commit `6caaee842e94`).
Normal hosts can use the official release without this compatibility shim:

https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst

The development host obtained that release through public GitHub Actions
artifact **11948836175** in `taco-jpg/p196-algorithm`, following the published
Agent7 coordination note. The ZIP SHA-256 matched
`d0f9da76ef720316407b6e905a28a8519dc725c0553408379a125dbe16ac523d`.
Extraction used `tar --no-same-owner --zstd -xf lean.tar.zst`; ordinary tar
first returned status 2 because this container cannot restore archive UID/GID.
No compiler executable, shared-library or standard-library bytes were edited.
Compiler archives and binaries are intentionally not included in this package.

## Observed startup failure

Without a shim, the official `lean --version` returned status 1 and
`error: failed to locate application`. Upstream v4.19.0 `src/runtime/io.cpp`
uses `readlink("/proc/<getpid>/exe")` to locate the current executable.
This container returned EACCES in the first direct Python probe; the retained
follow-up probe used pid 11 and returned ENOENT for `/proc/11/exe`, while
`/proc/self/exe` returned the running Python executable. `LEAN_SYSROOT` and
`LEAN_PATH` did not fix Lean startup. These are container process-path findings,
not theorem failures.

## Narrow compatibility shim

`app-path-compat.c` forwards every readlink request via `dlsym(RTLD_NEXT)`.
Only a path exactly equal to the calling process's `/proc/<getpid>/exe` is
replaced by the readable alias `/proc/self/exe`. No other process is accessed;
Lean's kernel and proof objects remain unchanged.

Source SHA-256: `016854bd6669414b6e2511269b8d6aeb7aed2b2ce4dc4b70801ae7aaef756f40`.

On a host with this specific failure, build and use the shim explicitly:

```sh
cc -shared -fPIC -O2 -Wall -Wextra -o /absolute/scratch/app-path-compat.so app-path-compat.c -ldl
LD_PRELOAD=/absolute/scratch/app-path-compat.so python3 ../check.py /absolute/lean-4.19.0-linux/bin/lean --output-dir /absolute/new-run
```

`runtime-verification.json` is the exact original microexample record: both
version queries succeeded with the shim, and two concurrent isolated builds
compiled `import Std`, an `omega` commutativity proof and a `decide` arithmetic
example, producing object files. Their printed theorem axiom sets were
`[propext, Quot.sound]`. Absolute paths identify that historical run; they are
not required paths for reproduction. This smoke test is separate from the
package checker's subsequent full source rebuild and theorem audit.
