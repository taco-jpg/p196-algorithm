# Next exact spectral follow-on: read-only coverage scout

Repository: taco-jpg/p196-algorithm. Session: 43cf6e114472. Scout: Agent 15 / next_claim_scout.
Original source pin: 5ff4f607535587d572fbc9e95ba9501d1fbe5fc5.
Status: proposal only. No new claim, theorem implementation, Lean execution, remote mutation, or acceptance decision was made by this scout.

## Recommendation

Claim the **actual outgoing-carry and neutral-nine support bridge** next, after refreshing the task directory and obtaining the normal protected claim. It is the smallest useful completion of the original source's mathematical assertion that is independent of Agent 14's developing H/T/R consumers. The proposed main endpoint is an exact equivalence:

    actualCharge(q,L) != 0
      iff there exists i < L with
        q(i) = 9 and carry(q,i+1) != carry(q,L-i).

Here q is any symmetric natural coefficient word bounded by 18 on its represented width, and actualCharge evaluates the already defined original U/S charge on the complete actually computed outgoing-carry list. This is a combined consequence of two literal source claims: charge vanishes exactly on symmetric carries, and carry asymmetry is supported at coefficient 9. It does not assert that the mere presence of a 9 makes the charge nonzero.

The four parity/overflow evolution laws are the next substantial central mechanism. Charge reflection alone should be a supporting lemma, not a separate task: the current halfCharge definition makes sign reversal almost immediate, while the original H reflection additionally needs H to be defined.

## Current ownership evidence and limits

The first fresh coordination read was p196/coordination at 8dbd35b190deefe66436f4cf5a6c92867c9ce35c, with 173 task records. Exact SHA comparison against the preserved 168-record map at 16642c928430f3531d401584b0ab28b3e241a5b9 found nine added/changed task versions; all nine were read. A second fresh read at 68affcc3dd7972d02f036aac5d9eb4f5ba163c14 had 174 records and three further task versions; all three were read. Their complete bodies and directory identities are retained in evidence.json.

At the second snapshot:

- Agent 15 still owns only the original U/S and binary full-word zero-charge task, blob 70340af5e48d1c965d012180c04bc6ea01f90b21.
- Agent 14's T/R coordinate-injectivity task is VERIFYING, blob 3154fcf1ea254ed1bb2acb445e61d76f59d563d2. Its reported source commit is 1418f5c176582435d6aa824da72513117da2832b, PR 144. This scout inspected source; it did not independently reproduce those verification claims.
- Agent 14 now has a separate CLAIMED carryfree-residue-saturation task, blob 8912d279695f7f298e0b1bcde5e612660e13ae5f. That exact scope includes the original Theorem 3 witnesses and their physical residue-coordinate bridges. It is excluded here.
- No inspected new/changed task reserves the three proposed endpoints below. This is not a new exhaustive proof of vacancy across all historical branches. The original 162-task semantic census is inherited evidence; the present scout independently read its targeted relevant records and all twelve current delta versions.

Issue 61 pages 5 and 6 were read directly. Page 6 was refreshed through comment 6226428852; spectral messages include 6226157675, 6226185223, 6226203256, 6226268078, 6226311107, 6226350049, and 6226399489. In particular, 6226399489 announces Agent 14's subsequent saturation proposal, which is now a protected task at the second snapshot. All future action still needs a fresh coordination check because the branch is changing rapidly. No GitHub Discussions were accessed.

## Exact source anchors

All original paths below are at the source pin above.

