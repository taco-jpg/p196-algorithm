# Sharp phase-aligned starting gap for a finite-core signed cycle

**PAPER PROOF.** Fix a nonempty, accepted, closed cycle of the finite mirrored-core Boolean edge checker already committed under calculation/decimal_frontier/finite_core_pumping. Every edge has the same nonzero spatial period m, with signed length shift delta_i = up_i - down_i. The checker requires that each SOURCE band gap be at least 2m and have the prescribed phase modulo m. This result optimizes the required starting gap for an ALREADY ACCEPTED certificate; it is not a new base-10 certificate.

Let p>=1 be the edge count, s_0=0, s_j=sum(delta_i for i<j), Delta=s_p, and s_min=min(s_0,...,s_(p-1)). The cycle closure ensures Delta is divisible by m; nonshrinking cycle acceptance also requires Delta>=0. Define

    T = 2*m - s_min,
    L_opt = rho + m*max(0, ceil((T-rho)/m)),

where 0<=rho<m is the first state's required phase. T>=2m, so the expression is nonnegative.

**Sharp theorem.** Every starting gap L>=L_opt with L mod m=rho satisfies ALL source gap and phase guards on every lap. Any smaller nonnegative phase-compatible gap fails at least one SOURCE guard in the first lap. Thus L_opt is the exact minimum for the checker's hypothesis, not a theorem of nonexistence for shorter gaps. This can improve strictly on the conservative earlier bound 2m+sum(max(0,-delta_i)).

**Proof.** Just before source edge j on lap zero, the gap is L+s_j. Its guard is L+s_j>=2m; all such guards are satisfied exactly when L+s_min>=2m, or L>=T. Because the finite checker checks rho_(j+1)=(rho_j+delta_j) mod m and equal source/target m, every source phase is correct if the initial one is. Euclidean division makes L_opt the smallest nonnegative integer >=T with congruence rho modulo m. Every smaller compatible integer violates the guard at an index achieving s_min. On lap n, length before edge j is L+n*Delta+s_j, which is no smaller than on lap zero since Delta>=0. The cycle returns to its identical finite state and phase each lap. Therefore the previously established accepted-edge soundness theorem applies indefinitely. No numerical sampling enters this general proof.

**Executable independent controls.** One new, self-contained Python-3-stdlib driver lives at calculation/decimal_frontier/finite_core_budget/sharp_budget.py and imports the existing checker rather than duplicating it. Exhaustively enumerates spatial periods m=1..6, edge counts p=1..5, all signed shifts in {-3,-2,-1,0,1,2,3}^p with Delta>=0 and Delta mod m=0, and all initial phases rho=0..m-1. Exactly 76,955 phase/shift cases match independent forward simulation at L_opt, the previous phase-compatible value, and the adjacent raw thresholds.

An algebraic gauge transformation of the KNOWN base-26 neutral-band four-edge control, with gauge vector (4,2,4,1), yields shifts [+2,-2,+3,-2] of total gain +1. All four finite Boolean checker edges are accepted. The sharp gap is L_opt=2, while the total-downshift conservative bound is 6. A separately implemented ordinary base-26 big-integer reverse-and-add replay verifies exact templates, canonical digits, and no palindromes for 2,000 steps, ending with gap 502. This gauge also lengthens the finite core, so it does not produce a numerically smaller Lychrel seed or a new existence theorem.

**Reproduce from the repository root:**

    python3 calculation/decimal_frontier/finite_core_budget/sharp_budget.py .
    # PHASE_MIN_BUDGET_EXHAUSTIVE_PASS 76955 exact cases
    # SIGNED_BASE26_POSITIVE_CONTROL_PASS 2000 steps, optimal gap=2, conservative gap=6, final gap=502

**Limits.** The sharp condition is for the specified Boolean edge source guards, not necessity for an actual reverse-and-add identity. This paper proof is not Lean-verified and implies nothing about decimal 196, all-width negative results, or the existence of a decimal certificate.
