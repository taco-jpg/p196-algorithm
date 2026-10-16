# Independent factorial acceptance gate

**PASS:** the frozen factorial recurrence 和 ordinary-decimal specialization passed independent semantic review 和 a fresh 11-module Lean 4.19.0 build with `--trust=0`. No mathematical source correction was requested or made by this reviewer.

## Checked result

| Quantity | Result |
| --- | --- |
| Mathematical module closure | Nine original dependencies plus two new proof modules |
| Source compilation | All eleven modules exit 0 |
| Explicit authored exports | All eleven named exports have literal transitive axiom reports |
| Exhaustive theorem audit | 1,456 theorem constants |
| Exhaustive safe-definition audit | 182 safe definition/opaque declarations |
| Coverage of the two new modules | 19 theorem constants 和 five safe definitions, including generated auxiliaries |
| Transitive axiom union | `Classical.choice`, `Quot.sound`, `propext` |
| Source/registry/compiler stability | Selected hashes unchanged |
| Initial project object files | Zero |

The module-origin audit includes every selected theorem 和 safe definition, including private/generated declarations. All eleven expected originating module names were checked within Lean; the complete wrapped origin list was also parsed into `EXPORTED_RESULTS.json`. The audit separately records 15 unsafe implementation axiom constants 和 807 unsafe implementation definitions in the closure. No theorem or safe-definition dependency falls outside the permitted standard axiom set.

The independent runner uses `LEAN_PATH` containing only its newly created build directory. It copies original source bytes exactly, verifies the registered import closure, rejects forbidden proof tokens after masking comments/strings, 和 checks original dependency Git commit/path/blob identities before compiling. Existing project `.olean` files are 不 reused. Installed standard-library objects come from the selected Lean runtime; this gate does 不 rebuild the standard library from source. Runtime-file hashes cover the executable, root runtime objects, 和 shared libraries explicitly listed in the raw record.

## Mathematical conclusion 和 scope

The generic theorem proves `E M ≤ (4*κ)^(M-1)*M!` under exactly `κ>0`, `M≥1`, `E1=1`, 和 the source recurrence. It leaves `E0` unconstrained. Its factorial is defined by the ordinary recursion `0!=1`, `(m+1)!=(m+1)m!`.

The unchanged decimal recurrence instantiates `κ=5`, giving `20^(M-1)*M!`. Its separately justified `M=0` extension uses the concrete recurrence's existing zero value. The original digit-sum horizon is evaluated at `2*B`, so the final window is inclusive:

```text
For every n>0 和 natural B,s,
there exists t with s≤t≤s+20^(2*B-1)*(2*B)!
和 B<digitSum(orbit(n,t)).
```

The exponent uses natural subtraction. At `B=0` the closed bound is one while the existing exact horizon is zero. No initial digit-sum upper bound, width bound, or gap assumption is added. The orbit continues after palindromes; the theorem makes no palindrome-avoidance or pointwise-divergence assertion. The 196 endpoint specializes only the positive-seed hypothesis.

Detailed source-equation, induction, zero-index, numeric transport, 和 endpoint checks appear in `SEMANTIC_REVIEW.md`.

## Provenance 和 evidence

`provenance.json` records independent original-source Git reads 和 matches the manuscript to blob `7103ee939d82740b970dd23fb91e9db50db4ea54`, SHA256 `15e07772d87cc4ee469541f4fb39ce1d0dce28ac5f630b16980c8abb02db258f`. It also checks every dependency's flattened path against the contract's source-main commit `ae8bbdfd2a18e8910eebc25fd2a81661c01abc16`. The working checkout's recorded HEAD remains `4b4edf976b2c7a9ba1dad80636c0e21c66350325`; exact selected source identities, rather than an unrelated checkout label, govern this review.

`inputs/` retains the contract, original mathematical source, new proof sources, authored audit support file, 和 the author's checker/dependency metadata as inspected at review start. The author subsequently corrected only the wrapped-origin parser in its checker; its original run record 和 original checker snapshot were preserved by the author. This independent review uses its own checker 和 is unaffected by that reporting correction.

`runs/full-001/` retains the unchanged raw report, every command log, the independently generated audit, the exact registry/verifier snapshots, 和 the complete export/origin index. Its `RETENTION.json` explicitly identifies reproducible build objects 和 duplicate source copies omitted from the retained packet. `EVIDENCE_FILES.json` indexes only files actually retained there.

`ALGEBRA_REVIEW_ATTRIBUTION.json` credits Agent #9/horizon-safety's additional read-only equation/algebra check. That helper performed no compiler replay; the independent full replay was executed by Agent #9/runtime-audit.

## Replay

From the repository root:

```bash
python3 proofs/contributions/agent-9/escape-factorial-bound-20261016/review/runtime-audit/verify.py \
  --lean /absolute/path/to/lean-4.19.0/bin/lean \
  --output /absolute/path/to/a-new-output-directory \
  --auditor 'Actual executing person or agent'
```

The output directory must be new. Historical Git objects from the recorded commits must be available. If relocating the retained checker snapshot, pass explicit `--repo`, `--package-root`, 和 `--manifest` paths. Every mathematical compile 和 the independent audit includes the explicit `--trust=0` flag.

| Retained item | SHA256 |
| --- | --- |
| Independent verifier | `95a32d0a29dcd18550ea2b6b4c660ddf7c732636bbbcc83377bf2dc434c1aa1c` |
| Independent source registry | `6265463f69bedd929d4b28e252e0a7293f0324cadda89d45907b6369076f3403` |
| Raw successful report | `cf8f2216ec521039dcffdf0cb760effb395e868be1b785d22c74166864f1f9f0` |
| Independent audit source | `57f6af2929ae82bd54d34e4b35eb51f121aead3c3b697397936798bff2fec932` |
| Independent audit log | `54fb78d30c611ad4b522fdd4aa9189d80e698167b31111007c0576a08533b027` |

Git writes, publication, 和 integration remain with the parent.
