# Agent 107 — neutral exterior alternating residue

## Status and exact scope

**PAPER PROOF + COMPUTED.** For every base `b >= 2`, every nonempty
closed exterior cycle allowed by the unchanged A120 neutral checker has

\[
\sum_{j=0}^{|B|-1}(-1)^jB_j\equiv(-1)^{|B|}\pmod{b+1}
\tag{1}
\]

at every phase. Width, period and legal neutral suffix trims are unrestricted.
This is a necessary condition, not a cycle decision or a decimal certificate.
The accompanying exact DP counts words satisfying (1); it does not construct
their transition graph. No new Lean theorem is claimed in this PR.

Coordination: issue #289, claim6432905598, progress6432977737, strengthened
all-base statement6433000323. Agent108 independently owns the decimal
A120 Lean bridge; Agent9 retains the bounded exterior census.

## Prior work and contribution

The alternating-charge mechanism is established prior work. Relevant modules:

- `P196/Drafts/D20261015Agent2ComplementarySearchAlternatingCharge/AlternatingCharge.lean`:
  alternating sum/sign, decimal normalization and complementary-map charge laws.
- `P196/Core/OuterCharge.lean` and `OuterOrbit.lean`: charge, suffix invariance,
  nonneutral overflow reset and finite-time absorption.
- `P196/Agent5EvenBaseAbsorption/GeneralMomentAbsorption.lean`:
  all-base normalization/moment algebra for its phase-changing exterior map.

Those exterior maps differ from A120's fixed neutral phase and complementary
reverse-entry carry. This report supplies the explicit A120 adaptation, the
strong residue (1) even when `b` is odd, and a small exact counting tool.
It does not claim invention of the alternating-moment method.

## Definitions and normalization identity

Put `q=b-1`, `m=b+1`, and define

\[
A(W)=\sum_j(-1)^jW_j,\qquad s(W)=(-1)^{|W|},\qquad
R(W)=A(W)-s(W),\qquad Q(W)=2A(W)+q\,s(W).
\]

For `norm b W c = (D,d)`, coefficientwise carry conservation gives

\[
A(D)+s(W)d\equiv A(W)+c\pmod m. \tag{2}
\]

To see this directly, write `D_j=W_j+c_j-b*c_(j+1)` and alternate the
sum. Internal carry terms have coefficient `±(b+1)`; only entry `c_0=c`
and exit `c_n=d` remain. This includes empty words.

Appending one neutral coefficient has the exact integer effects

\[
R(W+[q])-R(W)=m\,s(W),\qquad Q(W+[q])=Q(W). \tag{3}
\]

Thus every literal neutral suffix trim preserves `R mod m`, and preserves
`Q` exactly, including full trimming to the empty word.

## Exact neutral exterior law

For a source satisfying A120 `Hyp`, the carry bounds and carry inequality
force `e2=1-e1`. Write `e=e1`, `r=1-e`, `s=s(B)`, and

\[
(D,e)=\operatorname{norm}_b(B,0),\qquad
(H,g)=\operatorname{norm}_b(B^{\rm rev},r).
\]

Here `e,r,g` are bits. From (2), reversal and equal normalized lengths,

\[
A(D)\equiv A(B)-se,\qquad
A(H^{\rm rev})\equiv A(B)-sr+g\pmod m. \tag{4}
\]

When `g=0`, A120's raw next exterior is the coefficientwise sum
`D + H.reverse`, of length `|B|`. Hence

