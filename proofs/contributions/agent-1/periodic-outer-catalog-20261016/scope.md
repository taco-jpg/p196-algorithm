# Exact periodic outside coefficient × phase product: next scope

Source-only scout by Agent #1 specialist `/root/verification_plan`, 2026-10-16. No new Lean proof, mathematical search, experiment replay, Git mutation, or issue write was performed. Only this report was written. Stored JSON/gzip was decoded for source/provenance inspection, without running the original discovery modules.

## Proposed obligation and value

The exact outer arithmetic is already proved. The missing consequential interface is its projection through the **actual period-four maximal quotient**, followed by kernel certification of the retained 878-state/1,458-labelled-edge outer/phase product. This strengthens the new 59-phase abstraction by constraining each actual clock through the physical outside coefficient. It cannot establish a finite-interface return or the realizability of every abstract graph path.

Propose a narrow new task, subject to a fresh root claim:

1. Identify the quotient's physical outside head and actual last incoming carry using unchanged `Agent8.canonical_step`, including empty stored exterior blocks.
2. Combine this local outer relation with the frozen `rawPeriod_catalog_edge` using its **same actual rawGamma**.
3. Reify the already retained 878 product states and 1,458 labelled edges; kernel-check exact output specification, initial membership, and closure. Do not run another graph search.
4. Derive that every valid quotient transition from a catalog state remains in the product catalog. Any finite trajectory corollary must retain the original exponent guard for actual word transport.

The 878-state catalog is a stronger necessary projection than the phase catalog. Its concrete arithmetic connection is new glue; the scalar exterior map, carry rules, and original clock exclusions are prior work. The saved eight-clock loop survives this refinement, so this task is not an obstruction eliminating all nonzero cycles.

## Correct head coordinate, including empty exteriors

Use

```lean
outside B w := (B ++ w).headD 0
outerInput B H w := Agent8.lastInput (periodicWord B H w 3)
```

For positive exponents, `periodicWord_head` already proves that `outside B w` is the physical first coefficient of the full pair word. `B.headD 0` is wrong when `B=[]`; the period then supplies the positive outside coefficient.

The proposed exact local interface is:

```lean
theorem quotient_outside_step (B H w : Word)
    (hv : ValidPeriodic B H w) :
    outerInput B H w ≤ 1 ∧
    rawGamma B H w = overflow (outside B w) (outerInput B H w) ∧
    outside (quotientOuter B H w) (rawPeriod B H w) =
      nextExterior (outside B w) (outerInput B H w)
```

Also expose `0 < outside B w ∧ outside B w ≤ 18`, either directly from validity or by `canonical_head_bounds` at exponent three. No new normalization arithmetic is needed.

The source-backed derivation is precise:

- `periodicWord_canonical B H w 3 hv (by omega)` supplies `CanonicalPair Q3`.
- `canonical_step Q3 ...` supplies the actual output head, actual input-bit bound, and actual width update.
- `terminalCarry_eq_actual_overflow Q3 ...` identifies `rawGamma` with `overflow (Q3.headD 0) (lastInput Q3)`.
- `periodicWord_head` rewrites the input head to `outside B w`.
- `rawOuter` is `take (B.length+4)` of `stepWord Q3`. This prefix has positive length, so its head is the output head. Alternatively its exact length and existing `raw_outer_positive` exclude the empty case.
- `stripPeriodSuffix_outside (rawPeriod B H w) (rawOuter B H w)` proves
  `outside (quotientOuter B H w) (rawPeriod B H w) = outside (rawOuter B H w) (rawPeriod B H w)`.
- Because `rawOuter.length = B.length+4`, the right-hand head is simply `rawOuter.headD 0`.

This remains valid when stripping removes **all** of `rawOuter`. Then the residual head is supplied by `rawPeriod`; it is not silently replaced by zero. The center can be empty throughout. All-nine periods are handled by the existing phase edge's actual two boundary-bit labels; the outer incoming bit is the separate actual `lastInput Q3`, not an independently chosen realization.

For every actual input exponent `k≥3`, `quotient_step_bounded` identifies its successor with these same quotient blocks and gives a positive new exponent. Applying `periodicWord_head` on both sides yields the same head update. `scan_carry_stable` identifies that input's terminal carry with `rawGamma`. There is no need to prove equality of every exponent's `lastInput` to the exponent-three value merely to certify this product projection.

## Exact original outer relation and finite product

`outer_filter__4b3d159990f5e177.py`, lines 14–21, implements:

```
outer(p,g) = sorted set of
  p % 10 + (1 if g else (p+e)%10)
for e∈{0,1} with (p+e)//10 = g.
```

Under the existing physical bounds `1≤p≤18`, `e≤1`, this is exactly the already defined `Agent8.overflow` and `Agent8.nextExterior`:

```
overflow p e = if p+e<10 then 0 else 1
nextExterior p e = if p+e<10 then 2*p+e else p%10+1.
```

