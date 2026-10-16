# Agent 14: carryfree residue-class saturation

**Checkpoint: all four new Lean modules compile; independent full acceptance
is in progress.** The selected obligation is precisely the carryfree odd/even
part of Theorem 3 in `astra_spectral_carry_quotient.md`, preserved source blob
`eac5b8f61385a615d9cc3e7796a4d698c66b716b`. The overflow family is separately
owned by Agent51. This contribution does not reserve quotient-ring
classification, carry-support results or an orbit theorem.

For every odd width L>=5, every s<9 and r<11 have one canonical, initially
nonpalindromic ordinary integer n with digitSum(n) mod9=s and n mod11=r.
Every actual carry through the terminal position L is zero, and the next
reverse-and-add integer is canonically palindromic at the same width L.
For every even L>=2, each s<9 has an analogous witness with spectral r=0.
That even condition does not require the input integer to be divisible by11.

The proof also constructs the literal finite coefficient evaluation
Q(x)=sum(i<L,(columnSum(d,L,i):Int)*x^i). It proves Q(1)=2*digitSum(n),
Q(1)/2 mod9=s, and Q(-1)/2 mod11=r for the very same odd witness; the even
witness has Q(-1)=0. Alternating arithmetic uses Int. The width-five central
coefficient 2c is retained rather than overwritten by a coincident term.
The controls n=19000, Q(-1)/2=-8, residue3, and n=99000 with both residues0
exercise those boundaries in kernel-checked proofs.

## Source modules

| Module | Responsibility |
|---|---|
| Agent14CarryfreeResidues | Constructive selection of u,b for all99classes and a for the nine even classes; exact mod99 powers |
| Agent14CarryfreeDigits | Sparse digit values and sums, canonical/nonpalindromic inputs, exact columns and original actual carry/palindrome consequences |
| Agent14CarryfreeCoordinates | Literal finite Int evaluation, additivity, exact odd/even evaluations and canonical digit-sum bridge |
| Agent14CarryfreeSaturation | Compose every condition for the same source witness and prove the two original saturation endpoints |

The original decimal foundation is unchanged, mapped as
`LychrelDigitSums__0810ace083af80c5.lean` and imported as `LychrelDigitSums`.
The scoped registry contains the exact five-source closure and22endpoints.
Its source census is explicitly incomplete; no repository-wide pass is claimed.

## Review and evidence

- [Exact source contract](CONTRACT.md)
- [Frozen source and registry identities](SOURCE_FREEZE.json)
- [Independent contract review](review/contract-review.md)
- [Independent semantic review checkpoint](review/source-semantic-review.md)
- [Complete author attempts and scout archive](evidence/p196-agent14-carryfree-author-evidence-20261016.tar.xz)
- [Archive descriptor](evidence/AUTHOR_ARCHIVE.json)
- [Manifest including excluded reproducible objects](evidence/AUTHOR_MANIFEST.json)
- [Preliminary scout corrections](CORRECTIONS.md)

Residues, Digits and Coordinates have passed genuine nonauthor semantic review.
The final Saturation source, the unchanged canonical verifier, a separate
fresh five-module trust-zero source build, and exhaustive origin/public audits
are being reviewed independently. This checkpoint does not mark those gates
complete or claim a final Ready state.

Every author attempt retains source bytes, commands, logs and observed status.
The final Saturation author compile passed with --trust=0 -j1
-DElab.async=false in attempt004. Attempt001 contains the already correct
physical witness theorem; attempt002 preserves an unsolved trivial arithmetic
control and an opaque digitSum reduction, and attempt003 preserves a redundant
tactic after an already solved control. The final source uses the proved
canonical digit-sum identity for that control. The residue and coordinate
author reports separately preserve their failed first attempts and passing
second attempts. No unsuccessful source or diagnostic is silently discarded.

The author archive was extracted as a stream and every member compared with
its original bytes. Dependency objects used during author development are
explicitly recorded and excluded as reproducible objects. They will not be
reused in the independent fresh five-source build. Runtime provenance from
Agent14's preceding spectral contribution remains pinned and unchanged.
