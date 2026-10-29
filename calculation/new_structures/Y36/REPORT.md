# Y36 report: p8 rec0 emitter cost refund

**Status: PARTIAL**: the bounded E/J packet slice is exhausted for packets of at most four legal ±9 edits. It does not solve the decimal Lychrel problem.

## Exact statement

Fix the rooted p8/m20 rec0 source P=H ++ [5,5] ++ reverse(H), with H=B39 ++ W0^q ++ E ++ J ++ V7^k, q,k>=20, canonical B39, W0, V7, and phase clock g=(10)^4 repeated. Let E start as W0 and J as [18,0,1,1]. An allowed edit changes one coefficient of E or J by ±9, staying in [0,18], and a packet uses at most four edits at distinct physical sites.

The exact q=k=20 digit-array enumeration has 25, 299, 2,277, and 12,397 packets of sizes 1, 2, 3, and 4. Respectively, 17, 136, 684, and 2,435 restore the rooted prefix B39 ++ W0^(q+1) after 160 genuine reverse-and-add steps. All restoring packets have exactly the same first successor pairword as T14's emitter E[9]:1->10; hence they merge into its orbit at the next reverse-and-add edge and have the same t=160 V7 run, k-8. No alternative cost-refunding emitter exists in this packet class.

The all-width lift for q,k>=20 uses the exact p8 carry-reset/insertion argument: W0 and V7 have no adjacent 9s, so a changed carry is reset at a non-9 coefficient; the 160-step two-sided active cone has width at most 320, less than each 400-coefficient band at q,k>=20. The outer root and inner centre therefore cannot interact with the finite E/J transfer during this checkpoint. The overflow clock is the rooted (10)^80 sequence.

## Independent controls

verify_ledger.py compares actual arbitrary-precision integer arithmetic N -> N + reverse(N) with an independent digit-array implementation at q=k=20,40,80,160 for all six variant-2 one-site entries. It also checks the T14 t=160/240/320 checkpoints at those widths. exhaustive.cpp reproduces the complete finite packet counts at q=k=20.

## Scope and next move

This is a scoped cost lower bound, not a global p8 no-go and not an all-time Lychrel certificate. It does not cover packets of five or more edits, arbitrary edits, moving/growing junctions, phase changes, or a cross-epoch fractional ledger. Redirect the next search to those cases rather than repeating one-to-four-site ±9 emitter scans.
