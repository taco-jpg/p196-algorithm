# Existing unrestricted prefix obstruction and fixed-zero control

This review prevents duplication of an existing repository result. It
does not exclude arbitrary finite-state invariants or all prefix widths.

## The unrestricted-clock graph already exists

The exact construction and complete width-one-through-five results are in
[`research/main_existence_attempt/prefix_any_clock/`](../../research/main_existence_attempt/prefix_any_clock/README.txt).
The retained `search.cpp`, `results.jsonl`, and `validation.json` were read
for this review. No new execution of that complete global enumeration is
claimed here.

A state is a prefix `p=(q_0,...,q_(k-1))`, with `1<=q_0<=18` and the other
coefficients in `0,...,18`. It denotes **all** canonical symmetric pair
words with this outer prefix and arbitrary total width at least `2k`.
Normalize the prefix forward from carry 0 to get digits `l_i`; normalize
backward from an interior carry `gamma in {0,1}` to get digits `u_i` and
final overflow `h`. The next prefix is exactly

    h=0: p'_i = l_i + u_i;
    h=1: p'_0 = l_0+1,  p'_i = l_i+u_(i-1) for i>=1.

Each branch occurs in an actual canonical word: insert the even central
coefficient `18*gamma` between `p` and `reverse(p)`. That column resets
the carry to `gamma` regardless of the low-side carry. Thus both branches
are necessary for closure of a language containing all completions of
each retained prefix. This does not claim arbitrary carry choices over
many steps can be supplied by one fixed finite integer.

A prefix is universally safe for the next addition exactly when it
contains a coefficient at least 10 and does not lie entirely in `{0,11}`
with outside coefficient 11. Otherwise an even central zero gives an
actual palindrome-predecessor completion. This uses the two exact
`BadWord` classes, not an approximation to palindromicity.

The existing greatest-safe-set deletion removes an unsafe prefix and then
every predecessor with at least one removed successor. Its recorded
results are:

| Retained width | Canonical prefixes | Greatest universal safe set | Maximum deletion rank |
|---:|---:|---:|---:|
| 1 | 18 | 0 | 1 |
| 2 | 342 | 0 | 7 |
| 3 | 6,498 | 0 | 13 |
| 4 | 123,462 | 0 | 20 |
| 5 | 2,345,778 | 0 | 27 |

The source checks a strictly descending successor rank for every removed
safe state and both successor obligations for every survivor. Its source
logic agrees with the stated greatest-safe-set computation. The old
independent arithmetic controls cover all 13,716 branches at widths 1--3.

Consequently, no universally closed safe language of this precise kind,
using at most five outer coefficients, can contain any first-collision
state of the `(1,7)` gate. Width six or greater, restricted interiors,
carry histories, width information, and variable-time return domains are
outside this exclusion. The ranks do not bound a fixed integer's first
palindrome time.

## Why the obvious constant-zero induction fails

The new `fixed_zero_prefix.py` analyzes only the deterministic branch
`gamma=0`, at widths 1--3. The complete results are in
`fixed_zero_prefix.json`:

| Width | Prefixes reaching an unsafe state | Prefixes in a safe-cycle basin | Maximum finite escape time |
|---:|---:|---:|---:|
| 1 | 18 | 0 | 1 |
| 2 | 339 | 3 | 13 |
| 3 | 6,498 | 0 | 21 |

The unique safe cycle at width two is

    (8,12) -> (17,4) -> (8,12).

Both edges are checked by direct ordinary-integer realizations with
central coefficient zero. Therefore the assertion that fixing the
interior carry to zero eventually escapes from every safe prefix is
false. The width-three result does not repair that all-width assertion,
and no odd-width theorem is inferred from widths one and three.

At the level of a proposed induction from width `k-1` to `k`, the new
last coefficient `a` supplies the smaller prefix with carry
`floor((a+gamma)/10)`. It is forced to zero for `a<=8`, forced to one for
`a>=10`, and freely selectable only when `a=9`. Thus a winning carry
schedule for width `k-1` cannot simply be imposed at width `k`; an induction
must prove that the additional coefficient can supply the needed schedule.
This is the precise missing controllability assertion, not a consequence
of the existing finite-rank certificates.

Run the new finite classification from the repository root:

```sh
python -B proofs/contributions/2026-10-14-prefix-controls/fixed_zero_prefix.py
```
