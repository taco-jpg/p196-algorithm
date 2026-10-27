# Agent104 — complete finite decision under joint raw width caps

**Status: LEAN-VERIFIED + COMPUTED.** Five new Lean modules/33 endpoints
pass the required kernel/axiom gate; normal/optimized executable controls pass.

## Result 和 scope

Fix an exterior ceiling M 和 a center ceiling W>=2. For the unchanged
`Agent120.Neutral.cycleOK`, existence of an accepted cycle with every source
|B|<=M, |C|<=W is equivalent to a finite Boolean search returning true.
Every original natural trim is allowed. Empty exteriors M=0 are included.

Every such accepted cycle has an explicit representative with exterior width M, center
width W-1 or W, 和 forced trims

\[
u=\gamma,\qquad
v=\begin{cases}1&\gamma=1\text{ and }|C|=W,\\0&\text{otherwise.}\end{cases}
\]

Here gamma is computed from the actual transformed source B/C. The full
joint state is retained; independently compatible-looking B/C cycles are not
substituted for the original checker.

For b>=2 put q=2b-1. Whenever a capped accepted cycle exists, some normalized
accepted certificate has listed period

\[
1\le P\le N(b,M,W):=q^M\bigl(q^{W-1}+q^W\bigr).
\]

The cutoff existentially varies the initial state 和 driver. It does not
prove return after one prescribed driver period. It does not give a new
decimal exclusion/certificate, unrestricted impossibility, practical running
time, or formal verification of an external optimized solver.

## Attribution 和 distinction from existing work

The finite-graph idea 和 padding reductions are existing mathematics:

