# Q14 independent reproduction

Run from the repository root:

    python3 calculation/new_structures/Q14/positive_controls.py
    python3 calculation/new_structures/Q14/morphism_gate.py
    python3 calculation/new_structures/Q14/test_morphism_gate.py

positive_controls.py uses Python arbitrary-precision integers and recomputes the decimal reverse from current digits at every step. It independently replays the known base-9 Lean cycle and computed base-50 cycle at four parameters each. morphism_gate.py uses only the standard library and implements the all-time graph criterion plus exact finite maximum-increment checks in the bounded case. test_morphism_gate.py exhaustively checks all 216 two-letter morphism/seed cases in its stated small domain.

The T* diagnostics recorded in NOTES.md and IDEAS.md are not promoted as positive results or as a decimal certificate. No Lean source is changed in this result.
