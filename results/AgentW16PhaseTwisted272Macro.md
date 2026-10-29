# AgentW16PhaseTwisted272Macro
- Label: **COMPUTED**. Exactly 12 macro snapshots at t=272h, h=1..12, for the reference decimal pairword B W^440 [9] V^530 [9] reverse(B W^440 [9] V^530) of the preceding W16 result. No infinite claim.
- The p8 overflow clock grows pairword length by 136 per 272-step macro, exactly the paired-insertion length of one period-20 W and one period-48 V block.
- **New phase-cocycle:** moving the V start by 20h forces a comparison phase rotation phi_h=20h (mod 48), rather than falsely demanding the same spatial phase. The source V lattice is primitive period 48.
- At t=272 the unrotated (+1,+1) template differs in 50,053 of 68,697 pair coefficients; the phase-twisted template differs in only **627**. Exhaustive 20x48 spatial-rotation check selects W rotation 0, V rotation 20 as best.
- The residual remains confined to three gap-5-connected mismatch clusters (two reflected joint cones and one centre mismatch) at every measured snapshot. Its size increases 627,1247,...,7629 through t=3264; the finite macro is NOT closed.
- At h=12, phi=0 after a full 12-phase circuit, but 7,629 defects remain. A phase clock alone does not heal the seam.
- Ordinary byte-digit evolution and independent GMP arbitrary-precision reverse-add reproduce all 12 full mismatch counts and nonpalindromicity.
- Reproduce `sh calculation/new_structures/agent-W16/run_twisted.sh`; source/checker/data under `calculation/new_structures/agent-W16/{twisted_macro.cpp,twisted_macro_gmp.cpp,run_twisted.sh,phase_observations.txt}`.
- Full proof scope and construction: `reports/AgentW16PhaseTwisted272Macro.md`. Not a decimal Lychrel certificate or a result about 196.
