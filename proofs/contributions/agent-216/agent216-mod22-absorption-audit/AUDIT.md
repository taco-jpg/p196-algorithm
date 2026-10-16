# Agent #216 — mod-22 absorption audit

## Finding 1: forward absorption is valid and scoped

The current GeneralMomentAbsorption source proves, for general m >= 1, that if the exact exterior step overflows then the next moment is 0 modulo 2*(m+2). It also proves that a zero residue remains zero under subsequent exact exterior steps when exterior coefficients stay in 0..2m. For decimal m=9, the modulus is 22.

This is a forward absorbing-class statement. It is not an equivalence between zero moment and post-overflow state.

## Finding 2: a converse is false

For the exact decimal state (m,c,B)=(9,2,[1]), the formal source added by Agent #216 establishes moment 2 [1] modulo 22 = 0 while exteriorOverflow 9 2 [1] = 0. Thus zero residue does not imply overflow. The source is in proofs/contributions/agent-216/agent216-mod22-absorption-audit/Mod22AbsorptionAudit.lean, commit f71b90d4a00cde1d4d40745f0c90ada1b28c73b7.

Verification status is WIP/source-only because this execution has no available Lean compiler invocation. The proof text uses decide +kernel; that syntax is not being represented as executed verification.

## Finding 3: residue_filter enumerates the absorbing class, not only overflow states

proofs/residue_filter__6ccf2a4becd383d9.py defines exhaustive as all canonical exteriors satisfying moment(c,B) modulo 22 = 0. Its candidates generator is compared against exactly that set, and the verifier checks the next state also has zero moment. The enumeration does not impose exteriorOverflow(c,B)=1.

However, the module docstring says the prefilter concerns closed cycles with an overflow, not pre-overflow states. The mathematically accurate interpretation is: the script enumerates the full canonical zero-moment residue class in the finite cap and verifies closure of that class under transition. It does not enumerate only post-overflow states. This is a documentation/scope mismatch, not necessarily a mathematical defect in the residue-class filter itself.

## Consequence for P196

Neither result proves decimal Lychrel existence or proves anything about the 196 orbit. The mod-22 mechanism is useful as a necessary condition for closed cycles containing an overflow, but zero residue is a broader class than post-overflow. Any downstream argument silently replacing the former by the latter requires correction.