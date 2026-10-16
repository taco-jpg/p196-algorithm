# Agent 14 / coverage: exact-claim shortlist

## Scope and evidence status

This is a read-only claim scout, not a proof, build, independent mathematical review, or ownership claim. No Lean compiler was invoked and no repository source was changed. The parent owns all Git publication and issue 61 relays.

- Current source snapshot inspected: `main` at `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`.
- Historical source map base: `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.
- Ownership snapshot supplied by parent: 162 records at coordination commit `b0ee3d25fb1ddea0f741326b6401d81ae3d27626`, under `/workspace/scratch/d43e317f00d9/agent14-state`.
- GitHub issue 61 fetched through the supported all-pages tool. First result: 477 comments, last `6226122766`. Boundary refresh: 485 comments, last `6226157675`. Relevant recent comments and lexical matches were inspected; this does not claim a semantic audit of every historical conversation.
- Open pull request search returned 46 PRs, numbers 99 through 142 with gaps, before the later PR143 announcement. Their titles and relevant bodies were inspected. No spectral counterpart appeared in that result or in the refreshed issue messages. Parent must refresh ownership and PR deltas before any new reservation.
- Corpus actually searched: current `proofs/FINDINGS.md`, `REPORTS.md`, the reorganization-only `RESULTS.md`, source-map entries, selected archived original reports, current Lean files, and targeted all-archive Lean searches. This is deliberately a scoped census, not repository-wide exhaustive completion.

All eight entries below are original, precisely scoped mathematical claims or independently stated parts of original claims. The selected integer-coordinate injectivity does not close the real spectral interpretation, dynamical laws, quotient theorems, or any infinite-orbit target.

## Source references

All original paths below are relative to the repository at historical commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. Their preserved copies are under `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/` followed by the original path.

| Key | Original path | Git blob | SHA-256 |
|---|---|---|---|
| SPECTRAL | `proofs/research/creative_global_spectral_notes.md` | `cb1c355fa05916a770816a4d5ef680e54079cccb` | `e4a1e6b61848f473693c36d91d2a453b1dc82b26a347fa76b2a0b9a7e1228e27` |
| SPECTRAL-CODE | `proofs/research/creative_global_spectral.py` | `730acd722bf017b6bf1e51e5a0411169a7804da4` | `393545516c13d41c0416e560ec37bab6b1c1655357ae351b0f960dea76ff7448` |
| QUOTIENT | `proofs/research/astra_spectral_carry_quotient.md` | `eac5b8f61385a615d9cc3e7796a4d698c66b716b` | `d39212c9ab98f4c5b0fccb733d3b662e41a09804878178c82b8762684e97fb09` |
| STRENGTHENING | `proofs/research/continuation/strengthening_notes.txt` | `7103ee939d82740b970dd23fb91e9db50db4ea54` | `15e07772d87cc4ee469541f4fb39ce1d0dce28ac5f630b16980c8abb02db258f` |

The spectral code's current mapped path is `proofs/creative_global_spectral__8de5a77a944d0d04.py`. Source-map hashes are provenance evidence; this scout did not rerun the original numerical controls.

## Prioritized queue

| Claim ID | Exact target | Coverage disposition | Relative size / next action |
|---|---|---|---|
| SC14-SPECTRAL-INJECTIVE | Fixed-length reciprocal coefficient words are determined by their integer coordinate, for both parities. | UNFORMALIZED; parent has proposed this scope in issue comment `6226157675`. | Small–medium; prove recurrence domination and bounded weighted-sum injectivity. |
| SC14-SPECTRAL-CARRY-ZERO | The integer antisymmetric carry coordinate vanishes iff the complete outgoing carry word is symmetric. | PARTIALLY_FORMALIZED: local carry-reset facts exist; the coordinate theorem does not. | Small–medium; two more recurrence weight families and signed uniqueness. |
| SC14-SPECTRAL-EVOLUTION | The four exact integer-coordinate update laws hold for every canonical decimal input. | PARTIALLY_FORMALIZED: exact column/width arithmetic exists, but not its weighted transformation. | Medium; finite weighted sums of existing column identities. |
| SC14-SPECTRAL-PALINDROME | Exact coordinate criteria for whether the next actual integer is a palindrome. | PARTIALLY_FORMALIZED: digit/carry criterion exists; spectral equivalences do not. | Medium after injectivity and carry-coordinate lemmas. |
| SC14-CARRYFREE-CLASS-SATURATION | Every allowed fixed-length quotient class has a carry-free, nonpalindromic ordinary integer representative whose next iterate is a palindrome. | UNFORMALIZED at the exact short thresholds; related residue-palindrome theorems have different endpoints. | Medium, with a particularly short odd-width construction. |
| SC14-OVERFLOW-CLASS-SATURATION | Every surviving class also has such a representative with actual overflow at even lengths at least 18 and odd lengths at least 19. | PARTIALLY_FORMALIZED: the generic 0/11 palindrome criterion exists; the full quantified construction does not. | Medium; choose 1–9 symmetric 11-pairs and supply digit realizations. |
| SC14-CARRY-DEFECT-IDEAL | All actual carry defects generate exactly `(x^2-20x+1,9(x+1))`, even restricting to nonpalindromic inputs. | UNFORMALIZED. | Larger; begin with exact defect identities and three actual input witnesses. |
| SC14-ESCAPE-LOWER-DENSITY | Digit-sum excursions have lower asymptotic and lower Banach density at least `1/(F(B)+1)`. | PARTIALLY_FORMALIZED via Ready PR99's full finite interval count. | Medium if a compatible real-analysis environment is available; do not duplicate PR99. |

## 1. SC14-SPECTRAL-INJECTIVE

**Original source.** SPECTRAL, lines 23–38. For the fixed-length reciprocal word `q`, the integer coordinate is

`A(q,2m+1) = q_m + sum_(i<m) q_i T_(m-i)` and
`A(q,2m) = sum_(i<m) q_i R_(m-1-i)`,

where `T_0=2`, `T_1=20`, `R_0=1`, `R_1=19`, and each sequence satisfies `u_(k+2)=20*u_(k+1)-u_k`. Distinct reciprocal words of the same length, with coefficients in `0..18`, have distinct coordinates. The source supplies the strict weight-domination argument.

**Meaningful hypotheses.** Fix the same finite width for both words. Require coefficient bounds and reflection symmetry on that width. Do not require equality outside the finite width. The general lemma should not require positive outer coefficient or even center; the physical corollary may add those hypotheses. This distinction matters later when comparing `q` with `11*C`: the center of `11*C` can be odd, although it is bounded and reciprocal. Width one and the empty even half are explicit boundary cases; width zero is an optional documented extension.

**Existing coverage.** `SignedDigitUniqueness.all_zero_of_eval_zero_open` proves Horner positional uniqueness in a fixed integer base, not this second-order recurrence. `DifferenceObservability.smooth_five_rigidity` concerns iterated binomial smoothing, not weighted coordinates. Current `DecimalDigits.value_injective` is decimal positional uniqueness. None closes this target.

**Minimal dependencies / next step.** `Std`, finite Nat/Int sums and inequalities. Prove strict domination for weights `1,T_1,T_2,...` and separately `R_0,R_1,...`, then compare the largest differing half-coordinate. Preserve the exact recurrence if using natural subtraction by proving that subtraction does not truncate. A purely integer proof avoids adding a real square-root interpretation as an assumption.

## 2. SC14-SPECTRAL-CARRY-ZERO

**Original source.** SPECTRAL, lines 40–66; exact executable definitions in SPECTRAL-CODE `carry_coordinates`.

Let `c_i` be the outgoing carry bits of the actual normalization, or more generally any finite word in `{0,1}`. For odd `L=2m+1`, define `U_0=0,U_1=1` with the same recurrence and
`J = sum_(i<m) (c_(L-1-i)-c_i) U_(m-i)`.
For even `L=2m`, define `S_0=1,S_1=21` with the same recurrence and
`J = sum_(i<m) (c_(L-1-i)-c_i) S_(m-1-i)`.
Then `J=0` iff `c_i=c_(L-1-i)` for every valid index. The odd center is automatically symmetric and contributes no antisymmetric term.

**Existing coverage.** `CarryTransferNormalForm.carry_after_reset`, `IncomingCarrySensitivity.nonnine_carry_coalesces`, and `RawSymmetryObstruction.nonnine_binary_div` supply reset arithmetic. `resetOut_eq_actual_of_nonnine` compares seam-reset carries with actual carries. None defines this `J` or proves its zero set. Those existing results can justify the additional actual-decimal consequence that carry asymmetry is supported only at `q_i=9`; the useful new endpoint is still the exact `J` equivalence.

**Minimal dependencies / next step.** Reuse the selected generic weight-domination framework, instantiate `U_1,U_2,...` and `S_0,S_1,...`, and prove uniqueness with coefficient differences in `{-1,0,1}`. No real numbers are needed. Retain outgoing-carry indexing: the repository's `DecimalDigits.carry q (i+1)` corresponds to source `c_i`.

## 3. SC14-SPECTRAL-EVOLUTION

**Original source.** SPECTRAL, lines 40–55. With exact `A,H,J` from SPECTRAL-CODE and actual terminal carry `h`, the next canonical pair word satisfies

| Input parity | Overflow | Exact equation |
|---|---:|---|
| Odd | 0 | `A' = 2*A + 198*J` |
| Odd | 1 | `A' = A - 9*H + 99*J` |
| Even | 0 | `A' = 2*A + 9*J` |
| Even | 1 | `A' = 22*A - 99*H + 99*J` |

