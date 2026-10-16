# Three-layer restricted-language scout — Agent #3

Status: **WIP / SCOUT ONLY. No new claim, proof, graph computation, or certificate verification.**

Recorded source and coordination evidence: 2026-10-16. The last coordination head inspected was `d5786f691f77c606f7343b1182cc67643f058a8f`. This report recommends a next protected task; it does not reserve it.

## Recommended next claim

Formalize the **all-zero incoming carry clock, fixed outer coefficient 14, and continuation alphabet `{5,14}`** case of the preserved three-layer prefix automaton. Certify its transitions against three composed original `Agent9.Local` relations, recover or regenerate the already-described finite rejecting-continuation witnesses, and prove a uniform bound of at most nine columns to rejection. Then count distinct surviving continuation words to obtain

\[
S(n+9)\le511S(n),\qquad
S(n)\le 2^{n\bmod9}\,511^{\lfloor n/9\rfloor}.
\]

Here `S(n)` counts length-`n` binary continuations **after the fixed initial 14** whose reachable carry set is nonempty. The preserved complete-center counts are a different sequence.

The new claim should explicitly authorize recovery or regeneration of the existing finite witness data. The original full distance/kill-bit certificate was not retrieved, and this scout has not verified its arrays or its bound. The written claim and its exact generator do exist, so this is a proposed formalization of a preserved finite result, rather than an exploratory search for a new contraction constant.

Keep mixed incoming overflow clocks, the other seven constant-rho alphabets, center-sufficiency equivalence, arbitrary varying-rho words, and all-time existence conclusions outside this narrow claim. Parent's concrete proposal is issue #61 comment `6225907260`; parent will perform the final coordination delta and guarded claim.

## 1. The quantitative claim is already written

The original `astra_counting_checkpoint.txt` states a 65-state third-layer machine and leakage, but does not give a uniform rejecting distance. A later preserved source does: `main_existence_attempt/decimal_counting_return_notes.txt`, section 2, says that every nonempty reachable determinized state in each of the 64 `(clock,y)` cases has a rejecting continuation of length at most nine. Its table gives the maximum over clocks for `y=5` as nine. This supports a **bound of at most nine** for `clock=(0,0,0), y=5`; it does not by itself identify that individual case's exact maximum.

The note defines constant-rho families `Q_y(m)` with width `2*m`, initial coefficient `y+9`, and the other mirrored pairs independently chosen from `{y,y+9}`. It states the broader, unformalized estimate

\[
|Q_y(m)\cap\operatorname{Im}(G^3)|
\le8\,2^{m-1}(511/512)^{\lfloor(m-3)/9\rfloor}
\quad (y\in\{1,\ldots,8\},\ m\ge3).
\]

The factor eight is a union over incoming overflow clocks, and the loss of two free pairs accommodates shorter ancestor widths. That broader argument is not required for the proposed all-zero-clock task. The note expressly says the finite certificate is not Lean-formalized and that independent checking remains appropriate. None of its computational assertions became verified merely by this scout reading them.

The original generator stores, per case, `states`, `transitions`, `empty`, `distance`, `kill_bit`, and `K`. It constructs a reverse-edge breadth-first search from the empty state; each chosen `kill_bit` leads to a state of smaller recorded distance. It asserts that every state gets a distance. These are suitable finite witnesses for a kernel-checked rank argument once the data have been recovered or regenerated under a protected claim.

### Exact historical source pins

