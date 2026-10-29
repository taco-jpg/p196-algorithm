# Q03 running NOTES

- 2026-10-29: Read fresh AGENTS.md coordination migration, OPEN_PROBLEMS.md, docs/FOCUS_SWARM.md, the last 40 FEED/COMBINE lines on #474, and latest #475 coordination lines. Current owner focus is rooted p12/m9 T* with U3 exponent k -> k+5 in 120 ordinary steps; old p8/m20 work is no longer the primary target.
- Posted migrated CLAIM in #475 (comment 6490973867) after the first write attempt hit a temporary GitHub secondary rate limit.
- Derived and checked the T* deep-U3 first-contact table: in all 30 charge-zero U3 motifs and all 120 actual temporal phases, exactly one cell can hide a one-cell mirrored defect through the contact coefficient. Non-overflow gate is 9 -> 4/14; overflow gate is the even predecessor of 9, changed by ±9.
- Independent local checker passed 3,600 phase/motif rows, 10,800 physical carry ports, and 16,560 candidate edits; bigint and separately coded schoolbook digit-array successors agree. This is local necessary-condition progress only, not a full seam return.

- Follow-up deduction: every gate has an exact all-width post-contact transport signature. Gamma=0 emits a reflected ±1 pair one column inward; gamma=1 emits reflected two-column (∓10, ±1) packets. Extended the checker to assert the full successor difference support, not just prefix equality.

- New all-width local no-go: after a valid first-contact gate at j, an arbitrary second edit only at j+1 and its mirror cannot restore next-pairword equality through j+1. Proof splits by overflow: parity obstruction for gamma0; four exact threshold branches for gamma1. Independent controls exhaust all 19 adjacent replacements for all 3,600 phase/motif gates (68,400 actual-integer edits).