For odd length, `H=c_m+sum_(i<m)(c_i+c_(L-1-i))*(T_(m-i)/2)`; for even length, `H=sum_(i<m)(c_i+c_(L-1-i))*R_(m-1-i)`. The division by two is exact because every `T_k` is even.

**Existing coverage.** `FoldedDecimal.next_column_no_overflow`, `next_column_overflow_outer`, `next_column_overflow_interior`, `canonical_next_no_overflow`, `canonical_next_overflow`, and `representation_next` already cover the actual arithmetic and changed output width. They do not sum against these weights. The new proof should consume those theorems rather than posit abstract update equations or future canonicality.

**Minimal dependencies / next step.** Exact integer recurrences, finite reflection/reindexing, evenness of `T`, and the existing decimal core. Prove the weighted finite-sum identities in both width branches, then specialize them to every canonical integer input. Include `L=1`, both possible actual overflows, and the new leading output digit. No real-beta identity is required for the integer recurrence target, but it remains a separate original claim.

## 4. SC14-SPECTRAL-PALINDROME

**Original source.** SPECTRAL, lines 76–86. For every positive canonical decimal input:

- If `h=0`, the next integer is a palindrome iff `H=0` and `J=0`.
- If `h=1` and `L` is odd, it is a palindrome iff `J=0` and `A=11*H`.
- If `h=1` and `L` is even, it is a palindrome iff `J=0` and `2*A=11*H`.

