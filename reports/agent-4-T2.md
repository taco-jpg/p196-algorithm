# Agent 4 / T2: decimal neutral-band exterior overflow automaton and bounded B search

**Status: PAPER PROOF (necessary filter), COMPUTED (finite exhaustive results), NOT LEAN-VERIFIED.**
Coordination: #289. Prior review-only evidence: #290, #293, #298, #300, #311, #314.
No claim of a decimal Lychrel number, nor of universal one-band impossibility.
The contribution is restricted to the autonomous exterior B-component of the established Agent120 one-neutral-band formalism.

## 1. Exact necessary low-coefficient reduction (PAPER PROOF)

Under the Agent120 edge hypothesis, \`e2=1-e1\`; hence the exterior update is independent of C.
Let \`x=B[0]\` for nonempty B, which lies in \`1..18\`; use effective value \`x=9\` if B is empty.
For nonempty B, let \`c∈{0,1}\` be the carry **entering the final position**
of \`norm(reverse B,1-e1)\`, whose input coefficient is \`x\`.
The overflow is \`g=floor((x+c)/10)\`.

If \`g=0\`, the first coefficient of the raw next B equals \`x+(x+c)=2x+c\`
(because then \`x+c<10\`, so \`x<10\`). If \`g=1\`, it equals
\`(x mod 10)+1\` from the appended overflow digit.
Any legal next-B operation trims only a **suffix** of 9s, so this first
coefficient is retained, unless all coefficients are removed, in which
case it must equal 9, our effective coordinate. If B is empty, Hyp forces
\`e1=0,e2=1\`; the raw next B equals \`[10]\`, corresponding to surrogate
\`x=9,c=1,g=1,x'=10\`.

Thus *every* B cycle projects to a closed path on just 18 vertices \`x=1..18\`,
with edges \`g=(x+c)//10\` and
\`x'= (x%10)+1\` if g=1, else \`x'=2x+c\`, for some c=0 or 1.
This is a **one-way** implication: a surviving bit stream need not lift
to any complete B word or center.

The C++ \`low_digit_automaton.cpp\` implements an exact bitset propagation,
not a heuristic. For a fixed p it lists all binary necklaces (lexically
minimum cyclic rotations) and the subset labeling closed paths in this
18-state graph. There is no state/time cap for p<=24.

|p|Total binary necklaces|Pass necessary graph|
|---:|---:|---:|
|11|188|14|
|12|352|22|
|16|4,116|95|
|18|14,602|207|
|20|52,488|449|
|24|699,252|2,268|

The documented full-B streams p11 \`g=11100010000\` and
p12 \`g=100010001000\` pass; they are positive controls, not discoveries.

## 2. Full-width B position automaton (COMPUTED)

The fixed-g probe is an independently specialized implementation of the
repository's existing \`calculation/neutral_band/structure/bauto.cpp\` model,
**not a new independent mathematical method**. It represents boundary states
\`(L,H,Y)\` and exactly propagates possible period-p coefficient columns.
Starting state is \`L=0,H=g,Y=1\` at overflow positions. A closing
interface requires \`L+H=1\` bitwise and \`Y_i=9 L_{t_i}\`.
The packed key is 128-bit with the hard guard \`2*p+4*sum(g)<=127\`.
Each run must return exactly one of: \`ACCEPT\`,
\`EXHAUSTED-NO-B-CYCLE\`, \`CAPPED\`, or \`DEPTH-CAPPED-UNDECIDED\`.
**Caps and timeouts are not negative results.**

The model has unrestricted B width: exhausting its finite states decides the
given overflow word for *all widths*, not just initial bounded B seeds.
The known p11 stream ACCEPTs at depth 29 with e=10100110011; p12 ACCEPTs
at depth 53 with e=100101011010 (cyclic rotation). These are controls.

### The complete period-20 census

Exactly 449 p20 binary necklaces survive the proven 18-state necessary filter.
By number of overflows \`sum(g)\`, their counts are:
\`{5:1,6:23,7:164,8:219,9:41,10:1}\`; all other weights are rejected
by the necessary filter. All 449 survive-or-fail questions were passed to
the exact fixed-g B position solver, and **all 449 EXHAUSTED with zero ACCEPT**.
No caps or timeouts. Largest graph: 815,179 reached states, depth 47,
\`g=11100010011100010000\`. Runtime of the local batch was 8.43 seconds.
This is a **COMPUTED NEGATIVE for exactly p=20, all B widths**.
It is not a kernel proof, and independent second-agent confirmation is pending.

Reproduce from repository root (write compiled binaries only to your local
working tree, not to the PR):

\`\`\`sh
c++ -O2 -std=c++17 -o calculation/agent-4/low_digit_automaton calculation/agent-4/low_digit_automaton.cpp
c++ -O2 -std=c++17 -o calculation/agent-4/fixed_g_B_probe calculation/agent-4/fixed_g_B_probe.cpp
python3 calculation/agent-4/run_p20_all.py
calculation/agent-4/fixed_g_B_probe 11100010000 2000000 100
calculation/agent-4/fixed_g_B_probe 100010001000 2000000 100
\`\`\`

Expected batch summary:
\`\`\`text
p20 admissible_overflow_necklaces= 449
counts_by_overflow_weight= {5: 1, 6: 23, 7: 164, 8: 219, 9: 41, 10: 1}
status= {'EXHAUSTED-NO-B-CYCLE': 449}
max_states_word= (815179, '11100010011100010000', 47)
COMPUTED: ALL p20 B POSITION STATES EXHAUSTED, ZERO ACCEPT
\`\`\`

### Further strictly scoped checks

- **p16**: weight 5 (14/14) exhausted; weight 6 (54/54) and weight 7
  (25/25) independently corroborate Agent 2's earlier computations.
  Agent 2 owns these sub-tasks. At p16, weight 8 has a **capped,
  unresolved alternating stream**; p16 as a whole is not excluded.
- **p18**: weight 5 has three first-coordinate-surviving necklaces,
  all ruled out by direct first-two-position transfer (32 first-column
  boundary traces each, zero accepting/extendable). Weight 6 has 57/57
  exhaustive negative B solver results (maximum 808,563 states).
  Among weight 7–9 surviving words 146/147 exhausted, but
  \`g=101010100101010100\` is **UNDECIDED**: 2,027,121 states
  at depth 24 hit the 2-million-state cap; increasing the cap
  timed out in the bounded run. Manager has queued a Studio rerun,
  *not yet executed*. p18 is not excluded.
- **p21–24 with six overflows**: all 11 p21, four p22 and one p23
  graph-surviving words exhausted. The lone p24 word
  \`g=(100010001000)^2\` is a **known p12 B cycle repeated twice**;
  an explicit 51-coefficient B word was directly replayed at times
  12 and 24. The unrolled p24 BFS alone capped, but this does not
  negate existence of a *nonprimitive B-only return*. No center C
  was found.

## 3. Limits and verification

The autonomous B return is **necessary, not sufficient** for a
\`Agent120.Neutral.cycleOK 10\` certificate. No matched center cycle,
full edge list, or theorem \`cycleOK 10 ... = true := by decide\`
has been constructed. No proof that 196 is Lychrel, no arbitrary-period
negative theorem, and no general impossibility of one-band certificates.

This PR contains only source/reports in agent-owned paths.
**UNVERIFIED / DO NOT MERGE** pending a literal
\`python3 tools/verify.py --changed\` pass and second-agent review of
the numerical negative. No Lean file added; no claim of kernel verification.
