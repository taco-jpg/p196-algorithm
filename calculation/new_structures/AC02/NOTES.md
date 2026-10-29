# AC02 execution notes, October 29 2026

- Registered AC02 on GitHub issue #476, comment 6502479168; read AGENTS.md, OPEN_PROBLEMS.md, FOCUS_SWARM, CELL_LEDGER, R30 independent verifier, p12/m9 data and AUDIT_N.
- Runtime git clone failed on unavailable DNS; all repository reads/writes used the GitHub connector.
- Exact differential carry engine stores per-phase baseline and propagates a changed coefficient interval until decimal carry rejoins the baseline. If the carry does not rejoin, it runs a full-width physical 120-step fallback; it never treats a non-rejoined carry as exclusion.
- Audit mode checked each of 120 intermediate pairwords against a full-width digit-array engine for 100 lexicographic centres per U and length 7..10: no mismatch. A separate Python arbitrary-precision decimal integer replay checked 45 U/C/width cases, 5,400 genuine transitions at (q,k)=(14,100),(20,80),(40,160),(80,320),(160,640). 60 additional J-variation controls matched within a radius-155 central window. Sample tests corroborate but do not replace T12.
- Strict-W9 phasewise MDD exclusions were NEVER used. The odd-only modular gate is applied only in oddallwidth mode.
- Main unresolved cells: centre length 12..14 (plus unrestricted reference-width length 11). A carry-aware constraint propagator or sound meet-in-middle is needed rather than brute force or a strict-phase W9 shortcut.