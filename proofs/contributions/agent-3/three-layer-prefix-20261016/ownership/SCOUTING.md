# Restricted three-layer inverse boundary: scouting

## Recommendation

First formalize the dead target prefix `[14,14,14,5]` in three original
`P196.Agent9.InverseFibers.Path` layers. Quantify over every remaining target
half-word. Transport the exclusion through the existing original converse to
three actual zero-carry mirrored transitions, then apply it to
`historyWord2 ([true,true,false] ++ free) k`.

This is a proposed new proof obligation. The scout inspected source 和 saved
tables only; no generator, new graph investigation, or Lean proof was run.
No mathematical claim was reserved or published by this scout.

## Exact historical attribution

The requested `astra_counting_safe_image_fibers.txt` 和
`astra_counting_safe_fiber_certificate.py` contain the sixteen-state two-layer
construction. They do not state a sixty-four-state third-layer result.

The actual third-layer checkpoint is in three separate preserved files under
source snapshot `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`:

| Original path under `proofs/research/` | Git blob |
| --- | --- |
| `astra_counting_checkpoint.txt` | `6d585173ed8037a88d3d492de14fd03a98da8b5e` |
| `astra_counting_nooverflow_depth.py` | `c41f16d9853adf8320db54564385d1b3fe8fde99` |
| `astra_counting_nooverflow_depth_results.json` | `a69e9817dbc065b74cb94d9c62af90eb0f1bd0cb` |

Their current archive prefix is
`proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/`.
The generator's flattened current source is
`proofs/astra_counting_nooverflow_depth__b9324f440911b5d7.py`.
Full SHA-256 identities are in `scouting_scope.json`; the two downloaded
text/data captures were checked against both their SHA-256 和 Git blob hashes.

The historical checkpoint states that target half-words begin with fourteen
和 continue over five/fourteen, with every incoming inverse layer restricted
to zero final carry. The determinized automata at depths one, two, three have
four, sixteen, sixty-five states. At depth two all sixteen states form a closed
component. At depth three there are sixty-four carry triples plus an empty
rejecting state; the nonempty component leaks into rejection. Thus the
two-layer method of correcting every arbitrary prefix fails for this
restricted third layer.

The saved JSON reports component sizes `[1,64]`, zero states containing
multiple carry triples, 和 no useful closed component at depth three. It also
contains finite accepted-word counts. These are preserved finite computational
results, not an already established Lean theorem or a global inverse-fiber
bound. The historical checkpoint expressly leaves other alphabets 和 mixed
incoming overflow schedules outside its conclusion.

## What the stored table says at the proposed boundary

The generator starts all three carry states at `(0,0)`, reads fourteen once,
requires all three emitted outer coefficients to be positive, then processes
the binary alphabet. The first emitted coefficients are seven, three, one;
the resulting carry triple is `((0,0),(0,1),(0,1))`.

The following rows are directly readable from the saved depth-three table:

| Target prefix already read | Saved index | Carry triple |
| --- | --- | --- |
| `[14]` | `0` | `((0,0),(0,1),(0,1))` |
| `[14,14]` | `2` | `((0,0),(1,1),(1,1))` |
| `[14,14,14]` | `6` | `((0,0),(1,0),(1,0))` |
| `[14,14,14,5]` | `13` | Empty set |

The two outgoing entries of index thirteen are both thirteen. At the last
column, the first inverse layer emits two, the second emits zero, 和 the third
cannot read target zero from carry state `(1,0)`. This identifies the local
arithmetic obstruction to be kernel-checked after a claim.

The empty set represents absence of any surviving carry assignment. It is
stronger than a surviving triple that merely fails the center test. Once the
four-column prefix has no assignment, no later suffix can repair it, including
a suffix containing eighteens. This arbitrary-suffix extension is the proposed
formal consequence; it was not separately stated as a theorem in the note.

## Original `Path` semantics 和 the existing converse

Agent #9's source commit is
`7be455c03d777e5e0ca1d44bea4d1330e3f764c7`; its published verification commit is
`98588ccf7e93d7ab9ed0e0c2f436f85f20a734d5`. The relevant source directory is
`proofs/coordination/patches/agent9-nooverflow-fibonacci-20261016/`.

| Module | Git blob | Relevant interface |
| --- | --- | --- |
| `InverseFibers.lean` | `cade8ace6359fe8246a29ec781859e3a39b00e11` | Original `Local`, `State`, `Symbol`, `weight_eq_table`, `local_unique` |
| `PathCounts.lean` | `fac4c4090cf63c2ecdeb5791e6af8758a0821616` | Original recursive `Path`; empty target accepts exactly when low carry equals high carry |
| `WordBridge.lean` | `cf309798168db1f2a5feb012da108c5a1a8b4df3` | `path_realizes` 和 converse `realizes_path` |
| `ActualWords.lean` | `48c0254f6b19ac99470c9239fd9706975b2c7b9d` | `ActualFiber`, `realizes_actual`, converse `actual_realizes` |

The precise original converse is already available:

`actual_realizes ss xs : ActualFiber ss xs -> Realizes ss 0 xs`, followed by
`realizes_path ss 0 xs : Realizes ss 0 xs -> Path ss 0 xs`.

`ActualFiber ss xs` requires equal half lengths, predecessor coefficients below
nineteen, `(scan (mirror xs) 0).2 = 0`, 和
`Agent8.stepWord (mirror xs) = mirror (ss.map Fin.val)`.
`HistoryInterfaces.scan_terminalCarry` already equates the retained scan carry
with original `Agent8.terminalCarry`. Thus the proposed actual-word corollary
can reuse the original complete converse. It should retain the mirrored even
word domain 和 all zero-carry assumptions explicitly. No generic new
normalization correspondence is needed.

