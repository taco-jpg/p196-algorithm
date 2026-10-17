# Unconditional eighteen-label converse author receipt

Claim: `b184c77bd29fc1e9aa9bfaabb2169969da6d4084`.
Author: Agent1 specialist `/root/research_status/cap4_existing_theorems`.
Worktree: `/workspace/p196-agent1-reduced-core-20261017`.
Root is sole Git writer and issue61 relay.

## Frozen checked interface

Canonical source `proofs/Agent1PeriodicEighteenLabel.lean`:
SHA256 `050581493f32654bde2c0b2df3398fbc00861203122ed0a2f5aba8e68ae1cb4d`;
Git blob identity `3fbace9131adfc10f60661815566a20f0abab058`.
The only direct import is `Agent1PeriodicOuterRank`.

```lean
theorem Agent1.Periodic.outerComponent_eighteen_phase
    (s : Agent1.Periodic.OuterNode)
    (hc : Agent1.Periodic.outerComponent s = 130) :
    s.1 = [18,18,18,18]
```

This theorem is unconditional on catalog membership. It unfolds the unchanged
total component definition and follows its existing list constructors and digit
tests. Label130 occurs only in its constant-eighteen branch; the default is8.
The proof does not introduce a new classifier, graph row, rank, SCC, or closure
certificate. It does not itself prove the dependent reduced-return-core theorem.

`generate-structural.py` reads only the31 phase patterns in the original total
definition (original input SHA256
e345ef2c5fe7734f64ead7e971f0ea8b807dfcc2d84e3d50625109871fe10477), then
emits explicit constructor and digit case decisions. Lean checks every emitted
step against the original definition. This is structural proof-script generation,
not an empirical graph check. `structural-generation.json` records input/output
hashes. The original compiled match_9 is expanded directly to avoid its expensive
on-demand whole-pattern splitter; only the eight smaller outside matchers use
ordinary splitters. Original source and its catalog remain unchanged.

## Actual retained attempts

Each attempt preserves the exact source, run driver, dependency pins, command,
compiler version, logs and result from that execution.

- 001: `unfold` plus automatic phase-match split timed out at200000 heartbeats.
- 002: source-local heartbeat increase did not change that on-demand splitter
  timeout.
- 003: `delta` instead of `unfold` met the same timeout.
- 004: a diagnostic command-level heartbeat increase also met the same timeout.
- 005: destructing the node and an AFTER_DELTA trace localized the failure to
  splitting after unfolding, not the unfold itself.
- `matcher-inspect-001/002`: read-only compiler pretty-print diagnostics exposed
  the original compiled matcher and its constructor/conditional structure.
- 006: raw matcher expansion and length cases reached an unavailable `progress`
  tactic; parser/tactic failure retained.
- 007: removing that tactic left goals because the fallback `repeat first` hid
  an internal split simplifier failure; complete unsolved goals retained.
- 008: isolating the split exposed its internal simplifier step-limit failures.
- 009: explicit structural generator output compiled PASS; public theorem
  axiom-free. The initial audit rejected a generated safe splitter as an
  unexpected declaration category. This is a retained audit-driver inventory
  failure, not a failed mathematical theorem or a passing full audit.
- `runtime-inventory-001`: PASS, enumerates all generated safe and nonsafe
  definitions before fixing the exact audit whitelist.
- 010: same frozen source as009; ordinary command flags restored, strict
  compile and complete module-origin audit PASS.

No source used `sorry`, `admit`, `native_decide`, custom axioms, or skipped
kernel checking. Failed elaboration logs can contain Lean's generated `sorryAx`
for rejected goals; no such attempt is accepted.

## Final verification and limits

Pinned Lean4.19.0 commit6caaee842e94, compiler SHA256
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Final flags `--trust=0 -j1 -DElab.async=false`; source-local heartbeat budget
1600000 and4GiB process address-space cap. No diagnostic command-level budget
flag remains in attempt010.

Final compile: exit0,3.8245s,570180KiB maximum child RSS.
Final audit: exit0,1.3687s,780140KiB maximum child RSS.
Final object SHA256:
`eb9d5009819a82968b38802dd4d4f170e29a6ce8d15e5e2bbce7f8b82e3fe099`.

Full module-origin audit:55 theorem constants,8 safe definitions,24 precisely
inventoried generated runtime entries. Every theorem and safe definition is
axiom-free; union=[] and no custom axiom. The public endpoint is explicitly
required. Each safe small-matcher splitter is checked independently; its three
compiler cstage implementations are allowed only by exact observed names in
runtime-objects.json. Unknown constants and any unlisted nonsafe definitions
are rejected. The proof creates no public runtime definition.

The author increment reuses26 source/hash-pinned dependency objects from the
prior parent-clean ReturnCore build. This is not a fresh whole-closure build or
an independent package review; the parent performs those separately.
`manifest.json` hashes retained text/script/evidence files and records local
.olean files separately. No Git mutation or external message by this author.
