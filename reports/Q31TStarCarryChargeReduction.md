# Q31: T* width-independent carry-charge reduction

**Label: PAPER PROOF (conditional necessary-condition reduction).** This report supplies a width-independent mod-5 gate for a phase-lifted T* return. It is not a decimal Lychrel certificate and does not exclude every T* construction.

## Exact missing-lemma contribution

For a 120-phase candidate whose intermediate words retain a rooted, mirrored U3 bulk with exponent \(k+\delta_t\), fixed finite phase collars, and the Q01 complementary-carry law, the global mod-5 carry-count condition reduces to one finite 120-phase collar equation independent of the pumped width \(k\). The remaining gap is a physical full-interface return satisfying that equation, both carry ports, the overflow clock, and the phasewise nonpalindrome guard.

## 1. Hypotheses and notation

At phase \(t\), write the canonical symmetric pair-coefficient word as
\[
P_t(k)=H_t(k)\,C_t\,H_t(k)^R,
\]
where the phase-dependent finite words and the phase offsets are independent of \(k\), and \(H_t(k)\) contains a mirrored bulk \(U_t^{\,k+\delta_t}\) with \(|U_t|=3\). Assume \(k\ge k_0\) is large enough that every \(k+\delta_t\ge3\). The \(U_t\) are among the 30 charge-zero rotations of \((9,a,18-a)\), \(a\in\{0,2,\ldots,18\}\). The centre word \(C_t\) may change with phase, including its length parity, but is fixed as \(k\) varies. This is a **conditional phase-lift hypothesis**, not a claim that every candidate already has this form.

Let \(L_t=|P_t|\), \(\gamma_t\in\{0,1\}\) be the actual overflow, and \(c_{t,i}\) the incoming carry at coefficient \(i\). Define
\[
S_t=\sum_{i=0}^{L_t-1}P_t[i],\qquad
M_t(k)=\sum_{i=0}^{L_t-1}c_{t,i}.
\]
Thus \(M_t\) is the number of incoming one-carries in the full low-to-high normalization; it is not the centre word \(C_t\).

## 2. The mod-5 recurrence and its 120-phase consequence

For the ordinary column equations
\[
e_{t,i}=P_t[i]+c_{t,i}-10c_{t,i+1},
\qquad c_{t,0}=0,\quad c_{t,L_t}=\gamma_t,
\]
summing the output digits, including the possible leading overflow digit, gives
\[
S_{t+1}=2S_t-18\bigl(M_t(k)+\gamma_t\bigr).
\]
Consequently
\[
S_{t+1}\equiv 2S_t+2\bigl(M_t(k)+\gamma_t\bigr)\pmod 5.
\]
Iterating 120 steps, using \(2^{120}\equiv1\pmod5\), gives
\[
S_{120}-S_0\equiv
2\sum_{t=0}^{119}2^{119-t}\bigl(M_t(k)+\gamma_t\bigr)\pmod5.
\]

For the proposed endpoint \(P_0(q,k)\to P_{120}(q,k+5)\), the endpoint word has the same \(B,W,J,U,C\), with \(q\) fixed and five extra copies of \(U\) on each side. Since \(\sum U=27\),
\[
S_{120}-S_0=2\cdot5\cdot27=270\equiv0\pmod5.
\]
The overflow clock is \(g=(100010001000)^{10}\). Its 30 ones occur exactly at phases \(t\equiv0\pmod4\). For \(w_t=2^{119-t}\pmod5\), the phase weights are \(3,4,2,1\) for \(t\bmod4=0,1,2,3\). Therefore
\[
\sum_{t=0}^{119}w_t\gamma_t=30\cdot3=90\equiv0\pmod5,
\qquad
\sum_{t=0}^{119}w_t=30(3+4+2+1)=300\equiv0\pmod5.
\]
It follows that every such return must satisfy the exact necessary gate
\[
\boxed{\sum_{t=0}^{119}w_t M_t(k)\equiv0\pmod5.}
\]

## 3. Removing the pumped-width variable

The Q01 all-width complementary-carry lemma says that in each protected U3 bulk, every carry cut in each interior copy pairs with its reflected cut to sum to one. For a bulk exponent \(k+\delta_t\), all but two boundary copies are covered. There are three coefficient positions per interior copy, so the bulk contributes exactly \(3(k+\delta_t-2)\) one-carries across each mirrored pair of cuts. The remaining cuts belong to fixed finite collars and boundary copies; the carry-reset property makes their total independent of \(k\).

