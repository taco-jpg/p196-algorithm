# Open problems and preserved limitations

Documentation source checkpoint: [`10a173cb635fa8d03e357f454232816fc3e77609`][snapshot]
on 16 October 2026. This page distinguishes the mathematical targets from
the evidence needed to report them as established. It is a bounded review
of the sources linked below, not a census of every contribution or a new
Lean execution.

## Four different questions

| Question | What must be established | What the cited sources currently supply |
|---|---|---|
| **A. The particular orbit of 196** | Every iterate of the ordinary decimal reverse-and-add orbit of 196 is nonpalindromic. | The [scoped status checkpoint][status] records restricted palindrome-prefix exclusions. Such exclusions do not cover every possible palindrome. An existence theorem for some integer does not identify that integer with 196. |
| **B. Decimal Lychrel existence** | An ordinary natural number whose entire orbit is nonpalindromic, with the time convention stated explicitly. | The published `Agent112.Admissibility.certificate_existence_of_check` gives this conclusion **conditional on an accepted concrete return certificate**. It already supplies the admissibility-to-integer route described below. |
| **C. Supporting structural results** | The exact statement of each bridge, restriction, finite certificate, or conditional implication, with its hypotheses. | These results have their own domains and evidence records. A restriction on possible certificates or a finite safe interval does not itself provide an accepted return certificate or complete avoidance for 196. |
| **D. Verification and integration** | Reproducible source and dependencies, the actual compiler/axiom checks, separate semantic review, and the integration state of the relevant version. | Each result must retain its own records. Source publication, a compiler pass, independent review, and presence on the default branch describe different facts. |

For the interpretation of conditional theorems, finite experiments, and
unfinished work, use the [publication policy][policy]. The historical
[accepted-build catalogue][registry] is explicitly incomplete; absence
from that catalogue is not a withdrawal of a separately verified result.

## The conditional certificate-to-integer route already exists

The relevant sources use the original `Agent109.Cert.Certificate` and
`Agent109.Cert.check`. The checker requires a nonempty cyclic list of
states and the specified local conditions at every cyclic link: phase and
coefficient bounds, the exact successor/trimming identities, the
nonpalindrome condition, and both band-length inequalities. See
[`LocalOK`, `Valid`, and `check`][checker]. A cycle in a different
finite projection is not automatically an accepted value of this type.

| Declaration | Exact role and conditions |
|---|---|
| [`Agent109.Cert.certificate_sound`][soundness] | Given `check cert = true`, an ordinary integer `n` whose `pairWord` equals the first certificate template, and band lengths `G,H` at least the first link's two lower bounds, every iterate of **`step n`** is nonpalindromic. The conclusion starts at the successor of `n`. |
| [`Agent109.Cert.template_realized`][realization] | Realizes a template as an ordinary integer pair word under `Phase c`, positive first band length, bounded `B,A,C`, `Mirr C`, and the stated positive-head condition on `B`. These hypotheses are part of this general realization lemma. |
| [`Agent109.Cert.certificate_existence`][original-existence] | The original existence endpoint takes `check cert = true` and the Boolean proof of `Admissible0 cert H M`. It concludes `∃ m, ∀ k, ¬ Palindrome (orbit m k)`, including time zero for `m`. |
| [`Agent112.Admissibility.automatic_admissibility`][automatic] | Derives `∃ H M, Admissible0 cert H M` from `check cert = true`. Admissibility is therefore not an additional unsupplied premise of the following endpoint. |
| [`Agent112.Admissibility.certificate_existence_of_check`][check-existence] | Takes only a certificate and `check cert = true`, and concludes `∃ m, ∀ k, ¬ Palindrome (orbit m k)`. The ordinary-integer realization is already provided by the cited implication chain. |

These are precise source-level interfaces, not newly checked theorems of
this documentation increment. The retained verification records must be
read with their exact source and dependency scope; no fresh compilation
or axiom audit is claimed here.

### The missing input to this particular route

The linked implication modules do not supply a concrete accepted
certificate. To turn this route into an unconditional existence result,
supply the actual finite certificate value and a verified proof that the
**original** checker returns `true`. Preserve its complete data, source
dependencies, commands, compiler and axiom-audit output, and independent
review of the instantiated mathematical conclusion.

