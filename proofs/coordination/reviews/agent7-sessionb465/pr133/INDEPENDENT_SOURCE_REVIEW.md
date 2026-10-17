# PR #133 independent semantic and source review

## Decision and provenance

**PASS for the advertised finite one-step window and uniform sharpness by explicit witnesses. No new mathematical source is required.**

This report was written by Agent #7's independent review specialist, separately from both Agent #5 source authors and Agent #7's execution owner. The reviewer authored neither mathematical module and made no source-branch or remote changes. This is independent subordinate review, not GitHub approval, a claim of a separate platform account, or a merge result.

- Repository: https://github.com/taco-jpg/p196-algorithm
- PR: https://github.com/taco-jpg/p196-algorithm/pull/133
- Exact reviewed head: 9b1535d80ab3cb32d131306f089bcf524482ab09
- Stacked prerequisite, PR #121 head: 5c4d394f20b70547aa7cb8dd14091bcd391e424c
- Delivery owner: Agent #7, according to the parent's assignment.
- Active source writer: original Agent #5; no ownership takeover.
- Main writer: Agent #31 / session 02893e4f368d, according to the parent's live assignment.
- Execution owner: Agent #7 parent. This reviewer did not launch a duplicate Lean build.
- Fresh execution evidence: independently examined in EXECUTION_REVIEW.md and EXECUTION_BINDING.json.

The reviewer read both new modules completely, the README, executable registry, provenance/status records, original verifier, and all fifteen pinned prerequisite modules. Exact-H GitHub responses were retrieved independently and retained under remote/. They were compared byte for byte with the parent's isolated exact-H checkout. SOURCE_BINDING.json records every identity, import list, and endpoint binding.

## Exact identities and build binding

| Item | Git blob | SHA-256 |
|---|---|---|
| StreamAgreementWindow.lean, 209 lines | 6880fd23341a06ffa22a2c3735cb29836998485c | 023c5c692fbdc66a67faba66eb2b3c76082f4b25def9a69b53e4a65527d59899 |
| StreamWindowSharpness.lean, 246 lines | 2bdab169701d258a1961a2d505e4f7c3dcd8a53c | b0b0cfbc7e716071e2011f3ab0e80848223bd833f20770db1803b5c2e6a6d006 |
| Agent5StreamAgreementWindow.registry.json | 7d04008967b35aacb39594b45a2ed1b9ac5329ae | ad27c0f8d503ea7e322e3e436c0a7ab7ec4b0190b857193b0525511297714a93 |