| Source | Git blob | Relevant location |
| --- | --- | --- |
| proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/creative_global_spectral_notes.md | cb1c355fa05916a770816a4d5ef680e54079cccb | Lines 6–21 actual carry/next-pair equations; 27–33 T/R coordinate; 40–52 H/J and four laws; 58–66 support at 9 and zero charge; 76–86 palindrome targets. |
| proofs/creative_global_spectral__8de5a77a944d0d04.py | 730acd722bf017b6bf1e51e5a0411169a7804da4 | qstep lines 8–13; coordinate 20–26; carry_coordinates 28–38; predicted 40–44; exact support assertions 51–53. An identical archived source copy is preserved locally. |
| proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/astra_spectral_carry_quotient.md | eac5b8f61385a615d9cc3e7796a4d698c66b716b | Carry-defect formulas and universal quotient; final section explicitly preserves the missing actual-orbit persistence obligation. Carryfree saturation is now Agent 14's scope. |
| proofs/RawSymmetryObstruction__5c1be305a04af2b7.lean | 9d4250f3e5daa5ff26f097a7e12ce98830dd9e89 | Existing nonnine_binary_div and resetOut_eq_actual_of_nonnine; never reprove the local division fact. |
| proofs/IncomingCarrySensitivity__5d4952e23e746f6d.lean | 9ccc745471fd509fb68652fef40454478087e92e | Existing carryWith_zero, carry_difference, carry_difference_bit, actual_carry_shift, actual_block_carry_defect; prefix-nine sensitivity already belongs to the original source. |
| proofs/SeamCoefficients__e73d67d37698e702.lean | b4200954f47c13d30890673ecab7092578537fe5 | actualCoeff_eq_raw, lines 56 onward: complete E=Q+(x-10)C, including terminal carry and zero tail. |
| proofs/PairResponse__18d2d58355ed97f4.lean | b7e822e798d873e9b51f7e97eb9c4c78821bd1c2 | nextColumns_actualCoeff at 14; numeric_pair_response at 47. |
| proofs/Lychrel196Research__c696e0ea3db39d92.lean | c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506 | carry 517; carry_bounded 545; step_palindrome_iff_no_overflow 797; step_palindrome_iff_overflow 851; Canonical 898; next_column_no_overflow 1183; next_column_overflow_outer 1197; next_column_overflow_interior 1211; nextWidth 1506; representation_next 1559. |

FINDINGS.md labels the spectral work as lossless coordinate identities and exclusions of selected residue simplifications, with no persistent nonzero invariant found. The historical script's finite tests are implementation evidence, not a substitute for any proposed universal theorem.

## Ranked candidate 1 — Actual carry charge and neutral-nine support

**Readiness:** highest. **Difficulty estimate:** low to medium; principally a finite-list/function bridge plus reuse of the existing local arithmetic theorem. Rough authoring size: one new module, approximately 100–250 lines; not an execution promise.

Let q : Nat -> Nat and L : Nat satisfy

    hb : forall i < L, q(i) <= 18
    hs : forall i < L, q(i) = q(L-1-i).

Use the existing DecimalDigits.carry, whose argument is an INCOMING boundary index:

    carry(q,0) = 0
    carry(q,i+1) = (q(i) + carry(q,i))/10.

Define only the finite adapter and charge consumer:

    outgoing(q,L) = map (fun i => carry(q,i+1)) (List.range L)
    actualCharge(q,L) = P196.Agent15.SpectralCarry.carryCharge(outgoing(q,L)).

Proposed complete contract:

1. outgoing(q,L) has length L, has the stated entries, and is Binary under hb.
2. Under hb alone, actualCharge(q,L)=0 iff forall i<L, carry(q,i+1)=carry(q,L-i).
3. Under hb and hs, q(i)!=9 implies carry(q,i+1)=carry(q,L-i) for every i<L.
4. Under hb and hs, actualCharge(q,L)!=0 iff exists i<L with q(i)=9 and carry(q,i+1)!=carry(q,L-i).
5. Corollary: absence of 9 on the whole width implies actualCharge(q,L)=0.
6. Canonical specialization takes DecimalDigits.Canonical n d L and q=columnSum d L. It invokes existing columnSum_bounded and columnSum_symmetric; it must not introduce an assumed carry sequence.

**Existing exact APIs.** RawSymmetryObstruction.nonnine_binary_div takes a,b,c : Nat, a<=18, a!=9, b<=1, c<=1, and proves (a+b)/10=(a+c)/10. DecimalDigits.carry_bounded supplies both incoming bits. Current ChargeSymmetry.lean exports carryCharge_zero_iff {cs : List Nat} (hc : Binary cs) : carryCharge cs = 0 <-> cs.reverse = cs. SourceFormula.lean exports both carryCharge_eq_odd_source_sum and carryCharge_eq_even_source_sum.

**Exact remaining proof.** Set j=L-1-i, rewrite q(j)=q(i), and instantiate the existing local division lemma on carry(q,i) and carry(q,j). The two outputs are carry(q,i+1) and carry(q,L-i). Then identify List.reverse on the complete outgoing list with that same reflected index. Apply the already proved binary charge zero-set theorem; combine its contrapositive with the support result to obtain the displayed nonzero equivalence. No new weighted uniqueness or local decimal-division proof is needed.

**Boundaries.** Widths zero and one remain valid algebraic extensions. The word includes carry(q,L), the possible final overflow carry. Do not append carry(q,0)=0. Positivity of q(0), odd central parity, absence of overflow, and absence of 9 are not hypotheses of the general support theorem. J=0 iff no 9 is false and must not replace this contract.

