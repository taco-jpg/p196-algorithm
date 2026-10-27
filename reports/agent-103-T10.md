# Agent 103 — independent low-overflow certificate audit

Task: T10.low-overflow-independent, coordination issue [#289](https://github.com/taco-jpg/p196-algorithm/issues/289).

**Status: PAPER PROOF + COMPUTED; Lean formalization remains open.**

## Result 和 attribution

Every base-10 cycle accepted by the existing `Agent120.Neutral.cycleOK` must
have total overflow **G >= 6**, independently of its period, exterior width,
center width, or permitted neutral trimming choices. The decisive finite
exclusions below were executed to exhaustion, with explicit resource statuses.
这 is a restriction on the existing certificate format. Decimal Lychrel
existence 和 unrestricted one-band impossibility remain open.

Agent 104 retains the primary G<=4 synthesis claim
([6432782889](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432782889))
和 delivery [#334](https://github.com/taco-jpg/p196-algorithm/pull/334).
Agent 103's crossed claim became this independent audit
([6432840121](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432840121)).
Credit Agent 2's period bound, Agents 2/4/8's prior exterior computations,
the existing all-length center implementation, Agent 7's padding identity,
和 Agents 107/110's prescribed/balanced trim-schedule work. The new audit
supplies an independently implemented complete B census 和 a compact
independently implemented p11 all-length center certificate.

Repository baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.

## 1. Width-independent paper reduction

Let P>0 be the checked cycle length, g_t its overflow bits, e_t its first
band carry, 和 u_t,v_t its exterior/center trims. Hyp forces the second band
carry to equal 1-e_t. The exact raw lengths give

    |B_(t+1)| = |B_t| + g_t - u_t
    |C_(t+1)| = |C_t| + g_t - 2 v_t.

Summation around the cycle yields G=sum(g)=sum(u)=2 sum(v); hence G is even.
Centers are nonempty because an empty center preserves the incoming carry.
Every raw nextC is symmetric, so closure forces symmetry at every phase.

Set x_t=B_t[0] for nonempty B_t, 和 x_t=9 for an empty exterior. There is
a bit c_t with

    g=0: x'=2x+c,     x+c<10;
    g=1: x'=(x mod 10)+1, x+c>=10.

Suffix-9 stripping preserves this effective head, including a fully erased
exterior. Empty B has e=0, g=1, nextB=[10], represented by x=9,c=1.
Thus 1<=x<=18 throughout. The integer potential, indexed by x=1,...,18,

    V = [4,3,2,2,2,1,1,1,1,1,0,0,0,0,0,0,0,0]

satisfies `1 <= 4*g + V(x)-V(x')` on each head transition (36 carry choices).
Summation proves **P<=4G**, including the exclusion G=0. 这 is a finite
potential certificate for Agent 2's previously established period bound;
`low_overflow.py` checks every inequality explicitly.

Consequently G<=4 requires either G=2 with 2<=P<=8 or G=4 with 4<=P<=16.
The lower bounds P>=G follow because each g_t is a bit. No primitive-period
assumption is used.

## 2. Exact exterior census

`b_independent.py` uses a fresh temporal column-transfer implementation.
It imports only the Python standard library 和 visits every fixed-weight
overflow necklace directly, without the 18-state head prefilter.

At a spatial cut, the state retains each time's low carry L_t, required
reverse carry H_t, 和 previous reverse digit Y_t at overflow times.
A column chooses coefficients x_t 和 inward carries h_t subject to

    floor((x_t+h_t)/10)=H_t,
    x_(t+1)=(x_t+L_t)%10 + (Y_t if g_t else (x_t+h_t)%10),
    x_P=x_0.

The next cut is L'_t=floor((x_t+L_t)/10), H'_t=h_t, 和
Y'_t=(x_t+h_t)%10 at overflow times. The outer boundary is
L=0,H=g,Y=1. A neutral suffix requires L_t+H_t=1 和 Y_t=9L_t,
where the accepted e stream equals L.

Every genuine exterior cycle embeds in this fixed-coordinate system: choose
N>max_t|B_t| 和 pad B_t with N-|B_t| neutral 9s. The new exterior trim is
u_t+(N-|B_t|)-(N-|B_(t+1)|)=g_t, so every padded phase has the same width,
positive first coefficient (also when the original B is empty), 和 a neutral
inner cut. Conversely, the audit only
needs the necessary direction: absence of an accepting cut excludes a B
cycle of every width. First-column positivity is imposed at every time.
The boundary root is separate from ordinary-column states. Arbitrary-precision
packing prevents bit truncation. Searches continue after discovering an
accepting e stream, so the final list is complete. There is no depth cutoff.

| G | P | Necklaces | Transfer-state records | Accepting g words |
|---:|---:|---:|---:|---:|
| 2 | 2–8 | 16 | 440 | 0 |
| 4 | 4–7 | 10 | 10 | 0 |
| 4 | 8 | 10 | 244794 | 0 |
| 4 | 9 | 14 | 1614 | 0 |
| 4 | 10 | 22 | 394 | 0 |
| 4 | 11 | 30 | 18202 | 1 |
| 4 | 12 | 43 | 8694 | 0 |
| 4 | 13 | 55 | 1883 | 0 |
| 4 | 14 | 73 | 121 | 0 |
| 4 | 15 | 91 | 107 | 0 |
| 4 | 16 | 116 | 13285 | 0 |
| **Total** | | **480** | **289544** | **1** |

Exact aggregate output:

    cases=480
    statuses={"EXHAUSTED":480}
    total_states=289544
    accepted=[["00001110001",{"00111010011":29}]]

The sole accepted pair rotates jointly to
`g=11100010000, e=10100110011`. Its shortest accepting width is 29;
the full graph exhausts at 18061 states 和 depth 59. The largest graph
is p8/g01010101: 244785 states, depth 88, zero accepting carries.
The p16/G4 case exhausts at 13170 states, depth 13.

An additional source-reusing C++ wrapper (`classify_b.cpp`) records explicit
EXHAUSTED/CAPPED/TIMEOUT status around the existing `bauto.cpp` transitions.
Together with `low_overflow.py`, it checks the 48 head-admissible necklaces
among the same 480, exhausts every one, 和 obtains the same sole e/g pair.
This wrapper is a scoped reproduction harness; Agent 107 retains ownership
of the general bauto completion audit. The independent Python run supplies
the second arithmetic implementation, including the 432 screened necklaces.

## 3. Arbitrary center lengths: finite independent certificate

For fixed (e,g), write P_a(C)=9^a ++ C ++ 9^a. Agent 7's exact identity is
`nextC(P_a(C))=P_a(nextC(C))`; the incoming/outgoing carries are preserved.
For any two nonnegative schedules v,w with equal sum, choose cyclic
`a_(t+1)=a_t+v_t-w_t` 和 add a common constant so every a_t>=0.
Then C'_t=P_(a_t)(C_t) satisfies the same e/g stream with trims w.
This explains why one prescribed schedule suffices for unbounded-width
existence. It does **不** preserve a specified finite width cap.
Credit Agents 107/110 for the dedicated scheduling result; here it only
supplies the coverage step for the independent center exclusion.

Choose `v=11000000000` for the sole p11 driver. Its phase widths are

    m_t=m0+(0,-1,-2,-1,-1,-1,-1,0,0,0,0),

so m0>=3. `center_layers.py` derives layer constraints directly from the
normalization equations, without importing a C automaton. Each time retains
the left incoming carry, right outgoing carry, previous right digit needed
on overflow, 和 pending next-time coefficient across a trim. Local choices
enforce symmetry, carry equations, temporal output alignment, 和 exact
odd/even midpoint matching. Every actual center cycle induces a path.

Generic frontier sizes are **1,23,93,413,637,637**, with actual **set equality
F4=F5**. Their common SHA-256 is
`4d7f37832502342f4363780c7e56ddd287c3b84e4288756c4c643b1582d2e819`.
Equality of cardinalities alone would be insufficient; the code compares sets.

| Initial width | Complete frontier sizes |
|---:|---|
| 1,2 | Invalid phase lengths |
| 3 | 1,0 |
| 4 | 1,11,0 |
| 5 | 1,23,2,0 |
| 6 | 1,23,43,0 |
| 7 | 1,23,93,10,0 |
| 8 | 1,23,93,203,0 |
| 9 | 1,23,93,413,10,0 |
| 10 | 1,23,93,413,315,0 |
| 11 | 1,23,93,413,637,10,0 |
| 12 | 1,23,93,413,637,315,0 |

Put J_t=ceil(m_t/2) 和 j0=min(J_t)-1=ceil((m0-2)/2)-1. The layers before
j0 have generic boundary type. Once initialization is complete, the generic
relation is independent of the layer index, so F4=F5 proves F_j=F4 for j>=4.
For m0>=11, j0>=4. Increasing m0 by 2 shifts every midpoint 和 j0 by one
layer, preserving the terminal boundary-type sequence. Thus widths 11 和 12
represent every larger odd/even width. Both tails become empty, completing
the all-length exclusion. The sole B stream therefore has no compatible C
cycle with one period; combined with section 2, **G<=4 is impossible**.

## 4. Reproduction 和 validation

From the repository root:

```bash
python3 calculation/neutral_band_search.py selftest
python3 calculation/agent-103/b_independent.py --seconds 600
python3 calculation/agent-103/center_layers.py
g++ -O2 -std=c++17 calculation/agent-103/classify_b.cpp -o /tmp/a103-b
python3 calculation/agent-103/low_overflow.py --solver /tmp/a103-b --weights 2 4 --budget 300
python3 tools/verify.py --changed
```

Independent B run: 27.866 seconds, peak RSS 27316 KiB, 480/480 EXHAUSTED.
The Python center solver also passes 2720 direct-enumeration comparisons
in bases 2/3 (80 positive cases) 和 four original/transported known-source
controls in bases 2/26, zero mismatches. The mirror reaccepts eight known
certificate bases. The p12 exterior positive control separately returns
the documented three e rotations 和 exhausts its graph (136653 states).

The literal repository gate completed with `ALL CHECKS PASSED`: 5217 Lean
files 和 301 registered projects passed repository rules. With calculation/report
changes only, it builds zero Lean modules 和 audits zero new endpoints;
passing that gate does **不** turn these computations into Lean theorems.

## 5. Remaining scope

G=6 remains open. P<=24 follows, but the p24 overflow word `(1000)^6`
requires complete carry-stream classification. The existing replay of a
twice-repeated p12 exterior is only one positive example: periodic g does
**不** force e or B to have the smaller period. Agent 108 owns the general
saturation-family theory. Any later G=6 audit must state its exact additional
computations 和 preserve unresolved/capped cases.

## Sources

- Exact definitions: `A120Template.lean`, `A120Certificate.lean` under
  `lean/P196/Drafts/Agent120NeutralBandCalibration/`.
- Existing search arithmetic: `calculation/neutral_band/structure/bauto.cpp`,
  `cauto_fast.cpp`; the padding-vacuum formulation already appears in
  `calculation/neutral_band/breaks/studio/ccycle_padded.py`.
- Period bound: Agent 2 [#294](https://github.com/taco-jpg/p196-algorithm/issues/294)
  和 [#309](https://github.com/taco-jpg/p196-algorithm/pull/309).
- Padding/canonicalization: Agent 7 [#315](https://github.com/taco-jpg/p196-algorithm/pull/315)
  和 [#326](https://github.com/taco-jpg/p196-algorithm/pull/326).
- Primary low-overflow claim 和 independent scope correction linked above.
