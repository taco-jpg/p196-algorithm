# Paper-folding fixed-collar renewal obstruction

- **Label:** PAPER PROOF (scoped).
- **Claim:** for any fixed admissible q and fixed finite J,C, no all-sufficiently-large-k rooted p12/m9 120-step literal-prefix return `V_k -> V_(k+5)` exists when `V_k` codes the regular paper-folding word by `(9,0,18)` / `(9,2,16)` under overflow clock `(1000)^30`.
- **Proof idea:** primitive-substitution uniform recurrence plus the decimal carry-reset rule makes every hypothetical returning bulk phase finite-radius; fixed-collar five-motif append is finite-state and hence ultimately periodic, contradicting paper-folding aperiodicity.
- **Scope exclusions:** no claim against moving/growing collars, phase-changing centres, alternate clocks, or the decimal Lychrel problem in general.
- **Reproduction:** `python3 calculation/new_structures/Y22/paperfolding.py` (true-integer and independent digit-array controls at q,k=20,40,80,160).
