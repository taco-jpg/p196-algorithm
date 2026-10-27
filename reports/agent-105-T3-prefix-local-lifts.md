# Agent 105 — T3: exact local prefix lifts 和 residue-compatible middles

## Result 和 scope

**PAPER PROOF:** an extended-prefix condition characterizes genuine one-step
canonical center edges with prescribed source/target prefixes, carries, overflow,
和 trim count at every sufficiently large prescribed width. Every satisfying
extension has an explicit symmetric finite-center completion.

**PAPER PROOF, decimal:** with four additional middle positions, the completion
can attain any source value modulo 99 compatible with symmetry, while preserving
the required carry 和 an even physical midpoint coefficient at odd width.

**COMPUTED:** the 35 edges of the existing r4 p11/k1 和 p12/k2 prefix loops
都 admit genuine one-step lifts. Cyclic widths, the prior modulo-9 recurrence,
和 the prior modulo-11 center condition can also hold simultaneously.
The selected full centers do 不 join into a cycle: the strengthened constructions
have 9/11 和 21/24 incompatible consecutive full-center pairs, respectively.

Repeating the projected loops covers every positive p11 repetition 和 every
positive even p12 repetition **in this exact four-prefix local relation with
widths 和 residues**. This does 不 establish a full C-cycle, a decimal certificate,
an all-k negative, or a limitation of every finite-prefix method. Conditions
coupling the hidden interiors across consecutive edges remain essential.
没有 new Lean theorem or LEAN-VERIFIED mathematical claim.

## Dependencies 和 attribution

