# Independent audit of the finite collision-driver trace

**Result: PASS for all 10,000 saved states, covering driver times 0 through
9,999. Mathematical status remains UNKNOWN beyond that finite horizon.**

The audited data are the original lossless compressed trace and corrected
summary in [`../2026-10-14-collision-review/`](../2026-10-14-collision-review/).
The trace is referenced in place; this contribution neither changes nor
duplicates its 29,648,893 compressed bytes.

## What was checked

[`verify_driver_trace.py`](verify_driver_trace.py) imports no search code. It
reads each binary record sequentially and independently checks:

1. The eight-byte magic, complete record boundaries, contiguous times, exact
   initial words, and absence of trailing partial records.
2. Every saved word's positive endpoint, coefficient range 0 through 18,
   reflection symmetry, and even central coefficient when its length is odd.
3. Every one of the 9,999 saved transitions, including the cumulative spacer
   loss. Normalization explicitly transfers tens to the next coefficient.
4. Both exact predecessor-class predicates, all category counts, the first-hit
   report, every checkpoint, and every optional exceptional-state witness.
5. Saved-state count and horizon, final **tested** widths, compressed byte
   count and SHA-256, and binary format metadata. An additional SHA-256 covers
   the uncompressed binary stream.

For the central transition, let the normalized core word have length
\(m+f\), let the exterior overflow be \(e\), and put
\(\delta=\max(e,f)\). The verifier constructs

\[
W=0^{\delta-e}\,N(H)\,0^{\delta-f},\qquad H'=W+W^R.
\]

The length of \(W\) is \(m+2\delta-e\). Its reflected nonzero positions
give the same prescribed polynomial recurrence as the searcher. This
padding-and-reflection implementation is separate from the searcher's two
index-update loops. The exterior transition independently adds the
normalized exterior word to its reversal.

## Verified finite results

| Quantity | Verified value |
|---|---:|
| Saved states | 10,000 |
| Saved transitions | 9,999 |
| Last saved driver time | 9,999 |
| Cumulative spacer loss at last saved state | 5,077 |
| Last tested exterior width | 4,131 |
| Last tested core width | 6,030 |
| Both blocks safe | 9,990 |
| Exterior alone bad | 9 |
| Core alone bad | 1 |
| Both bad, different overflow classes | 0 |
| Both bad, same overflow class | 0 |

The exterior's bad times are exactly
\(\{0,1,2,3,9,10,16,26,33\}\); the core's only bad time is \(5\).
Here “bad” means membership in the exact predecessor class used in the
separated-block criterion. All other uses of that criterion remain subject
to its stated separation hypotheses.

Compressed trace SHA-256:

```text
6431d3a11008f81e9249f05187e207a73f9f1dc0e87c897e46030f2a16b02404
```

Uncompressed stream: 50,997,008 bytes; SHA-256:

```text
bb3e02a3b1f14278eaad67a7242aa56352516fd7434e59198a71fef9b5f2d7ab
```

The complete machine-readable audit is in
[`verification.json`](verification.json).

## Corrected reporting error

The initial search summary reported widths 4,132 and 6,031. Those were the
widths **after** the final loop update, at the unsaved successor time 10,000.
The last saved and classified state is time 9,999, with widths 4,131 and
6,030. This off-by-one reporting error did not affect the trace, category
counts, recorded horizon, or no-hit result.

The search now captures `last_tested_widths` before performing the update.
Its existing summary was corrected directly from the final saved record;
no longer search was run. The independent verifier confirms the correction
and labels the computed successor widths only as an untested diagnostic.

## Reproduction and verifier checks

From the repository root, using standard-library Python:

```bash
python -B proofs/contributions/2026-10-14-collision-audit/verify_driver_trace.py
python -B proofs/contributions/2026-10-14-collision-audit/test_verifier.py
```

The first command rewrites only its small `verification.json` report. The
second uses temporary two-state, hand-computed fixtures. All 16 fixtures
pass: valid input is accepted, while wrong initial states, valid-looking
wrong transitions, inadmissible words, loss errors, duplicate times,
truncations, and incorrect summary fields are rejected or reported as
summary mismatches. Details are in
[`verifier_tests.json`](verifier_tests.json).

This is an independent finite computational certificate check. It does not
establish any all-time driver invariant, describe evolution after spacer
collision, or prove the P196 conjecture. No conclusion about later driver
times follows from the absence of a hit in this trace.
