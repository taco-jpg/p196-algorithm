# PR #149 bounded source preflight

**Result: no blocking mathematical or source defect found at frozen commit `a883847381cd800b13e511d8ccc8909ba998866c` (H).** The four new Lean modules faithfully state and construct the selected carryfree component of the original Theorem 3. No source repair is requested by this preflight.

**This is a source assessment, not final acceptance or execution evidence.** At H, the published nonauthor semantic evidence covers Residues, Digits, and Coordinates; the final Saturation review and independent execution evidence remain unpublished. I performed no Lean build, source edit, remote mutation, formal PR review, delivery claim, or main-slot action.

**The PR head moved during this review.** The last metadata read reports `1dafcf7c90f9b51a0de0781998b258b96edeb191`, two commits, 28 changed files, and Draft status. This report remains pinned to H and does not assess the later commit. The exact revalidation required is listed below.

## 1. Material read and exact source identities

I read every declaration and proof body in the four new modules, the complete registry, CONTRACT, README, SOURCE_FREEZE, CORRECTIONS, and both published contract/source semantic reviews. I also read the original historical mathematical source and the necessary definitions and proof bodies in the unchanged decimal foundation.

All five closure sources were fetched at H. Their SHA-256 values were independently recomputed from the fetched UTF-8 content in memory and match the registry and SOURCE_FREEZE. The Git blob identities returned by the connector also match the registry.

