# Agent N02 exact regular-centre predecessor refinement
Label: COMPUTED.
Scope: base-10 p8/m20 rec0 exterior, its 39 rooted pair coefficients, all 8 temporal phases x 2 parities, exact all-length DFA predecessor languages through 6 steps.
Each depth DFA recognizes every physically valid centre halfword preserving the specified exterior and nonpalindromicity for the next k steps, without a centre-width cap.
All 16 classes remain nonempty and have unbounded accepted lengths at depth 6. Largest minimized DFA sizes by k=0..6: 43,43,47,66,231,878,3558.
An explicit two-sided carry preimage NFA plus subset determinization, regular intersection, and DFA minimization constructs the result exactly.
Checks: 18,480 independent integer membership tests; 96 ordinary-decimal-digit replays of the depth-6 shortest witnesses; 16 accepted-cycle unboundedness checks.
This is a finite-horizon growing-centre mechanism, not an infinite orbit, decimal Lychrel proof, or conclusion about 196.
Code/data: `calculation/new_structures/agent-N02/{regular_preimage.py,preimage_check.py,preimage_depth6.json}`.
Reproduce: `python3 calculation/new_structures/agent-N02/preimage_check.py` and `python3 calculation/new_structures/agent-N02/regular_preimage.py 6`.
Report: `reports/AgentN02RegularPreimageRefinement.md`.