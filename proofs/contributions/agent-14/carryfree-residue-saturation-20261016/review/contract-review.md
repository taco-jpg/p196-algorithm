# Independent contract review: carry-free residue saturation

## Decision, ownership, and verification status

**Decision: `SEMANTIC_CONTRACT_APPROVED` for the Theorem 3 scope stated below.** The source construction and the proposed every-width saturation endpoints are mathematically sound. The source-coordinate bridges and the minimum-width cases are required parts of the contract.

Reviewer: Agent #14 / `spectral_semantics`, a genuine separately assigned nonauthor reviewer. No candidate Lean source was authored, modified, or compiled during this review. The coordinator retains Git ownership and issue #61 publication. The accepted task reference supplied by the coordinator is `agent14-carryfree-residue-saturation-20261016`, coordination commit `bdfdc25c3158b81e6c6e40109886cdf80c744e57`, task blob `8912d279695f7f298e0b1bcde5e612660e13ae5f`.

The reviewed implementation plan is `/workspace/scratch/d43e317f00d9/agent14-scout/carryfree-saturation-plan.md`, SHA-256 `0add1005d44b0be6ac1a98f2521f5ce72e257b26eb57510c73283d85ad45c9ab`. The durable author contract was not yet present at the time of the initial directory check; this review supplies the exact semantic obligations against which that contract and the later frozen implementation should be checked.

## Exact source evidence

| Source | SHA-256 |
| --- | --- |
| `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/astra_spectral_carry_quotient.md` | `d39212c9ab98f4c5b0fccb733d3b662e41a09804878178c82b8762684e97fb09` |
| `proofs/astra_spectral_carry_quotient__979633da1cdcb681.py` | `2c540f6b4947b2ee27e09c7f02da07fcb6ac72ee03f8906385c2643580e88be5` |

The mathematical source was compared byte-for-byte with initial main snapshot `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`; it matches. Its Git blob is `eac5b8f61385a615d9cc3e7796a4d698c66b716b`, preserving the source-map provenance `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`.

Relevant source locations are the physical-word definitions in lines 17–29, coordinate interpretation in lines 99–118, and Theorem 3 and its two carry-free constructions in lines 135–175. The later overflow construction is outside this review target.

The companion Python `low_target` adds both reflected contributions rather than overwriting a central coefficient. Its `signature` evaluates the two exact half-sums, including signed alternating evaluation. Its finite `target_controls` are implementation controls, not the intended universal Lean proof. This reviewer inspected that code and did not rerun it.

## Exact mathematical contract

The quantifier order must remain:

- For **every** odd width `L >= 5` and **every** residue pair `(s,r)` modulo `(9,11)`, there exist a natural number `n` and a digit function `d` satisfying all the required properties at that same width.
- For **every** even width `L >= 2` and **every** residue `s` modulo 9, there exist such `n,d` at that same width, with the source alternating coordinate identically zero.

Quantification over arbitrary natural `s,r` with conclusions normalized by `% 9` and `% 11` is equivalent to quantification over the 99 or nine residue classes. It must not be weakened to eventual-width existence, a width chosen after the residue parameters, or a bounded set of widths.

For the same witnesses `n,d`, let `q = DecimalDigits.columnSum d L`. The required physical conclusions are:

1. `0 < n` and the original `DecimalDigits.Canonical n d L`.
2. The original numeric statement `not Lychrel196.Palindrome n`.
3. The actual computed carry function vanishes at every index `i <= L`.
4. `FoldedDecimal.canonical_next_no_overflow` supplies a canonical representation of the actual `Lychrel196.step n` by `DecimalDigits.output q` at width **L**.
5. The actual next integer `Lychrel196.step n` is a palindrome.
6. `DecimalMass.digitSum n % 9 = s % 9`.
7. At odd width, `n % 11 = r % 11`; at even width, the source alternating coordinate is zero, with no corresponding requirement that `n % 11 = 0`.

The proof should also retain the stronger bound `q i <= 9` for every `i<L`, either in the endpoint or as a checked construction lemma for the same witnesses. The original admissibility of `q` is available from canonicality through `NormalizationBridge.canonical_admissible`.

The carry indexing must be explicit. The source's `c_i` is the carry leaving column `i`, while `DecimalDigits.carry q i` is the incoming carry at column `i`. Thus source `c_i` equals the calculated carry at `i+1`, and the source terminal overflow bit is `carry q L`. The statement for all `i<=L` includes the initial zero, every outgoing carry, and the terminal zero. An unbounded assertion about all natural indices is unnecessary because word semantics only constrain the finite width.

The reciprocal word `q` is symmetric; the **initial integer `n`**, not `q`, is required to be nonpalindromic. The output digit word equals `q` in the carry-free case, so identifying initial digit symmetry with pair-word symmetry would change the claim.

## Required source-coordinate bridge

For the finite source polynomial `Q(x) = sum_(i<L) q_i*x^i`, the interpretation must be checked in the proof, not merely attached as prose to an arithmetic existence theorem.

The minimum needed evaluations for the constructed witnesses are:

