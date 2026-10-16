# An exact quotient with complementary nonneutral constant bands

This note gives an exact two-parameter whole-word transition and a conditional
cycle criterion. Its interiors follow either the two-cycle `6,12` or the
six-cycle `2,4,8,16,14,10`, or any other specified periodic orbit of the rule
below. No interface cycle has been found or searched for in this package.
The formula controls are finite verification of an implementation, not a
Lychrel witness or a proof about 196. The all-length identities below have
written proofs; they have not been formalized in Lean.

## 1. Relation to the concurrent work

The two- and four-band neutral quotient notes at external commit
`60d4348349a80c513008df9263905e7955b4ce79` provide the finite-interface and
coordinatewise-gain architecture used here. Their bands have coefficient nine
and require compatible actual carries to remain nine. The present bands have
complementary coefficients different from nine. Each resets its carry at its
first column, and both kinds of band survive as complementary bands under
every actual overflow choice.

During this work, external commit
`d528a5f96773cba3f3aee88d006ff60dc946581c` published
[`periodic_bulk_followup/METHOD_AND_PROOF.md`](../../research/main_existence_attempt/continuation_pass/periodic_bulk_followup/METHOD_AND_PROOF.md).
Its guard-period lemma treats an arbitrary repeated four-column block,
including a neutral or nonconstant phase, with one repeated exponent. Our
template instead has two independent lengths and two distinct complementary
constant phases. The common idea is to absorb boundary transients into finite
interfaces. Nonneutral constant bands permit the explicit one-column formulas
below, and their phase update does not depend on global overflow. Neither
result supplies a returned finite interface for the other. No periodic graph
or capped path search from the external work is repeated here.

The exact external periodic note read has Git blob
`5c5f94c66d6c3adb0288b610f748fcbed32b115c` and SHA-256
`45c34243ff0eef9fb30ef91e2d43ae933a77e4ca4d0b4bd307e9f0c259781559`.
Its guarded all-exponent theorem, necessary graphs and eleven capped probes
retain their stated distinct scopes. In particular, its reported probes do
not establish a nonconstant interior that survives indefinitely.

## 2. Actual whole-word semantics and the template

Words are indexed from the least significant end. Write juxtaposition for
concatenation, `rev` for reversal, and `x^g` for a constant word of length
`g`. For equal-length words, `+` means coordinatewise addition. Put
`pair(D)=D+rev(D)`.

A canonical mirrored-sum word is symmetric, has coefficients in `0,...,18`,
has a positive exterior coefficient, and has an even middle coefficient if
its length is odd. Every such word is realized by a canonical ordinary
integer: split each mirrored coefficient into digits between zero and nine,
choose a positive most significant digit at the exterior, and halve a middle
coefficient. If `q` is realized by `n`, then evaluation of `q` at ten is
exactly `T(n)=n+reverse(n)`. Let `G(q)` be the mirrored-sum word of the
canonical decimal digits of this value. These are actual whole-word maps.

Let

\[
 c\in\{1,\ldots,17\}\setminus\{9\},\qquad d=18-c,
\]

and define

\[
 Q(c;B,A,C;g,h)
 =B\,c^g\,A\,d^h\,C\,d^h\,\operatorname{rev}(A)\,
 c^g\,\operatorname{rev}(B).                 \tag{1}
\]

The source hypotheses are:

* `g,h>=2`;
* all coefficients of `B,A,C` lie in `0,...,18`;
* `C` is symmetric and has even middle coefficient when its length is odd;
* the first coefficient of `B` is positive if `B` is nonempty.

All three finite blocks may be empty. If `B` is empty the exterior is `c>0`.
If `A` is empty the unlike bands meet directly; they do not merge since
`c!=d`. If `C` is empty the two central `d` bands meet, but they remain two
equal halves parameterized by the same `h`. Thus (1) remains a precise
parameterization even when the number of maximal constant runs changes.
These hypotheses make (1) canonical for every allowed pair of lengths.