**Existing coverage.** `DecimalDigits.step_palindrome_iff_no_overflow`, `step_palindrome_iff_overflow`, and `step_palindrome_iff` already give exact ordinary-integer carry/pair-sum conditions. They do not give the spectral conditions. This is a reformulation of an existing mathematical criterion, so mathematical discovery must remain attributed to the original source.

**Minimal dependencies / next step.** Prove `H=J=0` iff the complete carry word is zero, and use SC14-SPECTRAL-CARRY-ZERO plus SC14-SPECTRAL-INJECTIVE to derive `q=11*c` from the relevant spectral equality. The generic injectivity theorem must allow reciprocal bounded words with odd central coefficient. Finish using the unchanged actual palindrome criterion; do not add the desired coefficient equality as a premise.

## 5. SC14-CARRYFREE-CLASS-SATURATION

**Original source.** QUOTIENT, Theorem 3, lines 137–175. At every odd width `L>=5`, all 99 pairs `(s,r)`, where `s=S(n) mod 9` and `r=n mod 11`, are realized by positive canonical nonpalindromic inputs with carry-free pair sums and a palindromic next output. At every even width `L>=2`, all nine quotient classes `s` (whose alternating component is automatically zero) are realized in the same way.

**Exact construction.** For odd `L`, choose `1<=U<=10`, `0<=B<=9`, `A=min(U,9)`, `C=U-A`, and
`n=A*10^(L-1)+B*10^(L-2)+C*10^(L-3)`.
The source's reciprocal pair word has `A` at the outer pair, `B` at the next pair, and `C` at the third pair. At `L=5`, the last two source monomials coincide and the center is `2*C`; that boundary must be proved. All pair coefficients are at most 9, the leading input digit is positive, and the units digit is zero. Also `S(n)=U+B` and `n mod 99=(U+10*B) mod 99`. The 100 choices of `(U,B)` cover integers 1 through 100 and therefore all 99 residues. For even `L`, take `n=A*10^(L-1)` with `1<=A<=9`.

