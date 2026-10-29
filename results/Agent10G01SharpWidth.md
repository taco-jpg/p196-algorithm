# Agent10G01SharpWidth
**PAPER PROOF.** In every integer base b>=2, a canonical-root period-two
neutral exterior with overflow g=01 can reach its first accepting cut
at spatial width m>=2 only if b<=3*2^(m-1)-4.
The bound is sharp for EVERY m>=2: in b=3*2^(m-1)-4, the first accepting
width is exactly m (strengthening the prior infinite-family exterior theorem).
All-parameter four-state corridor, one-carry lemma and terminal-predecessor
proof: `reports/Agent10G01SharpWidth.md`.
Primary exact checker: `calculation/decimal_frontier/lattice_formats/code/agent10_g01_sharp_width.py`.
Independent original-equation checker:
`calculation/decimal_frontier/lattice_formats/code/agent10_g01_sharp_width_independent.py`.
Commands: `python3 calculation/decimal_frontier/lattice_formats/code/agent10_g01_sharp_width.py --prove 512`
then `python3 calculation/decimal_frontier/lattice_formats/code/agent10_g01_sharp_width_independent.py`
and `python3 calculation/decimal_frontier/lattice_formats/code/agent10_g01_sharp_width.py --controls`.
No centre closure, other format, decimal Lychrel result, or Lean verification is claimed.
