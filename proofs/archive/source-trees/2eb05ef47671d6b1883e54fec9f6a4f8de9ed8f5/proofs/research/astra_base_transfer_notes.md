# Stationary block transfer: an exact obstruction through block width four

**Status: no finite decimal Lychrel seed has been constructed.** The result
below excludes one specified transfer mechanism. It does not exclude general
finite-state encoders, arbitrary frames, larger blocks, or decimal Lychrel
numbers. The finite enumeration is executable exact integer arithmetic,
not a Lean-certified computation. No novelty or publication-priority claim.

## 1. Precisely excluded class

Let `T(n)=n+reverse_10(n)` be ordinary decimal reverse-and-add. Let

    x_m = 10 1^m 01 0^m,       m >= 3,

be the archived binary control family. Binary reverse-and-add has
`T_2^4(x_m)=x_(m+1)`, with nonpalindromic intermediate words.

Choose a fixed positive block width `k`, a decimal block `U` of width `k`
(initial zeros allowed), and a block `V` of width `k` with first digit
nonzero. Substitute `0 -> U`, `1 -> V` literally, without any other frame:

    n_m = V U V^m U V U^m.

Let `A=value_10(U)`, `B=value_10(V)`, and `Q=10^k`.

**Checked obstruction.** For `1 <= k <= 4`, there do not exist such `U,V`
and an integer `M` such that for every integer `m >= M` there is a positive
integer `p_m` satisfying

    T^(p_m)(n_m) = n_(m+1).

The return time may depend on `m`. Intermediate palindromes are allowed in
the excluded property, so this is stronger than excluding safe transfers.
The two blocks need not be palindromic, complementary, or distinct.

Thus the obstruction covers literal nonpalindromic and noncomplementary
blocks, arbitrary positive time dilation, and removal of any finite initial
part of the binary control. It is more than a failed test at `m=3`.

It does **not** cover an encoder with different blocks at different returns,
external framing words, parameter-dependent block lengths, a return that
advances `m` by two or more, a finite-state encoder whose output depends on
more than the current source bit, or any alternative decimal construction.

## 2. Two necessary congruences, valid for variable return times

### Modulo 9

The source word has `m+2` zeros and `m+2` ones. Consequently

    n_m = (m+2)(A+B) (mod 9).

Reversal preserves value modulo 9, so `T^p(n)=2^p n (mod 9)`. A proposed
return therefore gives

    [2^(p_m)(m+2) - (m+3)](A+B) = 0 (mod 9).

Choose any sufficiently large `m = 9t-2`. Then `m+2=0 (mod 9)` and
`m+3=1 (mod 9)`. Every iterate of `n_m` is therefore zero modulo 9, while
the target is `A+B` modulo 9. It follows that

    A+B = 0 (mod 9).

No fixed return time was used.

### Modulo 11

Each `n_m` has even decimal width `(2m+4)k`. For an even-width decimal
integer, reversal negates value modulo 11. Thus `T(n_m)` is divisible by
11. Every later iterate remains divisible by 11: at any width reversal is
either value or its negative modulo 11. Therefore every target `n_(m+1)`
of a positive-time return must be divisible by 11.

If `k` is even, `Q=1 (mod 11)`, so

    n_r = (r+2)(A+B) (mod 11).

If `k` is odd, `Q=-1 (mod 11)`, and direct alternating evaluation of the
block word gives

    n_r = 0             (mod 11), if r is even;
    n_r = 3(A-B)        (mod 11), if r is odd.

Requiring divisibility for every sufficiently large `r` forces
`A+B=0 (mod 11)` in the first case and `A-B=0 (mod 11)` in the second.
Together with the modulo-9 condition, both cases are exactly

    A + Q B = 0 (mod 99).                          (1)

All code pairs not satisfying (1) are excluded by this argument, without
an orbit search.

## 3. A finite, uniform bound on every possible return time

Write `q` for the sum of the outer decimal digits, counting a one-digit
numeral's digit twice. The outer sum is positive. At a step without leading
overflow, `q <= 9`, and the next outer sum is at least `2q`. Hence five
consecutive non-overflow steps are impossible: before the fifth one the
outer sum would be at least 16.

In any segment with exactly `d` overflows there are at most `d+1` runs of
non-overflow steps, each of length at most four. Thus its total length is
at most `5d+4`. An ordinary reverse-add increases width by zero or one and
never decreases it. A return `n_m -> n_(m+1)` increases width by exactly
`2k`, so

    1 <= p_m <= 10k+4.                            (2)

Once an iterate is wider than `n_(m+1)`, no later return is possible. The
enumeration may therefore stop at that point.

## 4. Exact periodic-word arithmetic; no finite-sample extrapolation

The new checker stores least-significant-first words as finite lists of
segments `(P,a,b)`. A segment repeats the finite digit pattern `P` and takes
its first `a*m+b` digits. An integer threshold `M` is maintained so all
segment lengths are strictly positive for `m >= M`. Every variable slope
is divisible by its pattern period. The initial family has two variable
segments with period `k`, plus four constant blocks.

Reversal is exact: the reversed segment's pattern is

    P[(b-1-j) mod |P|],       j=0,...,|P|-1,

because `a` is divisible by `|P|`. Segment order is reversed too.

To add the word to its reflection, align segment lengths. For two affine
lengths their eventual ordering is decided by their slopes and intercepts;
raise `M` beyond any crossing. If an aligned span has constant length,
perform literal finite digit addition.

