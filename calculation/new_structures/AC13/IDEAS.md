# AC13 attempted routes and next directions

- Full branching on unknown upper-port carry costs exponentially many prefixes; 185,139 overapproximate states at step 31 on one initial 140-cell prefix. Discarded.
- Bare W9 prefix lacks enough reach after 120 steps (160 known to 70). Appending a finite U collar is sound and recovers the endpoint no-go.
- Next: a q-uniform carry-port transducer, or the same endpoint-safe collar test on longer J; an exclusion at reference q alone is not a decimal certificate.
