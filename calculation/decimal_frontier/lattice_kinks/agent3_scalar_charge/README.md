# Agent3ScalarCarryModuli reproduction (standalone)

This folder contains the exact rec2 lattice snapshot used by the theorem, one arithmetic witness generator, and an **independent Horner/Bézout checker**. Python 3 standard library only.

From repository root, run:

```sh
python3 calculation/decimal_frontier/lattice_kinks/agent3_scalar_charge/classify.py
python3 calculation/decimal_frontier/lattice_kinks/agent3_scalar_charge/independent_check.py
```

Expected outputs:

```text
PAPER PROOF arithmetic: gcd(Q)=99; gcd(D0,D2)=1; gcd(Delta01,Delta12)=99
Control moduli 2,3,9,11,37,99,101,9999,10000: PASS
INDEPENDENT PASS: Horner vs direct powers, both carry streams, explicit Bezout 99, moduli 2..10000
```

Each script accepts an optional data-file path, and both accept the committed `lat2.txt` snapshot. The independent checker constructs descending cyclic carries and ascending controls without importing the main program. The theorem does not enumerate centre widths or derive a Lychrel certificate. No third-party packages, external data downloads, or state caps.
