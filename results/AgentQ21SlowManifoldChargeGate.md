# AgentQ21SlowManifoldChargeGate

**PAPER PROOF**, necessary condition only, not a decimal Lychrel certificate.
For rooted decimal p8/m20 B ++ W^q ++ A ++ V^s ++ J ++ rev(V)^s ++ rev(A) ++ rev(W)^q ++ rev(B), with fixed literal caps and true overflow 10101010, suppose **all** q,s above thresholds return after 88r genuine reverse-add steps to identical blocks with q->q+e, s->s+delta, e>=0, delta>=1.
Then 20e+|V|*delta=22r; (7^r-1)*sum(V)=0 (mod 9); and 3|r implies delta*sum(V)=0 (mod 9).
If gcd(sum(V),9)=1, any such return requires r>=6 (at least 528 additions). Three 88-step renewals **cannot** close a unit-charge slow-band return with nonshrinking W; r=6,e=3,|V|=8,delta=9,sum(V)=64 is only arithmetically compatible, not physically realized.
Full proof and exact scope: reports/AgentQ21SlowManifoldChargeGate.md.
Independent tests: calculation/new_structures/Q21/charge_gate.py (true-integer vs pairword arithmetic at q=20,40,80,160).
No physical periodic repair, safe all-phase cycle, Lean verification, 196 claim or all-time decimal instance is proved.

**Stronger one-dimensional slow-manifold PAPER corollary:** if q(s)=a*s+beta with integer a>=0 and the exact macroreturn is s->s+delta, then the unit-charge condition forces 9|r and 9|delta, hence at least 792 (9*88) true additions, even without independently adjustable q,s. Reproduce: `python3 calculation/new_structures/Q21/correlated_gate.py`. No positive cycle is constructed.
