# AgentW03CapSteeredTenStepRepair

- **COMPUTED:** changing the two-digit end caps makes the inserted-99 defect heal for ten consecutive true decimal steps (H,T,Q)=(88,26,200), after collision t=681, healing t=686..695.
- Earlier comparison (12,26,200): collision t=662, repair t=665..671 (7 states). These are genuine full-integer arithmetic steps, not symbolic guesses.
- Three complete finite grids: 2250 suffix/Q trials, 90 prefix trials, 361 focused-Q trials; 20 independently replayed Python bigint controls and a rejected mutation.
- Independent genuine 20,000-step palindrome-free replay for the fixed seed 88(99)^20026: final 8638 digits, checksum modulo 1000000007 = 232300713, C++ overflow count 8234.
- Source/checker/runner: calculation/new_structures/agent-W03/cap_scan.cpp, independent_caps.py, independent20k.cpp, replay20k.py, reproduce_caps.sh; sample data cap_events.csv.
- Full scope: reports/AgentW03CapSteeredTenStepRepair.md.
- No infinite certificate, no Lean proof, no invariant pairword shape after the repair ends, and no claim about 196.
