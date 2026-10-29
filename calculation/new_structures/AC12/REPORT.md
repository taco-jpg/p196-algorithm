# AC12: phase-3 rooted p12/m9 short-junction endpoint census

**Label: COMPUTED.** Scoped decision, not a base-10 Lychrel certificate.

**Exact missing-lemma subcase supplied:** For the published phase-3 B3/W3 and each of 30 U3 rotations, no stationary fixed junction of coefficient length 3 or 4 restores the W9 prefix at the T12 reference width after 120 genuine decimal reverse-and-add steps. Consequently none supplies the exact stationary template return T(q,k)→T(q,k+5). This rules out this narrow finite branch, not moving seams, other phases, or arbitrary J lengths.

**Predicate.** H = B3 ++ W3^14 ++ J ++ U^100, P=H ++ C ++ reverse(H), where J in {0,...,18}^n and n=3 or 4, U ranges over all rotations of (9,a,18-a), a=0,2,...,18, and C is either [4,14,4] (odd) or [4,4] (even). After exactly 120 physical decimal n+reverse10(n) steps, require the first 34+9·14=160 pair coefficients to equal B3 ++ W3^14; that is necessary for a literal endpoint return to the same J,C with U^(100+5). No strict-per-phase W9 pruning is used.

**Exhaustive results:**
- J3: **411,540/411,540** = 19^3×30×2 cases, W9-prefix survivors **0**, full returns **0**, length errors **0**, overflow-count errors **0**. First-mismatch offsets from W9 cut 160: -26:3468, -25:21762, -24:49156, -23:181264, -22:108834, -21:26750, -20:16706, -19:1730, -18:1544, -17:42, -16:234, -15:20, -14:14, -13:14, -12:2. Histogram sum 411,540.
- J4: **7,819,260/7,819,260** = 19^4×30×2 cases, W9-prefix survivors **0**, full returns **0**, length errors **0**, overflow-count errors **0**. Mismatch offsets: -26:68478, -25:414870, -24:944542, -23:3428816, -22:2067800, -21:507604, -20:319902, -19:32032, -18:29648, -17:502, -16:4180, -15:326, -14:302, -13:224, -12:24, -11:6, -9:4. Histogram sum 7,819,260.
- **Total 8,230,800/8,230,800, zero restorations.** The J4 search used disjoint base-19 code ranges [0,26065), [26065,52130), [52130,78195), [78195,104260), [104260,130321).

**Proof boundary and carry soundness.** The C++ engine first normalizes the symmetric pair coefficients using the genuine decimal carry, including overflow, then forms the next pairword from the resulting digit array. It does not overwrite reflected input digits in place. Phase3 has actual overflow clock (0100)^30, yielding 30 extra digits. B3[0]=5 is physically realizable with low digit 0 and leading high digit 5; every allowed input pair coefficient is in 0..18 and the odd centre has an even midpoint. Python arbitrary-precision n+reverse10(n), independent schoolbook digit normalization and folded-pair arithmetic were cross-checked at each of 120 steps for examples of J3/J4, U rotations and C parities at widths (q,k)=(14,100),(20,80),(40,160),(80,320),(160,640). These are controls only; they do not replace a proof of all-width pumping.

The previously published T12 paired-insertion/reset-cone analysis bounds U3 junction-side erosion by 152 and centre-side erosion by 122: k=100 leaves 300-152-122=26 protected U cells. Hence the W9-prefix obstruction is centre-independent under the rooted phase-3 clock hypotheses. T12's insertion reduction links the physical reference-width necessary-condition failure to the absence of an **all-width fixed-J** return. The result makes no claim for J>=5, q-changing edges, growing seams, or the decimal Lychrel existence question.

**Reproduce** from repository root:

```sh
g++ -O3 -std=c++17 calculation/new_structures/AC12/census.cpp -o /tmp/ac12
/tmp/ac12 3 0 6859
/tmp/ac12 4 0 130321
```

For the independently executed decimal checks, see the AC12 coordination record and committed C++ carry engine; an additional Python source may be attached separately due heavy concurrent main updates.

**Status: one exact short-junction obstruction, no all-time decimal certificate.**
