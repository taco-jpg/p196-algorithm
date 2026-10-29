# AgentQ14MorphicIncrementCriterion

**Label: PAPER PROOF.** Generic all-time substitution-growth theorem and its exact application as a necessary condition on the T* centre-reservoir route. This is not a decimal Lychrel certificate and does not close the physical T* interface.

## Theorem

Let A be a finite alphabet, sigma:A->A+ a nonerasing morphism, and w a finite seed word. Set L_m=|sigma^m(w)| and Delta_m=L_(m+1)-L_m. Let E={a in A: |sigma(a)|>1}. Form the directed occurrence multigraph with one edge a->b for each occurrence of b in sigma(a). Let G* be the induced graph on letters both reachable from the support of w and able to reach some letter in E. Then Delta_m is bounded for all m>=0 if and only if:

1. Every cyclic strongly connected component of G* is a simple directed cycle, with exactly one internal outgoing edge per vertex, counting parallel edges.
2. No directed path in the SCC condensation graph connects two distinct cyclic SCCs.

In the bounded case, Delta_m is eventually periodic from m>=3|A|, with period dividing P, the least common multiple of the cyclic-SCC lengths (P=1 if there are none). Therefore its exact maximum is obtained by checking only m=0,...,3|A|+P-1.

## Proof

Let c_m(a) count occurrences of a in sigma^m(w). If M is the incidence matrix, then c_(m+1)=M c_m and

\[
\Delta_m=\sum_{a\in A} (|\sigma(a)|-1)c_m(a).
\]

Equivalently, Delta_m counts length-m walks from the seed support to marked endpoints in E, with multiplicity and positive terminal weight |\sigma(a)|-1. Trimming to G* discards exactly the walks that cannot contribute.

If a cyclic SCC has an internal branch, strong connectivity supplies two distinct closed walks from some vertex back to itself. Repeating them to a common length gives two distinct equal-length loops; concatenating arbitrary choices yields exponentially many productive walks along a subsequence of lengths. Therefore Delta_m is unbounded. If two cyclic SCCs lie on one directed path in G*, choose fixed paths from the seed to the first cycle, between the cycles, and from the second cycle to a marked endpoint. For r common-length laps, distributing the laps between the two cycles in r+1 ways gives r+1 distinct productive walks of the same length. Again Delta_m is unbounded. This proves necessity.

Conversely, under conditions 1 and 2, every productive walk crosses at most one cyclic SCC, and that SCC is a deterministic simple cycle. Each walk is specified by one of finitely many acyclic prefixes, an entry/exit phase in that cycle, a finite acyclic suffix, and a number of whole cycle laps. For a fixed total length, each such skeleton determines the number of whole laps uniquely. There are finitely many skeletons, so the number and total terminal weight of productive walks of any length are uniformly bounded. Hence Delta_m is bounded.

For periodicity, every acyclic prefix and suffix has length at most |A|-1, and a partial cycle traversal has length less than |A|. Thus each productive walk skeleton has at most 3|A|-3 edges outside its full laps. For m>=3|A|, the existence and multiplicity of each skeleton depend only on m modulo its cycle length. The common period P therefore works for all m>=3|A|. Checking the transient and one full period gives the exact maximum.

## T* length consequence

For the rooted p12/m9 T* template P=H C H^R, H=B34 W9^q J U^k, with |W9|=9, |U|=3, and the exact 120-step overflow clock containing Gamma=30 ones, a phase-0 return with the same top-carry convention has exact coefficient-length ledger

\[
18\Delta q+2\Delta|J|+6\Delta k+\Delta|C|=30.
\]

For the centre-only substitution variant, q and J are fixed, C_m=pi(sigma^m(w)) is nonerasing and palindromic, and k_(m+1)>=k_m. Therefore

\[
6\Delta k_m+\Delta|C_m|=30,\qquad 0\le\Delta|C_m|\le30,
\]

so every centre-length increment belongs to {0,6,12,18,24,30}. The theorem above is consequently an exact finite graph filter for every proposed substitution centre on this route. It excludes productive expanding SCCs and chains of productive cycles, while retaining linear-growth/unipotent reservoirs.

## Reproduction and scope

- python3 calculation/new_structures/Q14/morphism_gate.py: named substitutions and exact increment/period checks.
- python3 calculation/new_structures/Q14/test_morphism_gate.py: 216 small two-letter morphism/seed cases.
- python3 calculation/new_structures/Q14/positive_controls.py: independent arbitrary-precision integer controls for the known base-9 Lean cycle and computed base-50 cycle at parameters 20, 40, 80, 160.

The graph theorem is a paper proof; the code is an executable finite checker for its hypotheses and consequences. Neither the theorem nor its implementation establishes a physical T* edge, a centre/carry closure, or an infinite base-10 Lychrel orbit. Those obligations remain open.
