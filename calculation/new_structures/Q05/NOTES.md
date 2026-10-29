# Q05 running notes

- Read current AGENTS.md top: coordination moved to issue #475; issue #474 is full/read-only.
- Read the last 40 FEED/COMBINE entries on #474 and the current #475 tail. Current T* target is rooted p12/m9 B34–W9^q–J–U3^k–C with a 120-step physical return and k→k+5.
- Reposted the migrated route as CLAIM agent-Q05 in #475, comment 6493451412. Route: unify physical carries, drift, first contact, reservoir budget and root reachability; explicitly retain even-centre branches.
- Read docs/FOCUS_SWARM.md, docs/EPOCH_INVARIANTS.md, docs/GAP_MAP.md, docs/LEMMA_GRAPH.md, Q03 first-contact results, ExtremeUniformIsolation10, AgentX04ExactZeroCorridorBudget, and AgentY12NeutralNineIrreversibility.
- New paper lemma: phasewise centre-length parity is a deterministic cocycle of the actual overflow stream. Proof uses exact template length 2*(34+9q+|J|+3k)+|C| and true digit length increment gamma.
- Independent control script verify_parity_cocycle.py passed at q=20,40,80,160 (k=5q), 120 true decimal edges each; Python big integers and a separate schoolbook digit-array engine agree at every step; each run has 30 actual overflows and exact carry-mass identity. No survival/certificate claim is made.
- Unified theorem's inputs are scope-preserving: strict drift (REPORT_208/218), physical carry reset and first contact (Q03), zero corridor budget (X04), neutral-nine irreversibility (Y12), extreme uniform isolation (Lean-verified E2), and the new parity cocycle.
- Exact missing-lemma contribution: the T* finite-interface return graph must carry centre-length parity as a state; every overflow toggles it, so fixed-centre-length-per-phase paths are impossible.
- Remaining gap is still the full rooted all-width 120-edge physical return or a finite exclusion of every moving-centre/active-seam case.
