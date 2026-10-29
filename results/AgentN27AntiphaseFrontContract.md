# AgentN27AntiphaseFrontContract
**PAPER PROOF (local arbitrary-base front transfer)** and **COMPUTED (five explicit decimal trajectories)**.
For base b>=2, symmetric central pair-coefficient block C=L ++ [2(b-1)]^q ++ reverse(L), q>=3, with L ending in a non-maximal coefficient, let c be the carry after normalizing L from the current exterior carry, and gamma the 0/1 leading overflow. The next central saturated-run length is EXACTLY
q_next = q - gamma - 2*(1-gamma)*(1-c).
This is a precise one-step sound centre-front format, derived by digit-pair cases, not extrapolated numerically. Independent exhaustive arithmetic checks cover 255,816 instances across bases 2..20.
In five actual decimal orbits with inner initial 9-run m=40,80,200,500,3000 and B=[12,9], the carry/overflow locking condition c+gamma=1 holds at EVERY transition with q>=3: 89,182,473,1181,7251 transitions respectively. Thus q_next=q-gamma and the absorbing front behaves as an overflow clock, as observed in the prior N27 result. Full ordinary decimal digit-list replay verifies the pairword every time.
For m=3000 the 7251 antiphase transitions comprise c=0,gamma=1:2997 and c=1,gamma=0:4254; neither alternative appears.
This does NOT prove an all-m temporal lock or infinite Lychrel number. A future certificate must regenerate a different band species or hand off between fronts, rather than relying on one monotonically eroding saturated plateau.
Reproduce: sh calculation/new_structures/agent-N27/run_guard.sh.
Code: calculation/new_structures/agent-N27/{guard_replay.cpp,guard_generic.py,guard_expected.json,run_guard.sh}. Detailed proof: reports/AgentN27AntiphaseFrontContract.md.
