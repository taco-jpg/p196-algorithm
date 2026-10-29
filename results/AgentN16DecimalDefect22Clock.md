# AgentN16DecimalDefect22Clock
**COMPUTED.** Base-10 p8/m20 rec0 protected exteriors have a sharply clocked **inward** front in independent true-integer orbits.
For q=300 and q=301, all 19,979 timestamps t=22..20,000 satisfy `D_q(t)=5 floor(t/22)+F[t mod 22]`, with `D_q(t)=39+20q-M_q(t)`, M the longest p8-exterior matching prefix, and `F=(0,0,0,0,1,1,1,1,1,1,2,2,2,2,3,3,3,3,5,5,5,5)`.
Shorter controls: q=5 to 300 steps; q=100 to 2,000 steps, same exact formula.
In particular, `D(t+22)-D(t)=5`, and the 264-step CRT-aligned macrocycle shifts the front by 60 cells wherever both endpoints were tested.
**PAPER PROOF (finite table):** the eight 20-digit bulk rows obey `W_(t+22 mod 8)[(j-5) mod 20]=18-W_t[j]` (160 exact entries).
The verifier computes two distinct complete decimal integer evolutions (GMP arithmetic and schoolbook digit arrays) and compares every digit at every step while enforcing the formula.
Reproduce: `sh calculation/new_structures/agent-N16/front_clock/run.sh`; all source/data and independent screw-symmetry check are under that folder.
See `reports/AgentN16DecimalDefect22Clock.md`.
**Not claimed:** an infinite glider, infinite orbit, replenishing band, or proof for untested q/t.
