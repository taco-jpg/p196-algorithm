# Agent 106 — T2.p24-exterior-regular-language

**PAPER PROOF + COMPUTED. UNDECIDED at unrestricted width. No new Lean theorem.**
Coordination: issue #289, claim #6433401663, progress #6433518657.
This is a standalone three-file checkpoint based on main
`eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.

## Result and attribution

An exact regular-language engine represents every positive repetition of
a fixed exterior driver at each spatial width. For the priority P24
driver, complete minimized frontiers through width 7 have empty terminal
intersection for **every** positive lap count. Construction of width 8
reaches a resource cap. Neither exhaustion nor a language recurrence was
found, so the unrestricted-width question remains **UNDECIDED**.

This checkpoint's contribution is the exact all-lap language engine,
reconstruction, export interface, and independent audit. It does not
improve Agent109's stronger all-lap canonical-width-16 bound in
[PR #427](https://github.com/taco-jpg/p196-algorithm/pull/427).
Agent101 supplies the actual center itinerary in
[PR #381](https://github.com/taco-jpg/p196-algorithm/pull/381).
The cut arithmetic comes from the established exterior automaton;
Agent7's neutral padding and Agent114's
[PR #400](https://github.com/taco-jpg/p196-algorithm/pull/400)
justify a common exterior width with trims `u=g`.
Agent116 independently explores block-coded forward languages, Agent113
backward languages, and Agent111 independent invariant verification.
Their searches are not repeated here.

The files are `calculation/agent-106/p24_exterior_regular.py`,
`calculation/agent-106/p24_exterior_regular_audit.py`, and this report.
No frontier dumps, process logs, or new Lean files are committed.

## Fixed driver and cut language

The default decimal driver and credited center witness are

```text
E  = 010100110100101011001011
G  = 110001001000110001001000
V  = 100001000000100001000000
C0 = (9,14,13,18,13,14,9)
```

The center has 24 steps, total overflow 8, total pair trim 4, and widths
6 and 7. Repeating this center is allowed, but the exterior need not
return after one lap. The engine never imposes that restriction.

For base `b`, a cut letter is `(t,L,H,Y)`, with phase `t`, two carry bits,
and `0<=Y<b` on overflow phases; `Y=0` otherwise. Its integer encoding is

```text
t*(4*b) + L*(2*b) + H*b + Y.
```

The physical outer boundary is the nonempty repetition language `r+`,
where `r[t]=(t,0,G[t],1 if G[t] else 0)`. The exact inner boundary is
`q+`, where `q[t]=(t,E[t],1-E[t],(b-1)*E[t] if G[t] else 0)`.
The default alphabet has 384 well-typed letters.

One column chooses coefficients `x[t]` in `0..2b-2` and inward carry
bits `h[t]`. The following integer equations define its complete tile
relation, with temporal indices cyclic over the **whole** word:

```text
H[t]       = (x[t]+h[t]) // b
Lnext[t]   = (x[t]+L[t]) // b
r[t]       = (x[t]+h[t]) % b
x[t+1]     = (x[t]+L[t]) % b + (Y[t] if G[t] else r[t])
output[t]  = (t,Lnext[t],h[t],r[t] if G[t] else 0).
```

Only the first column requires every `x[t]>0`. Subsequent columns allow
zero. There are 7,296 default local tile rows. Natural exterior trims
are covered by the cited common-padding theorem, not by assuming that
the original representatives already have equal widths.

## PAPER PROOF: exact language construction

Let `L0=r+`. Form `L1` with the positive first-column relation, then
`L(n+1)=T(Ln)` with the unrestricted column relation. An image NFA has
states `(input_DFA_state, initial_coefficient, current_coefficient)`.
Its initial coefficients are unrestricted within the relevant range.
A state is final exactly when the input state is final and the current
coefficient equals the initial coefficient.

Each NFA path records exactly the local tile equations, and whole-word
closure is precisely the temporal coefficient seam. Conversely every
valid column supplies such a path. Intermediate final states retain
their outgoing edges even if the coefficient has not yet returned.
Consequently the image is exact for all positive lap counts, with no
reset or closure requirement at an individual 24-phase boundary.

Induction on spatial width shows that `Ln` contains exactly the cuts
obtainable after `n` columns of a closed temporal coefficient strip.
Intersecting with `q+` imposes the actual finite exterior boundary.
A positive intersection is initially a B-only lead; reconstruction and
ordinary normalization replay must establish the literal exterior cycle.
An empty intersection excludes that width at every positive lap count.

The sparse NFA is trimmed, determinized by full subsets, and minimized.
The implementation checks the determinization subsets and every quotient
transition, including absent labels. Equivalence uses the full reachable
product for symmetric difference, not node counts or hashes.

For the default first column, `G=(110001001000)^2` forces the 12-phase
head trajectory

```text
(9,10,1,2,5,11,2,5,10,1,2,4).
```

Its inward high carries are `(1,a,0,1,1,b,1,0,c,0,0,1)` with independent
bits `a,b,c`; inward low carries are `(0,1,0,0,0,1,0,0,1,0,0,0)`.
Overflow reflected digits at phases `0,1,5,8` are `(0,a,1+b,c)`.
Thus one 12-phase block has 8 possibilities, one P24 lap 64, and two
laps 4,096. Choices are fresh on each block. `L1` is the positive closure
of the union of 64 words, not the union of their separate powers.
Its minimal DFA has 25 states and 31 arcs; the generic image is checked
against this independently constructed complete language.

## Exact coaccessibility and stopping rules

Before materializing the coefficient-seam NFA, a shared product with
states `(input_state,current_coefficient)` computes a bit mask of final
coefficients reachable from each state. A seam NFA state `(q,a,x)` can
reach a final state exactly when bit `a` occurs in that product mask.
The mask is seeded at every input final and propagated backward to a
fixed point. This is an exact trim, not a bound on temporal period.
First-column positivity is used consistently in seeds and outgoing
tiles. Any unfinished mask computation raises a resource limit.

Terminal intersection repeatedly follows one full `q` block in the
deterministic automaton. It accepts at the first positive final, rejects
at a dead transition, or rejects after a previously visited boundary
state repeats. This decides `Ln intersect q+` for all lap counts.

An all-width negative would require either an empty complete language,
or exact equality of two completed `Li,Lj` with `1<=i<j` after all prior
terminal queries were empty. The same unrestricted image then repeats
forever. The code checks full canonical DFA structures and verifies any
declared recurrence by the full equivalence product. No termination or
eventual recurrence theorem is assumed.

State, product-slot, edge, operation, wall-clock, memory, and layer caps
always return `UNDECIDED`. A completed image with an unfinished terminal
query is marked `PENDING`; it is not reported as terminal-empty.
The alternative cyclic-graph/power-lifting method claimed in comment
#6433654839 is separate work, not a reinterpretation of these DFAs.

## COMPUTED frontiers and bounded runs

Every row below is complete, minimized, and terminal-empty for all laps:

| Exterior width | DFA states | Labeled arcs |
|---:|---:|---:|
| 1 | 25 | 31 |
| 2 | 25 | 34 |
| 3 | 137 | 192 |
| 4 | 1,860 | 2,836 |
| 5 | 5,157 | 7,710 |
| 6 | 59,559 | 99,363 |
| 7 | 195,342 | 322,743 |

Commands from the repository root, with current source:

```bash
python3 calculation/agent-106/p24_exterior_regular.py --no-pretrim
python3 calculation/agent-106/p24_exterior_regular.py --seconds 120 --memory-mib 4096 --operation-cap 200000000
python3 calculation/agent-106/p24_exterior_regular.py --seconds 180 --memory-mib 4096 --operation-cap 300000000 --product-cap 4000000
```

The first actual pilot predated the mask optimization; `--no-pretrim`
reproduces that method. It completed width 6, then reached 500,001 NFA
states during width 7: 16.000690 seconds, 15,063,599 counted operations.
RSS was not measured in that initial version.

The second completed width 7, then required 3,711,498 shared product
slots at width 8, above its 2,000,000 cap: 57.217360 seconds,
66,872,188 operations, peak RSS 503,076 KiB. Peak materialized NFA:
301,065 states/507,217 arcs; peak DFA: 223,283 states/376,126 arcs.

The third completed the 3,711,498-slot mask with 1,061,807 nonzero masks,
then reached 500,001 materialized NFA states during width 8:
78.489051 seconds, 72,985,615 operations, peak RSS 502,368 KiB.
It used `run(budget=Budget(seconds=180, operation_cap=300000000,
product_cap=4000000), on_layer=checkpoint)` under a 4 GiB address-space
limit; the third command has the same search parameters without the
development-only checkpoint write. Its wrapper caught the limit and
printed `UNDECIDED`; the public CLI exits 2 on a resource cap.
All three results are `UNDECIDED`, not all-width negatives.

## Independent verification and positive reconstruction

Run the committed independent audit and actual reconstruction controls:

```bash
python3 calculation/agent-106/p24_exterior_regular_audit.py
python3 -O calculation/agent-106/p24_exterior_regular_audit.py
python3 calculation/agent-106/p24_exterior_regular.py --selftest-positive
python3 -O calculation/agent-106/p24_exterior_regular.py --selftest-positive
python3 tools/verify.py --changed
```

Both audit modes pass with identical counts: 9,032 typed arithmetic
cases; 2,696 ordinary integer edges/11,335 tiles; the complete 8/64/4,096
head histories; 27 NFA controls/376 full product states; six independent
dense image comparisons; 609 independently checked mask-product states;
nine terminal controls; and four negative guards. The guards include
equal-size unequal languages, missing-label quotient failure, and a
capped run that must remain `UNDECIDED`. Checks survive Python `-O`.

A base-2 one-phase tile control accepts the two-letter output `(0,5)`
with a coefficient cycle `0 -> 1 -> 0`, while neither singleton closes.
It detects the unsound shortcut of resetting the coefficient each lap.
The independent audit also replays all 24 center edges with local dummy
exteriors realizing the prescribed bits; those probes are not a B cycle.

Reconstruction backtracks whole-word preimages through every spatial
frontier, recovers all coefficients, and replays ordinary normalization
and raw exterior edges with `u=g`. Known base-2 and base-4 controls recover
width-2 exteriors and respectively 4 and 6 full mirror-accepted edges.
For the default driver, full decimal edges are returned only after the
credited center repetition is joined and unchanged `cycleOK` accepts.
No target lead was found. A reconstruction exception preserves the
completed `TERMINAL_LEAD`, its width/laps, and the terminal word; it never
turns a positive finding into a negative result.

Additional development checks compared optimized/unoptimized complete
languages from the physical-root image through width 6, all equal;
240 randomized forward-reachability models independently checked masks.
Five injected reconstruction failures also retained the positive lead.
These checks support implementation correctness, not all-width closure.

The literal repository gate passes: 5,217 Lean files/301 projects satisfy
the rules; zero changed Lean modules and zero endpoints are built/audited;
`ALL CHECKS PASSED (changed files only, against origin/main)`.
This is not a claim of a new kernel-verified mathematical result.

## Export and remaining question

`export_payload(dfa,driver,width)` returns schema
`p196-exterior-dfa-v1` with `base,g,e,width,kind,start,finals,transitions`.
Each transition row is a sorted list of `[integer_symbol,target]` pairs;
an absent transition rejects. `kind=frontier` is explicit: an individual
frontier is not an inductive invariant. `run(...,on_layer=callback)` can
export each completely checked layer; the callback is skipped on a lead.

The open question is whether a finite-width exterior exists at any
positive repetition of the exact P24 driver. This checkpoint supplies
neither such an exterior nor a proof of its nonexistence. It makes no
claim about other drivers, global decimal Lychrel existence, or failure
of the full neutral-band route.
