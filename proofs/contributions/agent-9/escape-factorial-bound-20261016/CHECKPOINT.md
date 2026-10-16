# Checked factorial escape checkpoint

Status: **LEAN_CHECKED; independent review 和 publication pending**.

The fresh author build began at `2026-10-16T21:35:11.648306+00:00` 和 finished at `2026-10-16T21:37:01.283978+00:00`.

Compiler:

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
```

Executable SHA-256:

```text
92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023
```

All nine unchanged local dependencies, both new mathematical modules, 和 the final audit module compiled from source with `--trust=0` into an initially absent directory. No compiled object was copied into the build. Every compiler command exited zero.

| Frozen source | SHA-256 |
|---|---|
| `Agent9FactorialRecurrence.lean` | `62ac425c0522fed1ea4cef602779018a7833ad8a12e65b34fe11c13503e471ef` |
| `Agent9DecimalFactorialEscape.lean` | `e8bfbb937aab16552e253b6c8db3581b6408de4d6a70ef64f6b046b0d1a77d28` |
| `Agent9FactorialEscapeAudit.lean` | `1e225f85fa917248953967ab09a2b1d7c96c2e3bb43e4131d9003a757386f914` |

## Exact checked meaning

`recurrence_factorial_bound` proves the source estimate for every positive natural `κ`, every function `E` with base value `E 1=1` 和 the exact stated recurrence, 和 every `M≥1`. No premise concerning `E 0` occurs.

`sharpEscapeBound_factorial` instantiates that result at `κ=5` for the existing decimal recurrence. It includes `M=0` via a separate proof using the existing zero value. `sharpDigitSumEscapeBound_factorial` then applies the unchanged mass index `2*B`.

`digitSum_uniform_window_factorial` proves that, for every `n>0` 和 all natural `B,s`, some actual time `t` satisfies

```lean
s ≤ t ∧ t ≤ s + 20 ^ (2 * B - 1) * factorial (2 * B) ∧
  B < DecimalMass.digitSum (Lychrel196.orbit n t)
```

`digitSum_uniform_window_196_factorial` specializes it to 196. The window is inclusive. At `B=0`, the closed expression equals `1`, while the exact existing horizon equals `0`; the result deliberately allows this coarser bound.

## Audit 和 retained attempts

The final module printed the exact endpoint types 和 literal axiom reports for all ten explicitly declared new theorems, plus the factorial definition. The factorial definition, zero/successor equations, 和 positivity use no axioms. The generic recurrence bounds 和 decimal horizon comparisons use only `propext` 和 `Quot.sound`. The actual decimal-window results additionally inherit `Classical.choice` from the existing orbit/escape development.

The exhaustive module-origin gate accepted **1,456 theorem declarations 和 182 safe definition/opaque declarations** from the nine unchanged dependency modules 和 the two new mathematical modules. Every selected module origin was checked. Its transitive axiom union is exactly `propext`, `Classical.choice`, 和 `Quot.sound`. These counts describe the audited closure, including generated declarations; they do not count independent new results.

The exact completed author record is `development/full-001/summary.json`, with original stdout/stderr, source snapshots, dependency metadata, 和 verifier snapshot. `module-origins-supplement.json` preserves the complete wrapped origin list; this corrects only the JSON reporting parser, while retaining the original summary. The mathematical source files remain unchanged.

The first generic proof attempt failed because its arithmetic equality lacked a distributivity rewrite. Both that source 和 its compiler output remain in `development/generic-001/`. The corrected generic module passed in `development/generic-002/`. Every compiler attempt is retained; no failed attempt is presented as a checked theorem.

## Scope

The written source is the retained `strengthening_notes.txt`, section 5, equation (9), at original commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, blob `7103ee939d82740b970dd23fb91e9db50db4ea54`. `PROVENANCE.json`, `dependencies.json`, 和 the unchanged retained source text provide the precise record.

This contribution proves a coarse closed bound 和 actual finite decimal escape windows. It makes no optimality, general-base dynamics, real density-limit, pointwise divergence, palindrome-avoidance, novelty, or 196-conjecture claim. The delegated proof author has performed no Git or remote writes.
