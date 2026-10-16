# Finite diagnostic controls

The independent `research_status` reviewer ran `diagnostic_controls.py` successfully on its first attempt. Exact script, standard output, standard error and command receipt are preserved under `diagnostics-001/`. The original quotient Python source is pinned by SHA256 and imported without running its discovery main.

Twelve selected states are checked at exponents1,2,3,7: 48 alphabet/head/Boolean-versus-BadWord comparisons. Empty outer/center words, the low-coefficient and outer11/{0,11} rejection patterns, an unbounded nonsymmetric list input, and period lengths1,2,4 are included. The unbounded case exercises only the combinatorial statement; it is not interpreted as a decimal realization.

Ten stripping cases check exact reconstruction, retained alphabet, outside head and Boolean invariance. They include empty residuals, short constant remainders, a seven-column overlap boundary, nonprimitive periods, and the total empty-period conventions. The period remains explicitly present in the stored alphabet.

Two separately claimed fixed boundaries are sampled. The k=0 input `B=[1], H=[], w=[18,18,18,18]` has a true stored state flag while the expanded word `[1,1]` is BadWord. The valid input `B=H=[], w=[10,10,10,10]` is safe and its literal original transition reports `unsafe_target`, with target `([1,2,2,2],[2],[2,2,2,2])`, gamma1, u0, v1 and signed delta-1. These finite observations are not presented as formal proofs; the root author supplies their separate kernel-checked Boundary declarations.

Result: PASS, process exit0, approximately0.044 seconds. Script SHA256 `464f84360c1391b635e6d31eb27936162981c2d7c6f52a1a6f9a608df25050d6`. This execution establishes no safety closure, time-zero numeral property, return or infinite-orbit claim.
