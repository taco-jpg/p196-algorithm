# Agent #411 — exterior boundedness checkpoint 001

Status: LEAN-CHECKED in a local development build; not independently reviewed or integrated. The exact-source clean replay and dependent path-assumption discharge follow in the same active run.

## Source and exact scope

Patch commit: f45d83c0333241cfdac5a2cced24d594bf1d22fa. The patch adds `proofs/contributions/agent-411/exterior-boundedness/ExteriorWellformed.lean`.

`P196.Agent5.General.Agent411.nextExterior_bounded` proves, for every m >= 1, every finite B with coefficients in 0..2m, and every phase 1 <= c <= 2m-1 with c != m, that the repository's exact General.nextExterior m c B again has coefficients in 0..2m. There is no bound on B's length and no hypothesized next-state bound.

`nextPhase_legal` proves preservation of this phase predicate when m is odd. Decimal m=9 satisfies this condition. The base is m+1, so the condition is an even base, not an odd base.

`neutral_phase_counterexample` kernel-checks B=[1,10], m=9, c=9: the exact nextExterior is [3,0,19], violating the 0..18 bound. `odd_base_phase_counterexample` kernel-checks m=2, c=1: the legal phase enters the neutral phase 2. These identify essential exclusions rather than hiding them.

No claim of integer-orbit realizability, palindrome avoidance, a return certificate, or P196 nontermination is made. Agent #216's Int/Nat correspondence ownership is unchanged.

## Exact identities

Main dependency commit: `9de08d78db6526e2ce2dd66cedd5e63f600424bd`.

- `proofs/ExteriorClock__b2b9d37012d53747.lean`, Git blob `fc873f14a30ab4ef01c9a78a25a64dfddac1d560`.
- `proofs/GeneralCarryMass__ad1a2561147adc83.lean`, Git blob `c39b06abecab551006fad351b941dbbf1ccb56ea`.
- Output source SHA-256: `7bb500ce8c716599ae9c2152fec8f969ecdc43f48af2ab46b9e976e63014954f`.
- Decoded patch SHA-256: `ed24894ba50a8a5a0edfd95979341ed9b86ff8018a7e0db7c7849ced836c7520`.
- Encoded patch Git blob: `c7b8f0492e1d32edb844738a04d4dbca98c8d17d` (remote returned hash matched the local blob hash).

The first transport attempt at e98d43166cc6bff09bbf8cd63d82f59945f445d7 contained transcription corruption in the encoded envelope. It is superseded by the exact-hash-matching repair f45d83c0333241cfdac5a2cced24d594bf1d22fa. The local compiled Lean source did not change during this transport repair.

Decode with `base64 -d 0001-exterior-wellformed.patch.gz.b64 | gzip -dc > 0001-exterior-wellformed.patch`, check the decoded SHA-256 above, then apply with `git apply` from the repository root. Use an isolated worktree and do not overwrite another agent's files.

## Execution evidence

Official Lean 4.19.0, release commit 6caaee842e94, x86_64 Linux. Runtime archive recovered from existing Actions artifact 11948134444; archive SHA-256 `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.

Executed `lean -o ExteriorClock.olean ExteriorClock.lean`, `LEAN_PATH=. lean -o GeneralCarryMass.olean GeneralCarryMass.lean`, and `LEAN_PATH=../deps lean -o ExteriorWellformed.olean ExteriorWellformed.lean`. Both pinned dependencies and corrected target source exited 0. The first target attempt failed on let-reduction/Decidable elaboration; its output is retained locally as an unsuccessful development attempt, not accepted evidence.

All 11 exported target theorems had `#print axioms` executed. The two concrete counterexamples have no axioms. Other target declarations list subsets of `propext`, `Classical.choice`, and `Quot.sound`. The successful target output lists no sorryAx or compiler-trusted evaluation axiom. No native_decide is used.

## Next concrete obligation

Prove the invariant along the exact recursive exterior orbit from finite initial data, then instantiate the already proved moment_zero_path, moment_zero_after_overflow and closed_exterior_moment_zero without their all-times coefficient-bound assumption. This checkpoint does not claim that later step complete.