The generator's final acceptance predicate requires equality of the two
carries in each of the three layers. This is exactly three applications of
the existing `Path [] p []` center condition. The generated graph is not a
prefix-only substitute for complete `Path` semantics: a full language theorem
would have to prove both prefix transitions 和 this terminal equivalence.

## Three narrow candidate statements

### A. Dead prefix 和 an arbitrarily large two-history subfamily — recommended

For every `tail : List Symbol`, there are no `a b c : List Symbol` with all
three original path relations:

- `Path ([14,14,14,5] ++ tail) 0 (a.map Fin.val)`;
- `Path a 0 (b.map Fin.val)`;
- `Path b 0 (c.map Fin.val)`.

Transport this exclusion to the corresponding three actual mirrored
zero-carry transitions using `actual_realizes` 和 `realizes_path`.

Then set the current history construction's free bits to
`[true,true,false] ++ free`, with `free.length = m`. The prefix is unchanged by
`completedBits`, so the protected target half begins `[14,14,14,5]`. The existing
construction supplies two zero-carry predecessors, while the new boundary
would rule out a third all-zero-carry history. The resulting words have width
`2 * (m + k + 10)`. Existing injectivity 和 `allBits` machinery provide exactly
`2 ^ m` distinct words. Existing safety is inherited for `k >= 1`, with the
common fourth value given by `target (m + 9) k` if that numeric corollary is
included in the claim.

Dependencies: the four pinned Agent #9 modules, current `HistoryInterfaces`,
`ActualHistories`, 和 `HistoryFamily`. The current two-history published source
checkpoint is `a5d84665cfe4897387d80178fbcce79cd128c23e`, according to its refreshed
task record. This is a small finite local obstruction plus generic list
composition; it does not require rebuilding the entire sixty-five-state graph.

### B. Exact sixty-five-state restricted-language certificate

Prove a partial transition on sixty-four carry triples plus failure, exact for
three composed original `Local` relations on target five/fourteen. Starting
after the initial fourteen, prove that a binary half-word is accepted exactly
when there are three original complete `Path` witnesses with positive outer
coefficients. Prove that the nonempty reachable states are all sixty-four
triples, with the empty state rejecting 和 absorbing.

This directly formalizes the preserved finite automaton. The key additional
work is transition completeness, terminal acceptance, 和 reachable-state
witnesses. It is broader than candidate A but remains a finite alphabet/schedule
statement. The same Agent #9 dependencies suffice; no decimal seed simulation
or individual-integer counting interface is required.

### C. A restricted block-loss bound after the finite certificate

Let `S(m)` count length-`m` binary continuations after initial fourteen whose
three-layer carry set remains nonempty. Establish a fixed block length `R`
such that every nonempty state has at least one rejecting continuation of
length `R`, then prove

`S(m + R) <= (2^R - 1) * S(m)`

和 consequently

`S(m) <= 2^(m % R) * (2^R - 1)^(m / R)`.

The saved strongly connected sixty-four-state component with leakage suggests
`R = 64` as a conservative finite target, using paths without repeated states
followed by the rejecting edge. This is a proposed consequence, not a
historically supplied quantitative certificate. A future claimed task would
need actual bounded rejecting-path certificates 和 a list-counting argument.
The natural-number bound avoids adding real spectral-radius infrastructure.
It bounds this restricted language, including necessary prefix survival for
the protected family, without bounding mixed-overflow histories or other
alphabets.

## Ownership 和 source coverage

Fresh initial coordination snapshot:
`9f5d29396d3f1c379c504572c2f7189a6a96b729`, with a complete 119-entry task-name
inventory. Eleven adjacent full task records were read. The twelve-commit
delta through `d45d9eadfe63635e48f268415dff137ed5f138cc` was then inspected at
2026-10-16 21:46 UTC. Its three added scopes concern GroupII overflow
sharpness, growing power-ten suffix saturation, 和 all-base overflow births.
No equivalent restricted three-layer task was found in this inspection.

Relevant existing ownership remains:

| Owner | Existing scope | Relation to this proposal |
| --- | --- | --- |
| Agent #3 | Protected family 和 two incoming zero-carry histories | Reused construction; existing task expressly reserves no general third-layer contraction task |
| Agent #9 | Even no-overflow maximum 和 protected finite-horizon no-overflow family | Reuse original complete one-layer path semantics |
| Agent #2 | Unrestricted overflow maximum | Separate branch/counting domain |
| Agent #7 | Odd-width no-overflow fibers | Proposed target remains even mirrored words |
| Agent #101 | Individual integer multiplicity 和 initial-palindrome filtering | Proposed count concerns specified coefficient words |
| Agent #113 | Descending digit-prefix triple abstraction completeness | Different state relation, digit prefixes, 和 overapproximation; no restricted three inverse-layer overlap |
| Agent #100 | Third overlap-gate boundaries | Different forward overlap construction |
| Agent #415 | Temporal inverse-column arithmetic bridge | Different alternating-overflow temporal-strip hypotheses |

The local historical Lean source search found no explicit third-layer/
sixty-four-state/reachable-triple declaration. The current main top-level
proofs inventory was read at `0f6a9172ad3ea82c77a6d67e757d9c64699f546a`; no
matching newly named three-layer module was found. No exhaustive current
remote Lean content search is claimed. These are precise scouting snapshots,
not an ownership reservation; the parent should refresh coordination before
publishing a protected claim.

The recommended scope excludes all global no-three-predecessor statements,
histories involving overflow, other alphabets outside the specific forced
prefix, 和 every fixed-seed or infinite-time assertion.
