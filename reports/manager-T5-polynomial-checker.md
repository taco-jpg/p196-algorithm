# T5 polynomial checker correction

Status: PAPER PROOF for the corrected acceptance predicate; COMPUTED regression
checks. 没有 new Lean theorem or decimal certificate. Repository-gate status is recorded below.

## Problem 和 correction

The exact published core in [issue #305](https://github.com/taco-jpg/p196-algorithm/issues/305)
supplies the original unguarded core. Independent execution reproduced
`check([], 10) == True` in ordinary Python. Under `python3 -O`, it also accepts
`[('1', '0', '', '0', '2')]` in base 10; its initial number 12 reaches palindrome
33 in one step. These 是 checker false accepts, independent of whether any
valid decimal certificate exists. The original polynomial argument remains valid
under its stated digit-template hypotheses.

The correction retains the original phase representation 和 final-edge shift.
It explicitly rejects malformed inputs before arithmetic. Acceptance conditions 都 use explicit branches; assertions do 不 control acceptance. Samples use
actual integer digit reversal. Exact polynomial coefficient identities are
checked in addition to the three samples.

## Exact accepted language

`check(phases, base)` returns a Boolean. `inspect(phases, base)` additionally
returns a short reason. Input requirements:

1. `base` 是 an ordinary integer in 2..36. Boolean, floating, string, unary,
   negative, 和 unsupported-alphabet bases are rejected.
2. `phases` 是 a nonempty list or tuple of five-string lists or tuples
   `(U, x, M, y, V)`.
3. Every symbol 是 a valid digit of the selected base, using the uppercase
   alphabet `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ`. `x` 和 `y` must each contain exactly
   one digit. Empty `M` is permitted.
4. `U` 和 `V` must be nonempty, 和 `U[0] != '0'`.
5. Each phase 有 a fixed outer mismatch:
   `U[j] != V[-1-j]` for some `j < min(len(U), len(V))`.
6. The parameter stays constant on every edge except the last, which increases
   it by exactly one. Arbitrary or negative shifts are outside this API.

The checker accepts a sufficient language: a nonpalindromic family
without a mismatch in these fixed outer blocks can be rejected. Soundness remains intact. Accepted words 都 有 its displayed canonical width for
every integer parameter `n >= 0`.

## Soundness argument

Write `W(n)=U x^n M y^n V`, with repetition interpreted as concatenation.
Let `t=b^n`, `r=|M|`, `s=|V|`, 和 `u,m,v` be the positional values of the fixed
blocks. Then `(b-1) val(W(n)) = A t^2 + B t + C`, where

```
A = b^(r+s) * ((b-1)*u + x)
B = -x*b^(r+s) + (b-1)*m*b^s + y*b^s
C = (b-1)*v - y*b^s.
```

The reversed word 有 the same form with tuple
`(reverse(V), y, reverse(M), x, reverse(U))`. Its leading zeroes do not change
numeric reversal 因为 the original word satisfies canonical digit conditions. A target shift by one
substitutes `b*t` for `t`; a shift by zero leaves it unchanged. Thus the scaled
difference between ordinary reverse-add 和 the target 有 degree at most two.
Acceptance verifies zero difference at distinct points `t=1,b,b^2`, so the
identity holds for every `n>=0`. The additional coefficient check verifies the
same identity directly.

The fixed mismatch compares positions in the unchanging outer blocks. They are
disjoint even at `n=0`, so it excludes palindromes at every phase 和 parameter.
Induction through the accepted phase edges yields the actual infinite ordinary
orbit, with the parameter increasing by one per complete cycle. Every state avoids
palindromes. The argument establishes the stated sufficient PAPER certificate
predicate. Kernel verification remains open.

## Reproduction 和 results

Keep `two_run_checker.py` 和 `test_two_run_checker.py` together. From a full
repository checkout, run:

```bash
python3 calculation/manager/test_two_run_checker.py --source reports/REPORT_213.md
python3 -O calculation/manager/test_two_run_checker.py --source reports/REPORT_213.md
```

The harness reads the literal known phase tables from REPORT_213 through Python
AST literal parsing; it does not execute that report. It runs the corrected
checker tests in normal 和 optimized Python, requiring identical output.

```
known_positive_bases: [11,17,26]
negative_regressions: 24
ordinary_integer_phase_controls: 112
rejected_center_mutations: 16
random_polynomial_cases_both_orders: 10000
NORMAL_AND_OPTIMIZED_IDENTICAL True
```

The 112 independent ordinary-integer controls cover every phase at
`n=0,1,2,3,10,100,301`. The three known families 是 pre-existing positive controls.
没有 new seed or existence theorem. The corrected source 和 regression harness
were staged on main `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`; repository
`python3 tools/verify.py --changed` checks the exact proposed tree before publication.
That gate selects zero changed Lean modules 和 supplies no new kernel theorem.
