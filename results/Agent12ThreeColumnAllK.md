# Agent12ThreeColumnAllK
**PAPER PROOF:** For every integer k>=1, the canonical-root base-10 bauto3 position automaton under g=(11000)^k has exactly 4^k time-closed **first-three-spatial-column histories**, before any fourth-column requirement.
The forced temporal coefficient blocks are x0=(9,10,1,2,4), x1=(13,3,4,8,16), x2=(15,10,4,8,17), each repeated k times; all first/second-column boundary carries are forced by three-column closure, while each 5-step block has four freely chosen third-column outgoing carry words (a,b,0,1,0).
Proof: the exact first-column 8-edge, second-column 19-edge and third-column 12-edge 5-step transfer graphs have a unique viable self-loop at each layer (and multiplicity 4 at the third).
**COMPUTED controls:** a standalone exhaustive finite transfer enumerator and a distinct whole-period DP cross-check k=1..8 produce (third-history counts) 4,16,64,256,1024,4096,16384,65536; full-SCC base-9/13 controls reproduce 956310/250302 states and 7/5 SCCs.
Source: `calculation/decimal_frontier/threecol_allk/{block_graph.py,independent_whole_period.cpp,full_scc_controls.cpp}`.
Commands: `python3 calculation/decimal_frontier/threecol_allk/block_graph.py`; compile both `.cpp` with `c++ -O2 -std=c++17` and execute (`independent_whole_period 8` and `full_scc_controls`).
Detailed finite relations, proof and exact control outputs: `reports/Agent12ThreeColumnAllK.md`.
Not claimed: a fourth-column extension, reachable accepting SCC, finite decimal Lychrel certificate, orbit of 196, or Lean verification.
