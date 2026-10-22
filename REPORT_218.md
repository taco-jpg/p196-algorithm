# REPORT_218 — Return-certificate satisfiability audit

Agent #218; direction 8. Source snapshot: `c6902ac6c366ce018e68a810f58b400dda07145a`. Toolchain: Lean 4.19.0, core + Std, without Mathlib.

## Answer in one paragraph

**THEOREM:** every accepted certificate in the phase family \(6\leftrightarrow12\) satisfies \(2\Gamma<P\), where \(P\) is the period 和 \(\Gamma\) counts actual overflow steps; consequently the entire saturated subfamily is impossible, independently of block widths, period, maximal-trimming choices, or zero gain in a band. The new ingredient is an explicit common fixed-cut construction that puts the same adjacent columns inside the outer band throughout the actual orbit, permitting the existing exact carry-strip obstruction to apply. **LEAN-VERIFIED:** for a fixed cyclic list of states 和 trims, the checker's lower-bound fields are satisfiable exactly when the outer 和 inner net gains are nonnegative; exact common-padding identities also permit band letters to move into finite blocks, with a concrete local transition excluded by the original one-sided trimming syntax. **LEAN-VERIFIED:** an explicit period-three carry-strip counterexample refutes a direct extension of the scalar erasure argument to the six-phase family. **IDEA / unresolved target:** joint satisfiability of the complete original checker remains unresolved; 这 audit supplies neither an accepted certificate nor a decimal Lychrel witness. The saturated \(6/12\) exclusion below is a complete mathematical proof; its new combined bridge is distinguished from the separately compiled Lean endpoints.

## 1. THEOREM — Original checker requirements

Write a state as \(s=(c,B,A,C)\), where the words contain column sums in \([0,18]\). In units-first order its template is

\[
\mathcal T_s(G,H)=B\,c^G\,A\,(18-c)^H\,C\,(18-c)^H\,A^R\,c^G\,B^R.
\]

The phase condition is \(1\le c\le17\), \(c\ne9\). For a cyclic link from \(s_i\) to \(s_{i+1}\), the checker requires the following groups of conditions:

| Group | Exact mathematical requirement |
|---|---|
| Valid source | Legal phase; each coefficient in \(B_i,A_i,C_i\) lies in \([0,18]\). |
| Phase update | \(c_{i+1}=2t(c_i)\), with \(t(c)=c-9\mathbf 1_{c\ge10}\). |
| Exterior return | \(B_{r,i}=B_{i+1}c_{i+1}^{j_i}\). |
| Interface return | \(A_{r,i}=c_{i+1}^{j_{1,i}}A_{i+1}(18-c_{i+1})^{j_{2,i}}\). |
| Center return | \(C_{r,i}=(18-c_{i+1})^{k_i}C_{i+1}(18-c_{i+1})^{k_i}\). |
| Safety | The exact normalized digit blocks fail the length-independent `StepPal` test. |
| Lower bounds | \(\ell_i,h_i\ge2\); \(\ell_{i+1}\le\ell_i+\gamma_i+j_i+j_{1,i}-2\); \(h_{i+1}\le h_i+\gamma_i+j_{2,i}+k_i-2\). |

Here \(\gamma_i\in\{0,1\}\), \(B_{r,i},A_{r,i},C_{r,i}\) are calculated from complete block normalization; the checker never supplies arbitrary carry choices. The exact source is [ReturnCertificate.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/ReturnCertificate.lean), with the carry formulas in [TemplateStep.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/TemplateStep.lean).

**THEOREM — existing bridge audit.** The source already derives center symmetry with an even middle coefficient, canonical positive exterior, 和 ordinary-integer realizability from acceptance. The endpoint `Agent112.Admissibility.certificate_existence_of_check` requires only `check cert = true`. The witness is the first successor \(m=\operatorname{step}(n)\); the safety conclusion includes time zero of \(m\), so the initial safety obligation is covered. A short `links` list fails at a default link with lower bounds zero. Entries beyond the state count are unused. These are source-audit findings, rather than new existence results. Sources: [AdmissibleCenters.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/CertificateToLychrel/AdmissibleCenters.lean) 和 [AdmissibleHeads.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/CertificateToLychrel/AdmissibleHeads.lean).

## 2. THEOREM — exclusion of every saturated 6/12 certificate

**THEOREM.** Let `cert` be a certificate for the unchanged `Agent109.Cert.check`. If `check cert = true` 和 its initial phase belongs to \(\{6,12\}\), then, writing \(P\) for its number of states 和 \(\Gamma=\sum_{i=0}^{P-1}\gamma_i\) for the actual terminal carries,

\[
2\Gamma<P.
\]

Equivalently, acceptance in 这 phase class forbids equality in the exterior carry-density bound \(\Gamma/P=1/2\). 这 statement permits arbitrary finite block widths, nonmaximal trimming, arbitrarily large period, 和 a zero net gain in either band. Its exclusion concerns the saturated subfamily; unsaturated certificates 和 the six-phase class remain unresolved. The new contribution is the common fixed-cut bridge from an actual return certificate to the existing alternating-strip obstruction. Global certificate existence remains unresolved. The proof below is a mathematical proof; the new combined endpoint is outside the independently compiled Lean endpoint list.

### 2.1. The exact existing saturation input

The current source already contains the theorem

