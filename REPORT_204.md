# REPORT_204 — Periodic bands: exact maps 和 obstructions

Agent #204 · Direction 4 · 2026-10-22

## Answer in one paragraph

**THEOREM / outcome.** Decimal Lychrel existence remains unresolved by this work. The exact periodic carry maps yield a complete classification of anchored one-step fixed words at every spatial period, a complete classification of the nonconstant period-2 bulk cycles, 和 a finite-template obstruction: if a symmetric column word consists of at most \(r\) bands of spatial period at most 2 plus at most \(B\) other columns, then after \(m\) steps containing an overflow it admits at most \(B+(4m+1)r+m\) constant pieces. Consequently, a positive-growth return in that class cannot retain an unbounded primitive period-2 band. A separate integer-divisibility argument excludes nonconstant bulk returns of **any** spatial period when every phase uses spatially uniform carries. Explicit primitive period-3 和 period-4 bulk cycles escape that restriction through mixed carries; each was checked for 1000 bulk steps. Two finite embeddings were also checked for 1000 ordinary decimal steps, 和 both failed their proposed template returns. The remaining question concerns compatible finite interfaces, a center, positive run growth, 和 palindrome exclusion for a specified surviving bulk cycle.

## Scope 和 conventions

Here \(T\) denotes the induced map on full column-sum words. Spatial period means the length of a repeated column block; temporal period means the number of steps before that block returns. These quantities differ.

A full word \(q=(q_0,\ldots,q_{L-1})\) satisfies

\[
0\le q_i\le18,\qquad q_i=q_{L-1-i}.
\]

For ordinary positive integer realizability, also require \(q_0>0\), 和 require the middle coefficient to be even when \(L\) is odd. A realization follows by taking \(d_i=\max(0,q_i-9)\), \(d_{L-1-i}=q_i-d_i\) on the lower half, 和 half the middle coefficient at the center. The supplied verifier checks that construction against ordinary integer arithmetic.

The mathematical statements below have complete paper proofs or explicit finite carry tables. No result in this report receives a new **LEAN-VERIFIED** designation. The 1000-step checks corroborate the formulas; their scope remains finite.

## THEOREM 1 — Exact periodic block maps, including the neutral symbol

Define the carry transition

\[
C(s,c)=\left\lfloor\frac{s+c}{10}\right\rfloor,
\qquad c\in\{0,1\}.
\]

The complete carry table:

| Column \(s\) | Incoming 0: outgoing carry, digit | Incoming 1: outgoing carry, digit |
|---|---|---|
| \(0\le s\le8\) | \(0,s\) | \(0,s+1\) |
| \(s=9\) | \(0,9\) | \(1,0\) |
| \(10\le s\le18\) | \(1,s-10\) | \(1,s-9\) |

For a full word, set

\[
c_0=0,\quad c_{i+1}=C(q_i,c_i),\quad
e_i=q_i+c_i-10c_{i+1},\quad \delta=c_L.
\]

When \(\delta=1\), append \(e_L=1\). Because \(q_0>0\), the leading digit of the resulting ordinary integer never vanishes in the no-overflow case.

For a repeated block \(w=(w_i)_{i\bmod p}\), let \(a_i\) be the incoming carry in the increasing direction, 和 \(b_i\) the incoming carry in the decreasing direction. Then

\[
a_{i+1}=C(w_i,a_i),\qquad b_{i-1}=C(w_i,b_i),
\]

\[
f_i=w_i+a_i-10a_{i+1},\qquad
g_i=w_i+b_i-10b_{i-1}.
\]

If some entry differs from 9, both cyclic carry sequences exist uniquely. To determine \(a_i\), find the preceding non-9 entry in cyclic order: its type, low or high, gives 0 or 1. To determine \(b_i\), use the following non-9 entry. Every intervening 9 preserves that bit. Thus a finite periodic interval agrees with these cyclic carries after at most \(p\) positions from the corresponding boundary.

The anchored bulk maps are

\[
\boxed{F_0(w)_i=f_i+g_i},\qquad
\boxed{F_1(w)_i=f_i+g_{i-1}}. \tag{1}
\]

**Proof of the alignment.** Without overflow, output position \(i\) pairs with \(L-1-i\). Symmetry of the input identifies that reflected digit with \(g_i\), giving \(F_0\). With overflow, the new length equals \(L+1\), so position \(i\) pairs with \(L-i=L-1-(i-1)\), giving \(F_1\). At the exterior, handle the appended digit separately:

\[
q'_0=q'_L=1+(q_0\bmod10)\qquad(\delta=1).
\]

