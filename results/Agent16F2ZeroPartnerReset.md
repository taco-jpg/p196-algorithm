# Agent16F2ZeroPartnerReset

**PAPER PROOF.** In any base `b>=2`, any binary-overflow period, and any cut state of the exact lattice position automaton, suppose consecutive time indices satisfy `g_t=1`, `Y_t=0`, `L_t=0`, `g_(t+1)=0`, `H_(t+1)=L_(t+1)=1`. Any temporal trajectory then has `x_(t+2)=0`.
For any `q>=0` subsequent non-overflow steps (`g_(t+2)..g_(t+q+1)=0`),
`x_(t+2+q)<=2^(q+1)-2`; hence `H_(t+2+q)=1` is impossible whenever `b>=2^(q+1)`.
The base bound is sharp for every `q>=1` at `b=2^(q+1)-1`, with explicit carries and lower bits equal to one.
The all-base, all-`q` theorem requires no root-state, graph, length, or carry-pattern enumeration.
It gives a rigorous pruning lemma for the still-**UNDECIDED** diagonal all-`r` graph, but does not prove its state-template exhaustiveness or exclude every terminal state.
There is no claim about other local configurations, a complete Lychrel certificate, or decimal 196.
Proof and sharpness: `reports/Agent16F2ZeroPartnerReset.md`.
Exact primary and independent controls, separate b9/b13 full reachable positive SCC controls, and commands:
`bash calculation/decimal_frontier/lattice_formats/code/agent16_reset_run.sh /tmp/a16-reset`.
