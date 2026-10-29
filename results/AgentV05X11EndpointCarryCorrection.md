# AgentV05X11EndpointCarryCorrection
**PAPER PROOF (red-team correction):** X11's proposed universal rotation-sheet reverse-add edge criterion is unsound unless the final normalized carry equals the prescribed digit-length increment, `c_n=gamma`.
**Counterexamples:** specified `98->87` (actual `98->187`, dropped carry) and `21->133` (actual `21->33`, invented carry) satisfy X11's stated local obligations, leading-digit and nonpalindrome guards.
**Corrected lemma:** for columns `d_i+d_(n-1-i)+c_i=e_i+10c_(i+1)` and `c_0=0`, summation yields `N+rev(N)=val(e_0...e_(n-1))+c_n*10^n`; the intended canonical output has that value exactly iff `c_n=gamma` and its optional top digit equals 1.
**Scope:** repairs the soundness *specification* of a potential all-time checker. Does not refute the existing finite decimal computations, close a template cycle, establish base-10 Lychrel existence, or have Lean verification.
**Reproduce:** `python3 calculation/new_structures/agent-V05/x11_endpoint_carry.py`.
**Audit:** `reports/audit_2026-10-28/AUDIT_X11-X20.md`.