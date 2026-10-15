# Finite signed-digit zero uniqueness

`SignedDigitUniqueness.lean` formalizes the critical finite uniqueness step
in `2026-10-14-general-base-seams/GENERAL_BASE_SEAMS.md`. It imports only
Lean 4.19.0's `Std`. All nine public theorems pass a fresh compilation and
transitive axiom audit.

Coefficients are integers, listed least significant first. Evaluation is
defined recursively:

```text
eval b []       = 0
eval b (a::xs)  = a + b * eval b xs.
```

The main theorem says that for an integer base `b ≥ 3`, a finite list with
every coefficient in `[-2,b−1]` evaluates to zero **if and only if every
coefficient is zero**. Empty lists and trailing zeros are included.

The stronger theorem `all_zero_of_eval_zero_open` needs only a positive
base and coefficients strictly between `−b` and `b`. Its key scalar lemma
is `head_tail_zero`: if `a + b*t = 0` and `−b < a < b`, then both `a` and
the integer tail value `t` are zero. A positive tail would force `a ≤ −b`;
a negative tail would force `a ≥ b`. Induction removes one coefficient at
a time. This is the integer-multiple argument underlying reduction modulo
the base, written without requiring additional division machinery.

`all_zero_of_reverse_eval_zero` handles the coefficient reversal used when
clearing powers from a reciprocal-base evaluation. It proves only the list
reversal implication; it does not formalize a rational polynomial evaluation
or the polynomial reflection identities in the accompanying written proof.

`carry_residual_bounds` formalizes the preceding local bound as well. Given
the explicit column equation

```text
coefficient + incoming = digit + base * outgoing,
```

with a coefficient in `[0,2b−2]`, incoming carry in `[0,1]`, outgoing carry
equal to zero or one, and digit in `[0,b−1]`, it proves

```text
−2 ≤ coefficient − (b+1)*outgoing ≤ b−1.
```

The carry-bit and digit-range conditions remain explicit premises. The
lemma does not assert that an arbitrary sequence is an actual normalization.

## Sharp base threshold

`base_two_failure` proves all three facts about the concrete list `[-2,1]`:

- every coefficient belongs to `[-2,1]`;
- its base-two value is `−2 + 2*1 = 0`;
- its coefficients are not all zero.

Thus the requested closed-interval theorem genuinely fails at base two.
The result is uniqueness of the **zero representation** under these bounds,
not general injectivity of signed-digit representations of arbitrary values.
For example, in base three `[1]` and `[-2,1]` both represent one.

This package supports the finite general-base seam argument. It does not
formalize the full raw-symmetry equivalence, prove an infinite invariant,
or establish a Lychrel witness or the 196 conjecture.

## Reproduction

```sh
python check.py /path/to/lean-4.19.0/bin/lean
```

The checker copies the exact source to a fresh temporary directory,
compiles it, and audits every theorem's transitive axioms. Proof placeholders,
extra axioms, and `native_decide` are rejected. Only Lean's standard logical
axioms are permitted. `verification.json` records SHA256 and Git blob hashes;
`compile.log` contains the complete compiler and axiom-audit output.

Development record: the core uniqueness proofs and base-two failure compiled
on the first attempt. The reversal, nonzero-member, and local carry-bound
lemmas were added and also compiled without warnings. The saved report is
a fresh clean build of the final source.
