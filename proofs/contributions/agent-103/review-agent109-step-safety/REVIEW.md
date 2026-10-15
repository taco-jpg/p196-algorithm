# Independent review: Agent #109 complementary template step safety

Task `agent103-review-agent109-step-safety`. This is a replication review only; it
adds **no new theorem**. Reviewed source commit:
`5808b992ab4e6c302aa083924e3441f9b47f5216`.

## Inputs

`sources.sha256` pins the seven compiled sources. `NoPalStep.lean` and
`NoPalCompat.lean` match the author's `SHA256SUMS`. The dependencies
`TemplateStep`, `Compat` and `ReturnCertificate` are byte-identical to the
versions I reviewed earlier in `../review-agent109-certificate/`. The compiler is
the official Lean 4.19.0 `6caaee842e94` release, downloaded independently. The
author's `build.sh` was not used.

## Rebuild and audit

I compiled all modules in an empty directory with
`lean -j1 -DElab.async=false -o M.olean M.lean`:

| Module | Exit status | Time |
|---|---|---|
| LychrelDigitSums | 0 | 96 s |
| PeriodObstructions | 0 | 6 s |
| TemplateStep | 0 | 7 s |
| Compat | 0 | 1 s |
| ReturnCertificate | 0 | 4 s |
| NoPalStep | 0 | 9 s |
| NoPalCompat | 0 | <1 s |

`AuditAll.lean` prints the axioms of all 15 non-private top-level declarations
in `NoPalStep` and `NoPalCompat`:

- 6 depend on `[propext, Classical.choice, Quot.sound]`;
- 8 depend on `[propext, Quot.sound]`;
- 1 depends on no axioms.

The log contains no `ofReduceBool` or `sorryAx`. A token scan of both sources
finds no `sorry`, `admit`, `native_decide`, `axiom`, `implemented_by`, `extern`
or `unsafe`.

## Statement review

- **`not_stepPal`.** For `Phase c` (c in 1..17, c ≠ 9) and bounded `B`, `A`,
  the statement is `¬ StepPal c B A C`. `StepPal` is the criterion proved
  exact and band-length independent in `ReturnCertificate`, which I reviewed
  earlier. Hence the `¬ StepPal` conjunct of `Agent109.Cert.check` holds
  automatically.
- **`template_step_not_palindrome`.** For an ordinary `n` with
  `pairWord n = template c B A C (g+2) (h+2)` and bounded blocks, `step n` is not
  a palindrome.
- **`template_orbit_safe` and `NoPalCompat.lychrel_template_orbit_safe`.** If
  both bands are at least `2k+2`, then there is no palindrome at times
  `1..k+1`. Time 0 is correctly excluded from the claim. The Compat version
  concludes with the base file's unmodified `Lychrel196.Palindrome` and
  `Lychrel196.orbit`, through the `Compat` equalities verified in my earlier
  review.
- **Scope.** This is finite-time safety for realized complementary templates.
  The template's realizability is a hypothesis. There is no all-time claim, no
  Lychrel witness and no statement about 196.

## Verdict

INDEPENDENTLY-REVIEWED (PASS) at `5808b992`. This review does not integrate
the package.
