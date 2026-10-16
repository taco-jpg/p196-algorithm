# Exact finite-wall renewals and the limits of their continuation

No finite decimal Lychrel witness or all-time closure is established here.
The positive results below are algebraic identities valid for every indicated
integer parameter. The searches and literal integer tests are independent,
bounded implementation controls, not evidence extrapolated to infinite time.
All words are written from low to high decimal column. A superscript on a
word denotes repetition; juxtaposition denotes concatenation.

The notation `Delta_C(W)` is the finite difference construction in
`astra_moving_boundary_notes.md`. A valid pair-sum word `q` is *balanced at C*
when every residue-class sum modulo C is 18. Its total coefficient sum is
18C. At an ordering failure with E missing carries the only possible new
balanced parameter is C+E.

## 1. An unbounded family of safe alternating-hole renewals

For any integer m>=1 put

    C = 4m+2,
    W_m = (10,8)^m · 0 · (2,7)^m · 9 · (11,16)^m · 18 · (10,8)^m.

This is an anti-complement wall of width 8m+3. Its finite difference is

    H_m = (10,8)^m · 0 · (2,7)^m · 9 · (1,8)^m,
    q_m = H_m · 18 · reverse(H_m),                     (1)

of length 12m+5. To verify the difference formula directly, the first C
positions are unchanged. In the overlap the paired blocks subtract as
(11,16)-(10,8)=(1,8), 18-0=18, and (10,8)-(2,7)=(8,1).
The remaining tail is 18 minus the corresponding final wall segment.
All coefficients in (1) belong to 0,...,18, its center is even, and its outer
coefficient is 10. Thus it is a valid finite decimal pair-sum word.

The actual carry positions (columns whose outgoing carry is one) are

    {0,2,...,2m-2},
    {6m+2},
    {12m+4,12m+2,...,10m+6}.                         (2)

Each 10 in the outer (10,8) blocks creates a carry, the following 8 kills
it, and the central18 creates the only other carry. The blocks between
these positions have no other carries. Modulo C, (2) lists every even
residue exactly once and no odd residue. Therefore the missing-carry word
is exactly 0101...01, E=2m+1=C/2, and

    D = C+E = 6m+3 = 3C/2.                          (3)

Here is also the complete output digit word, split into two equal halves:

    A_m = (0,9)^m · 0 · (2,7)^m · 9 · (1,8)^m · 8,
    B_m = (9,1) · (8,1)^(m-1) · 9 · (7,2)^m
          · (0,8,0) · (9,0)^(m-1) · 1.

Ordinary decimal carrying gives d=A_m B_m. Both halves have length D.
Adding A_m to reverse(B_m) column by column gives exactly

    V_m = 1 · 9^(2m-1) · (8,2) · 9^(2m-1)
          · (16,10) · 9^(2m-1) · 17.               (4)

Thus the next pair-sum word is

    q'_m = V_m reverse(V_m) = Delta_D(V_m).        (5)

The wall V_m has width D, is anti-complementary, and has no remaining18
reservoir. Equations (1)-(5) prove the safe renewal for every m, without a
finite-range extrapolation. The output ends in decimal0 and begins in1,
so it is visibly not a palindrome.

This supplies safe balanced renewals of arbitrarily large old and new
parameter. It does not imply an infinite orbit preserving balance.
In particular, this family's D=6m+3 is odd; it is outside the even-C domain
of another alternating-hole renewal. More generally, an uninterrupted
sequence of parameter changes C -> 3C/2 from a fixed positive integer C
cannot be infinite: every such change consumes one factor of2.

The exact subsequent evolution and loss of balance of V_m are treated in
`wall_renewal_notes.md`. Its symbolic block calculation proves eight
ordered steps, followed by a ninth safe failure that does not rebalance.
For m>=2 the candidate new parameter is D+1, and residue1 of the resulting
q has sum12+3=15. For m=1 the candidate parameter is D+2, and the singleton
center residue has coefficient16. Neither is18.

## 2. A second all-length renewal and exact failure of its renewed phase

For k>=0 let

    A_k = (5,4) · 9^k · (14,13),   C=k+3.

Then

    Delta_C(A_k) = (5,4) · 9^k · (14,8,14) · 9^k · (4,5).

Carrying gives the low digit word

    (5,4) · 9^k · (4,9,4) · 0^k · (5,5).

Its mirrored pair sums are

    (10) · 9^(k+1) · (8,18,8) · 9^(k+1) · (10),

which is Delta_(k+4)((10) · 9^(k+1) · (8)). This is one safe renewal,
with E=1. The input has two asymmetric output columns, so the resulting
number is not a palindrome.

Put D=k+4. The following exact wall states all retain this same D:

| Step from A_k | Wall |
|---|---|
| 1 | 10 · 9^(k+1) · 8 |
| 2 | 1 · 0 · 9^k · 18 · 17 |
| 3 | 2 · 1 · 9^k · 17 · 16 |
| 4 | 4 · 3 · 9^k · 15 · 14 |
| 5 | 8 · 7 · 9^k · 11 · 10 |
| 6 | 16 · 15 · 9^k · 3 · 2 |
| 7, k>=1 | 7 · 13 · 5 · 9^(k-1) · 13 · 5 · 11 |
| 7, k=0 | 7 · 13 · 9 · 5 · 11 |

These entries follow by carrying each constant9 block. A9 block preserves
its incoming carry and emits respectively all9 or all0. In steps2-6 the
remaining four boundary entries update as

    (a,a-1,19-a,18-a) -> (2a,2a-1,19-2a,18-2a)

