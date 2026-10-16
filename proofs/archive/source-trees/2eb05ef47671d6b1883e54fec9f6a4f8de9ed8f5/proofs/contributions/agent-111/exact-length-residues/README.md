# Agent #111: exact-length palindrome residues

This contribution formalizes the existing written argument in
`proofs/research/astra_modular_fixed_modulus_theorem.md`, sections 1–2.
It is not a novelty claim, an actual palindrome hit, or a proof of P196.

The full arbitrary-modulus saturation theorem and fixed-modulus invariant
obstruction are **INDEPENDENTLY-REVIEWED**, including an independent fresh rebuild from
the immutable remote source commit
`c3192d5bf2962298bcb2bb209a0947f657e8a7e5`. There is no unproved saturation or
certificate premise in the final endpoints. The accepted entry point is
`All.lean`; historical attempts under `development/` are not build targets.

For every positive modulus M, every sufficiently large exact decimal length L
has a positive palindrome in residue class a exactly when

- it is not the case that both M and a are divisible by 10; and
- if L is even, gcd(M, 11) divides a.

For M = (2^alpha * 5^beta) * q with q positive and coprime to 10, a proved
threshold is 2*k + 4*q*r, where k = max(1, alpha, beta) and r is any positive
period of 10 modulo q. The q = 1 case is included; minimality is not claimed.

| Completed theorem in namespace `ExactLengthResidues` | Meaning |
|---|---|
| `exact_length_palindrome_residues` | Arbitrary positive modulus; exact necessary and sufficient conditions above. |
| `exact_length_palindrome_residues_explicit` | The same criterion at the displayed explicit threshold. |
| `every_orbit_matches_palindrome` | A positive actual orbit has a state with the same width and fixed residue as a palindrome. It need not equal that palindrome. |
| `fixed_modulus_closed_set_contains_palindrome` | A nonempty positive forward-closed set whose eventual membership depends only on exact width and one fixed positive modulus contains a palindrome. |

Supporting modules construct the nonzero outer block, split the modulus, span
residues, and realize disjoint mirrored digit pools as ordinary finite decimal
integers using the repository's unchanged canonical digit semantics.

The claim is serialized on `p196/coordination` as
`agent111-exact-length-residue-saturation`; its first successful publication
was `3996f9b99037484056b9c541b06dd869470365e5`. The source baseline is
`main` at `eec3d5f3646cab50abad6e610ea19626cd249070`.

Lean is pinned to 4.19.0, release commit `6caaee842e94`, using Lean/Std and
`proofs/research/Lychrel196Research.lean`; no Mathlib is needed. The complete
13-module import closure was independently rebuilt with no existing project
objects. All 1004 compiled theorem constants (including private and generated
ones, not 1004 distinct research results) were audited. The axiom union is
`propext`, `Classical.choice`, and `Quot.sound`. No `sorryAx`, custom safe axiom,
or compiler-trusted evaluation dependency occurs. Thirteen compiler-generated
unsafe implementation auxiliaries are separately recorded and do not appear
in theorem axiom dependencies.

See [the independent rebuild](review/INDEPENDENT_REBUILD.md) and
[its full report](review/independent-full/verification.json). The local
runtime's disclosed process-path adapter is infrastructure only; normal Linux
uses the official compiler directly. Independent automated review does not
mean external human peer review.

Semantic review covers every new module with a reviewer who did not author it:
[ten modules](review/span-author-other-modules.md),
[the span and orbit interfaces](review/digits-author-span-orbit.md), and an
additional [endpoint review](review/digits-author-saturation.md).
[ACCEPTANCE.json](review/ACCEPTANCE.json) records that coverage and the exact
source pins. Main-branch integration is a separate coordination step.

Both [official Linux CI runs](review/official-linux/CI.json) also passed the
same 13-module, 1004-theorem audit with an empty `LD_PRELOAD` and identical
mathematical source hashes. Their complete audit archives, decoded file
inventories, checksums, and recovery commands are retained in that directory.

From the repository root, use fresh, separate output directories:

```sh
python3 -B proofs/contributions/agent-111/exact-length-residues/check.py \
  /absolute/path/to/lean-4.19.0-linux/bin/lean --module All \
  --build-dir /tmp/p196-agent111-build \
  --output-dir /tmp/p196-agent111-report
```

The checker verifies the pinned Linux compiler and runtime fingerprints,
rebuilds the entire local import closure, enumerates compiled theorem
constants, and checks their actual transitive `#print axioms` output. Source
hashes, commands, exit codes, and substantive logs are retained. It is an
audit harness; the mathematical proofs are checked by Lean's kernel.

`development/` retains substantive failed attempts, successful compilation
logs, and API probes. Such drafts are outside the accepted module list.
`verification/base/` records the clean build of the unchanged dependency;
`verification/clean/` and `review/independent-full/` retain the author and
independent fresh builds. `COMPRESSED_EVIDENCE.json` identifies the one
losslessly compressed API probe, including exact recovery instructions.
Compiled objects, duplicate build trees, runtime installations, Python caches,
and publishing helpers are reproducible infrastructure and excluded.

The modular invariant obstruction supplies a limitation on one proof strategy.
It does not prove decimal Lychrel existence, an infinite safe seed, an actual
palindrome hit in the orbit of 196, or the unrestricted 196 conjecture.
