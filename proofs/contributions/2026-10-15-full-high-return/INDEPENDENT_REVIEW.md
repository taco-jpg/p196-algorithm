# Independent review of the full high-region return bound

**Verdict: PASS.** The complete written proof, its actual-width bridge, and all small-width cases have been reviewed independently. A separate literal-integer oracle checks all 1,800 controls of the 900-vertex relation. Independent sink deletion confirms that it is a DAG with exactly 258 labeled edges and rank counts `760,123,14,3`; every recorded rank agrees. The complete independent controls and deletion order are retained, not just their totals.

## Actual carry criterion

The first high-carry update has the stated symmetric coefficients and grows the physical width by one. The neutral-exterior lemma is valid in every base at least two: at the first nonneutral coefficient, final overflow forces the high type; the low digit there is at most `b-2`, while its partner at the increased physical width is a zero from the neutral suffix. Their pair is therefore at most `b-2`. The partner is a genuine source column because the first nonneutral index is positive and no farther than the center. This excludes the overflowing second addition in every high-region return without excluding the nonoverflowing maximum-exterior case.

At the remaining physical width, each pair is the sum of two equal coefficients with their actual incoming and outgoing carries. Low, neutral, and high coefficients give exactly the three displayed formulas. In particular, a center overlap merely makes the incoming-carry sum twice one bit; the formulas still hold. The allowed coefficient set, the special restrictions at four/fourteen and nine, and the strengthened outside requirement are all necessary and sufficient.

The nearest-nonneutral reformulation has the correct directions and endpoint conventions. A carry is the type of the last nonneutral coefficient before its position; symmetry turns the carry at the reflected position into the nearest nonneutral type on the other side. Missing neighbors contribute zero. No independently selectable bit is introduced in this exact criterion. The safety addendum is also correct: a returning original word has outside at least fourteen, while its intermediate pair word has outside at most nine. Thus the intermediate word gives a nonpalindromic next output exactly when it has a high coefficient somewhere.

## Projection and complete graph audit

For original width at least three, the first three intermediate coefficients are `a=A-9`, `x=A+B-18`, `y=B+C-18`. The low carries into the next two positions are zero and `floor(x/10)`. Taking the actual carry into the high reflection of position two determines the other two high carries, giving precisely the stated successor triple. This argument does not require disjoint observations: in short words the actual bit is more constrained, and allowing both bits remains an overapproximation. Because a return grows width by one, the projection stays applicable throughout every sequence starting at width at least three.

The independent oracle uses the symmetric coefficient word `(a,x,y,18t,y,x,a)` for each of the two controls `t`. Its central coefficient forces the desired high incoming carry regardless of the low incoming carry. Exact integer evaluation and positional digit extraction recover all low and high carries and successor coefficients independently of the producer's transition routine. Overflow controls are retained but not misinterpreted as no-overflow successors. All rejection reasons, target IDs, and ranks match the supplied certificate. Sink deletion, rather than the producer's recursive rank traversal, removes all 900 vertices and gives maximum path length three edges.

This finite audit verifies the complete necessary relation. It does not assert that all abstract edges or paths are actual high-region trajectories. The separate `HighReturnRank.lean` source and its five standard-axiom reports were also read: its kernel claim is correctly limited to this finite relation. No independent compilation was performed here, and the actual-map projection remains a written proof.

## Small widths and sharpness

The width-one argument uses the necessary even center coefficient. Its only returning cases are fourteen, sixteen, and eighteen, and each following return fails. At width two, symmetry fixes both coefficients; the three-digit formula has a high center only for outside seventeen, and its next two-step image leaves the region. Thus no small-width case can evade the uniform bound.

The explicit positive integer `80999` has initial pair word `(17,9,18,9,17)`. Literal integer reversal and addition reproduce all three high-region returns in the theorem. The full eight-transition continuation, actual carry arrays, and ordinary palindrome flags are saved in `explicit_witnesses.json`. This proves that the unrestricted bound three is attained. Its second positive output is `889988`, a palindrome; continuing the mathematical map after that point does not make it a palindrome-avoiding example.

## Preserved completion failures

All 18 distinct explicit completions attempted during this review are retained, including the sharp word and every failed attempt. These are bounded constructions from the three rank-three prefixes, not an exhaustion of all canonical words. No word in this list demonstrates three returns while all six positive outputs remain nonpalindromic. That sharper safety question remains **UNKNOWN**.

The suggested family `(17,16,9,18^m,9,16,17)` was evaluated at `m=2,4,6,8,10,12`; every case fails the third high-region return. There is also an all-parameter obstruction for this particular family, for every integer `m>=2`. Its first two-step image is

- `(17,10,16,9,16,9,16,10,17)` when `m=2`;
- `(17,10,16,9,17,18^(m-3),17,9,16,10,17)` when `m>=3`.

Both are high. Their next two-step image begins `(16,18,16,14)`: the next intermediate coefficient is seven or eight and resets the relevant high carry. If that image is not high, the proposed third consecutive return already fails. If it is high, its following first-update prefix is `(7,16,16,12)`. The actual incoming carry at the low twelve is one; the reflected incoming carry is some bit `t`. Hence the following pair coefficient at position three is `(12+1) mod 10 + (12+t) mod 10 = 5+t`, at most six. The third return again fails. This eliminates this family only; it does not decide safe three-return sharpness in general.

Reproduce the independent artifacts from the repository root:

```sh
python proofs/contributions/2026-10-15-full-high-return/independent_prefix_audit.py
python proofs/contributions/2026-10-15-full-high-return/check_explicit_witnesses.py
```
