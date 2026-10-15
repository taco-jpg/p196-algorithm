# Full high-region return criterion and a sharp three-return bound

Let `T` be decimal reverse-and-add and `Q(n)` the canonical symmetric pair-coefficient word of a positive ordinary integer, stored least significant coefficient first. Define the high region

`H = {Q : every coefficient lies in 9..18, and Q_0 >= 10}`.

The result concerns membership of `Q(T^(2j)(n))` in this region at consecutive even times. It does not require the intermediate integers to avoid palindromes.

**Theorem.** If `Q(T^(2j)(n))` belongs to `H` for every `0<=j<=R`, then `R<=3`. Three returns are attained by an actual canonical word. Therefore `H` cannot support a permanent two-step return invariant. The sharp example is not a permanently safe orbit and already has a palindrome at positive time two.

The actual-orbit bridge below is a written proof. The complete finite relation is retained in `prefix_certificate.json.gz`, with all accepted and rejected controls. The separate package `../2026-10-15-high-return-rank-formal/` kernel-checks its finite rank obstruction; it does not claim a Lean formalization of this written bridge.

## 1. Exact pair update and exclusion of second overflow

Start with `Q=(q_0,...,q_(L-1))` in `H`. Put `r_i=q_i-9`, `a=r_0`, and `M=L+1`. The established high-carry formula gives

`P=Q(T(n))=(a,r_0+r_1,...,r_(L-2)+r_(L-1),a)`.

For `L=1`, this means `P=(a,a)`. In every case `1<=a<=9`, and `P` is symmetric with coefficients in `0..18`. This is the first of the two updates under consideration.

Let `c_i` be the actual carry into column `i` when normalizing `P`, so `c_0=0` and `c_(i+1)=floor((p_i+c_i)/10)`. All carries are binary. Second overflow is possible only when `a=9`. The neutral-exterior obstruction in `../2026-10-15-neutral-exterior-overflow/NEUTRAL_EXTERIOR.md` states that a symmetric bounded word with exterior nine which overflows produces a new pair coefficient at most eight. Consequently **a return to `H` always has `c_M=0`**.

Thus every return increases the pair-word width by exactly one: the first addition overflows, while the second does not. The actual reflection width in the second update is `M`, not `M+1`.

## 2. A complete carry-aware criterion

Assume second overflow is absent and write `S=Q(T^2(n))`. Define

`u_i=c_i+c_(M-1-i)`, in `{0,1,2}`.

Pairing the two actual output digits at physical width `M` gives the exact formula

| Coefficient `p_i` | Updated pair coefficient `S_i` |
|---|---|
| `0..8` | `2p_i+u_i` |
| `9` | `18-9u_i` |
| `10..18` | `2p_i-20+u_i` |

For example, below nine both outgoing carries are zero, at nine each outgoing carry equals its incoming carry, and above nine both outgoing carries are one. This proves the formula even when the two reflected positions overlap.

It follows that `S` belongs to `H` if and only if all of the following hold:

- there is no second overflow;
- `q_0` belongs to `14..18`;
- every `p_i` belongs to `{4,5,6,7,8,9,14,15,16,17,18}`;
- at every coefficient four or fourteen, `u_i>=1`;
- at every coefficient nine, `u_i<=1`.

Indeed, coefficients `0..3` and `10..13` yield a value at most eight. Four and fourteen give `8+u_i`. Nine gives either eighteen, nine or zero. The remaining allowed coefficients automatically produce values in `9..18`. At the exterior, `u_0=c_(M-1)` is binary and `S_0=2a+u_0` when `a<=8`. Hence `S_0>=10` requires `a>=5`. If `a=9`, absence of overflow forces `u_0=0` and `S_0=18`. This accounts for the stronger exterior condition in the definition of `H`.

### Removing the carry variables

A coefficient different from nine resets the carry to zero when it is below nine, and to one when it is above nine. Therefore `c_i` is the high/low type of the nearest coefficient different from nine strictly to its left, with missing neighbors assigned type zero. By symmetry, `c_(M-1-i)` is the type of the nearest coefficient different from nine strictly to its right.

The criterion can consequently be read directly from the finite word `P`:

1. Its exterior lies in `5..9`, all its coefficients belong to the displayed allowed set, and its first coefficient different from nine is low (`4..8`), unless the whole word consists of nines. This is exactly the no-overflow requirement in the present symmetric setting.
2. Every occurrence of four or fourteen has a high (`14..18`) nearest non-nine neighbor on at least one side.
3. No nonempty run of nines has high nearest non-nine neighbors on both sides.

These are exact conditions, with absent neighbors treated as low; they do not introduce independently selectable carries. A return is safe at both positive intermediate times precisely when `P` additionally contains a high coefficient. The first output is already nonpalindromic because a returning word has `q_0>=14`. For the second output, its exterior `p_0<=9` rules out the exceptional exterior-eleven palindrome class, so the all-small case is the only possible palindrome case.

## 3. The necessary three-column relation

For `L>=3`, write the first three coefficients of `Q` as `(A,B,C)`. They lie in

`A in 10..18`, `B,C in 9..18`.

The first three coefficients of `P` are

`a=A-9`, `x=A+B-18`, `y=B+C-18`.

Let `w=c_(M-3)` be the **actual** carry into the reflection of column two. Define

