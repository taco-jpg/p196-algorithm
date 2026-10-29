# AC05: rooted p12/m9 centre-only U-group 4 census

**Labels:** COMPUTED (exact complete/reference-width enumerations); PAPER PROOF (conditional application of published T12 cut/cone theorem); UNDECIDED (base-10 all-time Lychrel existence).

**One-sentence missing lemma supplied:** For all three U-group-4 rotations and every palindromic coefficient centre C of length 7–10, the 120-step centre interface cannot reproduce itself at phase 0 for any fixed finite J and independently large q>=14,k>=100, because a protected radius-5 or radius-6 centre window fails after genuine decimal reverse-and-add.

## Precisely decided predicate

LSD-first coefficients of the physical rooted p12/m9 template are `H ++ C ++ reverse(H)`, `H=B34 ++ W9^q ++ J ++ U^k`. B34 and W9 are published row zero in `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`, q=14,k=100, J=[5], U among `(9,8,10), (8,10,9), (10,9,8)`. Centre C is a palindromic word over 0..18 with even midpoint when its length is odd. The source is realized as canonical decimal digits and the endpoint is computed after 120 *genuine* reverse-and-add steps, with true overflow clock `(1000)^30`. The target is identical except k increases from 100 to 105.

**Exact unpruned enumeration L7–10:** the per-U counts at lengths 7/8/9/10 are respectively 68,590 / 130,321 / 1,303,210 / 2,476,099. Across all three U, 11,934,660 separate full-width central-radius-160 comparisons have **zero** successes. No intermediate strict-phase W9 condition, odd-centre modulus gate, heuristic pruning or sampled extrapolation was used in this enumeration. Exact physical clock and full original-source realization are checked.

**Stronger junction-independent test:** all 11,934,660 centres were separately enumerated against only the radius-five centre predicate. At lengths 7,8,10 there are zero matches (205,770 / 390,963 / 7,428,297). At length 9 there is exactly **one** radius-five match among 3,909,630 centres: U=(10,9,8), C=(2,1,13,4,2,4,13,1,2), base-19 index 321501. It FAILS at radius six, offset -6 (actual pair coefficient 5, required 9). Independent Python unbounded-integer replays reproduce the precise radius-five near miss and radius-six failure for q/k=(14,100),(20,80),(40,160),(80,320),(160,640), for multiple distinct J. Thus **all C length 7–10 fail a radius<=6 centre test**.

The published T12 PAPER PROOF gives at most 152 junction-side and 122 centre-side propagated coefficients through 120 steps. Their sum 274 is strictly smaller than U^100 width 300, and radius six is strictly inside the centre-side protected collar. Hence the radius-five/six failure is independent of all finite J. T12's paired-insertion theorem lifts each reference-width failure to all independent q>=14,k>=100. This is an all-width, **one-epoch negative sublemma**, not an all-time Lychrel certificate and not an exclusion of changing centres or mobile seams.

## Odd-length 11 extension, restricted scope

For J=[5], each U's 24,760,990 palindromic 11-coefficient centres was accounted for using a SOUND *centre-only* mod-11 necessary filter. After the first physical overflow, the even-digit step makes N divisible by 11, and all later ordinary reverse-add steps preserve that. For odd-length final pairwords `A(P_120)=0 (mod 11)`, `A(X)=sum((-1)^i X[i])`. T12 fixes the outgoing coefficients **outside** a centre collar of radius 152+|C|. Comparing the baseline C=0 full physical endpoint and the target inside the same collar gives necessary `A(C)=A(U) (mod11)`, namely residues 0,7,9 for U0,U1,U2. Only odd C is pruned; no even centre is pruned by this gate. An initial *full-template-only* modulus gate was discarded as UNSOUND for the centre-only predicate.

The exact surviving counts are (2,251,022; 2,251,022; 2,251,028), with 67,529,898 excluded by the proved residue condition and 6,753,072 candidates fully physically evaluated. **Zero** restores the radius-170 centre window, and zero switched from the fast port checker to its full-engine fallback. The radius-170 window is wider than the 163 protected centre radius; explicit baseline computations confirm the intervening ring already agrees independently of C at q14/k100. This is an EXHAUSTED-NONE cell for the **fixed J=[5] radius-170 central-window predicate**, not an all-J theorem and not a substitute for the known Q39 odd-centre full-return gate.

**Lengths 12–14:** PARTIAL, exactly 20,000 base-19 candidates per U and length, i.e. 180,000 distinct fixed-J central-window radius-160 tests in total, with zero matches. No exhaustive/no-go conclusion is claimed for those lengths. The full search spaces are 3*19^6, 3*10*19^6, 3*19^7 respectively.

## Sound engine and independent checks

`census.cpp` uses exact original LSD-first decimal digits, never modifies a source digit in place during addition. Its optional port accelerator retains both symmetric carry inlets and outflows and true digit length/clock at **every** of 120 steps; any carry-port discrepancy or non-baseline abandoned digit invokes full decimal replay. The emitted `first_offset_hist=UNREPORTED_FAST` intentionally avoids misleading pseudo-offset histograms from an accelerated path. There is no strict-per-phase W9 pruning.

Independent checks: 5,760 single-width and 2,400 multiwidth full-vs-port C++ controls (0 mismatches, 0 fallbacks); 120 Python arbitrary-precision vs independent decimal-array whole trajectories over five q/k scales (14,400 exact step agreements and exact 120-bit clocks); 240 independent outside-centre cone controls; 864 true-bigint controls comparing four other junction words to J=[5] in the central 10-pairword collar; and independent bigint replays of the sole radius-five near miss.

Reproduce (from repository root):

```sh
g++ -O3 -std=c++17 calculation/new_structures/AC05/census.cpp -o /tmp/ac05-centre
for L in 7 8 9 10; do for u in 0 1 2; do /tmp/ac05-centre "$u" "$L" 0 0 14 100 5 1 0; done; done
for u in 0 1 2; do /tmp/ac05-centre "$u" 11 0 0 14 100 170 1 1; done
g++ -O3 -std=c++17 calculation/new_structures/AC05/crosscheck.cpp -o /tmp/ac05-cross && /tmp/ac05-cross
g++ -O3 -std=c++17 calculation/new_structures/AC05/crosscheck_widths.cpp -o /tmp/ac05-widths && /tmp/ac05-widths
python3 calculation/new_structures/AC05/independent_check.py
python3 calculation/new_structures/AC05/j_independence.py
python3 calculation/new_structures/AC05/cone_check.py
```

No decimal certificate, invariant repair, 240-step closed endpoint cycle, or Lean-verified proof is claimed. This subcase redirects centre search to length>=12, odd/even parity-aware conditions, moving centres and genuine repair dynamics, rather than repeating already excluded small fixed centres.