**Dependency estimate.** Three original arithmetic modules (LychrelDigitSums, IncomingCarrySensitivity, RawSymmetryObstruction), the current three or four Agent 15 modules, and one new adapter: about seven or eight modules depending on the chosen source-formula import. Full closure must be resolved and audited; no new clean build occurred in this scout.

## Ranked candidate 2 — The complete four-case actual integer evolution law

**Readiness:** mathematically well specified, but consumes a frozen Agent 14 T/R coordinate interface and requires the original H definition. **Difficulty estimate:** medium to high; two or three new modules with integer recurrence cross-identities and finite telescoping. Rough authoring size 400–900 lines; the main risk is parity/index bookkeeping and Nat/Int compatibility.

For every bounded symmetric q at width L, define c=outgoing(q,L), h=carry(q,L), q'=FoldedDecimal.nextColumns q L, and L'=FoldedDecimal.nextWidth q L. Let

    A = (Agent14.Spectral.coordinate q L : Int)
    A' = (Agent14.Spectral.coordinate q' L' : Int).

Retain the literal original H:

    L=2m+1:
      H=c(m)+sum_(i<m)(c(i)+c(2m-i)) * (T(m-i)/2).
    L=2m:
      H=sum_(i<m)(c(i)+c(2m-1-i)) * R(m-1-i).

All arithmetic in the endpoint is integer arithmetic, with exact casts of Agent 14's natural weights. J is the existing original carryCharge, not a new right-hand-side definition.

| Current width | Actual h | Required equation |
| --- | --- | --- |
| odd | 0 | A' = 2*A + 198*J |
| odd | 1 | A' = A - 9*H + 99*J |
| even | 0 | A' = 2*A + 9*J |
| even | 1 | A' = 22*A - 99*H + 99*J |

A canonical ordinary-input corollary uses representation_next (or numeric_pair_response) to identify q' and L' with the true next integer. No next-coordinate identity may be assumed as a premise.

**Read existing interfaces.** Agent14.Spectral.coordinate : (Nat -> Nat) -> Nat -> Nat selects evenCoordinate/oddCoordinate. evenCoordinate q m is prefixSum (fun i => q i * R(m-1-i)) m; oddCoordinate q m is q m + prefixSum (fun i => q i * T(m-i)) m. Agent14.Spectral.T_recurrence_exact and R_recurrence_exact prove the addition-form recurrence without natural truncation. The inspected retained attempt-002 sources have blobs 6e37b9eb5d532c7c32559223a8672ba589488f7b and 929d6edd72185f4f5ed9c84e7540fe89c8372cbd, respectively, and are part of source commit 1418f5c176582435d6aa824da72513117da2832b. Expected exported module paths are proofs/Agent14SpectralInjectivity.lean and proofs/Agent14SpectralWeights.lean.

**Exact missing arithmetic.** Prove, from the already defined recurrences, the integer cross-identities

    R(k) = U(k+1)-U(k)
    S(k) = U(k+1)+U(k)
    T(k) = 2*(U(k+1)-10*U(k)).

These also justify exact division T/2. They are proposed sublemmas, not preexisting checked results. Introduce H through the literal source sum and prove its reflection symmetry. Evaluate the existing coefficient/pairing equations by the source weights, telescope the shifted carry terms, and handle the changed center and terminal term in each overflow parity. Reuse Agent107.SeamCoefficients.actualCoeff_eq_raw and Agent107.PairResponse.nextColumns_actualCoeff; alternatively consume the three already proved FoldedDecimal.next_column_* equations. Do not duplicate their E or q' normalization theorems.

**Reflection caveat.** The source reverses an existing carry word: J(reverse c)=-J(c) and H(reverse c)=H(c). It does not recompute carries after reversing q. Because q is symmetric, recomputing carries from reversed q usually returns c itself; confusing these operations would create a false claim.

No beta/square-root embedding is necessary to prove these exact integer identities. That embedding remains a separate original claim. The four-case law does not provide a closed recurrence on A,H,J alone and does not establish charge persistence.

## Ranked candidate 3 — Exact spectral one-step palindrome targets

**Readiness:** after H and a frozen general Agent 14 injectivity interface. It does not logically require the four-case evolution theorem. **Difficulty estimate:** medium; finite H positivity and scaling plus reuse of original decimal criteria. Rough authoring size 200–450 lines.

