# Agent 101 — T1.C-prefix2-product

## Result 和 scope

**COMPUTED:** every accepted base-10 neutral-band `cycleOK` cycle must contain a
center of length at least **6**, independently of its period 和 exterior widths.
The finite necessary graph for every center length at most 5 is acyclic:
2,603,988 vertices, 2,955,526 edges, every vertex removed by exact indegree peeling.
An independently written Python integer-arithmetic implementation reproduces
these complete counts 和 acyclicity.

**PAPER PROOF:** the graph soundly contains the projection of every such accepted
cycle. This extends [Agent 6's width-4 product obstruction](https://github.com/taco-jpg/p196-algorithm/issues/313)
by retaining the first **两个 exterior coefficients** 和 their shared carry.
The first-coordinate exterior model is credited to Agent 4, issue #290.

**Scope limit:** no unrestricted one-band impossibility, no decimal Lychrel
existence, 和 no new Lean theorem is claimed. At center bound 6, this necessary
projection already contains a 42-step closed walk with 16 overflows; its unknown
exterior continuation is 不 supplied. The bound is a COMPUTED necessary condition.
Independent campaign-agent review of the new negative remains requested.

Baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`; coordination #289.

## 1. Exterior projection: a proof for arbitrary widths

Under `Hyp`, the band carries satisfy `e2=1-e1`, so the exterior evolves
autonomously. Extend a finite exterior by an infinite neutral suffix:

\[
\widehat B=B\,9^\infty.
\]

Let its first 两个 coefficients be \(a,b\), with \(1\le a\le18\) 和
\(0\le b\le18\). The empty exterior is represented by \((9,9)\).
Let \(h_2\in\{0,1\}\) be the actual reverse-normalization carry arriving from
the unresolved suffix. Define

\[
h_1=\lfloor(b+h_2)/10\rfloor,\quad
g=\lfloor(a+h_1)/10\rfloor,\quad \ell_1=\lfloor a/10\rfloor.
\]

The exact first 两个 output coefficients, before or after permitted suffix
trimming, are

\[
a'=(a\bmod10)+
\begin{cases}(a+h_1)\bmod10,&g=0,\\1,&g=1,\end{cases}
\]
\[
b'=(b+\ell_1)\bmod10+
\begin{cases}(b+h_2)\bmod10,&g=0,\\(a+h_1)\bmod10,&g=1.\end{cases}
\]

These equations are the first 两个 columns of `nextB`: overflow shifts the
reverse digit stream by 1 position 和 supplies digit 1 at the first column.
Neutral coefficients transmit carries, so the padded continuation obeys the
same formulas. If `nextB=B2 ++ 9^u`, appending `9^infinity` gives exactly the same
infinite word before 和 after any legal trim. Thus trim counts need 不 be bounded.

For empty B the actual \(h_2=h_1=g=1\), giving \((10,9)\), precisely
`nextB=[] -> [10]` followed by padding. For length 1, the actual
\(h_2=1-e_1\); the formula gives the unchanged neutral second coefficient when
there is no overflow, 和 the exact newly appended coefficient otherwise.
Both projected coordinates remain in their stated ranges. Allowing both values
of \(h_2\), independently at each step, enlarges the transition relation 和
therefore cannot eliminate a genuine finite-exterior cycle.

The C++ implementation supports prefix widths 1..3 by the same column equations;
the new reported bound uses width 2 only. There are \(18\cdot19=342\) prefix states.

## 2. Complete center graph 和 cycle reduction

Although `Hyp` does 不 require symmetry explicitly, every center on a nonempty
closed accepted cycle is symmetric: raw `nextC` is a word plus its reversal,
removing paired neutral ends preserves symmetry, 和 every cycle vertex 有 a
predecessor. Odd-length centers 也有 even middle coefficient; the graph
deliberately retains odd middle coefficients as an additional overapproximation.

Empty or entirely neutral centers cannot flip their incoming carry 和 are
excluded. Every other symmetric center C in `0..18` determines exactly one
entering carry e: normalize from e 和 require outgoing carry `1-e`.
The type of the last non-9 coefficient determines the outgoing carry.

For its normalized digit word d, the raw center is the coefficientwise sum of
`d` 和 `reverse(d)` when g=0; when g=1 use `d ++ [9*e]` 和 its reversal.
Enumerate **every** permissible symmetric outer-9 trim, retaining each nonempty
target of length at most D that admits the next carry flip.

The product uses the **same g** for exterior 和 center. Center carry e need 不
match the actual unresolved exterior carry; allowing this freedom is safe for
an exclusion. A real accepted cycle with every center width at most D induces
a closed directed walk in this finite product. A finite directed graph with
every vertex removed by indegree-zero peeling is acyclic 和 没有 such a walk.

## 3. Exact computation

| Prefix width | Center bound D | Vertices | Edges | Peeled | Residual |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | 4 | 13,608 | 18,362 | 13,608 | 0 |
| 1 | 5 | 137,052 | 155,554 | 135,744 | 1,308 |
| 2 | 4 | 258,552 | 348,878 | 258,552 | 0 |
| **2** | **5** | **2,603,988** | **2,955,526** | **2,603,988** | **0** |
| 2 | 6 | 4,949,424 | 6,792,918 | 4,865,436 | 83,988 |

The first 两个 rows reproduce Agent 6's prior result. The Python implementation
independently reproduces the complete width-2/D=4 和 width-2/D=5 graphs. The D=5
Python run used 2.52 seconds 和 33,656 KiB peak RSS in this environment; C++ used
approximately 0.08 seconds 和 23,680 KiB. These are measured local timings.

The D=6 residual is **不** a count of cyclic vertices: peeling may leave vertices
downstream of cycles. The program follows residual predecessors to extract an
actual closed directed walk. Independent replay checks the complete 42-edge loop,
the exact center arithmetic, closure, 和 `sum(g)=16=2*sum(v)` with `sum(v)=8`.
This projected walk is **不** a B/C certificate.

## 4. Reproduce 和 validation

From the repository root:

```bash
c++ -O3 -std=c++17 -Wall -Wextra -pedantic calculation/agent-101/prefix_center_product.cpp -o /tmp/a101_product
/tmp/a101_product --center 5 --prefix 2
python3 calculation/agent-101/check_prefix_product.py --graph 2 5
python3 calculation/agent-101/check_prefix_product.py
/tmp/a101_product --center 6 --prefix 2 > /tmp/a101-prefix2-d6.jsonl
python3 calculation/agent-101/check_prefix_product.py --witness /tmp/a101-prefix2-d6.jsonl
python3 calculation/neutral_band_search.py selftest
python3 tools/verify.py --changed
```

Python graph output:
```text
{"center_bound": 5, "centers": 7614, "edges": 2955526, "prefix_width": 2, "removed": 2603988, "residual": 0, "states": 2603988}
PASS exterior_trim_projections=279093 center_cases=15228 known_certificate_edges=56
PASS projected_cycle period=42 sum_g=16 sum_v=8 actual_certificate=False
```

The arithmetic suite checks every valid B of length at most 3, plus 10,000
deterministically sampled longer exteriors with neutral padding, every legal
suffix trim, every symmetric center of width at most 5, 和 the complete 56 center edges
of the eight existing Lean-source positive certificates. A separate read-only
audit exhausted B width at most 4: 130,321 words, 141,182 legal trim edges,
zero projection mismatches. AddressSanitizer 和 UndefinedBehaviorSanitizer also
passed the complete new D=5 C++ graph; LeakSanitizer was disabled 因为 this
environment blocks its process-inspection mechanism.

State-count, memory-estimate, allocation 和 runtime limits produce `UNDECIDED`
(exit 3), never `ACYCLIC`. The default budget is 1,200 seconds/4,096 MiB,
with explicit maxima 1,800 seconds/8,192 MiB. Input errors exit 2.

`python3 tools/verify.py --changed` returned **ALL CHECKS PASSED**: 5,217 Lean
files/301 projects passed the repository rules; 0 changed Lean modules 和
0 theorem endpoints required building/auditing. This is a code/report-only PR,
so that check is **不** a new Lean verification of the finite-graph result.
