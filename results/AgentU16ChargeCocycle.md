# Agent U16: full-pairword Q999 carry cocycle

**PAPER PROOF.** For every genuine decimal pairword P of length n, physical carries c_0=0,...,c_n=g, and kappa=sum_j c_j 10^(-j) modulo 999, the next pairword satisfies Q999(P')=(1+10^g)Q999(P)-99*10^(n-1+g)*kappa modulo 999, where Qm(P)=sum_i P_i 10^i modulo m.

The proof expands the exact paired output digits and telescopes the low/high carry sums. Hence Q9(P')=2Q9(P) modulo 9 and Q99(P')=(1+10^g)Q99(P) modulo 99; the latter only recovers the known odd-centre Q39 gate, while even centres remain unpruned.

For the rooted 120-step clock, the macro multipliers are 1 modulo 9, 55 modulo 99, and 73 modulo 999. Any T* return must satisfy (Q999(target)-73*Q999(source))/9 + 11*S = 0 modulo 111, with S the physical carry cocycle; this is necessary, not sufficient.

For H'=H U^5 and P=H C reverse(H), the target charge shift is 5*10^|H|*(Q999(U)+10^|C|Q999(reverse(U))) modulo 999. Across all 30 charge-zero U3 rotations, exactly one centre-length class preserves this template charge: rotation r=0,1,2 requires |C| congruent to 1,2,0 modulo 3, respectively.

Independent big-integer, fresh-buffer digit-array, and R30-style divmod arithmetic checks verify every step at q=20,40,80,160 and k=4q for three rooted phase-0 controls. No full return, uniform seam obstruction, or decimal Lychrel certificate is claimed.
