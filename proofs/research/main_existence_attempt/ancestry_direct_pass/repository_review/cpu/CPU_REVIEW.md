# Archived v8 CPU arithmetic and replay review

14 October 2026. **PASS for the finite tests described here.** No arithmetic,
palindrome-detection, or replay discrepancy was found in these tests.
This is not a proof of all-input correctness or of decimal Lychrel existence.

## Source and execution scope

Repository: [taco-jpg/p196-algorithm](https://github.com/taco-jpg/p196-algorithm),
review checkout identified by commit
`8219522a02d46fbb72a6ee38819e5723b8c8fc9f`. This review used the extracted
**v8 archive**, identified by Git blob
`3e105424f94ced716d9d145ac8c4af95b9b91bac`, at

    /workspace/scratch/fe6abe1df721/p196-repo-review/v8/lychrel196_v8

The source was inspected before compilation and execution. Its instructions
and agent task file were not treated as authority. No upstream source was
modified or copied into this research directory. Test inputs, binaries,
logs, and outputs are isolated under this directory.

Compiler: GNU g++ 13.3.0. Emulator builds used `-O2 -std=c++17 -fopenmp`,
`TB_CHECK_HYBRID`, and `TB_CHECK_GROWTH`, with `TB_J=8` and `TB_J=16`.
Tests ran with `EMU_CERTCHECK=1` and two OpenMP threads. Individual emulator
calls had a 45-second timeout. No CUDA compiler or CUDA hardware was used.
**v9 was not tested.** Per-file and binary SHA-256 values are recorded in
`provenance.json`; Git object identifiers above are not SHA-256 values.

## What the algorithm actually checks

`bits_core.h` stores one representative from each mirrored digit-pair sum
in five bit planes. It calculates the low and high carry chains using
generate/propagate masks. It handles no-overflow and overflow alignments
separately, including the changed center on even-width overflow.

The no-overflow palindrome vote compares the two incoming carries at each
mirrored pair. The overflow vote compares the newly aligned output digits.
These are per-step tests. They are not merely checks at saved checkpoints.

The time-blocked code tracks certified data intervals. The v8 hybrid path
also uses a prefix-derived growth tape and propagates certified spans
between register windows. In the driver, any failed certification or
palindrome flag restores the window backup and replays it with the
per-step implementation. On a palindrome report, the driver materializes
the actual decimal value and checks its symmetry again.

The emulator exercises shared arithmetic routines and a sequential model
of thread/barrier phases. Passing it does not establish GPU scheduling,
memory ordering, generated-instruction correctness, or speed.

## Independent arithmetic primitive checks

`check_core.cpp` includes the unmodified upstream `bits_core.h` but uses
its own schoolbook decimal addition oracle, input encoding, expected pair
calculation, and palindrome test. For every input it checks:

- Every word's growth bit against the actual change in decimal width.
- Every output pair sum against the schoolbook next integer.
- The OR of all mismatch votes against that integer's palindromicity.

Coverage: **1,000,579 inputs passed**:

- All 999,999 positive integers below one million.
- 500 random long inputs across 20 selected widths from 31 to 4,097 digits.
- 80 inputs with pair-sum-9 carry runs spanning the full width, with
  different central carry-generation cases.

The selected widths include odd/even centers and positions around
32-pair word boundaries. Results are in `core_results.json`.

## Strict driver and replay checks

`check_engines.py` uses Python integer arithmetic as an independent oracle.
For a terminating case it checks the **earliest** hit, exit code 3, reported
iteration including the supplied starting offset, exact palindrome-file
contents, and the driver's `cpu_check=PASS`. Otherwise it requires exit
code 0 and exact final output. Intermediate checkpoint contents and labels
are checked separately. Matching failures never count as a pass.

The final matrix contained **88 successful cases**, using:

- Per-step execution with batch 7.
- The older time-blocked path with hybrid disabled, `K=7`.
- The v8 hybrid path with `J=8,K=64` and `J=16,K=33`.
- Tiles 4, 8, and 32, nonmatching window lengths, and input widths from
  1 to 16,001 digits.

Known delayed-hit controls included 89 (24 steps), 10911 (55 steps), and
1186060307891929990 (261 steps), independently recalculated. Four generated
8,000-digit inputs reached their first palindrome at step 3 while hybrid
blocks were active, tested under both hybrid configurations. Thirty-two
of the 88 cases terminated at a verified first palindrome. Other cases
checked 196 through 500 steps, checkpoint boundaries, planted long carry
chains, and a prefix-growth detector stress pattern.

The instrumentation totals were:

| Measured item | Count |
|---|---:|
| Certified blocks checked against the per-step path | 7,768 |
| Blocks failing certification | 395 |
| Hybrid blocks executed | 531 |
| Hybrid blocks failing certification | 229 |
| Certified hybrid blocks cross-checked against the older path | 302 |
| Cross-checked block-steps with no mismatch vote | 250 |
| Window replay messages | 74 |
| Certification soundness violations | 0 |

The harness explicitly requires failed certifications, failed hybrid
blocks, successful cross-checks, and quiet block-steps to occur. Thus the
replay and interior-vote paths were exercised, not inferred from zero
failures. Exact case records and log paths are in `engine_results.json`.

One CLI detail affected test setup: benchmark positional `K` takes
precedence over `--K`; per-step mode also sets its batch from positional
`K`. The final harness supplies consistent values and verifies the
reported `K`, rather than assuming flag order determines the configuration.

## Weaknesses in the supplied test assertions

These are source-level observations, not observed arithmetic failures:

- `tests/diff_engines.py` accepts matching nonzero return codes as an
  identical result. Two matching crashes/errors, or two different
  palindrome outputs both returning 3, can pass that assertion.
- In the return-code-3 branch, `tests/test_growth_edge.py` checks for a
  palindrome file's existence and substitutes the expected result; it
  does not validate that file's value or first-hit iteration.
- `tests/pal_later.py` checks the reported iteration but does not require
  the success return code or verify the palindrome-file contents.

The supplied `test_exact.py` has stronger value and first-hit assertions.
The independent harness here closes the three listed assertion gaps for
its own cases. The supplied scripts were inspected; their published
aggregate pass counts were not adopted as this review's measurements.

## Reproduction and limits

From this review directory, obtain the pinned upstream archive (access to
this private repository is required). These commands create temporary source
files and do not modify the upstream checkout:

```sh
review_source_tmp=$(mktemp -d)
git clone --no-checkout https://github.com/taco-jpg/p196-algorithm.git "$review_source_tmp/repo"
git -C "$review_source_tmp/repo" show 8219522a02d46fbb72a6ee38819e5723b8c8fc9f:lychrel196_v8.zip > "$review_source_tmp/v8.zip"
python3 -m zipfile -e "$review_source_tmp/v8.zip" "$review_source_tmp/extracted"
v8_source="$review_source_tmp/extracted/lychrel196_v8"
```

Then compile and run:

    mkdir -p bin

    g++ -O2 -std=c++17 -I"$v8_source" check_core.cpp -o bin/check_core
    bin/check_core > core_results.json
    g++ -O2 -std=c++17 -fopenmp -DTB_CHECK_HYBRID -DTB_CHECK_GROWTH "$v8_source/emu196_v8.cpp" -o bin/emu_v8_j8
    g++ -O2 -std=c++17 -fopenmp -DTB_CHECK_HYBRID -DTB_CHECK_GROWTH -DTB_J=16 "$v8_source/emu196_v8.cpp" -o bin/emu_v8_j16
    python check_engines.py > engine_run.log 2>&1

Each integration replay creates a new isolated work subdirectory. No
production checkpoint was written. The bundled 4,942,464-iteration
checkpoint's claimed ancestry was not certified; this review used
independently generated inputs. Run-mode writer behavior, restart/crash
durability, hardware performance, extreme-size memory bounds, arbitrary
invalid CLI arguments, other `TB_J` values, and v9 remain outside this
execution scope. The finite tests are not a formal verification of the
interval certification implementation.

The algorithm is useful for exact finite orbit extension and tested
palindrome detection. Neither its compressed representation nor a long
successful run supplies an all-time palindrome-avoidance proof.

All compilation and test subprocesses have finished. Nothing was
published and no upstream repository mutation was performed.