## 3. One-column resets and the bulk phase

For `x` in the phase domain set

\[
 k_x=\mathbf1_{x\ge10},\qquad t_x=x-9k_x,\qquad F(x)=2t_x.
\]

For either incoming carry `e` in `{0,1}`, the first column of a nonempty
`x` band has outgoing carry `k_x` and digit `x+e-10k_x`. Every subsequent
column has digit `t_x` and the same outgoing carry `k_x`. This follows
directly from division by ten: `x<=8` forces outgoing carry zero and
`x>=10` forces outgoing carry one. In particular, a band's outgoing carry
is independent of its positive length.

For the complementary pair,

\[
 k_c+k_d=1,\qquad t_c+t_d=9,\qquad
 F(c)+F(d)=18.                              \tag{2}
\]

The next phases `c'=F(c)` and `d'=F(d)` are positive, different from nine,
and distinct. They lie in the same phase domain. Explicit periodic orbits
are

\[
 6\longmapsto12\longmapsto6,
\]

and

\[
 2\longmapsto4\longmapsto8\longmapsto16
 \longmapsto14\longmapsto10\longmapsto2.
\]

The complementary phase traverses the same respective cycle with the
corresponding offset. No classification of all possible phase orbits is
needed below.

## 4. The actual normalization, with no freely selected carries

Let `N(W,e)=(D,f)` mean: normalize the finite coefficient block `W` with
incoming carry `e`, recording its same-length decimal digit block `D` and
final carry `f`. For an empty block, `D` is empty and `f=e`. Compute

\[
\begin{array}{lll}
 N(B,0)=(D_B,e_0), & N(A,k_c)=(D_A,e_1),
     & N(C,k_d)=(D_C,e_2),\\
 N(\operatorname{rev}(A),k_d)=(D_{RA},e_3),
     & N(\operatorname{rev}(B),k_c)=(D_{RB},\gamma).
\end{array}                                                     \tag{3}
\]

Set

\[
 u_0=c+e_0-10k_c,\quad u_1=d+e_1-10k_d,\quad
 u_2=d+e_2-10k_d,\quad u_3=c+e_3-10k_c.            \tag{4}
\]

Every `u_i` lies in `0,...,9`. The canonical digit word of the actual value
of (1) is exactly

\[
 D_B\,u_0\,t_c^{g-1}\,D_A\,u_1\,t_d^{h-1}\,
 D_C\,u_2\,t_d^{h-1}\,D_{RA}\,u_3\,t_c^{g-1}\,D_{RB}
 \,[1\text{ if }\gamma=1].                         \tag{5}
\]

Indeed, each source band resets its outgoing carry, so the five block
inputs in (3) are exactly the inputs encountered by the left-to-right
normalization of the whole source. Its last carry is the `gamma` in (3).
If it is zero the last digit remains positive because the exterior source
coefficient is positive; if it is one the appended digit is the new leading
one. Thus no leading-zero trimming changes the physical width. All block
data and `gamma` are independent of `g,h>=1`.

## 5. The raw all-gap identity

Single digits in the following formulas denote one-letter words. When
`gamma=0`, define

\[
\begin{aligned}
 B_r&=(D_B\,u_0)+(\operatorname{rev}(D_{RB})\,t_c),\\
 A_r&=(t_c\,D_A\,u_1)+(u_3\,\operatorname{rev}(D_{RA})\,t_d),\\
 C_r&=\operatorname{pair}(t_d\,D_C\,u_2).
\end{aligned}                                                    \tag{6}
\]

When `gamma=1`, define

\[
\begin{aligned}
 B_r&=(D_B\,u_0)+(1\,\operatorname{rev}(D_{RB})),\\
 A_r&=(D_A\,u_1)+(u_3\,\operatorname{rev}(D_{RA})),\\
 C_r&=\operatorname{pair}(D_C\,u_2).
\end{aligned}                                                    \tag{7}
\]

