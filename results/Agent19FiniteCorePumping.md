# Agent19FiniteCorePumping

**PAPER PROOF.** A base-generic finite commuting-strip criterion is sufficient for a periodic mirrored band with an arbitrary finite palindromic core to propagate by ordinary reverse-and-add at every band repetition count `k>=0`, with a finite-cycle palindrome-avoidance corollary under explicit phase, signed-length, and nondecreasing-cycle checks.
The result extends the centreless/neutral-only template settings; it provides a finite-source checking mechanism, **not** a Lean-verified theorem or a base-10 certificate.
Positive controls: original b26 four-edge neutral-band orbit and the known b9 spatial-period-4, exterior-width-61 lattice rewritten as 20 cyclic finite-core edges (including a variant with maximal core length 1).
Independent replay checks 2,000 b9 steps for each variant and 600 b26 steps; the existing b13 period-10 controls with exterior widths 75 and 55 are checked for 300 steps each, with overflow word 1010010000.
Statement and proof: `reports/Agent19FiniteCorePumping.md`.
Executable finite checker, independent big-integer replay and exact reproduction command: `python3 calculation/decimal_frontier/finite_core_pumping/finite_core_check.py .` from repository root.
Scope excludes all-width nonexistence, any decimal certificate, any conclusion about 196, and kernel verification; Boolean commutation is sufficient but not necessary.