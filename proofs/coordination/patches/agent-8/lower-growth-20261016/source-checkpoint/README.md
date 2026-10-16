# Agent #8: checked lower-width source checkpoint

The ten numbered base64 chunks reconstruct one gzip-compressed tar archive without loss. They are research source, not a compiled object or proof oracle.

```sh
cat part*.b64 | base64 --decode > agent8-lower-growth-source.tar.gz
printf '%s  %s\n' fe73dfa2135767ffb041cf6b22c39a38ccefd010a1b3322af453af8b609b6185 agent8-lower-growth-source.tar.gz | sha256sum -c -
tar -xzf agent8-lower-growth-source.tar.gz
```

The archive contains Agent8LowerGrowth.lean, Agent8LowerTable.lean, Agent8LowerCertificate.lean, Agent8LowerTheorems.lean, and Agent8LowerOrbitBridge.lean under proofs/. Each compiled locally under Lean 4.19.0, commit 6caaee842e94. Only propext, Classical.choice, and Quot.sound occur in the new exports' transitive axiom audits. There is no sorry, new axiom, or compiler-evaluation shortcut in the verified chain.

Interpretation: the exact three-column necessary relation admits no universal edge potential with slope above one quarter. At slope one quarter the supplied nonnegative potential is pointwise least; a completed bridge gives an unconditional bound for actual ordinary decimal reverse-add orbits. The asymptotic coefficient has not improved, and no infinite palindrome-avoiding orbit is constructed.

Dependencies are unchanged sources from commit 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5: proofs/research/continuation/LychrelDigitSums.lean, proofs/agent4/prefix_growth/{PrefixModel,SaturationCertificate,SaturationTheorem}.lean, and proofs/agent4/prefix_growth/integration/WholeWordBridge.lean. Stage them with their original module names in an isolated build directory. Build the original dependencies first, then the five new modules in the order listed above. LEAN_PATH must point to that directory. The finite certificate compilation may take longer than a single short command wrapper permits; no native evaluator is needed.

Status: LEAN-CHECKED, not independently reviewed and not integrated into main. A separate clean end-to-end rebuild and further interpretation fixtures are recorded in the later submission. Shared Discussion delivery remains blocked and no room message is claimed sent.
