# Seven-column prefix certificates: exclusion of 739 and four improved depth bounds

Date: 2026-10-15 (UTC). Research baseline: `a71d6e79b009da691e2d97057f83e108a3fcff4f`.

**The full P196 conjecture remains unproved.** This directory preserves the written all-length coverage argument, five complete finite rank certificates, and verification programs. These are computer-assisted local theorems, without Lean formalization or external peer review.

Let `T(n) = n + rev(n)`, and let `H(P)` be the maximum number of iterations from any positive integer starting point to palindrome `P`, continuing iteration through any intermediate palindromes.

| First three palindrome digits | Previous uniform upper bound | New uniform upper bound |
|---|---:|---:|
| 739 | Not in the baseline catalogue | 39 |
| 217 | 28 | 23 |
| 218 | 36 | 34 |
| 620 | 14 | 12 |
| 777 | 27 | 25 |

These bounds apply to every target length and every choice of internal digits; no optimality is claimed. Combined with the exact first 39 steps from 196, they show that its orbit never contains a palindrome beginning with 739. The baseline three-digit prefix catalogue expands from 396 classes to 397; the other prefixes are not all resolved.

- [Complete proof](P196_739_Proof.md): the exact sum-word model, all-length coverage, inverse-edge equations, rank certificates, and the corollary for 196.
- [Verification results](verification_results.json): state counts, edge counts, hashes, and integer cross-checks for the five certificates.
- [Exploration scope](exploration/README.md): the precise meanings of state caps, interruptions, and unfinished branches.
- [Development history](development/README.md): original scripts, four-column/five-column graphs, and the 33/77 certificates confirmed to be rediscoveries.

Run in this directory using only the Python standard library:

```sh
sha256sum -c SHA256SUMS.txt
python3 verify_certificates.py
```

`SHA256SUMS.txt` preserves the delivered package's original byte inventory. The parent `proofs/MANIFEST.sha256` covers the complete inventory of the added navigation and historical materials.

Regenerate the certificates from scratch:

```sh
python3 generate_certificates.py
python3 verify_certificates.py
```

Independently replay the C++ long-prefix search; the complete argument also needs the Python verifier's short-number boundary checks:

```sh
g++ -O3 -std=c++17 extend_prefixes.cpp -o extend_prefixes
./extend_prefixes 7 1000000 < accepted_prefixes.txt
```

The research phase completed cross-checks between the two implementations and hash checks after certificate regeneration. Original file hashes were checked again at publication; committing the files was not described as a new independent mathematical review. The all-length interpretation of the finite certificates depends on the coverage lemmas in the complete proof, not on the integer scan alone.

Compiled binaries, Python caches, redundant ZIP packages, downloaded dependency copies, and upload helpers are not new research source; the publication inventory records their exclusion. All original research source, results, and existing exploration records are retained. This directory adds no claim that the main conjecture is proved, that the work is globally novel, or that external review occurred.
