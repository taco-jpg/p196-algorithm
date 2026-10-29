# Agent5P12SharpChangedRuns

**PAPER PROOF.** In the decimal p12/m9 lattice, among all finite-support
one-step-invisible symmetric bulk pairword perturbations at gamma=0,
the **sharp maximum run of consecutive changed lower-half coefficients**
is 3 at temporal phases t=1,5,9 and 5 at t=2,6,10.
At t=3,7,11 there is no nonempty such finite-support collision.
All residues, widths, parities and coefficients 0..18 are covered.
Thus every block of 4 (respectively 6) consecutive bulk coefficients
inside such a perturbation contains an unchanged baseline cell.
A <=36-state changed-edge DAG and independent 36-bit matrix closure
prove the bounds, attained by known 7-column integer collision motifs.
Reproduce (Python3 stdlib):
`python3 calculation/decimal_frontier/lattice_kinks/sharp_streak/run_checks.py`
No multistep, periodic-centre or decimal Lychrel conclusion.
