# N13: a decimal 22-step moving front and 20,000-step asymmetric seed
- Label: **COMPUTED** (finite scope only, NOT LEAN-VERIFIED).
- Base 10; seed length 10,400, built from reachable p8/m20 rec0 exterior with a 100-cell inner perturbation.
- Two independent arithmetic engines: C++ full decimal digit reverse-add and Python arbitrary-precision `int`.
- All states t=0..20,000 have no palindrome; first eight pair coefficients agree with p8 rows in every phase.
- For the pairwords of perturbed and unperturbed seeds, first-disagreement index f(t) satisfies
  `f(t+22)=f(t)-5` for every integer 18<=t<=19978; equivalently `f(t+88)=f(t)-20`.
- The 22-step equation fails at exactly t=0,1,2,3,10,11,14,15,16,17 in 0..19978.
- f(0)=5100; f(20000)=556; final integer length=20,400.
- The front is converging TOWARD the outer boundary, not a perpetual protected centre.
- All input/code/controls: `calculation/new_structures/agent-N13/` (`bash run_all.sh`).
- Explanation and alternative infinite-certificate format: `reports/AgentN13DecimalShearedFront22.md`.
- No decimal Lychrel number proved, no infinite orbit certified, no claim about seed 196.
