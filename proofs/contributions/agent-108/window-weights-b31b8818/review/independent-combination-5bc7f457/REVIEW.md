# Independent latest-weight combination review

**Disposition: PASS.**

Reviewer: Agent #108 claims_inventory, separate from the source authors within the same session and authenticated account.

This is a distinct verification from the earlier endpoint review using Weight snapshot 4dab41a5. Here the parent's expanded nine-declaration Weight module is fixed to **5bc7f457187ad0af4a4f7a340acf7f827b8e89537d73624519805d232c762eae**.

## Fixed closure and actual execution

The other files are unchanged:

- Defs: 147ae208dce3b612c6eb23091eab123b77bd46c86d216ab8a6199913015f0aa0.
- Products: 2920c9da6e3c06c40a1d8478fe1af0d87b00627976f53856f75b90de32a1e584.
- Endpoints: ebabfbfd366729846656ff5a56891c22f9c7f0868fca9c5918be433e5d5fbc22.
- EndpointWeights: 21355018606cf7c2cfe8c33a008be815bd546bbafc31be69bc428624de0acab1.

All five exact files were rebuilt from a new empty directory using Lean 4.19.0 with **--trust=0**. All five compilation commands and the independent audit exited zero. All **37 public source declarations** were audited. Every transitive axiom reported was propext, Classical.choice or Quot.sound; no unexpected axiom was found. Source copies, hashes, commands and literal output are retained beside this review.

## Expanded Weight module review

The existing windowProduct and PositivePotential definitions remain unchanged in mathematical meaning. In particular, positivity is required only for lists of actual width b+1 over coefficients 0..18.

The expanded module's six additional public theorems were checked semantically:

1. **window_mem_valid:** membership in the complete window list forces length b+1 and transfers membership of every window entry to the original word. An empty window list cannot furnish an invalid witness.
2. **positive_list_product:** a finite mapped product is positive when each factor at a list member is positive; the empty product is 1.
3. **windowProduct_pos:** bounded input coefficients together with PositivePotential give positive windowProduct. Short inputs have the empty product 1, with no false promise of a padded window.
4. **windowProduct_single:** an input of length exactly b+1 has exactly one complete window, equal to the input.
5. **windows_replicate:** a constant word of length n has exactly n−b complete width-(b+1) windows, all constant. Nat subtraction gives zero windows when n≤b.
6. **windowProduct_replicate:** applies that list identity to give the corresponding potential raised to n−b; zero exponent is preserved.

None of these facts assumes a coefficient bound for a purely combinatorial constant-word identity. The bound is used only where PositivePotential must be applied. No arbitrary-list positivity assumption was substituted for the intended fixed legal-window potential class.

The endpoint semantic review in ../independent-endpoints-21355018-02/REVIEW.md applies unchanged to the two fixed endpoint source files. The new combination proves they continue to elaborate and kernel-check against the expanded Weight module. This review does not extend to a later FamilyProducts source, global weighted-family ratio, or actual buffered arithmetic interface.

## Evidence boundary

build-results.json lists all 37 public declarations and all commands. source/ and logs/ are the exact independent snapshot and outputs. REVIEW_MANIFEST.json records their byte hashes. The earlier dependency-drift guard stopped before any Lean command and is retained separately; no unsuccessful attempt was overwritten.

No author proof source was edited during this review.
