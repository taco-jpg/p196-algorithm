# Agent 3 — T5: decimal signed two-band no-cycle for M≤4, A≤2, B=D=empty

**PAPER necessary quotient + COMPUTED exhaustive exclusion. NOT LEAN-VERIFIED.** Applies only to the signed two-neutral-band certificate language of draft [#320](https://github.com/taco-jpg/p196-algorithm/pull/320). This change is stacked on [#396](https://github.com/taco-jpg/p196-algorithm/pull/396), itself depending on [#359](https://github.com/taco-jpg/p196-algorithm/pull/359) for exact five-block signed helpers.

## Exact scope and result

For **base 10, ANY period**, no positive-total-gain closed certificate exists in this format if EVERY phase obeys:

- Nonempty central fixed block with 1≤|M|≤4.
- Matched outer fixed blocks 1≤|A|=|E|≤2; widths may change from one phase to the next.
- Side fixed blocks B=D=empty.
- All legitimate decimal fixed-block digits, canonical nonzero leading digit of A, complementary neutral paired run digits (on a closed cycle only 0/9).
- Exactly one signed move at each of eight run boundaries, in {-1,0,+1}, including zeros, with either relative ordering at each shared fixed block.
- Arbitrary run lengths g,h and period, valid individual signed run gains, positive total cycle pumping.

The negative is scoped to this format, NOT a theorem about all decimal Lychrel numbers, central length≥5, A width≥3, nonempty B/D, or multiple/larger boundary moves.

## PAPER PROOF: sound restriction to 244 central states

Project an exact full signed phase to (M,c2), its fixed central digits and incoming carry bit. Compute exactly the fixed-width center add R=M+reverse(M)+c2, requiring outgoing carry c3=1−c2 for inner output runs to remain neutral. If a and d denote net signed shifts at the left and right boundaries of M, all full signed edges satisfy **leading carry f=d−a∈{0,1}**. This follows from equal paired side fixed-block lengths and equal gains of the two inner neutral runs, independently of exterior width [#388](https://github.com/taco-jpg/p196-algorithm/pull/388). Enumerate all central moves each in {-1,0,+1}, both orders, and leave the *next* center carry bit free. The resulting finite graph is a necessary **overapproximation**.

Its full 22,220-state census for 1≤|M|≤4 has exactly **one cyclic strongly connected component containing both odd and even center lengths**, of size **244** [#396](https://github.com/taco-jpg/p196-algorithm/pull/396). On a positive-total-gain true closed signed cycle, the PAPER word-length budget implies

~~~text
2 * Σ(delta_g+delta_h) = Σ f > 0
|M_next|−|M| ≡ f (mod 2).
~~~

Therefore such a cycle must switch M parity and must project entirely inside the **unique 244-state mixed-parity SCC**. Only that SCC needs a full exterior check.

## PAPER PROOF: safe outer-pair quotient

For each of those 244 (M,c2) states, attach every A,E pair with 1≤|A|=|E|≤2 and A-leading digit nonzero. With B=D empty, c2 is exactly the carry of E+reverse(A). In each carry class, **4,545** outer pairs satisfy this constraint: 45 pairs of width1 plus 4,500 pairs of width2. Thus the necessary quotient contains exactly

~~~text
244 × 4,545 = 1,108,980 states.
~~~

For a closed neutral-band phase, the source run digits x,u belong to {0,9}, but they do NOT affect the five-fixed-block reverse-add carry/image: each complementary run transmits its incoming carry and emits a run digit determined by the incoming carry alone. Thus the quotient intentionally **forgets source x,u**. That can add spurious possible cycles but cannot remove a real signed transition.

At each quotient state the code computes the exact five-block image, generates every necessary 8-boundary signed move tuple with signed shifts in {-1,0,+1}, and checks **both local move orders** at each shared block. Enforce B'=D'=empty, target |A'|=|E'| in {1,2}, target leading A' nonzero, and target center (M',c2') in the 244-state SCC. Importantly c2' is computed from the **actual target** E'+reverse(A') carry; it is NOT freely guessed. The resulting directed quotient is an overapproximation of all exact full signed edges within the scope.

Therefore **complete acyclicity of this quotient is sufficient** to exclude all positive-total-gain actual full cycles with ANY period in the stated bounded class.

## COMPUTED: complete census, no caps

Reproduce from the repo root, with the stacked review parent dependencies #359 and #396 present:

~~~sh
python3 calculation/agent-3/center4_scc_exterior.py
~~~

Measured local output:

~~~text
PREFLIGHT centers 244 ae_pairs_per_carry 4545 quotient_states 1108980
center_traces 2870
PASS1 1108980 arcs 1034280 active 282216
FINAL quotient_vertices 1108980 active_sources 282216
arcs 1034280 peeled 1108980 residual 0 elapsed 61.73
BOUNDED NEGATIVE: no positive-gain cycle in M<=4 A<=2 B=D=empty signed model
~~~

Wall clock **62.43 seconds**, maximum resident memory **133,992 KB** (about 134MB), **exit 0**. No state cap or timeout. All **1,108,980 vertices** are removed by Kahn indegree peeling despite **1,034,280 exact overapproximation arcs** from **282,216 active vertices**; residual **ZERO**.

The script uses indexed 4,545-pair carry partitions, dense 32-bit indegree, compact FIFO, and two identical enumerations of outgoing edges (first for indegrees, then on popping vertices) to avoid a large Python adjacency object. It explicitly fails on guard mismatches, arithmetic overflow, or incomplete peeling, and returns a negative conclusion only on the exact expected zero-residual completion. Parent #359 supplies 18,000 ordinary big-integer reverse-add controls and known base2 positive witness testing. Parent #396 separately verifies its center-only 9-edge relaxation.

## Limits and verification

This is **COMPUTED bounded impossibility** plus a PAPER sufficient-for-negative overapproximation argument, not an accepted base-10 certificate, general base-10 Lychrel impossibility, or Lean kernel theorem. No Lean modules/registry entries. Full repository verification by python3 tools/verify.py --changed was **NOT RUN** in this sandbox lacking the complete repository checkout. Keep PR **DRAFT** pending independent source review, dependency integration and literal verification-gate PASS.