If an aligned span is variable, the raw pair-sum pattern is periodic.
For a decimal column sum `q` between 0 and 18, its carry map on `{0,1}` is

    c -> 0, if q <= 8;
    c -> c, if q = 9;
    c -> 1, if q >= 10.

Their composition across one period is again one of these three maps, so
it is idempotent. After the first period, the incoming carry is fixed under
an additional full period. Output consists exactly of one exceptional
period followed by copies of the stable output pattern and, if necessary,
a fixed-length partial period. Its final carry is computed explicitly.
The leading overflow digit is appended as the actual ordinary addition
requires; it is never treated as an encoded source digit.

This produces the complete next canonical decimal family for every
`m >= M`. It naturally retains the exceptional interfaces that invalidated
the earlier one-column affine encoders. It also retains arbitrary internal
orientation of each block and exact effects of normalization.

Equality with the target family is decided by the same eventual alignment.
On a variable span it suffices to compare a full common pattern period;
raise `M` until that span contains it. On a constant span compare every
digit. Consequently each equality or inequality returned by the checker
holds for **every** `m` at or above its explicit threshold. Checking (2)
then covers every possible return time. No claim is inferred from a few
large numerical examples.

The Python and C++ implementations are
`astra_base_transfer_eventual.py` and `astra_base_transfer_eventual.cpp`.

## 5. Complete enumeration and independent controls

For each `k`, enumerate every

    Q/10 <= B < Q,
    0 <= A < Q,
    A+QB = 0 (mod 99).

The exact symbolic enumeration completed with:

| k | Eligible code pairs | Uniform threshold M | Latest width overshoot | Returns |
|---|---:|---:|---:|---:|
| 1 | 1 | 3 | 3 | 0 |
| 2 | 91 | 7 | 15 | 0 |
| 3 | 9,091 | 12 | 25 | 0 |
| 4 | 909,091 | 13 | 37 | 0 |

In particular, among all eligible pairs of widths at most four, for every
`m >= 13` the target is never reached at any positive time. The modular
argument excludes all ineligible pairs from an eventual return family.
This proves the stated class obstruction, conditional only on correctness
of the finite enumeration and the supplied implementation of the proved
periodic-word algorithm. It is not a kernel-certified finite computation.

The plain digit-array program `astra_base_transfer_blocks.cpp` independently
replays ordinary decimal arithmetic at `m=3`, `m=10`, and `m=13`. It includes
no symbolic word operations. All 918,274 eligible pairs fail to return in
each replay. The symbolic computation is the part extending this to all
large `m`; these numerical replays alone would not do so.

Additional validation:

* Python ordinary-integer addition independently checks every symbolic step
  at `m=M`, `M+1`, and `M+7`, where `M` is the current certified threshold.
  This was completed for **all** 90 one-digit and 9,000 two-digit codes,
  without modular pruning, and all 9,091 eligible three-digit codes.
* A seeded test applies the same independent arithmetic validation to 1,500
  arbitrary block codes with widths from three through six. This sample is
  implementation validation, not an exclusion beyond width four.
* The symbolic arithmetic certifies the known binary four-step return and
  the known quaternary six-step return, with nonpalindromic intermediate
  phases for all parameters above their recorded thresholds. These are
  positive controls in their own bases, never decimal witnesses.

Result files are `astra_base_transfer_eventual_cpp.json`,
`astra_base_transfer_eventual_results.log`,
`astra_base_transfer_eventual_validation.log`,
`astra_base_transfer_blocks_m3.json`,
`astra_base_transfer_blocks_m10.json`,
`astra_base_transfer_blocks_m13.json`,
`astra_base_transfer_random_validation.json`, and
`astra_base_transfer_positive_controls.json`.

## 6. What the mechanism enables, and the unresolved obligation

Unlike scalar digit encoders, the periodic-word algorithm handles whole
blocks, actual carry normalization, and changing exceptional interfaces.
It can check a proposed framed or finite-state transfer once its eventual
word family and return relation have been specified. A finite-state encoder
acting on long constant source runs eventually produces periodic blocks;
after restricting the run parameter to suitable residue classes, such
families are natural inputs to this method. This is a checking mechanism,
not evidence that a compatible decimal family exists.

The exact missing positive object is still a nonempty finite decimal
family with a rigorously closed return, valid canonical numerals, and
palindrome avoidance at **every** intermediate phase. No such object was
found. A potential next construction must escape the specific stationary
width-at-most-four, one-parameter-step block class excluded above—for
example by genuinely different framing or encoder states at returns,
larger blocks, or a different parameter update. No assertion here says
that one of those alternatives will succeed.

## Reproduce

From the archive directory:

```sh
g++ -O3 -std=c++17 astra_base_transfer_eventual.cpp -o /tmp/astra_eventual
/tmp/astra_eventual 4
python3 astra_base_transfer_eventual.py --max-k 3 --validate
python3 astra_base_transfer_eventual.py --max-k 2 --validate --all-pairs
python3 astra_base_transfer_eventual.py --controls-only
python3 astra_base_transfer_eventual.py --random-count 1500 --random-seed 19610413
g++ -O3 -std=c++17 astra_base_transfer_blocks.cpp -o /tmp/astra_blocks
/tmp/astra_blocks 4 13
```

These programs use only standard Python and C++ libraries. No solver,
floating-point arithmetic, timeout, or resource cap decides the exclusion.
Elapsed times in JSON are descriptive only.
