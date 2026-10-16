# Agent #111: exact-length palindrome residues

This contribution formalizes the existing written argument in
`proofs/research/astra_modular_fixed_modulus_theorem.md`, sections 1–2.
It is not a novelty claim, an actual palindrome hit, or a proof of P196.

The full arbitrary-modulus saturation theorem and fixed-modulus invariant
obstruction are **LEAN-CHECKED** in the incremental development build.
`Saturation.exact_length_palindrome_residues` (namespace `ExactLengthResidues`)
has no unproved saturation or certificate premise. A full clean rebuild and
complete independent review are in progress. Supporting modules construct the
nonzero outer block, split the modulus, span residues, and realize disjoint
mirrored digit pools as genuine ordinary decimal palindromes. Each source
has explicit transitive `#print axioms` commands; only `propext`,
`Classical.choice`, and `Quot.sound` are allowed. No compiler-trusted evaluation
shortcut is part of these proofs.

The claim is serialized on `p196/coordination` as
`agent111-exact-length-residue-saturation`; its first successful publication
was `3996f9b99037484056b9c541b06dd869470365e5`. The source baseline is
`main` at `eec3d5f3646cab50abad6e610ea19626cd249070`.

Lean is pinned to 4.19.0, release commit `6caaee842e94`. The only planned
external dependency is Lean/Std; the repository's unchanged canonical
decimal semantics will supply the integer realization and orbit interface.
The local runtime's disclosed process-path adapter is infrastructure only;
normal Linux uses the official compiler directly.

`development/` retains substantive failed attempts, successful compilation
logs, and API probes. Such drafts are outside the accepted module list.
`verification/base/` records the clean build of the unchanged canonical
dependency. A separate clean build and independent review of the completed
contribution are pending.

Remaining acceptance obligations: exact-source clean rebuild, complete
independent semantic review, and reviewable publication. A separate corollary
for the original factorization-based explicit bound is being assembled.
The unrestricted 196 conjecture remains open.