**Existing coverage.** `Agent105.ResiduePalindromes.matching_even_palindrome` constructs already-palindromic integers in even-width residue classes. `ExactLengthResidues.exact_length_palindrome_residues` constructs already-palindromic representatives above an unspecified large threshold. Neither supplies nonpalindromic predecessors with actual zero final carry at these exact short thresholds. `FoldedDecimal.valid_word_realizable` supplies generic realizability but does not choose the source's nonpalindromic split.

**Minimal dependencies / next step.** Reuse `DecimalDigits.Canonical`, `digitSpike`/finite-value lemmas, `AstraModular.ten_pow_mod99`, and the carry-free palindrome criterion. Start with the explicit three-leading-digit construction and its exact width and value. Express the final result in the source's two residues, or prove its equivalence to the single modulo-99 statement; do not conflate a target palindrome's residue with the predecessor's residue.

## 6. SC14-OVERFLOW-CLASS-SATURATION

**Original source.** QUOTIENT, lines 177–195. For every even width `L>=18` and every odd width `L>=19`, every `s mod 9` admits a nonpalindromic canonical ordinary input with quotient class `(s,0)`, actual terminal carry one, and a palindromic next output.

Choose `k` in `1..9`, place 11 in exactly `k` symmetric pairs including the outer pair, and put zero elsewhere, including the center when present. Then `S(n)=11*k`; these values cover every residue modulo nine. Choose outer input digits 9 and 2, so the input is nonpalindromic. The actual carry polynomial is `C=Q/11`, and the actual output polynomial is `(1+x)*C`, which is reciprocal at the new width. For odd input width, the quotient alternating component is zero modulo eleven because every contributing pair is a multiple of eleven.

**Existing coverage.** `DecimalCarry.zero_or_eleven_digit_sums_give_palindrome` and `DecimalDigits.step_palindrome_iff_overflow` cover the generic palindrome consequence. They do not quantify and realize this complete class-saturating family or establish the claimed minimum sufficient widths. No current ownership record covers this spectral family.

**Minimal dependencies / next step.** Define an explicit selection of the first `k` mirrored positions, provide its canonical digit split, count the pair coefficients, and specialize the unchanged overflow criterion. Preserve the distinct even-18 and odd-19 thresholds. This does not require first proving the ring-quotient classification, although the coordinate-to-physical-class correspondence should be recorded.

## 7. SC14-CARRY-DEFECT-IDEAL

**Original source.** QUOTIENT, Theorem 1, lines 19–77. In `Z[x,x^-1]`, let `Delta_0=Q_new-2Q` in the actual no-overflow branch and `Delta_1=Q_new-(1+x)Q` in the actual overflow branch. The ideal generated by all such defects of positive canonical reciprocal decimal pair words equals `(p,g)`, where `p=x^2-20x+1` and `g=9(x+1)`. The equality still holds when restricting the inputs to nonpalindromic ordinary integers.

**Proof obligations.** For `T=(C-C*)/(x-1)`, establish the genuine divisibility and exact identities `Delta_0=p*(C*/x+T)+g*T` and `Delta_1=p*T+g*(T-C*)`. For the reverse inclusion, preserve the actual nonpalindromic witnesses `150`, `109`, `159`, with defects `p`, `-g*(1+x^2)`, and `-g*(1+x+x^2)`. Their difference gives `-x*g`; Laurent invertibility then recovers `g`.

**Existing coverage.** The decimal core supplies actual column normalization. The seam-polynomial `SignedDigitUniqueness` and `DifferenceObservability` results do not identify this ideal. No current or archived Lean occurrence of spectral/carry-blind terminology, no matching ideal construction, and no active task were found in the searched corpus. This is not an exhaustive semantic proof of absence in inaccessible branches.

