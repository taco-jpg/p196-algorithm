# Periodic parity author evidence

Frozen `proofs/Agent1PeriodicParity.lean`:
SHA256 `8eb97092e0c402f24e8163b51ed902f7e83f39b3c2a663698b08375147f2e129`;
Git blob `c5a2bfb004aa8421110403195abf9951572e7b4b`.

The four exports use the original `Agent8.pair`, `Agent8.zipAdd`, existing block powers, and executable center stripping. No arithmetic or validity predicate is replaced.

- `pair_middle_even D hodd`: the literal middle coefficient of `Agent8.pair D` is even at odd input length. The reversal index is exactly the same middle index; pairing therefore adds the middle digit to itself.
- `middle_append_eq P H S hPS hodd`: equal-length outside pieces leave an odd center's middle at the whole word's middle. This is an Option-index equality, not an assumption of symmetry.
- `stripPeriodCenter_even w H heven`: complete mirrored period-pair stripping preserves odd-middle parity, including the empty-period convention. Existing exact decomposition supplies equal-width sides; no symmetry, coefficient bound, or nonempty-period assumption is needed.
- `raw_center_even B H w hB hH hw hlen`: the literal exponent-three raw center is paired and hence has even odd-middle coefficient. Assumptions are only coefficient bounds18 and input period length4. It does not assume original center parity, symmetry, or positivity.

The prior general parity result is credited explicitly in source: `Agent112.Admissibility.pair_mirr`, preserved in `proofs/AdmissibleCenters__1024a5996f878a9e.lean`, blob `6366eaf4f5d16a8a1a999e7474c44239111e83e7`, SHA256 `7a7b9791e04994c8050606f211cac34b938ce8b63fa723ff54374c25eea97210`. It states the Agent109 pair map produces `Mirr`; `Agent109.Compat.pair_eq` already relates Agent8 and Agent109. The new module is the direct indexed compatibility glue needed by `ValidPeriodic`, avoiding an unnecessary certificate dependency, and makes no novelty claim for the general even-middle fact.

Executed author checks:

1. Exactly fourteen frozen prerequisite source/object pairs were copied from the prior checked parent strip build at `/workspace/p196-agent1-session-20261016/strip-parent-clean-001/agent1-periodic-quotient/source`. Each source was compared byte-for-byte to current pinned registry bytes and checked by SHA256. Every reused olean has its own hash in `reused-dependencies.json`. These dependencies were NOT rebuilt by this author for this task.
2. `compiler.json` records the actual Lean4.19.0 executable/version/SHA256 and source head. `attempt-001/` is the first and only proof compile; it contains the complete source snapshot, command, log, and exit0. No failed proof attempts occurred. All four literal axiom prints contain only the permitted standard axioms.
3. `audit-001/ParityAudit.lean` imports the accepted output and selects all declarations by actual module origin. All10 theorem/safe constants passed; there are zero unsafe implementation constants and no custom axiom. Transitive union is exactly `propext`, `Classical.choice`, `Quot.sound`. Full audit source, command, log, and result are retained.
4. Accepted-source forbidden-token scan passed. `frozen-receipt.json` records all results. No fresh complete dependency build or independent review is claimed by this author evidence; the parent will execute the separate combined fresh closure and review.

All executed Lean commands use `--trust=0 -j1 -DElab.async=false`. `run-attempt.py` is the exact source-preserving incremental compile driver used. For a full reproduction, stage the sources listed in `reused-dependencies.json` under their module names, compile them in registry dependency order in an empty directory, then compile the frozen Parity source with the command in `attempt-001/result.json` and run the audit command in `audit-001/result.json`. That fresh reproduction is distinct from the incremental checks recorded here.

This module alone does not establish full successor validity, positivity, safety, iteration at exponents below three, a safe cycle, or an infinite ordinary orbit. Parent owns the full validity assembly; the positivity specialist owns the remaining outside-head proof.
