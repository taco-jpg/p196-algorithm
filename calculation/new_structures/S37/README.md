# S37 cyclic seam pumping checker

The checker tests the finite hypotheses in `reports/AgentS37CyclicSeamPumping.md`; it does not infer a theorem from adjacent samples. Supply a JSON candidate with fields `Q`, `K`, `B`, `W`, `U`, `J`, `C`, `W_cut_copies`, `U_cut_copies`; `J` and `C` are arrays of `d` words indexed by `k mod d`. Optional fields are `steps` (must be 120) and `gain` (must be 5); the checker fixes the rooted `1000` clock repeated 30 times.

Run `python3 calculation/new_structures/S37/pump_window.py candidate.json`. Exit 0 means the exact finite conditions were satisfied, and only then does the theorem imply all-width pumping. Exit 1 means at least one condition failed; it is not a no-go theorem for other seams. Run the local insertion regression with `bash calculation/new_structures/S37/run_checks.sh`.
