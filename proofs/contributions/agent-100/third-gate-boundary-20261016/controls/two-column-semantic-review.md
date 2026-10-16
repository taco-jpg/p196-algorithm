# Two-column overflow / no-overflow: independent semantic review

**Source-semantic review PASS; finite execution PASS.** This review concerns the eight generic lemmas in `Agent100ThirdGateBoundary.lean` at SHA-256 `7f6992f08e7f7b75e0a609d54a64f9ac7c2b80344296761be111e740ef48a96c`. It does not claim an independent Lean rebuild. The formal task was claimed by the parent at coordination `2a0d376388cacc83ceab1caf1f2152c195329964`; the older scout artifacts retain their historical PRECLAIM status.

## Why the two columns suffice

The hypotheses retain the actual `Admissible L q`: positive width and outer coefficient, all represented coefficients at most 18, reflection symmetry, and an even odd-center coefficient. With `L>=2`, symmetry identifies the penultimate input coefficient with `q(1)`. Every incoming carry is at most 1. Therefore `q(1)<=8` resets the carry into the final column to 0, while `q(1)>=10` forces it to 1. Neither assertion needs any out-of-width value.

For prefix `(16,z)` with `z<=1`, the first terminal carry is 1 and the next pair prefix is `(7,7+z)`. The new second coefficient is at most 8. For prefix `(16,16+z)` with `z<=1`, the terminal carry is likewise 1 and the next prefix is `(7,14+z)`, whose second coefficient is at least 10. In either case the actual successor is admissible by the existing `admissible_next` theorem. Its outer coefficient 7 makes the second normalization non-overflowing. The carry into its final column then gives the next outer coefficient 14 or 15 respectively. Actual widths follow `L, L+1, L+1`.

These local lemmas are sufficient as stated. There is no need to strengthen `L>=2`, introduce a minimum interior gap, or assume all interior carries vanish. They are conditional statements; some small-width prefix combinations have no admissible realization.

## Small-width feasibility

| Hypotheses | Width 2 | Width 3 | Width at least 4 |
| --- | --- | --- | --- |
| `(16,z)`, `z=0` | Empty by symmetry | `[16,0,16]` | Realizable |
| `(16,z)`, `z=1` | Empty by symmetry | Empty: odd center | Realizable |
| `(16,16+z)`, `z=0` | `[16,16]` | `[16,16,16]` | Realizable |
| `(16,16+z)`, `z=1` | Empty by symmetry | Empty: odd center | Realizable |
| Outer 7, second at most 8 | Only `[7,7]` | Second must be even | Realizable |
| Outer 7, second at least 10 | Empty by symmetry | Second must be even | Realizable |

In particular, the high-prefix width-two case is not entirely empty: `97 -> 176 -> 847` realizes pair words `[16,16] -> [7,14,7] -> [15,8,15]`. The low-prefix width-three case is `907 -> 1616 -> 7777`, with outer pair coefficients 16,7,14. These are ordinary integer computations, not new kernel-checked theorems.

The digit-center parity hypothesis is needed for ordinary realizability, even though the local bounded-carry arithmetic itself does not rely on it. The source keeps that semantic boundary by using `Admissible` throughout.

## Why the excluded neutral value matters

The first two columns cannot decide the final carry when the second coefficient is 9. Both `[7,9,0,9,7]` and `[7,9,10,9,7]` are admissible width-five words with the same first two columns. Their next outer coefficients are respectively 14 and 15. Ordinary representatives are `70090 -> 79097` and `70590 -> 80097`. Thus neither low nor high conclusion can simply include second coefficient 9.

The low initial bound `z<=1` also cannot be relaxed to `z<=2` without more information: `[16,2,0,2,16]` has two-step outer coefficient 14, whereas `[16,2,18,2,16]` has two-step outer coefficient 15. Both have the same width and first two columns. Width five is the first possible such counterexample: width two contradicts symmetry, width three permits only `[16,2,16]`, and width four only `[16,2,2,16]`; the latter two have outer 14 after two steps. No widening of the current theorem scope is proposed.

## Independent exhaustive finite controls

The standalone Python source uses no project or external package dependency. For every width 2 through 10 it enumerates all admissible symmetric words with prefixes `(16,0)`, `(16,1)`, `(16,16)`, `(16,17)`, and all outer-7 words whose second coefficient is in `0..8` or `10..18`. All free independent coefficients range over `0..18`; an odd center ranges over `0,2,...,18`. This is full enumeration of these restricted finite profile sets, not all admissible words.

| Family | Profiles checked |
| --- | ---: |
| Outer 16, second 0 or 1 | 22,101 |
| Outer 16, second 16 or 17 | 22,102 |
| Outer 7, second 0 through 8 | 99,456 |
| Outer 7, second 10 through 18 | 99,455 |
| **Total** | **243,114** |

One canonical ordinary integer is constructed for each profile. Its next one or two values are computed by integer addition to decimal string reversal and checked digit-for-digit against a separate grade-school coefficient normalizer. All successor admissibility, incoming carry, terminal carry, width, prefix, and outer-coefficient assertions passed. This involved 287,317 ordinary additions. These controls do not quantify over all digit splits or all widths; the Lean statements supply those universal scopes.

Run from the repository root:

```sh
python proofs/contributions/agent-100/third-gate-boundary-20261016/controls/two_column_controls.py > proofs/contributions/agent-100/third-gate-boundary-20261016/controls/two-column-controls.log
python proofs/contributions/agent-100/third-gate-boundary-20261016/controls/two_column_examples.py > proofs/contributions/agent-100/third-gate-boundary-20261016/controls/two-column-examples.log
```

The full 243,114-record trace is `two-column-cases.jsonl.gz`, deterministic gzip with timestamp zero. Stored size 3,519,679 bytes; SHA-256 `77809423c7b365cf8ee2784e9fe7b62eb7f9518e09329be755b568e7bcb5a7dd`. Decoded size 48,028,259 bytes; SHA-256 `8fb2a448bb9f19905cecccb914a047d5fd114ea144fb0bfbbd51e7d6be5e1abc`. `two-column-summary.json` records every finite group count, every empty group, representative traces, and exact payload/source hashes.

No counterexample to the currently stated generic lemmas was found. The required adjustment is in interpretation: report empty small-width cells explicitly, retain `z<=1` for the low two-step conclusion, and do not describe the neutral second coefficient 9 as tail-independent. Final Lean source review and independent execution evidence remain separate.
