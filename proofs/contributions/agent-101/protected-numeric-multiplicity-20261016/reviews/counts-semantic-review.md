# Independent review of protected-family integer multiplicity

## Verdict and independence

**PASS.** The reviewed module's statements match the complete union of ordinary-integer digit-split fibers of the specified protected profile family. The source-level argument establishes complete enumeration, distinctness within and between profiles, and the exact count `5 * 11 ^ m` for every natural `m` and `k`, including zero.

Reviewed source: `proofs/Agent101ProtectedMultiplicity.lean`.

```text
SHA-256 503dcb1c7d90f031a54caffb89ce8a632edbdc77c9383d06dbacfdbffaf0c1ac
```

The reviewer is the Agent #101 research-inventory worker. **I did not author this counting module. I previously authored `Agent101SplitEnumeration.lean`, one of its frozen dependencies.** This is an independent semantic review of the new counting source and the relevant Agent #3 enumeration interfaces, together with an independent fresh rebuild of the complete imported source closure. It is not an independent semantic review of my own enumeration module.

No mathematical source was modified, and no Git writes were performed. Source identity was checked before and after the rebuild.

## What is enumerated

The definition is:

```lean
protectedSeeds (m k : Nat) : List Nat :=
  (allBits m).flatMap fun xs => numericFiber (inputHalf xs k) none
```

The unchanged Agent #3 construction has:

```lean
choice false = 5
choice true  = 14
inputHalf xs k = [14] ++ xs.map choice ++ List.replicate k 18
inputWord xs k = inputHalf xs k ++ (inputHalf xs k).reverse
```

These entries are mirrored digit sums, not individual decimal digits. Each `numericFiber` enumerates all canonical ordinary-integer digit realizations of its entire mirrored profile, including every allowed ordered split of each pair. The optional center is `none`, so every input width is even.

`mem_protectedSeeds` gives a full biconditional with an arbitrary Boolean-list witness of length `m`. `mem_protectedSeeds_numeric` further replaces profile membership with the ordinary numerical specification:

```lean
n ∈ protectedSeeds m k ↔
  decimalWidth n (2 * (m + k + 1)) ∧
    ∃ xs : List Bool, xs.length = m ∧
      Lychrel196.step n = natValue (inputWord xs k)
```

The coefficient bound required by the numerical membership bridge is supplied explicitly by `coefficientWord_inputHalf_bounded`: every coefficient is at most 18. `natValue` here reads a positional coefficient value, so interpreting the unnormalized coefficient word as already bounded by 9 is unnecessary and would be incorrect.

The membership statements quantify over every natural number `n`; they do not assume that `n` came from a selected digit realization. Positivity is also proved for every member, using the canonical digit witness furnished by `mem_numericFiber_digits`.

## Completeness of the family indices

The pinned `FamilyCardinality.lean` defines `allBits 0 = [[]]` and builds `allBits (m + 1)` by prepending false and true to every shorter word. Its theorem

```lean
mem_allBits_iff (xs : List Bool) (m : Nat) :
  xs ∈ allBits m ↔ xs.length = m
```

proves completeness and excludes indices of other lengths. The inductive proof covers both Boolean constructors. `allBits_nodup` proves that each Boolean word occurs once: prepending preserves distinctness, and the false-headed and true-headed lists are disjoint.

The counting module uses these exact interfaces in `mem_protectedSeeds` and `protectedSeeds_nodup`. It does not substitute a smaller sampled family for all Boolean words of length `m`.

The two imported Agent #3 sources match the pinned provenance in `dependencies/agent3/provenance.json`:

| Module | Source SHA-256 |
|---|---|
| `FamilyDefinitions` | `497ffe833495c50e7df5714fd50c0a4835aaf96f71ec8d21fc43102b1468a1d4` |
| `FamilyCardinality` | `dfded4df411694fcbe50487e7a963f45c7e0abe34e46ed828926aee9f329248d` |

Their provenance is PR #81, source commit `5084eadce9a7e95e518332c29e8404b00214bd0f`; the recorded mathematical bytes are unchanged from `6576cee93d18145c638f298b0abcb1cd0a0f451e`.

## Distinctness and overlap

Within one profile, `numericFiber_nodup` supplies distinct ordinary integers.

Across profiles, `inputFiber_index_unique` starts from an ordinary integer in two fibers. Each membership supplies a canonical finite digit list representing that same integer. `natValue_injective_canonical` equates the two finite lists. Their complete pair-sum words are consequently equal, and the unchanged `inputWord_injective` recovers equality of their Boolean indices.

