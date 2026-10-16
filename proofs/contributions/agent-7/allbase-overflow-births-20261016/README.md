# Actual all-base overflow births

Status: INDEPENDENTLY REVIEWED / canonical project verification PASS. All13 frozen modules,33 new public endpoints and338 module-origin theorem constants are checked. This scoped acceptance does not constitute a repository-wide build or main integration.

Agent #7 owns task `agent7-allbase-overflow-births-20261016`, claimed at coordination commit `cc9c01d128808d9c0b2b1cf3921a76f7c00e9cf1`. The initial claim and ownership census remain in `SCOPE.json` and `scope/`; current proof and execution status are recorded here and in the development reports. `OverflowEndpoints.lean` splits the already-claimed endpoint obligation into its own module.

## Mathematical statement

Let `b : Int` with `2 ≤ b`, and let `xs` be a finite tagged coefficient word of length `L`. Its original coefficient bound is `0 ≤ q_j ≤ 2*b-2`, its coefficient projection is reverse-symmetric, and the original ordinary normalization has computed terminal carry one. Write `q_j = xs[j].1`, `c_j = ActualBaseBirths.incoming b xs j`, and `Q = ReverseAdd.pairs (PhysicalWidth.actualDigits b xs)`.

The actual output has length `L+1`. At every interior position `0 < i < L`,

```
Q[i] = (q_i + c_i) % b + (q_(i-1) + c_(L-i)) % b.
```

The shifted reflection index is `L-i`. Both carries are the original recursively computed carries. With `a=q_(i-1)`, `z=q_i`, `u=c_i`, and `v=c_(L-i)`, the exact alternatives are:

| Row | `Q[i] = 0` | `Q[i] = 2*b-2` |
| --- | --- | --- |
| 1 | `a=0`, `z=0` | `a=2*b-2`, `z=2*b-2` |
| 2 | `a=b-1`, `z=b-1`, `u=v=1` | `a=b-1`, `z=b-1`, `u=v=0` |
| 3 | `a=b-1`, `z=b`, `u=0` | `a=b-1`, `z=b-2`, `u=1` |
| 4 | `a=b`, `z=b-1`, `v=0` | `a=b-2`, `z=b-1`, `v=1` |

Consequently, any new interior extreme that does not come from the corresponding homogeneous old extreme pair requires an old neutral neighbor: `a=b-1` or `z=b-1`.

Both genuine endpoints satisfy `Q[0] = Q[L] = 1 + q_0 % b`. They are positive for every base at least two. Under the original coefficient bound, either endpoint is maximal exactly when `b=2` and `q_0=1`. For `b ≥ 3`, endpoint nonextremity requires neither coefficient symmetry nor coefficient bounds; the remainder bounds suffice.

`canonical_reverse_add_overflow_theorem` specializes these facts to the unchanged canonical finite digit interface: `DigitBounds b digits`, `PositiveLast digits`, `xs.map Prod.fst = pairs digits`, and computed ordinary terminal carry one. It derives coefficient bounds and symmetry from that literal projection. It also retains the original digit bounds, positive high digit, output width `digits.length+1`, and numerical equality from `ReverseAdd.reverse_add_normalization`. Width one is covered; its interior quantifier is empty and its two endpoints remain explicit.

## Source structure and attribution

| Module | Obligation | New public theorems | Author |
| --- | --- | ---: | --- |
| `AdjacentBirths` | Coupled local residue classification | 8 | Agent #7 /root/odd_counts |
| `OverflowDigits` | Actual width, digit, shifted-index and carry bridge | 12 | Agent #7 /root/gap_inventory |
| `ActualOverflowBirths` | Complete actual-word interior classification | 4 | Agent #7 /root/odd_counts |
| `OverflowEndpoints` | Endpoint positivity and exact binary boundary | 8 | Agent #7 /root/gap_inventory |
| `CanonicalOverflowBirths` | Original canonical reverse-add specialization | 1 | Agent #7 /root |

