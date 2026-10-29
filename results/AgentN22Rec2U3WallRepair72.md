# AgentN22Rec2U3WallRepair72
- Label: **PAPER PROOF**, supported by an exact 73-state full-coefficient carry checker and independent ordinary-decimal **COMPUTED** replay; **not** Lean-verified.
- All-width statement: for every independent `q>=5,k>=34` and `d in {-5,4}`, canonical `P0=B0 W0^q [3,4] U3^k [10,4]` with charge-balanced changes at seam offsets `+2,+4` has rooted `B_(t mod8)` on every `t=0..72`, nonpalindromic throughout, alternating overflow `10` for 72 edges, and exactly `W0^q` intact after B0 at t72.
- U3=`(10,4,10)`; exact eight-step rec2 frontier gains `[0,-1,0,-1,0,-1,+1,0,-1,0]` for every q,k in the statement.
- Finite 73-phase **two-counter carry-pumping** proof checks commuting W48/U3 insertions, both reflected high/low carry fixed points and literal 2x2 parameter corner at every step.
- The two heads `d=-5` and `d=+4` coalesce at t2; eight width-pairs independently replayed with real Python big integers for both heads.
- Not an all-time return: inner U3 copies deplete and junction does not recur. No decimal Lychrel certificate, no claim about 196, no ALERT.
- Sources and commands: `calculation/new_structures/agent-N22/{repair72_pump.cpp,repair72_bigint.py,repair72_run.sh}`; `bash calculation/new_structures/agent-N22/repair72_run.sh`.
- Full soundness statement/proof scope: `reports/AgentN22Rec2U3WallRepair72.md`.