# Agent3SpatialWeightsMod198: fully reproducible exact certificates

Python 3 standard library only. From repository root run:

```sh
python3 calculation/decimal_frontier/lattice_kinks/agent3_spatial_mod198/generate.py
python3 calculation/decimal_frontier/lattice_kinks/agent3_spatial_mod198/independent_check.py
```

`generate.py` deterministically rebuilds four **integer** cancellation certificates and one exact **modulo-4** torsion certificate from the committed `lat2.txt`. It writes small (under 80 KB) local JSON files to `/tmp/agent3_rec2_spatial_certificates/`. All data, source, input and independent checking logic are in the same commit; no external solver, remote data or hidden sandbox files. The generator produces integer right-hand sides with gcd=396 and an 82-term congruence contradiction modulo 4. The independently implemented checker uses a different digit-normalization map to verify every coefficient of each certificate, both positive solutions on all 2252 row tests, and 2400 randomized cyclic updates.

Expected generator output includes:

```text
INTEGER CERTIFICATE (7, 7, 1, 0) terms 66 rhs 57722492937563942400
INTEGER CERTIFICATE (7, 9, -1, 0) terms 75 rhs -20438186631342374822400
MOD-4 CERTIFICATE (7, 0, -1, 0) terms 82 rhs=2
CERTIFICATES WRITTEN /tmp/agent3_rec2_spatial_certificates
```

The third/fourth integer certificates (389, 393 terms) also reconstruct with total gcd exactly 396. Independent expected output:

```text
INDEPENDENT PASS: two-digit-normalization carry solver checks four integer certificates and mod-4 torsion certificate
INDEPENDENT PASS: explicit mod-2/mod-99 solutions on 2252 tests; 2400 randomized cyclic controls
INDEPENDENT MODULUS CLASSIFICATION: all and only M dividing 198
```

Scope is only a specified cyclic-bulk covariance problem, not decimal centre existence or any Lychrel certificate.