A clean relational interface is `∃ e, e≤1 ∧ overflow p e=g ∧ nextExterior p e=p'`. Its correspondence with the literal Python finite list is a small bounded specification lemma, not a reproof of the decimal arithmetic. If an executable output list is used, it must deduplicate targets **before** constructing product edges: for high `p`, both incoming bits give the same outer target. The original graph does not retain that inner bit as an edge label. Failing to deduplicate increases the 1,458 count.

The product edges retain:

- source `(period, physical outside coefficient)`;
- actual clock;
- the original optional all-nine pair of boundary carry labels;
- target `(new period, new physical outside coefficient)`.

Use the existing exact `PhaseEdge`/`phaseOutputs` semantics; do not identify rotations or erase all-nine labels. One implementation can filter the already literal `phaseEdges` by source and combine them with the deduplicated outer outputs. The archived product uses `outputs(period)` directly; a finite specification must establish equality with the chosen representation, including ordering if equality of lists is asserted.

All 18 initials are `([14,14,4,4],p)` for `1≤p≤18`. Prove these initial memberships, literal state count 878, state distinctness, edge count 1,458, exact outgoing specification, and target closure. The actual transition theorem should exhibit an archived edge whose source and target are the stated physical tuple projections and whose clock equals `rawGamma`. Initial membership and closure prove confinement; without a separate reachability proof, do not advertise Lean verification that every listed state is reachable or that the catalog is minimal.

The proof is expected to consist of short structural head lemmas, reuse of the existing scalar arithmetic, product membership bookkeeping, and larger kernel finite checks. The finite check may require deterministic chunks/resource settings; preserve any actual failures. The arithmetic bridge itself does not require another foundational import or a generic finite-automaton framework.

## What the old graph already establishes, and what survives

Retained artifact inspection found exactly 18 initial states, 878 stored graph rows, and 1,458 stored labelled edges. The saved SCC distribution is one component of 696, three components of 18, and 128 singletons. These are prior stored computational facts; this scout did not replay SCC construction.

The stored successive-overflow path layers are:

```
1 edge: 9→10, 10→1, 11→2, ..., 18→9
2 edges: 9→10→1, 18→9→10
3 edges: 18→9→10→1
4 edges: none
```

Consequently the old bulk loop clock `1000111`, when repeated, is already rejected because the cyclic join requires four consecutive overflows. The exact witness loop begins `[0,0,18,18]`; do not present its exclusion as new mathematics. Existing `Agent8.path_potential_bounds` plus the finite bounds of `upperPotential` can transfer the same no-four-overflows fact without redoing the normalization proof. In the indexed ordinary semantics, `CarryHistory.nonoverflow_growth_bound` already gives `K ≤ 2*noOverflowCount +3`, so `K=4` excludes four consecutive overflows directly. No separate public named exact `1000111` endpoint was located in the inspected flattened source; a newly named corollary would still be attribution-preserving packaging of this existing obstruction.

The shortest recorded surviving outer/phase loop has clock `10101010`:

```
([0,9,18,9],17) → ([10,10,8,8],8) → ([1,1,17,17],17)
→ ([9,2,9,16],8) → ([9,6,9,12],17) → ([2,16,16,2],8)
→ ([5,13,13,5],17) → ([10,9,8,9],8) → ([0,9,18,9],17).
```

It has four overflows and survives the outer product. Repeating twice closes the width residue modulo eight; the separate width specialist is scouting that exact coordinate. The old center/exterior realization remains unsatisfied. Original maximal-growth outer-three constraints allow four temporal alignments, but do not create a finite matching interface. No zero-cycle result removes abstract zero-phase self-edges; no scalar two-phase exterior result automatically applies to these nonconstant four-site phases.

## Provenance and dependencies

Inspected worktree `/workspace/p196-agent1-phase-20261016`, observed HEAD `c440e01ee4375384317cc2e428b7c43e8a04ecdf`. The parent continued publication concurrently; the following exact file identities are the useful pins.

| Source | Git blob | Relevant interface |
| --- | --- | --- |
| `proofs/PeriodObstructions__70ce034b31b5b218.lean` | `a89dda20e9a9b3452f7d0272b4fbd28f7d6ce119` | `overflow`, `nextExterior`, `finite_exterior_certificate`, `path_potential_bounds` |
| `proofs/ActualWordBridge__7f032d27940694a8.lean` | `d3f49353f9970c610d818d8f5da78ad5c739e7df` | `lastInput`; `canonical_step` line 135; `canonical_head_bounds` line 194 |
| `proofs/PrefixSemantics__3798a605dd95d8c6.lean` | `04a8cc9e73b87d271ca857a218b240e23f57c939` | `terminalCarry_eq_actual_overflow` line 107 |
| `proofs/Agent1PeriodicPositivity.lean` | `bc392c470c3bf3389f4ae0166cf67dcaf2462e89` | `periodicWord_canonical`, `raw_outer_positive`, `stripPeriodSuffix_outside` |
| `proofs/Agent1PeriodicSafetyAlphabet.lean` | `e5c1480c24770054ff24b7c770e457a5162a7d26` | public `periodicWord_head` line 47 |
| `proofs/Agent1PeriodicQuotient.lean` | `63bd5f4319f6a79924b7292db3eb82e0d027b26c` | `quotientOuter`, `quotient_step_bounded`, exponent positivity |
| `proofs/Agent1PeriodicValidity.lean` | `3c5673981d4c9a73a0ade71552f5867d8f73dd69` | `quotient_valid`, `valid_quotient_transition` |
| `proofs/Agent1PeriodicPhaseCatalog.lean` | `a9414bc8c9be783f5dfc48778db7161c481a96fc` | exact `PhaseEdge`; `phaseEdges_spec`; `rawPeriod_catalog_edge`; closure |
| `proofs/LychrelDigitSums__75febdc48f0ca802.lean` | `8a865176625283648a8a20dd2411ed77670eb0a2` | existing `CarryHistory.nonoverflow_growth_bound` line 3581 |

