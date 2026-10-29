# AC45 exact-clock and guard audit (COMPUTED, bounded; pi185 UNDECIDED)

The earlier `engine.py` counts 30 overflows but does **not** establish the prescribed 120-bit phase clock or a phase-by-phase non-palindrome guard. This independently replayed add-on audits those separate obligations for the bounded J2 control, without mistaking a total overflow count for a physical-clock certificate.

Run: `python3 calculation/new_structures/AC45/clock_guard.py` (361 distinct J pairs, q14/k100); optionally `--wide` (three controls each at q20/k80, q40/k160, q80/k320, q160/k640). Every physical step is compared against an independent Python bigint reverse-and-add. A deliberately planted 10 -> 11 palindrome control tests rejection. The script asserts the genuine clock is `(100010001000)^10`. The exact source is the canonical `realize` routine in `engine.py`. Any mismatching clock is counted, not silently conflated with a mere total of 30.

**Missing lemma addressed:** trustworthy phase-by-phase physical-clock and non-palindrome verification for finite witnesses fed to a future complete reference-width pi185 symbolic product. This is a verifier correction/control, NOT a decision of the arbitrary-length J/C language, NOT an all-time base-10 certificate. Label: COMPUTED only for the explicitly replayed finite control cases; UNDECIDED for pi185.


## 2026-10-29 joined spatial-column result (UNDECIDED globally)
A further computed physical carry/lag composition across n=1..4 adjacent *joined* folded columns is in [JOINED_COLUMNS_REPORT.md](JOINED_COLUMNS_REPORT.md), code [joined_columns.py](joined_columns.py). It independently checks 1,440 short-clock counts, 3,600 physical steps and the 120-layer ROBDD node counts 90/515/4096/12999. This does **not** decide the arbitrary-J/C 120-layer pi185 language and adds no T* return or decimal all-time certificate.
