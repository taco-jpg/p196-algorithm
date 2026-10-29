# AgentX17ChargeSelectedGate
- **COMPUTED:** a one-digit perturbation's *position* controls entry charge to a 4,920-column neutral-9 corridor of a genuine decimal palindrome-adjacent orbit.
- Fixed 10,001-digit baseline palindrome with LSD motif `88283583`: `Q_k=P+10^(5000-k)`.
- At t=107, `k=1` yields unequal entering carries `0/1` and a 4,920-column neutral corridor, collapsing the matched high exterior to 60 digits at t=108.
- Changing just `k=1` to `k=3` gives equal entering carries `0/0` and a 4,916-column neutral corridor, preserving 4,978 matched high digits at t=108.
- Positive seed `Q_3`: exact decimal 20,001 states through t=20000, no palindrome, >=2,151 identical exterior digits per end; independent GMP/full decimal word agreement every step, final length 18,316.
- Exact 15-offset t=107..109 charge-table data and a base-generic carry firewall identity (PAPER PROOF), but no infinite closed certificate or Lean proof.
- Reproduce: `bash calculation/new_structures/agent-X17/charge_gate_reproduce.sh`.
- Code/data: `calculation/new_structures/agent-X17/charge_gate.py`, `charge_gate.csv`, `independent_offset_gmp.cpp`, `charge_gate_reproduce.sh`; details in `reports/AgentX17ChargeSelectedGate.md`.