# Seven-column prefix research publication record

Date: 2026-10-15 (UTC). Baseline: `a71d6e79b009da691e2d97057f83e108a3fcff4f`.

This publication adds the [seven-column prefix research directory](../contributions/2026-10-15-seven-column-prefix/README.md). The full P196 conjecture remains unproved.

## Accepted conclusions and evidence

Every decimal palindrome whose first three digits are 739 has maximum ancestry depth `H(P) <= 39`. Together with the absence of palindromes at steps 0–39 from 196, this excludes that family from its orbit at every time. The uniform bounds for 217, 218, 620, and 777 also tighten to 23, 34, 12, and 25 respectively. The three-digit prefix catalogue grows from 396 classes to 397; this is not a completion percentage for the full conjecture.

The evidence consists of a written all-length coverage argument and five complete finite rank certificates. Python recomputes every predecessor, checks closure and ranks, and checks each edge with forward formulas; an independent C++ implementation checks the layer cardinalities for long prefixes. Regeneration from scratch produced matching certificate hashes. Cross-checks cover every short-source boundary, seven/eight-digit raw sum words, long words with fixed random seeds, and small-integer height calculations. See the [proof](../contributions/2026-10-15-seven-column-prefix/P196_739_Proof.md) and [verification records](../contributions/2026-10-15-seven-column-prefix/verification_results.json) for the precise scope and results. There was no Lean kernel check or external review.

## Historical materials and publication checks

The early 33 and 77 exclusions were confirmed to be existing repository results. Their original cross-check certificates and exploratory source remain in `development/` and are not new results. All existing original research files are retained, and capped or interrupted attempts remain labelled incomplete. Binaries, caches, redundant packages, and publication infrastructure are excluded for reasons recorded in the overall inventory.

Publication checked delivery-package SHA-256 hashes, exact copying of original research files, the publication inventory, and the scope of the Git changes; it did not perform another independent mathematical proof review. Existing research files remain unchanged. This publication also includes the already-existing `chat-6acee928/` files in the cumulative file and byte inventories: completion of historical indexing, not new research. The earlier chat archive had modified `proofs/README.md`, so its old cumulative hash is updated with this index.

Further work must still address every remaining target family, including the 55 and 770 branches, or establish a whole-orbit invariant excluding all palindromes. Local exclusions do not replace a complete P196 proof.
