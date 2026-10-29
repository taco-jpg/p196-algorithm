# W42 running notes

- Read AGENTS.md, OPEN_PROBLEMS.md, docs/FOCUS_SWARM.md, AUDIT_N.md, AUDIT_Nseries.md, FORMATS.md, the last 40 FEED/COMBINE lines in #475, and the read-only #474 history before registering the route.
- Registered CLAIM agent-W42 on issue #475 (comment 6490999380). The broad phase-0 |J|=3–4 cell was already claimed, so this run follows the named disjoint U=(10,8,9), odd-centre shard.
- Applied the parity-correct odd-centre mod-11 gates. Since A(U)=0 mod 11, any admissible odd C must have A(C)=0 and J must have A(J)=0. Exact J counts: 623 length-3 words and 11,859 length-4 words.
- Directly enumerated every one of the 12,482 gate-admissible J words; the R02 MDD was not needed as a prefilter, so the search does not depend on that MDD's soundness or completeness.
- Built and ran a standalone C++ port of R30's affine-run symbolic pairword algorithm. All 12,482 admissible J words completed in six chunks at independent q,k>=512; zero symbolic errors, zero clock failures, zero W9-prefix survivors.
- The first mismatch is always inside W9, at cut offsets -25 through -15 (with -17 absent). Exact histogram is recorded in CELL_REPORT.md.
- Independent C++ digit-vector reverse-add exhausted all 12,482 J words at q=k=20,40,80,160. Independent Python-bigint reverse-add exhausted all 12,482 at q=k=20 and passed 192 controls across six odd centre lengths, two centre representatives, and four widths. Ten representative symbolic cases, one per mismatch class, agree with the original Python R30-style symbolic checker.
- No candidate was found; no all-time decimal certificate is claimed. The scoped obstruction is reported because it redirects the W search to other U/parity cells.
