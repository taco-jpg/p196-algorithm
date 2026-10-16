# Exactly two zero-carry histories for a protected finite-horizon family

Agent #3, protected task `agent3-three-layer-dead-prefix-20261016`.

For every `m : Nat` and `k > 0`, this contribution constructs exactly
`2^m` distinct initial coefficient words and exactly `2^m` distinct
protected coefficient words, all of width `2 * (m + k + 10)`. Each
protected word has two incoming layers in the original Agent #9
`ActualFiber` relation and has no third such layer. Every initial word
has a positive ordinary decimal realization, and every ordinary
realization avoids palindromes at every time `0 ≤ t ≤ k + 3` and has the
same time-four value, `digitValue (target (m + 9) k)`.

The complete statement is
`P196.Agent3.ThreeLayer.finite_horizon_exact_two_history_family` in
[SharpHistoryTheorem.lean](SharpHistoryTheorem.lean). The separate
`sharp_initial_canonical_chain` theorem records the three coefficient
transitions and their actual terminal carries `0, 0, 1`.

The four frozen mathematical sources and their author evidence were
published at
[`6ce47fddb10f15b4af1025954f1694825093673d`](https://github.com/taco-jpg/p196-algorithm/commit/6ce47fddb10f15b4af1025954f1694825093673d).
The contribution is submitted as [PR 130](https://github.com/taco-jpg/p196-algorithm/pull/130),
stacked on the prior two-history contribution. The ownership claim is
`3fbf616030a09c373b62b285827ff4851ada2052`; the exact scope was proposed on
[issue 61](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225498922).

## Construction and exact count

The existing two-history construction accepts a Boolean choice list.
Here its first three choices are fixed to `[true, true, false]`, followed
by an arbitrary list `free` of length `m`:

```lean
def depthBits (free : List Bool) : List Bool :=
  [true, true, false] ++ free
```

The inherited construction appends its six correction bits. Thus the
completed choice list has length `m + 9`. With the initial outer
coefficient and a reservoir of `k` copies of `18`, the protected half
has length `m + k + 10`; mirroring gives the stated even full width.
The first four target-half coefficients are `[14, 14, 14, 5]`.
[ActualDepth.lean](ActualDepth.lean) proves this prefix without imposing
any restriction on the remaining choices.

The two enumerations in [SharpHistoryFamily.lean](SharpHistoryFamily.lean)
are `sharpHistoryFamily0 m k` and `sharpHistoryFamily2 m k`. Both map the
duplicate-free enumeration of all length-`m` Boolean lists through an
injective word construction. Their list lengths are exactly `2^m`, and
both lists satisfy `Nodup`. Applying `stepWord` twice to the initial list
gives the protected list in the same order. These counts concern
coefficient words; individual decimal realizations are quantified
separately.

Write `q0`, `q1`, and `q2` for the successive canonical words. For `k > 0`,
`sharp_initial_canonical_chain` supplies the following actual transitions:

| Input | Image under `Agent8.stepWord` | Computed terminal carry | Width of input |
| --- | --- | --- | --- |
| Initial word `q0` | `q1` | `0` | `2 * (m + k + 10)` |
| First successor `q1` | Protected word `q2` | `0` | `2 * (m + k + 10)` |
| Protected word `q2` | `target (m + 9) k` | `1` | `2 * (m + k + 10)` |

The three words are canonical and even. The common coefficient target
has one additional position and is the unchanged prior target

```text
[5] ++ replicate (m+9) 10 ++ [14] ++ replicate (2*k-1) 18 ++
  [14] ++ replicate (m+9) 10 ++ [5].
```

Here `replicate` denotes repeated list entries. Coefficients such as
`14` and `18` are column sums, not decimal digit characters.

## What “exactly two” means

The definition `ExactlyTwoZeroCarryLayers ss` uses the unchanged original
relation from
[Agent #9 ActualWords.lean](../two-history-20261016/dependencies/agent9/ActualWords.lean).
For a target half `ss : List (Fin 19)` and candidate half `ys : List Nat`,
that relation is precisely

```lean
ys.length = ss.length ∧ (∀ y ∈ ys, y < 19) ∧
  (scan (mirror ys) 0).2 = 0 ∧
  Agent8.stepWord (mirror ys) = mirror (ss.map Fin.val)
```

Thus every edge is an actual full-word transition of bounded, equal
half-width mirrored coefficient words with zero computed terminal carry.
The exact-depth assertion says that two such incoming edges exist and
that no sequence of three such incoming edges exists. Its depth endpoint
is the protected word `q2`.

[DeadPrefix.lean](DeadPrefix.lean) proves the more general obstruction

```lean
no_three_paths_dead_prefix
  (tail a b : List Symbol) (c : List Nat) :
  ¬ (Path ([14, 14, 14, 5] ++ tail) 0 (a.map Fin.val) ∧
     Path a 0 (b.map Fin.val) ∧ Path b 0 c)
```

The local transition relation forces first-predecessor prefix
`[7, 7, 7, 2]` and second-predecessor prefix `[3, 13, 13, 0]`. A third path
reaches state `2` immediately before coefficient `0`, where no local
transition exists. The argument works for every remaining tail.

`no_three_actual_fibers` in [ActualDepth.lean](ActualDepth.lean) transports
that result to three actual fibers. Each layer uses the original
`actual_realizes` followed by `realizes_path`. Existence of two layers
uses the existing `history_path1` and `history_path0` witnesses and the
original forward bridge. The arithmetic converse and path semantics
remain those of the imported Agent #9 sources.

The resulting initial-word exclusion is stated with its full scope in
`sharp_initial_no_zero_predecessor`. For every listed initial word `w`
and every `ys : List Nat`, the premises

```lean
2 * ys.length = w.length
∀ y ∈ ys, y < 19
Agent8.terminalCarry (mirror ys) 0 = 0
```

imply `Agent8.stepWord (mirror ys) ≠ w`. This covers every bounded
mirrored candidate of the same width with zero terminal carry. The
result makes no claim about different widths, incoming overflow edges,
or unrestricted ancestry. The prefix obstruction, the two-layer
existence statement, the enumeration, and this exact predecessor
exclusion also hold when `k = 0`; the combined overflow and numeric
safety package assumes `k > 0`.

## Ordinary integers and time indexing

The inherited
[IntegerInterfaces.lean](../two-history-20261016/IntegerInterfaces.lean)
defines `IntegerRealizes n w` by a canonical finite decimal digit
representation of `n` whose mirrored column sums are exactly `w`.
All families here have even canonical words, so the existing
realizability theorem supplies at least one positive ordinary integer
for every initial word. `sharp_initial_integer_package` applies to
**every** `n` satisfying this realization relation.

Let `orbit n 0 = n` and let each further step be ordinary decimal
reverse-and-add. The theorem proves

```lean
0 < n ∧
  (∀ t, t ≤ k + 3 → ¬ Palindrome (orbit n t)) ∧
  orbit n 4 = digitValue (target (m + 9) k)
```

The coefficient words of the integer orbit at times zero, one, and two
are `q0`, `q1`, and `q2`. At time three the normalized decimal output
has the common coefficient word `target (m + 9) k`; its next numeric
step, at time four, is the common ordinary value. `digitValue` evaluates
the finite coefficient list as a base-ten polynomial, so the displayed
target is not being interpreted as a string of single decimal digits.

The safety proof reuses
[HistorySafety.lean](../two-history-20261016/HistorySafety.lean): odd outer
column sums exclude palindromes at times zero and one; the existing
central `18` reservoir excludes time two; the inherited normalized
finite-horizon theorem covers times three through `k + 3`. For `k = 1`,
this includes time four. The family varies with the prescribed finite
horizon `k`. No fixed seed or all-time avoidance assertion follows from
these quantifiers.

## Source provenance

The prior 23-module closure is reused byte-for-byte from reviewed base
`89287c9d3eb7dd801c2b1a59eff03140d47d24ec`. The mathematical two-history
source checkpoint is `a5d84665cfe4897387d80178fbcce79cd128c23e`. The original
core sources retain their `4b4edf976b2c7a9ba1dad80636c0e21c66350325` pins;
the four original Agent #9 copies retain provenance from
`7be455c03d777e5e0ca1d44bea4d1330e3f764c7`. Complete per-module hashes,
Git blob identities, direct imports, and declaration lists are in
[verification/source-pins.json](verification/source-pins.json).

The historical third-layer observation comes from the separate
[checkpoint](source-preservation/astra_counting_checkpoint.txt),
[generator](source-preservation/astra_counting_nooverflow_depth.py), and
[saved result table](source-preservation/astra_counting_nooverflow_depth_results.json)
under original snapshot `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.
Their exact original bytes are retained with SHA-256 and Git blob
identities in
[source-preservation/source_identity.json](source-preservation/source_identity.json).
The earlier safe-image note supplies context for the inherited
two-history family; it is a separate source from this third-layer table.

This contribution formally checks the four-column obstruction and its
application to the specified family. Preserving the historical generator
and result table does not certify every entry in that table or the full
determinized graph. The package records the historical observation and
the formal result without a novelty claim.

## Verification and retained attempts

The canonical and independent clean builds both passed all **27 pinned
modules** under Lean 4.19.0 with `--trust=0`. The canonical run produced
**zero warnings** and audited **231 explicit declarations**, including
all **three private helpers**, across **17 contribution modules**. Its
complete compiled-owner inventory contains **620 constants**: **373
logical constants**, each receiving a `#print axioms` audit, and **247
compiler implementation constants** recorded separately. Every explicit
source declaration belongs to the logical set. The only reported axioms
are `Classical.choice`, `Quot.sound`, and `propext`.

The portable verifier, source pins, and canonical report are in
[verification/](verification/). The independent source review and clean
rebuild are in [review/](review/). The canonical
[artifact index](verification/evidence/artifact-index.json) hashes all
**35 retained evidence files**, excluding the index itself.

| New module | Explicit declarations | Purpose |
| --- | ---: | --- |
| `DeadPrefix` | 15 | Local forced transitions and the arbitrary-tail obstruction |
| `ActualDepth` | 14 | Original actual-fiber transport and exact predecessor scope |
| `SharpHistoryFamily` | 16 | Injective enumerations, widths, and inherited integer safety |
| `SharpHistoryTheorem` | 7 | Exact-depth and finite-horizon aggregate |

The frozen source hashes are:

| Module | SHA-256 |
| --- | --- |
| `DeadPrefix` | `09c01111e2eb2f57637fe7d3a04e45aca4ca3d20c0248dc349e956c6ffc1fc64` |
| `ActualDepth` | `dcc9655c0fe9f60419fc60b821e225f705f3ce713792419586d623125ca9d0e2` |
| `SharpHistoryFamily` | `6e3b02999b118ed00133d7bebdbf553a6f19d6bfaec4f6abbf982ab7ee2fb002` |
| `SharpHistoryTheorem` | `d6afdf3e252b1b223ad30548ba6f72a3ba17604dfba43563ea28a5a9435a2f29` |

The original source snapshots, commands, compiler hashes, logs, and axiom
reports remain in [development/](development/). `dead-prefix/` retains
the failed first elaboration, which required unfolding `Forced` before
finite `decide`, and its successful second attempt. `actual-depth/`
retains a dependency-path preflight and the failed first proof attempt,
which needed explicit reduction of `(18 : Symbol).val`; its second
attempt passed. `family/` and `aggregate/` retain their successful first
attempts. These author checks identify their reuse of the existing
dependency cache; the final canonical and independent checks each build
all 27 modules afresh.

[ownership/](ownership/) preserves the claim and scope checks.
[CHECKPOINT_02.md](CHECKPOINT_02.md) remains the historical checkpoint
preceding final packaging. Resource cleanup records retain evidence that
only reproducible objects and a byte-identical duplicate download were
removed. All substantive mathematical attempts and verification records
remain available.
