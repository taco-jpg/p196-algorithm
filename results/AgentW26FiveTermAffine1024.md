# AgentW26FiveTermAffine1024
**COMPUTED (exact symbolic arithmetic):** for every integer k>=111, N(k)=val_10(P(k)) with P(k)=H(k)++[9]++reverse(H(k)), H(k)=B++W^k++[9]++V^k (N01's explicit B/W/V), has 1024 successive nonpalindromic base-10 reverse-add steps.
All 1025 canonical states have a five-term rational-polynomial value in X=10^(k-111) with support {0,20,68,116,136}; all 1024 equalities N_(t+1)(X)=N_t(X)+rev(N_t)(X) were checked by exact Fraction coefficients, not interpolation.
The endpoint digit pairs are (7,1) for 513 even times and (8,9) for 512 odd times, for EVERY k>=111; each is strictly nonpalindromic.
**PAPER PROOF (format):** exact carry stabilization on a repeated coefficient block converts all affine-repeat coefficient templates into canonical affine-repeat digit templates; each edge is then a finite polynomial identity. See report.
C++ ordinary digit-array oracle for three nearby k values proposes the templates; its samples do not justify universality. The rational-polynomial identities plus endpoint witnesses do.
Reproduce from repo root: `python3 calculation/new_structures/agent-W26/run_fast.py` (Python 3, g++); default kmin=110, outer cut=1300, inner cut offset=1016.
Source: `calculation/new_structures/agent-W26/{affine_core.py,run_fast.py,orbit_coeff.cpp,expected_summary.json}`; report: `reports/AgentW26FiveTermAffine1024.md`.
**NOT claimed:** a decimal Lychrel number, a temporal cycle, 20,000-step uniform shape, a Lean proof, or a repository verifier run.
