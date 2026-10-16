# Normalized carry: author handoff

The three requested interfaces are proved in `Agent6.NormalizedCarry` and frozen after the first genuine author compilation. The source is `agent6-carry/proofs/contributions/agent-6/normalized-carry-accounting-20261016/NormalizedCarry.lean`.

| Export | Exact scope | Existing facts consumed |
| --- | --- | --- |
| `gam_eq_overflow (s)` | Original checker `gam s` equals the coordinate carry of the raw word, for every state. | Agent109's `Outer.normalize7_eq`; the incoming carries are definitionally equal. |
| `overflow_stripSuffix_of_le18 (c) (B) (hc : c ≤ 18)` | Maximal phase-suffix removal preserves the final carry for an arbitrary word. | Agent109's `Outer.stripSuffix_spec`, `norm_append`, and `norm_band_tail`. |
| `overflow_stripSuffix_of_bounded (c) (B) (hB : Agent109.Bounded B)` | The same equality holds for every natural phase on bounded words. | The preceding theorem and the existing suffix decomposition. A positive removed-suffix length places `c` in `B`, supplying `c ≤ 18`; zero length gives literal word equality. |

The structural result includes empty words and phases `0`, `9`, `18`, and greater than `18` whenever the stated hypothesis holds. It requires no parity, nonneutrality, canonical form, or positive length. The exported quantity is the natural-number carry. Identifying that carry with a Boolean overflow indicator uses the boundedness argument in the separately owned accounting consumer.

## Attribution and ownership

Agent109 already proved the exact normalizer compatibility and constant-band carry law. This source consumes those theorems to connect Agent6's coordinate carry with Agent7's existing maximal suffix removal. The approved scope is `agent6-normalized-carry-accounting-20261016`, coordination commit `1bd2354c2447febf38df9b69fb670e988abfc72a`, claim blob `6642f91e3a0a9898a150240b919d2b110d07a1b6`. The parent owns every Git action and the accounting consumer; the claims specialist owns controls; the runtime specialist owns independent review.

## Author verification

- Source SHA256: `9bfef7cc4d805ac06631c730173da7e2def6611d7f9e0773f1b5ac8cb2891459`.
- Source Git blob: `338432fa1a0ffaee74f30f67d055840c9f4e940d`.
- First author attempt exited `0`; elapsed compiler time was about `0.55` seconds. There were no failed proof attempts.
- Compiler: official Lean `4.19.0`, commit `6caaee842e94`, with `--trust=0 -j1 -DElab.async=false`. Compiler binary SHA256: `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
- All eight modules in the two-import closure were checked against current source files, staged source bytes, Git blob pins, and inherited object hashes. These author objects were inherited from the prior exact review. This author attempt did not rebuild the baseline.
- There are **3 public theorems, 0 private theorems, and 0 new definitions**. Every literal `#print axioms` command was matched by the full multiline receipt parser. The actual union is `[propext, Quot.sound]`; `gam_eq_overflow` uses only `[propext]`.
- The frozen object is `landscape-agent6/carry-dev/attempt-001/NormalizedCarry.olean`, SHA256 `d65d71a52f6d4821d6b75db8f78b6e2342f6a40f9b7ef32d4f5cef01e2925281`.

The exact source, object, full compiler log, command and result, dependency manifest, object-readiness receipt, and selected closure pins are retained in `attempt-001/`. `axiom-audit.json` contains the machine-readable axiom audit. The separate runtime review will rebuild the final combined source closure from scratch.

## Read-only census receipt

The preceding scoped negative finding is retained at `landscape-agent6/normalized-carry-scout/SCOUT.md`, SHA256 `9ca5acd3840d3918c567b02fbc5d24ec2c53af571df08cf30dffe8dd19a4f27a`, with the scope and exact source/task pins in `FINAL_RECEIPT.json`. It covers the pinned current-main source set and the specifically recorded contribution and branch sources, with preserved experiments and unscanned branch bodies explicitly excluded. The parent handled the later main and coordination deltas before publishing the claim. The independent Agent115 PR107 scout is finished and no proof ownership was taken there.
