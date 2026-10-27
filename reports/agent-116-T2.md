# Agent 116 — independent period-20 exterior audit

## Result 和 attribution

**PAPER PROOF + COMPUTED:** an independently authored, explicit carry-tuple
implementation corroborates Agent4's complete decimal period-20 exterior
negative in [issue #311](https://github.com/taco-jpg/p196-algorithm/issues/311)
和 [PR #323](https://github.com/taco-jpg/p196-algorithm/pull/323).
Every overflow necklace is covered, including words with smaller primitive
period. All 449 head-admissible graphs exhaust with no accepting interface.
Thus there is no period-20 finite exterior return in the stated A120 model,
at any width or natural neutral-suffix trim schedule.

This is independent corroboration, not a new primary discovery or a new
mathematical automaton. The all-width reduction is proved below; the finite
exhaustion is computed. No new Lean theorem is asserted. No center cycle,
decimal Lychrel number, arbitrary-period exterior obstruction, or general
one-band impossibility follows.

Claim: issue #289, comment 6433028463. Progress: comment 6433119206.
The reviewed primary report is `reports/agent-4-T2.md` at PR323 head
`6e06c860bc658af484355725d26232c9fa3f285f`. Its first-coordinate filter
comes from Agent4's issue #290; its positional model comes from the existing
`calculation/neutral_band/structure/bauto.cpp`.
Agent7's neutral-padding work 和 Agent114's later Lean padding bridge
(PR366) retain their separate attribution.

## Exhaustive coverage 和 exact output

The new recursive necklace enumeration emits every least cyclic rotation.
It checks uniqueness 和 minimality directly; independent Burnside counts
check the total at every weight. Imprimitive necklaces are retained.

| Overflow weight | All necklaces | Head survivors / exhausted | Tuple state records |
|---:|---:|---:|---:|
| 0–4 | 314 | 0 | 0 |
| 5 | 776 | 1 | 44,160 |
| 6 | 1,944 | 23 | 3,719 |
| 7 | 3,876 | 164 | 252,088 |
| 8 | 6,310 | 219 | 877,293 |
| 9 | 8,398 | 41 | 259,825 |
| 10 | 9,252 | 1 | 29,697 |
| 11–20 | 21,618 | 0 | 0 |
| **Total** | **52,488** | **449 / 449** | **1,466,782** |

Every target status is `EXHAUSTED`; no acceptance, state cap, time cap,
memory cap, partial expansion, or unprocessed word remains.
The largest graph has **815,179 states**, maximum spatial depth **47**,
at `g=00001110001001110001`, a rotation of Agent4's
`11100010011100010000`. Its state/depth counts agree exactly with the primary
report. State counts include one FIRST seed plus distinct INTERIOR tuples.

The complete run, including coverage checks 和 five known-positive queries,
took **11.608054 seconds**, peak child RSS **441.644531 MiB**.
There were **1,466,333 generated columns** across the 449 target graphs.
The lexicographically sorted survivor list, one LF-terminated word per line,
has SHA-256:

```text
ff374f36e358683977f34e9e3f100981b537e7b114fe24380f9b032dd975bf3f
```

## Why the head filter is sound — PAPER PROOF

For nonempty B let x=B[0], in 1..18; use x=9 for empty B.
If c is the inward reverse carry at that first coefficient, then

```text
g = floor((x+c)/10)
x_next = 2*x+c              if g=0
x_next = (x mod 10)+1       if g=1.
```

A legal trim removes only a suffix of 9s. It preserves the first coefficient
unless the whole raw word is neutral, in which case the empty target's
effective coordinate is again 9. For empty source B, e=0 和 g=1,
the raw successor is [10], represented exactly by x=9,c=1.
Every true exterior cycle therefore projects to a closed walk in this
18-state labelled graph. Rejected overflow words cannot support B cycles.

For weight k, the independent necklace count is

```text
N(20,k) = (1/20) * sum_{d divides gcd(20,k)} phi(d)*binomial(20/d,k/d).
```

Every emitted weight count equals this formula. Distinct checked least
rotations with the complete count exhaust the rotation classes.
Changing time origin merely rotates g, so one representative per class suffices.

## Why a finite tuple graph covers all widths — PAPER PROOF

Write h=b-1. Let F_b(B) be A120's exterior successor with reverse incoming
carry 1-e, where e is the low normalization's outgoing carry.
Neutral coefficients transmit either incoming carry unchanged, so

```text
F_b(B ++ h^a) = F_b(B) ++ h^a,
```

with e 和 overflow g preserved, including B empty. In the two normalizations,
the new neutral digits are h(1-e) 和 he; their reflected sum is h.
Substitution in both overflow branches gives the stated covariance.

Suppose arbitrary-width words satisfy F_b(B_t)=B_(t+1)++h^(u_t) cyclically.
Choose N at least one 和 every phase width; put Q_t=B_t++h^(N-|B_t|).
Since |B_(t+1)|+u_t=|B_t|+g_t, covariance gives

```text
F_b(Q_t) = Q_(t+1) ++ h^(g_t).
```

All Q_t now have common width N 和 positive first coefficients. Originally
empty words become nonempty neutral padding. Thus searching common-width
words with u_t=g_t loses no arbitrary-width exterior cycle.

At spatial cut j, the tuple stores, for every time t:

- L_t: the low normalization carry entering column j.
- H_t: the reverse normalization carry leaving column j toward lower indices.
- Y_t: the previous column's reverse digit, used only when g_t=1.

Initially L=0, H=g, 和 Y_t=1 on overflow phases. For candidate coefficient
x_t 和 guessed reverse incoming carry q_t in {0,1}, impose

```text
floor((x_t+q_t)/b) = H_t
d_t = (x_t+L_t) mod b
r_t = (x_t+q_t) mod b
x_(t+1) = d_t+r_t if g_t=0, otherwise d_t+Y_t.
```

The next spatial tuple is L'_t=floor((x_t+L_t)/b), H'_t=q_t,
Y'_t=r_t on overflow phases. Closing x_p=x_0 enumerates every permissible
temporal column exactly. The first column requires every x_t>0; interior
columns allow zero. All generated coefficients stay in 0..2h.

The terminal condition is L_t+H_t=1, 和 Y_t=h*L_t on overflow phases.
The first equality supplies the reverse incoming carry 1-e_t. The second
makes the overflow's extra last coefficient h(1-e_t)+Y_t=h, exactly the
neutral suffix in the common-width equation. Conversely, an accepted finite
path reconstructs common-width words satisfying that equation.

Every terminal tuple admits a neutral-column self-loop. Canonical witnesses
may therefore strip their terminal neutral coefficients without changing
their emitted carries or exterior return. The implementation independently
replays each printed canonical witness.

There are at most 4^p*b^(sum g) interior tuples. Complete reachable-state
traversal with no terminal tuple therefore excludes every finite width.
Hash collisions are resolved by full array equality; no packed integer key
or depth cutoff is used. FIRST 和 INTERIOR modes are explicitly separate.
The search keeps all accepted carry streams e; it does not assume that a
repeated g word forces the same smaller period in B or e.

## Independent controls

`exterior_tuple_oracle.py` computes the full exterior map using whole-integer
positional values 和 division. It enumerates complete fixed-width functional
graphs, finds their cycles, includes temporal repetitions, 和 compares exact
e-to-minimum-width maps with the tuple solver's bounded-width mode.

| Control | Result |
|---|---|
| Bases 2,3,4; every g necklace, periods 1..6; width bounds 1..3 | 333 exact comparisons |
| Positive / negative comparisons | 10 / 323 |
| Full nonempty coefficient words | 492 |
| Words including empty B controls | 495 |
| Neutral-padding / all-legal-trim equalities | 990 / 641 |
| Decimal head projection direct controls | 6,859 words / 7,432 legal trimmed edges |
| Necklace generator versus brute rotations, p1..10 | 261 necklaces |

Both ordinary 和 optimized Python execute explicit validation exceptions;
neither relies on removable `assert` statements. Their oracle JSON agrees
exactly after removing elapsed time. These bounded controls check both
acceptance 和 rejection, independently of the local tuple transitions.

The main harness additionally exhausts known-positive exterior drivers at
bases 2,4,10,20, reconstructing 和 independently integer-replaying **18 carry
streams / 143 B edges**. Decimal p11 recovers e=10100110011 at width29;
p12 recovers all three documented e streams at common padded width53.
The base20 control uses the independently reconstructed PR356 driver;
the harness needs no file or commit from PR356 to run.

## Reproduction 和 resource semantics

From repository root, Python 3 和 a C++17 compiler suffice:

```bash
python3 calculation/agent-116/p20_independent.py
c++ -O3 -std=c++17 -Wall -Wextra -pedantic calculation/agent-116/exterior_tuple.cpp -o /tmp/agent116-exterior-tuple
python3 calculation/agent-116/exterior_tuple_oracle.py --solver /tmp/agent116-exterior-tuple
python3 -O calculation/agent-116/exterior_tuple_oracle.py --solver /tmp/agent116-exterior-tuple
python3 calculation/agent-116/p20_coverage.py --selftest
```

The first command compiles fresh in a temporary directory. Default limits:
one process at a time, 2,000,000 states, 30 seconds 和 4 GiB address space
per graph; 900 seconds for the target batch. The complete observed run is
well below those limits. No Studio computation is required.

`STATE_CAP_UNDECIDED`, `TIMEOUT_UNDECIDED`, `MEMORY_CAP_UNDECIDED`, process
failure, malformed output, 和 unprocessed words cannot produce a negative
verdict. The optional `--prefix-width` mode returns `BOUNDED_WIDTH_ONLY`
when an unexpanded frontier remains; the all-width harness rejects that mode.
For every reported exhaustion it checks an empty frontier, completed initial
expansion, no partial expansion, 和 all reached interior states processed.
Any acceptance is retained 和 independently replayed, even if a later cap hits.

Source SHA-256 of the tested C++ implementation:

```text
98f1e1afa74f7bbe085b003719644252012d3d400fa2e52a319443204f8652d9
```

## Repository gate 和 limits

The final contribution is based directly on main
`eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`, with four new source files 和 this
report only. It has no dependency on Agent4's branch or PR356.
No README, RESULTS, registry, or other agent's source changes are included.

The literal isolated-tree `python3 tools/verify.py --changed` passed:

```text
[rules] 5217 Lean files, 301 projects, OK
[changed] against origin/main: 0 new/changed Lean file(s); building 0 module(s); auditing 0 project(s)
[build] OK
[axioms] 0 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

No new Lean module is added. This repository-gate PASS validates the repository
rules; it does not convert the computed exhaustion into LEAN-VERIFIED.
