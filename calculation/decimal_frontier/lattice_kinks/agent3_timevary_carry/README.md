# Agent3TimeVaryCarryNoGo reproducibility

This commit includes the exact rec2 lattice snapshot plus **two independent Python 3 standard-library implementations**. There is no state cap, hidden dependency, or uncommitted data.

From the repository root:

```sh
python3 calculation/decimal_frontier/lattice_kinks/agent3_timevary_carry/witness.py
python3 calculation/decimal_frontier/lattice_kinks/agent3_timevary_carry/independent_check.py
```

Expected primary output:

```text
PASS: 8 rec2 phases; time-varying 384-variable witness (0,47),(2,5),(3,5)
WITNESS 1: phase0 position47+1 has bare=1-10^48, coeff=0
WITNESS 2: 2*(phase2 position5+1)+(phase3 position5+1) has bare=-99*10^4, coeff=0
gcd(10^48-1,99*10^4)=99; hence M|99
```

Expected independent output:

```text
INDEPENDENT PASS: modulo-normalization witness and 2400 positive cyclic controls across divisors of 99
```

`witness.py` uses the exact integer carry recurrence; `independent_check.py` uses digit normalization and a separate carry construction. Both test the rec2 8-phase row map and explicit coefficient cancellations. The randomized independent controls cover both g=0 and g=1 in M=3,9,11,33,99. This is a *cyclic bulk* covariance result, NOT a finite centre search or a decimal Lychrel certificate.
