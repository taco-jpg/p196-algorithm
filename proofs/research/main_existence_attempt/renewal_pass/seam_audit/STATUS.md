# Independent seam audit: active seams certify one-step safety

**For any canonical whole decimal pair word and any block partition,
nonzero seam correction K certifies that the next reverse-add output is
nonpalindromic.** This is a realizable one-step safety test; no symmetry
hypothesis on the raw isolated digits E is needed.

The whole-block seam identity and mass-iff theorem are correct. The previously
considered extra condition that E be symmetric is impossible when K is
nonzero, and was unnecessarily restricting the useful criterion.

For the raw sum E of isolated normalized blocks, actual whole digits D,
and seam correction K in `D=E+(x-10)K`, the audit proves:

`E symmetric in actual width <=> D symmetric in actual width`.

Whenever these equivalent conditions hold, K=0. Without overflow they
force every whole input coefficient to be at most 9. With overflow they
force every coefficient to be 0 or 11, with outer coefficient 11. These
are exactly the two palindrome-predecessor cases, not safe collision states.

The proof applies to arbitrary partitions, including reflection-symmetric
lists of symmetric blocks and BHB. The unrestricted overflow argument reduces
to a nine-row local arithmetic relation: every finite path from state zero
back to zero stays at zero and emits only coefficients 0 or 11. Full
definitions, the coefficient bridge and both overflow cases are in
`METHOD_AND_PROOF.md`.

An explicit active collision has B=(9,9), H=(18), so
`Q=BHB=(9,9,18,9,9)` and `K=x^3+x^4`. A canonical realization gives
`99900 -> 100899`, a nonpalindromic output. More generally, an active seam
supplies both a coefficient 9 and an earlier coefficient at least 10,
excluding both exact palindrome-predecessor classes.

The criterion is sufficient, not necessary. For example
`22900 -> 23822` is safe although its pair word `(2,2,18,2,2)` has no 9s
and K=0 under every partition.

Independent checks pass:

- all 2,737 original seam controls, including 1,767 canonical ordinary-integer
  controls and 645 nonzero corrections;
- all 608 possible local arithmetic tuples, leaving nine valid rows and
  four rows on zero-to-zero paths;
- all 3,969 canonical whole words of widths one through five under all
  58,221 consecutive block partitions;
- a separate replay of every short control using decimal conversion and
  polynomial division, with exact independent coverage and class counts.
- all 395 canonical nonzero-K cases in the original archive (91 without
  overflow, 304 with overflow) and all 2,100 in the short archive, with
  independently reconstructed seam masks and ordinary integer outputs.

The short archive contains 2,100 nonzero corrections. Its 8,122 nonoverflowing
and 54 overflowing symmetric-E cases all have K=0. These finite counts audit
the implementation; the proof covers arbitrary widths and arbitrary block
counts.

Two explicit nonsymmetric whole-word examples have symmetric E and nonzero
K, one for each overflow flag. They confirm that the general algebraic
implication is valid but unusable on the canonical pair-word domain.
They are retained in `noncanonical_examples.json`.

The original report, including its explicitly uninstantiated proposal, is
preserved in `source_SEAM_RESPONSE_snapshot.md`. All probes, exact inputs,
responses and logs are retained, including the corrected serialization error.
No finalized language report was modified. The remaining recurrence
obligation is to regenerate nonzero K, or another valid safety certificate,
at every future update. One active collision alone does not prove that
coverage. No positive invariant, recurrent reset or Lychrel result is claimed.

Reproduce from this directory:

```sh
python3 -B audit_seam.py
python3 -B check_overflow_local.py
python3 -B check_short_controls.py
python3 -B check_positive_safety.py
```

The first command independently replays the source archive and regenerates
the full compressed short-control record. The next two check the local
certificate and that archive without importing any generator. The final
command preserves all 2,495 active canonical controls and both explicit
examples in `positive_safety_controls.json.gz`.
