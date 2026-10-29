# AgentN22Rec2MovingCentre20000
- Label: **COMPUTED**.
- Scope: one explicit base-10 seed `q=100` with pairword `B0 ++ W0^100 ++ [10,14,1,10] ++ reverse((B0 ++ W0^100 ++ [10,14,1,10])[:-1])` (odd length).
- Independent exact digit-array and GMP arbitrary-precision reverse-and-add replays: **20,000 steps**, no palindrome, every overflow bit `1010...`, all 20,001 phase-8 `B11` and at least `W128` coefficients verified.
- Stronger digit-array replay: the maximal matched rec2/m48 band is **at least 1,900 coefficients at every step**; length 9,629 -> 19,629.
- Drifting-centre mechanism: front site 4,811 -> 1,911; centre half-width 4 -> 7,904 (central defect grows, not periodic).
- First exterior-clock failure occurs at step **33,062**; no assertion of infinite survival or a decimal Lychrel number.
- Full exact code, 48-site eight-phase data, independent checks, corruption and palindrome controls: `calculation/new_structures/agent-N22/`.
- Reproduce: `bash calculation/new_structures/agent-N22/run.sh` (requires g++, GMP/gmpxx, Python3).
- Details/precise caveats: `reports/AgentN22Rec2MovingCentre20000.md`.
