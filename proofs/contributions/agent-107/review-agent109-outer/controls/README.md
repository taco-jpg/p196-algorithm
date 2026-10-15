# Independent exact-integer controls

**PASS.** One deterministic Python run checked 10,944 actual ordinary-integer
trajectories, seven updates each, with no mismatch. These are bounded arithmetic
controls for the independent review of source
`b2374410d427beb78fc601ee81cf15e34a1ac934`, not a new proof or Lean rebuild.

The initial exterior domain contains every valid normalized word `B` of length
at most two for each of the eight even phases `2,4,...,16`: 2,736 `(c,B)` states.
For each state the run uses four fixed interface/center choices, including empty
blocks, odd centers, and even centers. All initial bands have `g=h=14`.

Each initial symmetric coefficient word is explicitly split into decimal digits
with a nonzero leading digit, valid central parity, and exact original width.
The program checks that the realized integer's pair word equals the entire
initial template before taking any step. Actual iteration is literally
`n + int(str(n)[::-1])`, including the discarded leading zeroes of a reversed
integer whose units digit is zero. There are 5,472 initial zero-units examples.

The quotient implementation was written independently from equations (1),
(3)-(8) and section 6 of the pinned `METHOD_AND_PROOF.md`. It imports no author
implementation. Its block normalizer evaluates a block as an integer and divides
by its decimal place value; it does not copy the author's recursive normalizer.
Only the maximal `B` suffix is stripped. The raw `A` and `C` interfaces are
retained, matching the representation used by `OuterBridge.lean`.

At every update the controls compare the written output digit word to the
canonical decimal digits of the actual new integer, check the full pair word
against the returned template, verify the physical-width overflow bit, and
compare the raw outer prefix to an exterior-only computation. At every time
0 through 7 the chosen phase/exterior equals its independently iterated exterior
coordinate; all coefficients, center parity, leading exterior, suffix trimming,
and finite band budgets are checked.

| Result | Count |
|---|---:|
| Initial exterior states | 2,736 |
| Canonical initial realizations / trajectories | 10,944 |
| Actual transitions | 76,608 |
| Nonoverflow transitions | 45,368 |
| Overflow transitions | 31,240 |
| Mismatches | 0 |

Every configured trajectory has a selected exterior longer than two by time
seven. First-exit counts at times 1 through 7 are respectively
`7744, 2084, 776, 240, 72, 24, 4`. The four time-seven trajectories have the
same initial exterior `(c,B)=(14,(2,17))` and different interface/center choices.
The observed minimum band at time seven is one; no update from a source outside
the required `g,h>=2` domain is used.

## Reproduction and retained evidence

From the review worktree root, using a checkout of the pinned source:

```sh
python3 -B proofs/contributions/agent-107/review-agent109-outer/controls/independent_integer_controls.py --source-root /absolute/path/to/pinned-source --output /absolute/path/to/control-output
```

`report.json` records exact counts, source/formula SHA-256 identities, Python
version, source commit, configuration, and the script/transcript digests.
`trajectories.jsonl.gz` retains every actual integer and selected template at
every recorded time, with deterministic gzip metadata. `sample_trajectories.json`
contains the eight empty-interface exterior examples and the sharp time-seven
example. `failures.json` is empty. `run.log` is the successful command output;
the process returned exit code zero. `archive_check.json` separately records
the decompressed archive count and hash check without rerunning the experiment.

The experiment uses no random generator or seed. It covers one explicit digit
realization and four interfaces per initial exterior, not every interface or
every realization. Exit refers only to this constructed maximally B-trimmed
coordinate; uniqueness over all template decompositions is not asserted.
There is no all-time, safe-orbit, cycle, palindrome-hit, or P196 conclusion.