Equation (1) applies to an interior where both indicated old positions 和 their synchronized carries remain inside the band. The overflow bit comes from the entire finite word; it cannot be selected independently when constructing an ordinary orbit.

**The all-9 exception.** In a band \(9^p\), let the directional entering bits be \(A,B\). Each bit persists throughout the band, so

\[
f_i=9(1-A),\quad g_i=9(1-B),\quad
\boxed{F_\delta(9^p)=\bigl(18-9(A+B)\bigr)^p}.
\]

The four cases \((A,B)=(0,0),(0,1),(1,0),(1,1)\) give constants \(18,9,9,0\), respectively, for either overflow flag. A deterministic map on undecorated all-9 words would lose essential boundary data. ∎

## THEOREM 2 — Complete anchored fixed-point classification

For either \(F_0\) or \(F_1\), an anchored fixed periodic word containing a non-9 entry must equal \(0^p\) or \(18^p\), for arbitrary \(p\). The additional all-9 fixed state requires unequal directional entering carries.

### Proof for \(F_0\)

At a non-9 entry, let \(h_i=0\) for \(w_i\le8\), 和 \(h_i=1\) for \(w_i\ge10\). Both outgoing carries equal \(h_i\). The fixed equation gives

\[
w_i=2w_i+a_i+b_i-20h_i,
\qquad w_i=20h_i-a_i-b_i.
\]

For \(h_i=0\), nonnegativity forces \(w_i=0\) 和 \(a_i=b_i=0\). For \(h_i=1\), the bound \(w_i\le18\) forces \(w_i=18\) 和 \(a_i=b_i=1\).

At every non-9 entry, the incoming forward carry therefore equals its own type. Consecutive non-9 entries around the period must share that type: the previous non-9 entry sets the carry, 和 intervening 9s preserve it. Hence the non-9 entries share one type \(h\), with both carry sequences constantly \(h\). An entry 9 would then map to \(18\) when \(h=0\), or to \(0\) when \(h=1\), contradicting fixedness. The entire word equals \(0^p\) or \(18^p\).

### Proof for \(F_1\)

The fixed equation gives

\[
g_{i-1}=10a_{i+1}-a_i.
\]

The digit bound \(0\le g_{i-1}\le9\) excludes carry transitions \(0\to1\), which give 10, 和 \(1\to0\), which give \(-1\). Thus \(a_i\) is constant. Since a non-9 entry exists, its low/high type determines that constant \(h\); every non-9 entry has the same type, 和 the backward carries also constantly equal \(h\). Therefore

\[
F_1(w)_i=w_i+w_{i-1}-18h.
\]

Fixedness forces \(w_{i-1}=18h\) at every position. For an all-9 word, Theorem 1 gives fixedness exactly when \(A+B=1\). ∎

This classification concerns anchored one-step equality. A rotated return can occur without an anchored fixed point.

## THEOREM 3 — Spatial periods 1 和 2: complete bulk cycle analysis

### Period 1

For a constant \(s\ne9\), both clocks give

\[
f(s)=\begin{cases}2s,&0\le s\le8,\\2s-18,&10\le s\le18.\end{cases}
\]

After one step the value is even. Writing \(s=2a\) gives \(a\mapsto2a\pmod9\), with the endpoints \(a=0,9\) kept distinct. The complete cycles are

\[
(0),\quad(18),\quad(6,12),\quad(2,4,8,16,14,10).
\]

The externally decorated all-9 state can stay at 9 with opposite entering bits, or leave for 0 or 18 with equal bits.

### Period 2 carry table 和 overflow collapse

For \(w=(a,b)\ne(9,9)\), the cyclic forward 和 backward digit words coincide. Let the common word be \((x,y)\). The complete cases are:

| Condition | \(x\) | \(y\) |
|---|---:|---:|
| \(a\le8,\ b\le8\) | \(a\) | \(b\) |
| \(a\le8,\ b\ge10\) | \(a+1\) | \(b-10\) |
| \(a\ge10,\ b\le8\) | \(a-10\) | \(b+1\) |
| \(a\ge10,\ b\ge10\) | \(a-9\) | \(b-9\) |
| \(a=9,\ b\le8\) | \(9\) | \(b\) |
| \(a=9,\ b\ge10\) | \(0\) | \(b-9\) |
| \(a\le8,\ b=9\) | \(a\) | \(9\) |
| \(a\ge10,\ b=9\) | \(a-9\) | \(0\) |

When neither entry equals 9, the nearest non-9 on either side of an \(a\)-position has type \(b\), 和 conversely. When exactly one entry equals 9, both directions receive the type of the other entry. The truth table in Theorem 1 gives each displayed digit. Consequently,

