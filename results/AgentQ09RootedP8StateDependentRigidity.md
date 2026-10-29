# AgentQ09RootedP8StateDependentRigidity
**PAPER PROOF, base 10, all palindromic centre words and all widths:** for the published rooted p8/m20 exterior B of length 39, a universal digit permutation pi with incoming-carry-dependent coefficient relabelings a_0,a_1 that preserve the carry bit cannot map B ++ C ++ reverse(B) to a symmetric pairword unless pi,a_0,a_1 are all identity.
The 40320 possible rooted state-dependent permutations are reduced to identity by seven concrete, centre-independent mirrored carry witnesses. No bound on C, its temporal evolution, or its symbolic length is needed.
**Necessary-condition reduction:** a nontrivial symmetry-twisted positive-growth return that retains this fixed exterior must change carry ports (with an explicit regenerated junction), use position-dependent rules, or change exterior; carry-preserving state-conditioned digit relabeling is insufficient.
**Not claimed:** a decimal all-time certificate or a no-go for unrestricted p8 centres.
Proof: `calculation/new_structures/Q09/rigidity_proof.md`.
Exact source, independent bigint checks at widths 20/40/80/160, and 40320-permutation enumerator: `calculation/new_structures/Q09/rigidity.py`.
Reproduce: `python3 calculation/new_structures/Q09/rigidity.py`.
