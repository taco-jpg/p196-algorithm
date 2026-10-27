# Agent 104 — every decimal neutral-band certificate needs at least six overflows

**Status: COMPUTED + PAPER PROOF; no new Lean theorem.**

For every nonempty edge cycle accepted by `Agent120.Neutral.cycleOK 10`,
the total overflow count satisfies

\[
G=\sum_{t=0}^{P-1}\gamma_t\ge6.
\]

The widths of the exterior B 和 center C, the period, the trim counts,
和 the primitive periods of the individual streams are unrestricted.
The numerical exclusion uses finite positional automata; it is not a
kernel-checked nonexistence proof. It does not exclude G>=6, prove that
the whole neutral-band route fails, or establish decimal Lychrel existence.

## 1. Attribution 和 scope

The campaign claim is [T1.total-overflow-at-most4](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432782889).
This result combines established mechanisms into a global overflow-budget
obstruction, with fresh complete executions of every numerical subcase.
It does not claim the earlier p11/p12 census, first-head inequality, or
neutral-padding identity as new discoveries.

- The baseline [neutral-band README](https://github.com/taco-jpg/p196-algorithm/blob/eafbbbfd6b5b857597f95f68268c56dbd96b6bcb/calculation/neutral_band/README.md)
  records the exact B/C decoupling 和 original all-length p11 exclusion.
- Agent 4's [first-head analysis](https://github.com/taco-jpg/p196-algorithm/issues/290)
  和 Agent 2's [overflow-period bound](https://github.com/taco-jpg/p196-algorithm/issues/294)
  supply the finite reduction used below.
- Agent 7's [neutral-padding theorem](https://github.com/taco-jpg/p196-algorithm/pull/315)
  supplies the covariance identity. The arbitrary-schedule application below
  was independently identified during this audit; Agents 107 和 110 claim
  the dedicated T3 schedule-equivalence work in issue #289.
- Agent 107 owns the general `bauto` completion audit. This report's local
  diagnostic only establishes actual exhaustion for its own 48 inputs.

Source baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.
Only `calculation/agent-104/` 和 this report are added.

## 2. PAPER PROOF: reduction to G=2,4 和 P<=16

All carries are bits because the coefficients lie in 0..18. The flip
condition in `Hyp` forces the outgoing center carry to be 1-e.
The exact lengths before trimming satisfy

\[
|\operatorname{nextB}|=|B|+\gamma,
\qquad |\operatorname{nextC}|=|C|+\gamma.
\]

Summing the edge equations around the cycle gives

\[
\sum u=G,\qquad 2\sum v=G.
\]

Thus G is even. Empty C is impossible because it cannot change the
entering carry. Although `Hyp` does not explicitly require symmetry,
each `nextC` is symmetric, 和 deleting equal neutral prefixes/suffixes
preserves symmetry. Every C on a closed cycle is therefore symmetric.

For a nonempty exterior define x=B[0]; for an empty exterior define x=9.
Then 1<=x<=18. Some carry c in {0,1} gives the exact necessary transition

\[
\gamma=0:\quad x+c<10,\quad x'=2x+c;
\qquad
\gamma=1:\quad x+c\ge10,\quad x'=(x\bmod10)+1.
\]

The empty case has e=0, gamma=1, raw successor [10], hence effective
9->10. If an entire raw B is removed by neutral trimming, its first
coefficient was 9, agreeing with the empty target's effective head.

G=0 is impossible: each step strictly increases the positive head.
Consequently G is positive 和 even.

Consider a segment of length ell from just after one overflow through
the next overflow. Its initial 和 final heads x,y lie in 1..10. Before
the last overflow, the head z satisfies z>=2^(ell-1)*x 和 z<=18.
If y=1, the overflow formula additionally forces z=10. These bounds give

\[
\ell\le4+[x=1]-[y=1].
\]

Indeed, the four cases (x=1 or x>=2, y=1 or y!=1) give respectively
ell<=4,5,3,4. Summing the segment inequalities cancels the indicators:

\[
P\le4G.
\]

Therefore G<=4 reduces completely to G=2 with 2<=P<=8, 和 G=4 with
4<=P<=16. A returned B may have a smaller primitive period; the census
includes such repetitions rather than assuming stream primitivity.

## 3. COMPUTED: complete exterior classification in this budget

`calculation/agent-104/overflow_budget.py` enumerates every binary
rotation class with the prescribed P 和 G. Counts are independently
checked using the fixed-weight Burnside formula. A necessary 18-state
head filter is applied before the existing exact B position automaton.

For completeness, pad each B_t to a common positive width N with trailing
9s. Exterior padding covariance preserves e/g. Its new trim equals
u_t+(N-|B_t|)-(N-|B_(t+1)|)=gamma_t by the length equation. Thus every
original cycle lifts to the automaton's common-width model. At the inner
cut its boundary conditions are L=e, H=1-e, 和 pending reflected digit
9e on overflow phases, precisely the accepting predicate. Keeping every
accepted e stream covers every possible driver seen by the center.

| G | P | Overflow necklaces | Head survivors | Fully exhausted | Accepted (g,e) |
|---:|---:|---:|---:|---:|---:|
| 2 | 2,3,4,5,6,7,8 | 1,1,2,2,3,3,4 | 0,0,1,2,2,1,1 | 7 total | 0 |
| 4 | 4,5,6,7 | 1,1,3,5 | 0,0,0,0 | 0 | 0 |
| 4 | 8 | 10 | 1 | 1 | 0 |
| 4 | 9 | 14 | 4 | 4 | 0 |
| 4 | 10 | 22 | 7 | 7 | 0 |
| 4 | 11 | 30 | 9 | 9 | 1 |
| 4 | 12 | 43 | 9 | 9 | 0 |
| 4 | 13 | 55 | 6 | 6 | 0 |
| 4 | 14 | 73 | 3 | 3 | 0 |
| 4 | 15 | 91 | 1 | 1 | 0 |
| 4 | 16 | 116 | 1 | 1 | 0 |
| **Total** | | **480** | **48** | **48** | **1** |

The totals are 16 necklaces for G2 和 464 for G4. Agent 103's independent
audit caught an initial summary addition error; the per-period table,
enumerated inputs, state counts, 和 mathematical conclusion were correct.
The harness now prints these aggregate counts directly.

The unique accepted pair is

```text
P=11 G=4 g=00001110001 e=00111010011
```

It is the joint left rotation by seven phases of the documented pair

```text
g=11100010000 e=10100110011
```

This accepting graph was fully exhausted: 18,061 states, depth59.
Its first witness is at depth29; every reconstructed B transition,
carry/overflow bit, return, 和 total trim was independently replayed
through the existing `structure/bsys.py` arithmetic implementation.
The largest graph in the census was P8, g=01010101: 244,785 states,
depth88. There were zero caps, timeouts, or unfinished depth frontiers.
The combined census visited 289,112 (overflow-word, state) pairs:
431 for G2 和 288,681 for G4.

The first-head projection was also checked on all 6,859 valid B words
of widths 0..3, including empty B. All 35 distinct overflow-to-overflow
segment triples satisfy the inequality in Section 2.

### Actual exhaustion, packing, 和 the first column

The original `bauto.cpp` stops at depth400 without labelling that exit
as incomplete. The harness compiles the unchanged source through stdin
with one diagnostics-only statement reporting whether its final BFS
frontier is empty. An ordinary `done` message is never accepted as proof
of exhaustion. It retains every accepting e stream, even after a hit.

For this scope the packed key needs at most 2P+4G=48 bits, below its
128-bit capacity. Phase masks 和 arrays are also within their limits.
Source SHA-256 is printed; an ambiguous insertion point fails closed.

The initial key uses stricter nonzero column conditions than later
keys. This causes no missing path if that key recurs: with G>0, a
closed temporal column at the initial key cannot contain zero. A zero
would force its predecessor to have gamma=0, x=0,c=0; iterating backward
eventually reaches an overflow, whose output is at least one.

## 4. PAPER PROOF: arbitrary center trims are covered

Write P_a(C)=9^a ++ C ++ 9^a. Fix a legal driver (e,gamma), 和 let F
be its raw center transition. The neutral-padding identity is

\[
F(P_a(C))=P_a(F(C)).
\]

Explicitly, if D=norm(C,e).digits, normalizing P_a(C) gives
x^a ++ D ++ y^a, where x=9(1-e), y=9e. For gamma=0 the reflected
pair sum adds x+y=9 at both ends. For gamma=1 the output uses the same
word with one further y appended; its reflected pair sum gives the
same covariance. The outgoing carry remains 1-e in either case.

Suppose F_t(C_t)=P_(v_t)(C_(t+1)). Given ANY nonnegative schedule w
with the same total sum as v, solve cyclically

\[
a_{t+1}=a_t+v_t-w_t.
\]

The equal totals give closure; adding a common constant makes every
a_t nonnegative. Then C'_t=P_(a_t)(C_t) obeys

\[
F_t(C'_t)=P_{w_t}(C'_{t+1}).
\]

B 和 the e/g streams are unchanged. Thus unrestricted-width center
existence is invariant under replacing v by any schedule of equal
total. This is not valid as a transfer of fixed-width negative results.

For P11,G4, sum(v)=2. Therefore a single chosen binary schedule, such
as 11000000000, already suffices existentially. The audit nevertheless
checks all 55 binary schedules, then checks the chosen schedule again
with the separate legacy full-state layer engine.

## 5. COMPUTED: the only surviving stream has no center

`calculation/agent-104/center_budget.py` compiles the existing
`cauto_fast.cpp`, validates eight known positive drivers, 和 runs:

```text
CENTER base=10 p=11 G=4 mode=fast patterns=55 instances=1320 hits=0 maxstates=1437 max_jstar=6 max_period=1
CENTER base=10 p=11 G=4 mode=legacy patterns=1 instances=24 hits=0 maxstates=0 max_jstar=4 max_period=1
CENTER_G4_SURVIVOR_EXCLUDED all_lengths=true status=COMPUTED
```

Every fast pattern has `status=none`, a detected generic-frontier period
of one, 和 zero feasible terminal classes. The eventual-length cutoff
is mlo=23; short lengths 和 both parity classes above that cutoff are
checked. All 55 generic frontiers stabilize by layer6. The legacy
engine independently reaches jstar4, period1, mlo23 for the chosen
schedule. Its `maxstates=0` field is an unpopulated diagnostic, not a
claim that it explored zero states. Neither run has CAPPED or NOPERIOD.

Positive controls: every known base 2,4,8,11,16,17,26,32 certificate
passes the Python mirror. All eight driver streams remain center-feasible
when their one center trim is placed at phase0. The 56 source edges
also pass 224 padding-covariance checks at padding depths 0,1,2,5.

The positional center method covers arbitrary finite lengths through
exact generic-frontier repetition 和 its finite terminal layer checks.
This use stays at P<=12 和 small trim budgets; none of the P33/P48
array/packing extension issues discussed elsewhere is involved.

## 6. Reproduction 和 verification

From the repository root, with Python3 和 a C++17 compiler:

```bash
python3 calculation/neutral_band_search.py selftest
python3 calculation/agent-104/overflow_budget.py
python3 calculation/agent-104/center_budget.py
python3 tools/verify.py --changed
```

The B script ends with:

```text
FINAL {"accepted_e": 1, "accepted_g": 1, "complete": true, "exhausted_words": 48, "necklaces": 480, "necklaces_by_weight": {"2": 16, "4": 464}, "undecided_words": 0, "weights": [2, 4]}
```

The center script ends with `CENTER_G4_SURVIVOR_EXCLUDED`.
Both scripts reject incomplete solver coverage; an incomplete search
cannot become a negative result. Compilation 和 default computations
complete well inside the campaign's 30-minute sandbox budget.

The literal `python3 tools/verify.py --changed` gate passed:
`ALL CHECKS PASSED (changed files only, against origin/main)`.
It checked 5,217 Lean files 和 301 registered projects for repository rules.
This change adds no Lean modules or registry entries, so there were zero
new Lean endpoints to build/audit. The pass does not promote the numerical
result to LEAN-VERIFIED.

Combining Sections 2–5 excludes G=0,2,4 和 all odd G. Therefore every
accepted decimal certificate has G>=6, while existence at larger G
remains unresolved.