```lean
Agent2.SaturatedProfile.saturated_overflow_profile
```

in [Agent2SaturatedProfile.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/Agent2SaturatedProfile.lean). Its hypotheses are a finite closed path in the exact three-column prefix transition, bounded coefficients, an actual incoming carry bit at every edge, 和 equality \(2\sum\gamma_i=P\). Its conclusion includes

\[
\gamma_i=(r+i)\bmod2
\qquad(0\le i<P)
\]

for some \(r\in\{0,\ldots,7\}\). 这 is stronger than the separate older theorem asserting only \(8\mid P\).

The exact path is supplied for an accepted return certificate by

```lean
Agent110.CertificateSaturation.certificate_closed_prefix_path
Agent110.CertificateSaturation.path_total_eq_totalGam
```

in [CertificateSaturation.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Agent2SaturatedProfile/CertificateSaturation.lean). The required positive exterior follows from accepted-check automatic admissibility in [AdmissibleHeads.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/CertificateToLychrel/AdmissibleHeads.lean).

For clarity, the saturation argument imports an explicit finite potential certificate, rather than assuming alternation merely from the numerical average. Each exact prefix edge satisfies

\[
82\gamma_i+U(s_{i+1})\le41+U(s_i).
\]

Closure 和 \(2\Gamma=P\) make the sum of the nonnegative edge slacks zero, so every edge is tight. The accompanying clock certificate forces clock advancement by one modulo eight. The nonzero clock values identify seven specified prefix states; the edge from clock seven determines the remaining zero-clock state. Their exterior coefficients alternate between \(8\) 和 \(17\), whose actual terminal carries are respectively zero 和 one. The full current theorem cited above implements these implications. The odd-position inner carry inputs remain unrestricted.

### 2.2. Actual carry slots for one nonoverflow/overflow pair

Consider an actual decimal reverse-add orbit in mirrored column-sum form. At paired time \(j\), let the even-time word be \(q^j\) of width \(L_j\), 和 the following word be \(r^j\) of width \(L_j\), with actual terminal carry zero on the first step 和 one on the second step. Write \(u^j_i\) for the carry into column \(i\) of the even word, \(v^j_i\) for that of the odd word, 和 \(f^j_i\) for its normalized odd-time output digit. Extend the digit convention by \(f^j_{L_j}=1\), the actual overflow digit.

At spatial cut \(0\le i\le L_j\), define

\[
X_i^j=(a_i^j,b_i^j,c_i^j,z_i^j)
=\left(u_i^j,v_i^j,u_{L_j-i}^j,
f^j_{L_j-i}-v^j_{L_j-i}\right).
\]

Widths at different temporal pairs may differ. Every high index in 这 definition uses that pair's own actual width. The first step within a pair emits terminal carry zero, so its even 和 odd source widths agree.

The three stored carries 都 lie in \(\{0,1\}\), 和 \(-1\le z_i^j\le9\). The physical outside cut is always

\[
X_0^j=O:=(0,0,0,0),
\]

因为 the low incoming carries 都 equal zero, the even terminal carry is zero, 和 the odd terminal output digit 和 terminal carry 都 equal one.

For adjacent cuts \(X=X_i^j\), \(Y=X_{i+1}^j\), put

\[
q=q_i^j,\quad r=r_i^j,\quad
e=v^j_{L_j-i},\quad q_+=q_i^{j+1}.
\]

The complete local identities used below are

\[
\begin{aligned}
&0\le q,r\le18,\qquad e\in\{0,1\},\\
&r=Y.z+10e,\\
&r<9\Longrightarrow e=0,\qquad r>9\Longrightarrow e=1,\\
&Y.a=\left\lfloor\frac{q+X.a}{10}\right\rfloor,\\
&r=(q+X.a)\bmod10+(q+Y.c)\bmod10,\\
&Y.b=\left\lfloor\frac{r+X.b}{10}\right\rfloor,\\
&X.c=\left\lfloor\frac{q+Y.c}{10}\right\rfloor,\\
&q_+=(r+X.b)\bmod10+X.z+e,\\
&0\le X.z+e\le9.
\end{aligned}
\tag{1}
\]

The low equations are ordinary carry recurrences. The high even equation uses symmetry of the input column-sum word. The equation for \(r\) is the reflected pairing after the nonoverflow step. The equation for \(q_+\) is the reflected pairing after the overflow step; the extra leading digit shifts the high alignment by one. Finally, if \(w=v^j_{L_j-i-1}\), then

\[
f^j_{L_j-i-1}=r+w-10e,
\quad
Y.z=f^j_{L_j-i-1}-w=r-10e,
\]

which gives the second line of (1). The final inequality holds 因为 \(X.z+e=f^j_{L_j-i}\) is an actual digit.

These are precisely `Agent9.AlternatingScalarBoundary.Tile` 和 its actual specialization `Agent112.TwoPhase.actual_tile`; see the pinned [Core/AlternatingScalarBoundary.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Core/AlternatingScalarBoundary.lean) 和 [ActualInfiniteStrip.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Drafts/Agent112TwoPhaseObstruction/ActualInfiniteStrip.lean).

### 2.3. Four exact fibers

Define the two scalar cuts 和 their exceptional predecessor letters:

\[
S_6=(0,1,0,2),\quad E_6=(0,0,0,3),\qquad
S_{12}=(1,0,1,6),\quad E_{12}=(1,1,1,5).
\]

