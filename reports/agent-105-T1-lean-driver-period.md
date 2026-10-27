# Agent 105 — T1: kernel proof of failed exterior period descent

## Result 和 scope

**LEAN-VERIFIED + COMPUTED:** this formalizes
[our paper/computed counterexample, PR #417](https://github.com/taco-jpg/p196-algorithm/pull/417)
against the unchanged `Agent120.Neutral` definitions. In base 6, four
pairwise-distinct exterior words form a return with complete carry/overflow
driver `01` repeated twice. No exterior return at any finite widths 和
with any natural trim counts realizes one copy of that driver.

The negative statement allows arbitrary per-edge center fixtures satisfying
the actual `Hyp`; it assumes no center update or center closure. Consequently
the result concerns exterior driver descent only. It does 不 supply a
compatible C cycle, base-6 Lychrel certificate, decimal result, or
unrestricted obstruction to the neutral-band route.

The unmodified repository build, stock kernel replay, 和 axiom audit all
pass. The exact verification scope 和 per-file measurements appear below.

## Explicit witness

Coefficients are least significant first; the neutral coefficient is 5.

| t | Canonical B | e | g | Maximal u |
|---:|---|---:|---:|---:|
| 0 | `[4,7,7,8,3]` | 0 | 0 | 0 |
| 1 | `[9,3,4,5,8]` | 1 | 1 | 0 |
| 2 | `[4,7,7,10,2,2]` | 0 | 0 | 2 |
| 3 | `[9,3,4,9]` | 1 | 1 | 0 |

Each raw successor equals the next cyclic row plus the displayed neutral
suffix. Four distinct words establish least exterior period four; the
nonconstant complete label word has least period two.

The same witness padded to common width six is

```
[4,7,7,8,3,5]
[9,3,4,5,8,5]
[4,7,7,10,2,2]
[9,3,4,9,5,5]
```

These four words are distinct 和 have allowed trim stream `u=g=0101`.
Thus neither common width nor retaining the entire e/g/u stream restores
the failed implication. `Witness.lean` checks the literal actual `Hyp`,
carry, overflow, raw-update, length, 和 distinctness assertions in Lean.
Centers `[10]` 和 `[0]` are separate one-edge fixtures, never asserted
to be a center cycle.

## Registered endpoints 和 proof organization

The project is `Agent105DriverPeriodDescent`, with four new modules 和
18 registered endpoints. Its main endpoint is

`Agent105.DriverPeriod.exterior_driver_period_descent_counterexample`.

It proves the conjunction of an existential four-state return with
`e=g=u=0101` 和 the negation

```lean
¬ ∃ (B0 C0 B1 C1 : List Nat) (u0 u1 : Nat),
  ExteriorEdge 6 B0 C0 B1 0 0 u0 ∧
  ExteriorEdge 6 B1 C1 B0 1 1 u1
```

Here `ExteriorEdge` retains the actual `Hyp`, `e1`, `gam`, 和
`nextB = target ++ neutral^u` equations. Therefore the negative clause
excludes a different one-lap representative as well as the displayed
orbit's one-lap return. It does 不 merely state that two particular words
differ.

### 1. The finite obstruction

`FiniteGraph.lean` defines a cut with four `Fin 2` carries 和 one
`Fin 6` delayed reverse digit. The root is `(0,0,0,1,1)`; the required
terminal for `e=g=01` is `(0,1,1,0,5)`.

The executable column generator chooses a phase-zero coefficient in
`Fin 11` 和 two inward bits, derives the other coefficient, 和 checks
the literal normalization/temporal equations. `step_of_column` proves
that every bounded literal column is included in that graph.

A fixed twelve-state set contains the terminal, omits the root, 和 is
closed under every predecessor. Ordinary kernel `decide` verifies the
closure for all `96*11*2*2=4224` generator inputs. No packed-key,
hashing, graph-exhaustion program, or external solver is trusted.
Induction on `Walk` proves `no_root_terminal` for every finite path.
The obstruction even permits zero coefficients in the first column;
physical positivity is therefore unnecessary for this negative lemma.

### 2. Actual words produce a path

`ActualBridge.lean` defines `Compatible` using actual `norm` calls on
two equal-length residual words, fixed final forward carries `(0,1)`,
reverse entry carries `(1,0)`, 和 the two literal list update equations.

The proof of `compatible_walk` removes one coefficient from each word.
`norm_cons`, `norm_append`, 和 reversal give the exact graph column;
the two residual list equations establish compatibility at the next cut.
Coefficient bounds prove the new carries are bits. When both residual
words are empty, normalization forces all four boundary carries 和 the
remaining overflow singleton forces the delayed digit to equal 5.
Thus the terminal is exactly the state excluded by the finite proof.

`no_fixed_width_two_step` starts from actual `Hyp`, `e1=0/1`,
`gam=0/1`, 和 `nextB` equations. The complementary center carries
follow from `Hyp`, rather than being imposed as an extra assumption.
There is no bound on the common word length 和 no nonempty-word premise.

### 3. Arbitrary widths 和 trims

`GeneralCounterexample.lean` imports the existing, unchanged exterior
padding theorem from [Agent114, PR #366](https://github.com/taco-jpg/p196-algorithm/pull/366).
The underlying mathematical padding/canonicalization attribution remains
[Agent7, #315](https://github.com/taco-jpg/p196-algorithm/pull/315)
和 [#326](https://github.com/taco-jpg/p196-algorithm/pull/326).

For hypothetical one-lap edges with trims `u0,u1`, the actual output
lengths give

```
|B0| = |B1| + u0,
|B1| + 1 = |B0| + u1.
```

Choose `M=max(|B0|,|B1|)+1` 和 pad by `a0=M-|B0|`, `a1=M-|B1|`.
Then `u0+a0=a1` 和 `u1+a1=a0+1`. Existing covariance produces
`W0 -> W1` 和 `W1 -> W0 ++ [5]`, preserving both original centers,
Hyp, e, 和 g. The fixed-width obstruction now applies. This covers
empty original exteriors 和 every nonnegative original trim count.

## Dependency integrity 和 independent checks

The imported #366 head is
`7ccb2d3fbc04a9cfb15d56f2d1528707361219d8`.
Its two Lean files, existing control script, report, 和 registry entry
are included unchanged. Their source blobs are:

| Dependency | Git blob |
|---|---|
| ExteriorPadding.lean | `6cade3b5e4eaaa0f4bd7110c78fd5d0b17f1cc09` |
| EdgeTransport.lean | `364cce5f29b7862d7e79e6973f9902c284656296` |
| exterior_padding_controls.py | `ea5dae3037ee5813051d85bd6d77bb549be74a43` |
| agent-114-T2.md | `f707d02058690b356f016850d405b4e4005372e9` |

The parent paper/computation is #417 at
`515d20f59e8d083be4a18a5140086f2fe452b799`; its existing three
files are unchanged. Its independent whole-integer 和 mirror checks,
96-state Cartesian transition enumeration, six-state paper certificate,
alternative twelve-state separator, seven complete graph comparisons,
empty-word control, 和 false-primitive binary control remain applicable.

Separate source review checked reverse-digit orientation, the overflow
appended low digit 0, terminal delayed digit 5, both padding-count signs,
empty words, 和 the fully quantified final existential negation. No
additional symmetry, width cap, parity condition, center update, or
unproved period-descent assumption enters the formal theorem.

## Reproduction 和 resource gate

With the pinned stock Lean 4.19.0 toolchain on PATH, from the repository
root:

```sh
python3 calculation/agent-105/period_descent.py
python3 calculation/agent-105/period_descent_audit.py
python3 -O calculation/agent-105/period_descent_audit.py
python3 tools/verify.py --changed
```

The unmodified repository gate is run with `LEAN_NUM_THREADS=1` 和
stock `lean4checker` tag `v4.19.0`, commit
`e11f65c651edd58d68ba260015d2bfde5102cd7f`, from a clean checkout.
The `LEAN4CHECKER` setting only selects that existing stock executable.
No verification script or checker source is changed.

All four final source files compiled successfully under explicit 8 GiB
address-space 和 1,200-second per-file limits:

| New module | Seconds | Peak RSS, KiB |
|---|---:|---:|
| FiniteGraph | 6.743573 | 932,284 |
| ActualBridge | 0.572248 | 462,212 |
| Witness | 0.583142 | 475,332 |
| GeneralCounterexample | 0.687939 | 467,080 |

Actual `python3 tools/verify.py --changed` PASS against pinned
`origin/main`: 5,223 Lean files, 303 projects; six new modules built 和
kernel-replayed, two projects audited, 32 endpoints checked. Four modules
和 18 endpoints are new here; two modules 和 14 endpoints belong to
the unchanged #366 dependency. Only the permitted axioms `propext`,
`Classical.choice`, 和 `Quot.sound` occur. The original mirror/audit
commands above pass, including optimized Python. The final staged tree
is checked before publication; its hash is recorded in the PR.

The result validates a physical multiple-lap positive control already
being adopted by the team's exterior-language tools. It leaves the
priority decimal P24 repeated-lap question open.
