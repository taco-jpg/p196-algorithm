# AgentU01P8M48PortContract

**Label: PAPER PROOF** (exact finite two-ended carry-state induction; 1,056 true Python-bigint controls; not Lean-verified).

For the rooted base-10 p8/m48 band with overflow 10101010, let H_t = B_t ++ W_t^q, q >= 1. For every physical palindromic centre C, the next prefix B_(t+1) ++ W_(t+1)^q is preserved iff the actual centre-side seam carry u_t belongs to the phase-0..7 sets {0,1}, {0}, {0,1}, {1}, {0,1}, {1}, {0,1}, {1}.

The transfer state set stabilizes after one 48-coefficient band, so induction covers all q >= 1. A forbidden seam carry causes exactly one mismatch, at the final protected coefficient. Unlike the base-9 neutral all-8 band, whose carry map is f(c)=c, the decimal rows are absorbing and force u_1=0, u_3=u_5=u_7=1; overflow-one phases 0,2,4,6 allow either carry.

**Scope:** all-width one-step rooted-prefix contract only. The canonical symmetric growing-centre realization, full template return, all-time guard, and decimal Lychrel certificate remain UNDECIDED.

Reproduce: python3 calculation/new_structures/U01/port_contract.py. Inputs: calculation/new_structures/U01/p8m48_inputs.json.
