# Safe sharpness of three consecutive high-region returns

**Established:** the existing upper bound of three consecutive two-step
returns to the high region is attained while every intermediate integer
remains nonpalindromic. This resolves the explicitly UNKNOWN safe-sharpness
question in the earlier full-high-return checkpoint.

**Latest accepted extension (Agent #1):** [the all-width family](FAMILY_PROOF.md)
`81*10^(m+7)-1`, m>=0, has a complete Lean proof of three safe returns, including
the ordinary-integer bridge. [Formal status and source pins](FORMAL_STATUS.md)
distinguish five axiom-free finite-witness theorems from 70 family-support
declarations using only propext and Quot.sound. No novelty, external human
peer review, or resolution of P196 is claimed. The general upper bound retains
its existing written-bridge / finite-rank-kernel-certificate distinction.

## Definitions and dependencies

Let `T(n)=n+reverse10(n)` on positive ordinary decimal integers. Let `Q(n)`
be the digit word plus its reversal, indexed least significant first.
Let `H` consist of canonical symmetric pair words whose coefficients all
lie in `9..18` and whose exterior coefficient is at least ten.

This contribution was based on main commit
`a71d6e79b009da691e2d97057f83e108a3fcff4f`. The upper bound and its precise
formal/written distinction are in
[`FULL_HIGH_RETURN.md`](../2026-10-15-full-high-return/FULL_HIGH_RETURN.md),
sections 3--6, and the
[prior checkpoint](../../coordination/2026-10-15-full-high-return-bound.md).
The earlier example 80999 reaches a palindrome at time two; it did not
settle safe sharpness. That earlier record is preserved unchanged.

## Exact witness and proof

Take `n0 = 809999999`. Direct additions give:

| t | T^t(n0) | Q(T^t(n0)) is in H | Palindrome |
|---:|---:|:---:|:---:|
| 0 | 809999999 | yes | no |
| 1 | 1809999907 | no | no |
| 2 | 8909998988 | yes | no |
| 3 | 17808998086 | no | no |
| 4 | 85898978957 | yes | no |
| 5 | 161886968815 | no | no |
| 6 | 680756656976 | yes | no |
| 7 | 1360413314062 | no | no |
| 8 | 3964546454693 | no | yes |

The four high-region pair words, in order, are:

```
(17,9,18,18,18,18,18,9,17)
(16,17,9,17,18,18,17,9,17,16)
(15,10,17,17,15,18,15,17,17,10,15)
(12,15,9,13,10,12,12,10,13,9,15,12)
```

Every displayed coefficient is between nine and eighteen, and every exterior
is at least ten. The actual integers at times zero through six are visibly
nonpalindromic. The additions and all digits are reproduced in `witness.json`.
Thus three safe returns exist. The prior upper bound applies without any
safety restriction, so it also bounds safe returns by three. Hence **the
optimal safe-return bound for H is exactly three**.

This is a finite exact proof, not an extrapolation from a long trajectory.
In fact the witness reaches a palindrome at time eight. It is not a Lychrel
number, does not continue forever in H, and has no demonstrated link to the
orbit of 196 beyond sharing the same map.

## Reproduce

```
python3 proofs/contributions/2026-10-15-safe-high-return/verify_witness.py
```

The program compares two implementations at every transition and checks the
stored evidence. It uses no third-party dependencies, network, random search,
or assumptions about independently selected carry bits. The printed numeric
strings preserve exact integers in JSON consumers.

## All-width extension and evidence boundaries

[FAMILY_PROOF.md](FAMILY_PROOF.md) proves the parametric extension, and
`SafeHighFamily.lean` kernel-checks it without a missing ordinary-integer bridge.
The seed above is its m=0 instance. The complete accepted audit is documented
in [FORMAL_STATUS.md](FORMAL_STATUS.md). The prior UNKNOWN safe-sharpness record
is preserved as historical context, not silently changed.

This is finite-time safety for infinitely many seeds, not all-time safety for
one seed. The example terminates at time eight. All work is isolated under
this contribution directory; coordination is in issue #1, as Agent #1.
