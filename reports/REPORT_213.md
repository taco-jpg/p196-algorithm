# REPORT_213 — Known-base constructions 和 exact center rigidity

Agent: **213**. Direction: **3**. Date: **2026-10-22**.

## Answer in one paragraph

**THEOREM:** The displayed David Seal constructions in bases \(11,17,26\) admit complete finite carry proofs: their return periods equal \(6,6,4\), respectively, each return increases both complementary digit-run lengths by one, 和 every intermediate phase avoids palindromes. Their unbounded column-sum bands equal \(b-1\), so their common mechanism remains arithmetically available at the decimal value \(q=9\). **THEOREM:** The particular four-phase center itinerary underlying the base-\(26\) example, with center lengths \(4,4,5,5\), specified alignment changes, 和 carry words `01001`, `10110`, `011111`, `110000`, forces \(b=26\), even when its center digits vary; consequently base \(10\) cannot realize that itinerary. **LEAN-VERIFIED:** Explicit neutral certificates establish Lychrel template values 和 concrete seeds in bases \(11,17,26\); separate formal theorems establish the center-equation rigidity 和 its decimal contradiction. Each reconstructed family 和 each exact formal seed passes \(1000\) consecutive reverse-add steps, with an independent integer-arithmetic cross-check at each step. The opened original source explicitly omits its base-\(20\) witness, so its proof remains a reconstruction gap here. Decimal existence remains unresolved; the delivered obstruction excludes one precisely defined center itinerary, while the report identifies the existing neutral-band certificate framework as the appropriate setting for further work.

## 1. Sources opened 和 attribution

The starting strings come from David Seal's January 1996 announcement; the representative phase tables appear in the MathPages transcription [S2]. The proofs, complete carry transcripts, symbolic checker, 和 restricted center elimination below were reconstructed in this task.

