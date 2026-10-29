# AC19 phase-10 fixed-junction endpoint obstruction

**Label: COMPUTED.** This is a complete *necessary-condition exclusion* for the specified stationary T* subcell, not a decimal all-time Lychrel certificate and not Lean-verified.

**The exact missing sublemma supplied:** for rooted phase-10 decimal p12/m9, q=14, k>=100, every fixed junction J of length 3 or 4 and every charge-zero U3 rotation fails W9 endpoint restoration after 120 genuine reverse-and-add steps, independently of the palindromic centre C. Therefore none can realize the stationary 120-step T* return at this reference width.

## Exhaustive scope and result

- B10=(2,11,1,1,11,17,14,3,9,3,0,0,12,13,16,4,9,6,6,4,6,4,8,14,12,16,12,8,17,5,6,5,9,16); W10=(0,9,11,1,10,8,5,9,16).
- U is all 30 distinct rotations of (9,a,18-a), a=0,2,...,18. J ranges over all 19^3+19^4=137,180 words, including zeroes and coefficients 18. Thus there are exactly **4,115,400** different J/U cases.
- **4,115,400 / 4,115,400 examined; 0 endpoint-W9 restorations, 0 unknowns, 0 incorrect 30-overflow clocks.** Both odd/even and arbitrary long palindromic C are covered without enumeration.
- First endpoint mismatches (absolute LSD index): 135:1,671,590; 136:516,263; 138:1,562,920; 139:193,807; 140:84,543; 141:70,986; 142:9,294; 143:4,841; 144:430; 145:597; 147:115; 148:4; 149:8; 150:2. Sum=4,115,400. Every mismatch is before the 160-coefficient B10 W10^14 endpoint cut.
- The scan is **endpoint-only**: there is no strict-per-phase W9 pruning and no mod-11 pruning of even C.

## Sound two-ended carry-cone argument

Let P be any palindromic pairword with first and last L coefficients known; normalizing P (the actual digit vector of N+rev(N)) gives a *known* low L-digit segment, and the carry entering the high L-digit segment may only be 0 or 1. For any coefficient x in 0..18, the carry leaving x is independent of its entering carry exactly when x!=9. Let r be the number of initial 9s of the high segment as encountered from its inner boundary. Both incoming carry cases then agree on all high digits after the first non-9, and on the final overflow bit gamma. Pairing low and high digits (with the one-column shift if gamma=1) therefore determines the first L-r-1+gamma coefficients of the *next* palindromic pairword, irrespective of the unknown middle. Induct this exact inclusion for 120 steps; no radius approximation or intermediate W9 restriction is used.

The initial known symmetric prefix is B10 W10^14 J U^44 (a prefix for every k>=100). If the cone becomes too short to decide the entire 160-coefficient endpoint W9 prefix, the checker retries with the longer known U^100 collar. All cases are decided; an excluded candidate has a concrete mismatch at or before coefficient 150. The proof is unconditional over valid palindromic centres, because neither cone assumes their values. The reference-width condition q=14 is essential; extension via the existing T12 cut/insertion theorem requires checking its premises separately.

## Reproduction and independent checks

```sh
c++ -O3 -std=c++17 calculation/new_structures/AC19/scan.cpp -o /tmp/ac19_scan
/tmp/ac19_scan 4115400 0 1
python3 calculation/new_structures/AC19/verify_bigint.py
```

The full scan was partitioned into five disjoint blocks of 823,080 J/U cases; the counts and histograms add exactly to 4,115,400. An independent Python big-integer engine and separate non-in-place schoolbook digit-array engine agree at every one of the 120 steps for physical controls with q=14/20/40/80/160, k=100/80/160/320/640 and both C parities. Another 7,500 arbitrary pairword/carry-cone property comparisons and 300 Python/C++ candidate histograms agreed locally.

**BREAK of AB19's PARTIAL diagnostic:** for q14/k100 J=(1,2,3), U=(9,0,18), C=(4,14,4), the true first mismatch is 138, not coefficient 10; coefficient 10 stays zero. This discrepancy was posted to issue #476. No fixed-seam all-time certificate is claimed.