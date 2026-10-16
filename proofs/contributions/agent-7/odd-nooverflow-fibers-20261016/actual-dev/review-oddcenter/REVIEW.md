# Independent review of OddCenter

**Disposition: PASS for the frozen source and stated finite-word scope. No blocking finding.**

Reviewer: Agent #7 runtime/actual-arithmetic specialist, genuine subagent `/root/runtime`.
Author reviewed: Agent #7 center/enumerator specialist, genuine subagent `/root/gap_inventory`.
The reviewer did not author or edit the reviewed source. The shared Agent #7
namespace does not identify these two specialist executions as the same actor.

Reviewed source: `OddCenter.lean`, SHA-256
`72f1c2e64a587e25f85482b6f61ceea0763218d60c7c7cc5eaa7d1d31ca65728`.
This review pins exact source bytes; it does not invent a source commit before
the parent publishes those bytes. Coordination claim commit:
`3c415e96dcc95c28752fd1deaf6ad3185a4690ba`.

## 1. Center arithmetic and the two carries

The source center is an even pair coefficient `z` with `z < 19`; this is the
correct range 0 through 18 for twice one decimal digit. The target normalized
center is `v : Fin 10`. The state encoding is the pinned Agent #9 encoding:
`low p = p.val / 2`, `high p = p.val % 2`, so the four states encode the
incoming/outgoing carry pairs `(0,0)`, `(0,1)`, `(1,0)`, `(1,1)`.

`Center` checks both actual equations at the middle column:

```
(z + low p) / 10 = high p
(z + low p) % 10 = v.val
```

Thus neither boundary carry is a free certificate bit disconnected from decimal
normalization. Their combined integer equation is
`z + low p = v.val + 10 * high p`. Since the source center is even, its parity
forces `low p = v.val % 2`. Conversely, that parity condition yields exactly
the following bounded even coefficient:

| State p | Low carry | High carry | Allowed target digit | Source center |
|---|---:|---:|---|---|
| 0 | 0 | 0 | even v | v |
| 1 | 0 | 1 | even v | v + 10 |
| 2 | 1 | 0 | odd v | v - 1 |
| 3 | 1 | 1 | odd v | v + 9 |

This table was separately kernel checked for all 760 triples
`v : Fin 10`, `p : Fin 4`, `z : Fin 19` in
`ReviewCenter.center_carry_table`. Its proof uses direct `decide` reduction of
`Center`, not the author's `center_iff` theorem. The finite fixture checks the
explicit table interpretation; the author's universal `center_iff` supplies
the all-natural-source statement with its explicit bound.

The subtraction in `centerValue = v.val + 10 * high p - low p` is safe on
the permitted parity branch: when the subtracted carry is 1, the target digit
is odd and therefore at least 1. The upper boundary remains 18: even digits
are at most 8, and odd digits are at most 9. There is no hidden exclusion of
source center zero.

## 2. Boundary cases zero and eighteen

Two independent fixtures checked the complete boundary classifications:

- `Center v p 0` holds exactly for `(v,p) = (0,0)` or `(1,2)`.
- `Center v p 18` holds exactly for `(v,p) = (8,1)` or `(9,3)`.

The corresponding empty-half enumerator outputs were also kernel checked:

```
oddPreimages [] 0 0 = [([], 0)]
oddPreimages [] 1 2 = [([], 0)]
oddPreimages [] 8 1 = [([], 18)]
oddPreimages [] 9 3 = [([], 18)]
```

Separate fixtures confirmed the four matching wrong-parity states return the
empty list. Both computed carry bits matter at these endpoints: adding the
low carry 1 to source zero yields center digit 1 and high carry 0; adding it
to source 18 yields center digit 9 and high carry 1.

## 3. Enumeration completeness

The base case of `OddPath` accepts precisely `Center` when both outer lists
are empty. Length mismatches are explicitly false. Its inductive case keeps
the original Agent #9 `Local` relation and recurses with the actual next
state. The length and coefficient-bound lemmas preserve every required
condition, including source-center evenness.

The enumerator's terminal parity guard is equivalent to existence of a
center by `center_exists_iff`; the supplied `centerValue` is the unique one
by `center_iff` and `center_unique`. The recursive enumerator tries all four
states using the proved `mem_states`, and `labels` enumerates exactly the
bounded local arithmetic labels via the pinned `mem_labels` theorem.

The proof of `mem_oddPreimages` establishes both directions for arbitrary
symbol lists, carry states, half-words, and natural-number centers. In the
recursive direction the pair equality is decomposed into head, tail, and
center equality; the center is not discarded while the half-word is rebuilt.
This is an exact membership theorem, not a claim that a finite search happened
to find all examples.

## 4. Duplicate freedom

For each fixed first label, the extension map preserves the center and is
injective in the entire `(half-word, center)` pair. Distinct first labels have
distinct list heads. The source label list is a filter of the noduplicate
`List.range 19`.

The remaining possible duplication would come from two different guessed
next carry states producing the same extended pair. Equality of the extended
half-words forces the first arithmetic label to agree. The imported
`local_next_unique` then forces the next states to agree from their actual
local equations. I inspected that pinned lemma: it reconstructs both state
components from quotient/remainder identities and does not assume path
uniqueness or enumerator correctness. The proof therefore establishes list
`Nodup`, rather than just uniqueness of a projected path description.

## 5. Independent execution and axiom evidence

The exact reviewed source was already rebuilt independently by this reviewer
in `actual-dev/clean-004`, as an imported dependency of the separately authored
actual-word bridge. That execution compiled all seven local modules from
fresh source snapshots, with no project-object reuse. The reviewed center
module's four-module import closure is contained in that fresh build.

Every command used official Lean 4.19.0, release commit `6caaee842e94`, with
`--trust=0 -j1 -DElab.async=false`; every command exited 0. The executable
SHA-256 was
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
The same recovered official toolchain was shared; no independent toolchain
download is claimed.

The original 15 exported center theorem axiom reports were independently
checked from that execution. Their union is exactly the allowed foundational
set `propext`, `Classical.choice`, and `Quot.sound`. The additional five
review fixtures compiled successfully against source/object-hash-matched
objects from that build; every fixture reports only `propext`. There is no
`sorryAx`, custom mathematical axiom, or compiler-trusted evaluation shortcut
in the reported theorem dependencies.

Evidence:

- `actual-dev/clean-004/verification.json`: independent fresh execution.
- `actual-dev/clean-004/logs/OddCenter.log`: all 15 original export reports.
- `actual-dev/review-oddcenter/verification.json`: exact source/compiler/object
  checks, reviewer attribution, fixture command and log hash.
- `actual-dev/review-oddcenter/ReviewCenter.lean` and `.log`: independent boundary
  interpretation fixtures and their actual successful axiom reports.

## 6. Scope and downstream integration note

This source classifies finite odd mirrored coefficient words and their folded
local paths. It does not by itself claim canonical positive input, an
all-time decimal integer realization, or a result about the complete orbit of
196. The separate actual-normalization equivalence is in `OddActual.lean`;
this report is not represented as independent review of the reviewer's own
actual-bridge source.

For the parent's subsequent canonical filter, use positivity of the full
input head: `(oddMirror xs z).headD 0`, equivalently `xs.headD z`. Reusing the
even-word filter `xs.headD 0` would discard valid positive one-column odd
inputs because their outside half `xs` is empty. The reviewed source correctly
retains those inputs and intentionally leaves this later canonical filter
separate.

No source repair is requested. Remote publication, formal PR delivery,
integration, and any broader acceptance decision remain with the parent and
the repository's existing coordination protocol.
