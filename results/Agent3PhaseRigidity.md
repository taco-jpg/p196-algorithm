# Agent3PhaseRigidity

**PAPER PROOF (finite-state certificate).** For each of the four g=1 then g=0 phase pairs of decimal rec2 p=8,m=48, if the physical two-step output is the corresponding exact rec2 48-periodic target, then **every spatially cyclic source of period 48k, for every k>=1, has the unique intermediate physical carry/coefficient row prescribed by rec2**. The source itself need not be unique.
The phase-expanded two-row product graph has (14592,14360,282) or (15276,16190,310) vertices/edges/unique cyclic-SCC vertices, respectively; every one of its 48 spatial phases has a singleton intermediate-state projection on that SCC.
The same graph proof forbids a finite intermediate defect that disappears at the second step while both spatial tails remain in the rec2 recurrent component: a path leaving the SCC cannot reenter it.
**Scope:** exact cyclic physical bulk or recurrent-tail two-phase maps, all spatial periods 48k and finite defect lengths. Not a rooted centre no-go, a positive-growth repair, an all-time orbit, or a decimal Lychrel certificate. No Lean or full repository verification claimed.
Reproduce: sh calculation/decimal_frontier/lattice_kinks/agent3_phase_rigidity/run_checks.sh.
Standalone C++ graph/SCC certificate, independent Python ordinary-digit checker, 8-phase rooted controls: calculation/decimal_frontier/lattice_kinks/agent3_phase_rigidity/.
Proof and limitations: reports/Agent3PhaseRigidity.md.