`Agent1PeriodicPhaseCatalog.lean` SHA-256 is `44445a343635503c940ea125727d0bbb75bbf7dce24be62c28a660241363f9f9`. Its author check is complete; the parent's independent combined review was running when this scout began. This report does not claim a later review outcome.

Archive base:

`proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/`

- `outer_filtered_graph.json.gz`: blob `c7bcc931f3cb36bd6845abeade0f7fd7b9723e08`; compressed SHA-256 `c3eb0a4bd4bc8e390d7681746e66300851035dff1b102412e2d14977ed1088e5`; decoded SHA-256 `cbd5c62ac2af58d0d0ce1cbb6f0cf9199ac49c75291d062179caf15f96e1ad50`.
- `outer_filtered_results.json`: blob `29ff1888439d8be43f3161dbdb59846d82063d7f`; SHA-256 `b444d8bcea8fb07368638b2f52cea57f2b4647dd385864313c12c9d0c4498506`.
- Flattened original `proofs/outer_filter__4b3d159990f5e177.py`: blob `ca0fe5e4cf9f6df4528d1e1375c9bfc404ad04f6`; SHA-256 `6c336a1b7d1d71e6525bec42a001572bfd7ee98115c2991b961d10c455f30d9c`.
- Original METHOD blob `5c5f94c66d6c3adb0288b610f748fcbed32b115c` explicitly classifies the product as necessary compatibility and its finite-interface lift as not instantiated.

## Ownership check and first action after a claim

Read all relevant direct task records at local coordination `cbb85526bf68812527c7392d3318a79315213093`; inspected the exact changed/new task records at remote snapshot `d8aab676e88fa0a42a3a660687e4a7a4d26e64c4` (163 direct tasks, complete nontruncated remote tree). Recent issue comments were read through `6226135055`, including Agent6's latest `6226131657`.

- **Agent6:** exterior coordinate dynamics is integrated, signed certificate accounting is reviewed, and normalized scalar carry accounting is now reviewed at Ready PR137 `f0e2097b82286128005ba81d8e50f2dca4e2d50b` (math `affa037ad537f3ae66a97008991850ce397f613a`). Its stripSuffix/normalized scalar stateOuter indicator bridge is a different object from the physical outside head of this four-site tuple. The next public proposal concerns scalar template finite-prefix band guards and palindrome avoidance. Preserve it; do not reuse its coordinate name as if it were the same head.
- **Agent110:** `agent110-exterior-two-step-return-20261016` remains claimed, target `advance (advance s) ≠ s` for every canonical `P196.Agent6.Exterior` at phase six, or an exact counterexample, including unbounded finite exterior words. This is a scalar two-phase state-return problem, not the four-site phase/head product. No reservation of that acyclicity lane is proposed.
- **Agent414:** active tasks concern original `bulkWord` temporal-period divisibility, the parsed/literal K boundary certificate bridge, and nonauthor review of Agent415's actual-strip correspondence. None is the 878-state product. Keep all these restricted-model and certificate scopes separate.
- **Historical interface lift:** `periodic_interface_followup` remains named in the retained original research without a recovered release or acknowledged transfer. This task would certify a necessary projection only; it must explicitly leave affirmative finite exterior/center lift and search ownership untouched.
- **Other boundaries:** do not broaden into Agent107's generic DFA/Horn closure, Agent7 run ancestry, Agent15 temporal-column lift, Agent418 multiblock realization, or the width specialist's modulo-eight coordinate task.

No exact equivalent active product-projection claim or declaration was found in the inspected sources/records. This is a scoped negative finding; a fresh claim check is still needed because coordination advances concurrently.

The first concrete action after claim should be the short `quotient_outside_step` interface above, using the existing canonical and strip lemmas. Publish that checked source checkpoint before the larger literal catalog certificate. Root can independently own catalog transcription/specification; a separate reviewer should check all archived labels, deduplication, physical head semantics, and a new complete source build/axiom audit. This partitions genuinely independent work without duplicating the original outer arithmetic.
