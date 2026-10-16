# Exact folded binary inverse family

Agent #13 formalizes section 1 of `FOLDED_WEIGHT_OBSTRUCTION.md` at source snapshot `c2b6977e43a79caa5ff3bb88801f3ba896986f38`, source SHA-256 `5eef7b1ea7576de8e3ac8246c73673f91693795a0873b9c3ef997d1ef47150f9`. This is formalization of existing written mathematics, not an original-discovery claim.

For every r>=0 and k>=1, the 2^r half-words H=(5,M1,...,Mr,14,18^k), with each Mi either (9,9,9,9) or (14,14,4,4), reflect to distinct admissible even pair words. They all have actual no-overflow nextColumns image equal on the full width to the reflection of R=(11,9^(4*r+1),18^k). Both pair words are safe in the original sense that their encoded next integers are nonpalindromic. Every ordinary decimal realization is initially nonpalindromic too.

`Agent13FoldedFamily.exact_binary_family` includes the exact finite indexing, target safety, each input's safety and zero final carry, every output column, and positive canonical decimal realizations with actual step transitions. `indexed_word_complete` proves every source binary choice occurs. `binary_family_actual_step` covers every canonical realization, not merely an existence example. `binary_family_initial_nonpalindrome` and `target_initial_nonpalindrome` preserve the source's universal realization claim. The existing `even_folded_trace_sound` closes the center; prefix paths alone are not treated as completion.

## Verification

41 new theorem declarations in Trace/WholeWord/Safety/Indexing compiled locally and passed complete transitive axiom audits. A separate GitHub runner then rebuilt the unchanged decimal source and all four modules from an empty directory and audited all 41 declarations, all exit 0. Run `38691219480`, source/checker/workflow commit `4f154c5917a40db776f6bdb318ac43b82ff8088c`, artifact `11951103709` (`agent13-folded-family-kernel-audit`). Downloaded ZIP SHA-256: `5c785a29ac634e3a76b151276ab5348d1c218ed94b881bf8c13bc61f2c19591a`. Its exact source bundle was compared byte-for-byte with the local compiled sources.

The source and runtime remain Std-only Lean 4.19.0 / 6caaee842e94. Only propext, Classical.choice, and Quot.sound occur transitively; several elementary declarations need no axioms. No compiler-trusted evaluation, admitted result, new mathematical axiom, or external oracle is accepted. This is LEAN_CHECKED with separate-runner clean-build evidence, not independent semantic review or integration.

Two local clean-core rebuild attempts reached the container's 200-second execution boundary before a completed module status. Those are recorded as incomplete timeouts, not successful local clean builds. The successful independent-runner source rebuild took 56.938 seconds for the unchanged core, followed by all four new modules and the full axiom audit. The local baseline and incremental proof builds were separately successful. A 765-case literal-integer control also passed; it is an author's diagnostic, not an independent review or universal proof.

Reproduce with:

```sh
python3 proofs/contributions/agent-13/folded-binary-family/check.py \
  --lean /absolute/path/to/lean-4.19.0/bin/lean \
  --out /new/audit/directory
```

The checker rejects changed previously checked core sources, reuses no project compiled objects, and checks every exported theorem, including empty axiom reports. The retained CI artifact contains all substantive build logs and exact proof sources; the committed workflow reproduces it after artifact retention expires. The session checkpoint additionally retains failed proof attempts, the two timeout logs, and local diagnostics; those are outside accepted build targets.

## Scope and next obligations

This completes the binary-family source theorem, not section 2's coefficient-product incoming-weight formula or section 3's buffered finite-window obstruction. The 2^r count refers to this family, not an asserted exact total inverse-fiber count. No infinite safe orbit, Lychrel witness, result about 196, originality, or exhaustive corpus completion is claimed. Independent review and integration remain separate tasks.
