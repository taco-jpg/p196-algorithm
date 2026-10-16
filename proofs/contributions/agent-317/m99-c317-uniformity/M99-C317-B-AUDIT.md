# Agent #317 — M99-C317-B fixed-ensemble audit

Audit basis: current main evidence at commit 9de08d78db6526e2ce2dd66cedd5e63f600424bd, plus the open M99-A07 contribution PR #58.

## Finding

No accepted result inspected here supplies the fixed finite ensemble required by the uniformity extraction theorem.

The current evidence does establish several nearby facts:

1. The finite-horizon density result gives increasingly many seeds surviving a horizon as width grows, but its stated limitation is that it does not yield a fixed infinite-safe seed.

2. The explicit family C_D = 2 * (10^(2D+1) - 1) is safe through time D for every D. This is a family indexed by the horizon parameter D; it therefore does not instantiate the fixed-ensemble premise. The repository explicitly records that no D satisfying the universal finite-delay bound has been supplied.

3. The archived/current research record also contains an infinite family of finite seeds safe through time 10000 (for r >= 5078, with the smallest certified member having 10163 digits). This is still only a fixed finite-time guarantee. The family is infinite in the seed parameter, not one fixed finite candidate ensemble with guarantees for every horizon.

4. The exact finite-kernel result says every finite safe kernel is nonempty while no fixed finite pair word belongs to all kernels. This is directly consistent with the quantifier boundary: nonemptiness of each finite-horizon kernel is weaker than a common member across all horizons.

## Quantifier diagnosis

The desired extraction has the form:

exists fixed finite K, forall N, exists x in K, forall t <= N, Safe(x,t)
implies
exists x in K, forall t, Safe(x,t).

What the existing finite-horizon constructions provide is instead of the form:

forall N, exists x_N in K_N, forall t <= N, Safe(x_N,t),

where K_N may change with N. The C_D family makes this dependence especially explicit because the candidate itself is indexed by D.

Therefore it would be incorrect to combine the existing finite-horizon family results and silently conclude an all-time seed. A missing theorem must establish a horizon-independent finite candidate set (or another genuine compactness/finite-state mechanism with a separately proved realizability bridge).

## Consequence for P196

This audit does not prove or disprove existence of a Lychrel seed and does not affect the specific status of 196. It identifies the exact missing uniformity premise needed for the finite-ensemble route.

## Evidence

- proofs/FINDINGS.md at 9de08d78db6526e2ce2dd66cedd5e63f600424bd
- PR #58, Agent #17 M99-A07, head b1cee0df38a410cce8462db56266860a4e7ec0be
- Existing finite-delay/safe-ancestry and C_D records cited by FINDINGS.md
- Explicit finite-time safe family record cited by proofs/README__a9cde297f7bac39f.md

Status: SOURCE_AUDITED. No Lean execution is claimed for this audit.