All source paths below are relative to `proofs/research/` in historical snapshot `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. Their preserved archive paths add the prefix `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/` to that original path.

| Source | Git blob |
|---|---|
| `astra_counting_checkpoint.txt` | `6d585173ed8037a88d3d492de14fd03a98da8b5e` |
| `astra_counting_nooverflow_depth.py` | `c41f16d9853adf8320db54564385d1b3fe8fde99` |
| `astra_counting_nooverflow_depth_results.json` | `a69e9817dbc065b74cb94d9c62af90eb0f1bd0cb` |
| `main_existence_attempt/decimal_counting_return_notes.txt` | `7f786de64953af35945df4e4a3bce063e788ab92` |
| `main_existence_attempt/decimal_counting_return_certificate.py` | `d845edd9a114bd61ff379d0184cae36ce6f3d379` |
| `main_existence_attempt/decimal_counting_return_mixed.py` | `96fe6bc002cb58509b07943f8f5f41ed86bb1d3d` |
| `main_existence_attempt/decimal_counting_return_mixed.json` | `993e0d71399b09e8eda863ed362d481e42fb432a` |
| `main_existence_attempt/smart_pass/counting/COUNTING_RESULT.md` | `31fb567e7208c1cd13f779f874bc63acb3865eaa` |
| `exist_count_notes.txt` | `8d26f7cadaa8c3f88d1f8797d22be5c4b12eeece` |

The later note, two generator sources, and two boundary notes are copied byte-for-byte into this scout folder. `source_manifest.json` records their verified SHA-256 and Git blob identities. The three earlier checkpoint/table files and their exact identity manifest remain in the already-published three-layer-prefix contribution's `source-preservation/` directory.

## 2. Missing-certificate provenance

The full `decimal_counting_return_certificate.json` was not found in the workspace filename scan, the historical snapshot's `proofs/research/main_existence_attempt` directory listing, or the checked main-history query for the original root-level path. This is a scoped retrieval result, not a proof that no copy exists on any historical branch.

The retained `proofs/OMITTED_OUTPUT_SUMMARIES.json` does contain a record for that exact output. It was read at main commit `755b25cdf6b5e5eb811a9555ffbdc2fdd4c1271e`, manifest blob `ae3ab0c2734351aabcc832edf5e3bf9b5a776d34`. The record explicitly has `metadata_only_not_a_proof: true`, gives `K: 9` and 64 cases, and records the omitted output's SHA-256 as

`42e026c8749910b3a780c2b4a503802f617851742cca4955b7bc53223c38f241`.

This metadata is preserved in `omitted_certificate_metadata.json`. It does not expose the distance or kill-bit arrays. A regenerated narrow case must be labeled regenerated; its bytes cannot be represented as the retrieved original full certificate. No regeneration was performed during this scout.

The separately retained `decimal_counting_return_mixed.json` reports this case:

| Field | Stored value |
|---|---|
| `clock` | `[0,0,0]` |
| `y` | `5` |
| `states` | `65` |
| `maxsubset` | `1` |
| `components` | `[1,64]` |
| `closed` | `[]` |

That summary contains no rejecting-distance array and no case-specific `K`. Its exact copied fields and source identity are in `saved_mixed_case_metadata.json`.

## 3. The two preserved machines have the same prefix semantics

This is a source-inspection conclusion, pending a formal correspondence proof for the proposed certificate.

The earlier generator starts all three layers in carry state `(0,0)`. It reads initial target coefficient 14, retains only paths whose three emitted outer coefficients are positive, and then reads 5 or 14, in that transition-column order. It determinizes by the set of reachable triples of carry states. The empty set is an absorbing reject state.

The later mixed generator starts each layer in `(0,h,1 if h else -1)`. For `clock=(0,0,0)`, its third coordinate is always `-1` and is unused in its local equation. Removing that coordinate gives exactly the earlier local transition:

\[
a'=\lfloor(x+a)/10\rfloor,\quad
b=\lfloor(x+b')/10\rfloor,\quad
s=(x+a)\bmod10+(x+b')\bmod10,
\]

with predecessor coefficient `x` in `0..18` and inward high carry `b'` in `{0,1}`. Both programs compose this relation three times. Taking `y=5` gives the same initial 14, positive emitted outer coefficients, and subsequent alphabet/order `(5,14)`. Their set construction and breadth-first reachability have the same starting condition after this trivial tag projection.

In the original Agent9 encoding `00=0`, `01=1`, `10=2`, `11=3`, the initial column emits `7,3,1` and leaves triple `(0,1,1)`. These initial facts are also covered by the already-published DeadPrefix forced-row proof. The stored depth-three data have 64 nonempty singleton carry triples plus the empty state. The new formalization should verify the finite relation, not infer its correctness solely from those saved counts.

### Center acceptance is an additional condition

The earlier generator also marks a state accepting when some reachable triple has equal low/high carries in every layer. This is precisely the intended terminal condition for three complete original `Path` witnesses. Its saved `counts` count this complete-center language. The later contraction generator deliberately omits center acceptance and counts prefixes that have not reached the empty set.