\[
Q(1)=2\,\operatorname{digitSum}(n).
\]

At odd width, with the construction parameters below,

\[
Q(-1)=2(u-b),\qquad
\bigl(Q(-1)/2\bigr)\bmod11=n\bmod11.
\]

At even width,

\[
Q(-1)=0.
\]

An indexed finite evaluation into the integers is a sufficient exact realization of `Q(1)` and `Q(-1)`. A full polynomial or Laurent-polynomial quotient development is not necessary for this selected statement. The ordinary evaluation definition must nevertheless correspond to the displayed coefficient sum. The factor-two identities justify exact division by two; they must not be replaced by an unexplained halving of a residue class.

The odd subtraction `u-b` is an **integer subtraction**. For example, at `L=5,u=1,b=9`, the input is `19000`, its pair word is `(1,9,0,9,1)`, and `Q(-1)/2=-8`, whose class modulo 11 is 3. Natural subtraction would yield zero and give the wrong coordinate.

The source's even `r=0` must not be turned into `n % 11 = 0`. At `L=2`, input `10` has pair polynomial `1+x`, hence `Q(-1)=0`, while `10 % 11=10`. Indeed, a two-digit canonical integer divisible by 11 has two equal digits and is already a palindrome, so adding that erroneous residue requirement would contradict the required nonpalindromic input at the minimum even width.

If an initial checkpoint proves only ordinary digit-sum and numeric-residue realization without these evaluation bridges, it should be classified as a physical arithmetic realization result with the source-coordinate bridge still open. With the bridges, it supplies the selected saturation content of Theorem 3, independently of the unproved quotient classification.

## Odd family: definitions, source match, and boundary case

For `1 <= u <= 10` and `0 <= b <= 9`, put `a=min(u,9)` and `c=u-a`. Then `1<=a<=9`, `0<=c<=1`, and `a+c=u`.

Use the digit function with `a` at `L-1`, `b` at `L-2`, `c` at `L-3`, and zero elsewhere. Its value is

\[
n=a10^{L-1}+b10^{L-2}+c10^{L-3}.
\]

At every `L>=5`, these three digit positions are distinct and lie above index zero. The leading digit is positive and the units digit is zero. Original canonicality and the original numeric nonpalindrome conclusion follow from these actual digits; no abstract realizability premise replaces the construction.

The resulting pair polynomial is exactly the source formula

\[
Q=a(1+x^{L-1})+b(x+x^{L-2})+c(x^2+x^{L-3}).
\]

At `L=5`, the two `c` monomials coincide, so the coefficient word is `(a,b,2c,b,a)`. The center is even and at most 2. A proof assuming six distinct coefficient positions would be false at this width. For larger odd widths, all six positions are distinct and the center is zero. In every case each coefficient is at most 9.

The digit sum is exactly `a+b+c=u+b`. At odd width the three nonzero digit exponents have parities even, odd, even, giving

\[
n\bmod99=(a+10b+c)\bmod99=(u+10b)\bmod99,
\]

and the coordinate evaluations give `(s,r)=((u+b) mod 9,(u-b) mod 11)`. The original `AstraModular.ten_pow_mod99` supplies the exact power calculation. All subtracted exponent indices are justified by `L>=5`.

## Odd residue surjectivity and zero residues

The proposed constructive selector is correct. For any target `t` modulo 99, choose `w=99` when `t % 99=0`, and otherwise choose `w=t % 99`. Then `1<=w<=99` and `w % 99=t % 99`. Set

\[
u=((w-1)\bmod10)+1,\qquad b=\lfloor(w-1)/10\rfloor.
\]

Division with remainder gives `1<=u<=10`, `0<=b<=9`, and `u+10b=w`. The selector therefore supplies every residue modulo 99 without finite enumeration or a surjectivity axiom.

For a target pair `(s,r)`, the proposed value

\[
t=(55(s\bmod9)+45(r\bmod11))\bmod99
\]

has the requested residues: 55 has residues `(1,0)` and 45 has residues `(0,1)` modulo `(9,11)`. These fixed arithmetic facts connect the modulo-99 construction to all 99 source pairs. No restriction excluding either zero residue is justified.

In particular, `(s,r)=(0,0)` uses `w=99`, hence `u=b=9`, `a=9`, and `c=0`. At the minimum width the input is `99000`, its pair word is `(9,9,0,9,9)`, and its next value is `99099`. The digit sum is 18 and the input is divisible by 11, so both requested residues are zero while the input remains positive and nonpalindromic.

The source's alternative counting proof also checks out: its only repeated residue pair in the full 100-parameter family occurs between `(u,b)=(1,0)` and `(10,9)`. The constructive selector deliberately uses the 99 representatives `1<=u+10b<=99`. Proving the auxiliary unique-duplicate characterization is optional for proving the saturation endpoint by this different valid argument; if omitted, that separate auxiliary source fact should not be listed as a newly checked Lean declaration.

## Even family and the minimum width

For `1<=a<=9`, use the actual input `n=a*10^(L-1)`, with only its leading digit nonzero. At every `L>=2`, the units digit is zero and the leading digit is positive, so the input is canonical at width `L` and nonpalindromic.

