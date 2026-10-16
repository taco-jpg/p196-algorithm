# Author checkpoint: spectral recurrence weights

## Frozen source and scope

`proofs/Agent14SpectralWeights.lean`

SHA-256: `d691d02f3170db988ac9c5529402f5c09cf83425c7188d78cd0f2a6a8f4568c8`.

The guarded parent task was published at coordination commit
`82b9e59b5efa82fa463b9084da270ef646e39aeb`, with parent
`2d189730e7c2ac8e0e2fcbd38e54ce684bc7bca8` and task blob
`07b8587f411d2e3d47ec12e62cb77e41e2656547`.

Author: genuine subagent `Agent14/coverage`, reassigned from read-only source
scouting to the weights module. The parent authors the separate coordinate
and finite-encoding proofs. This report is author verification, not an
independent review.

The original mathematical source is
`proofs/research/creative_global_spectral_notes.md` at
`2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, blob
`cb1c355fa05916a770816a4d5ef680e54079cccb`, lines 23–38.

## Exact result

The module imports `Std` and defines the original natural recurrences
`T 0=2`, `T 1=20`, `R 0=1`, `R 1=19`, each with
`u (n+2)=20*u (n+1)-u n`.

The theorems `T_recurrence_exact` and `R_recurrence_exact` prove that these
natural subtractions do not truncate:

```lean
T (n + 2) + T n = 20 * T (n + 1)
R (n + 2) + R n = 20 * R (n + 1)
```

The odd weights replace the unused `T 0` with the actual central weight:

```lean
oddWeight n = if n = 0 then 1 else T n
prefixSum f 0 = 0
prefixSum f (n + 1) = prefixSum f n + f n
```

The principal exact endpoints, for every natural `n`, are:

```lean
Agent14.Spectral.oddWeight_dominates (n : Nat) :
  18 * prefixSum oddWeight n < oddWeight n

Agent14.Spectral.R_dominates (n : Nat) :
  18 * prefixSum R n < R n
```

Additional interfaces include positive weights, monotonicity of each
recurrence, `19*T(n+1)<=T(n+2)`, `19*R n<=R(n+1)`, and
`19*oddWeight n<=oddWeight(n+1)`. Initial weight values
`T 2=398`, `R 2=379`, `oddWeight 0=1`, and `oddWeight 1=20` are checked.

## Proof correspondence

Monotonicity is inductive: if `u_n<=u_(n+1)`, then
`20*u_(n+1)-u_n>=19*u_(n+1)>=u_(n+1)`. This first establishes the exact
nontruncating recurrence and then its growth consequence.

For any positive initial weight sequence growing by at least nineteen,
strict domination follows by induction. If `18*P_n<f_n`, then
`18*(P_n+f_n)<19*f_n<=f_(n+1)`. The odd and even source sequences satisfy
the required base cases and growth inequalities. In particular, the
domination at `n=0` is preserved for both parities.

These proofs establish the original arithmetic domination statement. They
do not by themselves establish the coordinate's injectivity, the real
evaluation at `10+sqrt(99)`, or any dynamical update theorem.

## Actual execution evidence

Every Lean invocation used this executable:

`/workspace/scratch/f8aedc6d7adf/runtime-agent6/lean-4.19.0-linux/bin/lean`

and explicit flags `--trust=0 -j1 -DElab.async=false`. The parent is
separately checking the official distribution provenance. The standard
runtime was imported, not rebuilt by this subagent.

| Directory | Actual result | Scope |
|---|---|---|
| `attempt-001/` | Exit 1 | Preserved substantive failed source. `omega` treated `R(n+1+1)` and `R(n+2)` as different atoms in `R_growth`. |
| `attempt-002/` | Exit 0 | Fresh module compilation after one explicit `change` normalized the index. Source hash matches the frozen file. |
| `audit-001/` | Exit 0 | All 22 explicit theorems and all 4 explicit definitions audited by exact-name `#print axioms` using the successful author object. |

Each compile attempt retains the complete source snapshot, exact command,
UTC timestamps, exit status, and raw compiler log. The failed attempt's
automatically reported `sorryAx` dependencies reflect that failed
elaboration; the failed file is not an accepted source. The successful
source contains no omitted proof or compiler-trusted evaluation shortcut.

The complete explicit-declaration audit contains exactly 26 matching output
lines. Its observed axiom union is `{propext, Quot.sound}`. The definitions,
initial value lemmas, and several reflexive helper facts are axiom-free.
`audit-001/parsed-axioms.json` records each declaration and its exact report.
This is not an assertion that all generated internal declaration names
were independently enumerated; the parent's full origin audit remains a
separate acceptance check.

The successful compiled object has SHA-256
`55d6f4ee50cf1775e46e1d6ed7438ac8fe4cf21ffecfc9be64386f2f45814cdd`.
The audit deliberately records that it reused this author object. A genuine
nonauthor must compile the frozen source in a fresh directory for the
independent gate.

## Handoff

The mathematical file and all interfaces are frozen. No Git mutation, issue
post, PR update, or main integration was performed by this subagent. The
parent may publish this source and its preserved development evidence with
the stated attribution and actual verification level.