for a=1,2,4,8. The next overflowing step splits the two sides of the9 block
as displayed in the final row. These are finite symbolic carry identities,
valid for all k>=1; k=0 has its separately displayed empty-block case.

The eighth update has the exact pair-sum word

    (15,6,12) · 9^(k-1) · (6,11,8,11,6) · 9^(k-1) · (12,6,15)

for k>=1, and (15,6,9,11,8,11,9,6,15) for k=0. Its total coefficient
sum is18(k+5), so exactly one carry is missing. Its output length is
2(k+5)-1 and its central coefficient is8. Balance at
the only candidate modulus k+5 would require that singleton central
residue to equal18. It therefore fails for every k. The output remains
nonpalindromic: the previous digit sum was9(k+4), and it rises by only9,
so neither palindrome-predecessor digit-sum ratio (2 or4/11) is possible.

At that failure the heterogeneous residue budgets, for k>=2, are exactly

    (26,12,21) · 18^(k-2) · (21,12,26,8).            (6)

They sum to18(k+5). Formula (6) identifies a finite set of budget defects,
but several budgets exceed18. It consequently does not fit the original
0/18 wall model and supplies no renewed closure. The exceptional small
budgets are (26,15,15,26,8) for k=0 and (26,12,24,12,26,8) for k=1.

The two-event examples discovered below are central9 lifts of

    (1,6,4) · 9^k · (14,12,17), C=k+3.

Its first update renews at C+1; one ordered step then produces A_(k+1),
which performs the second renewal above. This explains two events but
does not evade the later all-k obstruction.

## 3. Exact scope of exhaustive finite searches

`renewal_search_scan.py` enumerates every anti-complement wall with
half-width<=3 (width<=7), and C=1,...,|W|+2. It finds 62,090 valid
finite differences and11,517 ordering failures:

| Failure outcome | Count |
|---|---:|
| Safe and balanced at C+E | 37 |
| Palindromic and balanced at C+E | 442 |
| Safe and not balanced at C+E | 8,783 |
| Palindromic and not balanced at C+E | 2,255 |

`renewal_search_half4.py` adds every wall of widths8 and9 and C=1,...,|W|.
Larger C cannot be an ordering failure, by the positive-reservoir theorem.
This adds673,158 valid differences,227,920 ordering failures, and465 safe
one-step rebalances. Thus all wall widths<=9 yield502 safe rebalancing
seeds in total, with no omitted larger-C failures.

For these502 seeds, after the first renewal and before the first loss of
balance or first palindrome:

| Outcome | Number of seeds |
|---|---:|
| One renewal, then loss of balance | 377 |
| One renewal, then palindrome | 121 |
| Two renewals, then loss of balance | 4 |

All terminate that balanced phase within17 updates of the original seed;
no case hits the120-step cap. The four two-event seeds are k=0,1,2,3
of the displayed two-event family. This excludes a third such event for
those exact finite seeds only. It does not exclude other walls.

A separate250-step cap for each of those502 seeds, allowing unbalanced
intervals, finds38 seeds with one delayed balanced return each. Among all
502 runs,195 encounter a palindrome and307 reach the cap. Reaching the cap
is not an all-time safety claim. No extra increase in C at a balanced step
is found after these delayed returns.

The empty-wall controls C=1,...,64 were also followed for at most300 steps.
Their only balanced return after an increase/loss within that cap is the
palindromic C=1 return. No assertion outside those finite bounds is made.

## 4. Bounded SMT searches and independent controls

The linear integer SMT encoding uses ordinary decimal carry bits and
explicit symmetric pair-sum words. Every returned witness is replayed by
the separate q-step implementation and wall reconstruction.

- `renewal_search_smt.py` attempted three consecutive +1 renewals. It
  stopped after about49 seconds:194 UNSAT answers,52 UNKNOWN answers,
  no witness. This is a partial scan, and no entire width range is claimed
  excluded; UNKNOWN is not UNSAT. The recorded cutoff is in the result.
- `renewal_search_alt_smt.py` found the first C=4 ->6 alternating-hole
  example at pair-sum width15 and overflow1. Its old wall width11 explains
  why it is absent from the exhaustive width<=9 search.
- `renewal_search_alt_minima.py` found alternating-hole witnesses for
  C=4,6,8,10,12,14,16, with first found widths15,17,27,29,39,41,51.
  These widths are certified minimal within the scanned branches except
  C=16: UNKNOWN occurred at (L,h,phase)=(47,1,0) and(50,0,1).
  For C=2, all four (overflow,phase) choices at L=2,...,16 returned UNSAT;
  no larger-width exclusion is claimed.
- `renewal_search_alt_pattern.py` fixes a simple carry-support pattern;
  it led to the all-m formula in section1. The formula's validity rests
  on the block calculation above, not on the solver's first ten examples.
- `renewal_search_family_check.py` checks section1 at m=1,...,64 by literal
  integer reversal and addition, including the complete output digit word,
  hole pattern, and returned wall. It also checks all eight transitions
  of section2 at k=0,...,64 (520 transitions).

All scripts resolve the original checker relative to the archive root,
with a fallback to `research/` for the active workspace. Run, for example:

    python continuation/renewal_search_family_check.py
    python continuation/renewal_search_scan.py
    python continuation/renewal_search_half4.py

The algebra here supplies several exact finite return maps. It supplies
no nonempty family preserved by those maps for all time and no particular
finite seed with an infinite nonpalindromic orbit.
