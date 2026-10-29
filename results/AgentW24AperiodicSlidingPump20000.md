# AgentW24AperiodicSlidingPump20000
**COMPUTED.** The W24 9-complemented p8/m20 family has an exact whole-pairword **moving-cut period-20 insertion identity** between q=900 and q=901 at EVERY t=0..20,000.
Let P_t(q) be the actual base-10 digit-pair word, low-first. For each t choose c_t as midpoint of the longest lower-half run of P_t(900)[i]=P_t(900)[i+20].
Then P_t(901) is obtained by inserting P_t(900)[c_t:c_t+20] at position c_t AND its mirrored block on the upper side; full-word equality is checked, including the inserted coefficients.
All 20,001 paired states are nonpalindromic, both independently GMP-replayed for 20,000 steps; length difference is identically 40 digits.
The spatial-period-20 run remains >=2732, the moving-cut margin >=1366, while all **20,001 cyclic-rotation-normalized 20-word bulk necklaces** are distinct (finite horizon).
This is not a stationary 8-phase pump: the measured bulk has **no temporal necklace recurrence** through step 20,000.
Small q=100/101 control: 2500 complete pumped nonpalindromic steps, but the band collapses near 2558, so no infinite extrapolation.
Code: calculation/new_structures/agent-W24/sliding_pump_gmp.cpp; data: calculation/new_structures/agent-W24/sliding_pump_20k.json.
Reproduce: g++ -O3 -std=c++17 calculation/new_structures/agent-W24/sliding_pump_gmp.cpp -lgmpxx -lgmp -o /tmp/w24pump && /tmp/w24pump 900 20000
Detailed scope: reports/AgentW24AperiodicSlidingPump20000.md. **No infinite Lychrel certificate or Lean verification.**
