# Independent review of the external raw-symmetry module

This package independently reviews the exact external source at commit
`4c3970c04f7997db76f82a5806168b2d0790cfb3` of
`taco-jpg/p196-algorithm`. The target is
`proofs/research/main_existence_attempt/renewal_pass/lean/raw_symmetry/RawSymmetryObstruction.lean`,
SHA-256 `922b660e5b3ac42389cd6ea00885075327d4b44fb315b9cc496e1323890e9c87`.

The written mathematical review and fresh machine audit both **PASS**. Lean
4.19.0 checked all 42 target theorems; their transitive axiom sets contain only
the three standard axioms allowed below. Fresh compilation took 70.59 seconds
for the decimal dependency, 1.70 seconds for incoming carry, 3.27 seconds for
the target, and 0.96 seconds for the axiom audit. The reproducible machine
result is recorded separately in `independent_verification.json`; a rerun is
successful only when that file states `PASS_FRESH_EXACT_SOURCE_42`.

## Exact scope

The target contains 42 theorem declarations. The independent checker rebuilds
the unchanged `LychrelDigitSums`, `IncomingCarrySensitivity`, and target sources
in a new, initially empty temporary directory, then asks Lean for the transitive
axioms of every target theorem. It permits only `propext`, `Classical.choice`,
and `Quot.sound`. It separately rejects `sorry`, `admit`, source axiom
declarations, and `native_decide` in all three local sources. The import chain
is checked exactly and ends at Lean's `Std` library.

This is a fresh audit of those 42 target declarations and their used dependency
closure. It is not an audit of all 135 declarations in the wider external
renewal contribution, and it does not independently enumerate all theorems in
the decimal dependency. The preserved upstream checker and report are
provenance, not the implementation of this independent check.

All three source files, the external status note, its checker, and its report
are preserved byte for byte in `sources/`. `source_manifest.json` records their
original paths, exact commit, byte counts, SHA-256 digests, and Git blob SHA-1
digests. The snapshot was obtained by the publishing agent using exact Git
blob verification; this checker verifies both kinds of digest again before
and after compilation. No prebuilt local `.olean` is reused, and temporary
compiled objects are deleted when the checker exits. Runtime binaries are
not included.

## Mathematical review

The formalization represents a finite partition by a Boolean cut function.
The isolated incoming carry resets to zero at each cut, and the first incoming
carry is zero regardless of the initial cut bit. `resetOut_on_block` proves
that the recurrence on a delimited block is its ordinary normalization from
zero. `rawCoeff_is_placed_sum`, `resetRaw_lt`, and `resetRaw_terminal` include
all placed terminal carries, so the baseline is the actual raw sum of isolated
block normalizations, rather than a truncated digit word.

For a symmetric coefficient word with entries in `0..18`, symmetry of that raw
baseline at the **actual next width** forces agreement of every actual and
isolated outgoing carry. The proof handles both width branches:

- Without final overflow, carry domination removes the isolated terminal
  carry. Exact value conservation and bounded symmetric-word injectivity force
  equality of the raw word and input word. The column equation then forces
  every isolated carry to vanish and every input coefficient to be at most 9.
- With final overflow, the complete raw reflection equations imply a finite
  backwards recurrence. Zero extension proves its terminal boundary, and the
  local normalized-remainder bounds force all coefficients to lie in
  `{0,11}` and all carries to agree. The separately named arithmetic auxiliary
  theorem assumes a terminal boundary; the main raw theorem derives it and
  does not inherit an unproved boundary assumption.

The admissible and canonical bridges then use the exact immediate-palindrome
classification. The canonical hypothesis supplies positivity and the integer
digit realization; no claim about arbitrary unrealizable odd centers is
needed. The algebraic rigidity theorem itself does not need this canonical
hypothesis.

The positive safety corollary has the intended stronger scope: a nonzero
actual-minus-isolated outgoing carry at any column within the word excludes
both immediate-palindrome classes. It therefore certifies a nonpalindromic
next ordinary reverse-and-add output **without assuming raw symmetry**. This
is exactly `numeric_nonzero_defect_safe`, not a converse inferred from the
raw-symmetry theorem. The concrete witness uses seed `99900`, partition
`(9,9)|(18)|(9,9)`, defect 1 at column 3, and next value `100899`.

These are one-step theorems. They neither regenerate a nonzero defect nor
prove an infinite safe orbit, decimal Lychrel existence, or the behavior of
the seed 196 for all time. The external status note states these limits
correctly.

## Reproduction

From this directory, with a working Lean 4.19.0 executable:

```sh
python check_independent.py /path/to/lean
```

In the review environment the exact invocation was:

```sh
python check_independent.py \
  /workspace/scratch/fe6abe1df721/lean-runtime/lean-4.19.0-linux/bin/lean \
  --preload /tmp/p196-lean-compat/readlink_self.so
```

The existing compatibility shim redirects only the runtime's self-executable
path lookup; it does not modify Lean's kernel. All builds use `-j1` and
`-DElab.async=false`. Full compiler output is retained in `logs/`, and the
generated 42-command axiom audit is retained in `Audit42.lean`. The checker
overwrites the previous result with `RUNNING` before starting and records
`FAIL` on an exception, so a failed rerun cannot leave an old `PASS` result.
