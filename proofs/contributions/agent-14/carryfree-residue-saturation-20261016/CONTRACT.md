# Exact carryfree residue saturation

## Source and ownership

This contract formalizes Theorem 3, its two carryfree constructions, and the elementary physical-coordinate interpretation in `astra_spectral_carry_quotient.md`. Source baseline: `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`; historical source commit: `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`; source blob: `eac5b8f61385a615d9cc3e7796a4d698c66b716b`; source SHA-256: `d39212c9ab98f4c5b0fccb733d3b662e41a09804878178c82b8762684e97fb09`.

Protected ownership was accepted at coordination commit `bdfdc25c3158b81e6c6e40109886cdf80c744e57`, task blob `8912d279695f7f298e0b1bcde5e612660e13ae5f`. Mathematical discovery remains attributed to the original source. Agent 14/root and its actual coverage specialist author the Lean construction; the semantics and runtime specialists are nonauthors.

## Exact propositions

For every natural width L with 5 <= L and L % 2 = 1, and every s < 9 and r < 11, construct an ordinary natural n and least-significant-first digit function d such that:

- `DecimalDigits.Canonical n d L`;
- `not Lychrel196.Palindrome n`;
- `DecimalMass.digitSum n % 9 = s` and `n % 11 = r`;
- every original computed carry `DecimalDigits.carry (columnSum d L) i` is zero at every i <= L;
- the ordinary next integer `Lychrel196.step n` is palindromic and its original output digits are canonical at the same L.

For every even L >= 2 and s < 9, construct the analogous canonical nonpalindromic input with digit sum class s and all the same no-carry and next-palindrome conclusions. No condition n % 11 = 0 is introduced in this even-width theorem.

The odd input is exactly a*10^(L-1)+b*10^(L-2)+c*10^(L-3), where 1 <= u <= 10, b <= 9, a=min(u,9), and c=u-a. The even input is a*10^(L-1), where 1 <= a <= 9. The parameters are selected by a proved Euclidean or equivalent exact modular argument, not a finite experiment.

## Source coordinate bridge

For the actual pair word q=columnSum d L, use the literal finite coefficient evaluation Q(x)=sum_(i<L) (q i : Int)*x^i. Prove Q(1)=2*digitSum n. At odd width prove the constructed Q(-1)=2*((u:Int)-(b:Int)) and that its half modulo eleven equals n modulo eleven. At even width prove Q(-1)=0. The negative value of u-b must use integer subtraction. These are elementary evaluation statements, not a proof of the quotient ring presentation or universal property.

## Boundary conditions

The quantified width is the actual canonical width, with a positive leading digit. The units digit is zero, so the positive input is not already palindromic. At L=5, the two central monomials coincide and have coefficient 2*c <= 2. At L=2 the input a0 maps to aa. Residue zero is represented using nonzero leading digits, including a=9 in the even family. All computed carries include the terminal index L. No assertion is made about later orbit visits to these witnesses.

## Dependencies and acceptance

Reuse the unchanged original `LychrelDigitSums` module, source blob `8a865176625283648a8a20dd2411ed77670eb0a2` and SHA-256 `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`, mapped to `proofs/LychrelDigitSums__0810ace083af80c5.lean`. Reuse its actual carry, canonicality, digit-sum, reversal and palindrome theorems. Do not import a conflicting second concatenated decimal core.

Acceptance requires exact frozen source matching, actual Lean 4.19.0 builds with --trust=0 -j1 -DElab.async=false, all public types and literal axiom reports, complete module-origin theorem and safe-definition audits, and genuine nonauthor semantic and fresh execution review. Only propext, Classical.choice and Quot.sound are permitted mathematical dependencies. All failed attempts, successful source snapshots, commands, logs, and provenance are preserved. Reused compiled objects in author development are labeled as such; the final fresh build uses source copies.

## Exclusions and completion accounting

The carry-defect ideal, the 1782-element quotient isomorphism, overflow saturation, U/S and J, and all orbit-persistence or 196 conclusions remain separate. A checkpoint lacking the literal Q-coordinate bridge is only a physical arithmetic realization result. The original Theorem 3 is marked complete only after that bridge and all verification gates pass. The source census remains explicitly scoped and incomplete across the whole repository.
