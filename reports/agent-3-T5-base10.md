# Agent 3 — T5: bounded decimal signed two-neutral-band obstruction

**Status:** PAPER PROOF for necessary relations and COMPUTED for the finite graph. **NOT LEAN-VERIFIED.** Scoped negative of the signed format from [draft #320](https://github.com/taco-jpg/p196-algorithm/pull/320), not general decimal Lychrel nonexistence. This review-only draft has **not passed** \`python3 tools/verify.py --changed\` because a complete repo checkout is unavailable in this sandbox.

## Exact model and exhaustiveness

Use most-significant-first digit blocks and complement-paired runs:

\`W(g,h) = A x^g B u^h M v^h D y^g E\`

where \`x+y=u+v=b-1\`, \`|A|=|E|>=1\`, \`|B|=|D|\`, \`A[0]!=0\`, and all digits are legitimate base-\`b\` digits. A signed edge uses **exactly one boundary move at each of the eight boundaries**, size in \`{-1,0,+1}\` (zero allowed), with **any ordering**. Positive moves extract a matching digit from the fixed block into its run; negative moves absorb a run digit back into the block. Every finite set of such moves is valid for sufficiently large initial \`g,h\`. This report excludes multiple moves on a boundary, absolute shifts above 1, larger fixed-block bounds, and other certificate languages.

The exact exhaustive state family is:

- base 10, **all ten** allowed fixed-block digits, not a reduced alphabet;
- \`|A|=|E|=1\`, A=1..9, E=0..9;
- \`|B|=|D|<=1\`, both empty or each a single arbitrary digit;
- \`|M|<=2\`, with all 0-, 1-, or 2-digit blocks;
- both independent neutral run pairs in \`0/9\`, that is \`(x,u) in {0,9}^2\`.

Precisely \`90 * (1+100) * (1+10+100) * 4 = 4,035,960\` phase states. Only cycles **entirely inside** these fixed-block bounds are excluded. The graph permits successor search within the same bounded family; an orbit that exits and returns is outside this theorem.

## PAPER PROOF 1: run alphabet is exhaustive for closed cycles

Neutral reflected digits add to \`b−1\`. Incoming carry \`c in {0,1}\` transmits unchanged through any such run, emitting the repeated output digit \`(b−1)(1−c)\`. Each of the four output run digits is therefore 0 or \`b−1\`. Every phase of an exact closed cycle is a previous output, so \`x,y,u,v in {0,b−1}\`. The restriction to decimal 0/9 runs omits **no closed cycle of this particular signed five-block template**.

## PAPER PROOF 2: complete bounded trace reduction

Let \`f in {0,1}\` be the five-block reverse-add leading carry and \`L_i,R_i\` signed move sizes at the left/right boundaries of run \`i=0,1,2,3\`. After block addition, the five fixed-block lengths are \`(a+f,d,m,d,a)\`. The successor must satisfy \`|A'|=|E'|\`, \`|B'|=|D'|\`, and equal final length shifts of the two outer and inner mirrored runs. Comparing lengths yields the four necessary equalities:

\`\`\`text
L0 = R3 + f
L3 = R0 + f
L1 = R2 + f
R1 = L2 - f
\`\`\`

Proof: outer-block equality gives \`L0−R3=f\`; paired outer-run shifts give \`L3=R0+f\`; paired inner side-block lengths give \`L1=R2+f\`; paired inner-run shifts give \`R1=L2−f\`. Each signed boundary move belongs to \`{-1,0,+1}\`, leaving exactly **81** admissible move vectors when \`f=0\`, **16** when \`f=1\`. No admissible bounded edge is filtered by these identities.

The three inner fixed blocks each receive two moves. The checker tests both relative move orders at each of those three blocks, and takes the product of possible results. Moves touching different fixed blocks commute, so all orderings of the eight bounded moves are included. This independently strengthens the fixed chronological-order checker (which had fewer edges). Large initial \`g,h\` remove temporary negative-run concerns.

## PAPER PROOF 3: necessary closed-cycle overflow budget

Let \`F=2|A|+2|B|+|M|\` denote the total length of the fixed blocks. On a signed edge, the raw reverse-add output has fixed-block length \`F+f\`. Extracting \`delta_g\` in *both* outer mirrored runs and \`delta_h\` in *both* inner runs changes total fixed length by \`-2(delta_g+delta_h)\`, even if the shifts are negative. Hence \`F'=F+f−2(delta_g+delta_h)\`. Summing over any closed itinerary gives

\`\`\`text
2 * sum(delta_g + delta_h) = sum(f).
\`\`\`

In particular, positive total pumping requires at least two leading carries; the sum of leading carries is even. The formula is arbitrary-base and independent of the bounded state search; it does **not** exclude all long decimal cycles.

## COMPUTED: exact graph census and controls

Run from the repo root with standard Python 3; no external solver or dependency:

\`\`\`sh
python3 calculation/agent-3/base10_restricted.py --test --base 10 --alphabet 0123456789 --runs 09 --max-a 1 --max-d 1 --max-m 2
\`\`\`

The file independently computes the five fixed-block additions, generates all bounded trace vectors and all local orders, looks up every matching bounded successor, and runs **full Kahn indegree peeling**. Completed local run:

\`\`\`text
bigint_formula_controls 18000 PASS
base2_4phase_4000step_positive_control PASS
base 10 alphabet 0123456789 runs 09 maxa 1 maxd 1 maxm 2
states 4035960 active 1008000 leading_overflow_sources 604800
edges 725940 peeled 4035960 residual 0
\`\`\`

Local benchmark of mathematically equivalent all-orders script: 152.185 s internal elapsed, **2:33.09** wall, **1,474,584 KB max RSS**, exit 0. No state cap, timeout, or overflow condition. Control with \`|M|<=1\`: **399,960** states, **72,000** edges, residual **0**. Control limited to fixed digits 0,1,8,9 and \`|M|<=2\`: **17,136** states, **628** edges, residual **0**. All-orders edge count is larger than the canonical-ordered graph's count (725,940 vs 711,540 at max \`|M|=2\`), but still fully peels.

The 18,000 big-integer reverse-add controls cover bases 2, 3, 10, 11, 17, 26 and compare the independent ordinary integer operation against the block-carry output. The 4,000-step positive control replays the previously established base-two four-phase witness from draft #320 with an independent integer reversal. Its existence was already known from other Lean certificates; here it tests that the checker is not vacuous.

**Conclusion (COMPUTED, bounded):** The displayed 4,035,960-state graph has no directed cycles of any length, so no signed two-band closed certificate has every phase inside these block bounds and at most one ±1/0 move at each boundary.

**What is NOT claimed:** no decimal Lychrel number exists; any unbounded two-band format fails; arbitrary repeated signed moves are covered; all decimal cycles are excluded; a new Lean theorem or a successful verification gate exists. A complete independent implementation review is welcome before integration.