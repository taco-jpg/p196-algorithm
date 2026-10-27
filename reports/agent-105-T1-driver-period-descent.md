# Agent 105 — T1: exterior driver-period descent fails

## Result 和 exact scope

**PAPER PROOF + COMPUTED:** in base 6 there is a canonical exterior B cycle
of least period four whose complete `(e,g)` driver has least period two,
but there is **no** exterior return for one copy of that same driver at
any finite width or with any admissible neutral trimming. Thus the general
existential period-descent implication is false, as is same-orbit rigidity.

The counterexample also has a common-width representative with `u=g`, so
even the joint `(e,g,u)` stream has period two while B needs four steps.
This is 不 merely a consequence of a longer canonical trim schedule.

This result concerns exterior dynamics in base 6. It does 不 settle a
decimal-specific descent statement, the priority P24 driver, center
compatibility, or the existence of a decimal certificate. 没有 compatible
C cycle or new Lean theorem is supplied; this is 不 LEAN-VERIFIED.

## Prior work 和 the proposed implication

The autonomous exterior update is established in
[`decouple.py`](../calculation/neutral_band/bases/decouple.py).
Neutral padding/canonicalization retain [Agent7's attribution, #315](https://github.com/taco-jpg/p196-algorithm/pull/315)
和 [#326](https://github.com/taco-jpg/p196-algorithm/pull/326).
Agent114's [#400](https://github.com/taco-jpg/p196-algorithm/pull/400)
formalizes the common-width reduction. The spatial carry model was
independently audited in [our #401](https://github.com/taco-jpg/p196-algorithm/pull/401).

For a fixed driver D of length p, the proposed implication is:

`a finite B return with driver D repeated k times, k>=1`

`implies a finite B return with driver D once, possibly using different B`.

The example below refutes this stronger existential statement, rather than
only showing that a particular orbit has a larger period. Previous warnings
against replacing repeated g by repeated B/e remain credited to the team.
The present obstruction fixes **both** carry 和 overflow streams.
Agent106/116/111 retain arbitrary-lap P24 languages/checking, Agent115 P48,
Agent109 bounded-B/all-laps, 和 Agent117/108 the one-lap results. This task
does 不 replace those scopes or claim their discoveries.

## An exact four-step exterior orbit

Coefficients are least significant first. Put `b=6`, `h=5`. Define F(B)
as the raw exterior update with the reverse normalization carry `1-e(B)`.
The following table lists all four edges; B2 is the next row cyclically.

| t | B | e | g | Raw F(B) | Maximal u |
|---:|---|---:|---:|---|---:|
| 0 | `[4,7,7,8,3]` | 0 | 0 | `[9,3,4,5,8]` | 0 |
| 1 | `[9,3,4,5,8]` | 1 | 1 | `[4,7,7,10,2,2]` | 0 |
| 2 | `[4,7,7,10,2,2]` | 0 | 0 | `[9,3,4,9,5,5]` | 2 |
| 3 | `[9,3,4,9]` | 1 | 1 | `[4,7,7,8,3]` | 0 |

Every coefficient lies in `0..10`, every first coefficient is positive,
和 every B ends in a coefficient different from 5. Removing the indicated
neutral suffix gives the next B. All four B are distinct, so their least
period is four. Their complete joint label word is `(e,g)=(01,01)` twice.

Padding every B to width six gives

```
W0 = [4,7,7,8,3,5]
W1 = [9,3,4,5,8,5]
W2 = [4,7,7,10,2,2]
W3 = [9,3,4,9,5,5]
```

Directly, `F(W_t)=W_(t+1) ++ 5^g_t`. These allowed trims are
`u=g=0101`; they need 不 be maximal. The four padded words are still
distinct. Thus fixed width 和 a period-two trim schedule do 不 restore
the failed implication.

## Why another one-lap representative is impossible

### Reduction to a common width

Neutral suffix padding preserves e/g 和 satisfies
`F(B ++ 5^a)=F(B) ++ 5^a`. For an arbitrary two-edge return
`F(B_t)=B_(t+1) ++ 5^u_t`, choose positive `M>=max_t |B_t|` 和 pad
each phase to M. The length identity `|B_(t+1)|=|B_t|+g_t-u_t`
then gives `F(W_t)=W_(t+1) ++ 5^g_t`. Empty B is covered by its
positive all-neutral padded word; indeed `F([])=[6]`.

It therefore suffices to exclude equal-width words for driver `e=g=01`,
with `F(W0)=W1` 和 `F(W1)=W0 ++ [5]`, at every positive M.

### Exact spatial equations

At a cut use state `s=(L0,L1,H0,H1,y)`: the two forward carries, the
two reverse boundary carries, 和 the previous reverse digit at overflow
phase 1. Carries are bits 和 `0<=y<=5`. The physical initial cut is
`R=(0,0,0,1,1)`.

For coefficient column `(x0,x1)` in `0..10` 和 inward bits `(a0,a1)`,
the exact transition is

```
D0=(x0+L0) mod6,       L0'=(x0+L0)//6,
D1=(x1+L1) mod6,       L1'=(x1+L1)//6,
R0=(x0+a0) mod6,       H0 =(x0+a0)//6,
y'=(x1+a1) mod6,       H1 =(x1+a1)//6,
x1=D0+R0,              x0=D1+y,
s'=(L0',L1',a0,a1,y').
```

Both coefficients must be positive at the first column. Later zero
coefficients are allowed. The required final state is
`T=(0,1,1,0,5)`: forward carries equal e, reverse entries equal `1-e`,
和 the extra overflow coefficient is neutral exactly when `y=5*e1=5`.
Every complete padded return supplies a path from R to T by these equations.

### A carry-sum invariant

Put `S=L0+L1`, `S'=L0'+L1'`. Adding the temporal equations gives

`6*S' = S + R0 + y`.

At R the right side belongs to `[1,6]`, so `S'=1`. When `S=1` it
belongs to `[1,11]`; its only multiple of 6 is 6. Therefore every cut
after the first has `L0+L1=1`. This argument also works in every base
b, replacing 6 by b 和 bounding the two digits by `b-1`.

### Six states form a complete inverse obstruction

Inside this invariant, write a target as `(U,V,s,t,Y)`. Choose bits
`l,h,k` for predecessor `L0,H0,H1`; then `L1=1-l`. Every predecessor
must have

```
x1 = 6*k + Y - t,
x0 = (x1-l-s + 6*(U+h))/2,
y  = x0 - ((x1+1-l) mod6).
```

Retain only integral coefficients in `0..10`, y in `0..5`, 和 all
four carry equations above. The complete predecessor table is:

| Target | All predecessors with S=1 | Their columns `(x0,x1)` |
|---|---|---|
| `T=(0,1,1,0,5)` | `T`; `A=(0,1,0,0,2)` | `(5,5)`; `(2,5)` |
| `A=(0,1,0,0,2)` | `B=(0,1,0,1,1)` | `(4,8)` |
| `B=(0,1,0,1,1)` | `C=(0,1,0,1,2)` | `(3,6)` |
| `C=(0,1,0,1,2)` | `D=(1,0,0,1,2)` | `(3,7)` |
| `D=(1,0,0,1,2)` | `E=(1,0,1,0,5)` | `(6,1)` |
| `E=(1,0,1,0,5)` | None | — |

Here is a direct check of exhaustiveness, without trusting a graph search.
For T, the coefficient bound forces `k=0,x1=5`; `V=1` forces `l=0`.
The two h values give `x0=2,5` 和 `y=x0`, yielding A 和 T.
For A, `V=1` forces `k=1,x1=8`; `U=0,s=0` forces `h=0`.
Integrality then forces `l=0,x0=4,y=1`, yielding B.
The same argument for B gives `x1=6,l=0,x0=3,y=2`, yielding C;
for C it gives `x1=7,l=1,x0=3,y=2`, yielding D.
For D, `V=0` forces `k=0,x1=1`; integrality forces `l=1` 和
`x0=3+3*h`. The required `U=1` forces `h=1,x0=6,y=5`, yielding E.
For E, `x1=5` 和 `V=0` force `l=1`; since also `s=1`, the temporal
equation would be `5=2*((x0+1) mod6)`, impossible by parity.

The first-column equations from R force `(x0,x1)=(4,9)` or `(5,10)`.
Their four successors are

```
(0,1,1,0,3), (0,1,1,1,4),
(0,1,0,0,4), (0,1,0,1,5).
```

None is in `{T,A,B,C,D,E}`. That set contains T 和 is closed under
all predecessors within the invariant. A path from a first-column state
therefore cannot reach T. This proves the exclusion for every finite M,
和 hence for arbitrary original widths 和 neutral trims. Together with
the four-step witness it proves the claimed existential counterexample.

## Computation, independence, 和 reproduction

From the repository root:

```sh
python3 calculation/agent-105/period_descent.py --table
python3 calculation/agent-105/period_descent_audit.py
python3 -O calculation/agent-105/period_descent.py
python3 -O calculation/agent-105/period_descent_audit.py
python3 tools/verify.py --changed
```

The primary verifier replays the witness using whole-integer evaluation
和 the unchanged official mirror, checks every entry of a static
24-state/24-transition forward graph, 和 separately checks generic vector
graphs for p2 和 p4. The complete p2 graph has maximum shortest depth 7
和 accepts only `e=10` (at width 5), whereas p4 has 65 states/68
transitions, maximum shortest depth 8, 和 accepts `e=1010` at width 5
和 `e=0101` at width 6. 没有 cap, timeout, or unprocessed frontier occurs.

The independent audit compares seven complete graph state/depth sets,
uses different coefficient/carry enumeration, checks all 96 generic states
和 96 labelled transitions, 和 verifies the six-state inverse certificate.
It also checks a backward-closed 12-state set in
the full 96-state universe, independently of the carry-sum restriction.
The positive p2 control is
`[4,7,7,6,8] -> [9,3,4,2] -> first`, with `e=10,g=01`.
Empty/all-neutral padding is checked explicitly. Essential checks use
exceptions 和 remain active under optimized Python.

The mirror replay uses per-edge centers `[10]` or `[0]` only to realize
the required carry flip. These separate fixtures are **not** a C cycle.
The computation is a verifier of the explicit witness 和 finite paper
obstruction, with no broad bounded search needed to reproduce the result.

Actual `python3 tools/verify.py --changed` PASS: 5,217 Lean files 和
301 projects checked; zero new/changed Lean modules 和 zero endpoints
audited. This zero-module gate does 不 kernel-verify the mathematical
claim above. Both verifier commands also PASS under normal 和 optimized
Python on the final source.

## Consequence 和 remaining question

A complete fixed driver can have a genuine multiple-lap exterior return
even when its one-lap exterior language is empty. The padded two-step map
exchanges W0 和 W2, so it cannot preserve any total order on that pair;
a general monotone-map argument cannot restore the proposed descent.

This base-6 example is a useful positive control for repeated-driver
exterior-language tools. It does 不 show that the priority decimal P24
driver has a multiple-lap return. A specifically decimal reduction needs
additional proof; otherwise the distinct repeated-lap searches remain
necessary.
