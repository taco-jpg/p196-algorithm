# X05 running notes

- 2026-10-29: Read the current AGENTS.md mission and coordination switch, docs/FOCUS_SWARM.md, OPEN_PROBLEMS.md, AUDIT_N.md, AUDIT_Nseries.md, and FORMATS.md. Read the recent #475 DONE/ALERT and FEED/COMBINE lines plus the read-only tail of #474.
- 2026-10-29: Registered the initial phase-0 route in #475, then noticed it overlapped X12's all-U C=2..13 closure audit. Posted BREAK and re-claimed the disjoint phase-two shard U=(9,6,12), odd C lengths 15..23, |J|=3..4.
- 2026-10-29: Inspected R30's canonical source and symbolic-step semantics, T12's all-width insertion theorem, and Q03's first-contact transition code. R02's 361-state MDD transition artifact is absent from main (also reported in #475 comment 6491116882), so the search uses a direct complete J enumeration rather than an unavailable prefilter.
- 2026-10-29: Implemented and ran search.cpp with q=14,k=100 and C length 15, midpoint 4. Exhausted 19^3+19^4=137,180 J words; all 137,180 have the exact 120-bit clock (1000)^30; zero restore B W^14. First mismatch indices are 135..146, relative to the W9|J cut at index 160.
- 2026-10-29: Independently recomputed the U=(9,6,12) 120-phase bulk cycle and reset cones: seam-side 152, centre-side 121, leaving 27 cells inside U^100. This makes the W9 endpoint independent of C for all claimed odd centre lengths.
- 2026-10-29: Ran independent.py: 100 real-decimal controls (4 J representatives x 5 centre lengths x 5 width pairs) for 120 steps each. Python big-integer reverse-and-add and fresh-buffer schoolbook digit addition agree at every step; all clocks are (1000)^30, no control orbit hits a palindrome, and the final mismatch is 14..25 cells before the W9|J cut.
- Reproduction: g++ -O3 -std=c++17 -Wall -Wextra -pedantic -fopenmp calculation/new_structures/X05/search.cpp -o /tmp/x05-search && /tmp/x05-search
- Reproduction: python3 calculation/new_structures/X05/independent.py