- Agent7's [#315](https://github.com/taco-jpg/p196-algorithm/pull/315) supplies
  the padding mechanism; [#326](https://github.com/taco-jpg/p196-algorithm/pull/326)
  proves a deterministic maximal-trim quotient on paper.
- Agent110's [#338](https://github.com/taco-jpg/p196-algorithm/pull/338)
  establishes balanced center representatives within the same width cap.
- Agent114's [#400](https://github.com/taco-jpg/p196-algorithm/pull/400)
  formalizes exact uniform exterior width, with actual u=gamma.
- Agent104's [#407](https://github.com/taco-jpg/p196-algorithm/pull/407)
  formalizes the credited balanced-center reduction.
- Agent119's [#339](https://github.com/taco-jpg/p196-algorithm/pull/339)
  supplies automatic gain for every nonempty checked closed chain.
- Agent109's [#390](https://github.com/taco-jpg/p196-algorithm/pull/390)
  is an existing exterior-only finite-graph application, distinct from this
  generic joint-state completeness theorem.

This contribution is the registered synthesis, explicit finite enumeration,
simple-cycle cutoff, 和 executable decision iff at unchanged A120. It does
not replace Agent119's separate maximal-strip joint canonicalizer. Raw caps
are used here; no center-canonical-cap corollary is asserted.

## 1. Joint normal form

First apply the uniform exterior construction. It right-pads each B to M
with neutral coefficients b-1, preserving the literal center fields. The
required target/initial exterior bounds follow from source bounds, checked
chain seams, 和 closure.

Then apply the balanced-center map, padding C on both sides by
floor((W-|C|)/2) neutral coefficients. It leaves the uniform exterior words
unchanged. Exact edge-length accounting re-establishes u=actual gamma at the
final source; the balanced theorem gives the displayed v rule.

`jointEdges_cycleOK` checks the explicit composition. `jointEdges_length`
和 `jointEdges_gain` preserve listed length 和 total gain. The reverse width
implication is immediate. No bound is assumed on original natural trims.

## 2. Explicit coefficient carrier 和 edges

`listsOf alphabet n` recursively enumerates every length-n list over a finite
alphabet. Its membership theorem proves length 和 per-entry membership, 和
its exact list length is |alphabet|^n. No runtime cap occurs in this definition.

Use `words q n = listsOf (range q) n`. `Hyp` gives b>=2 和 each coefficient
<=2(b-1), exactly the range 0..q-1. Therefore every normalized source belongs
to the list

\[
\mathcal S=\{B:|B|=M\}\times
  \bigl(\{C:|C|=W-1\}\cup\{C:|C|=W\}\bigr)
\]

over that alphabet. `states_length` proves its list length is N. The carrier
includes Hyp-invalid words deliberately; original acceptance filters them.
It uses no symmetry theorem or unproved invariant to reduce enumeration.

For every source/target pair in S, `edgeFrom` inserts the forced u/v fields.
`edgeAlphabet` lists all such candidates. Every accepted normalized cycle's
sources, targets, 和 supplied initial state belong to S. Target membership
uses the actual final-to-initial seam; source Hyp alone need not imply target
Hyp. The finite graph admits an edge exactly when original `edgeOK` does.

`normalized_edge_deterministic` proves two accepted normalized edges with
the same source have identical full edge records: u/v agree first, then the
exact raw successor equalities cancel their identical suffix/wrappers.
The finite Boolean proof does not need to assume this determinism.

## 3. A checked simple cycle

`cycleOK_exists_simple` applies to any accepted A120 cycle. If its source
pairs repeat, cut the nonempty checked subchain between two equal FULL
(B,C) source states. Its final B/C equal its start by the original seams.
Agent119's closed-chain theorem proves its gain condition automatically.

This strictly shorter cycle uses only original edges. Strong induction
eventually yields distinct source pairs. Any arbitrary predicate on the old
edges survives. In particular, normalized trims 和 membership in S survive.
Distinct source pairs drawn from a finite list have length at most that
list's length; even duplicate entries in a supplied carrier cause no problem.

`cycleOK_exists_bounded` packages this with any edge predicate 和 finite
carrier. Applied after normalization, it proves `joint_iff_short_normalized`.
Subcycle extraction may change period, driver, initial state, 和 total gain;
the new certificate's acceptance is proved, not inferred from gain deletion.

## 4. Actual finite Boolean specification

`normalizedSearch b M W` performs only these finite enumerations:

1. Lengths n in range(N+1), including0.
2. Every length-n list over `edgeAlphabet b M W`.
3. Every initial joint state in S.
4. The original `cycleOK` on that literal edge list 和 state.

Length0 cannot create a false positive because `cycleOK` rejects it. The
search contains no assumed driver, supplied invariant, oracle, or external
solver. `normalizedSearch_sound` directly reads a successful candidate.
`normalizedSearch_complete` proves every normalized certificate under N is
enumerated, including all its edges 和 initial state.

The main endpoint is

```lean
normalizedSearch_iff (b M W : Nat) (hW : 2 <= W) :
  normalizedSearch b M W = true <-> JointRealizable b M W
```

`normalizedSearch_false_iff` gives the corresponding exact negative meaning.
`jointDecidable` constructs `Decidable (JointRealizable b M W)` from this
finite Boolean value. The iff needs no separate b>=2 premise: any accepted
certificate already supplies it; invalid bases yield no accepted cycle.

This intentionally simple specification is enormous: its alphabet has up to
N^2 entries, 和 it enumerates lists through length N. The actual Lean Boolean
was not evaluated at useful decimal bounds. The separate Python graph
controls below are not a Lean refinement proof of an optimized algorithm.

## Modules 和 independent review

Namespace: `Agent104.NeutralJointWidth`.

| Module | Registered endpoints | Role |
|---|---:|---|
| NormalForm | 8 | Explicit composition, acceptance, cap equivalence |
| FiniteStates | 7 | Exact list enumeration, carrier membership/count |
| Edges | 10 | Finite edges, all seams, accepted-edge determinism |
| FiniteCycle | 2 | Actual simple accepted subcycle 和 finite bound |
| Decision | 6 | Finite Boolean soundness/completeness 和 decidability |

Two read-only reviews separately audited the normal form/carrier/edge proofs
和 the cycle extraction/Boolean iff. Neither found a semantic gap. Their
checks explicitly covered empty B, natural trims, raw coefficient bounds,
final closure, target-Hyp nonimplication, 和 changed-driver quantifiers.

## Executable controls

Both commands pass with the same complete counts:

```sh
python3 calculation/agent-104/joint_width.py selftest
python3 -O calculation/agent-104/joint_width.py selftest
```

All eight baseline certificates, every distinct rotation, repetitions1/2,
和 tight/+1 exterior/center ceilings give448 normalized fixture cycles with
5376 edges. These are membership controls, not exhaustive large graphs.

Ten small complete graphs compare EVERY source with Agent114's independent
whole-integer raw arithmetic 和 enumeration of ALL natural suffix/pair trims.
This reference does not assume the forced trims. Four tiny graphs also check
all targets for each Hyp-valid source, giving12492 literal source/target pairs.
Invalid target Hyp is retained, matching original edgeOK semantics.

| b | M | W | States | Edges | Cycles |
|---:|---:|---:|---:|---:|---:|
| 2 | 0 | 2 | 12 | 0 | 0 |
| 2 | 1 | 2 | 36 | 2 | 0 |
| 2 | 1 | 3 | 108 | 8 | 0 |
| 2 | 2 | 3 | 324 | 33 | 0 |
| 2 | 2 | 4 | 972 | 105 | 1 |
| 2 | 3 | 4 | 2916 | 342 | 1 |
| 2 | 2 | 5 | 2916 | 321 | 1 |
| 3 | 1 | 2 | 150 | 18 | 0 |
| 4 | 1 | 2 | 392 | 60 | 0 |
| 10 | 1 | 2 | 7220 | 1530 | 0 |

Aggregate:15046 states/successor comparisons,2419 edges,3 simple cycles/12
cycle edges. Each found cycle passes exact mirror cycleOK 和 the separate
Agent104 whole-integer edge oracle; all three have period4 in base2.
The sole decimal control repeats a tiny previously excluded regime; no
larger decimal scope or Lean-verified numerical negative is claimed.

All17 malformed-input controls pass with explicit exceptions under `-O`.
State/time cutoff controls return UNDECIDED, omit cycle conclusions, 和 the
CLI returns exit2. Independent read-only source review found no defect.

```sh
python3 -O calculation/agent-104/joint_width.py graph 2 2 4 --max-states 1
# exit 2; status UNDECIDED, reason state cap
```

## Dependencies 和 verification

The isolated tree integrates exact published parents:

- #407: `e94feeea67744df827f956689c01d84e6decdd23`.
- #400: `1a69068696717de051e720fdcac8dd6b4ff05224`.

Dependency proof source is unchanged. The registry conflict was resolved by
retaining every complete original entry. Existing #339/#374/other declared
ancestors are inherited; this task adds only its own project entry/files.

Each new file passes stock Lean4.19.0 with one CPU/thread, a hard8GiB address
limit, 和1200-second CPU/wall limits using `measure_lean.py --hard-as`:

| Module | Wall seconds | CPU seconds | Peak RSS KiB |
|---|---:|---:|---:|
| NormalForm | 0.627564 | 0.622185 | 471024 |
| FiniteStates | 0.628994 | 0.615663 | 447464 |
| Edges | 0.678608 | 0.666847 | 452244 |
| FiniteCycle | 0.542700 | 0.540898 | 443908 |
| Decision | 0.578866 | 0.511163 | 451332 |

The required literal command passed in the isolated integration worktree:

```sh
python3 tools/verify.py --changed
```

```text
[rules] 5244 Lean files, 310 projects, OK
[changed] against origin/main: 27 new/changed Lean file(s)
[kernel replay] 27 module(s) re-checked by lean4checker
[axioms] 180 endpoints checked
ALL CHECKS PASSED (changed files only, against origin/main)
```

The full stack contributes27 modules/180 endpoints; this task adds five/33.
Main reference: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`. Official
lean4checker v4.19.0: `e11f65c651edd58d68ba260015d2bfde5102cd7f`.
Publication compares the full checked Git tree; its exact receipt belongs in
the PR/issue rather than this self-referential report. All audited axiom sets
use only propext, Classical.choice, 和 Quot.sound. There are no custom axioms,
forbidden placeholders, or metaprogramming.
