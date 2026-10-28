# Agent11E2P48M8OneLap

**COMPUTED.** Base 10, overflow `g=(01)^24` (48 time steps): there is NO
self-mirror non-neutral absorbing bulk row of exact spatial period `m=8`
that returns after one 48-step temporal period. All eight reflection axes
were exhausted: `4*19^5+4*19^4=10,425,680` indexed symmetric initial rows,
with exact cyclic carries recomputed at each intermediate step; zero hits.
Independent C++ cyclic-carry fixed-point solver agrees on all returned-row
counts; both methods reproduce the `m=4` control (96 primitive returns among
14,440 indexed starts). Mandatory b9 `1100011000` and b13 `1010010000`
full-SCC controls passed. No state or time cap in the completed census.
Reproduce (nice, checkpointed):
`bash calculation/decimal_frontier/lattice_formats/code/agent11_p48_m8_reproduce.sh /tmp/a11-p48-m8`.
Not claimed: m8 temporal periods longer than 48, other spatial periods,
root reachability of any other bulk, a centre, or decimal Lychrel existence.