**Minimal dependencies / next step.** A compatible polynomial/Laurent-polynomial and ideal environment, or a carefully proved equivalent universal ring-evaluation interface, plus actual-decimal normalization. This is larger than the six preceding tasks. Start with the coefficient identity and actual witness calculations; do not present a generic formal ideal calculation without the arithmetic defect bridge as the full source theorem. The separate quotient-isomorphism/1782-cardinality Theorem 2 remains unreserved and unproved by this entry.

## 8. SC14-ESCAPE-LOWER-DENSITY

**Original source.** STRENGTHENING, Section 6, lines 237–247. For every positive ordinary decimal seed `n` and integer threshold `B>=1`, the set `A_B={t>=0 : digitSum(orbit n t)>B}` has lower asymptotic density and lower Banach density at least `1/(F(B)+1)`. The latter bound is uniform over translated long intervals. Iteration continues after an earlier palindrome.

**Existing coverage.** Ready PR99, exact source `d81784d62b399775982084a54313b6df1695b2c4`, supplies `P196.Agent9.IntervalCounts.digitSum_interval_count`: every `[s,s+N)` contains at least `N/(sharpDigitSumEscapeBound B+1)` qualifying times. Its task explicitly excludes real asymptotic-density theorems. Ready PR109 separately supplies the factorial bound and should not be duplicated. The original recurrence horizon can be retained by proving it is no smaller than the available sharp horizon, or by applying the generic count theorem to the original uniform escape.

**Minimal dependencies / next step.** Fetch and pin the unchanged PR99 selected source closure, verify its exact interval convention, and derive the real inequality from `floor(N/w)>=N/w-1`. Then prove the translated uniform liminf statement, from which ordinary lower density follows by setting `s=0`. The quantifier order `forall epsilon>0, exists N0, forall s, forall N>=N0` is essential for the lower Banach assertion. Check the available real-analysis environment before selecting this task; no Mathlib availability or new build success is claimed here.

## De-duplication exclusions and ownership-sensitive legacy repair

- General-base carry-word normalization is not a fresh task. Agent421 owns the interior bounds and has checked no-overflow and overflow-clock packages; Agent422 owns width-five sharpness and the protected neutral-run rule; Agent4 has related general-base packages. The historical FINDINGS label “not formalized” is therefore stale as a blanket statement.
- The exact zero-gap/mass bound and pure-Nat quadratic running maximum are integrated in `Agent104FiniteMassBound`. They are not new candidates.
- PR99, PR109, PR123, and PR131 already cover, respectively, finite interval escape counts, the factorial horizon, the complete finite marker-complement count, and arbitrary one-step digit-sum collapse.
- The original `BoundaryCertificate`, `ArithmeticBridge`, `BulkTargets`, and `BulkDerivation` still contain actual `native_decide` proofs. The scoped arithmetic/bulk declarations include `candidates_complete_checked`, `bulk_edges_checked`, `bulk_cycles_checked`, and `derived_targets_checked`. Their original downstream endpoint therefore has a legacy trust issue.
- This legacy family is ownership-sensitive: `agent414-kernel-boundary-certificate`, `agent414-bulk-period-premise-discharge`, and `agent415-actual-inverse-column-bridge` are active. Agent414's record explicitly limits its reservation to the original graph0 equality and excludes the other 31 internal certificate-table equalities, but that does not establish a vacant full endpoint. Coordinate an exact residual table repair before implementation; do not reserve the existing all-width endpoint wholesale.
- Plain mentions of `native_decide` in `OuterEscape`, `SafeHighWitness`, `CycleConstraints`, and several audit files are comments describing its exclusion, not actual shortcut proofs. A lexical file count would overstate the trust problem.

## Recommended scheduling decision

Begin with SC14-SPECTRAL-INJECTIVE after the parent's successful guarded claim. Keep a genuine nonauthor for semantic review and fresh build verification. The most direct next ordinary-integer task is SC14-CARRYFREE-CLASS-SATURATION; the most reusable nearby dependency is SC14-SPECTRAL-CARRY-ZERO. All remaining proposals are a queue, not ownership reservations. Refresh issue 61, coordination, and relevant PRs before claiming any successor.
