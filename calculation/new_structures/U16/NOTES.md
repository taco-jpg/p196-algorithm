# U16 running notes

## 2026-10-28 / 2026-10-29 session

- Read AGENTS.md, OPEN_PROBLEMS.md, docs/FOCUS_SWARM.md, AUDIT_N.md, AUDIT_Nseries.md, FORMATS.md, and the requested #475 and historical #474 comment ranges. Posted the #475 CLAIM and first FEED.
- R05 already covers a mod-9/11/99/101 carry-cocycle route. U16 is specifically the full-pairword mod-999 / mod-111 cocycle extension, not a replacement for R05. Agent3CentreBoundaryFlux covers a half-word boundary flux modulo 99; no exact full-pairword Q999 recurrence was found in repository search.
- For a genuine symmetric pairword P of length n, physical carries c_0=0,...,c_n=g, and kappa=sum_j c_j 10^(-j) modulo 999, expansion of paired output digits gives Q999(P')=(1+10^g)Q999(P)-99*10^(n-1+g)*kappa modulo 999.
- Projections: Q9(P')=2Q9(P) modulo 9 and Q99(P')=(1+10^g)Q99(P) modulo 99. For the 120-step p12 clock (90 g=0 and 30 g=1), multipliers are 1 mod 9, 55 mod 99, and 73 mod 999.
- A genuine T* return must satisfy (Q999(target)-73*Q999(source))/9 + 11*S = 0 modulo 111, where S is the physical carry cocycle accumulated over the 120 steps. This is necessary, not sufficient.
- For H'=H U^5 and P=H C reverse(H), the target charge shift is 5*10^|H|*(Q999(U)+10^|C| Q999(reverse(U))) modulo 999. Among all 30 U3 rotations, exactly one centre-length residue per rotation preserves this template charge: rotation r=0 needs |C|=1 mod 3; r=1 needs |C|=2 mod 3; r=2 needs |C|=0 mod 3.
- The validation script checks q=20,40,80,160 with k=4q for three rooted phase-0 controls. Every step is checked against Python big-int reverse-add, a fresh-buffer LSD-first digit-array engine, and a port of R30 parametric.py's divmod/value/actual_pair arithmetic semantics. All have 30 actual overflows; the Q9/Q99/Q999 recurrences and Q999 cocycle identity agree at every step. These are regression checks, not return claims.
- Next: classify the physical carry cocycle S(q,k) symbolically for one fixed phase-0 seam family. Do not infer a universal obstruction from sampled nonzero residues.
