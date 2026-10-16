# Exact collision digit-mass correction

This contribution proves 17 Lean theorems, including an exact all-length
mass identity for finite collision words B H B and a bridge to the ordinary
digit sum of the actual integer reverse-and-add step. It does not prove
an invariant collision family or decimal Lychrel existence.

## Full normalized mass response

Let M_c(W) be the sum of the normalized digits of a finite coefficient
block W when its incoming carry is c, **including the outgoing carry**.
Let k(W) be the number of consecutive nines at the start of W, counted
from its least-significant end. It may be the entire block length.

For coefficients in {0,...,18} and c in {0,1},

\[
M_c(W)+9c\,k(W)=M_0(W)+c.
\]

`massIn_response_computable` proves this using the recursively computed
`initialNinesLength`; there is no unproved run-length hypothesis. Empty
blocks and all-nine blocks are included. In the latter case the retained
digits all change from nine to zero, but the outgoing carry increases by
one. Omitting that outgoing carry would give the wrong formula.

## Exact B H B collision identity

Write e for the carry after the first B and h for the carry after B H,
both computed in the actual concatenated word starting at carry zero.
Then

\[
M_0(BHB)+9\bigl(e\,k(H)+h\,k(B)\bigr)
=2M_0(B)+M_0(H).
\]

The theorem `three_block_collision_mass` assumes only finite coefficient
bounds and equality of the two B blocks. It includes empty blocks and
does not require symmetry. For canonical digit-pair words,
`actual_step_three_block_collision_mass` substitutes the ordinary numeric
digit sum of the actual next integer on the left side.

Two immediate corollaries are also checked:

* The actual collision mass is at most the sum of independently normalized
  block masses.
* Equality holds exactly when both e k(H) and h k(B) vanish.

The normalization arithmetic is exact even at zero separation. It is not
valid in general to normalize each block with a fresh incoming carry of
zero and then add its mass without the correction.

## Concrete canonical example

Take B=(10,10), H=(9,9). The symmetric pair word is realized by 555455:

\[
555455+554555=1110010.
\]

The resulting digit sum is four. Separate normalization of B, H, B would
give mass 22; the actual correction is 18 because e=h=1, k(H)=2, k(B)=0.
`concrete_collision_mass_loss` checks the arithmetic in Lean.

## Reproduction and limits

```sh
python check.py /path/to/lean-4.19.0/bin/lean
python finite_controls.py
```

The checker rebuilds `LychrelDigitSums.lean`, the previously checked
`IncomingCarry.lean`, and the new module in a fresh temporary directory.
It audits all 17 new theorem declarations, permits only Lean's standard
logical axioms, and records exact source hashes after checking they stayed
unchanged during the run. Results are in `verification.json` and the full
compiler output is in `compile.log`.

The independent Python control exhausts every B,H pair of lengths zero
through two over coefficients zero through eighteen. These controls are
finite sanity checks; the Lean theorem supplies the all-length result.

This identity determines the mass lost at a finite collision. It does not
prove that the resulting block word belongs to a proposed return family,
that a residual carries a permanent obstruction, or that 196 avoids all
future palindromes.
