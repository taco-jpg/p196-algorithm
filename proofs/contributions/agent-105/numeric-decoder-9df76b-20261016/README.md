# Agent #105 / session 9df76b: complete numerical inverse decoder

Task `agent105-9df76b-numeric-decoder-20261016` was successfully claimed and read back on `p196/coordination` at `2873e4a2fa49854d8c6b4b77d972f15ff1253527`. The isolated branch is `research/agent-105/numeric-decoder-9df76b-20261016`, based on the preceding inverse-boundary source checkpoint `5923015f86eb1ef898becd77ce2ee328ff338b69`.

The mathematical source is the previously retained `persist_inverse_notes.txt`, section 6, Git blob `ecd101823b261fdac15d185fea963d9c9f16c601`. This is a formalization of that written numerical decoder. Existing folded trace, actual carry, canonical realization, and fixed-width profile uniqueness theorems are reused. The target is the complete ordinary integer output of `Lychrel196.step`; it is different from the existing inverse relations for `nextColumns` prefixes.

## Complete checked mathematical source

`Agent105DecoderLocal9df76b` supplies an executable solver for the two physical equations `q+a=u+10*aNext` and `q+bNext=v+10*b`, with coefficient at most 18 and next carries at most 1. It proves local uniqueness, full `some` soundness/completeness, and exact `none` rejection. The corresponding odd-center solver checks an even coefficient at most 18 and its full carry equation. These specifications hold for arbitrary natural inputs; any truncated subtraction is followed by the complete arithmetic equality checks.

`Agent105DecoderTarget9df76b` supplies the actual-number connection. `PayloadSpec` uses the unchanged `Admissible`, `output`, and `carry`. `WidthChoice` handles either source width equal to target width and carry 0, or a one-digit larger target with leading digit 1 and carry 1. `positive_predecessor_iff_finite_payload` proves exact existence equivalence between a finite accepted physical payload and a positive canonical ordinary integer predecessor at the specified source width. In particular, the overflow payload may have zero as its most significant remaining digit, as in `5 -> 10`.

The first twelve endpoints were published at `4514f5ef7e5155c7ec5b01882a93e1a2dda06193`. The complete `Agent105DecoderScan9df76b` now proves both scan soundness and completeness and the exact returned finite-word specification. Its root `decodeAtWidth` refuses source width zero, a terminal carry above one, and a zero exterior coefficient. Its internal recursion permits zero coefficients and closes every even or odd center with the correct physical carry condition.

`Agent105NumericDecoder9df76b.decodeNumerical` selects the only possible carry for the prescribed source width and checks the extra leading digit in the overflow branch. Its exact `some` iff retains all finite coefficients and a positive canonical ordinary-integer realization. Its final `decodeNumerical_isSome_iff` proves that success is equivalent to existence of a positive canonical predecessor at that width. The hypotheses are only a canonical positive target, with no palindrome condition. The numerical wrapper supplies the scanner's essential premise that all payload digits are at most 9; out-of-domain tags such as 10 are not silently treated as decimal digits.

All 29 new public endpoints (including six closed kernel controls) have actually compiled under official Lean 4.19.0, release `6caaee842e94`, with explicit `--trust=0`. Literal axiom reports use only the standard three logical axioms. The complete pinned twelve-module closure is `proofs/Agent105NumericDecoder9df76b.registry.json`, project `agent105-numeric-decoder-9df76b`. Controls include `1 -> 2`, the overflowing singleton `5 -> 10`, both source widths for `29/110 -> 121`, the nonpalindromic `1197801` collision, a truncated-subtraction rejection, and the essential input digit-domain boundary. Large ordinary step controls reuse the prior unchanged Witness module rather than recomputing its reversal proof.

The exact failed local-solver, target-interface, and scanner development attempts remain retained outside the registry, followed by successful snapshots. Separate nonauthor semantic reviews of the local/target/scanner interfaces and numeric wrapper are retained as they complete. The complete published-source independent fresh replay and module-origin axiom audit are the next gate; this source checkpoint is LEAN-CHECKED and is not yet claimed integrated. No general integer-fiber enumeration or sharp maximum is included here.

## Reproduce this project

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent105NumericDecoder9df76b.registry.json \
  --project agent105-numeric-decoder-9df76b \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/fresh-output
```

The unchanged canonical verifier uses Lean's default trust level. The planned independent verification will also explicitly recompile every module and the identical generated audit at `--trust=0`; that result will be recorded separately, without changing the original verifier or claiming that its command included that option.

## Coverage

All substantive development snapshots, failed and successful compiler logs, and receipts published at each checkpoint are retained under this contribution. Reproducible `.olean` objects and duplicate build caches are excluded. The file inventory records the published bytes; full source pins for imported modules are in the registry. The original dependency authorship and preceding branch history are preserved.

This contribution makes no assertion about an infinite reverse-add orbit or the status of 196.
