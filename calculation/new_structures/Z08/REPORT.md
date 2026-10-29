# Z08 report: growing-seam packet census

**Overall status: PARTIAL. Scoped result: EXHAUSTED-NONE for odd-length palindromic C, U ranks 8 and 20, `|J0|=5`, `|R|=3`. Label: COMPUTED with a paper cone-reduction argument; not Lean-verified.** This is not a decimal Lychrel existence proof. Even-length centres and the other U rotation ranks remain open.

## Exact statement

For the physically rooted phase-0 p12/m9 family

`P(q,m,k)=H C reverse(H)`, `H=B W^q J0 R^m U^k`,

with U8=`(6,12,9)` or U20=`(9,18,0)`, a fixed 5-coefficient J0, a fixed 3-coefficient R packet, and an odd-length palindromic centre C, there is no exact 120-step transition

`P(q,m,k) -> P(q,m+1,k+4)`

for all independent `q>=14,m>=120,k>=100` in this subclass. The obstruction is a necessary local endpoint mismatch in the guarded window `W^12 ++ J0 ++ R^57`; every genuine template return would have to restore this window at t=120.

## Exact search space and gates

- All possible packets: `19^3 = 6,859`; exactly 763 have `sum(R)=0 mod 9`.
- The odd-C gate `A(R)=A(U) mod 11` leaves 72 packets per U.
- The exact rooted 120-phase period-three bulk carry map leaves 7 cycles for U8 and 11 for U20, including the degenerate `R=U` in each case. No such cycle visits `999` or has adjacent 9s in any phase. Removing `R=U` leaves 6 and 10 packets.
- The junction gate `2A(J0)=A(U) mod 11` leaves 225,092 J0 words for U8 and 225,107 for U20, out of all `19^5=2,476,099` words.
- Exact compiled collar tests: `6*225,092 + 10*225,107 = 3,601,622` `(U,R,J0)` combinations. Endpoint restorers: **0**.

## Why the finite collar gives an all-width obstruction

The local window is 108 W coefficients, all five J0 coefficients, and 171 R coefficients, for 284 coefficients total. For a coefficient x in 0..18, the carry transfer is c -> floor((x+c)/10): it is the identity only at x=9 and otherwise is constant (0 for x<=8, 1 for x>=10). Every phase of every surviving R bulk cycle has no adjacent 9s, so carry dependence resets within two coefficients. The rooted 120-step lag-clock cone bounds are therefore 91 columns on the W side and 152 on the R side (the latter includes 120 temporal steps, 30 overflow-alignment shifts, and a two-cell reset allowance). The left collar 108 exceeds 91 by 17; the right collar 171 exceeds 152 by 19. At m=120, the window's right edge is 189 coefficients from the U seam, also beyond the 152-column cone. At q>=14 the W band has 126 or more coefficients, so the window fits wholly inside it and has two full W periods to settle the incoming low carry. Thus the local transition is independent of q,m,k,C for q>=14,m>=120,k>=100. At t=120 both bulk motifs return, so the target window is exactly the initial window; a local mismatch rules out a whole-template return for every admissible width in the stated range.

## Independent genuine-decimal verification

`verify_growing_bigint.py` independently constructs canonical integers from symmetric pairwords, applies 120 actual arbitrary-precision decimal operations `N <- N + reverse(N)`, and compares the full local window at every phase with a separately implemented local recurrence. It checks all 16 nondegenerate R packets, one valid J0 and odd C per U, at q=20,40,80,160 with m=120,k=100:

- 64 independent big-integer runs;
- 7,744 window checks including t=0 and t=1..120;
- exact physical overflow clock in all runs;
- zero local-window discrepancies;
- zero full 120-step template returns in these controls.

The controls are independent validation of the local simulator, not the exhaustive proof itself. The exhaustive proof is the finite packet/J0 enumeration plus the reset-cone reduction.

## Reproduction

From the repository root:

```bash
cd calculation/new_structures/Z08
python3 bulk_cycle_census.py
python3 verify_growing_bigint.py
g++ -O3 -march=native -std=c++17 -fopenmp grow_packet_scan.cpp -o /tmp/z08-grow-scan
OMP_NUM_THREADS=5 /tmp/z08-grow-scan | tee scan.log
```

The full scan output is preserved in `scan.log`; running `verify_growing_bigint.py` regenerates `bigint_controls.json` with per-case details. No `ALERT` is warranted because no 240-step restored template was found. Redirect: continue with even-length C or other U ranks; this odd-C U8/U20 packet family is exhausted.
