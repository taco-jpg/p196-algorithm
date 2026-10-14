# Independent rebuild of the published delayed overlap gate

**Result: PASS. All six project modules compile, and all 49 theorem axiom
sets match the published report exactly.**

This audit targets immutable commit
[`7c699a370198a3e306524948f468ba319c620b18`](https://github.com/taco-jpg/p196-algorithm/commit/7c699a370198a3e306524948f468ba319c620b18),
specifically
[`DelayedOverlapGate.lean`](https://github.com/taco-jpg/p196-algorithm/blob/7c699a370198a3e306524948f468ba319c620b18/proofs/research/main_existence_attempt/renewal_pass/lean/DelayedOverlapGate.lean).
The source SHA-256 is:

```text
c24d7774af6487fcab63a4d60cd10aaabb1b270b3dc0f4ac42dd3655b416b112
```

## Independent verification

The checker in this directory fetches nothing during compilation and does
not execute or alter the other contributor's `check.py`. Its inputs were
retrieved separately through the GitHub connector at the exact commit ref.
Every staged source was checked against the remote Git blob SHA and its
SHA-256. The immutable paths, sizes, and hashes are recorded in
[`source_manifest.json`](source_manifest.json).

[`recheck.py`](recheck.py) rebuilds all six project modules in a newly created
temporary directory:

1. `LychrelDigitSums`
2. `SafeDelay`
3. `DecimalSafeRuns`
4. `DecimalDelayBridge`
5. `PairDelayBridge`
6. `DelayedOverlapGate`

No previously compiled project `.olean` files are imported. Lean's standard
library remains the installed Lean 4.19.0 distribution. The checker discovers
all 49 theorem declarations from the gate source, independently generates a
`#print axioms` command for each, and verifies that the declaration list
matches the published `AllAxioms.lean`. It requires every transitive axiom
set to contain only `propext`, `Quot.sound`, and `Classical.choice`, and
compares all 49 exact sets with the published report. It also excludes
`sorry`, `admit`, `native_decide`, explicit `axiom`, and `sorryAx` tokens from
the gate's uncommented source, then checks that input files remained
unchanged throughout the build.

The machine-readable result is [`verification.json`](verification.json);
the compiler and all axiom outputs are preserved in
[`compile.log`](compile.log).

## Scope of the checked result

The gate holds for all natural parameters satisfying

\[
r\ge1,\qquad 1\le p\le4,\qquad u\ge1,\qquad v\ge5,\qquad u+v\le8.
\]

The checked statements include the exact two-step overlap repair, the
coefficient and normalized-digit defects, actual decimal realization, safety
of positive ordinary steps 1 and 2, and the exact third-step criterion

\[
\operatorname{Palindrome}(\operatorname{orbit}(n,3))
\iff p\le2\ \land\ u=1\ \land\ v=5.
\]

These are parameter-uniform Lean proofs, not a numerical search over sample
values of `r`. Their time horizon is finite. The same file explicitly proves
that the returned parameters
\((4p,4u+1,4v-19)\) lie outside the gate's parameter domain. Thus this result
does not supply an indefinitely repeatable gate, an all-time safe orbit, or
a proof of decimal Lychrel existence or P196.

## Reproduce

Use a checkout containing the pinned original source paths and Lean 4.19.0:

```bash
python -B proofs/contributions/2026-10-14-external-gate-audit/recheck.py \
  --lean /absolute/path/to/lean
```

For independently retrieved flat inputs, append
`--source-dir /absolute/path/to/staged-sources`. All source hashes are checked
before compilation. Only this audit's own small report and log are written;
temporary build products are discarded.

In the audit environment, numeric `/proc/<own PID>/exe` lookup is denied,
although `/proc/self/exe` works. A small libc `readlink` compatibility adapter
redirected only that one own-process path lookup to `/proc/self/exe`.
It changed no Lean source, parser, elaborator, kernel, or library. The
adapter had previously passed a positive axiom-free theorem check and
rejected an attempted proof of `False`. A normal Lean installation needs
no adapter.

The earlier local copies used in a separate build had one extra terminal
newline in four dependency files. Byte comparisons showed no other
difference. This audit nevertheless rebuilt the exact remote bytes rather
than reusing those earlier build artifacts.