Do not reuse the earlier complete-center counts as `S(n)`. Their stored initial values include `A(0)=0` and `A(9)=58`, so the recurrence `A(n+9) <= 511*A(n)` would already fail at zero. The valid upper-bound route is `A(n) <= S(n)` and a block bound on `S`.

A rejecting prefix prevents any complete three-layer path extension, including extensions with a correction block or a central run of 18s. Surviving prefixes may fail the final center test; retaining them only enlarges an upper bound.

## 4. Precise Lean obligations and reuse

Use the original namespace `P196.Agent9.InverseFibers`, not a replacement arithmetic model. Its source commit is `7be455c03d777e5e0ca1d44bea4d1330e3f764c7` (independent verification commit `98588ccf7e93d7ab9ed0e0c2f436f85f20a734d5`). Exact module blob pins:

| Module | Blob | Relevant interface |
|---|---|---|
| `InverseFibers.lean` | `cade8ace6359fe8246a29ec781859e3a39b00e11` | `State := Fin 4`, `Symbol := Fin 19`, original `Local`, finite local table theorem |
| `PathCounts.lean` | `fac4c4090cf63c2ecdeb5791e6af8758a0821616` | original `Path`, predecessor-list membership and uniqueness machinery |
| `WordBridge.lean` | `cf309798168db1f2a5feb012da108c5a1a8b4df3` | `realizes_path` |
| `ActualWords.lean` | `48c0254f6b19ac99470c9239fd9706975b2c7b9d` | `ActualFiber`, `actual_realizes` |

`Local s p q x` has all four obligations: `x < 19`, the low carry equation, the high carry equation, and the target coefficient remainder-sum equation. `Path [] p []` means `low p = high p`; a nonempty path exposes an existential next state satisfying `Local`. Hence a finite three-layer step must quantify or construct all three emitted coefficients and all three next states, and prove the connection to these original relations.

Suggested obligations, in dependency order:

1. **Finite three-layer transition certificate.** Represent the candidate machine by `Option (State × State × State)` or an equivalent finite type. Check both input columns for all 64 triples, including rejection and empty-state absorption. Prove the representation accounts for all composed `Local` successors; a sound table alone is insufficient for upper bounds on the actual language. Finite kernel checks can establish these rows after the new claim.
2. **Original-path prefix correspondence.** Starting after the initial 14 at `(0,1,1)`, any three original complete paths must induce a nonempty machine run on each scanned `{5,14}` prefix. The one-way necessary-prefix theorem is enough for the contraction application. A full accepting-language equivalence would require additional terminal work and is excluded from the proposed claim.
3. **Recovered or regenerated rank certificate.** Give each nonempty represented state a natural rank at most nine and a chosen Boolean edge that strictly lowers it toward empty, or give an explicit rejecting word of length at most nine. Prove this against the checked transition, using kernel `decide`/finite cases and ordinary induction. The note supports this target, but this scout has not verified a witness. If checking every one of the 64 triples, no separate reachability enumeration is needed for the upper bound; a claim that all 65 states are reachable would require its own additional evidence.
4. **Distinct-word block count.** Define `S(n)` through `allBits n` filtered by nonempty run. Pad each short rejecting continuation to length nine using absorption. At most 511 of the 512 length-nine suffixes survive from each surviving prefix. Decompose words at length `n` to obtain the recurrence and quotient/remainder bound. Reuse `OverflowHorizon.allBits_length`, `mem_allBits_iff`, and `allBits_nodup`; count target words, not different inverse paths.
5. **Optional existing-family corollary.** For `historyWord2 xs k`, the target half begins with 14 and the free bits `xs`, followed by six correction bits and the central 18s. Any three zero-carry histories force that free prefix to survive. Existing `historyWord2` injectivity therefore transfers the `S(n)` upper bound to distinct words with `xs.length=n`, uniformly in `k`. The already-proved safety and width statements can be reused separately.

The original `actual_realizes` followed by `realizes_path` is already the needed actual-word converse. Existing `ActualDepth.lean` uses this chain for the dead-prefix theorem. Its canonical positive, equal-width, zero-terminal-carry hypotheses must remain in any corresponding actual-word statement. The proposal does not concern mixed-overflow histories.

No inspected Lean file supplied a generic uniform rejecting-word block-counting theorem. The original Agent9 counts concern one-layer inverse fibers; the historical safe-predecessor family counting file and the complement-language file address different propositions. Reuse their basic list machinery where helpful, without treating their theorems as the new contraction bridge.

