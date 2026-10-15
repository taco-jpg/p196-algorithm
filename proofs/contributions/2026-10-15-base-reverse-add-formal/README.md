# Ordinary reverse-and-add bridge in every base

`ReverseAdd.lean` adds 15 formally checked declarations connecting the
all-base raw-symmetry and carry-defect theorems to the ordinary integer
reverse-and-add operation. Its dependencies are the frozen 58-declaration
reflection package and nine signed-digit uniqueness declarations. A fresh
Lean 4.19.0 build and axiom audit passes all 82 declarations.

## Input and reversal conventions

A digit list is least significant first, with every digit in `[0,b-1]`
and a strictly positive last digit. `PositiveLast` explicitly excludes
empty and leading-zero input lists. `canonical_input_positive` proves
that such a list evaluates to a strictly positive integer for `b>=2`.

The reversed integer is `eval b digits.reverse`. If the original integer
ends in zeros, the reversed list has zeros at its most significant end.
Integer evaluation ignores those zeros, matching ordinary integer
reversal. No string reversal with a fixed padded numeric width is used.

Define the pair coefficients by

\[
Q=\operatorname{zipWith}(+,D,\operatorname{reverse}(D)).
\]

The module proves that this list has the original digit length, is
symmetric, has coefficients in `[0,2*b-2]`, and has a positive terminal
coefficient. It also proves the exact identity

\[
\operatorname{eval}_b(Q)
 =\operatorname{eval}_b(D)+\operatorname{eval}_b(\operatorname{reverse}(D)).
\]

These facts are derived from the actual digit list. They are not extra
pair-word assumptions supplied to the final result.

## Main results

`reverse_add_normalization` holds for every base `b>=2`. A tagged list
`xs` may put arbitrary reset flags on the pair coefficients; its required
projection equality is `xs.map Prod.fst = pairs digits`. The actual
continuous-carry normalization ignores these flags. The theorem proves:

- its digits lie in `[0,b-1]` and its leading digit is positive;
- its length is the original digit length plus the computed terminal bit;
- its evaluated integer is exactly the input plus its integer reversal.

`reverse_add_defect_safety` holds for every base `b>=3`. If any outgoing
carry computed with the chosen block resets differs from the actual
continuous-carry outgoing carry at the same position, the theorem proves
that this ordinary reverse-and-add result has a **nonpalindromic canonical
digit expansion**, together with digit bounds, positive leading digit,
and the exact integer-value identity.

Every consecutive partition can be represented by its reset flags. As in
the prerequisite package, this uses reset-stream semantics directly;
there is no separate nested block-list concatenation interface.

## The input can still be palindromic

The defect criterion concerns the output. It does not claim that the
input is nonpalindromic in every base. The declaration
`base_three_palindromic_input_control` verifies the following example
using kernel reduction:

\[
212_3+212_3=1201_3.
\]

The pair word is `(4,2,4)`. Resetting at the middle column gives outgoing
carry zero there, while continuous normalization gives outgoing carry
one. The input is palindromic; the output is not. This retained control
prevents importing a decimal-specific input-parity conclusion into odd
bases.

These are one-step theorems. No defect-preservation invariant, infinitely
safe trajectory, or Lychrel witness is claimed. The definitions here are
self-contained all-base lists and integer evaluation, rather than a
claim that the repository's separate decimal iteration API was changed.

## Verification

From the repository root:

```sh
python proofs/contributions/2026-10-15-base-reverse-add-formal/check.py /path/to/lean
```

The checker freshly compiles all six exact source files, verifies their
hashes remain unchanged, audits all 82 declarations, and permits only
`propext`, `Classical.choice`, and `Quot.sound`. It does not reuse local
compiled objects. `verification.json` records exact SHA-256 and Git blob
hashes; `compile.log` retains the complete axiom audit. The single rejected
draft and its replayed compiler failure are retained in `failed_attempts`.
Runtime binaries, compiled objects and temporary source copies are excluded.
