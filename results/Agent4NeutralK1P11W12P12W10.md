# Agent4NeutralK1P11W12P12W10

**COMPUTED** (exhaustive finite-window bitmask DFS; no state cap).
For base 10 neutral p=11, `g=11100010000`, `e=10100110011`, no centre of
lower-half free width <=12 survives 100 steps for either starting parity.
For base 10 neutral p=12, `g=100010001000`, `e=101010010101`, none of
width <=10 survives 80 steps for either parity (other exteriors are rotations).
Each of 19 low-to-high first-digit prefixes per parity was exhausted (38/stream),
with exactly zero survivors; all possible temporal periods are thereby excluded.
Build and rerun the executable solver with resumable checkpoints and controls:
`python3 calculation/decimal_frontier/lattice_formats/agent4_neutral_wide/run_neutral_wide.py --workdir /tmp/agent4-k1`.
The input data, independent 36-case direct-digit checker, six partition checks,
and known base-26 positive control (width 3, survivors 4 and 2) are alongside it.
Dependencies: existing `calculation/decimal_frontier/lattice_formats/code/kinkdfs_mask.cpp`.
Not claimed: wider centres, other decimal exteriors, a certificate or 196 Lychrel.
