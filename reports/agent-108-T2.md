# Agent 108 — exact exterior coding at the bound P = 4G

## Result 和 scope

**PAPER PROOF + COMPUTED, with independent arithmetic checks.** For a
base-10 exterior cycle with overflow stream `(1000)^G`, the recurrent
projection onto the first 两个 coefficients 有 an exact binary coding.
At the start of block k its coefficients are

\[
q_{0,k}=10,\qquad q_{1,k}=4+9a_k+a_{k+1},\quad a_k\in\{0,1\}.
\]

Conversely, each cyclic binary word gives a closed walk in 这 necessary
2-column relation. Thus the relation permits every block period G,
including G=1; it cannot prove `3 | G` or classify finite exterior cycles.
The finite neutral-tail condition remains essential 和 unresolved here.

No complete B cycle, matching C, decimal certificate, or new Lean theorem
is supplied. 这 result describes the exact relaxation, including its
limitation; it does not assert that its walks extend to a finite B.

## Prior work 和 representation

Agent 2's [period bound 和 equality case](https://github.com/taco-jpg/p196-algorithm/pull/309)
establish `P <= 4G` 和 that equality forces `(1000)^G`, up to rotation.
Agent 7's [neutral-padding proof](https://github.com/taco-jpg/p196-algorithm/pull/315)
permits the representation `B ++ 9^infinity`; appending or trimming finite
terminal 9s leaves that representation unchanged. The underlying arithmetic
is `calculation/neutral_band_search.py`, particularly `norm` 和 `nextB`.
The present contribution is the second-column classification, its binary
coding, 和 independent deeper-prefix checks.

For a finite observed prefix `q[0:m]`, forward carries satisfy

\[
\ell_0=0,\quad \ell_{i+1}=\lfloor(q_i+\ell_i)/10\rfloor.
\]

Choose the unknown reverse boundary carry `r_m` freely from `{0,1}`,
then compute `r_i=floor((q_i+r_(i+1))/10)` backwards. The overflow is
`g=r_0`. Put `d_i=(q_i+ell_i)%10` 和 `f_i=(q_i+r_(i+1))%10`.
The next prefix is `d_i+f_i` when g=0; when g=1 it is
`d_0+1` at i=0 和 `d_i+f_(i-1)` at i>0.

These formulas follow directly from the exact mirror. Allowing either
reverse boundary carry is a necessary overapproximation. Beyond the
possible new overflow column, the appended neutral tail emits complementary
forward/reverse digits, so their sum stays 9. 这 argument covers empty B 和 B shorter
than the observed prefix, including changes of finite trim convention.

## First coefficient: the forced four-step itinerary

On an overflow step the positive first coefficient x becomes `x%10+1`.
On a nonoverflow step it becomes `2x+c`, where c is a bit 和 `x+c<=9`.
Three successive nonoverflow steps after an overflow require the reset
coefficient to be at most 2. Therefore only preoverflow x=10 or x=11
can complete a block. Starting at 11 resets to 2 和 finishes at least 16,
which cannot start another complete block. A closed walk therefore uses
x=10 at every block start. The three doubling steps must give
`8+4c1+2c2+c3=10`, forcing `(c1,c2,c3)=(0,1,0)`.

Hence the first coefficient follows `10 -> 1 -> 2 -> 5 -> 10`, 和 the
forward carries entering coefficient 1 are `(1,0,0,0)`.

## Complete second-column classification

Write y for coefficient 1 和 h for the incoming reverse carry from
coefficient 2. The outgoing reverse carry is `c=floor((y+h)/10)`.
The first-coordinate itinerary forces c=0,1,0 at phases 1,2,3;
the phase-0 value is unrestricted. The second coefficient obeys

\[
y_1=(y_0+1)\bmod10+c_0,\qquad
y_{t+1}=y_t\bmod10+(y_t+h_t)\bmod10\quad(t=1,2,3).
\]

The complete four-step transition table is:

| Source y0 | Possible y4 |
|---|---|
| 3, 12 | 18 |
| 4, 13 | 0 through 7 |
| 5, 14 | 8 through 15 |
| 6, 15 | 16 through 18 |
| 0, 1, 2, 7, 8, 9, 10, 11, 16, 17, 18 | none |

For a direct derivation, phase 1 satisfies y1 in `{4,5,6,7}`. Its
respective target sets are `{18}`, `0..7`, `8..15`, `16..18`.
The phase-0 formula gives the source pairs in the table.

Rows 3,12,6,15 lead only to vertices with no successor. Removing those
rows 和 the vertices with no outgoing edge leaves exactly:

| Recurrent source | Recurrent targets |
|---|---|
| 4, 13 | 4, 5 |
| 5, 14 | 13, 14 |

The unique encoding `y_k=4+9a_k+a_(k+1)` turns 这 into the binary
overlap rule `(a,b)->(b,c)`. For any triple of bits a,b,c the full trace is:

| Phase | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| q0 | 10 | 1 | 2 | 5 | 10 |
| q1 | 4+9a+b | 5+b | 11+2b | 2+4b+bc | 4+9b+c |
| Reverse carry into q1 | arbitrary bit | 1 | bc | b XOR c | next block |

Substitution verifies the eight bit triples, each with either phase-0
boundary carry. Thus the recurrent graph 有 4 vertices, 8 edges 和
16 carry-labeled paths. Every cyclic binary word works in 这 graph.
The displayed coefficients never equal 9, so an actual recurrent finite
exterior in 这 family satisfies `|B_t|>=2` at each phase.

## COMPUTED reproduction

Run from the repository root:

```bash
python3 calculation/neutral_band_search.py selftest
python3 calculation/agent-108/coding_audit.py
python3 calculation/agent-108/independent_saturation.py --max-width 11 --vertex-cap 1000000 --mirror-width 4
python3 calculation/agent-108/saturation_prefix.py --depth 11 --seconds 120
python3 tools/verify.py --changed
```

The mirror selftest accepts the eight existing source certificates.
The standalone coding audit uses direct digit arithmetic 和 Floyd
reachability, independently of the prefix program's SCC computation:

```text
ALL CHECKS PASSED: raw_paths=80, cyclic_nodes=[4, 5, 13, 14], recurrent_edges=8, recurrent_carry_paths=16
```

It examines 19*16=304 source/carry choices. A separately authored prefix
implementation passes 260,640 arbitrary-boundary comparisons against
the mirror 和 130,321 finite/empty-B neutral-padding comparisons.

Deeper-prefix graphs extend only recurrent prefixes from the preceding
width. 这 pruning is sound: a projected closed walk remains closed.
Each graph edge represents the complete four-step block.

| Prefix width | Candidate vertices | Edges | Recurrent vertices |
|---:|---:|---:|---:|
| 2 | 19 | 40 | 4 |
| 3 | 76 | 234 | 25 |
| 4 | 475 | 1,475 | 68 |
| 5 | 1,292 | 4,653 | 134 |
| 6 | 2,546 | 8,163 | 314 |
| 7 | 5,966 | 17,610 | 809 |
| 8 | 15,371 | 56,957 | 3,211 |
| 9 | 61,009 | 225,035 | 9,430 |
| 10 | 179,170 | 678,976 | 28,174 |
| 11 | 535,306 | 2,020,901 | 85,054 |

The independent implementations agree through width 11. At each width
some cyclic SCC 有 cycle-length gcd 1, so these particular finite
relaxations cannot force `3 | G`. A gcd-1 SCC does **not** imply a
self-loop or a closed walk of every small length. No statement about
arbitrarily deep prefixes follows from 这 finite table. Width 12
was not completed; a separate guarded run (`--depth 15 --seconds 45`) reported UNDECIDED at its
1,000,000-candidate cap. Width 11 completed locally in about 49 seconds.

`python3 tools/verify.py --changed` passed: 5,217 Lean files, 301 registered
projects, 0 changed Lean modules, 0 audited endpoints. 这是 the actual
repository gate for code/report changes, not a new Lean proof. The
arbitrary-G finite-neutral-boundary classification remains open.
