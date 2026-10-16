# Agent #105 / session 9df76b: complete numerical inverse decoder

Task `agent105-9df76b-numeric-decoder-20261016` was successfully claimed and read back on `p196/coordination` at `2873e4a2fa49854d8c6b4b77d972f15ff1253527`. The isolated branch is `research/agent-105/numeric-decoder-9df76b-20261016`, based on the preceding inverse-boundary source checkpoint `5923015f86eb1ef898becd77ce2ee328ff338b69`.

The mathematical source is the previously retained `persist_inverse_notes.txt`, section 6, Git blob `ecd101823b261fdac15d185fea963d9c9f16c601`. This is a formalization of that written numerical decoder. Existing folded trace, actual carry, canonical realization, and fixed-width profile uniqueness theorems are reused. The target is the complete ordinary integer output of `Lychrel196.step`; it is different from the existing inverse relations for `nextColumns` prefixes.

## Complete checked mathematical source

`Agent105DecoderLocal9df76b` supplies an executable solver for the two physical equations `q+a=u+10*aNext` and `q+bNext=v+10*b`, with coefficient at most 18 and next carries at most 1. It proves local uniqueness, full `some` soundness/completeness, and exact `none` rejection. The corresponding odd-center solver checks an even coefficient at most 18 and its full carry equation. These specifications hold for arbitrary natural inputs; any truncated subtraction is followed by the complete arithmetic equality checks.

`Agent105DecoderTarget9df76b` supplies the actual-number connection. `PayloadSpec` uses the unchanged `Admissible`, `output`, and `carry`. `WidthChoice` handles either source width equal to target width and carry 0, or a one-digit larger target with leading digit 1 and carry 1. `positive_predecessor_iff_finite_payload` proves exact existence equivalence between a finite accepted physical payload and a positive canonical ordinary integer predecessor at the specified source width. In particular, the overflow payload may have zero as its most significant remaining digit, as in `5 -> 10`.

The first twelve endpoints were published at `4514f5ef7e5155c7ec5b01882a93e1a2dda06193`. The complete `Agent105DecoderScan9df76b` now proves both scan soundness and completeness and the exact returned finite-word specification. Its root `decodeAtWidth` refuses source width zero, a terminal carry above one, and a zero exterior coefficient. Its internal recursion permits zero coefficients and closes every even or odd center with the correct physical carry condition.

`Agent105NumericDecoder9df76b.decodeNumerical` selects the only possible carry for the prescribed source width and checks the extra leading digit in the overflow branch. Its exact `some` iff retains all finite coefficients and a positive canonical ordinary-integer realization. Its final `decodeNumerical_isSome_iff` proves that success is equivalent to existence of a positive canonical predecessor at that width. The hypotheses are only a canonical positive target, with no palindrome condition. The numerical wrapper supplies the scanner's essential premise that all payload digits are at most 9; out-of-domain tags such as 10 are not silently treated as decimal digits.

All 29 new public endpoints (including six closed kernel controls) have actually compiled under official Lean 4.19.0, release `6caaee842e94`, with explicit `--trust=0`. Literal axiom reports use only the standard three logical axioms. The complete pinned twelve-module closure is `proofs/Agent105NumericDecoder9df76b.registry.json`, project `agent105-numeric-decoder-9df76b`. Controls include `1 -> 2`, the overflowing singleton `5 -> 10`, both source widths for `29/110 -> 121`, the nonpalindromic `1197801` collision, a truncated-subtraction rejection, and the essential input digit-domain boundary. Large ordinary step controls reuse the prior unchanged Witness module rather than recomputing its reversal proof.

The exact failed local-solver, target-interface, and scanner development attempts remain retained outside the registry, followed by successful snapshots. Separate nonauthor semantic reviews of the local/target/scanner interfaces and numeric wrapper are retained. The complete published-source independent fresh replay and module-origin axiom audit have now passed in both runs described below. This verification result does not claim integration. No general integer-fiber enumeration or sharp maximum is included here.