\[
A(B_{\rm raw}')\equiv2A(B)-s,\qquad
R(B_{\rm raw}')\equiv2R(B)\pmod m. \tag{5}
\]

When `g=1`, the raw lists are `D++[q*r]` and `[1]++H.reverse`, of length
`|B|+1`. Therefore

\[
A(B_{\rm raw}')\equiv s\bigl(b-me\bigr),\qquad
R(B_{\rm raw}')\equiv s\bigl(b-me+1\bigr)=sm(1-e)\equiv0\pmod m.
\tag{6}
\]

Equations (3), (5), (6) give, for every legal suffix trim to `B'`,

\[
\boxed{R(B')\equiv\begin{cases}2R(B)&g=0,\\0&g=1\end{cases}\pmod{b+1}.}
\tag{7}
\]

The raw alternating-sum statements are congruences, not integer identities.
All derivations include `B=[]`: its entry carry is0, reverse entry is1,
overflow is1 and raw successor is `[b]`.

## Closed cycles and finite-time absorption

A closed exterior cycle must contain an overflow. Otherwise no phase could
be empty, because an empty exterior emits overflow1. Let `x>0` be the first
coefficient of a nonempty phase. On an overflow0 edge, the final reverse
normalization gives `x+h<b`, where `h` is a bit. Thus the raw successor's
first coefficient is `2*x+h >= 2*x`. Removing a proper suffix preserves it.
Full removal would create an empty phase, already excluded in a hypothetical
all-overflow0 cycle. Strict increase of the first coefficient at every step
contradicts closure.

Start immediately after an overflow. Equation (7) sets the residue to0 and
keeps it0 on every later edge, including a full turn around the cycle.
This proves (1) at all phases. In particular, neither empty nor all-neutral
exteriors can occur: (3) gives their residue `R=-1 mod(b+1)`.

The same argument bounds any consecutive overflow0 run by
`L=ceil(log2(b))` edges. At its `t`-th source the positive head is at least
`2^t` and must be at most `b-1`. Consequently every continued legal path
enters residue0 within `L+1` edges (five in decimal) and stays there.
This is a statement about accepted template transitions, not an orbit bound
for arbitrary decimal integers.

For comparison, `Q=2R mod(b+1)`. Inferring (1) merely by dividing the
zero-Q condition would be invalid for odd bases. The stronger conclusion
uses (5)–(7) directly. At `b=3,B=[1]`, Q is0 modulo4 but R is2 modulo4;
this word passes the weaker filter and fails the necessary cycle filter.

An equivalent exact-suffix charge is `J=A-1` at even width and `J=A-b` at
odd width. Then `J=R mod m`, `J(B+[q])=J(B)` over the integers, and
`Q=2*J+m` exactly. Thus the full cycle condition also reads
`Q=b+1 mod(2*(b+1))`, which is stronger than zero-Q modulo `b+1` in odd bases.

## Exact state counts

The counted universe consists of all coefficient words of lengths0 through M,
with coefficients in `0..2*(b-1)` and nonzero first coefficient when nonempty.
Empty is included only in the total. Neutral suffixes are permitted; these
are not counts of distinct maximally trimmed representatives.

For each exact length n the DP records the distribution of `A(B) mod(b+1)`.
It starts with residue0, uses `1..2*(b-1)` at position0 and
`0..2*(b-1)` thereafter, and adds each signed coefficient to the residue.
The accepted residue is `(-1)^n`. Thus the cumulative decimal universe
has `19^M` words; the following counts are exact integers.

| Maximum width M | All words, including empty | Words satisfying (1) |
|---:|---:|---:|
| 1 | 19 | 1 |
| 2 | 361 | 34 |
| 3 | 6,859 | 620 |
| 4 | 130,321 | 11,856 |
| 5 | 2,476,099 | 225,077 |
| 6 | 47,045,881 | 4,276,958 |
| 7 | 893,871,739 | 81,260,909 |
| 8 | 16,983,563,041 | 1,543,960,696 |
| 9 | 322,687,697,779 | 29,335,244,135 |
| 10 | 6,131,066,257,801 | 557,369,662,783 |
| 11 | 116,490,258,898,219 | 10,590,023,528,227 |
| 12 | 2,213,314,919,066,161 | 201,210,447,209,175 |

Odd-base controls at maximum width6 use the full modulus:

| Base | Modulus | Retained | All words |
|---:|---:|---:|---:|
| 3 | 4 | 3,906 | 15,625 |
| 5 | 6 | 88,584 | 531,441 |
| 11 | 12 | 7,147,242 | 85,766,121 |
| 17 | 18 | 71,748,306 | 1,291,467,969 |

Reproduce any row with the same `count` command, its base, and `--maxlen 6`.

The roughly elevenfold decimal reduction is a combinatorial count, not a
measured speedup. A search may safely remove nonzero-residue states when
seeking cycles. A bounded longest-path or transient classification must
account for the discarded initial steps separately.

## Reproduction and checks

From the repository root:

```bash
python3 calculation/agent-107/exterior_charge.py selftest
python3 -O calculation/agent-107/exterior_charge.py selftest
python3 calculation/agent-107/exterior_charge.py count --base 10 --maxlen 12 --include-empty
python3 -O calculation/agent-107/test_exterior_charge.py
python3 tools/verify.py --changed
```

The source selftest compares the carry-loop normalization with independent
whole-integer normalization at fixed width. It checks all literal suffix
trims and reads the eight concrete known-base certificates directly from
their Lean source; no new certificate is assumed.

Normal and optimized Python selftests return `status: PASS` with:

```text
strong_residual_laws=23380  exhaustive_words=18324  random_words=5000
source_certificates=8  source_certificate_edges=56
all_legal_raw_trims=27485  padding_controls=60140
normalization_identities=46760  dp_bruteforce_rows=25
empty_base_cases=199  odd_base_counterexample=1
```

The separate test suite passes6 tests. It uses whole-integer normalization
for3,356 odd-base steps and3,878 suffix trims, and replays112 exterior cycles
with1,792 edges after concentrating all trims at individual phases.
Its meet-in-the-middle enumeration of integer alternating sums independently
reproduces the decimal width8 count and odd-base counts through width6;
it does not call the DP to obtain its expected counts. Invalid numeric
inputs are rejected under optimized Python. No dependency on another new PR
is needed: its fixture reader is the existing main-branch mirror's parser.

Repository gate: `python3 tools/verify.py --changed` passes the repository
rules for5,217 Lean files/301 projects and selects0 changed Lean modules.
This gate supplies no new Lean proof of the mathematical result above.

## Limits

The residue is necessary only; no cycle is constructed, and no new decimal
period or width is excluded. The proof uses the A120 complementary-carry
condition and positive nonempty exterior head. It does not apply unchanged
to a different template, an arbitrary raw integer orbit, or a carry stream
that violates those hypotheses. Existing known-base certificates all pass.
