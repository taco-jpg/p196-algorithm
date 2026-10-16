# Original development and rediscovery records

This directory preserves verbatim the original research scripts, parameter lists, outputs, and early certificates from this working session. Filenames and contents were not retrospectively corrected. The proof, generator, verifier, and certificates in the parent directory define the five finally accepted results.

The 33 and 77 certificates in `p196_continuation/` were independently reconstructed before the original repository was reread. The corresponding conclusions were later confirmed to exist in the four-column and six-column reports, so these are historical cross-check materials, **not new results of this contribution**. `find_33.py`, `study_33.py`, and `sharp_first_33.py` belong to the same phase.

`graph4_rank.json` and `graph5_rank.json` preserve complete early graph results; they are not exhaustive certificates for the full seven-column graph. `prefix_graph_forward.py`, `prefix_inverse_fast.py`, and the other predecessor scripts preserve development of the model. `prefix_original.py` and `inverse_original.py` were extracted and reconstructed from archived arguments; see Section 1 of the parent proof for the cited baseline.

`extend_prefixes.cpp` is the historical exploratory version; the parent directory's file of the same name is the final version with width checks for 3–7 columns. Early code and generators may depend on the original working-directory layout and may overwrite outputs; study them only in isolated copies. Routine reproduction uses the parent's standalone generator and verifier.

The length of a parameter list does not establish that a search finished. See the [final exploration notes](../exploration/README.md) for the actual completed scope, CAP outcomes, and interruptions in each `seven_column_*.jsonl` file. Identical logs are retained here and in the parent directory as verbatim snapshots of the original and final delivery layouts, not as two independent experiments.

No unsaved terminal output was reconstructed, and no unfinished search was rewritten as an exclusion result.
