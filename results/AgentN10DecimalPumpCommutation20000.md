# Agent N10: exact decimal pairword pumping over 20,000 reverse-add steps
- **Label: COMPUTED.** Positive finite-horizon whole-pairword insertion identity in base 10.
- Define `I_t(P)=P[:39] ++ W_t ++ P[39:-39] ++ reverse(W_t) ++ P[-39:]`, where `W_t` is the previously committed eight-phase period-20 lattice.
- For the same symmetric central core and `k=300,301` copies of `W_0`, exact `P_t(301)=I_t(P_t(300))` holds for **all t=0..20000**, not just for a prefix.
- Independent C++ digit-list additions compare all 342,382,118 coefficients of the larger orbit (empty core); three other central cores independently pass.
- Independent Python arbitrary-precision integer reversal verifies full-word pumping for `t=0..1000`.
- Reproduction: `sh calculation/new_structures/agent-N10/run_pump.sh`.
- Code `pump.cpp`, `pump_bigint.py` and earlier deterministic phase data share `calculation/new_structures/agent-N10/`.
- Detailed soundness and limitations: `reports/AgentN10DecimalPumpCommutation20000.md`.
- **Not claimed:** an all-time commutation theorem, a periodic centre, or a decimal Lychrel certificate.
