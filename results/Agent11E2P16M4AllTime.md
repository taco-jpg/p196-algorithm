# Agent11E2P16M4AllTime

**COMPUTED.** For base 10 `g=(01)^8`, all `19^4=130,321` spatial-4
coefficient rows (0..18) are exhaustively classified under the exact
16-step cyclic absorbing-row map (all 16 intermediate times checked).
There are 128,126 valid mapped states and 2,195 dead ones. The directed
functional graph has 110 cyclic components: 60 fixed points and 50 3-cycles
(210 cyclic states total); no cycles of other length.
Among these, 64 have a reflection-symmetric primitive spatial-4 row:
48 fixed points and **16 three-cycles** (temporal periods 16 and 48).
The same deterministic classification is independently reproduced in C++
and Python; mandatory base-9/base-13 exterior controls are reproduced.
Not claimed: root reachability of the 16 longer cycles, a decimal certificate,
centres, larger spatial periods, or the fate of 196.
Reproduce: `bash calculation/decimal_frontier/lattice_formats/code/agent11_p16_m4_alltime_reproduce.sh /tmp/a11-m4-all`.
