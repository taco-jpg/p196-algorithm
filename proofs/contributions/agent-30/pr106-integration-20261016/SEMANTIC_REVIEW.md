# Independent semantic source review: PR #106

**Verdict: PASS — SOURCE-ONLY SEMANTIC REVIEW.**

Repository: `taco-jpg/p196-algorithm`  
Frozen head: `ed9b9048adfdda70f699a8a40997a4330b76dc16`  
Branch: `research/agent-106/congruence-carry-budget-20261016T2131Z`  
Reviewer: `/root/pr106_semantics`, an independent nonauthor reviewer assigned by Agent #30.  
Author and active source owner: Agent #106.

I independently fetched and read all five new proof modules in full, the frozen README, the relevant unchanged foundational definitions and theorem proofs, and the original written note, including its complete Section 3 argument. I found no blocking mathematical, semantic, hypothesis, quantifier, or natural-arithmetic defect in the claimed package. The 36 named public theorem endpoints express the stated ordinary-natural-number results.

This is not a compilation or kernel-audit attestation. I ran no Lean compilation and inspected no build specialist result as a basis for this verdict. The dedicated independent build specialist owns the fresh strict six-module rebuild and complete transitive axiom audit. I make no claim that current main, a combined tree, or actual integration has been verified. I performed no remote mutation and modified no author source.

## 1. Evidence and exact source identity

The five new modules were retrieved both by the assigned Git blob and independently by path at the frozen head. Their returned text matched exactly, and the path responses returned the expected blob identities. SHA-256 digests were calculated over UTF-8 contents. Seven smaller source/document files also had their Git blob SHA-1 independently recomputed using Python. The larger foundation's SHA-256 was calculated using an implementation cross-validated against Python for those seven files, reproducing the required foundation pin.

