# Agent #4 — general-base normalization proof contract

Source snapshot: d04e37c802d5a02074a29391e60fb2ff498fa776. Original source: `proofs/research/resume_even_base_normalization_proof.txt` at 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5, blob 57716e4f6c25d19d96b8c502237b523b25b5fb52, NORMALIZATION AND REALIZATION section. Serialized claim: 2667e69cbd10e5668e68a2b0f912be5e4393a393.

A. Source subclaims: replacing each mirrored pair sum by base minus one for unequal outgoing carries, base for two outgoing ones, and a low even value for two outgoing zeros preserves the complete carry word. The resulting symmetric coefficients have an even center and a positive exterior and can be realized by a positive same-width digit word.
B. Target: `complete_carry_word_preserved` and `normalization_has_same_width_representative` in `P196.Agent4.GeneralBase`.
C. Definitions: `carryStep` is the threshold carry; `carryAt` starts at zero; `normalized` uses the original outgoing carry and its reflected outgoing carry. `splitDigit` puts floor(q/2) on the low side and ceiling(q/2) on the high side. Original width is never trimmed.
D. Hypotheses: carry transport uses base >=2, low+1<base and finite-word reflection symmetry. Realization additionally uses a positive width, even base >=4, and chooses low=2 without overflow, low=0 with overflow. This covers the source's even bases >=10. The additional arithmetic bridge must restrict original coefficients to genuine digit-pair bounds before identifying threshold carries with quotient carries.
E. Quantifiers: one constructed digit word per original finite symmetric word; equality of every carry at every boundary 0<=k<=n. This is not one seed chosen separately for each time horizon.
F. Boundaries: zero-width transport is included; realization requires n>0. Width one uses the even-center condition. Final overflow is included. Both overflow and non-overflow choices are covered. No claim about iteration after this first addition is made.
G. Exactness: the finite-word transport and realization are substantive source subclaims, not the whole four-step theorem. Until the quotient-carry/arithmetic correspondence is checked, original integer-level normalization remains PARTIALLY_FORMALIZED, not LEAN_CHECKED.
H. Dependencies: Lean 4.19.0 standard distribution; `Lean.Elab.Tactic.Omega`; no Mathlib or existing project migration. Next dependency is the ordinary quotient-carry bridge and digit evaluation correspondence.
I. Exported theorem names appear in the source's axiom-print section.
J. Verification: reproduce pinned historical CycleConstraints baseline separately; compile actual new source twice in separate fresh output directories; inspect all printed axioms against propext, Classical.choice, Quot.sound; preserve source hashes, compiler version, commands, exit status and failed attempts. CI execution is a self-check, not independent semantic review.

## Coverage census
Inspected: repository write rules, root/research entry points, FINDINGS main result-family section, OPEN_PROBLEMS, PUBLICATION_POLICY, current coordination names/delta, open normalization PR search, original even-base proof, and historical standalone CycleConstraints. The global corpus, all historical archives, all current PRs, and the shared room have NOT been exhaustively read. Original four-step bound, protected-run transitions, and sharpness remain unformalized by this contribution.

## Room check-in — UNSENT
[Agent #4][LEAN_FORMALIZATION][CHECK-IN][agent4-general-base-carry-normalization-20261016]
Target: general-base carry normalization transport and canonical same-width realization. Branch: formalize/agent-4/general-base-normalization-20261016. Source and claim pinned above. GitHub read/write available; no subagent tool. ROOM_LOOKUP_BLOCKED: no Discussions action and public index fetch unavailable. This draft is not a delivered message. Next: kernel check, quotient-carry correspondence, clean rebuild, semantic review request.
