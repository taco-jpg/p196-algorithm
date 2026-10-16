# Kernel-checked counterexample to eight-word reconstruction

## Certified conclusion

`Agent10EightCarryCounterexample.lean` proves that the two canonical width-17 inputs

- `n = 90000000560706169`,
- `m = 90000000806235169`

have identical complete carry words at observation times `0` through `7`, including every terminal overflow carry, although their active initial pair sums and their next ordinary integers differ. The proof uses the unchanged decimal definitions `Canonical`, `columnSum`, `carry`, `iterPairs`, `Lychrel196.step`, and `Lychrel196.orbit`.

The exact initial symmetric pair words are:

```text
q = [18,6,1,6,0,7,0,6,10,6,0,7,0,6,1,6,18]
r = [18,6,1,5,3,2,6,0,16,0,6,2,3,5,1,6,18]
```

The differing active coefficient is index `3`, where `q 3 = 6` and `r 3 = 5`. The next integers are respectively `186160707060706178` and `186153261606235178`.

The first carry separation is at time `8`: carry index `4` is `1` on the left and `0` on the right. Both widths at that time are `21`, so the separating index is in range. The widths at times `0` through `8` are exactly `[17,18,19,20,20,20,20,21,21]`.

This is a result about unrestricted continued iteration. Both inputs first reach decimal palindromes at time `4`, namely `16999899899899899961` and `16989989999998998961`. Their exact values, palindrome status, and absence of earlier palindromes are proved in the same module. No palindrome-avoidance assertion or claim about 196 is made. A matching uniform upper bound is a separate theorem composed by the parent.

## Carry trace

Each string below lists carries in increasing index order, beginning with index `0` and ending with the terminal carry. Times `0` through `7` have the same entire string on both sides.

| Time | Width | Common complete carry word |
|---:|---:|---|
| 0 | 17 | `010000000100000001` |
| 1 | 18 | `0010000000000000011` |
| 2 | 19 | `01011111111111111101` |
| 3 | 20 | `000000000000000000000` |
| 4 | 20 | `001111111111111111110` |
| 5 | 20 | `000111111111111111100` |
| 6 | 20 | `011111111111111111111` |
| 7 | 21 | `0001111111111111111100` |

At time `8`, the left word is `0000110010010010011000` and the right word is `0000001001111100100000`. The full ordinary-integer, digit, pair-sum, and carry trace is retained in `thrice-padded-width17-001/first_eight_integer_replay.json`.

## Proof interface

All public declarations use namespace `Agent10EightCarryCounterexample`.

| Endpoint | Scope |
|---|---|
| `left_canonical`, `right_canonical` | Exact width-17 digit representations of both ordinary integers. |
| `left_widths`, `right_widths`, `widths_agree` | Actual widths for all times at most eight. |
| `eight_complete_carries` | For every `t < 8` and every `i ≤` the current left width, the actual carries coincide. |
| `initial_pair_sums_differ` | Index three has exact values six and five. |
| `initial_pair_difference_active` | Index three is less than seventeen and the two values differ. |
| `next_integer_values`, `next_integers_differ` | Exact unequal values of the next ordinary reverse-and-add step. |
| `numeric_orbit_representations` | Canonical ordinary-orbit semantics for the carried recursion, at every time at most eight. |
| `ninth_carry_differs` | At time eight, carry index four is one versus zero. |
| `first_separation_at_eight` | All earlier complete words agree and an in-range carry differs at time eight. |
| `eight_carry_counterexample` | Combined canonical-input, eight-word agreement, pair-sum inequality, and next-integer inequality theorem. |
| `palindrome_values_at_four`, `first_palindromes_at_four` | Exact first palindrome time and values for both inputs. |

The source records nine finite pair-sum rows. Kernel-evaluated certificates verify both initial representations, every adjacent actual `nextWidth`/`nextColumns` step, all carry equalities, and the finite palindrome prefix. The finite step domain uses `Fin 21`, while the complete carry domain uses `Fin 22`, so a terminal carry at index 21 is included. Existing finite-prefix congruence transports the checked rows to the original `iterPairs` recursion.