Sources: [general window](https://github.com/taco-jpg/p196-algorithm/blob/9b1535d80ab3cb32d131306f089bcf524482ab09/proofs/contributions/agent-5/stream-agreement-window-20261016/StreamAgreementWindow.lean), [sharpness](https://github.com/taco-jpg/p196-algorithm/blob/9b1535d80ab3cb32d131306f089bcf524482ab09/proofs/contributions/agent-5/stream-agreement-window-20261016/StreamWindowSharpness.lean), [registry](https://github.com/taco-jpg/p196-algorithm/blob/9b1535d80ab3cb32d131306f089bcf524482ab09/proofs/Agent5StreamAgreementWindow.registry.json).

The roots are StreamAgreementWindow and StreamWindowSharpness; each imports OrdinaryStreamStep directly. Their exact union closure is seventeen modules:

OuterFinite, TARGET, ExteriorFactorizationProof, DigitDefinitions, AdicDigits, FractionDigits, CoordinateStreams, CoordinateThreshold, CoordinateOnlyStreams, ExteriorCore, ExteriorBridge, ExteriorProjection, ExteriorArithmetic, RawPrefixStreams, OrdinaryStreamStep, StreamAgreementWindow, and StreamWindowSharpness.

The independent binding check establishes:

1. Every actual source SHA-256 and Git blob equals its registry pin.
2. Each independently retrieved exact-H response has the same bytes and blob.
3. Every actual import list equals its registry declaration.
4. The roots reach all seventeen modules, with no extra registered module and no cycle.
5. All fifteen prerequisites are byte-identical at PR #121's exact base head.
6. The twenty-six registry endpoints equal the top-level declarations of the roots exactly once: seven general theorems, seventeen sharpness theorems, and two definitions.
7. Comment/string-masked accepted-source inspection finds no prohibited proof token. This source check is supplemented by the parent's actual transitive axiom audit.

No adapter is present. Historical failed attempt sources remain outside these roots and do not enter the accepted closure.

## Definitions and hypotheses

All words are List Nat; digit words use little-endian order. The inspected definitions are:

- paired D = List.zipWith Nat.add D D.reverse: raw mirrored-sum coefficients, not normalized decimal digits.
- surrounded B c g W = B ++ replicate (g+2) c ++ W ++ replicate (g+2) c ++ B.reverse.
- norm and normalize both emit (x+carry) % 10 and recurse with (x+carry) / 10. The unchanged normalize7_eq_norm6 identifies their entire output pair for every word and incoming natural carry.
- normalizedDigits appends the actual final carry if nonzero.
- reverseAddDigits D = normalizedDigits (paired D).
- Coefficients X means every entry is at most 18.
- nonneutralPhase c means membership in [2,4,6,8,10,12,14,16].
- Nonneutral c means 0 < c, c ≤ 17, and c ≠ 9.
- DecimalDigits D means every entry is less than 10.
- PositiveLast D means D = front ++ [last] for some last > 0.
- numeral [] = 0 and numeral (x :: xs) = x + 10 * numeral xs.

The coordinate-window statements assume the eight-phase predicate, coefficient bounds on B and W, and exact equality paired D = surrounded B c gap W. They do not assert that every arbitrary bounded B,W is realizable by an ordinary input. The shape premise retains that obligation. Raw list statements need no DecimalDigits or PositiveLast premise; the numerical wrapper adds both.

With n = B.length, lowValue B is the low-first sum Σ B_i 10^i, and

    zValue c B = 9 * lowValue B - c * (10^n - 1)    in Int.

highValue B reads the same coefficients high-first, and

    rhoNum c B = 9 * highValue B + c              in Nat.

The low stream uses adicNumeratorDigits N (zValue c B - (c : Int)). The subtraction is integer subtraction. The recurrence chooses d = ((-a) % 10).toNat and continues at (a - 9*d)/10. The high stream is literal long division, emitting 10*r / D and recursing with 10*r % D. The actual definitions and their correspondence proofs were inspected, rather than inferring semantics from theorem names.

Relevant definitions occur in TARGET, DigitDefinitions, ExteriorCore, ExteriorBridge, ExteriorProjection, and ExteriorArithmetic. The complete normalizer/stream proofs and coordinate threshold interface were also read.

## General finite window: all seven theorems

All names in the table belong to Agent5.OrdinaryStreamWindow.

| Theorem | Exact role |
|---|---|
| take_prefix_replicate | Extracts L ++ replicate q t from L ++ replicate m t ++ M when q ≤ m. |
| paired_bands_window | Combines protected ends under e ≤ 1 and L.length = R.length+1; permitted extension q ≤ gap+e. |
| surrounded_raw_exterior_window | Uses the original whole-word normalization and actual carry under bounded B,W and the broader original Nonneutral predicate. |
| ordinary_raw_prefix_from_normalized_streams_window | Applies the exact shape and unchanged literal stream identities with the actual normalizer carry. |
| ordinary_raw_prefix_from_streams_window | Replaces actual outgoing carry by the exact coordinate threshold. |
| ordinary_raw_prefix_from_streams_window_quotient | Replaces the carry by rhoNum c B / (9*10^n) in both the bound and denominator exponent. |
| ordinary_reverse_add_from_streams_window | Adds decimal, positive-last, and numerical-value conclusions using the original arithmetic theorem. |

Set

    gamma = if 9 * 10^n ≤ rhoNum c B then 1 else 0.

For every natural q with q ≤ gap+gamma, the first n+1+q entries of paired (reverseAddDigits D) equal the coordinatewise sum of

    adicNumeratorDigits (n+1+q) (zValue c B - (c : Int))
    fractionDigits (n+1+q) (rhoNum c B) (9*10^n*10^gamma).

This covers every allowed q, including zero and the maximal extension. It does not merely assert the endpoint cutoff. The sum is raw and untrimmed; entries may exceed 9. No trim, stripSuffix, validOuter, positive exterior head, or canonical exterior suffix assumption appears.

### Why the bound is correct

surrounded_normalization exposes a low boundary block of length n+1, gap+1 stable digits, the normalized middle plus one boundary digit, gap+1 stable digits, a high block of length n, and the actual final carry.

If that carry is zero, the high prefix of length n+1 consumes n high-block digits plus one stable digit. It leaves gap stable high digits. If the carry is one, the carry supplies the extra first digit, leaving gap+1 stable high digits. The low side always retains gap+1 after its first n+1 entries. Their common guaranteed extension is gap+gamma. The source explicitly checks both carry cases and each take bound.

The quotient identity needs c ≤ 17 and c ≠ 9, supplied by the eight-phase predicate. Bounded B makes the outgoing carry a bit. The threshold theorem then identifies it with gamma. The outgoing carry can differ from the initial phase carry if 10 ≤ c then 1 else 0; those two quantities are kept distinct.

### Boundary cases and ordinary values

B=[] and W=[] are allowed by the quantified statements and proofs. gap=0 is allowed. Zero gap still gives original phase bands of length two and normalized stable bands of length one; zero-length phase bands are not claimed to satisfy the theorem. The finite extension itself may have length zero.

The ordinary wrapper assumes DecimalDigits D and PositiveLast D and obtains decimal output, positive last output digit, the value equation

    numeral (reverseAddDigits D) = numeral D + numeral D.reverse,

and the prefix identity. The original PositiveLast predicate excludes the empty input and zero most significant digit. Reversing a canonical input can create a list with most-significant zeros when the original number ends in zero; numeral handles that finite list without changing ordinary reversal value. Output canonicality and value are reused from reverseAddDigits_correct, with unchanged hypotheses.

## Uniform sharpness: exact all-gap witnesses

The two actual definitions have the requested offsets:

    D0(g) = replicate (g+2) 1 ++ [9] ++ replicate (g+2) 1
    D1(g) = replicate (g+2) 5 ++ [0] ++ replicate (g+2) 5.

All seventeen theorems in Agent5.OrdinaryStreamWindow.Sharpness are complete:

| Theorems | Meaning |
|---|---|
| D0_decimal, D1_decimal | Decimal entries for every natural g. |
| D0_positive_last, D1_positive_last | Positive final digits 1 and 5. |
| D0_paired, D1_paired | Exact shapes surrounded [] 2 g [18] and surrounded [] 10 g [0]. |
| D0_reverseAddDigits, D1_reverseAddDigits | Complete normalized ordinary output words. |
| D0_first_excluded_prefix, D1_first_excluded_prefix | Actual pair prefixes at the first excluded cutoff. |
| empty_exterior_carry_controls | Actual carry and coordinate selector are 0 for (2,[]) and 1 for (10,[]). |
| D0_coordinate_streams, D1_coordinate_streams | Literal stream predictions at those same cutoffs. |
| D0_stream_mismatch, D1_stream_mismatch | All-gap actual-prefix/stream inequality. |
| gap_zero_actual_prefixes, gap_zero_stream_prefixes | Explicit minimal-gap comparisons. |

The complete output formulas are

    reverseAddDigits (D0 g) =
      replicate (g+2) 2 ++ [8,3] ++ replicate (g+1) 2

    reverseAddDigits (D1 g) =
      [0] ++ replicate (g+2) 1 ++ [0] ++ replicate (g+2) 1.

For an empty exterior, zValue c []=0 and rhoNum c []=c. Thus the low numerators are -2 and -10 and high denominators are 9 and 90, using the actual selectors.

| Branch | Last guaranteed length | First excluded length | Actual paired prefix | Stream prediction |
|---|---:|---:|---|---|
| gamma=0, B=[], c=2, W=[18] | g+1 | g+2 | replicate (g+1) 4 ++ [5] | replicate (g+2) 4 |
| gamma=1, B=[], c=10, W=[0] | g+2 | g+3 | [1] ++ replicate (g+1) 2 ++ [1] | [1] ++ replicate (g+2) 2 |

In the first case, q=g+1 exceeds the q≤g bound by one, giving final coefficient 5 rather than 4. In the second, q=g+2 exceeds q≤g+1 by one, giving 1 rather than 2. Both sides have equal finite lengths; neither mismatch is caused by unequal length or truncation.

At g=0, the canonical ordinary inputs are 11911 and 55055. The actual prefixes are [4,5] and [1,2,1], whereas the predictions are [4,4] and [1,2,2]. These controls specialize the universal formulas and do not replace their all-gap proofs.

The witnesses show that the guaranteed window cannot be uniformly increased by one column over all admissible inputs, in either carry branch. They do not assert that every middle, phase, exterior length, or individual input fails at its next column. The README correctly says other middles can agree farther.

## Concrete findings and required action

### Stale live PR description

The independently retrieved PR body still calls the sharpness families intended witnesses and says the literal comparisons are finishing. Exact-H source already contains both coordinate-stream formulas and both mismatch proofs. The README/status files correctly distinguish source completion from then-pending combined audit/full replay.

The live description and current task status should be updated by the authorized writer to reflect the actual source and execution state. This is a metadata defect, not a missing mathematical proof. No duplicate sharpness implementation is justified.

The retained CHECKPOINT.json, original CLAIM.json, failed author attempt 001, and historical ownership survey have explicit historical roles. Earlier WIP or failure records should remain preserved and should not be treated as current accepted proof defects.

### Verification provenance

At H, checked-in metadata marks the parent full-package replay NOT_RUN_FOR_THIS_PACKAGE. The general-window author evidence used fifteen inherited dependency objects and checked seven exports. Those assertions alone do not establish a fresh seventeen-module result.

The parent's newly executed strict replay supplies separate new evidence. Its actual receipt, command sequence, full-origin axiom audit, and supplementary endpoint audit are qualified in EXECUTION_REVIEW.md. No source author's compile assertion is promoted into an execution performed by this reviewer.

### No mathematical repair required

No missing hypothesis, off-by-one error, altered canonical family, unproved endpoint, wrong denominator, freely selected carry, hidden trimming, or finite-to-infinite inference was found.

The inherited TARGET header says WIP/outside accepted builds while its body defines coordinates and a proposition and ExteriorFactorizationProof proves that proposition. The actual closure imports those definitions and the proof. That historical comment is not an admitted theorem or a new PR133 mathematical defect and does not justify editing an actively owned prerequisite.

## Scope and delivery handoff

The result is finite and one-step under an explicit input shape. Universality over all natural gaps does not prove that subsequent ordinary outputs keep this shape. Nothing here proves infinite safety, a Lychrel existence result, an all-time result for 196, or global acyclicity.

Agent #7 remains responsible for delivery through the acknowledged writers: publish the scoped independent evidence, correct live metadata while retaining historical records, process the stacked PR #121 prerequisite, and qualify the actual combined target/platform gates before any Ready or merge action. This reviewer performed no remote mutation.

Retained evidence comprises SOURCE_BINDING.json, check_source_binding.py, remote exact-H responses, and the separate EXECUTION_REVIEW.md / EXECUTION_BINDING.json. The report is source-specific and does not assert repository-wide completeness or integration into main.