This result follows [claim 6432984389](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432984389).
It is stacked on [Agent 105 PR #343](https://github.com/taco-jpg/p196-algorithm/pull/343),
whose `calculation/agent-105/prefix_budget.py` supplies the original prefix loops
和 is imported by the new scripts; the parent API head has prefix `d10a7f`.
PR #343 must be present before these scripts are run.

Arithmetic uses [the exact mirror](../calculation/neutral_band_search.py) 和
[A120Template.lean](../lean/P196/Drafts/Agent120NeutralBandCalibration/A120Template.lean).
[Agent 7's normalization](https://github.com/taco-jpg/p196-algorithm/pull/315)
和 [canonical quotient](https://github.com/taco-jpg/p196-algorithm/pull/326)
retain attribution for maximal neutral stripping.
[Agent 117's head analysis, PR #347](https://github.com/taco-jpg/p196-algorithm/pull/347)
和 [Agent 114's center-core congruences, PR #350](https://github.com/taco-jpg/p196-algorithm/pull/350)
are prior results. The contribution here is simultaneous constructive realization
with the same four-coefficient prefixes 和 checked source extensions.

## Exact extended-prefix condition

Fix base `b>=2`, neutral coefficient `h=b-1`, depth `r>=1`, source prefix A,
target prefix T, carry e, overflow g, 和 trim v. Prefixes have length r,
coefficients in `0..2h`, 和 nonneutral heads. Put `s=r+v`.

Seek an extension X of A of length s 和 a carry k in `{0,1}`. Normalize X
from e to obtain low digits L. Normalize reverse(X) from k, require exit
`1-e`, 和 reverse its emitted digits to obtain R. The raw prefix is

`P[i]=L[i]+R[i]` when `g=0`;

`P[0]=L[0]+h*e`, `P[i]=L[i]+R[i-1]` for `i>0` when `g=1`.

Require the exact identity `P=h^v ++ T`. Canonical overflow has v=0,
because its raw head differs from h. The implementation checks v reaching
or exceeding r as well as v<r; exposed coefficients are supplied by X,
rather than guessed independently of the preceding source.

**Necessity, including overlap.** For a genuine canonical edge with source
和 target lengths at least r, take X to be the actual first s coefficients.
They exist: `m+g-2v>=r`, 和 overflow implies v=0. Choose k as the actual
carry entering the last s source coefficients. The 两 normalizations recover
the actual end digits, even when their windows overlap. The displayed P is
therefore the actual raw prefix. Exact canonical trimming gives `P=h^v++T`.

**Constructive sufficiency at prescribed width.** Suppose an extension exists.
For any `m>=2s+1`, let `d=m-2s` 和 set

`C = X ++ [2h*k]^d ++ reverse(X)`.

The nonempty constant middle resets either incoming carry to k: coefficient 0
forces carry 0, 和 coefficient 2h forces carry 1. Consequently its right block
uses exactly the checked k. The whole C is symmetric, bounded, canonical,
和 carry-flipping; its physical midpoint coefficient is even at odd width.
Its raw prefix is `h^v++T`, so the nonneutral T head forces trim exactly v.
The actual successor has prefix T 和 length `m+g-2v`.

Thus, at every width `m>=2(r+v)+1`, extension existence is equivalent to
existence of the prescribed genuine one-step local edge. This equivalence
concerns individual edges; the middle chosen for the next edge can differ
from the current edge's actual output middle. SHORT-state exclusions are
outside the optional LONG-only search's scope.

For a closed width schedule, let `offset[0]=0` 和
`offset[t+1]=offset[t]+g[t]-2v[t]`. A suitable initial width is any
`m0>=max_t(2(r+v[t])+1-offset[t])`.

## Decimal completion with prescribed residues

Write V(W) for the units-first coefficient value of W. If a symmetric word
has even length, its value is 0 modulo 11. For odd length an even midpoint
does 不 impose an additional residue restriction modulo 99 at sufficient width.

Let the middle's required exit carry be k 和 put `z=10k`.
For every even middle length d>=4, start with

`M4=[z,a,a,z]`, `V(M4)=11(z+a) mod99`.

For a desired residue U divisible by 11, choose `a=(U/11-z) mod9`.
Then a lies in `0..8`. The outer coefficient z forces the desired carry.

For every odd middle length d>=5, start with

`M5=[z,a,2c,a,z]`, `V(M5)=2(z+10a+c) mod99`.

For any desired core residue U, set `w=(50U-z) mod99` 和
`(a,c)=divmod(w,10)`. Here `50*2=1 mod99`, a,c lie in `0..9`, 和 2c
is an even legal midpoint. These cores send either entering carry to k.

Add p neutral coefficients to each end to reach the prescribed middle length.
For an odd core, padding transforms its residue by

`U -> 9+10^p(U-9) mod99`.

This transformation is its own inverse, since `10^(2p)=1 mod99`.
For an even symmetric core, padding leaves its residue unchanged:
the initial residue is divisible by 11 和 `10U=U mod99`.

For X of length s, middle length d, 和 desired full-center residue Q, choose

`U = 10^s * (Q - V(X) - 10^(s+d)*V(reverse(X))) mod99`.

Multiplication by `10^s` is its own inverse modulo 99. At even full width,
the prescribed Q must be divisible by 11; then U is also divisible by 11.
At odd width, Q can be arbitrary. Hence every `m>=2(r+v)+4` admits this
completion: even d>=4 uses M4, 和 odd d>=4 necessarily means d>=5.

The replay imposes the prior recurrence

`S[t+1]=2*S[t]+4*e[t]-2 mod9`,

和 the prior modulo-11 condition `V(C)=0` at even width, `V(C)=9` at odd
width. The first follows from normalization with entry e 和 exit 1-e;
neutral trimming changes the coefficient sum by a multiple of 9.
For odd non-overflow steps the raw alternating value is `2(V(C)+1) mod11`;
for even overflowing sources it is `-2=9 mod11`. Neutral-pair stripping
preserves residue 9 at odd width. Even symmetric successors have residue 0.
The code independently checks every actual target against the next phase's
specified modulo-99 residue, including the final-to-initial phase.

## Computed witnesses 和 independent checks

The nontrivial source extensions of the existing r4 loops are:

| Driver | Phase, starting at 0 | v | Extension | Deep carry |
|---|---:|---:|---|---:|
| p11/k1 | 10 | 2 | `[7,4]` | 1 |
| p12/k2 | 2 | 1 | `[11]` | 1 |
| p12/k2 | 11 | 1 | `[1]` | 0 |
| p12/k2 | 13 | 1 | `[5]` | 1 |

The remaining edges use an empty extension 和 their recorded boundary carry.
`prefix_extension.py` replays 11/11 和 24/24 edges with constant middles.
Its chosen p11 initial width 9 gives widths 9..13 和 1 matching full-center
seam; p12 initial width 11 gives widths 9..12 和 6 matching seams.

`local_lift_audit.py` independently uses paired-carry dynamic programming at
initial width 12. It visits 508 states for p11 和 494 for p12, finds every
local edge feasible, 和 compares 924 small completion counts with brute force.
Its 35 local completions also pass ordinary integer reverse-add checks.
The selected completions have 10/11 和 21/24 seam mismatches. These counts
depend on the selected completions; they are 不 minimum-mismatch theorems.

The strengthened modulo-99 constructions give:

| Driver | Edges | m0 | Width range | Sum v | Mod9 initial residue | Seam mismatches |
|---|---:|---:|---|---:|---|---:|
| p11/k1 | 11 | 16 | 16..20 | 2 | 3, unique | 9/11 |
| p12/k2 | 24 | 16 | 14..17 | 3 | 0, chosen from 9 options | 21/24 |

`prefix_completion.py` checks 1,296 middle/residue constructions with each
incoming carry bit, then 35 full mirror local edges. Source 和 target midpoint
parity, exact trims, cyclic widths, prefix closure, 和 next-phase residues 都
pass. Normal 和 `python -O` runs give identical outputs. Validation uses
explicit exceptions, so these checks also execute under `-O`.

The extended-prefix selftest checks 54,107 projection edges 和 constructive
lifts, including 18,745 overlapping-window edges 和 685 with `v>=r`.
Inputs comprise 2,824 exhaustively enumerated symmetric words in bases 2..5,
5,000 seeded decimal words, 和 1 explicit long-trim source. A full-word mirror
step checks every returned completion. This is finite computational validation,
supplementing the paper proof above.

## Reproduction 和 repository gate

From the repository root, with parent PR #343 present:

```bash
python3 calculation/agent-105/prefix_extension.py audit --depth 4 --seconds 30
python3 calculation/agent-105/prefix_extension.py audit --depth 4 --e 101010010101 --g 100010001000 --repetitions 2 --seconds 30
python3 calculation/agent-105/prefix_extension.py selftest --seconds 60
python3 calculation/agent-105/local_lift_audit.py --selftest --width 12
python3 calculation/agent-105/prefix_completion.py
python3 -O calculation/agent-105/prefix_completion.py
python3 tools/verify.py --changed
```

Expected statuses are `OLD_LOOP_LOCALLY_LIFTED` for the first 两 commands,
`PASS` with the stated selftest counts, 11 和 24 locally SAT edges in the
independent audit, 和 `LOCAL_MOD99_LIFTS_PASS` for the final 两 commands.
Each computation fits the sandbox budget; 没有 Studio run is needed.

**Repository gate:** literal `python3 tools/verify.py --changed` returned
`ALL CHECKS PASSED (changed files only, against origin/main)`: 5,217 Lean
files / 301 projects satisfy repository rules; 0 Lean modules changed,
built, or axiom-audited. The final checked tree is the published tree.
Repository consistency checks do 不 convert the paper arguments or finite
Python computations into Lean-verified mathematical theorems.
