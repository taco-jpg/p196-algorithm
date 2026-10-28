# Agent9F1PowerClosure
**PAPER PROOF with exhaustive exact finite-state check.** In base 10, a binary
overflow word w passes the first-coordinate F1 cycle condition iff w^k does
for every positive integer k: repetition cannot revive a rejected word.
Proof: the 18-state position-zero NFA generates exactly 434 Boolean relations;
176 have a diagonal entry; the other 258 are nilpotent, all R^5=0.
Nilpotency-index histogram among rejected relations: 1:1, 2:251, 3:4, 4:1, 5:1.
Writing A(d,g) for accepted time-rooted length-d words of Hamming weight g,
the number N(p,G) of accepted necklaces satisfies
N(p,G) = (1/p) sum_{k | gcd(p,G)} phi(k) A(p/k,G/k);
primitive necklaces use the same formula with Mobius mu(k) instead of phi(k).
**COMPUTED.** Independent Burnside engine agrees for every p<=60 and weight G.
Reproduce: `python3 calculation/decimal_frontier/exterior_census/py/f1_power_closure.py 60`.
**Not claimed:** any full exterior B-cycle, absorbing centre or decimal Lychrel number.
