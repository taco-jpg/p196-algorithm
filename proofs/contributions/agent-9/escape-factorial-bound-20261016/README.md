# Agent #9: factorial upper bound for uniform decimal escape

This contribution formalizes the closed upper bound in the retained `strengthening_notes.txt`, section 5, equation (9), then applies it to the existing ordinary-decimal escape theorem. The recursive bound 和 all arithmetic dynamics remain unchanged.

The latest author build result is recorded in `development/full-001/summary.json`; exact source snapshots 和 every compiler stdout/stderr accompany that record. Independent review 和 publication are separate steps.

## Exact generic statement

For natural `κ > 0`, a function `E : Nat → Nat`, the base value `E 1 = 1`, 和 the exact recurrence

```lean
∀ i, E (i + 2) =
  κ * ((i + 2) + (i + 1) * (2 * E (i + 1) + 1))
```

the theorem

```lean
P196.Agent9.FactorialEscape.recurrence_factorial_bound
```

proves, for every `M ≥ 1`,

```lean
E M ≤ (4 * κ) ^ (M - 1) * factorial M
```

`factorial` belongs to `P196.Agent9.FactorialEscape`. It is the ordinary natural factorial, defined by `factorial 0 = 1` 和 `factorial (m+1) = (m+1) * factorial m`. The equations 和 positivity are proved directly. A search across every shipped Lean 4.19.0 source file found no existing factorial identifier; its exact command 和 empty output are retained in `source/lookup-record.json` 和 the associated logs.

The generic theorem places no condition on `E 0`. Its conclusion is restricted to positive indices. It assumes no monotonicity of `E`, no separate growth lower bound, 和 no arithmetic-orbit hypothesis.

The proof first establishes the shifted form `E (i+1) ≤ (4*κ)^i * factorial (i+1)`. Writing its positive right side as `C`, the induction uses

```text
(i+2) + (i+1)*(2*C+1)
  ≤ (i+2)*C + (i+1)*(3*C)
  ≤ 4*(i+2)*C.
```

Multiplication by `κ`, the power recurrence, 和 the factorial recurrence give the next bound. Conversion to `M-1` occurs only after establishing that `M` is positive.

## Unconditional decimal instance

The existing `DecimalProfile.sharpEscapeBound` has `κ=5` 和 exactly the recurrence above. The theorem

```lean
P196.Agent9.FactorialEscape.sharpEscapeBound_factorial
```

therefore proves, for every natural `M`,

```lean
DecimalProfile.sharpEscapeBound M ≤ 20 ^ (M - 1) * factorial M
```

The additional `M=0` case is handled separately using the existing theorem `sharpEscapeBound_zero`. The generic theorem is never applied at zero.

At the unchanged digit-sum index `2*B`, the theorem `sharpDigitSumEscapeBound_factorial` gives

```lean
DecimalUniformEscape.sharpDigitSumEscapeBound B ≤
  20 ^ (2 * B - 1) * factorial (2 * B)
```

for every natural `B`.

## Actual ordinary-decimal time window

For every positive ordinary decimal integer `n`, threshold `B : Nat`, 和 starting time `s : Nat`,

```lean
P196.Agent9.FactorialEscape.digitSum_uniform_window_factorial
```

proves

```lean
∃ t, s ≤ t ∧ t ≤ s + 20 ^ (2 * B - 1) * factorial (2 * B) ∧
  B < DecimalMass.digitSum (Lychrel196.orbit n t)
```

It applies `DecimalUniformEscape.digitSum_uniform_window_sharp` from the unchanged `SharpUniformDecimal` module, then enlarges its upper time endpoint using the proved factorial estimate. The final theorem `digitSum_uniform_window_196_factorial` specializes the result to 196.

All natural thresholds 和 starting times are included. The time window is inclusive at both endpoints. Its horizon is the displayed expression; a count of consecutive integer times would be that horizon plus one.

