# Reverse accepting-input realization

`Agent107TransducerInput.lean` closes the reverse legal-input obligation
inside the original full-path task. Its thirteen exported theorems compile
under Lean 4.19.0 with `--trust=0 -j1 -DElab.async=false`. All exports have
printed transitive axiom reports, with union `propext, Quot.sound` only.
The successful author execution is `build-02.log`, exit zero. The failed
list-congruence attempt and its complete log remain preserved separately.
`manifest.json` pins every source dependency and log involved.

An arbitrary function accepted by `Accepts L q p` need not be symmetric:
its high half is never examined. `symmetrize` explicitly reconstructs this
high half from the read lower folded half and optional center. Acceptance
itself implies positive physical width, positive outer pair coefficient,
pair coefficient bounds, and bounded even center. Thus
`reconstructed_admissible` needs only literal acceptance, not an assumed
admissibility premise or an equality already asserting the goal.

The same reconstruction leaves `Accepts`, `foldPrefix`, and `pathOutput`
unchanged. `accepting_input_realizable` applies the existing attributed
`valid_word_realizable` theorem to these derived premises and produces an
ordinary positive finite decimal numeral with a canonical representation
at exactly width `L`. No new generic realizability theorem is claimed.

This author compilation uses the already compiled frozen definitions,
Path module, and separately rebuilt original foundation. It is not labeled
an independent clean rebuild. The full package review and fresh dependency
build remain the coordinator/reviewer's separate evidence obligation.

Reproduce from the repository root with the fixed dependency directories:

```sh
LEAN_PATH=/workspace/scratch/94808c4aecb2/agent107-path-build:/workspace/scratch/94808c4aecb2/agent107-build:/workspace/scratch/94808c4aecb2/agent107-runtime/baseline \
  /workspace/scratch/94808c4aecb2/agent107-runtime/lean-4.19.0-linux/bin/lean \
  --trust=0 -j1 -DElab.async=false \
  -o /workspace/scratch/94808c4aecb2/agent107-path-build/Agent107TransducerInput.olean \
  proofs/Agent107TransducerInput.lean
```