For DecimalDigits.Canonical n d L, set q=columnSum d L, c=outgoing(q,L), A=coordinate(q,L), H and J to their literal source formulas, and h=carry(q,L). Prove the original endpoints exactly:

    h=0:
      Palindrome(step n) iff (H=0 and J=0).
    h=1 and L odd:
      Palindrome(step n) iff (J=0 and A=11*H).
    h=1 and L even:
      Palindrome(step n) iff (J=0 and 2*A=11*H).

**Existing exact APIs.** DecimalDigits.step_palindrome_iff_no_overflow identifies the no-overflow class as forall i<L, q(i)<=9. DecimalDigits.step_palindrome_iff_overflow identifies the overflow class as q(0)=11 and all q(i) in {0,11}. Agent14.Spectral.coordinate_injective accepts any two bounded symmetric words in 0..18 at a fixed width, without requiring even central parity. Agent 15's carryCharge_zero_iff supplies carry symmetry.

**Exact remaining proof.** Show H=0 iff every outgoing carry is zero. Under J=0, show H=A(c) in odd width and H=2*A(c) in even width, using exact evenness of T. Prove finite coordinate scaling; turn each displayed equality into A(q)=A(11*c). Apply Agent 14's bounded symmetric injectivity, whose domain includes 11*c even when its central entry is 11. Use h=1 and carry symmetry to obtain q(0)=11. The converse uses the existing 0/11 criterion and computed carry recurrence. Preserve the true Canonical numeral bridge and the exact current-width flag.

This completes a coordinate reformulation of the existing one-step target; it does not prove that an orbit avoids that target.

## Exclusions and evidence quality

Do not claim the already owned T/R injectivity, carryfree saturation, local non-nine division, incoming-carry response, or E/next-pair coefficient identities. Do not reuse a historical no-Lean label as current ownership evidence. Do not count reflection alone as the next substantive completion. The quotient ideal, 1782-element ring isomorphism, overflow saturation, and an actual-orbit nonzero invariant remain outside these proposed packages.

The report is source-level scoping only. It contains no theorem implementation, proof build, axiom audit, numerical experiment, or new assertion of formal acceptance. A final implementation must preserve the selected contract, original attribution, all source and failure history, and the existing strict fresh-build and genuine nonauthor review gates.

## Read failures and preservation

1. An initial guessed refs/heads/coordination read returned GitHub 404; the correct existing branch was then read as refs/heads/p196/coordination.
2. A local inventory request named nonexistent repo/coordination and returned rg exit 2; the actual coordination files were obtained through the branch API.
3. Some overly broad rg/source batches were output-truncated. The necessary source sections and current scope records were then read separately. These truncations are not treated as complete semantic reads.
4. One later local source read failed before execution with: CreateProcess: Rejected("Failed to create unified exec process: exec-server transport disconnected"). The same pinned source section was read through the approved GitHub read connector. No denial was bypassed and no mathematical execution occurred.

Existing original source bytes remain at /workspace/scratch/43cf6e114472/scout/source/. This scout's only requested outputs are this report and evidence.json in its isolated /dev/shm report directory, for parent publication through the already authorized channel.

## Immediate implementation handoff clarification

The actual existing arithmetic import closure for candidate 1 is exactly:

    LychrelDigitSums.lean
      -> IncomingCarrySensitivity.lean
        -> RawSymmetryObstruction.lean

The selected flattened foundation is proofs/LychrelDigitSums__0810ace083af80c5.lean, Git blob 8a865176625283648a8a20dd2411ed77670eb0a2, SHA-256 ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57, 218799 bytes. It imports Std. Its copies of DecimalDigits.carry, carry_bounded, columnSum_bounded, columnSum_symmetric and Canonical are the arithmetic interfaces to import. The separate Lychrel196Research source anchor above records original provenance, not a request to introduce another foundational module.

The Agent 15 side imports the existing SpectralWeights -> BinaryCode -> ChargeSymmetry -> SourceFormula chain. A single new module may import SourceFormula and RawSymmetryObstruction; there is no need to create a parallel carry recurrence, normalize implementation, or general-base layer. Its finite outgoing list is solely an adapter over DecimalDigits.carry.

Parent checkpoint received during this scout: PR 145 at e8d706dc8a67248e1531b0b828fbe05ff50052ed is published; parent reports a fresh five-module/69-export author PASS and two genuine nonauthor reviews active. These are attributed parent statements, not this scout's execution. Candidate 1 is outside the existing protected U/S scope and still requires a separate fresh claim before implementation.