Then for every `g,h>=2`,

\[
 G(Q(c;B,A,C;g,h))
   =Q(c';B_r,A_r,C_r;g-2+\gamma,h-2+\gamma).       \tag{8}
\]

**Proof.** Add the word (5) to its reversal. Without overflow, a uniform
`t_c` run pairs with its reflected `t_c` run except for the first entrance
digit and the last column before the next interface; absorbing those two
columns gives the first two rows of (6), leaving `g-2` copies of `2t_c`.
The same calculation leaves `h-2` copies of `2t_d`. The central remaining
word and its reversal give the last row of (6). With overflow, the appended
one shifts the reflected alignment by exactly one column. The exterior
pairing is therefore `D_B u_0` against `1 rev(D_RB)`; the next interface
is `D_A u_1` against `u_3 rev(D_RA)`; and the central word is `D_C u_2`.
These are (7), and now each band retains one more uniform column. Symmetry
supplies the other half of (8). The displayed concatenations remain valid
when any finite block is empty. For gap two without overflow, a remaining
uniform run has length zero and the adjacent raw interfaces simply meet.
No identification of distinct positions is assumed. ∎

For `b=|B|,a=|A|,m=|C|`, these formulas give

\[
 |B_r|=b+1,\qquad |A_r|=a+2-\gamma,\qquad
 |C_r|=m+2-\gamma.                              \tag{9}
\]

Thus the raw gap loss is **two minus the actual overflow**. The neutral
band formula with raw gap `g-gamma` does not apply to these bands.

## 6. Trimming and an exact two-coordinate update

Use the new phases `c',d'`. Strip the maximal suffix of `c'` from `B_r`,
of length `u_B`. Strip the maximal prefix of `c'` from `A_r`, of length
`v_A`, and then the maximal suffix of `d'`, of length `u_A`. Since `c'!=d'`,
these two strips cannot overlap. Strip `v_C` paired exterior `d'` columns
from `C_r`, maximally while retaining a symmetric remainder: an even word
may become empty, but an odd word retains its middle column. Denote the
three remainders by `B',A',C'`. Put

\[
 \delta_g=u_B+v_A-2+\gamma,\qquad
 \delta_h=u_A+v_C-2+\gamma.                       \tag{10}
\]

Moving these equal coefficients into their adjacent constant bands in (8)
proves

\[
 G(Q(c;B,A,C;g,h))
   =Q(c';B',A',C';g+\delta_g,h+\delta_h).         \tag{11}
\]

The target gaps are nonnegative for all source gaps at least two, but need
not be at least two. Iterating this same lemma requires the latter domain
condition at each new source. Both deltas and the target finite blocks are
independent of source lengths. The target finite blocks retain the canonical
hypotheses: their coefficients are digit sums at most eighteen, `C'` is
symmetric with even middle coefficient, and a nonempty `B'` still has the
positive actual exterior coefficient. An empty `B'` instead exposes `c'>0`.

This defines a deterministic quotient state `(c,B,A,C)` with edge label
`(delta_g,delta_h,gamma)`. The phase is part of the state. A trimmed state
has no trailing `c` in `B`; a nonempty `A` starts differently from `c` and
ends differently from `d`; and a center of length at least two has exterior
different from `d`. Empty blocks are retained as legal states, without
introducing a new independent exponent for merged central halves.

Length conservation is exact:

\[
 2|B'|+2|A'|+|C'|+2\delta_g+2\delta_h
    =2|B|+2|A|+|C|+\gamma.                       \tag{12}
\]

It follows either by substituting (9)--(10), or by comparing the physical
widths in (11). This identity is useful for checking a returned interface,
but by itself does not ensure that either gap remains long enough.

## 7. Conditional cycle criterion and the ordinary seed

Suppose a nonempty finite directed cycle of the quotient states in section 6
is supplied. In particular its phase must return: a cycle based on `6` or
`12` has length divisible by two, and one based on the displayed six-cycle
has length divisible by six. Let `Delta_g,Delta_h` be the two total gap
increments around the cycle. Summing (12) gives

\[
 2(\Delta_g+\Delta_h)=\sum\gamma.                \tag{13}
\]

The right side is positive. Otherwise every step has no overflow. If `a_0>0`
is an actual exterior coefficient and `e` the actual carry entering its
reflected exterior, then absence of overflow implies `a_0+e<10`; the next
exterior coefficient is `2a_0+e`, strictly greater than `a_0`. The exterior
coefficient is determined by the quotient state, so it cannot return around
such a cycle. Consequently (13) implies positive total gap gain.

For infinite repetition of the **same** finite cycle the needed stronger
condition is

\[
 \Delta_g\ge0\quad\hbox{and}\quad\Delta_h\ge0.  \tag{14}
\]

A positive sum alone is insufficient: a coordinate with negative cycle gain
eventually falls below two for every finite starting gap. Under (14), let
`s_g(j),s_h(j)` be the within-cycle prefix sums, including the empty prefix.
Choosing

\[
 g\ge2-\min_j s_g(j),\qquad h\ge2-\min_j s_h(j)
\]

keeps every source gap at least two throughout every repetition. Equations
(11) and (14) then give an actual infinite orbit of canonical pair words.

Every such source is safe. It contains a positive coefficient at most eight
and a coefficient at least ten, because it retains both complementary bulk
types. It therefore belongs to neither exact palindrome-predecessor class:
it is not all at most nine, and is not a word over `{0,11}` with exterior
eleven. Equivalently, the two singleton blocks have different isolated
overflow bits, the previously proved mixed-coefficient safety criterion.
Thus the ordinary output from every source is nonpalindromic.

Realize the first pair word by any canonical ordinary integer `n_0`, and
put `n_1=T(n_0)`. The whole-word identity proves inductively that the
successive pair words are exactly those of this actual ordinary orbit.
The value `n_1` is nonpalindromic, and all its future reverse-and-add values
are nonpalindromic. **Such a supplied cycle satisfying (14) would therefore
give the finite Lychrel seed `n_1`.** We do not infer that `n_0` is
nonpalindromic: even bulk coefficients permit palindromic realizations at
time zero. The first positive output avoids this unsupported inference.

No cycle satisfying these premises is supplied here. No conclusion about
the existence of a decimal Lychrel number or about 196 follows from these
conditional statements alone.

## 8. Finite formula controls and preservation

Run `python3 check_formulas.py` in this directory. The checker covers all
sixteen nonneutral positive phases, seven outer blocks, seven intermediate
blocks, eight symmetric centers, and five pairs of gaps:
`(2,2),(2,3),(3,2),(5,7),(31,32)`. This is 6,272 block states and 31,360
ordinary-integer cases, including 13,440 overflow cases. Empty source blocks,
zero center endpoints, odd centers, minimal gaps and unequal long gaps are
included. The sample produced 504 empty target outer blocks and 490 empty
target centers; none of these cases is discarded. Both concrete phase cycles
are checked directly.

For every control the checker constructs a canonical decimal integer
realizing the source word, computes its literal reverse-and-add, and compares
its actual decimal digits and mirrored sums with (5), (8), and (11). It also
checks the physical width, output nonpalindromicity, target admissibility,
trim normal form and identity (12). Of these controls, 14,610 have both new
gaps at least two; the others remain valid single-step formula checks and
are not treated as iteratable states at those particular lengths.

All controls passed. This program is a formula audit and performs no graph,
interface-cycle or unbounded orbit search. The full 14,966,274-byte JSON
payload is preserved losslessly as `formula_controls.json.gz` (642,191 bytes).
`verification.json` records its source and compressed/decoded SHA-256 hashes,
the exact finite catalog, counts and recovery command. `check.log` records
the successful run. The finite controls support the implementation; the
proofs in sections 3--7 supply the all-gap and conditional infinite claims.