The following table follows from (1):

| Inner cut \(Y\) | \(q\) | \(r\) | \(e\) | \(X.a\) | \(X.c\) |
|---|---:|---:|---:|---:|---:|
| \(S_6\) | 6 | 12 | 1 | 0 | 0 |
| \(E_6\) | 1 | 3 | 0 | 1 | 0 |
| \(S_{12}\) | 12 | 6 | 0 | 1 | 1 |
| \(E_{12}\) | 17 | 15 | 1 | 0 | 1 |

Each case follows separately:

* For \(Y=S_6\), the identity \(r=2+10e\) 和 \(\lfloor(r+X.b)/10\rfloor=1\) force \(e=1,r=12\). Since \(Y.a=Y.c=0\), the low carry equation gives \(q+X.a\le9\), so the summands in the nonoverflow emission 都 remain unreduced. Thus \(12=2q+X.a\), forcing \(q=6,X.a=0\). The high carry is \(X.c=\lfloor6/10\rfloor=0\).

* For \(Y=E_6\), the identity \(r=3+10e\) 和 \(\lfloor(r+X.b)/10\rfloor=0\) force \(e=0,r=3\). The same low bound \(q+X.a\le9\) makes the emission \(3=2q+X.a\). Therefore \(q=1,X.a=1\), 和 \(X.c=\lfloor1/10\rfloor=0\).

* For \(Y=S_{12}\), the identity \(r=6+10e\) 和 \(\lfloor(r+X.b)/10\rfloor=0\) force \(e=0,r=6\). Now \(Y.a=Y.c=1\), so \(q+X.a\ge10\), hence \(q\ge9\). The quantities \(q+X.a\) 和 \(q+1\) 都 are between ten 和 nineteen. The emission becomes \(6=2q+X.a-19\), forcing \(q=12,X.a=1\). The high carry is \(X.c=\lfloor13/10\rfloor=1\).

* For \(Y=E_{12}\), the identity \(r=5+10e\) 和 \(\lfloor(r+X.b)/10\rfloor=1\) force \(e=1,r=15\). Again \(q+X.a\ge10\) 和 \(q\ge9\), so the emission is \(15=2q+X.a-19\). Therefore \(q=17,X.a=0\), 和 \(X.c=\lfloor18/10\rfloor=1\).

Each high incoming carry is determined by the displayed equations.

### 2.4. Reverse rigidity 和 erasure

First suppose an inner cut equals \(S_6\) at every paired time. Its predecessor cut \(X^j\) obeys the first table row, so \(q^j=6,r^j=12,e^j=1\) for every \(j\). Applying 这 at \(j+1\) gives \(q_+=6\). The overflow emission therefore reads

\[
6=(12+X.b)\bmod10+X.z+1
=3+X.b+X.z.
\]

Thus \(X.b+X.z=3\), 和 \(X^j\) is either \(S_6\) or \(E_6\).

For an inner cut constantly \(S_{12}\), the third row gives \(q^j=12,r^j=6,e^j=0\), 和 the next paired time gives \(q_+=12\). The emission reads

\[
12=6+X.b+X.z.
\]

Thus \(X.b+X.z=6\), 和 \(X^j\) is either \(S_{12}\) or \(E_{12}\).

The exceptional option cannot persist when another spatial predecessor exists.

For the \(6\)-case, suppose \(P^j\to X^j\) is an actual adjacent-cut relation, 和 \(X^j\in\{S_6,E_6\}\). If \(X^j=S_6\), the table gives \(r=12,e=1\), so

\[
q_+=(12+P.b)\bmod10+(P.z+e)\ge2.
\]

If \(X^j=E_6\), the table gives \(r=3,e=0\), so

\[
q_+=(3+P.b)\bmod10+(P.z+e)\ge3.
\]

The inequalities 都 use the actual digit bound \(P.z+e\ge0\). If \(X^{j+1}=E_6\), the second fiber row at the next time would require \(q_+=1\), contradicting either inequality. Consequently \(X^{j+1}=S_6\).

For the \(12\)-case, if \(X^j=S_{12}\), then \(r=6,e=0\), 和

\[
q_+=(6+P.b)\bmod10+(P.z+e)\le7+9=16.
\]

If \(X^j=E_{12}\), then \(r=15,e=1\), 和

\[
q_+=(15+P.b)\bmod10+(P.z+e)\le6+9=15.
\]

These bounds 都 use \(P.z+e\le9\). If \(X^{j+1}=E_{12}\), the fourth row at that time would require \(q_+=17\), contradicting either upper bound. Consequently \(X^{j+1}=S_{12}\).

### 2.5. Quantitative finite-strip obstruction

Consider a strip with spatial cuts \(0,\ldots,W\), the actual outside cut \(O\) at cut zero, 和 a constant cut \(S_6\) or \(S_{12}\) at cut \(W\) for \(D\) consecutive paired times. Every adjacent cut obeys (1). Then

\[
D\le2W-1\qquad(W\ge1).
\tag{2}
\]

Here is the complete induction. For \(W=1\), if \(D\ge2\), reverse rigidity at the first time forces the outside cut to belong to \(\{S_6,E_6\}\) or \(\{S_{12},E_{12}\}\). But \(O=(0,0,0,0)\) belongs to neither set. Thus \(D\le1\).

