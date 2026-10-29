# W18: a phase-aware local zipper for decimal reversal in radix-100/1000 blocks
**Label: PAPER PROOF** (exact recurrence and conditional soundness); numerical controls **COMPUTED**. Neither a new infinite decimal orbit nor Lean verification.

## Exact theorem: true decimal reversal, not grouped-digit reversal
Fix k>=1 and B=10^k. Write a positive decimal integer as the canonical least-significant-first base-B block word x[0..m-1]. Let its top block have h significant decimal digits (1<=h<=k); interior blocks have fixed width k. Define rho_j(a) to reverse exactly j decimal digits, including the necessary leading zero padding *before* the reversal. Put a_i=rho_k(x_i) for 0<=i<m-1, a_top=rho_h(x_(m-1)), H=10^h, C=10^(k-h).

For m>=2, the **exact block word of ordinary decimal reversal** R_10(N) is:
- r_0 = a_top + H*(a_(m-2) mod C);
- r_j = floor(a_(m-1-j)/C) + H*(a_(m-2-j) mod C), 1<=j<=m-2;
- r_(m-1) = floor(a_0/C), discarding a zero top block if necessary.
For m=1, r_0=rho_h(x_0). Every r_j is in [0,B-1], since its two nonoverlapping portions have h and k-h decimal digits. **Proof:** ordinary reversal is the h-digit reversed top block followed by the k-digit reversals of the remaining blocks, in opposite order. The formula splits this concatenation at each B-group boundary. Consequently R_10(N)=sum_j r_j B^j identically for every integer N, including a partial high block.

Next set c_0=0 and y_j=(x_j+r_j+c_j) mod B, c_(j+1)=floor((x_j+r_j+c_j)/B); add a last block 1 iff the final carry is 1. This is exactly the ordinary decimal integer N+R_10(N), expressed in groups. It does not matter that the final top-block phase may change. In a folded two-ended representation, each r_j depends on two *adjacent high-side* blocks and the fixed finite phase h; the addition uses one carry c_j. A finite-state graph can store a single high-neighbour block and (if required by folded output alignment) one output-delay block. The graph therefore defines a finite rational relation on folded grouped words, for fixed k.

**Conditional certificate soundness:** Let phase-indexed regular languages of canonical folded B-block words have at least one admitted seed, contain no decimal palindromes (a regular condition at fixed k, using the same alignment h), and be forward-closed under **both** exact overflow branches of the zipper relation. The ordinary decimal reverse-add orbit of any admitted seed stays in their union and is never palindromic, by induction. Product-automaton reachability decides the two language-inclusion conditions. This is a new *concrete grouped-coordinate realization* of the already known N07/N08 general regular-invariant principle, not a claim to have invented the general DFA theorem.

## Constructive base-100 edge with a changing high-block phase
For every Q>=2, define the true decimal integer N0(Q)=5(99)^Q4. In least-significant-first base-100 groups, the following **exact identities hold for every Q>=2** (99^q means q literal groups, not a finite sample):
- t=0: [94] ++ [99]^(Q-1) ++ [59] (full top h=2).
- t=1: [89] ++ [99]^(Q-1) ++ [09,01] (top h=1); the ordinary decimal reversed input was [95] ++ [99]^(Q-1) ++ [49].
- t=2: [90,98] ++ [99]^(Q-1) ++ [10] (full top h=2).
- t=3: [91,97] ++ [99]^(Q-2) ++ [89,20] (full top h=2).
These are exact ordinary decimal reverse-and-add edges: the first has 94+95=189, interior 99+99+1=199, upper 59+49+1=109; the next two follow by the explicitly proved partial-block formula and ordinary group carry. Every phase has different leading and trailing decimal digits, so these four states are nonpalindromic for all Q>=2. The formula has a real h=2 -> h=1 -> h=2 transition. **No phase closure after t3 is asserted.** The independent 100,000-step W18 wall witness is a separate finite-horizon result.

## Large-base controls and the correct redirect
The known base-50/146/1286 neutral-band four-phase certificates have low/central carries alternating (e,e2)=(0,1),(1,0),(0,1),(1,0), overflow stream 0101, paired neutral trimming totals 3, and overflow cost totals 2. Thus the neutral band grows by 3-2=+1 per four edges; this is the algebra of their closure, provided the complete exterior and centre also return. Their neutral coefficient b-1 is respectively 49,145,1285. Merely treating any of these as decimal blocks changes the positional base and does NOT commute with decimal reversal.

The restricted published canonical-root e=01 exterior generator is independently replicated in `root_probe.py`: base50 has 141 reachable states and target depth36, base146 has 318/depth80, base1286 has 4813/depth1204. For base100 the same **restricted** search has 85 reachable states but no target, and for base1000 293 but no target. This does not rule out other schedules or decimal centre formats. It directs the search toward actual h-aware block-synchronizer transitions rather than an invalid direct base lift.

## Reproduction and limitations
`bash calculation/new_structures/agent-W18/reproduce_zipper.sh` runs 66,847 comparisons of the zipper against independent ordinary decimal reversal/addition across k=1,2,3 (exhaustive small integers, seeded random up to 84 digits, 700 true orbit steps each at base100/base1000, and Q2..150 positive edge controls), then the restricted positive/exterior diagnosis. No automaton accepting an infinite decimal orbit has been found, and neither a base-100 nor base-1000 Lychrel certificate is claimed. Standalone controls passed; no Git checkout was available to run the repository-wide changed-file verifier and no Lean files were added.
