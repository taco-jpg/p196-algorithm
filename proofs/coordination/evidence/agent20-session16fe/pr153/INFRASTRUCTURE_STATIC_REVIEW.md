# PR #153 verifier infrastructure: independent static review

## Scope and current disposition

Reviewer: Agent #20, session `16fe9eef625c`, scoped specialist `/root/evidence_qualifier`. This review concerns the new `verify_pr153.py` and `Audit.lean.in` infrastructure only. It does not repeat the accepted mathematical semantic review. No Lean process was executed and no infrastructure or proof source was modified by this reviewer.

**Final disposition: PASS_STATIC_REVIEW_FOR_PINNED_SCOPE at corrected verifier SHA256 `2946672444067c646ff38a3a099bc8c69c9964d729a923cd7fbd27c44aebaddb`.** The confirmed preflight scanner blocker has been corrected and the narrow fix independently checked. No remaining concrete static or Lean 4.19 API blocker was identified. This is an infrastructure review, not a compiler result or an additional project approval gate. The coordinator decides execution. The original findings below remain preserved as historical evidence.

The pre-correction snapshot is retained under `infra-review-original/`:

| Input | SHA256 |
|---|---|
| `verify_pr153.py` | `d1a91879963e4a793d6a577ede14c053d44d7b0d19f226a1a2672db05521e1bd` |
| `Audit.lean.in` | `e0acf0ac8c33d6832d5a008d11d99b95950ff1ec7ea4d0f2d9c67b6f710d148f` |
| `source-manifest.json` | `a49d4fc3288c992465f355a8fef1a8e2977fd7dfd5507c4fa1e6e410b16175e7` |

The Python snapshot parses as Python source. The root coordinator and builder have received the concrete findings directly.

## Original confirmed blocker, now corrected: character literals invalidate the external-source scanner

`code_only` treats every double quote outside its comment/string state as a string opener. It does not recognize Lean character literals or raw strings. The external-import closure applies this scanner to entire valid installed Lean source files, not merely their import headers.

A static simulation of its state transitions, without running Lean or the verifier, establishes:

| Exact installed input | SHA256 | Result of the original scanner |
|---|---|---|
| `Lean/Parser/Basic.lean` | `9d5a01f7b5603c5d1a3b43ef9144af917d29ce385c3ef18ad216d5b54c` | Ends in `string=True`; false unterminated-string failure |
| `Lean/Data/Json/Parser.lean` | `f9f691a046004be29208e429018b0bf5387961ec9c9c3658d3c41c4c582e681b` | Ends in `string=True`; false unterminated-string failure |

Both are in the explicitly traversed `Lean` dependency closure. `Lean/Parser/Basic.lean` contains quote character literals at lines 736 and 762, among others; `Lean/Data/Json/Parser.lean` contains them at lines 32, 46, 187, and 221. The original scanner incorrectly interprets character-literal quote content as ordinary string boundaries. Its final erroneously open string positions are lines 1959 and 240 respectively. Exact findings are retained in `infra-static-lexer-findings.json`.

This causes a deterministic `Unterminated Lean comment or string` exception before any compilation, even with a complete correct external cache. A narrowly scoped remedy is either a correct scanner for Lean character/raw-string forms or parsing only the external module header with equivalent comment handling. The full local-source forbidden-construct inspection must remain intact. This defect is fail-closed: it cannot manufacture a proof pass.

## Positive findings

- Source scope is fixed at exact H, thirteen named local modules, and twenty-nine distinct endpoints. Every local file is read from Git, checked by SHA256 and Git blob identity, compared with its original source revision, and copied to isolated staging.
- The first eleven module records are compared with the retained original dependency manifest. The import graph must close over exactly all thirteen local modules, with local cycles rejected and a topological compilation order derived from the graph.
- A fresh output directory and initially empty project-object directory are required. The local object directory precedes the explicitly recorded external roots in `LEAN_PATH`; a clean environment is passed to subprocesses. No compiler starts without `--execute`.
- The executable and primary shared library have exact expected SHA256 values; additional runtime libraries and imported source/object files are hashed and checked for changes before a pass.
- Compilation uses `--trust=0`, one worker, and synchronous elaboration. Nonzero return codes and timeouts cause top-level failure; substantive stdout/stderr are retained and hashed. The final report cannot claim `PASS` merely because the source-only preflight succeeded.
- The audit inventories declarations by actual originating module, checks all local theorem axiom sets, requires all twenty-nine endpoints to be theorems, and traverses types, mathematical bodies, inductive families, constructors, and recursor rules of all safe local roots.
- Traversal rejects missing checked constants, unsafe/partial mathematical dependencies, `sorryAx`, the named compiler-trust bridges, and axioms outside the allowed three. Implementation redirections and extern attributes are recorded distinctly from mathematical proof-term dependencies.
- Python validates audit completion counts, unique names, module coverage, and endpoint inclusion. The later literal pass invokes Lean's real `#print axioms` for all selected theorems and safe definitions, and checks that the expected output names occur.

## Lean 4.19 API checks

The installed primary sources at `/tmp/p196-agent5-lean/lean-4.19.0-linux/src/lean/` were inspected directly. Their hashes are retained in `infra-lean-api-inputs.json`.

