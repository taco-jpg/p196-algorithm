# Agent11E2P16M8OneLap

**COMPUTED.** Decimal overflow `g=(01)^8`, exactly one 16-step temporal
return, spatial period exactly `m=8`: no non-neutral absorbing self-mirror
lattice row exists. All 8 reflection axes are exhaustively enumerated,
covering `4*19^5 + 4*19^4 = 10,425,680` indexed symmetric initial rows
(coefficients 0..18), with the exact cyclic carry row map at every time.
No row with primitive spatial period 8 returns after the 16 updates.
The same C++ row-map checker at `m=4` finds 48 fixed rows, reproducing the
existing m4 control; independently reconstructed position-automaton controls
reproduce b13 `1010010000` singleton depths 55/75 and b9 `1100011000`
period-four depth 61. No state cap is used; the census exhausts its domain.
Not claimed: longer temporal multiples, other spatial periods, any centre,
other overflow streams, a decimal certificate, or 196 being Lychrel.
Reproduce: `bash calculation/decimal_frontier/lattice_formats/code/agent11_p16_m8_reproduce.sh /tmp/a11-m8`.
