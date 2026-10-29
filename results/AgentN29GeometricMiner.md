# Agent N29: 400 universal decimal 9-band steps
- **COMPUTED**, base 10: starting words `12 9^q 34` with **every integer q>=600**, the first 401 orbit states (steps 0..400) are nonpalindromic.
- Every one of the 400 reverse-add transitions is independently certified as an exact rational-polynomial identity in `X=10^q`, using the earlier `AgentN29GeometricWords` sound checker.
- At every step, the entire word has the exact form `L_t ++ 9^(q+c_t) ++ R_t`; there is no fixed-width centre assumption.
- Independent normal Python big-integer reverse-add replay at q=637 matches the symbolic word at all 401 states, not just snapshots.
- For q=600, the 9-band shrinks from 600 to **360** digits; the two literal packets reach lengths 204 and 204 at step 400.
- Reproduce: `python3 calculation/new_structures/agent-N29/geometric_miner.py --q 600 --steps 400 --out /tmp/n29-9band.json`.
- Source: `calculation/new_structures/agent-N29/geometric_miner.py`; compact data: `calculation/new_structures/agent-N29/geometric_miner_checkpoints.tsv`.
- Scope and limitation: `reports/AgentN29GeometricMiner.md`.
- **NOT CLAIMED:** an infinite orbit, a periodic/closing template, a certificate for 196, or any statement after step 400.