- `Environment.checked` is a `Task Kernel.Environment`; `env.checked.get.find?` is precisely the access pattern used by Lean's own `Lean.Util.CollectAxioms` implementation. The custom audit does not substitute an unchecked elaborator constant when a checked constant is required.
- `Environment.constants`, `getModuleIdxFor?`, and `allImportedModuleNames` support the selected module-origin inventory. The explicit asynchronous-elaboration flag further limits synchronization ambiguity.
- `ConstantInfo.isUnsafe`, `isPartial`, and `value? true` exist with the used signatures; the last includes opaque mathematical bodies.
- `InductiveVal.all`/`ctors`, `ConstructorVal.induct`, and `RecursorVal.all`/`rules`/`RecursorRule.rhs` have the expected types. `Expr.getUsedConstants` returns an array supporting `.toList`.
- `Lean.collectAxioms`, `Lean.Compiler.getImplementedBy?`, and `Lean.getExternAttrData?` exist at the referenced namespaces.
- Lean's command parser accepts both `#print identifier` and `#print string`. Its information-message formatting emits information without source-position prefixes, so the audit's one-line JSON tags and literal marker parsing are consistent with the inspected implementation.

These are source-backed API checks, not a claim that the generated Lean audit has compiled. Compiler execution can still reveal elaboration, resource, or interaction problems.

## Assurance limitations

1. **External-cache authenticity is supplied by the coordinator's provenance work.** The verifier checks the expected Mathlib commit string and manifest hash in an external JSON record, inventories bytes, and rejects changes. Those operations do not independently authenticate that the restored objects were produced by the claimed upstream commit. The trusted artifact/source linkage must be evaluated from the coordinator's actual recovery evidence. A matching self-supplied metadata string alone is insufficient.
2. **The initial literal-output limitation was corrected.** The original generated audit set `pp.maxDepth` but left `pp.maxSteps` at Lean 4.19's default 5000; exceeding that limit emits `⋯`. The corrected script sets `pp.maxSteps` to 10,000,000 and rejects any literal output containing `⋯`, preserving the raw result. This turns that known truncation condition into an explicit failure. Actual successful rendering remains to be established by execution.
3. **Static review is not a compiler result.** Python text parsing and installed Lean API correspondence do not establish successful audit elaboration, complete cache availability, or any theorem build result. No such outcome is claimed here.
4. **Scope remains exact H.** The verifier reads exact H sources. Combined-tree equality, current base/ownership, platform checks, readiness, and final integration remain the coordinator's separate responsibilities.

## Correction review

The corrected verifier SHA256 is `2946672444067c646ff38a3a099bc8c69c9964d729a923cd7fbd27c44aebaddb`. The audit template remains byte-identical at `e0acf0ac8c33d6832d5a008d11d99b95950ff1ec7ea4d0f2d9c67b6f710d148f`. The source manifest remains byte-identical. Corrected inputs are retained under `infra-review-corrected/`, and the exact original-to-corrected diff is `infra-reviewed-correction.diff`.

The change is limited to character/raw-string handling, a separate external-header import parser, and literal pretty-print truncation controls. The local forbidden-construct scan, source pins, module inventory, mathematical dependency traversal, axiom restrictions, compiler flags, fresh-object requirement, and failure handling remain intact.

The new external parser reads nested comments, optional `prelude`, and successive `import` statements with the optional `runtime` marker, then stops at the first declaration. This matches the inspected Lean 4.19 `Parser/Module.lean` header grammar for the actual ASCII module names in the pinned corpus. It does not parse arbitrary tactic or interpolated-string bodies. The builder also preserved its second intermediate failure involving nested interpolated strings in `Mathlib.Tactic.Linter.DeprecatedModule`; reading headers alone removes that unrelated body-lexer dependency.

An independent Python-only source preflight extracted and invoked only the three reviewed pure text-parser functions, without invoking the verifier's `main`, starting Lean, inspecting or generating compiled objects, or writing outside the evidence directory. It checked all **13 exact local source hashes and import lists**, then traversed **2,665 uniquely resolved external source modules** from the local imports plus `Init` and the audit's `Lean` root. Its complete external source/hash/import mapping exactly matched the builder's retained `lexer-regression.json`, whose SHA256 is `b35301b5785f93b7b0fb48accf0a7646bd572f0372bd42aa1519a265cbd2889f`.

Both originally failing official files also passed the corrected full scanner with text length and newline positions preserved. Their parsed header imports are:

- `Lean/Parser/Basic.lean`: `Lean.Parser.Types`.
- `Lean/Data/Json/Parser.lean`: `Lean.Data.Json.Basic`, `Lean.Data.RBMap`, `Std.Internal.Parsec`.

The independent static-preflight result is retained in `infra-static-preflight.json`. Its canonical external-inventory SHA256 is `2056910c6a5ad595b4000cf0286d21bc943aaa288f8a91ad2ebe2d647cef0f8b`. The builder's separate regression suite was inspected and its recorded result reviewed: 21 fixture records, including four expected rejections, thirteen local sources, and 2,665 external sources. That recorded suite is attributed to the builder; this reviewer independently repeated the exact-source text preflight described above.

No additional semantic-proof review was performed or imposed. No Lean execution or mathematical success is established by this review. The coordinator retains external-cache provenance qualification and the actual execution decision.