For \(W\ge2\), suppose \(D\ge2W\). Reverse rigidity makes cut \(W-1\) a scalar or exceptional letter through times \(0,\ldots,D-2\); the final time is omitted 因为 rigidity uses the next temporal fiber. Erasure, using the additional predecessor cut \(W-2\), makes cut \(W-1\) exactly the scalar letter at times \(1,\ldots,D-2\). Restrict the shorter strip to 这 temporal interval. Its duration is \(D-2\ge2(W-1)\), contradicting the induction hypothesis for spatial width \(W-1\). 这 proves (2).

For actual words, two adjacent coefficients equal to six at every even time 和 twelve at every odd time give the scalar cut \(S_6\). The column before the cut fixes each low carry; the symmetric column after the cut fixes each high carry. Six resets carry to zero, 和 twelve resets it to one. The odd normalized high digit is \((12+1)\bmod10=3\), hence \(z=3-1=2\). Thus the slot is exactly \((0,1,0,2)\).

When the adjacent coefficients instead equal twelve at even times 和 six at odd times, the reset carries are one 和 zero. The odd normalized high digit is \((6+0)\bmod10=6\), hence \(z=6-0=6\). The slot is exactly \((1,0,1,6)\).

The existing exact endpoint (2) for actual words is `P196.Agent4.TemporalStrip.ActualWord.actual_band_duration_bound` in [ActualWordStrip.lean](https://github.com/taco-jpg/p196-algorithm/blob/c6902ac6c366ce018e68a810f58b400dda07145a/lean/P196/Drafts/Agent4SaturationLift/ActualWordStrip.lean). It requires only initial admissibility, \(0<W<L_0\), actual alternating overflows on the finite segment, 和 the stated two adjacent fixed-depth coefficients. It assumes neither a temporal return nor an abstract freely chosen carry path.

### 2.6. The new common fixed-cut bridge

Index the certificate states cyclically by \(i\in\{0,\ldots,P-1\}\). Write their exterior blocks as \(B_i\), their phases as \(c_i\), 和 the actual outer-band increments as

\[
\delta_i=\gamma_i+j_i+j_{1,i}-2.
\]

The checker requires the exact inequality

\[
\ell_{i+1}\le\ell_i+\delta_i
\]

for the outer lower bounds, with cyclic indexing. Summing gives

\[
\Delta:=\sum_{i=0}^{P-1}\delta_i\ge0.
\]

Define finite prefix sums \(S_0=0\), \(S_i=\sum_{h<i}\delta_h\). Let

\[
M=\max_{i<P}|B_i|,\qquad W=M+2.
\]

Choose an integer initial outer-band length \(G_0\) satisfying

\[
G_0\ge\ell_0,
\qquad
G_0\ge\max_{i<P}\bigl(W+1-|B_i|-S_i\bigr).
\tag{3}
\]

Choose the initial inner-band length at least its checker lower bound. Accepted-check automatic admissibility 和 `template_realized` provide an ordinary integer with 这 exact template. Repeated application of the already established exact whole-template step 和 trimming identities gives the actual orbit. Its outer-band length at time \(t=aP+i\) is

\[
G_t=G_0+S_i+a\Delta.
\tag{4}
\]

Every intermediate outer 和 inner length remains above its checker lower bound, by induction on the local lower-bound inequalities. Equation (4) therefore uses ordinary integer subtraction on admissible band lengths.

Equations (3) 和 (4), together with \(\Delta\ge0\), imply

\[
|B_i|\le M=W-2<W-1<W<|B_i|+G_t.
\]

The **same two column positions**, \(W-1\) 和 \(W\), consequently lie strictly within the outer constant band at every time. The coefficients 都 equal \(c_i\). The integer width is greater than \(W\), already at time zero, 和 widths never decrease.

这 is the missing alignment argument. Merely knowing that every state 有 a long band would be insufficient: (3) explicitly chooses one common finite cut that survives the entire sequence of changing exterior widths 和 band lengths. The argument also works when \(\Delta=0\).

### 2.7. Contradiction 和 scope

Assume an accepted \(6/12\) certificate satisfies \(2\Gamma=P\). Section 2.1 supplies alternation of its actual overflow bits. The phase transition is

\[
6\mapsto12\mapsto6,
\]

so \(P\) is even 和 the cyclic continuation preserves the temporal alternation. Shift the actual orbit by zero or one step so every even transition emits terminal carry zero 和 every odd transition emits terminal carry one. The fixed-cut property established in Section 2.6 continues to hold after 这 shift.

At the two fixed columns, the phase is either always \((6,12)\) on paired times or always \((12,6)\). Take the finite segment of \(D=2W\) paired times, namely \(4W\) ordinary transitions. Equation (2) gives

\[
2W\le2W-1,
\]

a contradiction. The existing exterior carry budget already gives \(2\Gamma\le P\), so equality is excluded 和 \(2\Gamma<P\) follows. Since \(P\) is even, the equivalent integral bound is \(2\Gamma\le P-2\).

这 uses a finite segment whose size is explicitly determined by the largest exterior block. The contradiction follows from the finite exact carry argument. Acceptance with \(2\Gamma<P\) remains unresolved. The six-phase class cannot be substituted into the proof: its even-time bulk phases rotate through \(2,8,14\) or \(4,16,10\), rather than staying constant. The scalar reverse-rigidity argument then changes, 和 exceptional predecessor letters can remain viable.


## 3. LEAN-VERIFIED — eliminate the lower-bound search variables

Hold the symbolic states 和 trimming counts fixed. Define signed increments

\[
d_i=\gamma_i+j_i+j_{1,i}-2,
\qquad e_i=\gamma_i+j_{2,i}+k_i-2,
\qquad D=\sum_{i<P}d_i,\quad E=\sum_{i<P}e_i.
\]

**LEAN-VERIFIED:** the four original natural-number lower-bound clauses can be filled iff \(D\ge0\) 和 \(E\ge0\). 这 is the exact statement `Agent218.ThresholdFeasibility.thresholdsFit_iff`; the source is `lean/P196/Agent218CertificateAudit/ThresholdFeasibility.lean`.

**THEOREM — complete proof.** For one coordinate the constraints are \(\ell_i\ge2\) 和 \(\ell_{i+1\bmod P}\le\ell_i+d_i\). Summation gives \(D\ge0\). Conversely set \(p_0=0\), \(p_i=\sum_{t<i}d_t\), \(M=2-\min_{0\le i<P}p_i\), 和 \(\ell_i=M+p_i\). Each threshold is an integer at least 2. Every edge before the last satisfies equality. The last edge satisfies

\[
\ell_0=M\le M+D=\ell_{P-1}+d_{P-1}.
\]

Applying 这 construction to \(d\) 和 \(e\) independently supplies the original lower-bound fields. The feasibility conditions separate by coordinate.

**THEOREM — pointwise least thresholds.** Let

\[
S_i(r)=\sum_{t=0}^{r-1}d_{(i+t)\bmod P},\qquad S_i(0)=0.
\]

For \(D\ge0\), the exact least feasible thresholds are

\[
\boxed{\ell_i^*=2-\min_{0\le r<P}S_i(r).}
\]

Any feasible vector obeys \(\ell_i\ge2-S_i(r)\), by iterating its inequalities for \(r\) edges, so it dominates \(\ell^*\). Conversely

\[
\ell^*_{i+1}-d_i
=2-\min_{1\le r\le P}S_i(r)
\le2-\min_{0\le r<P}S_i(r)=\ell_i^*.
\]

The inequality holds 因为 the first set replaces \(S_i(0)=0\) by \(S_i(P)=D\ge0\). Every future time is \(mP+r\), whose gain equals \(mD+S_i(r)\); hence the same formula is the sharp safe starting length for indefinite repetition. If \(D<0\), lengths at times \(mP\) eventually cross the floor for every finite start. The displayed argument establishes the least-threshold formula; the Lean module formalizes feasibility 和 the exact checker specialization.

**THEOREM — audit implication.** A negative net gain in either coordinate kills that exact cyclic transition list. Enlarging the initial runs or replacing the rectangular threshold invariant with a more elaborate invariant cannot rescue its indefinitely repeated negative drift. Conversely nonnegative net gains guarantee explicit feasible thresholds. The unresolved conditions are the exact returning blocks 和 safety checks.

## 4. LEAN-VERIFIED / THEOREM — a sound extension of trimming

The original local syntax permits stripping band letters from a raw returned block. It can reject a legitimate equality when the selected next-state representative puts additional band letters inside a finite block. 这是 a representational limitation. Whether every wider cycle can be re-encoded as an old cycle remains unresolved.

**LEAN-VERIFIED — common-padding equality.** Put \(c'=2t(c)\), \(d'=18-c'\). Allow nonnegative padding counts \(r,r_1,r_2,r_k,j,j_1,j_2,k\), 和 check

\[
\begin{aligned}
B_r(c')^r&=B'(c')^j,\\
(c')^{r_1}A_r(d')^{r_2}&=(c')^{j_1}A'(d')^{j_2},\\
(d')^{r_k}C_r(d')^{r_k}&=(d')^kC'(d')^k.
\end{aligned}
\tag{R}
\]

Then, for arbitrary natural \(u,v\),

\[
\mathcal T_{(c',B_r,A_r,C_r)}(u+r+r_1,v+r_2+r_k)
=\mathcal T_{(c',B',A',C')}(u+j+j_1,v+j_2+k).
\]

**Proof.** Apply the original `template_trim` equality once on each side; (R) identifies their padded finite blocks exactly. 这 proof contains only natural exponents. `template_reframe` 和 `stepWord_template_reframe` formalize 这 identity 和 its composition with actual normalization in `TemplateReframe.lean`.

**THEOREM — exact soundness conditions for a wider cycle checker.** Require a nonempty cycle, \(P>0\), 和 retain legal phases, bounded blocks, the phase update, 和 `¬StepPal`. Replace the original block equalities by (R). At each link impose

\[
\begin{aligned}
&\ell_i,h_i\ge2,\\
&2+r_i+r_{1,i}\le\ell_i+\gamma_i,\qquad
2+r_{2,i}+r_{k,i}\le h_i+\gamma_i,\\
&\ell_{i+1}+2+r_i+r_{1,i}
 \le\ell_i+\gamma_i+j_i+j_{1,i},\\
&h_{i+1}+2+r_{2,i}+r_{k,i}
 \le h_i+\gamma_i+j_{2,i}+k_i.
\end{aligned}
\tag{G}
\]

Require an admissible initial center 和 exterior, using the original `Admissible0` predicate. These explicit hypotheses suffice with the current realization theorem.

For actual current lengths \(G\ge\ell_i\), \(H\ge h_i\), the original exact step yields raw lengths \(G-2+\gamma_i\), \(H-2+\gamma_i\). The first guards in (G) make

\[
u=G-2+\gamma_i-r_i-r_{1,i}\ge0,\qquad
v=H-2+\gamma_i-r_{2,i}-r_{k,i}\ge0.
\]

Identity (R) gives next lengths

\[
G'=G+\gamma_i-2+j_i+j_{1,i}-r_i-r_{1,i},\qquad
H'=H+\gamma_i-2+j_{2,i}+k_i-r_{2,i}-r_{k,i}.
\]

The remaining guards give \(G'\ge\ell_{i+1}\), \(H'\ge h_{i+1}\). Realize the initial template using `template_realized`, then induct over actual steps. Every source retains lengths at least 2; `step_palindrome_template` 和 `¬StepPal` therefore exclude every successor palindrome. Taking the first successor as the seed proves the wider criterion sound. 这 criterion is a mathematical theorem built from the compiled local equalities. The full wider cyclic criterion is stated here as a paper theorem.

**LEAN-VERIFIED — a strict local syntax example.** For \(G\ge3\), \(H\ge2\),

\[
T\bigl(\mathcal T_{(2,[],[],[])}(G,H)\bigr)
=\mathcal T_{(4,[4,4],[5,13],[14,14])}(G-3,H-2).
\]

Here the actual raw blocks are \(B_r=[4]\), \(A_r=[5,13]\), \(C_r=[14,14]\), 和 \(\gamma=0\). The old requirement \([4]=[4,4]4^j\) is impossible by length. Taking \(r=1\), with every other padding count zero, gives (R). Endpoints `reframe_witness` 和 `reframe_witness_no_old_trim` check the identity 和 its rejection by the old local syntax. Its scope is a single transition. To retain next-state band lengths at least 2, take \(G\ge5\), \(H\ge4\).

## 5. LEAN-VERIFIED — The obstruction to extending scalar erasure

Use exactly the `Slot`, `Tile`, 和 `Step` relations of Section 2. Let the following traces repeat with temporal period 3:

\[
\begin{aligned}
S&=[(0,0,0,4),(0,1,0,6),(1,1,1,0)],\\
X&=[(0,1,0,3),(0,0,0,7),(1,0,1,1)],\\
Y&=[(1,0,0,-1),(1,0,0,3),(0,0,1,5)].
\end{aligned}
\]

The trace \(S\) belongs to constant bulk with successive even phases \(2,8,14\), followed by odd phases \(4,16,10\). **LEAN-VERIFIED:** \(\operatorname{Step}(Y,X)\), \(\operatorname{Step}(X,S)\), 和 \(X(j)\ne S(j)\) at every time. In particular the analogue of the scalar one-shift erasure claim is false.

The complete tile witnesses, including the temporal wrap, are:

| Spatial relation | \(j\bmod3\) | \(q\) | \(r\) | \(e\) | \(q_+\) |
|---|---:|---:|---:|---:|---:|
| \(X\to S\) | 0 | 2 | 4 | 0 | 8 |
| \(X\to S\) | 1 | 8 | 16 | 1 | 14 |
| \(X\to S\) | 2 | 14 | 10 | 1 | 2 |
| \(Y\to X\) | 0 | 6 | 13 | 1 | 3 |
| \(Y\to X\) | 1 | 3 | 7 | 0 | 10 |
| \(Y\to X\) | 2 | 10 | 1 | 0 | 6 |

Each row satisfies every bound, carry recurrence, reflected emission, pending-digit condition, 和 forcing condition in (1). For example the last row emits \(r=(10+0)\bmod10+(10+1)\bmod10=1\), then \(q_+=(1+0)\bmod10+5+0=6\); its high even carry is \(\lfloor(10+1)/10\rfloor=1\). The Lean proof checks each of the six concrete tiles independently 和 extends them by reduction modulo 3. `shifted_erasure_false` records the refuted universal claim.

**THEOREM — scope of the counterexample.** These traces are a local strip construction. They supply neither a full path from the physical outside cut nor an ordinary integer orbit. They refute the proposed erasure generalization, without establishing acceptance of any return certificate. A stronger six-phase spatial invariant must admit these viable non-erasing predecessors.

## 6. THEOREM — finite regression statements 和 reproducibility

The following deterministic checks validate four specified arithmetic fixtures for 1000 ordinary reverse-add steps each, the local reframe identity, the sharp threshold example for 1000 transitions from each phase, 和 the six-phase strip counterexample for 1000 temporal pairs. Each normalized column word is compared with independently calculated ordinary integer addition. The four fixtures cover initial overflow values zero 和 one, empty finite blocks, nonempty interface blocks, 和 odd-length centers.

The observed `first_palindrome=None` values mean only that the palindrome count of each named fixture equals zero through the tested time 1000. Their infinite-time behavior remains unresolved.

### Reproduction code

Save the following as `check_218.py`, then run `python3 check_218.py`:

```python
from hashlib import sha256


def digits(n):
    return [int(x) for x in str(n)[::-1]]


def value(d):
    return sum(x * 10**i for i, x in enumerate(d))


def reverse(n):
    return int(str(n)[::-1])


def pair(d):
    return [x + y for x, y in zip(d, reversed(d))]


def norm(w, carry=0):
    out = []
    for q in w:
        out.append((q + carry) % 10)
        carry = (q + carry) // 10
    return out, carry


def normalized(w):
    out, carry = norm(w)
    return out + ([carry] if carry else [])


def template(c, B, A, C, G, H):
    left = B + [c] * G + A + [18 - c] * H
    return left + C + left[::-1]


def raw(c, B, A, C):
    d = 18 - c
    kc, kd = int(c >= 10), int(d >= 10)
    tc, td = c - 9 * kc, d - 9 * kd
    DB, e0 = norm(B, 0)
    DA, e1 = norm(A, kc)
    DC, e2 = norm(C, kd)
    DRA, e3 = norm(A[::-1], kd)
    DRB, gamma = norm(B[::-1], kc)
    u0, u1 = c + e0 - 10 * kc, d + e1 - 10 * kd
    u2, u3 = d + e2 - 10 * kd, c + e3 - 10 * kc

    def plus(x, y):
        assert len(x) == len(y)
        return [a + b for a, b in zip(x, y)]

    if gamma == 0:
        X1, X5 = DB + [u0], [tc] + DRB
        X2, X4 = [tc] + DA + [u1], [td] + DRA + [u3]
        X3 = [td] + DC + [u2]
    else:
        X1, X5 = DB + [u0], DRB + [1]
        X2, X4 = DA + [u1], DRA + [u3]
        X3 = DC + [u2]
    Br, Ar, Cr = plus(X1, X5[::-1]), plus(X2, X4[::-1]), pair(X3)
    pal = X1 == X5[::-1] and X2 == X4[::-1] and X3 == X3[::-1]
    return 2 * tc, Br, Ar, Cr, gamma, pal


def realize(q):
    assert q == q[::-1] and q[0] > 0
    D = [0] * len(q)
    for i in range(len(q) // 2):
        D[i] = max(0, q[i] - 9)
        D[-1 - i] = min(9, q[i])
    if len(q) % 2:
        assert q[len(q) // 2] % 2 == 0
        D[len(q) // 2] = q[len(q) // 2] // 2
    assert pair(D) == q and D[-1] > 0
    return value(D)


fixtures = [
    (2, [], [], [], 5, 4),
    (12, [], [], [], 4, 5),
    (6, [10], [0, 18], [8], 4, 4),
    (8, [1, 9, 17], [0, 18], [3, 8, 3], 4, 5),
]
for index, (c, B, A, C, G, H) in enumerate(fixtures):
    q = template(c, B, A, C, G, H)
    cp, Br, Ar, Cr, gamma, pal = raw(c, B, A, C)
    out = normalized(q)
    assert pair(out) == template(cp, Br, Ar, Cr, G - 2 + gamma, H - 2 + gamma)
    assert (out == out[::-1]) == pal
    seed = n = realize(q)
    first_palindrome = None
    for t in range(1001):
        D = digits(n)
        if D == D[::-1] and first_palindrome is None:
            first_palindrome = t
        if t < 1000:
            new = n + reverse(n)
            assert normalized(pair(D)) == digits(new)
            n = new
    print(f"fixture {index}: seed={seed}, initial_gamma={gamma}, "
          f"first_palindrome={first_palindrome}, steps=1000, "
          f"final_digits={len(str(n))}, sha256={sha256(str(n).encode()).hexdigest()}")

for G, H in [(5, 4), (6, 7), (11, 9)]:
    source = template(2, [], [], [], G, H)
    assert pair(normalized(source)) == template(4, [4, 4], [5, 13], [14, 14], G - 3, H - 2)
assert raw(2, [], [], [])[1] == [4]
assert len([4]) < len([4, 4])
print("PASS: exact reframing identity; old raw block [4] cannot trim to [4, 4].")


def least_thresholds(d, floor=2):
    assert d and sum(d) >= 0
    answer = []
    for i in range(len(d)):
        partial = smallest = 0
        for r in range(len(d) - 1):
            partial += d[(i + r) % len(d)]
            smallest = min(smallest, partial)
        answer.append(floor - smallest)
    return answer


d = [-2, 3, -1, 1]
lo = least_thresholds(d)
assert all(lo[(i + 1) % len(d)] <= lo[i] + d[i] for i in range(len(d)))
endpoints, first_failures = [], []
for i in range(len(d)):
    x, bad = lo[i], lo[i] - 1
    failure = 0 if bad < 2 else None
    for t in range(1000):
        x += d[(i + t) % len(d)]
        bad += d[(i + t) % len(d)]
        assert x >= 2
        if bad < 2 and failure is None:
            failure = t + 1
    assert failure is not None
    endpoints.append(x)
    first_failures.append(failure)
print(f"thresholds: increments={d}, least={lo}, steps_per_phase=1000, "
      f"endpoints={endpoints}, one_below_first_failure={first_failures}")

S = [(0, 0, 0, 4), (0, 1, 0, 6), (1, 1, 1, 0)]
X = [(0, 1, 0, 3), (0, 0, 0, 7), (1, 0, 1, 1)]
Y = [(1, 0, 0, -1), (1, 0, 0, 3), (0, 0, 1, 5)]


def valid(s):
    a, b, c, z = s
    return a in (0, 1) and b in (0, 1) and c in (0, 1) and -1 <= z <= 9


def tile(o, i, q, r, e, qn):
    a, b, c, z = o
    A, B, C, Z = i
    return (valid(o) and valid(i) and 0 <= q <= 18 and 0 <= r <= 18
            and e in (0, 1) and r == Z + 10 * e
            and (r >= 9 or e == 0) and (r <= 9 or e == 1)
            and (q + a) // 10 == A and (q + a) % 10 + (q + C) % 10 == r
            and (r + b) // 10 == B and c == (q + C) // 10
            and qn == (r + b) % 10 + z + e and 0 <= z + e <= 9)


for j in range(1000):
    k = j % 3
    assert tile(X[k], S[k], [2, 8, 14][k], [4, 16, 10][k], [0, 1, 1][k], [8, 14, 2][k])
    assert tile(Y[k], X[k], [6, 3, 10][k], [13, 7, 1][k], [1, 0, 0][k], [3, 10, 6][k])
    assert X[k] != S[k]
print("PASS: 1000 temporal pairs, 2000 exact tiles, X differs from S at every phase.")
print("Scope: fixtures test arithmetic; the strip counterexample is local; no accepted return certificate is asserted.")
```

### Actual output

```text
fixture 0: seed=222229999777700000, initial_gamma=0, first_palindrome=None, steps=1000, final_digits=437, sha256=3f1b0cf24b168da9302019de5c2d5f7897dd874870b8c925e482dd63c3e28595
fixture 1: seed=999966666000003333, initial_gamma=1, first_palindrome=None, steps=1000, final_digits=437, sha256=93f8e6b3f81e9b34582780f8044f994c5a8708d9c4b88abee3dc76610c6803c8
fixture 2: seed=96666099999433339000001, initial_gamma=1, first_palindrome=None, steps=1000, final_digits=445, sha256=dc68b43f429daea4972fe24bb5cf4051e7f73a0a425b74517d6e24d9649fd30a
fixture 3: seed=1998888099999934011111900000800, initial_gamma=0, first_palindrome=None, steps=1000, final_digits=447, sha256=7aa59343dde1f448c76dd6aa7e1927ce60ea67dfd76c7a9670016c7eae2190f8
PASS: exact reframing identity; old raw block [4] cannot trim to [4, 4].
thresholds: increments=[-2, 3, -1, 1], least=[4, 2, 4, 3], steps_per_phase=1000, endpoints=[254, 252, 254, 253], one_below_first_failure=[1, 0, 3, 2]
PASS: 1000 temporal pairs, 2000 exact tiles, X differs from S at every phase.
Scope: fixtures test arithmetic; the strip counterexample is local; no accepted return certificate is asserted.
```

### LEAN-VERIFIED endpoints

The new registered project contains three modules:

| Module | Endpoints |
|---|---|
| `ThresholdFeasibility.lean` | `feasible_iff_total_nonnegative`, `two_band_feasible_iff`, `thresholdsFit_iff` |
| `TemplateReframe.lean` | `template_reframe`, `stepWord_template_reframe`, `reframe_witness`, `reframe_witness_no_old_trim` |
| `SixPhaseCounterexample.lean` | `step_XS`, `step_YX`, `everywhere_ne`, `shifted_erasure_false` |

Each module uses the existing repository arithmetic. The axiom audit permits only `propext`, `Classical.choice`, 和 `Quot.sound`; the threshold 和 strip-counterexample endpoints use only `propext` 和 `Quot.sound`. The saturated-certificate exclusion in Section 2 和 the full wider-checker soundness theorem in Section 4 are paper proofs. Their new combined endpoints are outside the compiled endpoint list.

Repository verification command:

```bash
python3 tools/verify.py --changed c6902ac6c366ce018e68a810f58b400dda07145a
```

Actual verification summary, preserving the relevant output lines:

```text
[rules] 4826 Lean files, 288 projects, OK
[changed] against c6902ac6c366ce018e68a810f58b400dda07145a: 3 new/changed Lean file(s); building 3 module(s); auditing 1 project(s)
[build] up to 1 Lean file(s) at a time
[build] OK
[axioms] 11 endpoints checked
ALL CHECKS PASSED (changed files only, against c6902ac6c366ce018e68a810f58b400dda07145a)
```

## 7. IDEA — sharpest remaining question

**Does the unchanged checker accept any cycle after the saturated \(6/12\) subfamily is removed?** Equivalently for a fixed candidate structural cycle, can the exact block return equalities 和 `¬StepPal` hold with nonnegative gains? Threshold selection is fully settled by Section 3; seed realizability is already settled by the existing bridge. The remaining cases are unsaturated \(6/12\) returns 和 six-phase returns. Even the saturated six-phase case requires a spatial argument stronger than scalar erasure, as the explicit counterexample establishes.

**IDEA — precise next lemma.** Characterize finite spatial paths from the physical outside trace \((0,0,0,0)\) to either six-phase bulk trace under the actual alternating-overflow relation, allowing the period-three predecessors in Section 5. An exclusion would remove the remaining saturated phase family. A surviving abstract path would still require whole-word realization, returning interfaces, center closure, 和 perpetual palindrome avoidance before it could support an accepted certificate.
