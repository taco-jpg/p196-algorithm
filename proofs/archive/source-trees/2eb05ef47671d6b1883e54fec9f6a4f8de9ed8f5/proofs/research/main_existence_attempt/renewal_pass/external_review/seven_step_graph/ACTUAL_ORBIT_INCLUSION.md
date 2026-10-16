# Actual-orbit inclusion in the six-coefficient phase graph

This note supplies the all-width mathematical bridge for the companion
graph and rank certificate. It applies to every canonical whole pair word
of width **L>=6**, including widths 6 through 11 where the two observed
six-column regions overlap. The graph is a necessary model of actual
orbits; arbitrary graph states or control choices need not be realizable.

## Exact six-coefficient update

Let `q_0,...,q_(L-1)` be a canonical whole pair word: its coefficients are
in 0,...,18, it is symmetric, its outside coefficient is positive, and its
center coefficient is even when L is odd. Set `p_i=q_i` for 0<=i<6.
These are the first six coefficients of the **full** symmetric word;
they need not be six distinct noncentral folded pairs.

Let a_i be the actual whole-word carry entering column i, with a_0=0.
For 0<=i<L, the ordinary normalized digit and next carry are

`d_i=(q_i+a_i) mod 10`, `a_(i+1)=floor((q_i+a_i)/10)`.

Every a_i is 0 or 1. Put e=a_L. Canonical outside positivity gives the
actual normalized width `W=L+e`: if e=1 the new leading digit is d_L=1;
if e=0 the digit at L-1 is positive. In either case W>=6.

Normalize `(p_0,...,p_5)` from incoming carry zero, retaining six digits
`ell_0,...,ell_5`. This is the restriction of the actual normalization to
columns 0,...,5, so `ell_i=d_i`.

Now set **beta=a_(L-6)**, the actual carry entering the last six original
columns. Whole-word symmetry gives, for every 0<=j<6,

`q_(L-6+j)=q_(5-j)=p_(5-j)`.

Normalize `(p_5,...,p_0)` from incoming beta, retaining six digits
`v_0,...,v_5` and a final carry. Induction along these six actual columns
shows that `v_j=d_(L-6+j)` and that this final carry is precisely e.

The next whole pair word is `q'_i=d_i+d_(W-1-i)`. Substitution gives its
first six coefficients exactly:

\[
p'_i=\ell_i+v_{5-i}\quad(0\le i<6),\qquad e=0;
\]

\[
p'_0=\ell_0+1,\qquad
p'_i=\ell_i+v_{6-i}\quad(1\le i<6),\qquad e=1.
\]

Every index used here is valid. In the overflowing case the reflected
column for i=0 is the new leading column L; for 1<=i<6 it is L-i, which
lies among the last six original columns. In the nonoverflowing case it
is L-1-i, also among those columns. These formulas are exactly the
`boundary` relation in `build_graph.py`.

### Why overlap causes no omission

The two six-column calculations are restrictions of **one actual carry
history**, not two independently chosen normalizations. When L<12 their
overlap imposes additional compatibility conditions on p and beta, but
both restrictions still give the same actual digits at every shared index.
Nothing in the derivation requires disjoint regions.

For example, at L=6 beta=a_0=0 is forced. The graph also tests beta=1;
that additional control is unrealizable at this width but cannot remove
the actual beta=0 transition. The same principle handles all overlaps
at widths 7,...,11. Center parity and other short-width restrictions may
exclude further graph states or edges. Omitting those restrictions enlarges
the necessary graph, which is sound for an impossibility proof.

The control beta must not be confused with the earlier three-column
control `c=a_(L-3)`. The latter equals the carry after the first three
columns of the upper-six normalization. Neither control is freely chosen
along a given actual orbit.

## Inclusion in the phase graph

Let the prescribed first-three-coefficient tuples be

```
P0=(4,4,0)    P1=(8,8,0)    P2=(16,16,0)
P3=(7,14,7)   P4=(15,8,15)  P5=(6,14,14)
P6=(13,9,9).
```

A vertex consists of a phase k in {0,...,6} and a six-coefficient prefix
`p=P_k ++ (u,v,w)`, where u,v,w independently range over 0,...,18.
There are exactly `7*19^3=48,013` vertices. For each vertex and each bit
beta, use the exact formula above to compute p'. Retain the labeled edge
to phase k+1 modulo seven exactly when `p'[0:3]=P_(k+1 mod 7)`.
No separate assumption about the unobserved interior is imposed.