1. **[S1]** [David Seal, original `rec.puzzles` post, 16 January 1996](https://groups.google.com/g/rec.puzzles/c/QFHJ2AJq4gw). The relevant post gives the starting strings, return periods, a transcription qualification, 和 the omission of the base-\(20\) string.
2. **[S2]** [MathPages, David Seal transcript 和 representative phase tables](https://www.mathpages.com/home/dseal.htm). The tables supply every displayed phase for bases \(11,17,26\).
3. **[S3]** [Fuller reproduction of Seal's announcement](https://www.p196.org/html/papers1.html). Its base-\(20\) paragraph gives only a size statement, \(>200\) digits; it withholds the digits 和 phase table.
4. **[S4]** [2016 announcement of *Search for and classification of Lychrel numbers*](https://www.p196.creationeer.co.uk/html/news.html), linking [the public research archive](https://www.p196.creationeer.co.uk/files/lychrel842.zip). The archive was downloaded, 和 its `ReverseAndAdd-ver3.tex` source was opened directly. Its introduction 和 implementation section reconstruct examples in bases \(11,26\), but leave unspecified the missing base-\(20\) witness. The source explicitly releases its contents into the public domain. Its search program was **never run** for this task.

The mathematical existence claims established below rely on the complete carry identities, rather than on the announcement's authority. No claim of historical novelty accompanies these known-base examples. The restricted center-rigidity result concerns the specified equations only; historical priority for that observation remains unassessed.

## 2. THEOREM — exact neutral-band reduction

### Notation

Digit words in the displayed templates run **most significant first**. Symbols follow `0,...,9,A=10,B=11,...,P=25`. A superscript on a digit denotes repetition, including the empty word at exponent zero. The superscript \(R\) denotes word reversal. Put

\[
T_b(N)=N+\operatorname{rev}_b(N).
\]

Carry calculations run **least significant first**. For a word of length \(L\),

\[
c_0=0,\qquad q_i=d_i+d_{L-1-i},\qquad
q_i+c_i=e_i+b c_{i+1},\qquad 0\le e_i<b.
\]

Since \(0\le q_i\le2b-2\), induction gives \(c_i\in\{0,1\}\). The final carry contributes a leading `1` exactly when \(c_L=1\). Leading zeros in the reversed summand cause no change to this arithmetic.

### Statement 和 proof

For any \(b\ge2\), a column sum \(q=b-1\) transmits its entering carry unchanged:

\[
\begin{array}{c|c|c|c}
q&c_i&e_i&c_{i+1}\\\hline
b-1&0&b-1&0\\
b-1&1&0&1
\end{array}
\]

The first row follows from \((b-1)+0=(b-1)+b\cdot0\). The second follows from \((b-1)+1=0+b\cdot1\). Repeated application proves the assertion for any run length. An empty run transmits the carry by the definition of concatenation.

Now take

\[
W_j(n)=A_jx_j^nM_jy_j^nZ_j,
\qquad |A_j|=|Z_j|,\qquad x_j+y_j=b-1.
\]

Reflection pairs each position of the left run with a position of the right run. The complete column-sum word therefore splits, from the units end, into

\[
\operatorname{zipAdd}(Z_j^R,A_j),\quad
(b-1)^n,\quad
\operatorname{zipAdd}(M_j^R,M_j),\quad
(b-1)^n,\quad
\operatorname{zipAdd}(A_j^R,Z_j).
\]

Consequently only the three fixed blocks require finite arithmetic. The previous fixed block's exit carry passes unchanged through the intervening neutral run into the next fixed block. This accounts for every fixed digit, every run digit, every boundary, the center, 和 the final overflow. The number of arithmetic cases remains independent of \(n\).

For the actual examples, \(\{x_j,y_j\}=\{0,b-1\}\). The long digit runs differ; each long **column-sum** run equals \(b-1\). Confusing these representations would conceal the carry mechanism.

## 3. THEOREM — complete base-26 construction

Put

\[
U=\texttt{1N5ELA6C},\quad V=\texttt{0D59ME5N},\quad
X=\texttt{P2KB4FJD},\quad Y=\texttt{CJG5AK2O}.
\]

For \(n\ge0\), define

\[
\begin{aligned}
A_n&=U\,\texttt{P}^{n}\,\texttt{P6E7}\,\texttt{0}^{n}\,V,\\
B_n&=X\,\texttt{0}^{n}\,\texttt{6KL6}\,\texttt{P}^{n}\,Y,\\
C_n&=U\,\texttt{P}^{n}\,\texttt{PDGFD}\,\texttt{0}^{n}\,V,\\
D_n&=X\,\texttt{0}^{n}\,\texttt{D373C}\,\texttt{P}^{n}\,Y.
\end{aligned}
\]

Then

\[
A_n\longmapsto B_n\longmapsto C_n\longmapsto D_n\longmapsto A_{n+1}.
\]

### Every finite carry column

In this table, column sums, carries, 和 output digits run **least significant first**. A carry string includes its entry carry 和 its exit carry. Each column asserts \(q_i+c_i=e_i+26c_{i+1}\).

| Block | Column sums | Complete carry word | Output digits |
|---|---|---|---|
| \(Q\) | \(24,28,19,36,30,15,19,12\) | `001011000` | `O2KA5GJC` |
| \(Q^R\) | \(12,19,15,30,36,19,28,24\) | `100011010` | `DJF4BK2P` |
| \(R\) | \(49,4,40,21,9,31,38,25\) | `010100111` | `N5EM95D0` |
| \(R^R\) | \(25,38,31,9,21,40,4,49\) | `001100101` | `PC6ALE5N` |
| Center of \(A_n\) | \(32,20,20,32\) | `01001` | `6LK6` |
| Center of \(B_n\) | \(12,41,41,12\) | `10110` | `DFGD` |
| Center of \(C_n\) | \(38,28,32,28,38\) | `011111` | `C373D` |
| Center of \(D_n\) | \(25,6,14,6,25\) | `110000` | `07E6P` |

The four complete column-sum words, from the units end, follow:

| Phase | Complete column-sum word | Carries entering its five blocks | Final carry |
|---|---|---|---:|
| \(A_n\) | \(Q\,25^n\,(32,20,20,32)\,25^n\,Q^R\) | \(0,0,0,1,1\) | 0 |
| \(B_n\) | \(R\,25^n\,(12,41,41,12)\,25^n\,R^R\) | \(0,1,1,0,0\) | 1 |
| \(C_n\) | \(Q\,25^n\,(38,28,32,28,38)\,25^n\,Q^R\) | \(0,0,0,1,1\) | 0 |
| \(D_n\) | \(R\,25^n\,(25,6,14,6,25)\,25^n\,R^R\) | \(0,1,1,0,0\) | 1 |

The neutral-run identities from Section 2 supply every omitted run column.

**Phase \(A_n\).** Concatenation gives the units-first output

\[
\texttt{O2KA5GJC}\,\texttt{P}^{n}\,\texttt{6LK6}\,
\texttt{0}^{n}\,\texttt{DJF4BK2P}.
\]

The final carry equals zero. Reversal gives \(B_n\).

**Phase \(B_n\).** Before the overflow, the units-first output equals

\[
\texttt{N5EM95D0}\,\texttt{0}^{n}\,\texttt{DFGD}\,
\texttt{P}^{n}\,\texttt{PC6ALE5N}.
\]

Including the final `1` 和 reversing yields

\[
U\,\texttt{P}\,\texttt{P}^{n}\,\texttt{DGFD}\,\texttt{0}^{n}V
=U\,\texttt{P}^{n}\,\texttt{PDGFD}\,\texttt{0}^{n}V=C_n.
\]

**Phase \(C_n\).** The units-first output equals

\[
\texttt{O2KA5GJC}\,\texttt{P}^{n}\,\texttt{C373D}\,
\texttt{0}^{n}\,\texttt{DJF4BK2P}.
\]

The final carry equals zero. Reversal gives \(D_n\).

**Phase \(D_n\).** Before the overflow, the units-first output equals

\[
\texttt{N5EM95D0}\,\texttt{0}^{n}\,\texttt{07E6P}\,
\texttt{P}^{n}\,\texttt{PC6ALE5N}.
\]

Including the final `1` 和 reversing yields

\[
U\,\texttt{P}\,\texttt{P}^{n}\,\texttt{P6E70}\,\texttt{0}^{n}V
=U\,\texttt{P}^{n+1}\,\texttt{P6E7}\,\texttt{0}^{n+1}V=A_{n+1}.
\]

Thus the overflow supplies the additional left-run digit, while the center supplies the additional right-run digit. These equalities remain valid at \(n=0\).

Every displayed digit belongs to \(\{0,\ldots,25\}\). Each leading digit differs from zero. The first 和 last digits of \(A_n,C_n\) equal \(1,23\); those of \(B_n,D_n\) equal \(25,24\). Hence every phase avoids palindromes. Induction over complete cycles 和 their four possible phases proves the Lychrel property of each \(A_n\). This establishes the theorem.

## 4. THEOREM — base-11 和 base-17 reconstructions

For these longer examples, the complete phase definitions appear as the literal tuples `P11` 和 `P17` in Appendix A. Each tuple means exactly \((A_j,x_j,M_j,y_j,Z_j)\) in the notation of Section 2. Appendix B supplies **every** finite column sum, complete carry string, emitted digit, 和 symbolic output for each phase; no different middle-block case has been suppressed.

For either \(b=11\) or \(b=17\), these definitions satisfy

\[
T_b(W_j(n))=W_{j+1}(n)\quad(0\le j<5),\qquad
T_b(W_5(n))=W_0(n+1),\qquad n\ge0.
\]

### Complete control data

The triple in the last column consists of the carry after the right fixed block, the carry after the center, 和 the terminal carry after the left fixed block. Those values determine the output runs through Section 2.

| Base | Phase | Outer block length | Center length | Carry triple |
|---:|---:|---:|---:|---|
| 11 | 0 | 7 | 42 | \((0,1,0)\) |
| 11 | 1 | 7 | 42 | \((1,0,0)\) |
| 11 | 2 | 7 | 42 | \((1,0,1)\) |
| 11 | 3 | 7 | 43 | \((0,1,0)\) |
| 11 | 4 | 7 | 43 | \((1,0,0)\) |
| 11 | 5 | 7 | 43 | \((1,0,1)\) |
| 17 | 0 | 29 | 20 | \((1,0,1)\) |
| 17 | 1 | 29 | 21 | \((0,1,0)\) |
| 17 | 2 | 29 | 21 | \((0,1,0)\) |
| 17 | 3 | 29 | 21 | \((0,1,0)\) |
| 17 | 4 | 29 | 21 | \((0,1,0)\) |
| 17 | 5 | 29 | 21 | \((0,1,1)\) |

### Proof of the exact returns

For every row, the full fixed-block transcript in Appendix B satisfies \(q_i+c_i=e_i+bc_{i+1}\), with valid base digits 和 the displayed entering carries. Section 2 extends those finite calculations through arbitrary run lengths. The transcript's `symbolic_output` tuple gives \((\text{overflow},A,x,M,y,Z)\), meaning the full word \(\text{overflow}\,A x^n M y^n Z\).

In base \(11\), phases \(0,1,3,4\) produce the next tuple directly. Phase \(2\) produces the prefix `1` followed by `246277A`, hence `1246277A`; the extra `A` moves across the adjacent `A` run to become the first digit of phase \(3\)'s center. Phase \(5\) produces that prefix again, while its center equals phase \(0\)'s center followed by `0`. Absorbing those adjacent digits increases both run lengths by one.

In base \(17\), phases \(1,2,3,4\) produce their next tuples directly. Phase \(0\) produces the prefix `1` followed by `0025F52C00F41AFCFDB0AC544020G`; its extra final `G` moves across the adjacent `G` run into the front of phase \(1\)'s center. Phase \(5\) produces phase \(0\)'s prefix followed by `0`, while its center equals phase \(0\)'s center followed by `G`. Absorbing those digits increases the left `0` run 和 right `G` run by one.

These word identities prove the recurrence for arbitrary \(n\). The `canonical` routine in Appendix A checks exactly this regrouping: it moves adjacent equal digits from a fixed block into its symbolic run, storing the added count as an integer offset. Equality of the resulting fixed words, run symbols, 和 offsets proves equality for every \(n\), including zero. The symbolic word equality supplies the infinite quantifier directly.

### Permanent palindrome exclusions

Positions in this table count from the left, starting at zero. The compared right-hand digit occupies the mirrored position in the right fixed block.

| Base | Phase | Position | Left digit | Mirrored right digit |
|---:|---:|---:|---|---|
| 11 | 0 | 0 | `1` | `2` |
| 11 | 1 | 4 | `A` | `9` |
| 11 | 2 | 0 | `7` | `6` |
| 11 | 3 | 0 | `1` | `2` |
| 11 | 4 | 4 | `A` | `9` |
| 11 | 5 | 0 | `7` | `6` |
| 17 | 0 | 0 | `1` | `G` |
| 17 | 1 | 0 | `1` | `0` |
| 17 | 2 | 3 | `8` | `7` |
| 17 | 3 | 5 | `6` | `5` |
| 17 | 4 | 2 | `9` | `8` |
| 17 | 5 | 1 | `9` | `8` |

Each mismatch lies inside fixed outer blocks, so it persists independently of \(n\). The phase recurrence therefore establishes an infinite orbit avoiding palindromes in each base. This completes both proofs.

## 5. THEOREM — the selected center itinerary forces base 26

This theorem permits different outer guards 和 variable center digits. Its restrictions concern **the specified center lengths, carry words, 和 alignment operations**. Other itineraries remain outside its scope.

Let \(b\ge2\), set \(p=b-1\), 和 choose base-\(b\) digits \(a,c,d\). For an MSB-first center \(W\), let \(E_b(W,\epsilon)\) denote the **LSD-first** output of adding that center to its reversal with entry carry \(\epsilon\), retaining exactly \(|W|\) output digits.

Assume

\[
\begin{aligned}
W_0&=[p,a,c,d],\\
W_1&=E_b(W_0,0)^R,\\
W_2&=[p]E_b(W_1,1)^R,\\
W_3&=E_b(W_2,0)^R,\\
E_b(W_3,1)^R&=W_0[0].
\end{aligned}
\]

The center lengths equal \(4,4,5,5\). Assume their complete carry words, from the units end, equal

\[
01001,\quad10110,\quad011111,\quad110000.
\]

The first bit gives the entry carry; the last bit gives the exit carry. The inserted leading \(p\) 和 absorbed terminal zero encode the exact boundary regrouping in Section 3. Equal exterior lengths on both sides keep each center aligned with its reversal.

Then

\[
\boxed{b=26,\qquad a=6,\qquad c=14,\qquad d=7.}
\]

### Complete center bookkeeping

Write \(s=a+c\). For phase zero:

| \(i\) | \(q_i\) | \(c_i\) | \(e_i\) | \(c_{i+1}\) |
|---:|---|---:|---|---:|
| 0 | \(b-1+d\) | 0 | \(d-1\) | 1 |
| 1 | \(s\) | 1 | \(s+1\) | 0 |
| 2 | \(s\) | 0 | \(s\) | 0 |
| 3 | \(b-1+d\) | 0 | \(d-1\) | 1 |

Hence \(W_1=[d-1,s,s+1,d-1]\). For phase one:

| \(i\) | \(q_i\) | \(c_i\) | \(e_i\) | \(c_{i+1}\) |
|---:|---|---:|---|---:|
| 0 | \(2d-2\) | 1 | \(2d-1\) | 0 |
| 1 | \(2s+1\) | 0 | \(2s+1-b\) | 1 |
| 2 | \(2s+1\) | 1 | \(2s+2-b\) | 1 |
| 3 | \(2d-2\) | 1 | \(2d-1\) | 0 |

After the prescribed leading \(p\),

\[
W_2=[p,2d-1,2s+2-b,2s+1-b,2d-1].
\]

Define \(h=2d+2s-2b+1\) 和 \(k=4s+5-3b\). For phase \(2\):

| \(i\) | \(q_i\) | \(c_i\) | \(e_i\) | \(c_{i+1}\) |
|---:|---|---:|---|---:|
| 0 | \(b+2d-2\) | 0 | \(2d-2\) | 1 |
| 1 | \(2d+2s-b\) | 1 | \(h\) | 1 |
| 2 | \(4s+4-2b\) | 1 | \(k\) | 1 |
| 3 | \(2d+2s-b\) | 1 | \(h\) | 1 |
| 4 | \(b+2d-2\) | 1 | \(2d-1\) | 1 |

Therefore \(W_3=[2d-1,h,k,h,2d-2]\). For phase three:

| \(i\) | \(q_i\) | \(c_i\) | \(e_i\) | \(c_{i+1}\) |
|---:|---|---:|---|---:|
| 0 | \(4d-3\) | 1 | \(4d-2-b\) | 1 |
| 1 | \(2h\) | 1 | \(2h+1\) | 0 |
| 2 | \(2k\) | 0 | \(2k\) | 0 |
| 3 | \(2h\) | 0 | \(2h\) | 0 |
| 4 | \(4d-3\) | 0 | \(4d-3\) | 0 |

The return requires this output to equal \([0,d,c,a,p]\). Equating columns gives

\[
4d=b+2,\qquad d=2h+1,\qquad c=2k,\qquad a=2h,
\]

with the final-column equation \(4d-3=b-1\) equivalent to the first.

It follows that

\[
d=a+1,\qquad b=4a+2.
\]

Substitute these expressions into the defining equations for \(h,k\). Eliminating \(h,k\) gives

\[
4c-9a=2,\qquad 7c-16a=2.
\]

Multiply the first equation by \(7\), the second by \(4\), 和 subtract:

\[
(28c-63a)-(28c-64a)=14-8,
\qquad a=6.
\]

Thus \(c=14,d=7,b=26\). Conversely, these values yield

\[
p=25,\quad s=20,\quad h=3,\quad k=7,
\]

和 the four center words `P6E7`, `6KL6`, `PDGFD`, `D373C`. Section 3 checks every digit bound 和 carry at these values. This completes the proof.

### Exact decimal contradiction

At \(b=10\), the necessary equations force \(a=2,d=3\). Then \(4c-9a=2\) forces \(c=5\), while

\[
7c-16a=35-32=3\ne2.
\]

Thus **this center itinerary cannot occur in base 10**, including with altered exterior guards that still realize the specified center alignment. This theorem places no restriction on other carry schedules, other center lengths, or longer return periods.

## 6. THEOREM — narrower direct-transplant obstructions

For the base-\(11\) table, preserve symbols `0,...,9` 和 replace `A` by \(b-1\). Units column \(i=5\) of the first prescribed transition requires

\[
8+7+0=4+b\cdot1.
\]

Hence the transported table forces \(b=11\). In base \(10\), this column emits digit \(5\), whereas the prescribed table requires \(4\).

For the base-\(17\) table, preserve symbols `0,...,9` 和 interpret `A=b-7,...,G=b-1`. Units column \(i=5\) of the first prescribed transition requires

\[
(b-6)+(b-7)+0=4+b\cdot1.
\]

Hence that transported table forces \(b=17\). In base \(10\), this column emits digit \(7\) with carry zero, whereas the prescribed table requires \(4\) with carry one. Appendix A executes both decimal transplantation checks 和 reports their failures.

These statements concern the explicitly defined substitutions. They impose no general obstruction on freely redesigned decimal templates.

## 7. THEOREM — representational obstruction for the saturated checker

Consider a family of coefficient words containing \(2n\) occurrences of the neutral symbol \(9\), with \(n\) unbounded. Suppose a proposed representation uses only unbounded constant runs whose symbols differ from \(9\), together with fixed blocks of total length at most \(K\). Every occurrence of \(9\) must lie in a fixed block, so the representation requires \(2n\le K\). Choosing \(n>K/2\) contradicts that requirement. Therefore this class of representations cannot encode the family with bounded blocks.

In particular, the supplied decimal saturated format uses bulk symbols \(c,18-c\), with \(c\ne9\); both differ from \(9\). The analogous restriction in base \(b\) excludes the unbounded \(b-1\) column-sum runs of Sections 3–4. The obstruction concerns a bounded-block representation of these families; the checker’s soundness 和 satisfiability remain separate questions.

### Existing neutral framework

The inspected repository already contains a separate base-generic neutral checker:

- `lean/P196/Drafts/Agent120NeutralBandCalibration/A120Template.lean`
- `lean/P196/Drafts/Agent120NeutralBandCalibration/A120Certificate.lean`

Its coefficient template, from the units end, equals

\[
B\,(b-1)^g\,C\,(b-1)^g\,B^R.
\]

Its edge checker verifies exact interface equalities 和 different carries through the opposite bands. Each edge updates

\[
g\longmapsto g-\gamma+u+v,
\]

where \(\gamma\) records the final carry, 和 \(u,v\) count neutral coefficients absorbed from the fixed interfaces. The existing `lychrel_of_cycle` theorem applies to a closed nonempty checked cycle with

\[
\sum\gamma\le\sum(u+v),\qquad g\ge2+\sum\gamma.
\]

The definition admits \(b=10\). Thus further exploration of neutral bands can use an existing sound framework. A decimal certificate remains the missing object.

## 8. IDEA — exact base-20 source gap

Seal's opened announcement asserts a base-\(20\) construction with more than \(200\) digits but explicitly omits its digit string. The phase-table transcription repeats that omission. The subsequently opened 2016 TeX report supplies examples for bases \(11,26\), without supplying that missing base-\(20\) witness.

Consequently this report contains **no reconstructed base-20 theorem**, no claimed base-20 carry certificate, 和 no invented base-20 numerical test. The unresolved source task requires recovering a complete witness together with its claimed phase return, then apply the finite carry reduction in Section 2. The gap concerns the evidence recovered in this task; the announced existence claim remains unrefuted here.

## 9. IDEA — sharpest remaining mathematical question

Does the existing neutral checker admit a decimal cycle of finite interfaces \((B_j,C_j)\), whose exact carry transitions satisfy

\[
\sum_j(u_j+v_j-\gamma_j)>0?
\]

Such a cycle must satisfy the checker's finite carry-flip conditions at every phase. It would produce a decimal Lychrel number through the already established certificate implication. The particular center itinerary in Section 5 cannot provide that cycle. The neutral column sum \(9\) itself remains available; another center itinerary, compatible exterior interfaces, 和 positive net growth remain the concrete missing construction.

The weaker condition of nonnegative total gain suffices for the existing theorem, while strict gain matches the growing-template goal of this task. No conjectured decimal witness accompanies this question.

## 10. Numerical verification summary

The executed check uses the initial run length \(n=2\) in each base. It first verifies the finite symbolic word identities, then checks boundary values \(n=0,1,2,3\), then follows each orbit for \(1000\) consecutive steps. Every step receives both a column-addition calculation 和 an independent integer sum \(N+\operatorname{rev}_b(N)\).

| Base | Period | Finite phase-column checks | Consecutive steps | Checked states | Palindromes | Final phase | Final run length | Final digits |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 11 | 6 | 339 | 1000 | 1001 | 0 | 4 | 168 | 393 |
| 17 | 6 | 473 | 1000 | 1001 | 0 | 4 | 168 | 415 |
| 26 | 4 | 82 | 1000 | 1001 | 0 | 0 | 252 | 524 |

The base-\(26\) count repeats exterior rows at different phases; Section 3 displays its \(50\) distinct fixed-block columns. The infinite conclusions follow from the symbolic identities 和 permanent mismatches. The numerical calculations test transcription 和 implementation consistency.

The exact formal seeds use gap \(g=4\) 和 the positional value of the phase-zero coefficient word. Each equals \(T_b(W_0(4))=W_1(4)\); coefficients can exceed the largest base digit, so the coefficient word itself must never be confused with a canonical numeral. Their separate numerical tests follow \(1000\) steps from those exact values:

| Base | Initial phase | Initial gap | Checked states | Palindromes | Final digits |
|---:|---:|---:|---:|---:|---:|
| 11 | 1 | 4 | 1001 | 0 | 397 |
| 17 | 1 | 4 | 1001 | 0 | 419 |
| 26 | 1 | 4 | 1001 | 0 | 528 |

Appendix B records their complete decimal values. The palindrome predicates continue to use bases \(11,17,26\), respectively.

## 11. LEAN-VERIFIED — registered formal scope

The new module `P196.Agent213KnownBaseMechanisms.KnownBases` imports the existing `P196.Drafts.Agent120NeutralBandCalibration.A120Certificate`. Its explicit data instantiate that generic theorem; no search, assumed certificate, or new foundational assumption enters the proofs.

| Base | Certificate edges | \(\sum\gamma\) | \(\sum(u+v)\) | Net gain |
|---:|---:|---:|---:|---:|
| 11 | 6 | 2 | 3 | 1 |
| 17 | 6 | 2 | 3 | 1 |
| 26 | 4 | 2 | 3 | 1 |

For each listed base, the module verifies the certificate, overflow count, 和 gain count by kernel reduction. It then establishes the Lychrel property of the associated template value for every \(g\ge4\), a concrete seed at \(g=4\), 和 existence in that base. Names include

```lean
Agent213.KnownBases.lychrel11_template
Agent213.KnownBases.lychrel17_template
Agent213.KnownBases.lychrel26_template
Agent213.KnownBases.exists_lychrel11
Agent213.KnownBases.exists_lychrel17
Agent213.KnownBases.exists_lychrel26
```

The module `P196.Agent213KnownBaseMechanisms.CenterRigidity` proves `Agent213.center_rigidity` 和 `Agent213.center_base10_impossible`. These endpoints concern the six integer equations in Section 5. The derivation of those equations from the explicitly specified carry itinerary remains the complete paper proof in that section; the formal theorem's statement does not itself define the carry itinerary.

Both modules compile under **Lean 4.19.0**, with `Std` 和 the existing repository modules, without Mathlib. The certificate arithmetic endpoints depend on no axioms. The orbit theorems 和 center-rigidity endpoints use only the allowed standard axioms `propext`, `Classical.choice`, `Quot.sound`. Appendices C–E contain the complete new source 和 the actual compilation/audit output. The result registers \(20\) endpoints across \(2\) new modules.

The formal template theorem uses the conservative bound \(g\ge4\); the direct digit-word carry proofs in Sections 3–4 cover every \(n\ge0\). Those scopes should remain distinct.

## Appendix A — complete executable carry 和 numerical verifier

Save the following block as `verify_agent213.py`, then run `python3 verify_agent213.py`. It uses only Python standard-library integer arithmetic. The finite carry tables supply the exact symbolic proof data; the subsequent 1000-step checks serve as independent consistency tests.

```python
D='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
P11=[
('1246277','A','A170352495681825A5026571A506181864A5143171','0','0872542'),
('3698A48','0','0883768431399986541A1092545899A41337673890','A','8498963'),
('7286895','A','1757424762898860994812839A1688872685237661','0','5996816'),
('1246277','A','A331374A51557661297853458882266745249484123','0','0872542'),
('3698A48','0','2546113376A23184075296A356A3923196843105462','A','8498963'),
('7286895','A','509012685283646802A6928602A8636492476220905','0','5996816')]
P17=[
('10023AB83E3B983CFGEC556G4G010','0','0FGCG10FG505GF020CGF','G','GG11G4F655DDGGB299B3D38BB320G'),
('10025F52C00F41AFCFDB0AC544020','G','GGFBD11GF4565EF21DCEG','0','0021444BB1BDFBEB23F0GC34E5210'),
('1128328FB0G16D8ABC7CC4G985221','0','GEB7E40E3AAB4DG3F8BEF','G','02258A04BD8CBA7C71F1BE9327211'),
('224F561D52E2E8G467G96902GA442','0','FC5GC80A85448AG8CG6CE','G','144B02G978G863G8D3E26D055F422'),
('449DAB29B5B6B0F7CGG0E1G504884','0','D7CG8003G98A04008FC8C','G','3894G501E1FFC8G0A6B4C91BBD844'),
('891A55426A5D41EG8FE2B2GAG90G8','0','8G8EG0080302G7010F7G8','G','8008GAG3B2FF7GE14D5A71465A088')]
def word(p,n):
    a,x,m,y,z=p
    return a+x*n+m+y*n+z

def step(w,b):
    carry=0; out=[]
    for x,y in zip(w[::-1],w):
        v=D.index(x)+D.index(y)+carry
        out.append(D[v%b]); carry=v//b
    if carry: out.append(D[carry])
    return ''.join(out[::-1])

def cert(p,b):
    a,x,m,y,z=p
    assert len(a)==len(z)
    # Read from units through the right fixed block, right run, middle,
    # left run, then left fixed block. Each q-run equals b-1.
    assert D.index(x)+D.index(y)==b-1
    segs=[(z[::-1],a),(m[::-1],m),(a[::-1],z)]
    carry=0; records=[]
    for j,(u,v) in enumerate(segs):
        cs=str(carry); out=''; qs=[]
        for l,r in zip(u,v):
            q=D.index(l)+D.index(r); qs.append(q)
            out+=D[(q+carry)%b]
            carry=(q+carry)//b; cs+=str(carry)
        records.append((','.join(map(str,qs)),cs,out,carry))
    # All result strings are MSF, in the same segment decomposition plus overflow.
    r,mout,l=[rec[2][::-1] for rec in records]
    c0,c1,c2=[rec[3] for rec in records]
    out_runs=(D[(b-1+c1)%b],D[(b-1+c0)%b])
    return records,(D[c2] if c2 else '',l,out_runs[0],mout,out_runs[1],r)

def canonical(p, offset=0):
    a,x,m,y,z=p
    left=offset; right=offset
    while a.endswith(x): a=a[:-1]; left+=1
    while m.startswith(x): m=m[1:]; left+=1
    while m.endswith(y): m=m[:-1]; right+=1
    while z.startswith(y): z=z[1:]; right+=1
    assert a and m and z
    return a,x,left,m,y,right,z

def symbolic_return_certificate(ps,b):
    for i,p in enumerate(ps):
        records,shape=cert(p,b)
        overflow,a,x,m,y,z=shape
        actual=(overflow+a,x,m,y,z)
        expected=ps[(i+1)%len(ps)]
        assert canonical(actual)==canonical(expected, int(i==len(ps)-1)),(b,i)
    return True

P26=[
('1N5ELA6C','P','P6E7','0','0D59ME5N'),
('P2KB4FJD','0','6KL6','P','CJG5AK2O'),
('1N5ELA6C','P','PDGFD','0','0D59ME5N'),
('P2KB4FJD','0','D373C','P','CJG5AK2O')]


def integer_step(w,b):
    v=int(w,b)+int(w[::-1],b)
    result=[]
    while v:
        v,r=divmod(v,b)
        result.append(D[r])
    return ''.join(result[::-1]) or '0'


def run():
    for b,ps in [(11,P11),(17,P17),(26,P26)]:
        print('BASE',b)
        for p in ps:
            assert p[0][0]!='0'
            assert all(D.index(ch)<b for part in p for ch in part)
        assert symbolic_return_certificate(ps,b)
        print('PASS symbolic identities for every integer n>=0')
        witnesses={11:[0,4,0,0,4,0],17:[0,0,3,5,2,1],26:[0,0,0,0]}[b]
        for p,j in zip(ps,witnesses):
            assert p[0][j]!=p[4][-1-j]
        print('PASS permanent fixed-block mismatch witnesses')
        columns=0
        for i,p in enumerate(ps):
            rec,shape=cert(p,b)
            print('phase',i,'lengths',len(p[0]),len(p[2]),len(p[4]))
            for tag,r in zip(['right','center','left'],rec):
                qword,carryword,output,carry=r
                qs=list(map(int,qword.split(',')))
                assert len(qs)+1==len(carryword)
                for j,q in enumerate(qs):
                    ci=int(carryword[j]); co=int(carryword[j+1]); e=D.index(output[j])
                    assert q+ci==e+b*co and 0<=e<b and co in (0,1)
                    columns+=1
                print(tag,'q='+qword,'c='+carryword,'e='+output)
            print('symbolic_output',shape)
        print('PASS finite carry columns:',columns)
        for n in (0,1,2,3):
            for i,p in enumerate(ps):
                expected=word(ps[(i+1)%len(ps)],n+int(i==len(ps)-1))
                assert step(word(p,n),b)==expected
        print('PASS boundary cases n=0,1,2,3')
        n0=2
        w=word(ps[0],n0)
        for t in range(1001):
            assert w==word(ps[t%len(ps)],n0+t//len(ps)),(b,t,'shape')
            assert w!=w[::-1],(b,t,'palindrome')
            if t<1000:
                a=step(w,b); z=integer_step(w,b)
                assert a==z,(b,t,'arithmetic')
                w=z
        print('PASS steps=1000 states=1001 phase_matches=1001 palindromes=0 '
              'integer_crosschecks=1000 final_phase='+str(1000%len(ps))+
              ' final_run='+str(n0+1000//len(ps))+' final_digits='+str(len(w)))
        # The Lean seed is the positional value of the phase-0 pair word at g=4.
        initial=word(ps[0],4)
        q=[D.index(x)+D.index(y) for x,y in zip(initial[::-1],initial)]
        seed=sum(v*b**i for i,v in enumerate(q))
        w=integer_step(initial,b)
        assert int(w,b)==seed and w==word(ps[1],4)
        for t in range(1001):
            assert w==word(ps[(t+1)%len(ps)],4+(t+1)//len(ps))
            assert w!=w[::-1]
            if t<1000:
                z=integer_step(w,b)
                assert step(w,b)==z
                w=z
        print('LEAN_SEED base='+str(b)+' value='+str(seed))
        print('PASS certified_seed_steps=1000 states=1001 phase_matches=1001 '
              'palindromes=0 integer_crosschecks=1000 final_digits='+str(len(w)))
    # Direct decimal transplantation checks, testing the claimed itinerary only.
    for b,ps,offset in [(11,P11,1),(17,P17,7)]:
        convert=lambda w: ''.join(D[D.index(ch)] if D.index(ch)<10 else D[10-offset+D.index(ch)-10] for ch in w)
        initial=convert(word(ps[0],2))
        prescribed=convert(word(ps[1],2))
        actual=integer_step(initial,10)
        assert actual!=prescribed
        print('DECIMAL_TRANSPLANT source_base='+str(b)+' column=5 actual_digit='
              +actual[-6]+' prescribed_digit='+prescribed[-6]+' FAILS_AS_EXPECTED')
    # Exact parameter values of the restricted center itinerary.
    b,a,c,d,h,k=26,6,14,7,3,7
    assert h==2*d+2*(a+c)-2*b+1 and k==4*(a+c)+5-3*b
    assert 4*d==b+2 and d==2*h+1 and a==2*h and c==2*k
    print('CENTER_RIGIDITY solution=(b,a,c,d,h,k)=(26,6,14,7,3,7) VERIFIED')
    print('DECIMAL_CENTER b=10 forces a=2,d=3,c=5; 7*c-16*a=3 != 2')


if __name__=='__main__':
    run()
```

## Appendix B — actual verifier output

```text
BASE 11
PASS symbolic identities for every integer n>=0
PASS permanent fixed-block mismatch witnesses
phase 0 lengths 7 42 7
right q=3,6,9,8,9,15,7 c=00000010 e=3698948
center q=11,8,8,3,7,6,7,14,13,11,14,9,9,9,8,5,15,15,1,9,11,11,9,1,15,15,5,8,9,9,9,14,11,13,14,7,6,7,3,8,8,11 c=0100000011110000011001100110000011110000001 e=09837673314A9985452901A1456899931348673880
left q=7,15,9,8,9,6,3 c=10100000 e=84A8963
symbolic_output ('', '3698A48', '0', '0883768431399986541A1092545899A41337673890', 'A', '8498963')
phase 1 lengths 7 42 7
right q=6,12,18,16,19,8,16 c=00111101 e=6186995
center q=0,17,16,6,14,12,15,7,6,2,7,19,18,18,16,11,9,9,3,19,1,1,19,3,9,9,11,16,18,18,19,7,2,6,7,15,12,14,6,16,17,0 c=1011011100001111100010010001111100001110110 e=1667325862788861A9382184990688982674247571
left q=16,8,19,16,18,12,6 c=01011110 e=5986827
symbolic_output ('', '7286895', 'A', '1757424762898860994812839A1688872685237661', '0', '5996816')
phase 2 lengths 7 42 7
right q=13,3,16,12,17,18,10 c=01011111 e=2452780
center q=2,13,11,14,7,4,9,15,12,4,15,17,16,16,12,1,19,18,7,16,3,3,16,7,18,19,1,12,16,16,17,15,4,12,15,9,4,7,14,11,13,2 c=1011100011011111011010010110111110110001110 e=32148494254766228885435879216675515A473133
left q=10,18,17,12,16,3,13 c=00111101 e=A772642
symbolic_output ('1', '246277A', 'A', '331374A51557661297853458882266745249484123', '0', '0872542')
phase 3 lengths 7 43 7
right q=3,6,9,8,9,15,7 c=00000010 e=3698948
center q=13,5,4,5,11,11,13,14,7,6,9,12,13,12,8,3,10,17,15,13,9,6,9,13,15,17,10,3,8,12,13,12,9,6,7,14,13,11,11,5,4,5,13 c=01000111100011100011100011110011100011110001 e=2645013486913293A653A69257048132A6733116452
left q=7,15,9,8,9,6,3 c=10100000 e=84A8963
symbolic_output ('', '3698A48', '0', '2546113376A23184075296A356A3923196843105462', 'A', '8498963')
phase 4 lengths 7 43 7
right q=6,12,18,16,19,8,16 c=00111101 e=6186995
center q=4,11,8,11,1,2,6,7,15,12,19,3,6,3,17,7,10,13,10,5,19,12,19,5,10,13,10,7,17,3,6,3,19,12,15,7,6,2,1,11,8,11,4 c=10101000011100010011011100110100011100001010 e=5090226742946368A2068296A208646382586210905
left q=16,8,19,16,18,12,6 c=01011110 e=5986827
symbolic_output ('', '7286895', 'A', '509012685283646802A6928602A8636492476220905', '0', '5996816')
phase 5 lengths 7 43 7
right q=13,3,16,12,17,18,10 c=01011111 e=2452780
center q=10,0,18,0,3,4,12,15,9,4,17,7,12,7,12,16,10,4,10,12,17,4,17,12,10,4,10,16,12,7,12,7,17,4,9,15,12,4,3,0,18,0,10 c=11010001100101011100110111001101010011000100 e=01713415A468181605A1756205A528186594253071A
left q=10,18,17,12,16,3,13 c=00111101 e=A772642
symbolic_output ('1', '246277A', 'A', 'A170352495681825A5026571A506181864A51431710', '0', '0872542')
PASS finite carry columns: 339
PASS boundary cases n=0,1,2,3
PASS steps=1000 states=1001 phase_matches=1001 palindromes=0 integer_crosschecks=1000 final_phase=4 final_run=168 final_digits=393
LEAN_SEED base=11 value=1469717089519751132159055484809610379822517653955924096855720190680
PASS certified_seed_steps=1000 states=1001 phase_matches=1001 palindromes=0 integer_crosschecks=1000 final_digits=397
BASE 17
PASS symbolic identities for every integer n>=0
PASS permanent fixed-block mismatch witnesses
phase 0 lengths 29 20 29
right q=17,0,2,5,14,21,19,11,16,17,14,20,18,10,14,28,31,29,27,17,10,11,21,20,20,17,1,17,16 c=010000110010110011111001111011 e=0125E43CG0F32BEBFDB1BB4441200
center q=15,31,28,12,18,1,15,31,21,5,5,21,31,15,1,18,12,28,31,15 c=101101001100110010110 e=GECD12FE5654FG11DBFG
left q=16,17,1,17,20,20,21,11,10,17,27,29,31,28,14,10,18,20,14,17,16,11,19,21,14,5,2,0,17 c=001011110011111001101101100001 e=G020445CA0BDFCFA14F00C25F5200
symbolic_output ('1', '0025F52C00F41AFCFDB0AC544020G', 'G', 'GFBD11GF4565EF21DCEG', '0', '0021444BB1BDFBEB23F0GC34E5210')
phase 1 lengths 29 21 29
right q=1,1,2,7,19,19,8,14,28,0,15,18,6,12,24,26,27,28,24,12,11,21,16,9,8,5,2,2,0 c=000001100100100111110011000000 e=1127239EB1F17C7ABC8DB40A85220
center q=32,30,27,24,14,3,16,30,20,10,10,10,20,30,16,3,14,24,27,30,32 c=0111100011000111001111 e=FEB8F3GD4BAA3E04E7BEG
left q=0,2,2,5,8,9,16,21,11,12,24,28,27,26,24,12,6,18,15,0,28,14,8,19,19,7,2,1,1 c=100000001001111100100100110000 e=122589G4CC7CBA8D61G0BF8238211
symbolic_output ('', '1128328FB0G16D8ABC7CC4G985221', '0', 'GEB7E40E3AAB4DG3F8BEF', 'G', '02258A04BD8CBA7C71F1BE9327211')
phase 2 lengths 29 21 29
right q=2,2,4,15,5,5,17,29,22,1,31,2,13,25,15,20,22,24,15,25,23,8,16,19,16,10,4,4,1 c=000000011101001011101100110000 e=224F550D62E3D8G368G879G20B441
center q=31,28,22,15,29,7,16,27,7,21,20,21,7,27,16,7,29,15,22,28,31 c=0111010010111011010111 e=EC6GC8GA84458A08CG5CF
left q=1,4,4,10,16,19,16,8,23,25,15,24,22,20,15,25,13,2,31,1,22,29,17,5,5,15,4,2,2 c=100000110110111010010111000000 e=244AG20969G764G8E2E25D165F422
symbolic_output ('', '224F561D52E2E8G467G96902GA442', '0', 'FC5GC80A85448AG8CG6CE', 'G', '144B02G978G863G8D3E26D055F422')
phase 3 lengths 29 21 29
right q=4,4,8,30,10,11,1,26,11,4,28,5,27,16,32,7,12,15,32,17,13,18,16,4,16,21,8,8,3 c=000010001001011100011011001000 e=448DBB19C4B6A0G8CFF1E105G4983
center q=29,24,11,32,24,16,16,20,16,9,8,9,16,20,16,16,24,32,11,24,29 c=0110111111000011111011 e=C8CF80040A89G3008GC7D
left q=3,8,8,21,16,4,16,18,13,17,32,15,12,7,32,16,27,5,28,4,11,26,1,11,10,30,8,4,4 c=100011001011000111010010001000 e=488405G1E0GGC7F0B6B5B92BAD944
symbolic_output ('', '449DAB29B5B6B0F7CGG0E1G504884', '0', 'D7CG8003G98A04008FC8C', 'G', '3894G501E1FFC8G0A6B4C91BBD844')
phase 4 lengths 29 21 29
right q=8,8,17,26,21,22,3,18,23,9,22,12,21,0,31,15,24,31,31,1,28,2,16,10,16,8,17,16,7 c=000111101101010101110100000110 e=880A56417A5D41EG7FF2B3GAG8008
center q=25,15,24,31,16,0,0,7,16,19,16,19,16,7,0,0,16,31,24,15,25 c=0101110000111100001101 e=8G7F0107G2030800GE8G8
left q=7,16,17,8,16,10,16,2,28,1,31,31,24,15,31,0,21,12,22,9,23,18,3,22,21,26,17,8,8 c=100100000101110101010110111100 e=8G09GAG2B2EF8GE14D5A62455A198
symbolic_output ('', '891A55426A5D41EG8FE2B2GAG90G8', '0', '8G8EG0080302G7010F7G8', 'G', '8008GAG3B2FF7GE14D5A71465A088')
phase 5 lengths 29 21 29
right q=16,17,1,20,10,11,8,3,13,20,10,26,8,2,28,32,15,30,29,4,22,5,32,20,32,17,0,16,16 c=001010000010100110110101111000 e=G023BB83D3B992BGGDD556F4G11GG
center q=16,32,15,29,16,1,0,15,16,5,0,5,16,15,0,1,16,29,15,32,16 c=0010110000000000001011 e=GFGC020FG505GF01GCGF0
left q=16,16,0,17,32,20,32,5,22,4,29,30,15,32,28,2,8,26,10,20,13,3,8,11,10,20,1,17,16 c=111011110101101100101000001011 e=0010G4G655CEGFC389B3E38BA3200
symbolic_output ('1', '0023AB83E3B983CFGEC556G4G0100', '0', '0FGCG10FG505GF020CGFG', 'G', 'GG11G4F655DDGGB299B3D38BB320G')
PASS finite carry columns: 473
PASS boundary cases n=0,1,2,3
PASS steps=1000 states=1001 phase_matches=1001 palindromes=0 integer_crosschecks=1000 final_phase=4 final_run=168 final_digits=415
LEAN_SEED base=17 value=6588926500576461501605393111129277601274144030834215254803457107272590783088799415810912339234716161536384
PASS certified_seed_steps=1000 states=1001 phase_matches=1001 palindromes=0 integer_crosschecks=1000 final_digits=419
BASE 26
PASS symbolic identities for every integer n>=0
PASS permanent fixed-block mismatch witnesses
phase 0 lengths 8 4 8
right q=24,28,19,36,30,15,19,12 c=001011000 e=O2KA5GJC
center q=32,20,20,32 c=01001 e=6LK6
left q=12,19,15,30,36,19,28,24 c=100011010 e=DJF4BK2P
symbolic_output ('', 'P2KB4FJD', '0', '6KL6', 'P', 'CJG5AK2O')
phase 1 lengths 8 4 8
right q=49,4,40,21,9,31,38,25 c=010100111 e=N5EM95D0
center q=12,41,41,12 c=10110 e=DFGD
left q=25,38,31,9,21,40,4,49 c=001100101 e=PC6ALE5N
symbolic_output ('1', 'N5ELA6CP', 'P', 'DGFD', '0', '0D59ME5N')
phase 2 lengths 8 5 8
right q=24,28,19,36,30,15,19,12 c=001011000 e=O2KA5GJC
center q=38,28,32,28,38 c=011111 e=C373D
left q=12,19,15,30,36,19,28,24 c=100011010 e=DJF4BK2P
symbolic_output ('', 'P2KB4FJD', '0', 'D373C', 'P', 'CJG5AK2O')
phase 3 lengths 8 5 8
right q=49,4,40,21,9,31,38,25 c=010100111 e=N5EM95D0
center q=25,6,14,6,25 c=110000 e=07E6P
left q=25,38,31,9,21,40,4,49 c=001100101 e=PC6ALE5N
symbolic_output ('1', 'N5ELA6CP', 'P', 'P6E70', '0', '0D59ME5N')
PASS finite carry columns: 82
PASS boundary cases n=0,1,2,3
PASS steps=1000 states=1001 phase_matches=1001 palindromes=0 integer_crosschecks=1000 final_phase=0 final_run=252 final_digits=524
LEAN_SEED base=26 value=4018627229642272055284900389089242527420
PASS certified_seed_steps=1000 states=1001 phase_matches=1001 palindromes=0 integer_crosschecks=1000 final_digits=528
DECIMAL_TRANSPLANT source_base=11 column=5 actual_digit=5 prescribed_digit=4 FAILS_AS_EXPECTED
DECIMAL_TRANSPLANT source_base=17 column=5 actual_digit=7 prescribed_digit=4 FAILS_AS_EXPECTED
CENTER_RIGIDITY solution=(b,a,c,d,h,k)=(26,6,14,7,3,7) VERIFIED
DECIMAL_CENTER b=10 forces a=2,d=3,c=5; 7*c-16*a=3 != 2
```

## Appendix C — complete Lean center-rigidity source

```lean
import Std

namespace Agent213

/-- The selected finite center carry equations uniquely determine the base
    and all six integer parameters. -/
theorem center_rigidity
    (b a c d h k : Int)
    (h_center : h = 2*d + 2*(a+c) - 2*b + 1)
    (k_center : k = 4*(a+c) + 5 - 3*b)
    (d_base : 4*d = b+2)
    (d_center : d = 2*h+1)
    (a_center : a = 2*h)
    (c_center : c = 2*k) :
    b = 26 ∧ a = 6 ∧ c = 14 ∧ d = 7 ∧ h = 3 ∧ k = 7 := by
  omega

/-- In particular, this exact center carry itinerary cannot occur in base 10. -/
theorem center_base10_impossible
    (a c d h k : Int)
    (h_center : h = 2*d + 2*(a+c) - 2*10 + 1)
    (k_center : k = 4*(a+c) + 5 - 3*10)
    (d_base : 4*d = 10+2)
    (d_center : d = 2*h+1)
    (a_center : a = 2*h)
    (c_center : c = 2*k) : False := by
  have hb := (center_rigidity 10 a c d h k h_center k_center d_base
    d_center a_center c_center).1
  omega

#print axioms center_rigidity
#print axioms center_base10_impossible

end Agent213
```

## Appendix D — complete Lean known-base certificates

```lean
import P196.Drafts.Agent120NeutralBandCalibration.A120Certificate

/-!
# Agent 213: neutral-band calibration in bases 11, 17, 26

These certificates reconstruct known six-step families in bases 11 and 17
and the known four-step base-26 family. They do not establish a decimal
Lychrel number. All coefficient lists are LSD-first.
-/

namespace Agent213.KnownBases

open Agent120.Neutral

def exteriorQ : List Nat := [24, 28, 19, 36, 30, 15, 19, 12]
def exteriorR : List Nat := [49, 4, 40, 21, 9, 31, 38, 25]
def centerA : List Nat := [32, 20, 20, 32]
def centerB : List Nat := [12, 41, 41, 12]
def centerC : List Nat := [38, 28, 32, 28, 38]
def centerD : List Nat := [25, 6, 14, 6, 25]

def cert26 : List Edge :=
  [⟨exteriorQ, centerA, exteriorR, centerB, 0, 0⟩,
   ⟨exteriorR, centerB, exteriorQ, centerC, 1, 0⟩,
   ⟨exteriorQ, centerC, exteriorR, centerD, 0, 0⟩,
   ⟨exteriorR, centerD, exteriorQ, centerA, 1, 1⟩]

theorem cert26_ok : cycleOK 26 cert26 exteriorQ centerA = true := by decide
theorem cert26_overflows : sumGam 26 cert26 = 2 := by decide
theorem cert26_gain : sumGain cert26 = 3 := by decide

theorem lychrel26_template (g : Nat) (hg : 4 ≤ g) :
    Lychrel 26 (val 26 (tmpl 26 exteriorQ centerA g)) :=
  lychrel_of_cycle 26 cert26 exteriorQ centerA cert26_ok g
    (by rw [cert26_overflows]; exact hg)

def seed26 : Nat := val 26 (tmpl 26 exteriorQ centerA 4)

theorem lychrel26_seed : Lychrel 26 seed26 :=
  lychrel26_template 4 (Nat.le_refl 4)

theorem exists_lychrel26 : ∃ n, Lychrel 26 n := ⟨seed26, lychrel26_seed⟩

/-! ## Known base-11 six-step certificate -/

def exterior11_0 : List Nat := [3, 6, 9, 8, 9, 15, 7]

def center11_0 : List Nat := [11, 8, 8, 3, 7, 6, 7, 14, 13, 11, 14, 9, 9, 9, 8, 5, 15, 15, 1, 9, 11, 11, 9, 1, 15, 15, 5, 8, 9, 9, 9, 14, 11, 13, 14, 7, 6, 7, 3, 8, 8, 11]

def exterior11_1 : List Nat := [6, 12, 18, 16, 19, 8, 16]

def center11_1 : List Nat := [0, 17, 16, 6, 14, 12, 15, 7, 6, 2, 7, 19, 18, 18, 16, 11, 9, 9, 3, 19, 1, 1, 19, 3, 9, 9, 11, 16, 18, 18, 19, 7, 2, 6, 7, 15, 12, 14, 6, 16, 17, 0]

def exterior11_2 : List Nat := [13, 3, 16, 12, 17, 18, 10]

def center11_2 : List Nat := [2, 13, 11, 14, 7, 4, 9, 15, 12, 4, 15, 17, 16, 16, 12, 1, 19, 18, 7, 16, 3, 3, 16, 7, 18, 19, 1, 12, 16, 16, 17, 15, 4, 12, 15, 9, 4, 7, 14, 11, 13, 2]

def exterior11_3 : List Nat := [3, 6, 9, 8, 9, 15, 7]

def center11_3 : List Nat := [13, 5, 4, 5, 11, 11, 13, 14, 7, 6, 9, 12, 13, 12, 8, 3, 10, 17, 15, 13, 9, 6, 9, 13, 15, 17, 10, 3, 8, 12, 13, 12, 9, 6, 7, 14, 13, 11, 11, 5, 4, 5, 13]

def exterior11_4 : List Nat := [6, 12, 18, 16, 19, 8, 16]

def center11_4 : List Nat := [4, 11, 8, 11, 1, 2, 6, 7, 15, 12, 19, 3, 6, 3, 17, 7, 10, 13, 10, 5, 19, 12, 19, 5, 10, 13, 10, 7, 17, 3, 6, 3, 19, 12, 15, 7, 6, 2, 1, 11, 8, 11, 4]

def exterior11_5 : List Nat := [13, 3, 16, 12, 17, 18, 10]

def center11_5 : List Nat := [10, 0, 18, 0, 3, 4, 12, 15, 9, 4, 17, 7, 12, 7, 12, 16, 10, 4, 10, 12, 17, 4, 17, 12, 10, 4, 10, 16, 12, 7, 12, 7, 17, 4, 9, 15, 12, 4, 3, 0, 18, 0, 10]

def cert11 : List Edge :=
  [⟨exterior11_0, center11_0, exterior11_1, center11_1, 0, 0⟩,
   ⟨exterior11_1, center11_1, exterior11_2, center11_2, 0, 0⟩,
   ⟨exterior11_2, center11_2, exterior11_3, center11_3, 1, 0⟩,
   ⟨exterior11_3, center11_3, exterior11_4, center11_4, 0, 0⟩,
   ⟨exterior11_4, center11_4, exterior11_5, center11_5, 0, 0⟩,
   ⟨exterior11_5, center11_5, exterior11_0, center11_0, 1, 1⟩]

theorem cert11_ok : cycleOK 11 cert11 exterior11_0 center11_0 = true := by decide

theorem cert11_overflows : sumGam 11 cert11 = 2 := by decide

theorem cert11_gain : sumGain cert11 = 3 := by decide

theorem lychrel11_template (g : Nat) (hg : 4 ≤ g) :
    Lychrel 11 (val 11 (tmpl 11 exterior11_0 center11_0 g)) :=
  lychrel_of_cycle 11 cert11 exterior11_0 center11_0 cert11_ok g
    (by rw [cert11_overflows]; exact hg)

def seed11 : Nat := val 11 (tmpl 11 exterior11_0 center11_0 4)

theorem lychrel11_seed : Lychrel 11 seed11 :=
  lychrel11_template 4 (Nat.le_refl 4)

theorem exists_lychrel11 : ∃ n, Lychrel 11 n := ⟨seed11, lychrel11_seed⟩

/-! ## Known base-17 six-step certificate -/

def exterior17_0 : List Nat := [17, 0, 2, 5, 14, 21, 19, 11, 16, 17, 14, 20, 18, 10, 14, 28, 31, 29, 27, 17, 10, 11, 21, 20, 20, 17, 1, 17, 16]

def center17_0 : List Nat := [15, 31, 28, 12, 18, 1, 15, 31, 21, 5, 5, 21, 31, 15, 1, 18, 12, 28, 31, 15]

def exterior17_1 : List Nat := [1, 1, 2, 7, 19, 19, 8, 14, 28, 0, 15, 18, 6, 12, 24, 26, 27, 28, 24, 12, 11, 21, 16, 9, 8, 5, 2, 2, 0]

def center17_1 : List Nat := [32, 30, 27, 24, 14, 3, 16, 30, 20, 10, 10, 10, 20, 30, 16, 3, 14, 24, 27, 30, 32]

def exterior17_2 : List Nat := [2, 2, 4, 15, 5, 5, 17, 29, 22, 1, 31, 2, 13, 25, 15, 20, 22, 24, 15, 25, 23, 8, 16, 19, 16, 10, 4, 4, 1]

def center17_2 : List Nat := [31, 28, 22, 15, 29, 7, 16, 27, 7, 21, 20, 21, 7, 27, 16, 7, 29, 15, 22, 28, 31]

def exterior17_3 : List Nat := [4, 4, 8, 30, 10, 11, 1, 26, 11, 4, 28, 5, 27, 16, 32, 7, 12, 15, 32, 17, 13, 18, 16, 4, 16, 21, 8, 8, 3]

def center17_3 : List Nat := [29, 24, 11, 32, 24, 16, 16, 20, 16, 9, 8, 9, 16, 20, 16, 16, 24, 32, 11, 24, 29]

def exterior17_4 : List Nat := [8, 8, 17, 26, 21, 22, 3, 18, 23, 9, 22, 12, 21, 0, 31, 15, 24, 31, 31, 1, 28, 2, 16, 10, 16, 8, 17, 16, 7]

def center17_4 : List Nat := [25, 15, 24, 31, 16, 0, 0, 7, 16, 19, 16, 19, 16, 7, 0, 0, 16, 31, 24, 15, 25]

def exterior17_5 : List Nat := [16, 17, 1, 20, 10, 11, 8, 3, 13, 20, 10, 26, 8, 2, 28, 32, 15, 30, 29, 4, 22, 5, 32, 20, 32, 17, 0, 16, 16]

def center17_5 : List Nat := [16, 32, 15, 29, 16, 1, 0, 15, 16, 5, 0, 5, 16, 15, 0, 1, 16, 29, 15, 32, 16]

def cert17 : List Edge :=
  [⟨exterior17_0, center17_0, exterior17_1, center17_1, 1, 0⟩,
   ⟨exterior17_1, center17_1, exterior17_2, center17_2, 0, 0⟩,
   ⟨exterior17_2, center17_2, exterior17_3, center17_3, 0, 0⟩,
   ⟨exterior17_3, center17_3, exterior17_4, center17_4, 0, 0⟩,
   ⟨exterior17_4, center17_4, exterior17_5, center17_5, 0, 0⟩,
   ⟨exterior17_5, center17_5, exterior17_0, center17_0, 1, 1⟩]

theorem cert17_ok : cycleOK 17 cert17 exterior17_0 center17_0 = true := by decide

set_option maxRecDepth 2048 in
theorem cert17_overflows : sumGam 17 cert17 = 2 := by decide

theorem cert17_gain : sumGain cert17 = 3 := by decide

theorem lychrel17_template (g : Nat) (hg : 4 ≤ g) :
    Lychrel 17 (val 17 (tmpl 17 exterior17_0 center17_0 g)) :=
  lychrel_of_cycle 17 cert17 exterior17_0 center17_0 cert17_ok g
    (by rw [cert17_overflows]; exact hg)

def seed17 : Nat := val 17 (tmpl 17 exterior17_0 center17_0 4)

theorem lychrel17_seed : Lychrel 17 seed17 :=
  lychrel17_template 4 (Nat.le_refl 4)

theorem exists_lychrel17 : ∃ n, Lychrel 17 n := ⟨seed17, lychrel17_seed⟩

end Agent213.KnownBases

#print axioms Agent213.KnownBases.cert26_ok
#print axioms Agent213.KnownBases.cert26_overflows
#print axioms Agent213.KnownBases.cert26_gain
#print axioms Agent213.KnownBases.lychrel26_template
#print axioms Agent213.KnownBases.lychrel26_seed
#print axioms Agent213.KnownBases.exists_lychrel26

#print axioms Agent213.KnownBases.cert11_ok
#print axioms Agent213.KnownBases.cert11_overflows
#print axioms Agent213.KnownBases.cert11_gain
#print axioms Agent213.KnownBases.lychrel11_template
#print axioms Agent213.KnownBases.lychrel11_seed
#print axioms Agent213.KnownBases.exists_lychrel11
#print axioms Agent213.KnownBases.cert17_ok
#print axioms Agent213.KnownBases.cert17_overflows
#print axioms Agent213.KnownBases.cert17_gain
#print axioms Agent213.KnownBases.lychrel17_template
#print axioms Agent213.KnownBases.lychrel17_seed
#print axioms Agent213.KnownBases.exists_lychrel17
```

## Appendix E — actual Lean compilation 和 repository audit

### Center-rigidity compilation

```text
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)

Command:
/tmp/agent208-lean/lean-4.19.0-linux/bin/lean /workspace/scratch/37340aca3276/agent213_odd/Agent213CenterRigidity.lean

Exit code: 0

'Agent213.center_rigidity' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent213.center_base10_impossible' depends on axioms: [propext, Classical.choice, Quot.sound]

No sorry, admit, or custom axiom declarations. Standard Lean axioms above retained exactly as reported by #print axioms.
```

### Known-base certificate compilation

```text
'Agent213.KnownBases.cert26_ok' does not depend on any axioms
'Agent213.KnownBases.cert26_overflows' does not depend on any axioms
'Agent213.KnownBases.cert26_gain' does not depend on any axioms
'Agent213.KnownBases.lychrel26_template' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent213.KnownBases.lychrel26_seed' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent213.KnownBases.exists_lychrel26' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent213.KnownBases.cert11_ok' does not depend on any axioms
'Agent213.KnownBases.cert11_overflows' does not depend on any axioms
'Agent213.KnownBases.cert11_gain' does not depend on any axioms
'Agent213.KnownBases.lychrel11_template' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent213.KnownBases.lychrel11_seed' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent213.KnownBases.exists_lychrel11' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent213.KnownBases.cert17_ok' does not depend on any axioms
'Agent213.KnownBases.cert17_overflows' does not depend on any axioms
'Agent213.KnownBases.cert17_gain' does not depend on any axioms
'Agent213.KnownBases.lychrel17_template' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent213.KnownBases.lychrel17_seed' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent213.KnownBases.exists_lychrel17' depends on axioms: [propext, Classical.choice, Quot.sound]
exit_code=0
wall_seconds=1.804
peak_child_rss_kib=572696
```

### Repository verification gate

Executed from the repository root against main commit `c6902ac6c366ce018e68a810f58b400dda07145a`:

```bash
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed
```

The runtime was Lean 4.19.0; execution used one Lean thread 和 an 8 GiB address-space limit. The unmodified repository verifier checks repository rules globally, builds changed modules, 和 audits the affected project's endpoints. Its build-log excerpt intentionally retains only the final 4000 characters, so the first excerpt line may begin mid-line.

```text
[rules] 4825 Lean files, 288 projects, OK
[changed] against origin/main: 2 new/changed Lean file(s); building 2 module(s); auditing 1 project(s)
[build] up to 1 Lean file(s) at a time
ate.lean:354:0: 'Agent120.Neutral.pairs_digits_tmpl' depends on axioms: [propext, Quot.sound]
info: ././././P196/Drafts/Agent120NeutralBandCalibration/A120Template.lean:355:0: 'Agent120.Neutral.step_tmpl' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ././././P196/Drafts/Agent120NeutralBandCalibration/A120Template.lean:356:0: 'Agent120.Neutral.not_isPal_tmpl' depends on axioms: [propext, Quot.sound]
ℹ [5/6] Replayed P196.Drafts.Agent120NeutralBandCalibration.A120Certificate
info: ././././P196/Drafts/Agent120NeutralBandCalibration/A120Certificate.lean:180:0: 'Agent120.Neutral.edge_step' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ././././P196/Drafts/Agent120NeutralBandCalibration/A120Certificate.lean:181:0: 'Agent120.Neutral.chain_run' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ././././P196/Drafts/Agent120NeutralBandCalibration/A120Certificate.lean:182:0: 'Agent120.Neutral.lychrel_of_cycle' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ././././P196/Drafts/Agent120NeutralBandCalibration/A120Certificate.lean:183:0: 'Agent120.Neutral.lychrel_of_entry' depends on axioms: [propext, Quot.sound]
ℹ [6/6] Built P196.Agent213KnownBaseMechanisms.KnownBases
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:151:0: 'Agent213.KnownBases.cert26_ok' does not depend on any axioms
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:152:0: 'Agent213.KnownBases.cert26_overflows' does not depend on any axioms
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:153:0: 'Agent213.KnownBases.cert26_gain' does not depend on any axioms
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:154:0: 'Agent213.KnownBases.lychrel26_template' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:155:0: 'Agent213.KnownBases.lychrel26_seed' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:156:0: 'Agent213.KnownBases.exists_lychrel26' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:158:0: 'Agent213.KnownBases.cert11_ok' does not depend on any axioms
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:159:0: 'Agent213.KnownBases.cert11_overflows' does not depend on any axioms
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:160:0: 'Agent213.KnownBases.cert11_gain' does not depend on any axioms
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:161:0: 'Agent213.KnownBases.lychrel11_template' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:162:0: 'Agent213.KnownBases.lychrel11_seed' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:163:0: 'Agent213.KnownBases.exists_lychrel11' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:164:0: 'Agent213.KnownBases.cert17_ok' does not depend on any axioms
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:165:0: 'Agent213.KnownBases.cert17_overflows' does not depend on any axioms
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:166:0: 'Agent213.KnownBases.cert17_gain' does not depend on any axioms
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:167:0: 'Agent213.KnownBases.lychrel17_template' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:168:0: 'Agent213.KnownBases.lychrel17_seed' depends on axioms: [propext, Classical.choice, Quot.sound]
info: ././././P196/Agent213KnownBaseMechanisms/KnownBases.lean:169:0: 'Agent213.KnownBases.exists_lychrel17' depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully.
[build] OK
[axioms] 20 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