Hence, for every phase \(t\),
\[
M_t(k)=3(k+\delta_t)+b_t=3k+d_t,
\]
for integers \(b_t,d_t\) fixed by that phase's collar and carry state. Substituting this into the boxed gate and using \(\sum w_t\equiv0\pmod5\) yields the **width-independent finite condition**
\[
\boxed{\sum_{t=0}^{119}w_t d_t\equiv0\pmod5.}
\]
A phase-lifted candidate that fails this condition is impossible for every sufficiently large \(k\), not merely at tested widths. Passing it is necessary, not sufficient: it does not certify the complete seam or centre return.

## 4. Cross-gate audit: mod 13 and mod 99

For the endpoint family,
\[
L(q,k)=2(34+9q+|J|+3k)+|C|.
\]
Changing \(q\) by one changes \(L\) by 18; changing \(k\) by one changes it by 6. Since \(10^6\equiv1\pmod{13}\), the prefactor \(10^{L(q,k)-1}\pmod{13}\) in Z59's reported endpoint cocycle is constant across all \(q,k\) for fixed \(J,C\). This removes a spurious width-dependent prefactor, but it does **not** decide the weighted carry moment. The current FEED statement does not by itself specify the full definitions and endpoint convention for \(Q_t,G_t,\kappa_t\), so this report does not promote that cocycle to a hard pruning rule.

There is also an unconditional scalar mod-99 identity for the stated clock. For any \(L\)-digit integer \(N\),
\[
\operatorname{rev}(N)\equiv10^{L-1}N\pmod{99},
\]
so one reverse-and-add step multiplies \(N\) by 2 modulo 99 when \(L\) is odd, and by 11 when \(L\) is even. The 120-phase clock has 60 odd-length and 60 even-length steps, regardless of starting parity. Thus
\[
N_{120}\equiv2^{60}11^{60}N_0\equiv55N_0\pmod{99}.
\]
This scalar identity gives \(N_{120}\equiv N_0\pmod9\) and \(N_{120}\equiv0\pmod{11}\). The mod-9 endpoint condition is already compatible with the coefficient-sum change 270. This scalar identity **does not by itself prove** Q54's stronger midpoint/junction equation; that equation needs its own explicit carry-reset, midpoint, overflow-lag, and independent-\(k\) proof before it can safely prune candidates.

## 5. Mod-11 parity and the Q54 caution

The current main result Q36TStarOddCentreScrewGate independently derives the phase-resolved odd-centre equations
\[
A(C_t)=A(U_t),\qquad
2A(J_t)+(-1)^{|J_t|}A(U_t)=-2A(B_t)\pmod{11},
\]
under its stated independent-parity and rooted-exterior hypotheses, where \(A(X)=\sum_i(-1)^iX_i\). Combined with the U3 40-step screw phase, it proves that a **single fixed odd centre** cannot satisfy the required centre charges at phases 0, 40, and 80. Phase-varying centres remain possible. Even-length centres are outside this gate and must not be pruned by it.

Q54's different proposed midpoint gate is still not established by that result. If the Q54 gate were separately proved, then \(u=\operatorname{val}_{10}(U)/9\equiv5A(U)\pmod{11}\) would turn it into
\[
2A(J)-(-1)^{|J|}A(U)\equiv0\pmod{11}.
\]
Combining that equation with the odd-centre Q39 gates would force \(A(U)=A(C)=A(J)=0\pmod{11}\), leaving \(U=(9,8,10)\) or \(U=(10,8,9)\). **This is conditional algebra, not a validated physical filter.** Do not apply it to even centres or before the missing Q54 derivation is supplied.

## Scope and remaining gap

The proved result is the width-independent mod-5 gate for the stated phase-lifted U3 subclass, plus the scalar residue audit above. It does not establish that a suitable phase lift exists, that its finite collars return, or that every intermediate integer is non-palindromic. The remaining construction problem is an exact rooted 120-step two-ended seam/carry/centre return with \(q\) fixed, \(k\mapsto k+5\), positive growth, and a phasewise nonpalindrome guard.