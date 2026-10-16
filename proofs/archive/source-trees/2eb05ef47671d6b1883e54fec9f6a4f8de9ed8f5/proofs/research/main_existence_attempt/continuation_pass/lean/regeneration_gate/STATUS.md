# Exact safe regeneration with four additional 9s per band

This bundle formalizes a concrete positive regeneration gate for every
natural gap g, including g=0. Its target has different finite interfaces,
so the theorem does not repeat itself and supplies no infinite invariant
or decimal Lychrel witness.

## Checked family and actual update

All words are least-significant first. Put

| Component | Source | Target |
|---|---|---|
| Outer block | B=(1,9,12,3,14,14) | C=(3,9,4,8) |
| Central block | H=(4,4,15,10,15,4,4) | J=(11,2,11) |
| Each 9-band length | g | g+4 |

The source word is `B,9^g,H,9^g,reverse(B)`. Its exact actual successor
pair word is `C,9^(g+4),J,9^(g+4),reverse(C)`. The ordinary update has
**no overflow**, and both words have width `2g+19`. The four added 9s
on each side compensate exactly for the shorter finite interfaces.

`RegenerationGate.lean` gives explicit finite coefficient functions and
proves the exact column identity

    normalized_i + 10*incoming_(i+1) = source_i + incoming_i

for every natural g and every natural column index i. The coefficient
functions are zero outside the word, so the identity includes its complete
terminal boundary. All normalized digits lie in 0 through 9 and the
initial and terminal incoming carries are zero.

The normalized digit blocks are

| Block | Actual digits |
|---|---|
| B | (1,9,2,4,4,5) |
| Left band | g zeros |
| H | (5,4,5,1,6,5,4) |
| Right band | g nines |
| reverse(B) | (4,5,4,2,0,2) |

`RegenerationGateDynamics.lean` proves that these functions equal the
actual decimal carry and output recurrences. It then proves the full
mirrored digit identity at every in-word column. The theorem `actual_update`
therefore uses the real overflow-dependent update, not a chosen clock or
an independently assigned carry stream.

## Ordinary numeric safety and nonvacuity

The source and target are admissible canonical pair words for every g.
For every canonical ordinary realization of the source, the module proves
the exact next canonical digits and proves that the input and its first
two ordinary reverse-and-add outputs are all nonpalindromic.

The safety witnesses are explicit instances of the intrinsic H9 criterion.
The source has the adjacent pair (12,9) at indices `2g+16,2g+17`. The target
has (11,9) at indices `g+10,g+11`. Thus the target still certifies the
following ordinary update. This holds at g=0, when the source's two
designated bands are empty and the target's bands have length four.

`gate_realized` supplies an actual positive finite decimal seed for every
parameter through the existing constructive canonical realization theorem.
No limit of growing words, unverified finite computation, or assumed
nonempty language is used.

The target interfaces C,J differ from the source interfaces B,H. The bundle
does not prove a return from C,J to B,H, an indefinitely repeated gap
increase, or safety at every later time. It does not prove decimal Lychrel
existence or the assertion for 196.

## Reproduction

The complete entry module is `RegenerationGateDynamics.lean`. From the
project root run:

    python main_existence_attempt/continuation_pass/lean/regeneration_gate/check.py /workspace/scratch/fe6abe1df721/lean-runtime/lean

The checker rebuilds all six source modules in a clean local build
directory and audits every new theorem and definition transitively. Only
`propext`, `Classical.choice`, and `Quot.sound` are permitted. It rejects
proof placeholders, custom axioms, and `native_decide`, and compares
source hashes before and after compilation. Full compiler output and the
per-declaration audit are retained in `compile.log` and `verification.json`.

The fresh build passed all seven compilation stages and audited all
29 new theorems and 5 definitions. Only the three standard axioms listed
above occur transitively. The decimal dependency rebuilt in 55.62 seconds;
the exact-column module rebuilt in 45.70 seconds and the complete dynamics
module in 25.53 seconds. All six source hashes remained unchanged during
the build.

The checked source hashes are:

| Source | SHA-256 |
|---|---|
| RegenerationGate.lean | b7451a6b9ecee59fe7a2a8e6b9545a24aa29629254032ce748400d7aa6c3ee49 |
| RegenerationGateDynamics.lean | 218d7b0bae80885a6693dee9c414316e555c555bbf223e02b8b2d0f1c914453e |

## Development history

All development source snapshots and complete compiler outputs remain in
`development_checks/`. The first direct arithmetic proof exceeded Lean's
default heartbeat budget. Partitioning the column index into the finitely
many fixed-block positions, the two symbolic bands, and the outside region
made the proof manageable; its heartbeat budget was raised for proof
search. The universal parameter g was never replaced by a finite bound.

A simplification-only attempt left conditional arithmetic goals, and the
completed proof adds explicit arithmetic case splitting. The first dynamics
draft also called a tactic after a goal had already closed; that redundant
tactic was removed. These were proof-engineering failures, not discarded
mathematical counterexamples or missing assumptions.
