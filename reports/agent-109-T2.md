# Agent 109 — alternating overflow: neutral-tail inverse language

## Result 和 scope

**PAPER PROOF:** the exact neutral-tail predecessor fiber is parameterized by a free binary temporal trace. A constant-trace eight-edge spatial cycle disproves a direct neutral analogue of the scalar reverse-erasure lemma used in REPORT_218. Arbitrarily many predecessor columns do 不 repair 那 local argument.

**COMPUTED:** a sound finite temporal-language construction excludes periodic strips from the physical outside cut to the neutral tail through spatial depth 10, with unrestricted temporal period. Consequently an alternating-overflow decimal exterior cycle must encounter a canonically normalized exterior of length at least 11. The spatial bound is explicit.

这 does **不** exclude wider exteriors, nonalternating overflows, or decimal neutral-band certificates generally. 没有 matching center, candidate certificate, or new Lean theorem is supplied. The local spatial cycle below does 不 start at the physical outside cut 和 不是 a B cycle.

Baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`. Source relations: `lean/P196/Core/AlternatingScalarBoundary.lean`; REPORT_218 §§2.2–2.6. Agent 106 independently found the same constant-trace counterexample in issue #289 comment 6432846116; forward prefix/density consequences belong to that agreed scope. Agent 7's neutral-padding normalization is credited. The old eight-phase prefix theorem is used as a control, not claimed as a new classification.

## 1. Exterior-to-strip bridge

Let $B_t$ be a closed autonomous exterior orbit with strictly alternating overflow $g_{2j}=0,\ g_{2j+1}=1$. Let $e_t$ be the carry from normalizing $B_t$ with initial carry zero. Append an infinite neutral suffix to form $q_t=B_t9^\infty$.

Define low carries $L_t(0)=0$, $L_t(k+1)=\lfloor(q_t(k)+L_t(k))/10\rfloor$. Define high carries by $H_t(k)=1-e_t$ beyond B, then backwards by $H_t(k)=\lfloor(q_t(k)+H_t(k+1))/10\rfloor$. Put

\[
d_t(k)=(q_t(k)+L_t(k))\bmod10,\quad
r_t(k)=(q_t(k)+H_t(k+1))\bmod10.
\]

The half-infinite successor is $d_t(k)+r_t(k)$ for $g_t=0$; for $g_t=1$, its first coefficient is $d_t(0)+1$, 和 the others are $d_t(k)+r_t(k-1)$. These are exactly the mirror's `nextB` formulas followed by neutral coefficients. Legal suffix trims 都 preserve the half-infinite orbit, including an empty B.

At paired time j 和 spatial cut $k\ge1$, define

\[
X_k^j=(L_{2j}(k),L_{2j+1}(k),H_{2j}(k),
q_{2j+1}(k-1)-10H_{2j+1}(k-1)).
\]

At cut zero use $O=(0,0,0,0)$. For adjacent cuts $X,Y$, the exact `Tile` equations are

\[
\begin{gathered}
r=Y.z+10h,\quad r<9\Rightarrow h=0,\quad r>9\Rightarrow h=1,\\
Y.a=\lfloor(q+X.a)/10\rfloor,\quad
r=(q+X.a)\bmod10+(q+Y.c)\bmod10,\\
Y.b=\lfloor(r+X.b)/10\rfloor,\quad
X.c=\lfloor(q+Y.c)/10\rfloor,\\
q_+=(r+X.b)\bmod10+X.z+h,\qquad0\le X.z+h\le9.
\end{gathered}
\]

Here $q=q_{2j}(k)$, $r=q_{2j+1}(k)$, $q_+=q_{2j+2}(k)$; bits lie in $\{0,1\}$, coefficients in $[0,18]$, 和 slot z in $[-1,9]$. Temporal closure requires the next-q of each tile to equal the q of the next paired time. The implementation retains 这 equality.

### Canonical width 和 the terminal cut

Strip the entire trailing run of 9s from each B. Padding covariance preserves the half-infinite orbit. An overflowing step from a nonempty normalized B with last coefficient x satisfies:

* $e=0,\ x<9$: the raw last coefficient is $10+x>9$;
* $e=1,\ x>9$: the raw last coefficient is $x-10<9$.

For empty B, the raw successor is $[10]$. Thus an overflow emits zero canonical trim, increases normalized B length by one, 和 flips e. Maximum normalized width zero is therefore impossible in an overflowing cycle.

If K is the maximum normalized B length, odd sources in the 0/1 pairing 都 satisfy $|B|\le K-1$, while even sources 都 satisfy $|B|\le K$. Therefore cut K, including the odd coefficient at $K-1$, is already neutral. Its slot is

\[
N(a_j,b_j)=(a_j,b_j,1-a_j,10b_j-1),
\quad a_j=e_{2j},\quad b_j=e_{2j+1}.
\]

The overflow flip gives $b_j=1-a_{j+1}$. The main computation permits **the four neutral letters independently**, a larger language, so its negative result does 不 depend on enforcing 那 additional constraint. Since depths zero through 10 都 exclude a closed B orbit, K≤10 is impossible. Raw B width≤10 implies canonical width≤10 as well.

## 2. Exact neutral inverse fiber

Tiles into $N(a,b)$ 都 satisfy

\[
r=9,\ h=1-b,\ X.a=a,\ X.b=b,\quad
q=4+5(a+X.c),\quad q_+=X.z+10(1-b).
\]

Indeed the inner z coordinate leaves only r=9. The odd low-carry equation fixes X.b. Parity of the nonoverflow emission fixes X.a=a, after which the even carry equations give the displayed q.

For a prescribed periodic neutral trace satisfying the overflow flip, binary traces $c_j$ 都 give precisely one predecessor:

\[
N_j=(a_j,1-a_{j+1},1-a_j,9-10a_{j+1}),\\
X_j=(a_j,1-a_{j+1},c_j,4+5(c_{j+1}-a_{j+1})),\\
q_j=4+5(a_j+c_j),\quad r_j=9,\quad h_j=a_{j+1}.
\]

Conversely, predecessors 都 有 这 form. Validity follows directly, including

\[
X_j.z+h_j=4+5c_{j+1}-4a_{j+1}\in\{0,4,5,9\}.
\]

Hence a fixed labelled m-periodic neutral trace 有 exactly $2^m$ labelled predecessor traces. The choice $c_j=1-a_j$ is neutral; other choices may be nonneutral.

## 3. Scalar erasure fails at arbitrary predecessor depth

Take constant traces $N=(0,1,1,9)$, $X=(0,1,0,4)$, $P=(0,1,0,1)$. Then $P\to X\to N$ are exact tiles with data $(q,r,h,q_+)=(7,14,1,7)$ 和 $(4,9,0,4)$. Temporal shifts 都 preserve the nonneutral X, refuting the two-column erasure implication.

More strongly, the following eight slots form a spatial cycle of constant temporal traces:

| i | slot $S_i$ | $q=q_+$ | r | h |
|---|---|---:|---:|---:|
| 0 | (0,1,1,9) | 10 | 0 | 0 |
| 1 | (1,0,0,0) | 7 | 16 | 1 |
| 2 | (0,1,1,6) | 12 | 5 | 0 |
| 3 | (1,0,1,5) | 13 | 8 | 0 |
| 4 | (1,0,1,8) | 11 | 3 | 0 |
| 5 | (1,0,0,3) | 5 | 11 | 1 |
| 6 | (0,1,0,1) | 7 | 14 | 1 |
| 7 | (0,1,0,4) | 4 | 9 | 0 |

Row i supplies `Tile(S_i,S_(i+1 mod8),q,r,h,q)`. Repeating the spatial cycle supplies arbitrarily deep predecessors while preserving the nonneutral immediate predecessor $S_7$ of N. The outside slot O never appears. Thus 这 refutes an unanchored erasure argument, while leaving a possible obstruction using the physical root open.

## 4. Unrestricted temporal period, bounded spatial depth

A labelled directed graph represents allowed periodic temporal traces: a closed walk reads one slot label per paired time. Initially one vertex 有 loops labelled by the four neutral letters.

For each edge (s\xrightarrow{Y}t), 和 each exact tile (X\to Y) with temporal values q,(q_+), introduce

\[
(s,q)\xrightarrow{X}(t,q_+).
\]

Actual periodic predecessor strips 都 map to closed walks in 这 product. Remove edges outside directed strongly connected components; closed walks retain their entire edge sets. Quotient vertices by their stable labelled-successor partition; original closed walks 都 project to quotient closed walks. For negative results, 这 preservation is sufficient even without a converse for a specified temporal period.

At each spatial depth, restrict to edges labelled O 和 test for a directed cycle. Absence excludes O repeated forever at arbitrary positive temporal period. Repeat the product for the next depth. 这是 a spatially bounded, temporally unbounded computation; the procedure 没有 a fixed-period cutoff.

Completed free-neutral run (没有 overflow-flip restriction):

| Spatial depth | Quotient vertices | Labelled edges | Outside-only cycle |
|---:|---:|---:|---|
| 0 | 1 | 4 | absent |
| 1 | 3 | 16 | absent |
| 2 | 11 | 66 | absent |
| 3 | 37 | 282 | absent |
| 4 | 89 | 838 | absent |
| 5 | 287 | 2,956 | absent |
| 6 | 1,025 | 10,892 | absent |
| 7 | 3,929 | 43,938 | absent |
| 8 | 14,731 | 173,984 | absent |
| 9 | 55,419 | 670,848 | absent |
| 10 | 213,651 | 2,669,442 | absent |

The completed depth-10 run took 32.854 seconds, peak RSS 1,526,708 KiB, under a 2,000,000 KiB address-space limit 和 a 600-second wall limit; exit status zero. A final replay reproduced the exact graph counts in 37.327 seconds / 1,526,288 KiB. Measured resource figures depend on hardware. The extra `--flip` control also completed depth 10: 213,650 vertices / 2,669,402 edges, outside absent. The unrestricted four-letter run is the primary negative.

## 5. Reproduction 和 validation

```bash
python3 calculation/agent-109/alternating_tiles.py --counterexample
python3 calculation/agent-109/alternating_prefix_bridge.py
python3 calculation/agent-109/neutral_language.py --selftest
python3 calculation/agent-109/language_audit.py --depth 5
ulimit -v 2000000
OPENBLAS_NUM_THREADS=1 timeout 600 python3 calculation/agent-109/neutral_language.py --compact --depth 10 --cap 2000000
python3 tools/verify.py --changed
```

The compact language backend requires NumPy 和 SciPy. Exact integer edges are packed into uint64 with an explicit capacity check; strongly connected components use SciPy. The standard-library implementation supplies independent small-depth comparisons. A cap, timeout, memory failure, or incomplete depth is **UNDECIDED**, never a negative result.

The mirror bridge controls cover 16,859 B words, 67,436 padding identities, 18,233 allowed trim edges, 164,097 prefix projections, 和 79,837 paired `Tile` instances. The inverse-fiber controls check 30,948 local instances by exhaustive enumeration of binary-trace pairs of lengths 1–6. The explicit spatial cycle satisfies the complete literal `Tile` equations.

`language_audit.py` independently enumerates the 1,640 exact local tiles, checks the SCC implementation against a separately written Tarjan algorithm on 120 graphs, 和 compares unquotiented products to the quotient on 3,360 periodic-pattern queries through depth 5 (free-tail 和 flip-tail starts). Ten separately enumerated/pruned product edge sets also agree exactly with both implementation backends. The independent unreduced free graphs contain 1,3,11,55,205,817 vertices 和 4,16,66,430,1958,8844 edges at depths 0–5. Comparisons 都 pass. 这是 a separate implementation check, with its depth stated explicitly; a second campaign-agent full-depth rerun remains requested.

Repository validation checks the unchanged 5,217 Lean files / 301 registered projects, with zero changed Lean modules. The literal command returned `ALL CHECKS PASSED (changed files only, against origin/main)`. 这 does 不 provide new kernel verification of the paper argument.

## Remaining question

Does a finite periodic strip of **unbounded spatial width** connect the physical outside cut O to the neutral-tail language? The eight-edge counterexample rules out the simplest scalar-erasure route. The finite-depth exclusion does 不 answer the unrestricted question.
