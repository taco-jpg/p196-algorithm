# Agent N29: 400 universal decimal 9-band steps
- **COMPUTED**, base 10: starting words `12 9^q 34` with **every integer q>=240**, all 401 orbit states (steps 0..400) are nonpalindromic.
- All 400 transitions hold as exact rational-polynomial identities in `X=10^q`; all 401 nonpalindrome properties follow from the integer-root constant-factor criterion.
- Every state has word form `L_t ++ 9^(q+c_t) ++ R_t`, where `min c_t=-240`, with no fixed-width centre.
- For **q=240**, an independent ordinary big-integer replay matches all 401 full predicted words; at step 400 the band count becomes **zero**.
- The maximum possible integer-root exponent in the 401 nonpalindrome polynomials is **239**, strictly below qmin=240.
- At sample q=600, the band shrinks from 600 to 360 and the literal packets reach 204 digits each (data every 25 steps).
- Reproduce: `python3 calculation/new_structures/agent-N29/geometric_miner.py --q 600 --qmin 240 --steps 400 --out /tmp/n29-9band.json`.
- Code: `calculation/new_structures/agent-N29/geometric_miner.py`; data: `calculation/new_structures/agent-N29/geometric_miner_checkpoints.tsv`.
- Scope: `reports/AgentN29GeometricMiner.md`. **NOT CLAIMED:** nonpalindrome beyond step 400, an infinite cycle or a result on 196.