Suppose a canonical actual orbit follows the prescribed phase prefixes
for N updates. Its widths never decrease and remain at least six. At
each time choose the vertex given by its actual first six coefficients
and the label `beta_t=carry(Q_t,L_t-6)`. The update identity proves that
the corresponding graph edge exists and lands at the next actual vertex.
Induction supplies a graph path of N edges. This is the required universal
actual-orbit inclusion; no converse realization claim is needed.

## From the rank certificate to at most three consecutive returns

The exact three-column boundary theorem in the external
`SEVEN_STEP_RESET.md` states that a start with first three coefficients
P0 returns to P0 after seven updates if and only if its actual three-column
carry controls have pattern `00*0*01`. On every such return its intermediate
first-three prefixes are precisely P0,...,P6,P0, and its actual overflow
word is `0010101`.

This endpoint iff is also independently reconstructed in the local
certificate. The generator retains all 128 three-prefix control traces;
the verifier recomputes them by integer evaluation and decimal digit
extraction, checks exactly four returning controls, and checks the complete
phase and overflow traces on each return. The argument below therefore
uses the independently checked local classification, rather than relying
only on the external report.

The displayed reset-family presentation there uses a nonempty padded
middle, hence L>=7. The same boundary formula and its 128-control
classification apply at L=6 as well: the lower and upper three-column
regions are then adjacent and disjoint, and the upper incoming carry is
still its actual whole carry. The external actual-boundary formalization's
reported theorem already states the L>=6 scope. No nonempty-middle
assumption is needed for the boundary implication used here.

Now suppose returns occur consecutively at times **7,14,21,28**, starting
from an actual P0 word of width at least six. Apply that seven-step iff at
times 0,7,14,21. Each segment must follow the prescribed intermediate
phases. Their concatenation therefore gives, by the inclusion proved above,
a graph path of 28 edges starting at phase zero.

The companion `graph_verification.json` reports independent reconstruction
of all 96,026 labeled controls, all 61,731 accepted labeled edges, every
rank inequality and all 48,013 exact rank recurrences. Its rank is a
nonnegative integer strictly decreasing along every retained edge, and its
maximum over phase-zero vertices is **26**. Any graph path beginning at
phase zero consequently has length at most 26. The required length 28 is
impossible. Thus there can be **at most three consecutive seven-step
returns** of P0 from any such actual starting word.

The boundary iff is essential here: the graph alone excludes prolonged
following of the displayed phases. The iff additionally forces those
intermediate phases from the four asserted endpoint returns. Without that
implication, a missing graph path would not by itself exclude an orbit
that departed from the phases and then returned at an endpoint.

The supplied seed **4401198500000** attains three safe returns, at times
7,14,21. The separate literal-integer checker retains all its states
through time 28: every positive output through 28 is nonpalindromic, it
follows the prescribed phases for 26 transitions, and its first deviation
is state 27. Thus this actual example attains both the three-return bound
and the phase-zero path-length bound; leaving the clock demonstrably need
not coincide with a palindrome.

## Scope and provenance

The graph/rank data were reconstructed locally from the boundary formula,
independently of the announced external graph implementation. The decoded
certificate SHA256 is
`05ada1d9d603a8dbae59d4d2500b9b31018094362405b0ab1dda28afdb52b642`.
The external obstruction announcement is commit
`8a42fe14262fee12ce1c8b40bf25e97b94044742`; the exact boundary and middle
formulas are in its seven-step reset report. This note independently
reviews the mathematical bridge and its overlap cases. The finite graph
rank is checked by the companion executable verifier, not by a new Lean
kernel rank proof.

No palindrome-safety assumption was used in the exclusion: it concerns
this particular prefix-return clock. Leaving the clock does **not** imply
a palindrome. A different clock, a variable return time, later re-entry,
or a different invariant language remains possible. This argument neither
excludes all carry clocks nor settles decimal Lychrel existence or 196.

Reproduce from this directory:

```sh
python3 -B build_graph.py
python3 -B verify_graph.py
python3 -B check_sharp_example.py
```

The source review found no scope mismatch between these programs and the
necessary relation above. The verifier checks all accepted and rejected
controls and every exact rank recurrence without importing the generator;
the example checker uses ordinary integer reversal and addition directly.
