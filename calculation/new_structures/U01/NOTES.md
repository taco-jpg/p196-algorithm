# U01 running notes

- Registered CLAIM agent-U01 in issue #475 as a route adjacent to U02 (periods 13–40) and U03 (periods 1–24).
- Parsed the existing rooted p8/m48 SCC (p8_scc.txt, blob dd81a09902e0165a1f54683770e7e3c20824167c) and checked its eight temporal rows against agent14_p8_rows.json (blob 28e538b21cf639f25228720095f5b629686190a4).
- Exact folded two-ended transfer stabilizes after one 48-coefficient block at every phase. Allowed centre-side seam carry sets, phases 0..7: {0,1}, {0}, {0,1}, {1}, {0,1}, {1}, {0,1}, {1}.
- Independent true Python-bigint reverse-and-add controls: 1,056 cases across q=1,2,3,5,8,20,40,80,160 and all eight phases. Every allowed port preserves the entire rooted prefix; every forbidden port produces exactly one mismatch at its final coefficient.
- Contrast with the base-9 neutral band: repeated 8 has carry map f(c)=c, so it transmits both carry values without erosion. The decimal p8/m48 rows are non-9 and have absorbing carry maps; the centre must realize the forced phase-1/3/5/7 ports.
- This is a one-step all-width port contract only. The growing-centre realization and a complete template cycle remain unproved; no ALERT or Lychrel certificate.