`ell=floor(x/10)`, `v=floor((y+w)/10)`, `z=floor((x+v)/10)`.

The low exterior is below ten, so the incoming carry at column one is zero and that at column two is `ell`. Symmetry gives the incoming carries at the high reflections of columns one and zero as `v` and `z`, respectively. Hence, when second overflow is absent, the new prefix is exactly

`A'=2a+z`,

`B'=(x mod 10)+((x+v) mod 10)`,

`C'=((y+ell) mod 10)+((y+w) mod 10)`.

The no-overflow requirement is `a+z<10`. Every actual return supplies one of `w=0,1`, satisfies that requirement, and has `A' in 10..18` and `B',C' in 9..18`.

These formulas require only `L>=3`, not disjoint reflected prefixes. At small widths, `w` may be determined by already observed columns. Permitting both binary values enlarges the relation, so such correlations do not invalidate its use as a necessary relation. No claim is made that every admitted edge arises from a complete high-region word, or that arbitrary admitted paths are realizable.

## 4. Complete finite rank certificate

There are exactly 900 input triples and 1,800 binary controls. The producer checks all of them, retaining rejection reasons, all computed carries, candidate prefixes, accepted targets, and ranks. The vertex index is

`100*(A-10)+10*(B-9)+(C-9)`.

Exactly 258 controls give admitted edges; 1,542 are rejected. The rank counts are:

| Rank | Number of vertices |
|---|---:|
| 0 | 760 |
| 1 | 123 |
| 2 | 14 |
| 3 | 3 |

Every admitted edge strictly decreases rank. The only rank-three triples are `(17,9,18)`, `(17,16,9)`, and `(17,16,10)`. Thus a path has at most three edges. Every sequence of actual high-region two-step returns projects to such a path, because its width increases by one at each return and the preceding bridge remains applicable. This proves `R<=3` for initial widths at least three.

The exact finite claim can be reproduced from the repository root:

```sh
python proofs/contributions/2026-10-15-full-high-return/build_prefix_certificate.py
```

The compressed certificate has SHA-256 `8cdd39028645f768a037e495aaba12dc1b75dd28f6ae90b30dfc9aa4bb81ab7a`; its recovered JSON has SHA-256 `ebcbd0686fed8b2988dc42f14a706f99f9403fe607108b9cfe99984bc315d201`. Rank verification is a complete finite calculation, not a sample of starting integers.

## 5. Widths one and two

Width one has an even coefficient `A`. Its first two-step result is `(2(A-9),2(A-9))`; a return is possible only for `A=14,16,18`. The returned words are respectively `(10,10)`, `(14,14)`, `(18,18)`. Their following two-step pair words are `(2,4,2)`, `(11,0,11)`, and `(10,8,8,10)`, respectively, all outside `H`. Thus width one permits at most one consecutive return.

At width two symmetry gives `Q=(A,A)` and `P=(a,2a,a)`, `a=A-9`. For `a<=4` the updated exterior is at most eight. For `5<=a<=8`, the new pair word is

`(2a+1,4a-20,2a+1)`.

This belongs to `H` only when `a=8`, giving `(17,12,17)`. Its following two-step pair word is `(17,3,3,17)`, outside `H`. The remaining case `a=9` overflows and is excluded by the neutral-exterior theorem. Thus width two also permits at most one consecutive return. This completes the uniform three-return upper bound.

## 6. Actual sharpness and its safety limitation

The canonical word

`Q=(17,9,18,9,17)`

has the following successive two-step pair words:

`(16,16,18,18,16,16)`,

`(15,9,14,18,14,9,15)`,

`(12,12,11,9,9,11,12,12)`.

All four words belong to `H`, proving sharpness of the unrestricted three-return bound. The initial center eighteen is even, and the word has an ordinary canonical realization. The independent review retains an explicit integer realization and actual transitions.

However, the first intermediate pair word is `(8,8,9,9,8,8)`. It has no coefficient above nine, so the integer at positive time two is a palindrome. Thus this example does not show three safe returns. The theorem excludes indefinite high-region returns whether or not intervening palindromes occur; it does not settle the optimal finite bound when all intervening outputs must remain nonpalindromic, and it does not exclude later returns after leaving `H`.

## 7. Relation to the restricted return result

The earlier `../2026-10-15-high-carry-renewal/HIGH_CARRY_RENEWAL.md` treats the subcase in which every interior coefficient of `P` is at least ten. Its threshold thirty-two and sharp bound two remain correct. The full criterion allows additional low and neutral coefficients, so that subcase does not exhaust all returns. The present three-return obstruction uses the complete necessary boundary relation, with all binary carry choices retained.

The high-carry map used here is proved in `../2026-10-15-high-carry-reduction-formal/HighCarryReduction.lean` in decimal and in the all-base written persistence note. The neutral-overflow exclusion is separately proved in the root-owned package cited above. The finite graph and its kernel rank certificate do not replace either of these actual-map arguments.

Six hand-constructed examples from the derivation, including two unsuccessful attempts to attain three safe returns, are preserved in `exploratory_controls.json` and reproduced by `retain_exploratory_controls.py`. Their complete integer and pair-word traces retain the distinction between successful high-region returns and palindrome avoidance. No exhaustion claim is attached to these exploratory controls.