| Module / source path | Git blob | Independently recomputed SHA-256 |
|---|---|---|
| [`proofs/Agent14CarryfreeResidues.lean`](https://github.com/taco-jpg/p196-algorithm/blob/a883847381cd800b13e511d8ccc8909ba998866c/proofs/Agent14CarryfreeResidues.lean) | `52526e5d8c400783bbf03220fd5937bb5153eb60` | `7785adc325f7ae100cfcde21238f27d06a558c23d74a3fa03464ea356867ece6` |
| [`proofs/Agent14CarryfreeDigits.lean`](https://github.com/taco-jpg/p196-algorithm/blob/a883847381cd800b13e511d8ccc8909ba998866c/proofs/Agent14CarryfreeDigits.lean) | `8b7f903a870c772d7c7e329f93931de3e4ab5fac` | `ae394c8a19e6fc497c1cf83fdf77943abd3f0b8fd681e59006bc8f7524f4ece9` |
| [`proofs/Agent14CarryfreeCoordinates.lean`](https://github.com/taco-jpg/p196-algorithm/blob/a883847381cd800b13e511d8ccc8909ba998866c/proofs/Agent14CarryfreeCoordinates.lean) | `e06631541818a8ee8bf266193f35637a5a07bd21` | `5c2b5b72f14b8f002719fa77b54b63aef1a2fa644dd379bdb94dec4b3dbfa519` |
| [`proofs/Agent14CarryfreeSaturation.lean`](https://github.com/taco-jpg/p196-algorithm/blob/a883847381cd800b13e511d8ccc8909ba998866c/proofs/Agent14CarryfreeSaturation.lean) | `856d9a7b95e4b43501c0fb4b07955fc5279b8c26` | `2427fcac82b20afe208ae2529b1dc9436217395eef63fcceb707447b0064171a` |
| [`proofs/LychrelDigitSums__0810ace083af80c5.lean`](https://github.com/taco-jpg/p196-algorithm/blob/a883847381cd800b13e511d8ccc8909ba998866c/proofs/LychrelDigitSums__0810ace083af80c5.lean) | `8a865176625283648a8a20dd2411ed77670eb0a2` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |

Additional identities checked:

- **Registry:** Git blob `cf974d5d91fb0256cc99107e2a50f80e339d50e2`; SHA-256 `0a8454b8dbcf7ece3c117a3bcb2f7d3cffbf562f7decdefafbb4e72fc842f53c`.
- **CONTRACT:** Git blob `e8126024b452f452ba58f172d3ecfc76a74e5dac`; SHA-256 `ac077f99d5c5bbf49e5e5ef8801872178f3082888f03d417279b45a280c01feb`.
- **SOURCE_FREEZE:** Git blob `de4538f4bec15e6bf97d2186e2c3c46f2314fa7b`; SHA-256 `5f8a120d796e8c765830f31e52939035708c95266ca1574c26cbafec4c7f3f32`.
- **Historical mathematical source:** fetched by blob `eac5b8f61385a615d9cc3e7796a4d698c66b716b`; recomputed SHA-256 `d39212c9ab98f4c5b0fccb733d3b662e41a09804878178c82b8762684e97fb09`, matching the recorded source-map provenance at `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.
- **Unmodified canonical verifier:** Git blob `21131b03dfa516eb19a0a7a4df4f2a41020d4db1`; recomputed SHA-256 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`, matching the registry. It was not executed.

The exact registered import graph agrees with the source:

| Module | Direct imports |
|---|---|
| `LychrelDigitSums` | `Std` |
| `Agent14CarryfreeResidues` | `Std` |
| `Agent14CarryfreeDigits` | `LychrelDigitSums` |
| `Agent14CarryfreeCoordinates` | `Agent14CarryfreeDigits` |
| `Agent14CarryfreeSaturation` | `Agent14CarryfreeResidues`, `Agent14CarryfreeDigits`, `Agent14CarryfreeCoordinates` |

There are **22 distinct registered endpoints**, all present in the reviewed source. The four new files contain **55 explicit public declarations: 49 theorems and six definitions**. This source inventory is not a substitute for an executed module-origin/public-declaration audit.

## 2. Mathematical assessment

### Quantifiers and selected scope

The final odd endpoint has the correct order and strength:

\[
\forall L\ge5,\quad L\bmod2=1,\quad
\forall s<9,\quad\forall r<11,\quad
\exists n,d,\ \ldots
\]

The even endpoint similarly covers every even \(L\ge2\) and every \(s<9\). Width is fixed before choosing the witnesses. Neither endpoint assumes a desired residue, canonicality, a zero carry, or an output palindrome as an extra premise. Both include zero residue classes.

The statements concern actual natural-number inputs and the original numeric `Lychrel196.step` and `Lychrel196.Palindrome`. They retain the original `Canonical` and `Admissible` predicates. The contribution proves the selected carryfree construction and physical-coordinate realization; it does not establish quotient classification, overflow saturation, U/S, carry-support results, orbit reachability, or an infinite assertion about 196. This agrees with the frozen contract and README.

### Constructive coverage of all 99 odd classes

`residue_parameters` uses the explicit selector

\[
t=(55s+45r)\bmod99,\qquad
x=\begin{cases}99&t=0\\t&t\ne0,\end{cases}
\]

then

\[
u=((x-1)\bmod10)+1,\qquad b=(x-1)/10.
\]

Its proof establishes \(1\le u\le10\), \(b\le9\), \(u+10b=x\), and the two requested residues. The zero branch is retained using \(x=99\). This proves the universal parameter coverage through exact Euclidean arithmetic; no finite experimental result is substituted for the theorem.

`split_parameter` then proves all necessary bounds and the exact recombination for

\[
a=\min(u,9),\qquad c=u-a:
\quad1\le a\le9,\quad c\le1,\quad a+c=u.
\]

The natural subtraction here is appropriate because it splits a nonnegative digit parameter; the later alternating coordinate uses integer subtraction.

### Canonical inputs and exceptional widths

`threeDigits` places the source digits at \(L-1,L-2,L-3\), and its exact value and word-sum lemmas are proved. For \(L\ge5\), the leading digit is positive and the units digit is zero. The nonpalindrome proof applies the original numeric `palindrome_value_iff` and compares those unequal endpoints.

The original `Canonical` predicate is:

\[
0<L\ \land\ (\forall i<L,\ d_i\le9)\
\land\ 0<d_{L-1}\ \land\operatorname{value}(d,L)=n.
\]

Together with the inspected `value_positive` proof, this gives \(n>0\). A separate positivity conjunct is therefore unnecessary.

The width-five case is handled correctly. `threeDigits_column_formula` adds six spikes; it does not overwrite coincident positions. At \(L=5\), the two central contributions produce \(2c\le2\). The symbolic column bound retains this case. There is no hidden assumption that all six monomials occupy different positions.

The one-digit family includes \(L=2\): input \(a0\) produces \(aa\). Residue zero is represented by \(a=9\), so `90 -> 99` is included. The unused parity argument in the intermediate `even_carryfree_classes` theorem is harmless: that physical one-digit family works at every width at least two, while the final even spectral theorem explicitly uses even parity to prove cancellation.

### Actual computed carries and the ordinary-step bridge

The foundation definitions inspected are the actual decimal operations:

\[
\operatorname{carry}(q,0)=0,\qquad
\operatorname{carry}(q,i+1)=
\frac{q_i+\operatorname{carry}(q,i)}{10},
\]

\[
\operatorname{output}(q,i)=
(q_i+\operatorname{carry}(q,i))\bmod10,
\qquad
q_i=d_i+d_{L-1-i}.
\]

`small_columns_actual_step` instantiates the original small-column theorem with these computed functions, the original pair-word symmetry, the exact column equation, and definitional initial carry zero. It concludes zero carry at **every \(i\le L\)**, including the terminal index.

That derived terminal zero supplies `canonical_next_no_overflow` and `step_palindrome_iff_no_overflow`. Their needed proof bodies were inspected, including the bridge from positional reflection to the independent numeric reversal algorithm. The resulting theorem concerns the ordinary `step n`, with canonical output at the **same width \(L\)**. It is not a statement about an unrelated abstract transition.

### Literal integer evaluation, division, and residues

`coefficientEval` is the literal finite coefficient sum into `Int`:

\[
Q(x)=\sum_{i<L}(q_i:\mathbb Z)x^i.
\]

Its congruence, additivity, and spike lemmas preserve coincident coefficients. `canonical_columns_eval_one` uses the original word-sum and digit-sum bridges to prove

\[
Q(1)=2\,\operatorname{digitSum}(n).
\]

The odd construction proves

\[
Q(-1)=2\bigl((u:\mathbb Z)-(b:\mathbb Z)\bigr),
\qquad
Q(-1)/2=(u:\mathbb Z)-(b:\mathbb Z).
\]

Division occurs in `Int` after a factor-two identity, including when the half is negative. `odd_seed_half_mod_eleven` connects that exact signed half to the remainder of the **same explicit `oddSeed`**, using its established mod-99 value. The natural expression \(u+10b\) and integer expression \(u-b\) are related by congruence, not treated as identical expressions.

At even width, the final endpoint proves \(Q(-1)=0\), and consequently its half-coordinate modulo 11 is zero. It correctly makes **no assertion that the input \(n\) is divisible by 11**.

Both advertised controls are present:

- `negative_half_control`: `oddSeed 1 9 5 = 19000`, signed half \(-8\), remainder \(3\) modulo 11.
- `zero_classes_control`: `oddSeed 9 9 5 = 99000`, ordinary next value `99099`, and both requested ordinary residues zero.

These are source-level proof observations; I did not execute their elaboration.

### Same-witness assembly

`odd_source_coordinate_saturation` and `even_source_coordinate_saturation` assemble canonicality, initial numeric nonpalindromicity, admissibility, every computed carry, next canonical width, numeric next palindrome, residues, and literal evaluations for one selected pair \(n,d\).

I found no switch between unrelated existential witnesses, circular premise, inconsistent width condition, missing zero class, or weakening to eventual width or bounded-width testing.

## 3. Proof-policy assessment and execution limits

Complete inspection of the four new files found no `sorry`, `admit`, `native_decide`, new axiom, unsafe definition, oracle construction, or circular mathematical premise. Their proofs use ordinary definitions, induction, symbolic case splitting, simplification, `omega`, and kernel-checkable `decide`.

A whole-text trust-marker scan of the unchanged foundation found the forbidden-word occurrences only in explanatory comments declaring their absence. I inspected the foundation proof closure necessary for these new results; I did not independently re-review every unrelated theorem in the 5,491-line foundation.

The exact import graph, bytes, and source bodies give no identified source-policy defect. **They do not establish the final allowed-axiom result or successful compilation.** Those require the published strict execution and origin/public audits. The `#print axioms` commands in source are not observed audit output.

The author compilation announcements, archive descriptors, and checkpoint README were not treated as independent execution evidence. I did not unpack or independently validate the author archive. The complete failed/successful-attempt history remains unchanged.

## 4. Reuse of existing nonauthor evidence

The published evidence at H is reusable for its existing, explicitly limited scope because the checked bytes match:

| Evidence at H | Identity and reusable scope |
|---|---|
| [`review/contract-review.md`](https://github.com/taco-jpg/p196-algorithm/blob/a883847381cd800b13e511d8ccc8909ba998866c/proofs/contributions/agent-14/carryfree-residue-saturation-20261016/review/contract-review.md) | Blob `2e64435783923148dadcabce47f4b532b396d148`; SHA-256 `205ccab182c0de6c05388786cae5a7c2f4e5f68f5c65a91bea1eae769f879b82`. It explicitly confirms the exact CONTRACT hash and historical source interpretation. |
| [`review/source-semantic-review.md`](https://github.com/taco-jpg/p196-algorithm/blob/a883847381cd800b13e511d8ccc8909ba998866c/proofs/contributions/agent-14/carryfree-residue-saturation-20261016/review/source-semantic-review.md) | Blob `80c8da59382f4f329e5ccad66213de8a6cdac0a9`; SHA-256 `ae40bfa8733ee0768f728d8982d27ca2a1fcc4bebeb3f98f271d9abcecc5a687`. Its reviewed Residues, Digits, and Coordinates hashes match the independently recomputed H hashes exactly. |

The review identifies its reviewer as a separately assigned nonauthor and preserves the earlier partial checkpoint when adding Coordinates coverage. Nothing in the reviewed source requires those unchanged assessments to be discarded.

Their reusable scope does **not** include final Saturation acceptance or independent execution. The report explicitly leaves both pending. This preflight supplies an additional bounded reading of Saturation; it does not alter the published review record or complete the delivery gates.

## 5. Remaining blockers and exact next action

**Source blocker:** none found at H.

**Final acceptance blocker at H:** the required final nonauthor Saturation evidence and independent strict execution/audit evidence are not published in that 18-file checkpoint. `SOURCE_FREEZE.independent_status` is `NOT_YET_RUN`, and the other checkpoint documents agree that those gates remain pending. No PASS should be inferred from the author’s announcement.

The newly observed head `1dafcf7c90f9b51a0de0781998b258b96edeb191` must be assessed separately:

1. **Compare H with that exact new head.** Recheck all five module Git blobs and SHA-256 values, direct imports, registry, CONTRACT, and SOURCE_FREEZE. If the source/contract/closure identities remain unchanged, this source preflight and the existing matching nonauthor source reviews remain reusable for their stated scopes.
2. **Read the newly published material and any changed records.** The metadata count rose from 18 to 28 changed files; this report has not established the contents or identities of that later delta. Confirm actual final Saturation review coverage and exact-source independent canonical/fresh-build evidence rather than relying on PR-body announcements.
3. **Check evidence coverage and provenance.** Require the specified Lean 4.19.0 strict settings, all five mapped sources, exact source and runtime identities, preserved commands/logs/statuses, allowed-axiom results, and complete origin/public/safe-definition audit coverage. The 22 registry endpoints alone do not establish that all new declarations and imported origins were audited.
4. **Refresh ownership and target state separately.** Agent #14/session `d43e317f00d9` retains final-evidence publication ownership under the supplied coordination snapshot. This preflight creates no delivery, review, or main-slot claim. The parent should refresh issue #61 and the relevant target state before any subsequent delivery action.

The last connector response also reported `mergeable=false` for the later head while retaining Draft status. I did not investigate that changing integration field; it is not evidence of a mathematical defect in H and is not target verification.

**Recommended next action:** retain the no-defect source assessment for H, preserve the unchanged earlier nonauthor evidence, and perform a bounded review of the new evidence commit with exact byte comparisons before considering any final acceptance step.


---

# Dated addendum: exact H1 source reuse and completed semantic evidence

Recorded at **2026-10-17 00:01:01 UTC** by Agent #28 / `/root/pr149_preflight`, session `72ab3fa8c99b`.

This is a later, narrowly assigned addendum to the original report above. The original report remains an assessment of **H = `a883847381cd800b13e511d8ccc8909ba998866c`** and preserves what had and had not been published at that checkpoint. It is not rewritten as though it originally covered **H1 = `1dafcf7c90f9b51a0de0781998b258b96edeb191`**.

## Decision

**PASS_EXACT_SOURCE_REUSE.** All five registered Lean source files, their Git blobs, their complete UTF-8 contents, their SHA-256 identities, their actual direct imports, the scoped registry, CONTRACT, and SOURCE_FREEZE are unchanged between H and H1. The no-defect mathematical source assessment above therefore applies to the exact mathematical source at H1 without a source rereview or build.

The final published semantic report at H1 now supplies the previously missing nonauthor Saturation assessment. Its complete new extension was read. It explicitly passes all four new modules and all 22 selected endpoints for the selected carryfree scope, with no requested source correction. The prior report's statements about missing final semantic evidence are historically correct for H; this addendum records that the semantic evidence is now present at H1.

**No execution acceptance or integration decision is made here.** Independent execution evidence is assigned to another specialist. No Lean build, canonical-verifier execution, full independent execution archive inspection, source edit, or remote mutation was performed in this follow-up.

## Exact unchanged material

The five module Git blobs and SHA-256 values are exactly those in section 1 of the preserved report. H1 source text was fetched independently by exact commit and compared in full with the previously fetched H text. Actual imports were parsed from both versions and match the registered closure:

| Module | Direct imports at both H and H1 |
|---|---|
| `LychrelDigitSums` | `Std` |
| `Agent14CarryfreeResidues` | `Std` |
| `Agent14CarryfreeDigits` | `LychrelDigitSums` |
| `Agent14CarryfreeCoordinates` | `Agent14CarryfreeDigits` |
| `Agent14CarryfreeSaturation` | `Agent14CarryfreeResidues`, `Agent14CarryfreeDigits`, `Agent14CarryfreeCoordinates` |

The SHA-256 values were independently recomputed during the H review. Complete UTF-8 content equality and matching Git blob identities at H1 preserve those exact digests; this is not an inference from filenames or an author's assertion.

The three requested non-source comparisons also pass complete content and Git-blob equality:

| File | Unchanged Git blob | Unchanged SHA-256 |
|---|---|---|
| `proofs/Agent14Carryfree.registry.json` | `cf974d5d91fb0256cc99107e2a50f80e339d50e2` | `0a8454b8dbcf7ece3c117a3bcb2f7d3cffbf562f7decdefafbb4e72fc842f53c` |
| `CONTRACT.md` | `e8126024b452f452ba58f172d3ecfc76a74e5dac` | `ac077f99d5c5bbf49e5e5ef8801872178f3082888f03d417279b45a280c01feb` |
| `SOURCE_FREEZE.json` | `de4538f4bec15e6bf97d2186e2c3c46f2314fa7b` | `5f8a120d796e8c765830f31e52939035708c95266ca1574c26cbafec4c7f3f32` |

CONTRACT and SOURCE_FREEZE are under `proofs/contributions/agent-14/carryfree-residue-saturation-20261016/`. The unchanged `SOURCE_FREEZE.independent_status = NOT_YET_RUN` remains the historical source checkpoint's status. This addendum does not reinterpret it as a final execution result.

## Final semantic report delta and preservation

[The exact H1 source-semantic review](https://github.com/taco-jpg/p196-algorithm/blob/1dafcf7c90f9b51a0de0781998b258b96edeb191/proofs/contributions/agent-14/carryfree-residue-saturation-20261016/review/source-semantic-review.md) has:

- Git blob: `2379beba424d08e7c1007ad5c53c14c80b5750ab`.
- SHA-256: `0e71e45559d9414ce2f1ad0b04719567f61ead23d46678f706b4498eddc1eeb7`.
- Decision: `PASS_SEMANTIC_REVIEW_COMPLETE_SCOPED_CLAIM`.
- A final extension beginning at line 177, entitled “Saturation and the complete selected registry.”

The current-status paragraph is updated. From “Initial decision and exact partial review set” through the end of the earlier Coordinates extension, the earlier report body is exactly preserved after removing trailing whitespace for comparison. The new final extension is appended after that preserved body. The former two-module and three-module review stages remain explicitly dated by their sequence and limited original coverage; they have not been rewritten into earlier complete acceptance.

The new extension explicitly records a complete read of Saturation's two definitions, thirteen theorem statements, and all proof bodies. It covers the parameter split including u=10; the same seed across all physical conclusions; exact integer halves; signed modulo-11 correspondence; the fixed-width odd/even endpoints; L=5 central coincidence; L=2; both zero classes; the negative control; all 22 registry names; and all 55 explicit public declarations across the four new modules. The listed five-source, contract, registry and SOURCE_FREEZE identities agree with this comparison.

Its source conclusion is consistent with the earlier preflight. No source-level defect or scope enlargement was found in that extension. It expressly keeps kernel execution, origin/axiom audits, publication, and integration separate.

## Reviewer independence and attribution

The semantic report retains the explicit attribution to **Agent #14 / `spectral_semantics`**, independently assigned and a nonauthor of every proof source under review. It states that this reviewer authored or modified no Lean source.

This is consistent with the unchanged registry's explicit source attribution:

- Residues and Coordinates: Agent 14 `/root/coverage`.
- Digits and Saturation: Agent 14 `/root`.
- Semantic reviewer: Agent 14 `/root/spectral_semantics`.

[Published COMMENT 5554881453](https://github.com/taco-jpg/p196-algorithm/pull/149#pullrequestreview-5554881453), created at 2026-10-16 23:55:36 UTC, was also read. It explicitly says that the submitting parent authored Digits and Saturation, Coverage authored Residues and Coordinates, and that the COMMENT relays the separately assigned nonauthor `/root/spectral_semantics` and `/root/runtime` specialists. It expressly disclaims treating the submitting parent's shared-account relay as separate-account independent self-approval.

Accordingly, the documented independence is a distinct nonauthor-agent assignment with matching authorship records, not an inference that the GitHub login belongs to a different person. No authorship-role contradiction was found in the inspected records. The execution assertions in that COMMENT were read as reported assertions only; the other specialist must assess their primary evidence.

## Provenance limitation retained by the semantic reviewer

The final semantic extension preserves the author attempt-004 receipt and explains its broad auxiliary-directory inventory, including an earlier same-module object. It distinguishes that inventory from the actual final target's direct imports and from a fresh independent build. The exact final source has no self-import. This is recorded as a historical receipt precision limitation, not a source-semantic defect. This follow-up did not inspect the independent archive or retry any mathematical gate.

## Exact next action and authority boundary

The source-reuse check and final semantic-evidence check are complete for H1. The parent may reuse the preserved H source assessment together with this dated addendum and the exact H1 nonauthor semantic report. No further source correction or repeated Lean build is requested by this task.

The separate execution specialist must finish the assigned primary-evidence assessment. Delivery coordination, any current-main check, ownership refresh, publication, and integration remain the parent's separate responsibilities under issue #61. This report grants or claims none of those roles and does not infer them from readiness, a comment, or the absence of a previous delivery owner.
