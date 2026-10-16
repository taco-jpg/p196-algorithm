# Zero-period state helper: author checkpoint

Source: `proofs/Agent1PeriodicZeroState.lean`, frozen SHA-256 `9e80cfe62a227bc6f7f5468549d2e5f6e9cbf22a3e927ee769c13eb573550aa1`.

This helper was authored under the published Agent #1 zero-cycle claim `d5786f691f77c606f7343b1182cc67643f058a8f`. Only the assigned state module and this evidence directory were written; no Git state was changed. Parent owns the subsequent exponent and cycle-obstruction arguments.

The module imports `Agent1PeriodicZeroPeriod` and uses the original quotient operations with period literally `[0,0,0,0]`. It introduces `ZeroState := Word × Word`, the exact `zeroNext`, and the recursive `zeroStateOrbit`. Its five public theorems prove orbit addition, original validity propagation, reduction of a positive exact cycle to its first period, an explicit finite-prefix bound, and the requested uniform bound on both interface length and mass.

The public API includes:

```lean
zeroStateOrbit_valid s hv t

zeroStateOrbit_cycle_bounded s P hP hcycle :
  ∃ M, ∀ t,
    2 * (zeroStateOrbit s t).1.length + (zeroStateOrbit s t).2.length ≤ M ∧
    2 * (zeroStateOrbit s t).1.sum + (zeroStateOrbit s t).2.sum ≤ M
```

Here `hP : 0 < P` and `hcycle : zeroStateOrbit s P = s`. The bound requires no validity assumption: it is a finite-orbit consequence of a positive exact return. The witness is the sum, over the first `P` states, of the interface length plus interface mass. No cycle existence, integer realization, numeric orbit, or palindrome statement is added.

`attempt-001` compiled successfully on its first attempt with official Lean 4.19.0, commit `6caaee842e94`, using `--trust=0 -j1 -DElab.async=false` (0.428 seconds). This author increment reused the provided dependency objects at `/workspace/p196-agent1-session-20261016/periodic-zero-period-author-build`; it is **not** an independent fresh dependency rebuild. The exact imported source and object hashes are recorded in its receipt. The ZeroPeriod source matches frozen SHA-256 `3761744f62cabdf25cf69f8e2990ce81eec9ac75cfb2273a5e80974304795a8a`.

`audit-001` passed with the same strict flags (1.669 seconds). It prints all ten public declaration types and axioms, selects every theorem and safe definition by actual new-module origin, and traverses their logical axiom dependencies. The complete new-module audit covers **20 theorem constants** and **9 safe definitions**, including generated auxiliaries; there are zero safe opaque declarations. All 29 audited logical constants use only `propext`, `Classical.choice`, and `Quot.sound`.

Compiler metadata is separately inventoried: one unsafe implementation axiom for the specialized `List.sum`, 17 unsafe implementation definitions, and two partial `_unsafe_rec` implementations. These are not custom source axioms and do not occur in the audited logical axiom sets. The source scan found no active proof placeholders, custom axioms, or external proof-oracle tokens. No compile or audit failure occurred.

The importable state object is retained at `attempt-001/Agent1PeriodicZeroState.olean`. Its bytes are for local author continuation; publication may omit generated objects while preserving the source, hashes, commands, receipts, and logs. An independent full-closure build and final review are delegated to the parent workflow.

The source is frozen. `frozen-receipt.json` records final source/object hashes and source consistency after audit.
