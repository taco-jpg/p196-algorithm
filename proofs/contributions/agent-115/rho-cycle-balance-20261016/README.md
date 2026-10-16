# Agent #115 — rational high-coordinate balance for exact exterior returns

**Research status: WIP mathematical argument + independently reproducible exact finite tests. NOT LEAN-CHECKED.** No statement here proves an infinite ordinary-integer orbit or resolves 196. Do not import `development/RhoCycleTargets.lean` into the accepted build.

- Coordination task: `agent115-rho-cycle-balance-20261016`, GitHub issue #61.
- Contributor source branch: `research/agent-115/rho-cycle-balance-20261016T2130Z`, starting from Agent #6's pinned exact-coordinate PR #90 source `a075b2719c4ff1cb972b68b1d9240d8eaa8d463f`.
- Reused actual definitions: `P196.Agent7.Finite.outerNext`, Agent115's unchanged `rawSucc_values` and `successor_observation`, and Agent6's `outerIter`. In particular, this is **not** a new abstract or surrogate map.
- Complementarity: Agent #6 owns the *signed low-coordinate* `betaNum` telescope; Agent #110 owns a separate all-width period-two exterior question; Agent #5 owns digit streams. This task studies the **positive rational high-coordinate** increment under all permitted phases.

## Proposed exact one-step formula

Let `s = (c,B)` with `c` in `{2,4,6,8,10,12,14,16}`, coefficients in `0..18`, `n=length(B)`, `D=10^n`, `V=lowValue(B)` and `H=highValue(B)` (big-endian). Set

```
k = 1 if c>=10 else 0
 t = c-9k                        (1 <= t <= 8)
 u = c+floor(V/D)-10k            (u >= 0)
 R = revN(n,V)                   (reversal of n low decimal digits)
 gamma = floor((H+k)/D)          (0 or 1 under the coefficient bound)
 rho(c,B) = (9H+c)/(9D)
 psi(c,B) = (90R+9u+t)/(90D)     (>0)
```

With `(c',B') = outerNext(c,B)` and *the actual `stripSuffix` operation*, the proposed theorem is the exact rational identity

```
rho(c',B') = psi(c,B) + rho(c,B)           if gamma=0
rho(c',B') = psi(c,B) + rho(c,B)/10        if gamma=1.
```

This includes the empty exterior `B=[]`, both carry branches, all allowed phases, and every canonical word. The proof obligation is *not* discharged in Lean yet.

## Written derivation to formalize

Agent115's exact `successor_observation` says suffix stripping leaves the high rational value unchanged when expressed at the untrimmed successor's original length `n+1`. Its `rawSucc_values` gives, with `Hraw = highValue(rawSucc c B)`:

```
Hraw = 10R + u + 10(H+k) + t   when gamma=0
Hraw = 10R + u + H+k + D       when gamma=1.
```

The successor phase is `c'=2t`, hence `rho(c',B')=(9Hraw+2t)/(90D)`. For `gamma=0`, subtract `(9H+c)/(9D)` and simplify using `c=t+9k`; the difference is precisely `psi`. For `gamma=1`, subtract `(9H+c)/(90D)` and again simplify; the difference is precisely `psi`. The phase restrictions ensure `t>0` and `u>=0`, making `psi>0`. The coefficient upper bound yields `H+k<2D`, so `gamma` is genuinely a bit. These identities are an algebraic argument, **not yet a compiled Lean proof**.

## Cycle consequence and quantitative boundary

For a trajectory `s_0,...,s_P` whose every intermediate state remains in the stated phase/coefficient domain, summing the one-step identities yields

```
rho(s_P)-rho(s_0) = sum_{j<P} psi(s_j)
                      -(9/10) sum_{j<P, gamma_j=1} rho(s_j).
```

If `P>0` and `s_P=s_0`, strict positivity implies the set of indices with `gamma_j=1` is nonempty. Thus *a closed exterior cycle cannot have zero high-side carries on every edge*. This is conditional on exact closure and is neither an acyclicity theorem nor a cycle witness.

The same argument suggests a bounded-width finite-horizon consequence: since `0<rho<2` for these coefficients/phases and `psi >= 1/(90*10^W)` whenever `length(B)<=W`, a no-high-carry segment of `P` edges staying below width `W` must satisfy `P < 180*10^W`. This needs its own quantified Lean implementation and interpretation audit; no stronger universal width-independent conclusion is claimed.

## Independent finite controls

Run in this directory:

```
python3 check_rho.py
```

`check_rho.py` independently translates the original Lean `outerNext` literally into Python decimal carry loops, uses exact `fractions.Fraction`, and verifies all **51,984 canonical words** of length at most three across eight nonneutral phases, **7,000 deterministic random words** of length up to 52 (including 725 noncanonical inputs), and **8,000 successive edges** in 500 independent finite-orbit telescope checks. The actual run produced zero mismatches; full parameter counts, examples, Python version, and deterministic case-stream hash are preserved in `evidence/controls.json`. No tested finite horizon supports an infinite-time conclusion.

## Remaining Lean gates

1. Develop and compile the exact rational one-step law using unchanged Agent115 and Agent6 imports, with explicit natural subtraction, gamma≤1, positivity and suffix-padding proofs.
2. Prove the finite telescope, closed-cycle overflow implication, and optional bounded-width bound in Lean 4.19.0 without `sorry`, `native_decide`, custom axioms or unchecked evaluation.
3. Audit actual statements and transitive `#print axioms`, independently rebuild from the pinned sources, then request semantic review before status upgrade.

The unproved target declarations in `development/RhoCycleTargets.lean` are just definitions of propositions. They have not been compiled in this session and are not accepted theorems.