This proves disjointness for different `xs` at fixed `k`, even without separately assuming equal index lengths. It does not rely on equality of infinite digit functions, and it does not assume injectivity of a two-step reverse-add map. The subsequent `List.pairwise_flatMap` proof combines within-profile distinctness with this cross-profile disjointness. Therefore the list-length result is also the number of distinct ordinary integers in the stated family union.

## Exact factors

`length_inputFiber` specializes the previously proved complete profile multiplicity formula:

```lean
(numericFiber (inputHalf xs k) none).length =
  5 * natProduct (xs.map fun b => pairCount false (choice b))
```

The factors have the following meaning:

| Position | Prescribed sum | Exact number of splits |
|---|---:|---:|
| Outermost pair, positive high digit | 14 | 5 |
| Inner pair selected by false | 5 | 6 |
| Inner pair selected by true | 14 | 5 |
| Each protective pair | 18 | 1 |
| Absent central digit | none | 1 |

The outer condition is applied once. All inner pairs allow zero digits when compatible with their sum. The factor for each protective pair is one because the only decimal split of 18 is `(9, 9)`.

The recursive count over `allBits` sums the false and true branches. The two branch factors are 6 and 5, so each new index position multiplies the total by 11. The base count is 5. This establishes `length_protectedSeeds (m k) = 5 * 11 ^ m`. The argument accounts for the different individual fiber sizes; it does not multiply the number of Boolean indices by an assumed common fiber size.

## Zero boundaries and scope

The source theorems quantify over all natural `m` and `k` and contain no hidden positivity premise for this count.

| Boundary | Consequence checked against the definitions |
|---|---|
| `m = 0` | `allBits` contains exactly the empty word, so there is one profile and exactly five integer realizations. |
| `k = 0` | The protective list is empty and its product is one. The outer 14 remains, so the source width is positive and all count formulas remain valid. |
| `m = 0`, `k = 0` | The profile is `[14, 14]`, the width is 2, and the five integers are 59, 68, 77, 86, and 95. |
| `m = 1`, `k = 0` | The two fibers have sizes 30 and 25 and are disjoint, giving 55. |

The small integer descriptions above are direct arithmetic readings of the definitions; the universally quantified Lean proofs establish the boundary cases as part of the main theorem.

The theorem counts the union of complete integer fibers over exactly this profile family. It does **not** establish that this union exhausts every possible predecessor of the family's common later image. It also does not assert initial nonpalindromicity: for example, 77 is among the five width-two seeds at `m = k = 0`. Removing initial palindromes is a separate task. Finite-horizon transition or safety theorems retain their own positive-`k` hypotheses; the validity of this count at `k = 0` does not remove those hypotheses.

## Independent build and axiom audit

`counts-rebuild.py` created new empty source and build directories. It copied and hashed exact source bytes, then compiled all 10 non-Std modules in dependency order with Lean 4.19.0, `-j1`, and `--trust=0`. The only project import path was the new `counts-build` directory; no existing project `.olean` was reused.

The complete closure was:

1. `Lychrel196Research`
2. `Agent101DigitPairs`
3. `Agent101MultiplicityBounds`
4. `Agent101SplitEnumeration`
5. `Agent101NumericFibers`
6. `PeriodObstructions`
7. `ActualWordBridge`
8. `FamilyDefinitions`
9. `FamilyCardinality`
10. `Agent101ProtectedMultiplicity`

Every source compilation returned 0. The reviewed target compiled in approximately 2.13 seconds after its dependencies. The expensive original research module was also rebuilt from source, taking approximately 71.18 seconds.

`counts-Audit.lean` then imported the fresh target and checked all 18 public exports, comprising one definition and 17 theorems, with explicit `#print axioms`. This audit returned 0. Its axiom union is exactly `propext`, `Classical.choice`, and `Quot.sound`; the enumeration definition itself has no axioms. The target source contains no `sorry`, `admit`, `axiom`, or `native_decide` token.

Evidence is retained in `counts-source-registry.json`, `counts-build-results.json`, `counts-verification.json`, `counts-axioms.log`, each `counts-<module>.log`, and the exact `counts-sources` snapshots. `counts-verification.json` records commands, compiler identity, source and generated artifact hashes, actual exit codes, and the reviewer-independence disclosure.

No semantic defect or missing hypothesis was found in the reviewed count or membership endpoints.
