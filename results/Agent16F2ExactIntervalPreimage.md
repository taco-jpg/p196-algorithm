# Agent16F2ExactIntervalPreimage

**PAPER PROOF.** For every integer base `b>=2`, every finite binary-overflow time word `g`, and every exact automaton cut `(L,H,Y)`, an exact, cap-free backward **integer-interval preimage** algorithm decides whether any (not necessarily periodic) coefficient trajectory traverses the whole temporal word. The preimage is obtained by partitioning `x` into `[0,b−2]`, `{b−1}`, `[b,2b−2]`, then splitting on carry bit `c` and inverting the resulting affine map. Empty initial domain is a sound proof that the cut has **no outgoing time-closed edge**; a nonempty domain alone does not prove an edge or SCC.
**COMPUTED control.** The algorithm exactly rejects all 32 explicitly generated depth-five successor states in each tested diagonal case `r=4..200`, `r=500`, and `r=1000`, with at most 3 intervals per suffix; **NO all-r state-exhaustiveness or infinite no-cycle theorem** is claimed.
Independent full integer-domain checks: 7000 random cuts, all suffixes; independent full-source boundary enumeration r=4..6; mandatory base9/base13 full-SCC controls reproduce.
Source, independent checker, C++ positive-control engine, output assertions, and exact commands:
`bash calculation/decimal_frontier/lattice_formats/code/agent16_interval_run.sh /tmp/a16-interval`.
Proof and precise limitations: `reports/Agent16F2ExactIntervalPreimage.md`.
No Lean changes or decimal Lychrel certificate is claimed.
