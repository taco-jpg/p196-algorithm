# Agent104 — verified functional search for bounded neutral certificates

**Status: LEAN-VERIFIED + COMPUTED.** Four new modules/22 endpoints pass the
required kernel/axiom gate; final normal/optimized executable controls pass.

## Result

At unchanged `Agent120.Neutral.cycleOK`, the explicit functional search decides
certificate existence under RAW caps |B|<=M, |C|<=W, for W>=2. It is proved
equal to the complete but impractical finite Boolean specification in
[PR422](https://github.com/taco-jpg/p196-algorithm/pull/422).

Instead of enumerating every edge list, it computes one possible successor
from the original raw transitions, checks that edge, 和 tests positive-length
returns from each finite carrier state. Original natural trims 和 empty B are
covered by the imported normal-form/cutoff theorem.

This is a registered Lean implementation proof. It does not establish a new
decimal lower bound/certificate, unrestricted impossibility, fixed-driver
period descent, practical performance at useful widths, or a formal
refinement theorem for the separate Python controls.

## Dependency 和 attribution

The single pinned parent is #422 at
`b0d30ba77a81aa7c9c457541b7c5da51f6aac51c`. Its proved normal form, coefficient
carrier, accepted-edge determinism, simple-cycle extraction, 和 finite cutoff
are reused unchanged. Its inherited sources credit Agent7/109/110/114/119.

This uses the fixed exterior/balanced center gauge, not maximal stripping.
Agent119's separate joint canonicalizer and other agents' actual driver
searches remain distinct. No dependency source or old project entry is edited.

## 1. The direct partial successor

`stateOK b M W (B,C)` checks only widths 和 coefficient bounds. The theorem
`stateOK_iff_mem` identifies it exactly with membership in the existing finite
carrier, without enumerating that carrier on each step.

For source s, let

\[
g=\operatorname{gam}(b,s.B,s.C),\qquad
v=[g=1\text{ and }|s.C|=W].
\]

Compute the sole possible target directly:

\[
t.B=\operatorname{take}_M(\operatorname{nextB}(s)),\qquad
t.C=\operatorname{take}_{|\operatorname{nextC}(s)|-2v}
       (\operatorname{drop}_v(\operatorname{nextC}(s))).
\]

Natural subtraction is used exactly as in Lean; acceptance still checks the
full original equations. The constructed `edgeFrom b W s t` has u=g 和 this v.
`successor` returns `some t` precisely when both cheap carrier tests 和 the
original `edgeOK` pass. Otherwise it returns `none`.

The principal local theorem, without extra base/width/Hyp assumptions, is

```lean
successor b M W s = some t <->
  s ∈ states b M W ∧ t ∈ states b M W ∧
  edgeOK b (edgeFrom b W s t) = true
```

The converse is not assumed from determinism. The proof recovers the literal
target from the accepted edge's suffix/pair equations using exact take/drop
identities. This also proves no legitimate normalized target is skipped.

Target Hyp is deliberately absent. For example, in decimal M=1,W=2,

\[
([1],[10])\longmapsto([3],[0])
\]

is accepted, but the latter state fails the carry-flip condition. The first
successor must return that target; only its following call stops. Both facts
are kernel-reduced in `Controls.lean`.

## 2. Positive returns 和 actual checked paths

`returns b M W start current fuel` is structural recursion on fuel:

1. At0, return false even if current=start.
2. Compute the current successor; `none` returns false immediately.
3. A successful target equal to start returns true.
4. Otherwise recurse at that target with fuel reduced by1.

It does not reject a repeated foreign state early or assume that every start
belongs to a cycle. Such a path may consume the full fuel without returning
to its specified start.

`returns_chain_sound` reconstructs a NONEMPTY literal checked chain from
current to start of length at most fuel. Every edge has the established
normalized fields. When current=start, `returns_cycle_sound` invokes the
existing closed-chain/gain theorem and yields original `cycleOK` acceptance.

Conversely, `returns_cycle_complete` follows every edge of an actual
normalized accepted cycle. All sources/targets are already in the finite
carrier, so the local iff forces the computed successor. A return earlier
than the supplied list's full period is allowed. Fuel at least the listed
length suffices; zero-length paths cannot create acceptance.

## 3. Complete finite functional decision

For the existing bound

\[
N=(2b-1)^M\bigl((2b-1)^{W-1}+(2b-1)^W\bigr),
\]

`functionalSearch` tests `returns s s N` for every carrier state s. It calls
the direct successor at most N times per start, hence at most N^2 calls over
the full scan. This is a structural algorithm bound, not a measured useful-
width performance promise; N itself is exponential in the widths.

Soundness reads the successful return witness. Completeness imports an actual
short normalized cycle from #422, whose source belongs to the scanned carrier
和 whose length is at most N. No fixed-driver period assumption is introduced.

Main endpoints:

```lean
functionalSearch_iff (b M W : Nat) (hW : 2 <= W) :
  functionalSearch b M W = true <-> JointRealizable b M W

functionalSearch_eq_normalizedSearch (b M W : Nat) (hW : 2 <= W) :
  functionalSearch b M W = normalizedSearch b M W
```

The corresponding false iff 和 `functionalDecidable` are also proved. This
establishes semantic refinement of the existing Lean specification by the
new Lean computation, not just a logical existence wrapper around an oracle.

## Kernel controls 和 resource-limited attempt

The final `Controls.lean` proves:

- The decimal accepted-edge/invalid-next-source boundary above.
- Complete binary search negatives at (M,W)=(0,2),N=12 and (1,2),N=36.
- A positive explicit binary return from `([2,1],[1,0,0,1])`, with fuel972.
- That return's carrier membership, hence `functionalSearch 2 2 4=true` 和
  `JointRealizable 2 2 4`.

The positive uses one exact `by decide` orbit and a proved existential scan
membership; it does not claim reduction of all972 starts. Direct local/orbit
reductions use no axioms; the higher-level search/existence consequences use
only the project's permitted logical axioms.

A combined attempt to reduce the full binary-positive/decimal-negative
carriers directly hit the hard8GiB address-space limit:90.052125s wall,
75.935807s CPU, peak5571272KiB RSS, exit134 allocation failure. Plain `decide`
had first hit its default recursion limit; the subsequent repository-approved
`decide +kernel` attempt was resource-limited. It supplied no retained proof.
The final file removes those attempted reductions. Binary success has the
explicit witness proof above; the decimal full-search negative has NO Lean
proof claimed here. Limits were not raised or bypassed.

## Independent executable controls

Both final-source commands pass:

```sh
python3 calculation/agent-104/functional_search.py selftest
python3 -O calculation/agent-104/functional_search.py selftest
```

The ten small scopes from #422 compare all15046 successors 和 all15046
N-fuel per-start return verdicts with its complete functional-graph oracle.
The reference also checks every natural trim through independent whole-integer
arithmetic; its earlier literal-all-target controls are not recounted here.
There are2419 edges, including1127 targets that fail Hyp, retained correctly.

The literal return loops consume335582 attempts, including full-fuel foreign-
cycle paths;12 positive starts lie on the3 known period4 binary cycles. The
largest per-start count is2916. Caching only stores this implementation's own
successor; every loop iteration still consumes fuel. Positive existential scans
may stop before exhausting the carrier and report that distinction explicitly.

Across eight baseline bases, four cap choices 和 every phase rotation give224
known-orbit returns/1792 replayed edges,32 short-fuel negative controls 和32
double-fuel first-return controls. Those large fixture carriers are not searched.
All positive edges receive exact mirror 和 independent integer replay.

Final guards:20 malformed inputs,4 outside-carrier states,5 positive-length/dead
return cases,6 state/step/time cutoffs. Cutoffs omit Boolean verdicts 和 return
CLI exit2. Normal/-O totals agree; independent read-only source/count review
found no defect. The only decimal complete graph is M=1,W=2, still a COMPUTED
control rather than a Lean numerical negative.

```sh
python3 calculation/agent-104/functional_search.py graph 2 2 4 --witness
# positive period4; 345 starts, 1336 attempts, 356 evaluated states
python3 -O calculation/agent-104/functional_search.py graph 2 2 4 --max-states 1
# exit2; UNDECIDED; no Boolean verdict
```

## Modules 和 verification

Namespace: `Agent104.NeutralFunctionalSearch`.

| Module | Endpoints | Role |
|---|---:|---|
| Successor | 6 | Cheap exact carrier predicate 和 literal step iff |
| Iteration | 3 | Checked-path reconstruction 和 cycle return completeness |
| Main | 6 | Functional decision, false iff, exact specification equality |
| Controls | 7 | Small kernel reductions 和 witness-based positive search |

Independent read-only review checked the local target recovery, all seams,
positive-length requirement, dead targets, fuel cutoff, changed-driver
quantifiers, 和 revised kernel-control scope. No semantic defect was found.

Each final source passes stock Lean4.19.0 under one CPU/thread, hard8GiB
address-space limit, 和1200-second CPU/wall limits:

| Module | Wall seconds | CPU seconds | Peak RSS KiB |
|---|---:|---:|---:|
| Successor | 1.058443 | 0.872254 | 465848 |
| Iteration | 0.564982 | 0.561462 | 465188 |
| Main | 0.517684 | 0.509019 | 430424 |
| Controls | 1.470355 | 1.156728 | 502144 |

Invocation: `python3 calculation/agent-104/measure_lean.py P196/Agent104NeutralFunctionalSearch/Controls.lean --hard-as --toolchain-bin /tmp/agent104-lean419/bin`,
with the corresponding source filename for each module. The literal gate passed:

```sh
python3 tools/verify.py --changed
```

```text
[rules] 5248 Lean files, 311 projects, OK
[changed] against origin/main: 31 new/changed Lean file(s)
[kernel replay] 31 module(s) re-checked by lean4checker
[axioms] 202 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

The stack contributes31 modules/202 endpoints; this task adds four/22.
Reference main is `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`; official checker
v4.19.0 is `e11f65c651edd58d68ba260015d2bfde5102cd7f`. Publication compares the
complete checked tree, with the exact receipt in the PR/issue. The final
deliverable uses only allowed axioms and no forbidden escape mechanism.
