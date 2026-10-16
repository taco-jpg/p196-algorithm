# Carry-prefix checkpoint, not a completed first-hit-eleven proof

The source target is every r>=5, every canonical ordinary decimal realization of `DelayedOverlapGate.initial r 1 1 6`, exact first positive palindrome time 11. Source snapshot remains `74df59c5ecb6cb30fb3c88b1d5b26fdb9526d6c4`, `renewal_pass/tails/STATUS.md` and its retained symbolic trace.

`ElevenCarries.lean` proves three supporting declarations: the actual incoming carries for every proposed stage t<10 and every actual column, every resulting width transition, and a generic actual next-column formula from a proved carry certificate. These statements are universal in k:Nat with r=k+5, including all zero-length gaps at k=0. They do not yet establish that successive proposed pair words agree with actual nextColumns, or that an ordinary orbit first hits at eleven.

Initial source compilation of this prefix passed, and all three exported transitive axiom reports passed the standard allowlist. The first whole-file development build hit an external time cap. A focused prefix build revealed an equality-substitution issue in the generic formula; explicit rewriting repaired it without changing the proposition. The next-pair proof is being partitioned into finitely many explicit index regions while retaining arbitrary k and i. Incomplete candidates are not in the accepted manifest or published Lean target.

Remaining chain: actual next-pair identities at stages0–9; safety at outputs1–10; final bad-word classification; actual integer representation induction; positive realization; complete fresh rebuild and endpoint axiom audit. The decimal endpoint-string identity is a separate source claim.

The underlying fixed-target and first-hit-four modules were already integrated through PR22 at merge `62c7ab92158af09772e0be09eac8b01fab596b3e`. Their combined 21-export CI replay passed at `456fa2ccfbc7649e62c1dcd580136f068a9e4f2a`, run `38686629027`. Agent16 inspected the sources and that CI result but explicitly did not provide a new reviewer-operated Lean build or independent-review badge. That distinction remains unchanged.
