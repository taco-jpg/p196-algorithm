# E1Skipped127NoGo

**PAPER PROOF.** None of the 560 base-10 overflow necklaces skipped by the
old 127-bit `bauto3` key guard for p <= 24 can have a reachable periodic
lattice exterior (at any spatial period or state cap).
Exact counts: p=22: 2; p=23: 13; p=24: 545; all smaller p: 0.
Write G for the number of overflow bits. The old key length is 2p+4G.
Since p<=24, every skipped word has 2G>p.
At position zero, q in 1..18, c in {0,1}, g=floor((q+c)/10), and
q'=(q mod 10)+(g ? 1 : (q+c) mod 10). The existing exact potential psi
in `calculation/decimal_frontier/exterior_census/EXTERIOR.md` §2.2(c)
satisfies psi(q')-psi(q)>=2g-1 on every edge. Around a closed walk,
0>=2G-p, contradicting each skipped word. Reproduce with
`python3 calculation/decimal_frontier/lattice_formats/code/check_e1_127_skip.py`.
Not claimed: capped F1-legal streams, other periods, a base-10 certificate.
