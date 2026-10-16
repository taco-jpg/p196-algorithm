# Finite probability audit: exact counterexamples and the missing inequality

14 October 2026. No all-time decimal avoidance estimate or Lychrel witness
was obtained. The completed results below are exact counting formulas and
counterexamples to specific probabilistic implications. They do not refute
the deterministic 196 conjecture.

Write `T(n)=n+reverse10(n)`. Probability in this note always means choosing
one seed from a specified finite ensemble once, then applying deterministic
`T`. There is no fresh randomness at later times.

## 1. Primary-source audit

Rostand S. Kuitché, *Lychrel Numbers in Base 10: A Probabilistic Approach*,
Advances in Pure Mathematics **14** (2024), 667–694,
[DOI 10.4236/apm.2024.148037](https://doi.org/10.4236/apm.2024.148037),
[primary PDF](https://www.scirp.org/pdf/apm2024148_45302477.pdf).
Section 3 counts uniform-width palindromes, substitutes such a density for
iterate probabilities, and uses approximate block frequencies to estimate
length growth. Page 680 bounds the probability of ever reaching a first
palindrome by one first-hit time probability. Section 3.3 also replaces
zero probability by a numerical threshold. These steps do not establish
an all-time estimate for a deterministic orbit or a finite seed ensemble.
The valid set inclusion “first hit at time t implies palindrome at time t”
does not imply the displayed bound for the union over all times.

Ando, *Carry Asymmetry, Palindrome Characterization, and Conditional
Non-Convergence in the Reverse-and-Add Process* (February 2026),
[primary LaTeX source](https://github.com/nkc-daiki/196-carry-asymmetry/blob/main/paper.tex),
Section 4. W2 bounds nontrivial Fourier coefficients of individual digit
marginals. Subsequent convolution and carry-decoupling assertions require
joint-distribution information absent from W2. Sections 2–3's elementary
column equations and palindrome characterization agree with the criterion
already formalized in this project. The counterexamples below concern the
W2-only probabilistic implications, not claims about a verified law for 196.

More precisely, they refute the local convolution and decoupling deductions
from the stated single-time marginal inequality. They do not construct an
ensemble satisfying that inequality at every sufficiently late RAA step,
so they are not by themselves counterexamples to an implication whose
hypothesis separately assumes such an all-future property.

## 2. Nondegenerate digit marginals can collapse to a certain palindrome

Fix any even width `L=2m`. Choose a leading digit `a_0` uniformly from
`{1,...,9}` and inner half-digits `a_1,...,a_(m-1)` independently uniformly
from `{0,...,9}`. Complete the other half by complementing mirrored digits
to 9. The resulting ensemble has exactly

    M = 9 * 10^(m-1)

distinct canonical inputs. Every mirrored pair sum is 9. Every input is
nonpalindromic, because equality of a mirrored pair would require `2a=9`.
Ordinary addition has no carries, so **every input maps to `10^(2m)-1`**.

Let `zeta=exp(2*pi*i/10)`. At an internal position the digit is uniform on
all ten residues, hence every nontrivial Fourier coefficient is zero.
Each endpoint is uniform on nine consecutive residues. For `k=1,...,9`,
the complete ten-root sum is zero, so deleting one term leaves a sum of
modulus 1. Thus the maximum nontrivial Fourier modulus is exactly

    eta_input = 1/9,       eta_output = 1.

This disproves an implication `eta_output <= alpha*eta_input^2`, with
`alpha<1`, from marginal nondegeneracy alone. The two mirrored digits
are dependent; their Fourier coefficients cannot be multiplied as if
they were independent. It also disproves any universal length-decaying
palindrome-probability bound derived solely from those marginals: the
palindrome probability is 1 at every chosen width.

All these inputs have digit sum `9m`, which can be arbitrarily large.
Consequently a high digit sum alone cannot exclude a next-step palindrome.
The uniform digit-sum theorem remains valid and useful for its stated
escape conclusion, but does not supply the missing conditional correlations.

## 3. Exact carry-decoupling counterexample with marginals one-half

Choose uniformly from the two nonpalindromic seeds

    a = 22421411,      b = 33532522.

Corresponding digits differ by exactly 1. At each position the marginal is
uniform on two adjacent residues, so its nontrivial Fourier moduli are
`|cos(pi*k/10)|` and `eta=cos(pi/10)<1`.

Use least-significant-first digits, `q_i=d_i+d_(L-1-i)`, and carries
`c_0=0`, `c_(i+1)=floor((q_i+c_i)/10)`. Define
`I_k=[c_k=c_(L-1-k)]`, exactly the carry-match index used in the source.

| Seed | Next iterate | Carry word `c_0,...,c_8` | `I_1,I_3` |
|---|---:|---|---|
| 22421411 | 33833833 | 000000000 | 1,1 |
| 33532522 | 56056055 | 000100100 | 0,0 |

Both final carries are zero. Hence

    P(I_1=1)=P(I_3=1)=1/2,
    P(I_3=1 | I_1=1)=1 > 1/2+1/100.

The proposed distance-two decoupling estimate therefore does not follow
from W2, even when both relevant unconditional match frequencies are
exactly one-half. The actual one-step palindrome probability is `1/2`,
larger than `0.512^floor(8/4)=0.262144`.

This is an all-length obstruction, not merely an eight-digit accident.
For width `4m`, specify the first `2m` pair coefficients as follows: at
even positions `2j`, alternate 3 and 8 starting with 3; at odd positions
use 3, except that the last coefficient is the opposite 3/8 type from its
preceding even coefficient. Reflect this half-word. Realize each pair 3
as low/high digits `(1,2)` and each pair 8 as `(4,4)`, obtaining `a_m`.
Obtain `b_m` by adding 1 to every digit.

For `a_m`, every carry is zero. For `b_m`, the pair sums are 5 and 10;
the carry after each column is therefore exactly the indicator that its
pair type was 8, independent of the incoming carry. The outer type is 3,
so final carry is zero. At every selected position
`k=1,3,...,2m-1`, the compared types are opposite, including the central
comparison by construction. Thus all selected indicators are 1 on `a_m`
and 0 on `b_m`. Their joint probability remains `1/2` for arbitrarily
large `m`; every conditional match after one previous match has probability
1. The digit Fourier bound is unchanged. For every `m>=2`, this exceeds
`0.512^m`.

## 4. Exact one-step counts under a genuinely uniform input law

The project theorem `DecimalDigits.palindromePredecessor_iff` in
`continuation/LychrelDigitSums.lean` says that a positive input produces a
palindrome exactly when either (A) all pair sums are at most 9, or (B) the
outer pair sum is 11 and all pair sums belong to `{0,11}`. The two cases
are disjoint.

There are 45 admissible outer digit pairs in A and 55 choices for each
inner pair. In B there are 8 choices for the outer pair and 9 choices
for each inner pair. For an odd center, A permits five digits and B
permits only zero. Therefore the exact number `N_L` of canonical `L`-digit
inputs whose **next** iterate is palindromic is

    N_1       = 4,
    N_(2m)    = 45*55^(m-1) + 8*9^(m-1),
    N_(2m+1)  = 225*55^(m-1) + 8*9^(m-1),   m>=1.

For uniform even-width inputs, division by `90*100^(m-1)` gives

    P(T(n) palindrome) = (1/2)*(11/20)^(m-1)
                         + (4/45)*(9/100)^(m-1).

This is already exponentially larger than the uniform-integer palindrome
density `10^(-floor(L/2))`. A deterministic pushforward of uniform input
digits is not uniform among output integers of the resulting length.

To require a first hit at step 1, remove initially palindromic inputs.
Exactly `4*5^(ceil(L/2)-1)` of those are in A, and none are in B. Thus
subtract this quantity from `N_L` and divide by
`9*10^(L-1)-9*10^(ceil(L/2)-1)` for `L>=2`. For instance, among the 810
nonpalindromic three-digit seeds, exactly 213 hit at step 1:

    P(first hit at 1) = 213/810 = 71/270.

For a separate elementary union counterexample, both 57 and 58 avoid a
palindrome at step 1 and hit at step 2. Under their uniform law,
`P(palindrome at step 1)=0` but `P(ever hit)=1`.

## 5. An exact local repair: actual prefix counts

Fix one finite nonpalindromic seed ensemble `E` of cardinality `M`.
Let `A_t` be the seeds surviving through time `t`. At time `t`, split
`A_t` by the actual width `L` of `T^t(n)`, retaining seed multiplicities
when different seeds merge. Call one such group `E_(t,L)`.

For this group, reveal one representative of each mirrored pair and the
center if present. Let `C_j` be the subset where the first `j` revealed
pair sums satisfy A. Let `D_j` be the subset where the outer sum is 11
and the next `j-1` sums belong to `{0,11}`. Define `C_0=D_0=E_(t,L)`.
At the last index `r=ceil(L/2)`, these are exactly the two disjoint
next-step first-hit sets. Consequently the exact identity is

    |H_(t+1)| = sum_L (|C_r| + |D_r|).

The sufficient local inequalities are **actual seed counts**

    |C_j| <= a_(t,L,j) * |C_(j-1)|,
    |D_j| <= b_(t,L,j) * |D_(j-1)|,                 (P)

with empty prefixes handled as zero. They give

    |H_(t+1)| <= sum_L |E_(t,L)| *
                  (product_j a_(t,L,j) + product_j b_(t,L,j)).

No independence, mixing, or probabilities for unspecified random digits
are needed. Only these two particular nested prefix families need to be
controlled; requiring all digit-history conditional laws to mix would be
stronger. Summing valid bounds for the right-hand side and obtaining a
total strictly below `M` proves a finite witness exists. The missing
ingredient is an all-time verification of (P) or another first-hit bound
for one fixed ensemble. None was established here. Both explicit
counterexamples show why single-position Fourier bounds cannot verify (P).

There is a nonnegotiable finite-atom consequence. Every nonzero first-hit
probability is at least `1/M`. A bound `|H_t|/M <= u_t` with `u_t -> 0`
therefore forces `H_t` to be empty after a finite threshold. In particular,
even a correct exponential bound for every future time of a fixed finite
ensemble is an eventual deterministic exclusion theorem. It cannot be
justified by finite numerical frequencies.

For completeness an explicit summable form can be stated. If `l_0` is
the minimum initial width, then

    length(T^t(n)) >= l_0 + floor(t/5).

Indeed, during a no-overflow step with leading/trailing digits `a,b`, the
new trailing digit is `a+b` and the new leading digit is at least `a+b`.
After the first such step both endpoints are positive and the trailing
digit at least doubles on every further no-overflow step. Five consecutive
no-overflow steps are impossible. Grouping time in blocks of five proves
the displayed bound.

Suppose one had actually proved, for `0<r<1`, `C>0`, and every `t>=H`,

    |H_t|/M <= C*r^(l_0+floor(t/5)).                (Q)

Write `H=5q+s`, `0<=s<5`. The tail sum would then be bounded by

    C*r^(l_0+q) * ((5-s) + 5*r/(1-r)).

If that is below the verified survivor fraction at time `H-1`, existence
follows. This is a fully quantified sufficient inequality with an explicit
tail, but (Q) is unverified. The digit-sum escape theorem does not imply it.

## 6. Concrete fixed-ensemble check and reproduction

Literal iteration of all 810 nonpalindromic three-digit seeds through
100 steps finds 797 first hits, all by step 23. The 13 survivors are

    196, 295, 394, 493, 592, 689, 691, 788, 790, 879, 887, 978, 986.

Their one-step images have multiplicities `887:7`, `1675:4`, `1857:2`.
Thus this surviving ensemble has at most three current states at every
future time; merging never adds entropy. Also `T(887)=1675`, so the first
two groups are phases of one orbit. The apparent thirteen samples are
strongly dependent. Nothing in this computation bounds their future hits.

Run from the project root:

    python main_existence_attempt/return_pass/probability/check_probability.py

The checker verifies the carry-decoupling construction at widths
`4,8,...,400`, exact one-step counts through width 5, the complete three-digit
first-hit table through 100, and finite controls of the five-step width
lemma. It writes `check_probability.json`. The all-length statements have
written proofs above, not new Lean formalizations. Root's separately
written `return_pass/root_probability_audit.py` independently checked the
sum-9 families through width 8, one-step counts for every positive
`n<10^6`, and the two explicit carry-indicator atoms.

No subprocess is left running. No package, upload, publication, or
modification of existing theorem files was performed in this branch.
