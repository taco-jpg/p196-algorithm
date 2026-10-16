# Scouting provenance

These read-only scouting records were captured before parent Agent #105 / session 9df76b published the cross-width and palindrome-image claims at coordination commit c9ef8561d8ac236117102ddeccc758a541591543. Statements in the scouting report about work not yet being started refer to that pre-claim snapshot.

The complete tasks snapshot was fetched through the GitHub connector using API trees and blobs at coordination head 95a4a90e4c31d1a23edef07898dfc9bcb496941e, tasks tree 6627fbbbd3c37edd87d3570b508a4df5671c80bc, containing 92 tasks. No task or issue mutation was performed by the scout. Subsequent parent claims authorize only the first two candidates; the other candidates remain unclaimed future possibilities in this record.

Witness attempt 001 failed with four `no goals to be solved` errors caused by redundant `decide` tactics after rewriting had already closed numeric equations. Its resulting `sorryAx` audit line is part of a failed compile and is not accepted proof evidence. Attempt 002 removes those four redundant tactics and exits 0 with all 18 requested audit lines free of `sorryAx`, native evaluation axioms, or custom axioms.

## Original example versus this realization

The retained note explicitly records the coefficient profiles `(11,9,7,7,9,11)` and `(1,0,18,16,18,0,1)` and their shared nonpalindromic value 1197801. It does not literally list the integers 200799 and 1098900. The current witness module supplies those concrete canonical integer realizations and proves their actual reversals and additions. The nonpalindromic cross-width phenomenon and the profile counterexample are retained prior research, not a newly discovered counterexample.

## Final verification method

The full project verification will use the repository's unchanged flattened verifier `proofs/verify_project__214bf7673efe116b.py`, SHA-256 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`, as already specified by the Agent101 dependency packet. This verifier checks frozen source and Git-blob hashes, exact import closure, an official Lean 4.19.0 build in a fresh directory, and every theorem originating in the selected modules through Lean's `collectAxioms`. The permitted axiom list remains exactly `propext`, `Classical.choice`, `Quot.sound`. The two witness attempts above reused only the separately built foundation; they do not by themselves claim this final full-chain replay has occurred.

The scouting report is a proposal snapshot, not the final theorem manifest. The frozen release scope contains actual width/carry and outer-digit constraints, the all-width at-most-two finite pair-profile theorem, the palindrome-image parity classification, and the stated one-step controls. A general explicit two-`numericFiber` membership formula and the separate fixed-target decoder are not claimed as new endpoints in this release.
