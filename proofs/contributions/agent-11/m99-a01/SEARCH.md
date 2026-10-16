# Agent #11 — M99-A01 concrete return-certificate search

## Status

The originally assumed finite-seed/admissibility premise is already proved in the merged Agent112 work. In particular, Agent112.Admissibility.automatic_admissibility proves check cert = true -> exists H M, Admissible0 cert H M, and Agent112.Admissibility.checked_positive_decimal_seed packages this into a strictly positive ordinary-decimal Lychrel seed, conditional only on an accepting certificate. Agent110 independently rebuilt and semantically reviewed that source closure.

Therefore M99-A01 cannot responsibly duplicate that theorem. The actual remaining hypothesis in the return-certificate route is stronger and concrete: an actual certificate with check cert = true must exist.

## Exact finite search performed

An independently written Python model implementing the Agent109 successor, normalization, carry, trimming, and deterministic state transition was run exhaustively on these domains:

| Domain | States | Successors leaving domain | Internal cycles |
|---|---:|---:|---:|
| all 16 phases; B,A,C lengths <=1; coefficients 0..18 | 128000 | 127640 | 0 |
| six-phase cycle {2,4,8,16,14,10}; B,A lengths <=2 over {0,1,8,9,10,17,18}; C symmetric length <=2 with even center | 350892 | 342229 | 0 |
| two-phase cycle {6,12}; same block domain | 116964 | 116612 | 0 |

The first domain is fully exhaustive over its stated state space. The latter two restrict C to the mirrored/even-middle shape already required by the certificate semantics and restrict coefficients to a deliberately small alphabet; they are not global searches.

No accepting ReturnCertificate was found. This is computational WIP evidence only, not a Lean theorem of global nonexistence.

## Consequence

The automatic finite-seed realization hypothesis is no longer the bottleneck: it is kernel-checked and independently reviewed. The bottleneck is finding an accepting cyclic certificate. Any future candidate should be passed through the original Agent109.Cert.check and then through the existing automatic-admissibility theorem rather than introducing a new realization premise.

Script SHA-256: 356b406af916bfebca4d62ee90938ab6b1356109178e30baab52a6535e6c90a2. Local Lean runtime is unavailable in this execution, so no new Lean theorem is labeled LEAN-CHECKED.


## Independent verification

`search.py` was rerun and reproduces all three rows exactly. Its transition was compared with Agent #109's `certificate_tool.step_state` on 20,000 random states: 0 mismatches. Because it follows only the maximal trim, see Agent #211's all-trim audit for the nondeterministic extension (same conclusion).
