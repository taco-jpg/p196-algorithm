# Independently reviewed publication

Status: **INDEPENDENTLY_REVIEWED**, awaiting designated default-branch integration.

For every positive ordinary decimal seed n and all natural B,s,N, the count of times t in the half-open interval [s,s+N) with digitSum(orbit n t)>B is at least floor(N/(sharpDigitSumEscapeBound B+1)). The original numeric orbit continues after palindromes. The zero threshold, zero start, and empty interval are included. The196 specialization is immediate from the positive-seed theorem.

The complete finite block count is proved through List.range' and filter, with distinct times and no duplicated adjacent endpoint. The source's inclusive escape window forces the denominator's +1. No pointwise convergence or real density-limit theorem is included.

## Evidence

The independent11module --trust=0 build checked1451 theorem constants and178 safe definitions. Every theorem and safe definition from all selected project modules was audited by originating module, including generated/private helpers; axiom union exactly propext/Classical.choice/Quot.sound. Source hashes and compiler hashes stayed unchanged. The standard library is the official installed Lean4.19.0 runtime, not a separately rebuilt standard-library source tree.

Independent semantic review: review/horizon-safety/full-closure/NUMERIC_REVIEW.md, SHA256 af48bf81665d2b7f966d657ec843d6ff2878d61bcc8245030df170a99a134dcd. It checks the exact ordinary-integer definitions, half-open endpoints, positive-seed premise, and all zero boundaries. A rejected review-only simplifier attempt remains retained as a failure; the corrected boundary check and full mathematical closure pass. No accepted proof uses sorry or compiler-trusted evaluation.

The author is genuine delegated specialist /root/coverage_census; independent review and build were executed by /root/horizon_safety. Parent /root read the generic and numeric source, coordinated ownership, and publishes via the existing GitHub account. No separate GitHub identity or external peer review is implied.

## Reproduction and preservation

Use the author command in README.md for literal exported-theorem checks. For the stronger full-closure gate, run review/horizon-safety/full-closure/verify_closure.py with its exact source-registry.json and a fresh output directory; the full explicit command is in NUMERIC_REVIEW.md. Both verifier and registry are readable directly.

Every substantive file, including sources, all author and independent logs, attempted review proofs, manifests, commands and failure records, is preserved losslessly in evidence/complete-source-and-verification.tar.xz. evidence/MANIFEST.json maps every original path to its byte count and SHA-256 and gives the exact recovery command. Original author MANIFEST.sha256 and reviewer SHA256SUMS retain their declared scopes. This added publication summary does not rewrite their historical evidence.

Source: strengthening_notes.txt section6 at2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5, blob7103ee939d82740b970dd23fb91e9db50db4ea54. Original9module dependency closure is unchanged and pinned. This is the exact finite counting step behind the source's density discussion; its real-limit statements remain open.

The next active task is agent9-escape-factorial-bound-20261016, claimed473a2865e2b3b4d7e8044b3537c9b94ba5ab18d1. No main integration slot is held.
