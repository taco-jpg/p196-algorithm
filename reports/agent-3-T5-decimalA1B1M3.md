# Agent 3 — T5 two-band decimal A1/B1/M≤3 signature quotient

**PAPER PROOF:** an exact finite output-signature quotient preserves all outgoing signed-edge options in the restricted template language. **COMPUTED:** the quotient is acyclic, confirmed by Kahn and independent DFS. **NOT LEAN-VERIFIED.** Negative result scoped to the widths and move alphabet below; second-agent independent confirmation still required. Coordination #289; signed two-band semantics in draft PR #320; original full-width M≤2 graph/crosscheck in stacked draft PR #354.

## Statement and strict scope

Fix base 10 and ordinary-digit two-band templates

`W(g,h) = A x^g B u^h M v^h D y^g E`, with `x+y=u+v=9`.

Every phase must satisfy `|A|=|E|=|B|=|D|=1`, leading A nonzero, `|M|≤3`, and all fixed digits A,B,M,D,E and band digits x,y,u,v ordinary decimal digits. All 100 choices `(x,u)∈{0,...,9}²` are implicitly included, and g,h are arbitrary nonnegative integers. **The edge language is restricted to eight ordered signed boundary moves**, left then right for each run from outer-left to outer-right, each move amount exactly −1,0,+1. Larger fixed blocks, repeated/multiple moves, larger amounts and alternative move orderings are outside scope. No one-band or decimal Lychrel conclusion is attempted.

## PAPER PROOF: sound signature quotient

The usual five-block reverse-add carry calculations give outputs `O0...O4` and emitted neutral runs `R=(X,U,V,Y)`. Because the reflected source repeated-digit pairs add to 9, **all these outputs depend exclusively on sums of fixed mirrored digit pairs, not on source x/u**. In this restricted width family, define the finite signature

`sig(P)=(s0,s1,t)`, where `s0=A[0]+E[0]`, `s1=B[0]+D[0]`, and `t[i]=M[i]+M[|M|-1-i]` for all i.

For m=1, t has one even entry; for m=2, t=(q,q) with 0≤q≤18; for m=3, t=(q,2r,q), 0≤q≤18, 0≤r≤9. The outer sums range 1≤s0≤18 and 0≤s1≤18. **Every permitted signature has a concrete ordinary-digit representative**: for sum s0 choose A=max(1,s0−9), E=s0−A; for s1 choose B=min(9,s1), D=s1−B; choose outer digits of M with sum q via `min(9,q), q−min(9,q)`, and for odd M its independent middle digit r. By the column carry equations, any two source phases with identical signatures give exactly the same output fixed blocks and emitted runs, irrespective of source repeated digits.

An actual signed-edge phase cycle projects to a directed cycle of these signatures: for each signature, enumerate every one of the 19 balanced outer and 19 balanced inner signed boundary-shift combinations (361 exact 8-move traces), apply moves to the signature's canonical output blocks, and require the resulting fixed target block lengths `[1,1,m',1,1]` with 1≤m'≤3, leading digit nonzero, and the next signature present in the active list. Trace targets are also independently checked by `signed_edge` on the canonical representative. The resulting graph is a **necessary overapproximation** because it forgets neutral-run starting-length feasibility; no accepted phase cycle can disappear under the projection. Empty M cannot occur in a cycle: its central carry transmits unchanged, so the two emitted inner run characters are both 0 or both 9 and cannot sum to 9.

For verification of the expansion count, the number of representations of a sum s by A∈1..9,E∈0..9 is `min(s,19−s)` for s=1..18; B,D∈0..9 with sum q has `min(q+1,19−q)` representations. Each outer mirrored M pair of sum r has `min(r+1,19−r)` representations, and an odd center digit has one fixed realization per chosen r. Summing these exact multiplicities over active signatures gives **24,750 actual fixed states for m=1, 222,750 for m=2, 2,475,000 for m=3; total 2,722,500**. Allowing all 100 source x/u choices yields **272,250,000 implicit complete phase configurations**. The algorithm works on only the 19,620 distinct active output signatures; it does NOT enumerate the 272.25 million phases individually.

A finite graph is acyclic iff indegree peeling removes every node. Kahn and separate iterative DFS are both implemented, and topological DP computes the graph's exact longest directed path. Acyclicity excludes every accepted positive-gain return within this narrowly bounded family, for **arbitrary period and neutral run exponents**.

## COMPUTED reproducibility

Python 3 standard library, requires the foundational `two_band.py`/`signed_rewrite.py` files in parent draft PR #320. Run:

```sh
python3 calculation/agent-3/decimal_signature_b1m3.py 2
python3 calculation/agent-3/decimal_signature_b1m3.py 3
```

Observed for M≤2 (independent quotient check against the original **247,500-state** complete all-trim explicit fixed-state enumeration in #354): **2,520 active signatures, 402 quotient arcs, Kahn acyclic, max path 3**. The **2,520 signatures** and longest-path bound match exactly the independent M≤2 source algorithm. The number of quotient arcs differs from the original 61,470 full fixed-state arcs because many original states share an output signature, as intended.

Observed for M≤3:

```text
random_signature_equivalence 20000 PASS
active_signatures 19620 Mmax 3
signature_edges 3594 kahn_removed 19620 dfs_acyclic True longest_path_edges 3 bigint_crosschecks 21564 rejections {'outwidth': 891840, 'badmove': 6169344, 'inactive_target': 7868, 'midwidth': 10174}
```

Exactly **20,000** seeded random original full phases (including arbitrary x,u) agree byte-for-byte with their canonical signature representatives on both image output fixed blocks and run digits. Every one of the **3,594** retained quotient arcs is checked under 3 distinct (x,u) pairs and 2 (g,h) parameter pairs by independent ordinary decimal-integer reverse-and-add, **21,564 checks, 0 failures**. All **19,620×361=7,082,820** quotient move-trace cases are exhausted with no cap. Runtime ~29.44 seconds, peak RSS ~125,568 KB in local sandbox, one process. Longest quotient directed path has exactly **3 edges**; DFS independently reports zero cycles.

## Conclusion / limitations

**COMPUTED bounded exclusion:** no closed positive-gain base-10 signed two-band certificate whose every phase has A/E and B/D each of length one, central fixed M of length at most three, and whose every edge uses the specific eight ordered signed moves bounded by ±1. No four consecutive edges can stay in this bounded family. This is stronger than the prior M≤2 finite result but does not exclude any wider fixed words, arbitrary signed move traces, or general decimal Lychrel existence. Not a Lean result; `python3 tools/verify.py --changed` NOT RUN. Independent **second-agent** source and arithmetic reproduction is required before promoting this negative to a closed task. All PRs remain DRAFT/DO NOT MERGE pending review.