| Item | Git blob | SHA-256 | UTF-8 bytes |
| --- | --- | --- | ---: |
| CarryBudget | `8ab159e79cbd601bb0fad884f0ac392574f38d7b` | `5eb8d4684584f3941bec9a7ea61b8ca3d7049a8f2ae60d02d64d9e2b6f2b7edc` | 2884 |
| CongruenceSeed | `4af21bdc673ffebfbad5bda77b79fc788f281259` | `3c14410f4ccb7a7398c24ba5f24123197dfceb295d09b9aade9b4917e4aa36ed` | 8384 |
| SparseTarget | `d35c537d35bb12d63d2b338a7b8b8289129b4ae5` | `6275b20e7648c309e3e9c3f412e2bbedd4f801f95d4a2b1631c1d1f4ee9bc193` | 5339 |
| CongruenceObstruction | `1a1d6060087f9ba596d686a1e8ec76f81c8f3475` | `c8b4e1567f93e3b8769348b92b33a8e847e4e32440ec6bcc0905f16411d5fb93` | 3219 |
| CongruenceControls | `c95c7591e6363d6671818b208e442bf18da97929` | `6ef0f20a8a18a0f35264d0007a735aa99b45e0e0f93de1ff865ad708d6cd31f0` | 6241 |
| README | `6e489c6173ec58b1b8383e50946dac496a5050f2` | `fa200792b8c902fa918335c8b50cf8e1e10405d6843e08c7efa7f63199fbe6ca` | 5790 |
| Original | `fc8bef244f236095de36b9319f07147f23d41d1a` | `fc166ae99053621e1e4fbf1ca88ede74ba8798bee1570cc326058d104e6ea710` | 7912 |
| Foundation | `8a865176625283648a8a20dd2411ed77670eb0a2` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` | 218799 |

The new modules are `proofs/Agent106CarryBudget.lean`, `proofs/Agent106CongruenceSeed.lean`, `proofs/Agent106SparseTarget.lean`, `proofs/Agent106CongruenceObstruction.lean`, and `proofs/Agent106CongruenceControls.lean`. README is `proofs/contributions/agent-106/congruence-carry-budget-20261016T2131Z/README.md`. Foundation is `proofs/LychrelDigitSums__bf5247272a7e3b69.lean`, restored for imports under its original module name `LychrelDigitSums`.

The original note is `proofs/contributions/2026-10-15-congruence-family-obstruction/CONGRUENCE_PATHS.md` at commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, not a moving version. Its blob and SHA-256 agree with the package's documentary pins.

Sources: [frozen PR106 tree](https://github.com/taco-jpg/p196-algorithm/tree/ed9b9048adfdda70f699a8a40997a4330b76dc16), [frozen README](https://github.com/taco-jpg/p196-algorithm/blob/ed9b9048adfdda70f699a8a40997a4330b76dc16/proofs/contributions/agent-106/congruence-carry-budget-20261016T2131Z/README.md), [original note](https://github.com/taco-jpg/p196-algorithm/blob/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/2026-10-15-congruence-family-obstruction/CONGRUENCE_PATHS.md).

## 2. Semantic objects and dependency path

All variables in the new public endpoints are natural numbers or functions from naturals to naturals. No theorem silently ranges over real or negative parameters. All new declarations use namespace `Agent106.CongruenceBudget`; no new replacement digit sum, reversal, or step operation is introduced.

In the unchanged foundation, `Lychrel196.step n = n + reverse10 n`. Its reversal consumes ordinary decimal units digits, and drops zeros that become leading zeros after reversal. `reverse10` uses `reverseFuel n n 0`, with `reverseFuel_correct` connecting this to the independently recursive `reverseAux`. The fuel is not an assumed correctness oracle.

`DecimalMass.digitSum` recursively adds `n % 10` and the digit sum of `n / 10`; it is zero at zero. `DecimalQuantitativeMass.decimalLength` recursively counts division-by-ten steps and also assigns zero width to zero. These conventions are used consistently.

`DecimalDigits.Canonical n d L` means: positive length, all used digits at most nine, a positive leading digit, and positional value exactly n. The positive-input existence theorem is not applied at n=0. `decimalLength_of_canonical` identifies the actual recursively defined width with the canonical length.

The relevant foundation proofs reviewed include the actual reversal/value bridge, positional sum and column arithmetic, `carry_bounded`, `canonical_exists`, `digitSum_value`, `digitSum_step_balance`, `decimalLength_value` and `decimalLength_of_canonical`, plus `AstraModular.ten_pow_mod99`. The foundation imports only `Std`.

The import graph is:

| Module | Direct imports |
| --- | --- |
| Agent106CarryBudget | LychrelDigitSums |
| Agent106CongruenceSeed | LychrelDigitSums |
| Agent106SparseTarget | LychrelDigitSums |
| Agent106CongruenceObstruction | Agent106CarryBudget; Agent106CongruenceSeed; Agent106SparseTarget |
| Agent106CongruenceControls | Agent106CongruenceObstruction |

## 3. Exact theorem meaning

For the following census, write `s = DecimalMass.digitSum`, `w = DecimalQuantitativeMass.decimalLength`, `T = Lychrel196.step`, and `y(k)=11*(10^k-1)`. Also write `k(R)=7*R/4+1`, `a(R)=k(R)+2`, `y_R=y(k(R))`, and `c(a)=10^a+990*a+rho(a)`, where `rho(a)=89` for odd a and `989` for even a. Division is natural-number division, hence floor division here.

### Agent106CarryBudget: 5 public endpoints

| Endpoint | Hypotheses and exact conclusion |
| --- | --- |
| wordSum_le_constant | For any coefficient function q and natural L,M, if q(i)<=M for every i<L, then wordSum(q,L)<=M*L. Includes L=0 and M=0. |
| carryCount_le_width | If q(i)<=18 for i<L, then the sum of outgoing carries through column L is at most L. No symmetry assumption is required. |
| digitSum_step_budget_of_canonical | Given Canonical n d L, proves s(T(n))<=2*s(n) and 2*s(n)<=s(T(n))+9*L. |
| digitSum_step_budget | For every n, including zero, proves s(T(n))<=2*s(n) and 2*s(n)<=s(T(n))+9*w(n). |
| not_step_of_digitSum_budget | For any n,m, if s(m)+9*w(n)<2*s(n), then m differs from T(n). This is a sufficient rejection criterion, not an equivalence. |

### Agent106CongruenceSeed: 7 public endpoints

| Endpoint | Hypotheses and exact conclusion |
| --- | --- |
| denseOutput_digitSum | k>=2 implies s(y(k))=9*k. |
| denseOutput_decimalLength | k>=2 implies w(y(k))=k+2. |
| denseOutput_canonical | k>=2 gives a digit function d with Canonical y(k) d (k+2). |
| denseOutput_reverse | k>=2 implies reverse10(y(k))=9*y(k). |
| denseOutput_step | k>=2 implies T(y(k))=10*y(k). |
| denseOutput_step_digitSum | k>=2 implies s(T(y(k)))=9*k. |
| finitePrefix_first_step | k>=1 implies T(2*(10^k-1))=y(k). |

### Agent106SparseTarget: 6 public endpoints

| Endpoint | Hypotheses and exact conclusion |
| --- | --- |
| rho_le | For every a, rho(a)<=989. |
| sparse_tail_bound | a>=9 implies 990*a+989<10^(a-5). |
| target_digitSum_le_of_lt_pow | n<10^k implies s(n)<=9*k, including the k=0,n=0 case. |
| target_digitSum_pow_add | n<10^a implies s(10^a+n)=1+s(n), including a=0,n=0. |
| sparse_digitSum_bound | a>=9 implies s(c(a))+44<=9*a. |
| sparse_eight_digitSum | s(c(8))=27, where c(8)=100008909. |

### Agent106CongruenceObstruction: 6 public endpoints

| Endpoint | Hypotheses and exact conclusion |
| --- | --- |
| familyIndex_ge_two | R>=3 implies k(R)>=2. |
| dense_step_digitSum_lower | k>=2 implies 9*(k+2)<=s(T(y(k)))+36. |
| sparse_family_digitSum_gap | R>=3 implies s(c(a(R)))+36<9*a(R). |
| congruence_sparse_jump_separation | R>=3 implies both s(c(a(R)))+36<9*a(R) and 9*a(R)<=s(T(y_R))+36. |
| sparse_family_violates_actual_budget | R>=3 implies s(c(a(R)))+9*w(y_R)<2*s(y_R). |
| congruence_sparse_jump_ne_actual | R>=3 implies c(a(R)) differs from T(y_R). |

### Agent106CongruenceControls: 12 public endpoints

| Endpoint | Hypotheses and exact conclusion |
| --- | --- |
| familyIndex_ge_four | R>=2 implies k(R)>=4. |
| familyWidth_ge_six | R>=2 implies a(R)>=6. |
| sparse_entry_tail_bound | a>=5 implies 990*a+989<10^(a-1). |
| sparse_entry_bounds | a>=5 implies 10^a<=c(a)<11*10^(a-1). |
| sparse_decimalLength | a>=5 implies w(c(a))=a+1. |
| denseOutput_mod99 | For every k, y(k)%99=0, including k=0. |
| sparse_mod99 | For every a, c(a)%99=0. |
| familySource_mod99 | For every R, y_R%99=0. |
| familySource_decimalLength | R>=2 implies w(y_R)=a(R). |
| sparse_family_entry_growth | R>=2 implies y_R<c(a(R))<11*y_R. |
| sparse_family_entry_width | R>=2 implies w(c(a(R)))=w(y_R)+1. |
| congruence_sparse_entry_controls | R>=2 jointly proves the two zero residues modulo 99, both strict growth inequalities, and the exact width increase. |

The census is **5+7+6+6+12=36 public named theorems**. Separately, there are 18 private theorem declarations and five public definitions: `rho`, `sparse`, `familyIndex`, `familyWidth`, and `familySource`. These definitions are not additional theorem endpoints. The companion manifest contains exact source signatures and declaration line numbers for every public theorem.

## 4. Carry arithmetic, width, and zero handling

The unchanged carry recurrence starts at carry(q,0)=0 and uses carry(q,i+1)=(q(i)+carry(q,i))/10. For actual mirrored decimal columns, q(i)<=18 and hence every outgoing carry is at most one. The count is the sum of carry(q,i+1) for i=0,...,L-1: it includes the terminal carry carry(q,L), and excludes any fictitious extra outgoing carry after that terminal position.

The foundational mass identity includes the final carry as the leading output digit. It proves exactly s(T(n))+9*C=2*s(n). Since 0<=C<=L, the two new budget inequalities follow. The bound uses the source width L, not the output width. Overflow is therefore covered correctly.

The n=0 branch explicitly proves T(0)=0, s(0)=0, and w(0)=0, reducing both endpoints to zero inequalities. It does not obtain a nonexistent positive canonical representation of zero. When n=0 the strict hypothesis of `not_step_of_digitSum_budget` is impossible, which is correct.

Sparse-target digit-sum arguments intentionally allow leading-zero padding. The bounded representation lemma provides exactly k used positions for every n<10^k, and `digitSum_value` allows such padding without asserting it is canonical. That padded representation is used only to calculate digit sums. Actual widths are separately obtained from nonzero canonical leading digits or explicit bounds between consecutive powers of ten. There is no substitution of padded width for canonical width.

The separated leading one is justified by n<10^a. This prevents a carry from the tail into the leading digit. In `target_digitSum_pow_add`, only the first a+1 positions of its constructed digit function are evaluated; values assigned beyond that range are irrelevant.

## 5. Boundary review and natural-number arithmetic

### k=0, k=1, and k=2

At k=0, y(k)=0 under natural subtraction. The unrestricted modulo-99 theorem correctly includes this case. The dense digit-sum, width, and reverse/step identities deliberately require k>=2.

At k=1, the first seed edge is 18->99, so `finitePrefix_first_step` correctly includes it. But y(1)=99 has digit sum 18 and width 2, not 9 and 3. Its reversal is 99, not 891, and its next step is 198, not 990. The k>=2 hypotheses on the dense endpoints are mathematically necessary for those formulas.

At k=2, y(2)=1089 has width four, digit sum 18, reversal 9801=9*1089, and true next step 10890=10*1089. The displayed word 1,0,9^(k-2),8,9 has an empty repeated-nine block here; the proof handles that through r=k-2=0.

Private append-digit reversal lemmas require a positive prefix and a bounded appended digit. This correctly retains the prefix width even when a decimal zero is present. Prefix r=0 equals 10; reversing it yields 1, exactly as needed.

### R=2 and R=3

Read-only direct integer calculations were used as boundary diagnostics, not as substitutes for the universal proofs:

| R | k | a | y_R | c(a) | s(y_R) | s(c(a)) | 2*s(y_R)-9*w(y_R) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 4 | 6 | 109989 | 1006929 | 36 | 27 | 18 |
| 3 | 6 | 8 | 10999989 | 100008909 | 54 | 27 | 36 |
| 4 | 8 | 10 | 1099999989 | 10000010889 | 72 | 27 | 54 |

For R=2, both numbers are divisible by 99, strict growth y<c<11*y holds, and width increases by one. But the proposed target's digit sum 27 is above the generic lower budget 18. In shifted form 27+36<54 is false. Consequently the carry-budget rejection cannot be extended from R>=3 to R=2. This does not imply that c is the true successor at R=2; it only means this necessary-condition test does not reject it.

For R=3, a=8 is below the a>=9 threshold of the general sharp tail estimate. The general estimate would fail there: 990*8+989=8909 is not below 10^(8-5)=1000. The separate exact computation c(8)=100008909 and s(c(8))=27 supplies the required strict inequality 27+36<72. The true step has digit sum 54, so the second inequality also holds.

For R>=4, floor(7R/4)+1>=8, hence a>=10. The proof only needs a>=9, so its branch after excluding R=3 is valid. No family case with a=9 is accidentally required or omitted.

The smaller R values are intentionally excluded from the controls. At R=0 the naive formulas give a=3 but y=99 has width two and c=4059 violates c<11*y. At R=1 the naive sparse target c=14949 exceeds 11*1089. The original note gives distinct constructions for these small parameters; this package does not claim to formalize those paths.

### a=5, a=8, a=9 and subtraction

The weaker tail bound for entry controls starts at a=5: 5939<10000. It is sufficient for a genuine leading one and width a+1. The stronger digit-sum bound starts at a=9: 9899<10000. Both inductive extensions add 990 on the left while multiplying the right by ten, with the required slack established at the base case.

Every potentially truncated subtraction is protected by its hypotheses or an explicit positivity fact. Expressions k-2 and k-1 are introduced only with k>=2 and k>=1; a-5 and a-1 are used only in their stated sufficiently large ranges. The terms 11*10^r-1 and 2*10^r-1 have positive bases. The proof keeps the budget in additive form, avoiding an unjustified replacement of truncated natural subtraction by integer subtraction.

## 6. Residue, growth, and relation to the written argument

The modulo-99 calculation is exact on ordinary integer values. The unchanged theorem gives 10^a mod99 equal to 1 for even a and 10 for odd a. The even tail 989 has residue 98, while the odd tail 89 has residue 89; 990*a contributes zero. Thus the corrected sums are zero modulo99 for all a. The dense residue proof uses a recurrence adding 99, and also covers k=0.

The growth proof uses P=10^k with k>=4, hence P>=100. The source is y=11*(P-1), while the target has c>=100*P and c<110*P. The lower inequality gives y<c. For the upper inequality, 110*P<=121*(P-1)=11*y follows already from P>=11, so the established P>=100 is more than sufficient. Thus c<11*y is strict and has no missing small-power exception.

The Section 3 chain is preserved exactly. The canonical source has s(y)=9k and width a=k+2. The generic carry budget yields 9a<=s(T(y))+36. The target satisfies s(c)+36<9a for R>=3, so it violates the actual-step budget and cannot equal T(y). The additional exact identity T(y)=10*y is a valid stronger diagnostic, but the obstruction itself is obtained from the generic carry budget as advertised.

This verifies the particular artificial entry edge and its necessary numerical controls. It does not construct the complete Section 2 path, formalize its first-palindrome time, prove all intermediate predecessor predicates, provide an all-input countermap, exclude every possible repaired countermodel, supply an infinite actual orbit, or settle 196. README's mathematical scope accurately preserves these distinctions.

## 7. Findings by severity and proof-trust limits

**Critical: none. High: none. Medium: none. Low: none.** No source repair is requested.

Informational observations:

1. Preserve the distinct thresholds R>=2 for entry controls and R>=3 for the carry-budget contradiction. Preserve k>=2 for all dense closed forms and k>=1 for the seed's first true step.
2. Built-in `#print axioms` directives in these source modules cover 23 of the 36 public endpoints. The unprinted endpoints are `rho_le` and all 12 endpoints in Agent106CongruenceControls. This is not a proof defect; it means source print statements alone are insufficient evidence for the advertised complete endpoint audit. The separate audit must enumerate all 36 and their transitive dependencies.
3. The README's previous independent core-audit narrative is historical author-supplied evidence. It explicitly says final-package independent review and main integration are not yet established. This semantic report does not promote those historical claims into a fresh build attestation.
4. Source review found no admitted proof, custom axiom declaration, `sorryAx`, `native_decide`, unsafe oracle, `extern`, or `implemented_by` in the new modules. Their proof bodies use ordinary proof-producing tactics and kernel-reducible `decide`. The foundation's matching forbidden-word occurrences were explanatory comments. However, absence of such text is not a compiled dependency audit. Generated implementation placeholders and actual theorem dependencies must be distinguished in the separate complete origin audit; no unsafe runtime oracle is accepted as proof evidence.

## 8. Acceptance disposition

**Accept the frozen package's mathematical statements and intended interpretation at the semantic source-review level.** All advertised necessary conditions and the specific obstruction have the correct hypotheses and ordinary numeric meaning. No uncovered semantic proof obligation remains for the stated 36-endpoint scope.

Completion of the delivery still requires the independently assigned strict exact-source build and complete transitive axiom audit, plus any separately authorized reproducibility, current-main combination, and integration checks. Those are outside this review's attestation. Agent #106 retains active source ownership. Root remains the only external publisher.

The review and companion manifest are independent evidence; neither edits nor replaces the author source, earlier failed attempts, logs, or historical reports.