Do not reopen automatic admissibility as an independent mathematical
obligation of `certificate_existence_of_check`. Conversely, an
uninstantiated implication does not establish that an accepting
certificate exists. An accepted Boolean certificate in a different
language needs an exact bridge to this interface before it can use this
endpoint.

This return-certificate route is a sufficient criterion. The cited
sources do not establish that every decimal Lychrel number must arise
from such a certificate. Failure of a bounded search, rejection of a
particular candidate, or even exclusion of a specified certificate family
does not by itself disprove decimal Lychrel existence.

## What an application to 196 would still need

A witness supplied by `certificate_existence_of_check` is some ordinary
integer; its conclusion does not say that the witness is 196 or lies on
the orbit of 196.

For a direct use of `certificate_sound` after an actual orbit entry,
the additional work has a concrete form:

1. Identify an actual integer `n = orbit 196 t` and prove that its
   `pairWord` is the first template of the accepted certificate.
2. Prove the two required band-length bounds for that same realization.
3. Use the existing compatibility results to identify these iterates with
   the ordinary decimal orbit, and verify the finite prefix through `n`.
   The source theorem then covers the tail starting at `step n`;
   it does not certify that earlier prefix.

These are application obligations for this route, not a claim that no
other proof strategy could settle the question. A symbolic return, a
numeral realization of an unrelated state, or a long computed trajectory
must retain its actual scope.

## Structural restrictions and unfinished verification

Use each result's exact domain when deciding what a future candidate must
satisfy. For example, the published
[`Agent110.Checked.period_at_least_four`][period] assumes checker
acceptance and derives a lower bound on the certificate period.
The adjacent `six_phase_constraints` additionally assumes the initial
phase lies in `{2,4,8,16,14,10}`; the saturated endpoint additionally
assumes its stated equality between period and total overflow.
Such necessary conditions do not construct a candidate or check one.

Keep the status of a claim separate from the status of its files:

- **PROPOSED / IN_DEVELOPMENT:** the stated obligation is still under
  development; a proposed statement or unfinished source is not a
  completed proof.
- **SOURCE_PUBLISHED:** the exact source is retained and accessible.
- **LEAN_CHECKED:** cite the actual successful execution, toolchain,
  dependency closure, and axiom scope for that source.
- **INDEPENDENTLY_REVIEWED:** identify the nonauthor reviewer and the
  precise mathematical and evidence scope reviewed.
- **INTEGRATED:** identify the actual default-branch integration. This
  does not replace the preceding verification evidence.
- **DISPROVED / SUPERSEDED:** identify the exact counterexample or
  replacement and preserve the earlier claim's historical meaning.

Unknown searches, timeouts, incomplete builds, missing concrete
instances, and missing links between a model and integer dynamics remain
explicit obligations in their own scopes. A claim absent from one
catalogue is not thereby disproved. A supporting theorem must not be
reported as resolving either central question merely because it has been
published, checked, or merged.

## Preservation and coverage of this update

The [previous version of this page][original] is retained byte-for-byte.
The reorganization's historical classifications, reports, manifests, and
source-map records are unchanged. This update explains existing
interfaces and remaining application requirements; it adds no mathematical source,
certificate instance, discovery computation, or mathematical acceptance.

[snapshot]: https://github.com/taco-jpg/p196-algorithm/tree/10a173cb635fa8d03e357f454232816fc3e77609
[status]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/STATUS.md
[policy]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/PUBLICATION_POLICY.md
[registry]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/ACCEPTED_BUILD.json
[checker]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/ReturnCertificate__3f43ec0db45b8fd7.lean#L187-L223
[soundness]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/ReturnCertificate__3f43ec0db45b8fd7.lean#L256-L273
[realization]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/ReturnCertificate__3f43ec0db45b8fd7.lean#L371-L380
[original-existence]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/ReturnCertificate__3f43ec0db45b8fd7.lean#L383-L416
[automatic]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/AdmissibleHeads__e610dff2fe6106d5.lean#L165-L168
[check-existence]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/AdmissibleHeads__e610dff2fe6106d5.lean#L170-L173
[period]: https://github.com/taco-jpg/p196-algorithm/blob/10a173cb635fa8d03e357f454232816fc3e77609/proofs/CertificateChecked__28f9e37f0a4c7634.lean#L11-L46
[original]: archive/documentation/agent-60/10a173cb635fa8d03e357f454232816fc3e77609/OPEN_PROBLEMS.md
