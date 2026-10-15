# Independent review of `agent109-template-step-bridge` (Agent #102)

Reviewed source commit: `9a2f01e3831763fea87021aa6b9e8af0b94c8beb` (branch `research/agent-109/s20261015`),
directory `proofs/contributions/agent-109/template-step-bridge/`. Replication only; no new theorem.

**Verdict: INDEPENDENTLY-REVIEWED, PASS.**

## Clean rebuild

Independently downloaded official Lean 4.19.0 (`lean-4.19.0-linux.tar.zst`, SHA-256
`6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`; `lean --version`: commit 6caaee842e94).
Empty build directory; no reused `.olean`. Files copied from the commit (TemplateStep, Compat, Audit,
`2026-10-15-agent8-complementary-bulk/PeriodObstructions.lean`) and from main
(`proofs/research/continuation/LychrelDigitSums.lean`). Source hashes equal Agent #109's `SHA256SUMS`;
`PeriodObstructions.lean` at the commit is byte-identical to `origin/main`
(`83102a94…2991a`). All five compilations exit 0. See `rebuild_log.txt`.

## Axiom and token audit

All 17 printed declarations (12 in `Audit.lean`, 5 in `Compat.lean`) depend only on subsets of
`[propext, Classical.choice, Quot.sound]`. Scan of TemplateStep/Compat/Audit/PeriodObstructions for
`sorry`, `admit`, `native_decide`, `ofReduceBool`, `axiom`, `implemented_by`, `@[extern`, `unsafe`,
`partial def`, `csimp`, `opaque`: only hit is a comment in `Audit.lean` stating that `decide` is used.

## Statement check

* `template` is METHOD (1) verbatim (low-first full symmetric word); `Compat.template_eq` is `rfl`
  against `Agent8.template`. `stepWord w = pair (normalize w 0)` is the actual G on realized words:
  `pairWord_step : pairWord (step n) = stepWord (pairWord n)` holds for **every** `n`, with
  `pairWord n = pair (digits n)` and `digits` canonical low-first; `Compat` restates it with the
  accepted `Lychrel196.step`/`orbit`, and `Compat.isLychrel_iff` matches `Lychrel196.IsLychrel`
  (which quantifies over all `k`, including `k = 0`).
* `data`/`u0..u3`/`digitWord` are (3)/(4)/(5) exactly; band lengths are written `g+1`, `h+1`, so
  `t_c^g` there is `t_c^{g-1}` of (5). `norm_template`/`normalize_template` give (5) with the overflow
  digit appended iff `γ ≠ 0`; `gamma_le` gives `γ ≤ 1`.
* `Br`/`Ar`/`Cr` are (6) (`γ = 0`) and (7) (`γ = 1`) entry for entry. `stepWord_template` is (8)
  with source lengths `g+2`, `h+2` and target lengths `g+γ`, `h+γ` (= `(g+2)-2+γ`).
* Hypotheses are only `Phase c` (`1 ≤ c ≤ 17`, `c ≠ 9`) and coefficients `≤ 18`; none is vacuous.
  The canonicity hypotheses of METHOD sec. 2 are needed only for realizability, which this package
  does not claim; `actual_template_step` assumes an integer whose pair word *is* the template.
* Not covered (as Agent #109 states): trimming/quotient (10)-(11), realizability, any returned
  interface, any safety or P196 statement.

## Independent semantic control (not proof evidence)

`review_control.py` was written from METHOD_AND_PROOF.md only (Agent #109's `controls.py` was not
read): 20,000 random canonical templates (all 16 phases, `|B|,|A| ≤ 3`, symmetric `|C| ≤ 5` with even
middle, `g,h ∈ 2..6`) are realized by integers; literal `n + reverse(n)` is compared with (5) and with
`Q(2t_c; B_r, A_r, C_r; g-2+γ, h-2+γ)`. Result: PASS (`review_control_result.json`, seed 102).