## Complete independent verification

The independently verified source checkpoint is `64bb07e9f8d3ffcfd141d58e01ec7e27964c5e5d`. Both actual full runs used the unchanged twelve-module registry, SHA-256 `10aa02456c15914a8dd00a1b3bf639a7e9f129262c54ef7bd894ec635eec9f52`, and audited **1,096 module-origin theorem declarations**. The five new decoder/control modules account for **112 declarations**, including private and generated auxiliary theorems; the registry lists **29 new public endpoints**. The two complete theorem-name-to-axiom dependency maps agree.

| Run | Actual result | Fresh source directory | Elapsed time |
|---|---|---|---:|
| Unchanged repository verifier | `PASS`, exit 0; 12 module compilations and the generated module-origin audit | `verification/fresh-scope105-001/agent105-numeric-decoder-9df76b/source` | 101.94 s |
| Explicit `--trust=0` replay | `PASS_EXPLICIT_TRUST_ZERO`, exit 0; official help, all 12 module compilations, and the identical audit | `verification/strict-scope105-001/source` | 96.19 s |

The first checker was not modified and its recorded argv does not include `--trust=0`; official compiler help identifies its default trust level as `max`. The second run started in another empty directory, rebuilt all selected local modules with explicit `--trust=0`, and ran the byte-identical generated `ProjectAudit.lean` with the same explicit option. It did not reuse local `.olean` objects from the first run or alter the registry or axiom policy.

Both exhaustive audits report only `[Classical.choice, Quot.sound, propext]` as theorem axiom dependencies. They separately record **22 inherited unsafe implementation declarations** in the old foundation and Agent101 dependencies, with **0 in the five new modules**. The source files, published Git objects, and both build snapshots are byte-identical. This is a scoped project pass, not a repository-wide claim.

The contribution-root `canonical-verification.json`, `strict-verification.json`, `scope105-final-review.md`, and `scope105-final-review.json` are byte-identical copies of the original receipts and final review. `VERIFICATION_ARCHIVE.json` records the original path and SHA-256 of every copy and every archived member. The copies preserve the original receipt contents and path references.

`verification-evidence.tar.gz` losslessly contains the original manifest's 70 files **plus that unchanged manifest itself**, for 71 members total. It preserves every original `verification/` path, both complete source snapshots and logs, the audit programs and outputs, drivers, and resource observations. Every written archive member was reopened and checked byte for byte and by size/SHA-256 against the frozen original. From this contribution directory, restore the complete original evidence with:

```sh
tar -xzf verification-evidence.tar.gz -C .
```

The original verification directories remain locally intact; the archive is their publication representation. Its member map provides complete restoration without publishing the same raw tree again.

## Reproduce this project

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent105NumericDecoder9df76b.registry.json \
  --project agent105-numeric-decoder-9df76b \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/fresh-output
```

The unchanged canonical verifier uses Lean's default trust level. The completed independent explicit `--trust=0` replay is recorded separately in `strict-verification.json`; the original verifier and its command were not changed. After restoring the archive, the exact replay helper is `verification/replay_strict_trust0.py` and both actual command records are retained under `verification/`. Any new replay must choose previously nonexistent output directories.

## Coverage

All substantive development snapshots, failed and successful compiler logs, and receipts published at each checkpoint are retained under this contribution. `FILES.json` inventories those published development records, the top-level final evidence copies, the archive map, and the lossless archive; it omits itself and the archive-represented raw `verification/` tree. `VERIFICATION_ARCHIVE.json` supplies the complete original-path-to-member restoration map. `INFRASTRUCTURE_EXCLUSIONS.json` separately records reproducible compiled objects, duplicate build caches, and raw verification copies represented losslessly by the archive. Nothing was deleted locally. Full source pins for imported modules are in the unchanged registry. The original dependency authorship and preceding branch history are preserved.

This contribution makes no assertion about an infinite reverse-add orbit or the status of 196.
