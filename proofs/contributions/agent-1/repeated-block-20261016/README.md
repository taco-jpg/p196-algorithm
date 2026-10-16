# Repeated-block normalization — Agent #1

Status: **INDEPENDENTLY-REVIEWED** for the exact normalization/carry/list-length statements. The core and context passed a separate source review and fresh eight-module `--trust=0` rebuild. Its exhaustive audit checked 1,236 theorem declarations, with only `propext`, `Classical.choice`, and `Quot.sound` in the transitive union. All 23 new theorem axiom prints are retained. The ten closed boundary witnesses have no axioms and were also independently compiled by the parent. No main integration or external PR approval is inferred from this internal specialist review.

`Agent1RepeatedBlock.normalize_pow_succ` uses the unchanged `Agent8.normalize`, `fixedDigits`, and `terminalCarry`. For coefficients at most 18 and incoming carry at most one, every positive block power has one possibly transient normalized copy, followed by exact copies of the stabilized normalized block, and the original terminal carry. Empty and all-nine blocks are retained. Carry classification is imported from `IncomingCarry.carryIn_transfer_trichotomy`; `Agent8.fixedDigits_append` is reused from `PrefixSemantics`.

`Agent1RepeatedBlockContext` supplies the exact fixed-context output formula, terminal-carry independence for two independently repeated bands, the symmetric-band specialization, and exact normalized **list lengths**. The last suffix may be arbitrary in the output/carry identities; bounds are explicit where a subsequent band must receive a bit carry. These are not automatically canonical natural-number digit-width claims: list words can retain leading zeros. The general statements neither assert symmetry nor positive ordinary-integer realizability.

This formalizes the repeated-block carry/digit stabilization used in the retained periodic guard argument. It does not prove mirrored-pair guard extraction, quotient stripping, a safe quotient cycle, an accepting return certificate, an infinite ordinary orbit, or the claim about 196.

Reproduce from the repository root with an unused output directory:

```sh
python3 -u -B proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent1RepeatedBlock.registry.json \
  --project agent1-repeated-block \
  --lean /absolute/path/to/lean-4.19.0/bin/lean \
  --output /tmp/agent1-repeated-block-fresh
```

The scoped registry pins all five unchanged dependency modules and all three new modules. The existing verifier checks exact hashes, import closure, source trust exclusions, fresh compilation and every theorem's transitive axioms. It does not modify the global accepted registry.

Parent Agent #1 is the sole Git writer and context-module author. Genuine specialist `/root/symbolic_scope` authored the core; `/root/research_status` performs separate semantic review. Failed and successful development attempts are retained under `author/` and `parent/`. A failed attempt's generated `sorryAx` report is a compiler-error artifact, never an accepted theorem. No incomplete attempt is a registry root. Runtime installations, copied dependency trees and compiled objects are reproducible infrastructure and excluded.

Claim: coordination commit `2cb89418916f1d0a22813028d5fea623e80900ad`; issue61 scope comment `6224692858`, accepted claim comment `6224749698`. Source baseline: `4b4edf976b2c7a9ba1dad80636c0e21c66350325`. Parent retains no main-write slot. Group III is published on a separate branch/PR so these statements can be reviewed independently.


Review: `review/statement-review.md`; independent execution: `review/clean-001/verification.json`; parent seven-module exhaustive run: `parent/clean-001/verification.json`; parent boundary replay: `parent/boundary-check/`. The parent run began before the first source commit; its publication receipt explicitly matches every built hash to published source `757b1a59f71a155779c27b7cc7842aa1fcd9a96b`, rather than treating the report's earlier HEAD as containing the new source.

The boundary module supplies exact kernel-checked witnesses for empty/all-nine behavior, a first-copy transient, and failures when the positive-count or carry/coefficient/context bounds are removed. Its retained-zero-columns witness makes the list-length/canonical-width distinction explicit.
