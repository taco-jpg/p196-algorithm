# Exact finite-support collision transfer for the decimal period-12 lattice

**PAPER PROOF.** This is a finite, exhaustive carry-state classification for **one reverse-and-add step only**. It completes the local first-defect gate analysis for the nine no-overflow temporal phases of the published p=12, m=9 lattice. It gives explicit families of distinct *ordinary decimal numbers* whose next numbers have the same **palindromic coefficient/pair word**. The next numbers themselves need not be equal; their subsequent steps need not be periodic. No base-10 infinite nonpalindromic orbit or certificate is claimed.

## Setting and exact finite reduction

Use the 12 temporal rows and carries of `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`, with base 10, exterior width 34, spatial period 9, and overflow word `100010001000`. A *bulk-supported perturbation* replaces finitely many coefficients at sites `i` and `n-1-i` in a symmetric pair-coefficient word P, changing nothing in the exterior or in the centre. Every changed lower-half position, and at least two further unchanged positions before the centre, lie in the established periodic bulk. The corresponding original and modified coefficient words are admissible (entries 0..18, odd centre even); both are assumed to have terminal carry zero, as P does in the nine `gam=0` phases. Repeated lengthening of the unmodified bulk is allowed, subject only to these margin conditions.

At one mirrored pair of bulk positions `i` and `i'=n-1-i`, write `q=P_i=P_i'`, and let `s` be the pair of NORMALIZED digits, `s=O_i+O_i'`, for the baseline. Scan from exterior toward the centre. The modified incoming carry at the lower position is `a`, while `b` is its outgoing carry at the upper mirrored position, that is the modified carry **into `i'+1`**. Choose the replacement coefficient `x` in 0..18 and an incoming upper carry `u` in {0,1}. The exact two-sided normalized digit equations are

```
b = floor((x+u)/10),                 (upper outgoing carry is already fixed)
(x+a) mod 10 + (x+u) mod 10 = s,     (next pair word unchanged)
a_next = floor((x+a)/10),             (lower outgoing carry)
b_next = u.                         (upper incoming becomes next cut value)
```

Thus the directed transfer state at the next bulk site is `(r+1 mod 9,a_next,b_next)` when the present residue is `r=(i-34) mod 9`. There are exactly `9*2*2=36` possible states; every choice of coefficient x and upper incoming carry u is explicitly enumerated. No SAT, time, or state cap is imposed. The time phase t is fixed because this is a *single step*, not a temporal centre-cycle search.

For each start residue r, the two entering cut carries equal the baseline carries. At the **first** site require `x != q`; after that allow all x, including q. Accept when BOTH cut carries return to the baseline values at the next bulk site. A path that accepts before reaching the centre gives a symmetric finite-support replacement, with the unchanged exterior and centre, because the two carry chains match the baseline at both cuts. Conversely, any finite-support perturbation sufficiently separated from the centre must eventually restore both cut carries: coefficient rows contain at most one consecutive 9, so after two consecutive unchanged positions each carry resets to the baseline. Its sequence of sites therefore gives a path in this exact 36-state graph and an accepting return. The first-defect restriction and the equality of all normalized pair sums are built into the edges. This proves completeness for precisely the stated bulk-supported class at **every width**.

The baseline triples `(q,s,lower incoming carry,upper outgoing carry)` repeat with period 9 once the site is beyond the exterior and away from the centre. Non-9 symbols reset carries. The reproducer independently checks this periodicity against fully normalized words at lengths 400,401,418,419,490,491 (including odd centres), at all nine residues and three successive repetitions. The logical reduction uses carry reset and the actual row values, not extrapolation from these lengths.

## Complete decision and explicit witnesses

Temporal phase t | First lower residue r admitting a finite bulk-supported collision | Minimum replacement span
:--:|:--:|:--:
1 | 7 | 7
2 | 7 | 7
3 | none | none
5 | 4 | 7
6 | 4 | 7
7 | none | none
9 | 1 | 7
10 | 1 | 7
11 | none | none

No other start residue in those phases has an accepting path. In particular, for each of phases 1,2,5,6,9,10, the **other** candidate gate from `Agent5Gamma0FirstDefectGate` does not extend to any centre-separated finite-support collision of arbitrary width. This is a genuine extension of the prior single-site response and first-defect necessary-gate results, not another finite-width SAT slice. The result does **not** claim that the displayed shortest replacement is the unique longer word at the viable residue.

There are only two spatial replacement motifs, repeated after the indicated temporal phase shifts:

```
t=1,5,9:  baseline [4,5,10,14,13,12,9]
          replace  [9,5, 0,15, 3,12,14]    delta [+5,0,-10,+1,-10,0,+5]

t=2,6,10: baseline [9,11,1,10,8,5,9]
          replace  [14,10,11,9,18,5,4]     delta [+5,-1,+10,-1,+10,0,-5]
```

For each phase, place its seven coefficients at any lower-half bulk index with the indicated residue (and the same seven coefficients at the reflected upper-half sites). All other coefficients are unchanged. The transfer equations guarantee the complete next pairword is identical for any sufficiently large compatible length. The available translation by 9 positions produces infinitely many distinct bulk placements as length increases. The initial first-defect gate at the first site does **not** predict the seven-site closure; that closure is what is new here.

## Reproduction and independent checks

Run, from the repository root:

```
python3 calculation/decimal_frontier/lattice_kinks/code/k2_gate_extension.py
```

This Python script reads the checked-in lattice rows, constructs the full 36-state transfer (the enumerated outgoing edges for x=0..18, u=0 or1), and performs exhaustive BFS for all 9 residues in each of the 9 no-overflow phases; failed BFS searches fully exhaust the reachable finite graph. It also checks the 9-periodic row/carry data independently against full-word arithmetic, constructs concrete palindromic coefficient words at lengths 200,201,210,211,400,401,418,419,700,701,1800,1801 with multiple shifts of each successful motif, and verifies full next pairwords by (a) independent coefficient normalization and (b) ordinary decimal digit-list reverse-and-add of canonical realizing seeds. A separate Python big-integer conversion and reverse-and-add verifies selected lengths 200,400,701,1800, not merely the pairword model. Every test passes. There are **no** control censuses over other bases in this result; the base-9/base-13 controls are required before *new exterior censuses*, whereas this is a self-contained finite p12 centre-response classification, not an exterior census.

The exact scope excludes modifications that begin in the exterior, touch the central transition before carry reset, change the output length, have a first defect in an excluded centre/parity case, or purport to return after multiple steps. It does not rule out any decimal Lychrel certificate.