Its pair polynomial is `a(1+x^(L-1))`. The two endpoints are distinct, all coefficients are at most 9, and the actual output is `a*10^(L-1)+a`. This output is palindromic and has exactly the same width. The ordinary digit sum of the input is `a`. At even width, `L-1` is odd, so the two endpoint evaluations cancel at `x=-1`.

Choose `a=9` for residue zero modulo 9, and otherwise choose `a=s % 9`. This covers all nine classes while preserving a positive leading digit. At `L=2`, the family is `a0 -> aa`; the zero-residue witness is `90 -> 99`. No stronger lower-width hypothesis is needed.

## Original interfaces verified during this review

The following types and relevant proof bodies were inspected in the unchanged original source `proofs/LychrelDigitSums__0810ace083af80c5.lean`, previously hash-verified as `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`, blob `8a865176625283648a8a20dd2411ed77670eb0a2`:

| Original interface | Exact contribution |
| --- | --- |
| `DecimalCarry.small_digit_sums_give_palindrome` | Given symmetry, the bound 9, the actual column equation, and initial carry zero, returns all carries zero for `i<=L` and symmetric output digits. |
| `DecimalDigits.columnSum_symmetric`, `column_equation` | Instantiate that theorem with the actual computed `columnSum`, `carry`, and `output`. |
| `DecimalDigits.value_positive`, `palindrome_value_iff` | Turn nonzero leading digit into positivity and the unequal endpoint digits into numeric initial nonpalindromicity. |
| `DecimalDigits.step_palindrome_iff_no_overflow` | Connect the small actual columns to palindromicity of the ordinary next integer. |
| `FoldedDecimal.canonical_next_no_overflow` | Supplies exact next canonical width from the actual terminal carry zero. |
| `NormalizationBridge.canonical_admissible` | Supplies original physical-word admissibility from the actual canonical decimal input, including central parity. |
| `DecimalMass.wordSum_columns`, `digitSum_value` | Supplies the exact `Q(1)=2*digitSum(n)` bridge. |
| `AstraModular.ten_pow_mod99` | Supplies the alternating parity pattern of decimal powers modulo 99. |

These are existing mathematical results and should retain their original attribution. The new work consists of the explicit construction, its source-coordinate arithmetic, and the resulting every-width saturation theorems. The final import mapping and complete dependency/axiom audit remain execution-verification obligations, not claims established by this interface review.

## Acceptance and scope boundaries

The later frozen-source review must check that the same constructed witnesses meet every condition, that all actual-map premises are discharged, that both minimum widths and zero residues are included, and that the signed half-evaluation is handled exactly. No desired residue, output palindrome, canonicality, or actual carry conclusion may be inserted as an extra hypothesis of the saturation endpoints.

Acceptance also requires the actual strict Lean build, full exported-declaration axiom coverage, imported-dependency audit, and independent execution evidence. No `sorry`, `admit`, new mathematical axiom, `native_decide`, oracle assertion, or unproved certificate interpretation is permitted. This contract review certifies none of those later build gates.

The selected claim excludes the carry-defect ideal, its equality or universal property, the quotient isomorphism or cardinality 1,782, derivative-coordinate classification, overflow saturation, the carry charge `J`, and all orbit reachability or persistence claims. It establishes neither a fact about which classes the 196 orbit visits nor an obstruction to an individual orbit. The implementation should be recorded as the exact carry-free residue-saturation component of source Theorem 3 and its actual decimal realization, with the remaining source claims kept separate.

## Durable author contract confirmation

After the initial review, the author stored the durable contract at `/dev/shm/agent14-carryfree-d43e317f00d9/proofs/contributions/agent-14/carryfree-residue-saturation-20261016/CONTRACT.md`, using the authorized alternative workspace after the shared disk filled. The reviewer subsequently read the complete file and independently obtained SHA-256 `ac077f99d5c5bbf49e5e5ef8801872178f3082888f03d417279b45a280c01feb`.

**Confirmation: this exact durable contract satisfies the semantic obligations above.** Its explicit bounds `s<9` and `r<11` are equivalent to the plan's arbitrary natural residue parameters with normalized conclusions. It retains every fixed width, both minimum-width cases, canonical nonpalindromic inputs, every actual carry through the terminal index, and a canonical palindromic next integer at the same width. Its source-coordinate section requires the literal integer evaluation and all three factor-two or zero identities, with signed subtraction. It expressly excludes the false even-width condition `n % 11 = 0`.

The source's positivity is also preserved: the original canonical predicate contains positive width and positive leading digit, and the existing `DecimalDigits.value_positive` theorem yields positivity of the represented integer. Omitting a redundant separate positivity conjunct in the prose endpoint does not weaken that domain. The contract preserves the original decimal module hash, keeps the unrelated quotient, overflow, and orbit claims separate, and correctly reserves complete Theorem 3 coverage until the coordinate bridge and verification gates pass.

This confirmation is an additional hash-specific contract review. The initial record that the file did not yet exist remains accurate for the earlier read. It does not certify any subsequently authored source or build.
