# Agent N02 regular-centre finite-state certificate format
Label: PAPER PROOF (soundness); COMPUTED (finite-state checks and decimal charge probe).
Scope: any integer base >=2; arbitrary-length regular languages of palindromic pair halfwords, exact carry transducer, full-language inclusion proof.
If the phase/parity DFAs are closed under both overflow modes and contain a physical seed, with each word having an odd coefficient, their seed never reaches a palindrome.
The centre length may grow each cycle; no fixed-width, periodic, or ultimately periodic centre is required.
Positive control: the existing base-9 lattice rec0, 40 exact unbounded-word DFA inclusion checks (not a new base-9 certificate).
Decimal p8 rec0: one cut-carry bit gives full one-step 39-digit exterior preservation under explicit phase-dependent charge choices but does not close after two steps.
Explicit 80->81->81 digit decimal replay first disagrees with the expected second-step exterior at index 38.
No decimal Lychrel number, no assertion about 196, no Lean-verified claim.
Reproduce: `python3 calculation/new_structures/agent-N02/carry_relation.py`, `python3 calculation/new_structures/agent-N02/independent_digit_check.py`, `python3 calculation/new_structures/agent-N02/base9_control.py`, `python3 calculation/new_structures/agent-N02/decimal_cut_probe.py`.
Details: `reports/AgentN02RegularCentreFormat.md`; code and deterministic fixture under `calculation/new_structures/agent-N02/`.