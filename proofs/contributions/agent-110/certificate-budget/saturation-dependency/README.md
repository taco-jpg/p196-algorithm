# Three-column saturation dependency cache

Operator: `/root/runtime_audit`, Agent 110 runtime/audit specialist.
Scope: compilation support for development of the direct certificate extension.
This is not a new independent mathematical review, a new saturation theorem,
or a claim that any abstract prefix path has an ordinary-integer realization.

The original source dependency closure is:

1. `proofs/agent4/prefix_growth/PrefixModel.lean`
   (official `Lean.Elab.Tactic.Omega` import; no theorem declarations).
2. `proofs/agent4/prefix_growth/SaturationCertificate.lean`
   (18 kernel-decided row theorems).
3. `proofs/agent4/prefix_growth/SaturationTheorem.lean`
   (10 theorem declarations).

`build.py` copies those exact source bytes only into the initially nonexistent
`/workspace/scratch/63e10b24caf2/saturation-deps` build directory, then compiles
them in dependency order with official Lean 4.19.0 / commit `6caaee842e94`,
using `-j1 -DElab.async=false`. The known current-process readlink adapter is
explicitly recorded. No existing project `.olean` is reused. LychrelDigitSums
is outside this dependency closure and is not rebuilt.

Only this new directory appears in the project `LEAN_PATH`; inherited Lean
path/sysroot/preload overrides are cleared before the documented launcher.
All source files are checked before/after compilation, and all resulting
objects are fingerprinted. No original Lean source or binary is copied into
this contribution directory.

The scanner is explicitly reused from Agent105's `actual-high-return/check.py`
and fingerprinted. It enumerates all 28 theorem declarations and rejects
unsupported declaration syntax. Decommented source is scanned for
sorry/admit/custom axiom/native_decide/sorryAx/ofReduceBool/unsafe/implemented_by.
`SaturationDependencyAudit.lean` reissues every theorem's `#print axioms`,
requiring exactly one result for each expected name and allowing only
`propext`, `Classical.choice`, and `Quot.sound`.

`verification.json` is the authoritative completion record, with exact source
hashes, version output, complete command lines, timings, log hashes, object
hashes and all theorem axiom sets. Compiler output is retained in `logs/`.
The completed cache is read-only. Consumers must build new modules elsewhere.

Session usage after the record reports PASS:

```sh
LEAN_PATH=/absolute/new-module-build:/workspace/scratch/63e10b24caf2/dev-deps:/workspace/scratch/63e10b24caf2/saturation-deps \
  /workspace/scratch/63e10b24caf2/runtime-audit/lean \
  -j1 -DElab.async=false -o /absolute/new-module-build/New.olean \
  /absolute/new-module-build/New.lean
```

This build creates a reusable development cache. Independent review of the
new extension must separately rebuild its selected dependency closure in an
empty directory.
