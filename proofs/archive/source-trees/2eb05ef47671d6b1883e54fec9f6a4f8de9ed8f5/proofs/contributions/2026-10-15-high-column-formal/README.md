# A high-column family reaches a palindrome within two positive steps

`HighColumns.lean` formalizes the decimal case of the larger family in
[`SEAM_PERSISTENCE_OBSTRUCTION.md`](../2026-10-15-seam-persistence-obstruction/SEAM_PERSISTENCE_OBSTRUCTION.md).
It imports only the existing frozen `LychrelDigitSums.lean`. There are 14
public theorems, including explicit ordinary-integer controls.

Suppose a canonical seed `n` has pair coefficients `q` of width `L` with

```text
9 ≤ q i ≤ 13  for every i < L,     10 ≤ q 0.
```

The exact ordinary-integer conclusions are:

- `Palindrome (orbit n 2)`;
- `Palindrome (step n)` if and only if every coefficient equals eleven;
- if any coefficient differs from eleven, time two is the first positive
  palindrome time.

“Positive” excludes time zero. The assumptions do not say whether the
original realizing seed is a palindrome: `55 → 110 → 121` is a checked
example where the seed is already palindromic. The theorem does not claim
time two is the first palindrome time under a convention including time zero.

## Proof

The initial coefficient is at least ten, so its outgoing carry is one.
Every subsequent coefficient lies between nine and thirteen, so adding the
incoming one preserves carry one. The first normalized output has width
`L+1`, leading digit one, units digit `q 0 - 10`, and internal digits
`q i - 9`. Every output digit is at most four.

Thus every next pair coefficient is at most eight. The existing ordinary
decimal classification proves that the following reverse-and-add output
is palindromic. The same classification shows that an immediate palindrome
inside this high-column range requires every coefficient to be eleven.
The proof works for `L=1` as well as all larger canonical widths.

The module proves the carry induction, exact digit formulas, new width,
output bounds, and next-column bound before transferring them to the actual
numeric orbit. It does not assume freely chosen carries or a normalized
symbolic representative in place of the ordinary orbit.

## Checked controls and scope

- `55 → 110 → 121`: the original seed is a palindrome, but the first output
  is not; the second output is.
- `56 → 121 → 242`: constant-eleven pair coefficients yield a palindrome
  already at positive time one.
- `999011 → 1110010 → 1210121`: the explicit active-seam family member in
  the written obstruction reaches its first palindrome at time two.
- `77 → 154 → 605`: allowing coefficient fourteen would invalidate the
  uniform two-step claim; its second output is not palindromic.

These controls are proved by Lean's kernel computation. The all-length
high-column result is proved symbolically and does not rely on a finite scan.
The all-base statement, explicit all-parameter seed formula, and seam-mass
calculation remain in the accompanying written proof; they are not all
formalized by this decimal module.

This result shows why current seam activity need not persist. It makes no
claim about the future orbit of 196 or the existence of a Lychrel number.

## Reproduction

```sh
python check.py /path/to/lean-4.19.0/bin/lean
```

The checker freshly rebuilds the exact original dependency and new module,
audits all 14 public theorem declarations, and records source hashes and
axiom dependencies in `verification.json`. `compile.log` preserves the
complete output. Only Lean's standard logical axioms are permitted.

Development record: the complete module, including all four controls,
compiled without errors or warnings on its first attempt. Final verification
uses a fresh source build rather than the development dependency cache.