The eight original dependencies are byte-identical pinned sources. `dependencies/SOURCE_PINS.json` gives their original commits, paths, Git blobs, SHA256 hashes and module identities. Existing `ActualBaseBirths` supplies the no-overflow domain; the prior decimal overflow formulas and original binary safety example are credited in the claim. This contribution fills the actual all-base overflow domain.

## Executed author verification

The final parent author replay is `canonical-dev/attempt-002/verification.json`, SHA256 `691824d7d0122b32fb14f553ccdc49c615ef4552f7e254c963943e49657178d7`. It freshly builds all 13 modules with official Lean 4.19.0, `--trust=0 -j1 -DElab.async=false`, and records 51 literal public axiom printouts, including every one of the 33 new endpoints. The allowed mathematical axiom union is `propext`, `Classical.choice`, and `Quot.sound`.

Each lane preserves its full author attempts, commands, source hashes, substantive logs and audit source. The canonical first attempt failed on a redundant `dsimp only` after the interior lets were already reduced; the original failed source and complete log remain. Its elaboration-error `sorryAx` is confined to the rejected attempt. The corrected accepted source introduces no sorry, axiom or unchecked shortcut. Endpoint fixture-only failures are likewise retained.

A separate nonauthor execution already reviewed the actual index bridge, including off-by-one negative controls. Endpoint fixtures cover bounded nonsymmetric binary sources, excluded binary heads, an unbounded-head counterexample to the maximum criterion, and bound-free signed ternary coefficients. The final reviewer /root/runtime independently compiled all13 frozen project modules with explicit trust0 and completed the full audit:338 project theorem constants plus11 constants from nine boundary contracts. All133 project public theorem roots plus9 review roots were inspected. The final report is review/final-003/verification.json, SHA256 eb4f8873b5001970d7a8140cb4a9b7c57661143e435010e9401ad49de8537101. Reviewer-only fixture/display failures remain preserved; the final audit pins the successfully compiled final-001 project objects. No mathematical source changed during review.

The unchanged canonical verifier can replay this exact registry:

```
python proofs/verify_project__214bf7673efe116b.py --lean /path/to/lean-4.19.0/bin/lean --registry proofs/contributions/agent-7/allbase-overflow-births-20261016/PROJECT_REGISTRY.json --project agent7-allbase-overflow-births --output /new/retained/output/path
```

This is a one-step finite coefficient and numeral theorem. Run population, growth, ancestry, lifetime, infinite avoidance and the 196 conjecture are outside its scope. Agent #7 holds no main integration slot.

## Final acceptance evidence

The unchanged canonical verifier passed on clean local commit `96c618e812f3675c460d259ca76d3ce1b7073bd3`, whose complete tree `3d952a0a1deef7aec912a93d8654b33734e4b847` equals published/read-back source `4512ecb58abd9ff464d8d3b1c70b6abeb85472d0`. Its report SHA256 is `0d892b22478ed833adc75ee3da1e46b9a8420b7ba5fe0a12c9792e220a3db664`. `verification/AGENT7_EXECUTION_RECEIPT.json` identifies the actual Agent7 parent executor while preserving the original verifier's historical Agent1 label and compiler flags. The separate author and independent executions explicitly used `--trust=0`.

`review/FINAL_REVIEW.json` records all semantic findings, authors/reviewers and the nine boundary contracts. The reviewer is a genuine nonauthor within the same Agent7 collaboration; no unaffiliated peer or separate-account approval is implied. `review/FINAL_STAGE_FILES.json` supplies the precise78-path final evidence packet. Publication manifests retain all substantive sources, failures, logs, commands and audits;122 identical source copies or reproducible objects have exact omission hashes. The four inherited compiler implementation constants are separately inventoried and absent from all theorem dependencies.

The reviewable contribution is PR127. Integration remains the responsibility of the designated serial main owner.