\[
\boxed{F_0(a,b)=(2x,2y)},\qquad
\boxed{F_1(a,b)=(x+y,x+y)}. \tag{2}
\]

The omitted pair \((9,9)\) also maps to a constant, by its four boundary-carry cases. An overflow therefore destroys primitive spatial period 2 in the bulk. A constant subsequently stays constant under either clock, including the boundary-sensitive value 9.

### Classification of nonconstant \(F_0\) cycles

A nonconstant cycle never visits a constant word. Equation (2) therefore makes every word on such a cycle even. Write

\[
(a,b)=(2A,2B),\qquad 0\le A,B\le9,\qquad N=10A+B.
\]

Put \(u=\mathbf1_{A\ge5}\), \(v=\mathbf1_{B\ge5}\). The carry table gives

\[
A'=2A-10u+v,\qquad B'=2B-10v+u,
\]

\[
\boxed{N'=2N-99u}. \tag{3}
\]

This is doubling modulo 99, with 0 和 99 represented as separate fixed endpoints. For a nonzero residue, put \(d=99/\gcd(N,99)\); its temporal period equals \(\operatorname{ord}_d(2)\).

| \(d\) | Temporal period | Number of residues | Number of anchored cycles |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 |
| 3 | 2 | 2 | 1 |
| 9 | 6 | 6 | 1 |
| 11 | 10 | 10 | 1 |
| 33 | 10 | 20 | 2 |
| 99 | 30 | 60 | 2 |

The first row represents \(N=99\); \(N=0\) supplies the other fixed endpoint. The orders follow from \(\operatorname{ord}_3(2)=2\), \(\operatorname{ord}_9(2)=6\), \(\operatorname{ord}_{11}(2)=10\), 和 the Chinese remainder theorem. Explicitly, \(2^3\equiv-1\pmod9\), while exponents 1, 2, 3 do not give 1; \(2^5\equiv-1\pmod{11}\), while exponents 1, 2, 5 do not give 1. These checks exclude the proper divisors of the candidate orders. The orders modulo 33 和 99 are the corresponding least common multiples.

Primitive spatial period 2 means \(A\ne B\), equivalently \(11\nmid N\). Thus \(d\in\{11,33,99\}\), giving exactly **3 anchored cycles of temporal length 10 和 2 of length 30**. Representatives:

| \(N\) | Initial block | Temporal period |
|---:|---|---:|
| 1 | \((0,2)\) | 30 |
| 3 | \((0,6)\) | 10 |
| 5 | \((0,10)\) | 30 |
| 9 | \((0,18)\) | 10 |
| 15 | \((2,10)\) | 10 |

Swapping the spatial phase acts by \(N\mapsto10N\pmod{99}\). For \(d=11\), \(2^5\equiv10\), giving one quotient cycle of length 5. For \(d=33\), a hypothetical \(2^k\equiv10\) would require \(k\) odd modulo the order at 11 和 even modulo the order at 3; impossible. The spatial swap therefore exchanges the 2 anchored length-10 cycles. For \(d=99\), the same congruence would require \(k\) odd at 11 和 divisible by 6 at 9; impossible. The swap exchanges the 2 anchored length-30 cycles. The rotation quotient consequently has exactly one primitive cycle of each length **5, 10, 30**. ∎

These nonconstant cycles require clock 0 throughout. The next theorem explains why finite decimal templates cannot use them as persistent growing alternating bands.

## THEOREM 4 — Uniform finite-template obstruction for period at most 2

Suppose a symmetric finite column word is partitioned into at most \(r\) nonoverlapping intervals of spatial period at most 2, with at most \(B\) other columns. Fix \(m\ge1\). If at least one of the first \(m\) steps overflows, the final word admits a partition into at most

\[
\boxed{K=B+(4m+1)r+m}
\]

constant pieces.

**Proof.** Track each original periodic interval at its original indices, removing 2 positions from each end per step. A non-all-9 period-2 interval synchronizes each carry within 2 positions. Formula (1), including the shift by one in \(F_1\), therefore applies throughout the retained core. An all-9 interval needs no synchronization: each directional entering bit remains constant throughout it, so its retained image is constant.

Before the first overflow, each retained core has period at most 2. The first overflow makes it constant by (2) 和 the all-9 cases. A retained constant core remains constant under every later clock. This also covers a value 9 reached later: its boundary bits can change the output value, but cannot produce variation within its core.

After \(m\) steps there are at most \(r\) surviving constant cores. At most \(4mr\) original band positions were removed; a short interval with an empty core contributes no more than \(4m\) positions. The original defects contribute at most \(B\) positions. Length can increase by at most one per step, adding at most \(m\) positions. Partition each remaining uncovered position as a singleton. This gives

\[
r+4mr+B+m=K
\]

constant pieces. No assumption about independent boundary carries or a prescribed overflow itinerary was used. ∎

**Return consequence.** Consider a family with fixed \(r,B,m\), allowing its band lengths to vary without bound. If \(T^m\) returns to that family with positive total length growth, some step overflows. An alternating segment with unequal symbols changes value at every adjacent pair, so a segment of length \(N\) intersects at least \(N\) constant pieces. The output therefore cannot contain an alternating band longer than \(K\). Any claimed return that retains an unbounded primitive period-2 band is impossible. Rotating band phases, permuting bands, or varying the overflow itinerary with the parameter does not evade the bound.

**Orbit consequence.** Every 5 consecutive steps of a positive ordinary decimal orbit contain an overflow. Indeed, a no-overflow step has \(1\le q_0\le9\), 和

\[
q'_0=2q_0+c_{L-1}\ge2q_0.
\]

Five no-overflow steps would require the fifth input to have \(q_0\ge16\), impossible. The bound is sharp:

\[
10\to11\to22\to44\to88\to176.
\]

Thus if every word of an orbit admits the stated decomposition with fixed \(r,B\), every word from time 5 onward admits at most

\[
\boxed{B+21r+5}
\]

constant pieces. This reduces the period-at-most-2 class to boundedly many constant runs; it does not exclude every constant-run template. The statement concerns **column-sum** bands. Periodic digit bands can fold to constant column bands.

## THEOREM 5 — Mixed carries are necessary at every spatial period

Suppose a nonconstant periodic block follows a finite sequence of bulk maps 和 returns to its initial word up to cyclic rotation or reflection. If at least one step has clock 0, then some phase contains both a low symbol in \(\{0,\ldots,8\}\) 和 a high symbol in \(\{10,\ldots,18\}\).

**Proof.** Suppose no phase contains both types. A nonconstant block necessarily contains a non-9 entry. Its cyclic carries in both directions then constantly equal one bit \(h\): 0 when only low entries 和 9 occur, or 1 when only high entries 和 9 occur. Formula (1) becomes

\[
F_0(w)_i=2w_i-18h,\qquad
F_1(w)_i=w_i+w_{i-1}-18h.
\]

Use integer adjacent differences

\[
\Delta_i=w_i-w_{i-1}.
\]

They transform as

\[
\Delta'_i=2\Delta_i\quad(\delta=0),\qquad
\Delta'_i=\Delta_i+\Delta_{i-1}\quad(\delta=1).
\]

Let \(g=\gcd_i|\Delta_i|>0\) initially. After \(u\) no-overflow steps, every resulting difference is divisible by \(2^ug\): an overflow takes integer sums 和 preserves the existing common factor; a no-overflow supplies another factor of 2. A constant intermediate block stays constant thereafter, preventing a nonconstant return. Otherwise a rotated or reflected return has difference gcd exactly \(g\). It would imply \(2^ug\mid g\), impossible when \(u\ge1\). ∎

**Actual-clock condition.** At most 3 consecutive actual decimal steps overflow. An overflow requires \(s=q_0\ge9\), 和 the next exterior sum equals

\[
s'=1+(s\bmod10).
\]

The possibilities are \(9\to10\to1\), \(10,\ldots,17\to1,\ldots,8\), 和 \(18\to9\to10\to1\). A value below 9 cannot overflow. Therefore a repeatable finite-template return cannot use overflow at every step. The mixed-carry necessity applies to every nonconstant bulk cycle in such a return.

**Quantitative consequence.** A persistent periodic bulk whose phases use uniform carries for 20 actual steps becomes constant by the end. Every block of 4 actual steps contains a no-overflow, so there are at least 5. Each final difference is divisible by \(32g\) while its absolute value is at most 18, forcing zero. This statement requires the tracked bulk to remain outside the moving interface regions.

## THEOREM 6 — Explicit primitive period-3 和 period-4 bulk cycles

The following cycles concern the maps (1). They retain the distinction between prescribed bulk clocks 和 actual finite-word clocks. The carry tables provide a complete finite proof; the appendix also repeats every cycle for 1000 steps.

### Period 3: clock \(0001\), temporal period 4

| \(w\) | \(a\) | \(b\) | \(f\) | \(g\) | Clock | Output |
|---|---|---|---|---|---:|---|
| \((2,9,7)\) | \((0,0,0)\) | \((0,0,0)\) | \((2,9,7)\) | \((2,9,7)\) | 0 | \((4,18,14)\) |
| \((4,18,14)\) | \((1,0,1)\) | \((1,1,0)\) | \((5,8,5)\) | \((5,9,4)\) | 0 | \((10,17,9)\) |
| \((10,17,9)\) | \((1,1,1)\) | \((1,1,1)\) | \((1,8,0)\) | \((1,8,0)\) | 0 | \((2,16,0)\) |
| \((2,16,0)\) | \((0,0,1)\) | \((1,0,0)\) | \((2,6,1)\) | \((3,6,0)\) | 1 | \((2,9,7)\) |

### Period 4A: clock \(0101\), temporal period 4

| \(w\) | \(a\) | \(b\) | \(f\) | \(g\) | Clock | Output |
|---|---|---|---|---|---:|---|
| \((3,10,15,8)\) | \((0,0,1,1)\) | \((1,1,0,0)\) | \((3,0,6,9)\) | \((4,1,5,8)\) | 0 | \((7,1,11,17)\) |
| \((7,1,11,17)\) | \((1,0,0,1)\) | \((0,1,1,0)\) | \((8,1,1,8)\) | \((7,2,2,7)\) | 1 | \((15,8,3,10)\) |
| \((15,8,3,10)\) | \((1,1,0,0)\) | \((0,0,1,1)\) | \((6,9,3,0)\) | \((5,8,4,1)\) | 0 | \((11,17,7,1)\) |
| \((11,17,7,1)\) | \((0,1,1,0)\) | \((1,0,0,1)\) | \((1,8,8,1)\) | \((2,7,7,2)\) | 1 | \((3,10,15,8)\) |

Every phase avoids 9 和 contains both low 和 high entries. Its adjacent-difference gcd follows \(1\to2\to1\to2\to1\). Mixed-carry overflow steps can remove the factor gained at no-overflow steps; the uniform-carry hypothesis of Theorem 5 therefore matters.

### Period 4B: clock \((00101)^2\), temporal period 10

This cycle also avoids 9. Its complete carry bookkeeping uses

\[
a_i=\mathbf1_{w_{i-1}\ge10},\quad b_i=\mathbf1_{w_{i+1}\ge10},\quad
f_i=(w_i\bmod10)+a_i,\quad g_i=(w_i\bmod10)+b_i.
\]

| \(w\) | Clock | \(f\) | \(g\) | Output |
|---|---:|---|---|---|
| \((2,3,4,3)\) | 0 | \((2,3,4,3)\) | \((2,3,4,3)\) | \((4,6,8,6)\) |
| \((4,6,8,6)\) | 0 | \((4,6,8,6)\) | \((4,6,8,6)\) | \((8,12,16,12)\) |
| \((8,12,16,12)\) | 1 | \((9,2,7,3)\) | \((9,3,7,2)\) | \((11,11,10,10)\) |
| \((11,11,10,10)\) | 0 | \((2,2,1,1)\) | \((2,2,1,1)\) | \((4,4,2,2)\) |
| \((4,4,2,2)\) | 1 | \((4,4,2,2)\) | \((4,4,2,2)\) | \((6,8,6,4)\) |
| \((6,8,6,4)\) | 0 | \((6,8,6,4)\) | \((6,8,6,4)\) | \((12,16,12,8)\) |
| \((12,16,12,8)\) | 0 | \((2,7,3,9)\) | \((3,7,2,9)\) | \((5,14,5,18)\) |
| \((5,14,5,18)\) | 1 | \((6,4,6,8)\) | \((6,4,6,8)\) | \((14,10,10,14)\) |
| \((14,10,10,14)\) | 0 | \((5,1,1,5)\) | \((5,1,1,5)\) | \((10,2,2,10)\) |
| \((10,2,2,10)\) | 1 | \((1,3,2,0)\) | \((0,2,3,1)\) | \((2,3,4,3)\) |

In each table, compute the output by adding corresponding entries for clock 0, or \(f_i+g_{i-1}\) for clock 1. The displayed input blocks are distinct within the anchored cycle, 和 each has the stated primitive spatial period. These tables establish the claimed temporal periods. They do not classify every period-3 or period-4 cycle.

## THEOREM 7 — Necessary width accounting for a full template return

Consider

\[
Q_k=B\,w^k\,H\,(w^{\mathrm{rev}})^k\,B^{\mathrm{rev}},
\]

with fixed \(B,H,w\), \(|w|=p\). Suppose an actual return satisfies \(T^m(Q_k)=Q_{k+d}\). Every step adds exactly its overflow bit to length, while \(Q_{k+d}\) has \(2pd\) additional positions. Therefore

\[
\boxed{\sum_{t=0}^{m-1}\delta_t=2pd}. \tag{4}
\]

For the displayed bulk cycles, this gives the following first positive count-compatible anchored schedules, when only whole repetitions of that bulk cycle are used:

| Bulk cycle | Overflows per bulk return | Spatial period | First count-compatible schedule for \(d=1\) |
|---|---:|---:|---|
| Period 3 | 1 per 4 steps | 3 | 24 steps, clock \((0001)^6\) |
| Period 4A | 2 per 4 steps | 4 | 16 steps, clock \((0101)^4\) |
| Period 4B | 4 per 10 steps | 4 | 20 steps, clock \((00101)^4\) |

This excludes interpreting either four-step bulk cycle as a four-step positive-growth return of this fixed-interface family. Satisfying (4) still supplies no interface return or palindrome exclusion. ∎

## THEOREM 8 — Explicit failures of lifting bulk cycles to integer constructions

### A bulk cycle can coexist with an immediate palindrome

The nonpalindromic integer 21110 has column word \(2^5\), whose bulk symbol lies on the six-cycle from Theorem 3. Nevertheless,

\[
21110+1112=22222.
\]

Its first output is palindromic. Thus bulk periodicity alone does not imply palindrome avoidance.

### Two direct finite embeddings fail their proposed returns

For each row below, use \(H\) empty 和 \(k=4\) in the preceding template. The deterministic realization from the scope section gives the displayed seed. The exact full-word update, checked against ordinary integer addition at every step, gives:

| Attempt | \(B\) | \(w\) | Proposed return | Actual result |
|---|---|---|---|---|
| Period 3 | \((1,5,10,10)\) | \((2,9,7)\) | \(T^{24}Q_4=Q_5\) | Both widths 38; words differ |
| Period 4A | \((8,11,10)\) | \((3,10,15,8)\) | \(T^{16}Q_4=Q_5\) | Actual width 45; required width 46 |

The respective seeds are

```text
15992972972972970000000000001100
89939983998399839980610061006100610120
```

Each was continued for 1000 ordinary steps. The first clock mismatch occurs at step 32 for Period 3 和 step 14 for Period 4A, with steps numbered from 1. No palindrome appeared in those 1000 steps; that finite observation supplies no all-time claim. In particular, the Period-3 test demonstrates that correct width accounting 和 the intended first 24 clocks can still coexist with a failed interface return.

These are counterexamples to the two specific proposed equalities at \(k=4\). They do not exclude other interfaces, larger thresholds, or the bulk cycles themselves. The full reproducible code 和 output follow.

## Existing repository context 和 source boundary

The existing period-4 framework already defines exact guarded bulk updates 和 a boundary-sensitive all-9 case. The source for `phaseCatalog` explicitly retains a 59-word catalog, with the initial word \([14,14,4,4]\); it does not claim an exhaustive classification of arbitrary period-4 words. This report uses independent paper derivations 和 the general-period gcd argument, 和 does not relabel those existing results as newly formalized work.

Sources opened at repository snapshot `c6902ac6c366ce018e68a810f58b400dda07145a`:

- [Agent1PeriodicDigits.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Foundations/Agent1PeriodicDigits.lean): finite repeated-block normalization 和 carry stabilization.
- [Agent1PeriodicPhase.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Foundations/Agent1PeriodicPhase.lean): boundary-independent non-9 phase map with the actual overflow bit retained.
- [Agent1PeriodicPhaseCatalog.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent1PeriodicPhaseCatalog/Agent1PeriodicPhaseCatalog.lean): retained catalog 和 labeled edges.
- [RESULTS.md, periodic section](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/RESULTS.md#periodic-repeated-block-words-and-their-quotient-dynamics): existing result scopes.

## IDEA — Sharpest remaining question

For \(w=(2,3,4,3)\), do there exist finite blocks \(B,H\) 和 \(k_0\), with \(H=H^{\mathrm{rev}}\) 和 ordinary realizability of \(Q_k\), such that for every \(k\ge k_0\),

\[
\boxed{T^{20}(Q_k)=Q_{k+1}},
\]

the actual overflow word equals \((00101)^4\), 和 the normalized output at each of the 20 intermediate steps is nonpalindromic?

The bulk already returns, the width increment agrees, 和 mixed carries evade Theorem 5. The unresolved obligations are the exact finite interface return, the center, 和 the palindrome condition at every intermediate step. A positive answer with full carry verification would supply a decimal Lychrel construction. No evidence here establishes that answer.

## Reproducible verification appendix

Save the following self-contained block as `verify_report_204.py`, then run `python3 verify_report_204.py`. It checks 1444 bounded local carry cases, 9 modulo-99 cycle representatives for 1000 steps each, the 3 displayed bulk cycles for 1000 steps each, 和 2 finite embeddings for 1000 ordinary steps each. It also continues the immediate-palindrome counterexample for 1000 steps. No search over integer seeds occurs.

```python
#!/usr/bin/env python3
"""Small exact checks for REPORT_204; no integer-seed search."""
from itertools import product
from math import gcd


def cyclic_data(w):
    p = len(w)
    assert p and all(0 <= x <= 18 for x in w)
    assert any(x != 9 for x in w)
    a, b = [], []
    for i in range(p):
        j = (i - 1) % p
        while w[j] == 9:
            j = (j - 1) % p
        a.append(int(w[j] >= 10))
        j = (i + 1) % p
        while w[j] == 9:
            j = (j + 1) % p
        b.append(int(w[j] >= 10))
    f = tuple(w[i] + a[i] - 10 * a[(i + 1) % p]
              for i in range(p))
    g = tuple(w[i] + b[i] - 10 * b[(i - 1) % p]
              for i in range(p))
    assert all(0 <= x <= 9 for x in f + g)
    return tuple(a), tuple(b), f, g


def bulk(w, delta):
    _, _, f, g = cyclic_data(w)
    return tuple(f[i] + g[(i - delta) % len(w)]
                 for i in range(len(w)))


def local(q, left, right):
    n = len(q)
    a, b = [left] + [0] * n, [0] * n + [right]
    for i in range(n):
        a[i + 1] = (q[i] + a[i]) // 10
    for i in range(n - 1, -1, -1):
        b[i] = (q[i] + b[i + 1]) // 10
    u = [q[i] + a[i] - 10 * a[i + 1] for i in range(n)]
    v = [q[i] + b[i + 1] - 10 * b[i] for i in range(n)]
    return ([u[i] + v[i] for i in range(n)],
            [None] + [u[i] + v[i - 1] for i in range(1, n)])


def normalize(q):
    c, digits = 0, []
    for x in q:
        c, d = divmod(x + c, 10)
        digits.append(d)
    delta = c
    if c:
        digits.append(c)
    return tuple(digits), delta


def fold(d):
    return tuple(x + y for x, y in zip(d, reversed(d)))


def column_step(q):
    d, delta = normalize(q)
    return fold(d), delta


def realize(q):
    assert q == q[::-1] and q[0] > 0
    d, n = [0] * len(q), len(q)
    for i in range(n // 2):
        d[i] = max(0, q[i] - 9)
        d[n - 1 - i] = q[i] - d[i]
    if n % 2:
        assert q[n // 2] % 2 == 0
        d[n // 2] = q[n // 2] // 2
    assert d[-1] > 0 and fold(d) == q
    return int(''.join(map(str, reversed(d))))


def digits(n):
    return tuple(map(int, reversed(str(n))))


def diff_gcd(w):
    out = 0
    for i in range(len(w)):
        out = gcd(out, abs(w[i] - w[i - 1]))
    return out


def check_local():
    count = 0
    for x, y, left, right in product(range(19), range(19), range(2), range(2)):
        f0, f1 = local([x, y] * 8, left, right)
        z0, z1 = f0[2:-2], f1[2:-2]
        assert all(z0[i] == z0[i + 2] for i in range(len(z0) - 2))
        assert len(set(z1)) == 1
        count += 1
    print(f'PERIOD2_BOUNDARY_CASES={count} PASS')


def check_mod99():
    representatives = [(0, 1), (1, 30), (3, 10), (5, 30), (9, 10),
                       (11, 6), (15, 10), (33, 2), (99, 1)]
    for seed, period in representatives:
        n = seed
        start = w = (2 * (n // 10), 2 * (n % 10))
        first = None
        for t in range(1, 1001):
            w = bulk(w, 0)
            n = 2 * n - 99 * int(n >= 50)
            assert w == (2 * (n // 10), 2 * (n % 10))
            if w == start and first is None:
                first = t
        assert first == period
        print(f'MOD99 N={seed:02d} period={period} steps=1000 endpoint={n:02d} PASS')


CASES = [
    ('P3', (2, 9, 7), (0, 0, 0, 1), 4),
    ('P4A', (3, 10, 15, 8), (0, 1, 0, 1), 4),
    ('P4B', (2, 3, 4, 3), (0, 0, 1, 0, 1), 10),
]


def check_bulk_cycles():
    for name, seed, clocks, period in CASES:
        w, first = seed, None
        for t in range(1, 1001):
            w = bulk(w, clocks[(t - 1) % len(clocks)])
            if w == seed and t % len(clocks) == 0 and first is None:
                first = t
        assert w == seed and first == period
        print(f'{name} BULK steps=1000 exact_clocked_period={period} endpoint={w} PASS')


def template(B, w, k):
    half = B + w * k
    return half + half[::-1]


def check_finite_attempts():
    cases = [
        ('P3', (1, 5, 10, 10), (2, 9, 7), (0, 0, 0, 1), 24),
        ('P4A', (8, 11, 10), (3, 10, 15, 8), (0, 1), 16),
    ]
    for name, B, w, clocks, return_time in cases:
        q = template(B, w, 4)
        n = seed = realize(q)
        first_bad_clock = first_palindrome = None
        clock_log = []
        returned = None
        length_at_return = None
        for t in range(1, 1001):
            next_q, delta = column_step(q)
            target_digits, _ = normalize(q)
            n = n + int(str(n)[::-1])
            assert digits(n) == target_digits
            assert fold(digits(n)) == next_q
            q = next_q
            clock_log.append(delta)
            if delta != clocks[(t - 1) % len(clocks)] and first_bad_clock is None:
                first_bad_clock = t
            if str(n) == str(n)[::-1] and first_palindrome is None:
                first_palindrome = t
            if t == return_time:
                returned = q == template(B, w, 5)
                length_at_return = len(q)
        assert returned is False
        print(f'{name} FINITE seed={seed}')
        print(f'  steps=1000 first_clock_mismatch={first_bad_clock}'
              f' first_palindrome={first_palindrome} final_length={len(q)}')
        print(f'  first32_clocks={"".join(map(str, clock_log[:32]))}')
        print(f'  return_t={return_time} actual_length={length_at_return}'
              f' required_length={len(template(B, w, 5))} exact_return={returned}')


def check_counterexample():
    n = 21110
    assert fold(digits(n)) == (2,) * 5
    m = n + int(str(n)[::-1])
    assert m == 22222 and str(m) == str(m)[::-1]
    first = m
    for _ in range(999):
        m += int(str(m)[::-1])
    print(f'COUNTEREXAMPLE seed={n} first_output={first}'
          f' first_palindrome=1 steps=1000 final_length={len(str(m))}')


if __name__ == '__main__':
    check_local()
    check_mod99()
    check_bulk_cycles()
    check_finite_attempts()
    check_counterexample()
    print('ALL_REPORT_204_CHECKS_PASSED')
```

### Executed output

```text
PERIOD2_BOUNDARY_CASES=1444 PASS
MOD99 N=00 period=1 steps=1000 endpoint=00 PASS
MOD99 N=01 period=30 steps=1000 endpoint=34 PASS
MOD99 N=03 period=10 steps=1000 endpoint=03 PASS
MOD99 N=05 period=30 steps=1000 endpoint=71 PASS
MOD99 N=09 period=10 steps=1000 endpoint=09 PASS
MOD99 N=11 period=6 steps=1000 endpoint=77 PASS
MOD99 N=15 period=10 steps=1000 endpoint=15 PASS
MOD99 N=33 period=2 steps=1000 endpoint=33 PASS
MOD99 N=99 period=1 steps=1000 endpoint=99 PASS
P3 BULK steps=1000 exact_clocked_period=4 endpoint=(2, 9, 7) PASS
P4A BULK steps=1000 exact_clocked_period=4 endpoint=(3, 10, 15, 8) PASS
P4B BULK steps=1000 exact_clocked_period=10 endpoint=(2, 3, 4, 3) PASS
P3 FINITE seed=15992972972972970000000000001100
  steps=1000 first_clock_mismatch=32 first_palindrome=None final_length=434
  first32_clocks=00010001000100010001000100010000
  return_t=24 actual_length=38 required_length=38 exact_return=False
P4A FINITE seed=89939983998399839980610061006100610120
  steps=1000 first_clock_mismatch=14 first_palindrome=None final_length=452
  first32_clocks=01010101010100101010100101010100
  return_t=16 actual_length=45 required_length=46 exact_return=False
COUNTEREXAMPLE seed=21110 first_output=22222 first_palindrome=1 steps=1000 final_length=434
ALL_REPORT_204_CHECKS_PASSED
```
