# Independent review of the seven-step 440 return

Verdict: the conditional boundary return and the proposed middle-word
formulas are correct. They require a **padded symmetric middle**, which
may have zero endpoints. The return and its first seven safe updates do
not establish a domain closed under indefinite iteration.

All words below are ordered least significant coefficient first. Start
with a canonical whole pair word

    Q = (4,4,0) ++ W ++ (0,4,4),

where `W` is nonempty and symmetric, has coefficients in `0,...,18`, and
has an even middle coefficient if its length is odd. Positivity of the
endpoints of `W` is neither needed nor preserved. For each update, let
`c_t` be the actual carry leaving the middle and entering the high-side
outer prefix.

The exact three-column prefix returns after seven updates if and only if

    (c_0,...,c_6) = (0,0,*,0,*,0,1).

Under these conditions the prefixes, lower carries entering the middle,
and whole-word overflow bits are:

| Time | Prefix | Lower middle carry | Overflow |
|---:|---|---:|---:|
| 0 | `(4,4,0)` | 0 | 0 |
| 1 | `(8,8,0)` | 0 | 0 |
| 2 | `(16,16,0)` | 0 | 1 |
| 3 | `(7,14,7)` | 0 | 0 |
| 4 | `(15,8,15)` | 1 | 1 |
| 5 | `(6,14,14)` | 1 | 0 |
| 6 | `(13,9,9)` | 1 | 1 |
| 7 | `(4,4,0)` | — | — |

The whole word and padded middle each gain exactly three columns.

## Why the middle formulas are exact

At one step write `m=|W|`, and normalize `W` with its actual lower
incoming carry, retaining exactly `m` digits `D`. At a nonoverflow step,
the corresponding middle of the next pair word is simply

    D + reverse_m(D).

At an overflow step it has width `m+1`. The new extra endpoint contribution
is the first normalized digit of the high-side exterior. If the current
prefix is `p=(p_0,p_1,p_2)`, that digit is

    E = (p_2+c_t) mod 10.

Consequently the exact new middle polynomial is

    D(x) + x^m D(x^-1) + E(1+x^m).

At steps 2, 4, and 6 the values of `E` are respectively `c_2`, `5+c_4`,
and 0, the last using the required `c_6=1`. This proves the proposed
endpoint corrections directly from ordinary digit placement. It also
explains why dropping or trimming zero endpoints would change the
coordinate system and cannot be done silently between cycles.

## Safety and the missing recurrence hypothesis

The first two prefixes contain only coefficients at most 9, with outside
coefficients 4 and 8. Therefore their next integers are nonpalindromic
exactly when their respective middle words contain a coefficient at least
10. At each of the remaining five steps, the displayed prefix itself
excludes both exact palindrome-predecessor classes.

Thus, conditional on the control word, seven-step safety is equivalent
to the two tests on `W_0` and `W_1`. A proof of repeated safe return must
also establish that the returned middle supplies the next required
control word and both new safety tests. These obligations do not follow
from one or two successful returns.

For a concrete failure, the initial middle

    W_0  = (1,1,18,1,1)

has two safe returns, with

    W_7  = (3,9,8,10,10,8,9,3),
    W_14 = (3,5,4,2,0,0,0,2,4,5,3).

At time 14 the entire pair word has coefficients at most 9. Its next
ordinary integer is therefore palindromic, giving a first positive hit
at step 15. This refutes automatic safe recurrence of the return domain;
it does not exclude a suitably restricted invariant subset.

## Independent finite controls

`independent_reset.py` imports no code from the gate implementation. It
uses ordinary integer evaluation and normalization, and computes boundary
carries as quotients of evaluated coefficient prefixes. It exhausts all
4,190 padded symmetric middles of widths 1 through 5. It separately
exhausts all 128 binary boundary-control words: exactly the four words
matching `00*0*01` return the prefix.

The controls check the return condition, every prefix and carry, the three
overflow corrections, the width increase, and the exact safety condition.
They include 33 returned middles with zero endpoints. All checks pass.
`verification.json` retains counts, complete representative trajectories,
and the two-return failure above.

```sh
python -B proofs/contributions/2026-10-14-seven-step-review/independent_reset.py
```

The finite enumeration is implementation evidence. The digit-placement
argument supplies the unrestricted middle formulas. No new Lean
formalization or infinite-orbit result is claimed by this review.
