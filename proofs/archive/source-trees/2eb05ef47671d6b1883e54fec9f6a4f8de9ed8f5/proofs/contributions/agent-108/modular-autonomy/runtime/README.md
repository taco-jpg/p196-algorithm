# Lean 4.19.0 runtime diagnosis and compatibility adapter

The official binary fails in this execution environment because its startup code reads
`/proc/<getpid()>/exe`, while the mounted `/proc` exposes the ancestor PID namespace.
The process reports a local PID such as 6, but `/proc/self` resolves to its ancestor PID
(such as 40111), and `/proc/self/status` reports `NSpid: 40111 6`. Consequently,
`/proc/6/exe` does not denote this process and returns EACCES. `/proc/self/exe`
correctly denotes the current process and is readable.

The original official binary and libraries were not modified. The approved adapter
`proc_self_readlink.c` redirects only an exact readlink request for
`/proc/<current getpid()>/exe` to `/proc/self/exe`. Other readlink calls are delegated
unchanged. It does not replace getpid, read other proc objects, modify Lean code,
change proof terms, or alter axiom checking. All new files are confined to this directory.

## Reproducible invocation

```bash
LD_PRELOAD=/workspace/scratch/28992391bdc2/runtime-diagnostics/libproc_self_readlink.so \
  /workspace/scratch/28992391bdc2/lean-runtime/lean-4.19.0-linux/bin/lean --version

LD_PRELOAD=/workspace/scratch/28992391bdc2/runtime-diagnostics/libproc_self_readlink.so \
  /workspace/scratch/28992391bdc2/lean-runtime/lean-4.19.0-linux/bin/lean \
  /workspace/scratch/28992391bdc2/runtime-diagnostics/Smoke.lean
```

Actual output (both exit 0):

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
'runtimeSmoke' does not depend on any axioms
```

The unadapted official invocation exits 1 with `error: failed to locate application`
for both --version and Smoke.lean. With the adapter, Rejected.lean (`1 = 2` proved by
`rfl`) exits 1 with the expected tactic failure. Details, exact argv, output, and hashes
are in official-runtime-results.json and adapted-runtime-results.json.

## Rebuild adapter

```bash
cc -shared -fPIC -O2 -std=c11 -Wall -Wextra -Werror -Wl,-z,relro,-z,now \
  -o /workspace/scratch/28992391bdc2/runtime-diagnostics/libproc_self_readlink.so \
  /workspace/scratch/28992391bdc2/runtime-diagnostics/proc_self_readlink.c -ldl
```

## Trust boundary

This is the official Lean checker with an explicit, separately inspectable runtime
compatibility adapter; it is not an entirely unadapted official execution. The new
trusted component is the small readlink adapter and the compiler used to build it.
The official bin/lean, libleanshared.so, libleanshared_1.so, libInit_shared.so and
Init.olean SHA-256 values were identical before and after tests. Those values do not
assert that any particular repository theorem has been checked: this task checked
only Smoke.lean and the expected rejection in Rejected.lean.

## Official source mechanism

- https://github.com/leanprover/lean4/blob/v4.19.0/src/util/shell.cpp
  lean_main initializes search paths before it parses command-line options.
- https://github.com/leanprover/lean4/blob/v4.19.0/src/Lean/Util/Path.lean
  initSearchPathInternal uses getBuildDir, which obtains IO.appDir.
- https://github.com/leanprover/lean4/blob/v4.19.0/src/runtime/io.cpp
  lean_io_app_path constructs /proc/<getpid()>/exe on Linux and returns
  failed to locate application when readlink fails.

LEAN_SYSROOT, LEAN_PATH, working directory, absolute executable path, PATH lookup,
and direct dynamic-loader invocation did not avoid the startup failure.

## Unadapted GitHub Actions verification

lean419-official-smoke.yml is a proposed manual workflow. It downloads the fixed
Lean 4.19.0 release on a standard hosted Ubuntu runner, checks the same official
binary/library hashes, and executes --version and the exact Smoke.lean content
without LD_PRELOAD. It is stored here only for review. No workflow was installed,
committed, or triggered. To verify repository contributions, the repository owner
should add its normal checkout and proof compilation steps to the approved workflow.