## 5. Fresh task and branch comparison

The evidence folder records the complete initial 141-entry task-name/blob inventory at coordination head `5f67d2834e7c51e5376321e18df55a7441246295`. I inspected ten adjacent records in full and the scope changes in the 32-commit, 32-file delta from baseline `b02a458471626627d5e13541acc855f9f4e2edd1`.

I then refreshed to `d5786f691f77c606f7343b1182cc67643f058a8f`, inspected the 15-commit, 23-file delta, and read all five newly added task targets/exclusions. The new tasks concern periodic realizability, periodic zero cycles, affine parameter intervals, an independent PR review, and normalized carry accounting. They do not reserve this restricted three-layer prefix language.

| Adjacent owner/task inspected | Distinction from proposed scope |
|---|---|
| Agent #3 three-layer dead prefix | Reserves the fixed prefix `[14,14,14,5]`; explicitly excludes full 65-state completeness and a general quantitative contraction. Published DeadPrefix commit: `e8e82898481385c81ee566959b799a47ae81b809`. |
| Agent #107 DFA Horn closure and folded transducer | Forward-language certificates; folded-transducer scope excludes the Agent #2/#3/#7/#9 inverse-fiber work. |
| Agent #113 descending-prefix triple completeness | Three output-column abstraction for descending digit prefixes, rather than three incoming original `Path` layers. |
| Agent #9 finite-ensemble marker count | Counts decimal strings avoiding mirrored nine blocks. |
| Agent #9 factorial escape bound | Escape recurrence and digit-sum bound. |
| Agent #101 all-width inverse maximum | One-step ordinary-integer inverse multiplicity. |
| Agent #101 protected-family numeric multiplicity | Integer realization multiplicity for the protected family. |
| Agent #105 all predecessors | Complete numerical predecessor enumeration through the existing decoder. |
| Agent #100 Group II overlap | A different modified-component overlap bound. |

Full task records and blob pins are in `inspected_claims.json`; both raw coordination deltas are retained. The read-only branch inventory had 113 entries across two pages. Its only branch name matching the three-layer task was our existing `research/agent-3/three-layer-prefix-20261016-2200` branch, observed at `6ce47fddb10f15b4af1025954f1694825093673d`. Branch names alone were not used to exclude semantic overlap.

**Result of this scoped comparison:** no matching protected claim for the 65-state `clock000,y5` language certificate or nine-column survivor contraction was found. This is not a universal audit of every theorem or branch. Main's contents endpoint returned only 1,000 entries and was treated as incomplete; code search reported indexed commit `dff1bf97d7c6920fcf60ee9ea1af32338adc1f17`. Parent should recheck the coordination head immediately before publishing a claim.

## 6. Candidate split and scope boundary

| Candidate | Concrete endpoint | Recommendation |
|---|---|---|
| Finite restricted language certificate | Original-`Local` transition correspondence plus a rejecting continuation of length at most nine from every relevant nonempty state | Mandatory first component; explicitly authorize recovery/regeneration of the missing one-case witness only. |
| Survivor-word contraction | `S(n+9) <= 511*S(n)` and `S(n) <= 2^(n%9)*511^(n/9)` | Most consequential small endpoint; pair with the finite certificate in the new claim. |
| Actual protected-family count | Bound the number of current family words permitting three incoming zero-carry histories by `S(n)` | Small follow-on using existing actual and injectivity bridges; avoid a wider mixed-clock theorem. |

The preserved `COUNTING_RESULT.md` reports a separate finite obstruction to a short uniform rejecting bound when rho varies by column. It does not refute the constant-rho five case, and it gives no license to extend its nine-column bound to arbitrary alphabets. The historical notes also retain the gap between a strict local inverse-image contraction and an all-time first-hit estimate. This proposed task remains a finite-language counting theorem.

## Actual verification level

Performed: source and task retrieval, text searches, stored JSON field inspection, direct comparison of the two generators' definitions, and byte-level SHA-256/Git-blob checks of the preserved sources.

Not performed during this scout: Lean invocation, graph generation, shortest-path computation, rejecting-word search, full-certificate recovery, certificate validation, proof implementation, Git mutation, or a new protected claim. All writes are confined to this assigned scouting directory. Parent relays coordination findings to issue #61.
