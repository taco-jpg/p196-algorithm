# Y36 emitter ledger

## Canonical bands and baseline

- Overflow clock: g=(10)^4 repeated; t=160 has 80 overflows and is phase-aligned (80 divides T).
- B39 = [17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13].
- W0 = [17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13].
- V7 = [9,11,5,1,15,17,5,1,7,4,15,0,17,16,18,11,15,4,6,3].
- Baseline E=W0 except E[9]: 1 -> 10; J=[18,0,1,1]; C=[5,5].
- At t=160, baseline restores B39 W0^(q+1) and its longest V7 run is k-8. At t=240 and t=320, the W-prefix first mismatch is 16 and 55 coefficients before the target cut, while the longest V7 runs are k-12 and k-15. These are diagnostics, not a renewal.

## Ordered one-site emitter list

A candidate edit changes one E or J coefficient by +9 or -9 while keeping it in [0,18]. This list is 1-based; variant-2 entries have ranks congruent to 2 modulo 4: 2, 6, 10, 14, 18, 22.

1. E[0]: 17 -> 8
2. E[1]: 3 -> 12 (variant 2)
3. E[2]: 1 -> 10
4. E[3]: 13 -> 4
5. E[4]: 17 -> 8
6. E[5]: 11 -> 2 (variant 2)
7. E[6]: 14 -> 5
8. E[7]: 3 -> 12
9. E[8]: 18 -> 9
10. E[9]: 1 -> 10 (T14 baseline)
11. E[10]: 2 -> 11
12. E[11]: 0 -> 9
13. E[12]: 7 -> 16
14. E[13]: 3 -> 12 (variant 2)
15. E[14]: 14 -> 5
16. E[15]: 12 -> 3
17. E[16]: 15 -> 6
18. E[17]: 9 -> 18 (variant 2)
19. E[17]: 9 -> 0
20. E[18]: 7 -> 16
21. E[19]: 13 -> 4
22. J[0]: 18 -> 9 (variant 2)
23. J[1]: 0 -> 9
24. J[2]: 1 -> 10
25. J[3]: 1 -> 10

## Exhaustive packet ledger at q=k=20

A packet consists of r edits at distinct physical E/J sites, each selected from the list above. For r=1,2,3,4, legal packet counts are 25, 299, 2,277, and 12,397. The counts restoring B39 W0^(q+1) at t=160 are 17, 136, 684, and 2,435. Every restoring case has T14's first successor pairword; no restoring case outside that equivalence class was found.

This is a bounded emitter-class ledger only. It does not cover five or more edits, arbitrary coefficient replacements, a changed band phase, a growing/moving seam, or a multi-epoch repair.
