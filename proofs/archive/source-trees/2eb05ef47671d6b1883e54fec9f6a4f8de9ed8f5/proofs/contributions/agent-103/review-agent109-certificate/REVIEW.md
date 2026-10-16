# Independent adversarial review: Agent #109 return certificates

Task `agent103-review-agent109-certificate`. Replication/review only: **no new
theorem, and no certificate instance**. Reviewed source commit
`0ace6dde2af6f7e4982e2765c599052812018a83` (branch `research/agent-109/s20261015`).

## Inputs and toolchain

`sources.sha256` lists the seven compiled sources; the five Agent #109 files
match the author's `SHA256SUMS`, and `LychrelDigitSums.lean` has the
project-pinned hash `ca5f4652...0b57`. Compiler: official
`lean-4.19.0-linux.tar.zst` downloaded independently from the leanprover/lean4
release (SHA-256 `6fe3ce97...ba813fe`), commit `6caaee842e94`. The author's
`build.sh` was **not** used.

## Clean rebuild

Empty directory, `LEAN_PATH` restricted to it,
`lean -j1 -DElab.async=false -o M.olean M.lean`:

| Module | Exit | Time |
|---|---|---|
| LychrelDigitSums | 0 | 92 s |
| PeriodObstructions (Agent #8) | 0 | 6 s |
| TemplateStep | 0 | 7 s |
| Compat | 0 | <1 s |
| ReturnCertificate | 0 | 4 s |
| CertCompat | 0 | 1 s |
| CertDemo | 0 | <1 s (toy certificate correctly evaluates `check = false`) |

Text scan of all non-base sources: no `sorry`, `admit`, `native_decide`,
`sorryAx`, `ofReduceBool`, `implemented_by`, `extern`, `unsafe` or `axiom`.

## Axiom audit

`AuditAll.lean` (generated here) prints axioms for **all 131** non-private
top-level `theorem`/`def`/`abbrev` declarations of `TemplateStep`, `Compat`,
`ReturnCertificate`, `CertCompat`. Exit 0, 131 reports: 29 use
`[propext, Classical.choice, Quot.sound]`, 28 `[propext, Quot.sound]`, 29
`[propext]`, 45 none. The headline theorems `Agent109.Cert.certificate_sound`,
`template_realized`, `certificate_existence`,
`Agent109.CertCompat.certificate_isLychrel` and
`certificate_existence_lychrel` are within `{propext, Classical.choice,
Quot.sound}`.

## Statement review (adversarial points checked)

1. **Genuine target notion.** `certificate_existence_lychrel` concludes
   `Lychrel196.DecimalLychrelExistence`, the base file's unmodified
   `∃ n, IsLychrel n` with `IsLychrel n := ∀ k, ¬ Palindrome (orbit n k)` and
   `Palindrome n := reverse10 n = n`. Since `reverse10 0 = 0`, a witness is
   automatically positive, and trailing-zero numbers are correctly
   nonpalindromic. `Compat` proves Agent109's private copies of `reverseFuel`,
   `reverse10`, `step`, `Palindrome`, `orbit` equal the base definitions by
   structural induction; no weakened definition is substituted.
2. **No hidden premise.** `certificate_existence` assumes only
   `check cert = true` and the decidable `Admissible0` first-state condition;
   realizability (`template_realized`) is proved, not assumed. The band lengths
   used are the certificate's own `lo_0, lo'_0 >= 2`.
3. **Soundness structure.** `Inv` (successor of an integer realizing some
   listed state above its bounds) is preserved by `inv_step`, using the proved
   exact identity (8) (`actual_template_step`) and `template_trim`, and excludes
   palindromes by the band-length-independent exact test
   `step_palindrome_template`. The cyclic index uses `% P` with `0 < P`
   required by `check`.
4. **Faithfulness to the written criterion.** The bound inequalities
   `lo_(i+1)+2 <= lo_i+gamma_i+j+j1` (and primed) encode "nonnegative gain in
   each gap with sufficient within-cycle minima" in a strictly sufficient form;
   the checker may reject some true cycles (completeness is not claimed), which
   affects only search power, not soundness.
5. **Vacuity.** Validity of an actual certificate is exactly the open question;
   no instance is supplied. Because soundness is proved, any accepted
   certificate would yield a genuine decimal Lychrel number; it would not
   concern 196 unless the realized seed's orbit were separately joined to it.

## Verdict

INDEPENDENTLY-REVIEWED (PASS) at `0ace6dde`: clean rebuild, full 131-declaration
axiom audit, statement review. Conditional theorem only. Not INTEGRATED by this
review.
