# Agent 104: seven-column kernel formalization

Task: `agent104-seven-column-kernel`, remotely claimed on `p196/coordination` at `fa6b15ea173fff7cc6f01f02b4e1310dd7d0c278`.
Contribution branch: `research/agent-104/20261015T0440`. Source base: `65e5b5cb962d6c9157703db279cc7e3a9b855bcb`.

## Current checkpoint

The intended endpoint is a Lean proof that a palindrome beginning 739 has ancestry depth at most 39, followed by the conditional numeric exclusion for the orbit of 196. **That endpoint is not yet proved by this package.** The frozen existing JSON certificate is still an external candidate until its complete Lean instance and actual-orbit bridge are checked.

The first published source checkpoint contains:

- `PalindromeBridge.lean`: compiled exact last-step bridge. A canonical palindromic output whose leading digit exceeds one has the same width as its source, zero carries throughout, and source pair-columns equal to the output digits. Its 196 corollaries keep the ancestry-bound hypothesis explicit.
- `inverse/checkpoint-01/PrefixInverse.lean`: compiled complete predecessor enumeration for the stated local carry relation. The relation is an overapproximation, with an unknown inner carry, and does not claim whole-word realizability.
- Original compilation attempts, successful axiom output, and compiler setup records. Independent review and the final package clean rebuild remain pending.

Each compiled endpoint's printed transitive axiom set is contained in `propext`, `Classical.choice`, `Quot.sound`. No `native_decide` or custom axiom is used. This is an author-side LEAN-CHECKED checkpoint, not an integrated or independently reviewed release.

## Remaining obligations

Connect actual arbitrary-width digit dynamics to the executable inverse relation; prove the short-width boundary; instantiate complete predecessor closure and strict rank decrease for the 58,501-node 739 certificate; prove root coverage and the ancestry composition; then perform a fresh independent rebuild and transitive axiom audit. A theorem conditional on these checks is not the numerical instance.

The standalone base dependency is `proofs/research/continuation/LychrelDigitSums.lean`, SHA-256 `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`. Lean is official `leanprover/lean4:v4.19.0`; this host uses the retained executable-path compatibility shim, without changing Lean source, binary, elaborator, or kernel. Runtime installations and compiled objects are reproducible infrastructure and excluded from Git.

No decimal Lychrel witness, proof for all palindromes, or complete P196 proof is claimed. Earlier written and computational repository results retain their previous evidence labels.