At `B=0`, natural subtraction gives `2*B-1=0`, so the closed expression equals `1` because `0! = 1`. The existing exact horizon at zero is `0`. The added zero case is consequently a valid coarser bound, with no assertion that an additional step is necessary.

The orbit 和 digit sum are the original ordinary-decimal definitions. Iteration continues after a palindrome, as in the existing development. This contribution proves finite escape windows; it makes no real density-limit, pointwise convergence, palindrome-avoidance, optimal escape-time, general-base dynamics, or 196-conjecture claim.

## Provenance 和 preservation

The exact written source is:

- Original commit: `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.
- Original path: `proofs/research/continuation/strengthening_notes.txt`.
- Git blob: `7103ee939d82740b970dd23fb91e9db50db4ea54`.
- Relevant statement: section 5, equation (9).

The full source text is preserved unchanged under `source/`. `PROVENANCE.json` also records attribution for the audit/verifier patterns. `dependencies.json` identifies the same nine unchanged modules used by the existing uniform decimal theorem, including their original paths, current flattened paths, Git blobs, 和 SHA-256 hashes.

The confirmed coordination claim is `473a2865e2b3b4d7e8044b3537c9b94ba5ab18d1`, task-record blob `c1a1e77bf905abbec633f324fad99dccc3c3a2cc`, task `agent9-escape-factorial-bound-20261016`. The parent supplied `CONTRACT.json` 和 created publication branch `formalize/agent-9/escape-factorial-bound-20261016` at `ae8bbdfd2a18e8910eebc25fd2a81661c01abc16` before implementation. The delegated proof author has made no Git or remote writes.

`development/generic-001/` retains the initial proof attempt, whose arithmetic helper lacked a distributivity rewrite. Its compiler rejected an unsolved equality. Any `sorryAx` printed in that failed attempt is the compiler's error-recovery placeholder; the attempt is explicitly failed. The corrected source compiled successfully under `--trust=0` in `development/generic-002/`. No failed source or compiler output was removed or overwritten.

## Reproduction 和 audit

Use official Lean 4.19.0, release commit `6caaee842e94`. Both output directories must be absent before invocation:

```sh
python3 -B verify.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --repo-root /absolute/path/to/p196-algorithm \
  --build-dir /absolute/new/factorial-build \
  --report-dir /absolute/new/factorial-report
```

The verifier checks the compiler version 和 each dependency hash, creates an empty build directory, copies source only, then compiles the nine dependencies 和 all three new modules with `--trust=0`, one compiler worker, 和 a private `LEAN_PATH`. Exact commands, durations, source hashes, exit codes, 和 full stdout/stderr are retained.

The final audit prints the endpoint types 和 literal axiom reports for the new factorial definition 和 all ten explicitly declared new theorems. It additionally enumerates every theorem 和 safe definition/opaque declaration whose module origin is one of the nine dependencies or the two new proof modules. The audit rejects any unexpected safe project axiom, any unapproved transitive dependency, or a missing selected module origin. Unsafe compiler implementation declarations are identified separately; an unapproved axiom cannot occur in an accepted theorem or safe definition.

The only permitted transitive axioms are `propext`, `Classical.choice`, 和 `Quot.sound`. Audit counts describe the inspected source closure; they are not counts of independent discoveries.

The original full-build JSON captured only the first line of Lean's wrapped module-origin list. The underlying Lean audit had already checked every selected origin. `development/full-001/module-origins-supplement.json` preserves the complete list from the original raw log 和 records the reporting-only parser correction. The original build summary 和 verifier snapshot remain unchanged; no mathematical source changed 和 no additional kernel run was needed for that metadata correction.

`MANIFEST.sha256` covers author-owned source, documentation, provenance, 和 retained attempts, relative to this directory. A separately supplied `review/` directory is excluded 和 carries reviewer-owned manifests. Reproducible compiled objects 和 temporary build trees remain outside this publication packet.