## Lean verification

The source compiled successfully on its first attempt using pinned Lean `4.19.0`, with `--trust=0 -j1 -DElab.async=false`. An additional exhaustive module-origin audit also passed with those flags. The source imports only `ActualCarryObservability`; its three-module dependency closure uses the original standalone `Lychrel196Research` foundation.

- **48** unique theorem declarations, including generated declarations.
- **16** public endpoint types, each checked and matched to its explicit source `#print axioms` output.
- The theorem axiom union is exactly `{propext, Quot.sound}`.
- No custom axioms, unsafe implementation declarations, `sorry`, or `native_decide` are used.
- All six finite kernel certificates are axiom-free.
- The exact canonical, numeric, initial active-difference, and first-palindrome facts are axiom-free.

The build and audit were executed by `Agent #10 specialist /root/formalization_scout`. The parent will execute the combined canonical project gate separately. A different specialist performed read-only arithmetic and source review; that review is separate from this compilation.

| Evidence | SHA-256 |
|---|---|
| `Agent10EightCarryCounterexample.lean` | `5da46ec31d7641307a6d8c1a5f81bd3b8bdfb097a39b5afa73145e062683d739` |
| Successful module log | `c63ccbb205dd0694df6cc6d71d154b94b476b155cadf4aa9cd58d033ce3a1c0f` |
| Exhaustive audit log | `874992d4d85a5998bfecd6a6c941e08b47da64de8fda044185da733f2dd1956d` |
| `eight-check-001/verification.json` | `a8d15217f76a963a09a6f5913f57959796181447895a17048fac0be765a62471` |

The source Git blob is `4868157b5c3005c8ec1eaae75b34e35579932e9a`. The source and compiled `.olean` are staged in `/workspace/scratch/4b20b8469eb3/agent10-count/eight-check-001/source`. The frozen source itself is `/workspace/scratch/4b20b8469eb3/agent10-count/Agent10EightCarryCounterexample.lean`.

## Computational discovery, retained separately

The source was found by an exhaustive lift of the 1,326 surviving five-coordinate prefixes. Every one of the `1,326×16,562 = 21,961,212` symmetric, center-even width-17 completions was tested using unchanged actual decimal simulation. CSV sample bit paths did not restrict actual trajectories.

| Matched complete words after the prefix filter | Surviving completions |
|---:|---:|
| 0 | 21,961,212 |
| 1 | 1,864,832 |
| 2 | 696,818 |
| 3 | 515,311 |
| 4 | 282,685 |
| 5 | 156,113 |
| 6 | 41,090 |
| 7 | 1,094 |
| 8 | **32** |

All 32 eight-word matches have overflow pattern `OOONNNON`. The compiled scan took 4.892462 elapsed seconds and peaked at 11,392 KiB resident memory. Its retained top-level artifacts occupied 210,643 bytes before adding the receipt; no repository copy was made.

The computational prefix inclusion has not been formalized, so the global exhaustiveness of this filtered search remains computational. The positive concrete example and its Lean certificate do not depend on that filter or the search program.

All lift evidence is in `/workspace/scratch/4b20b8469eb3/agent10-count/thrice-padded-width17-001`:

| Artifact | SHA-256 |
|---|---|
| `thrice_padded_witness_scan.cpp` | `fb0fe5be8ebaf49584f522b868842fcb7527ec43e5998af351ac85f59d0e089c` |
| Unchanged `actual_simulator.inc` | `e2bd06376e0f2309ec80e0a5ad3b1e5468e9f612fa72f3b79a4448205ac5f349` |
| `result.json` | `9b47c40ded89c714da4578e51b1af66e45772621506ab10af91cfc672a679ede` |
| `first_eight_integer_replay.json` | `b53c756862d5ad9d64fff1111ce2a29ef8265e8267c1111e5e9594a98aea73f6` |
| `lift_verification.json` | `0bbcbd9a79af6263bddece64381f93e3459347baebd27a636f1df7dd1e288810` |
