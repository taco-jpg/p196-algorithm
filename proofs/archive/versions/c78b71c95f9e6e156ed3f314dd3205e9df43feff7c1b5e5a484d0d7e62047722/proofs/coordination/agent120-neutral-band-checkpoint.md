# Agent #120 checkpoint — neutral one-band template calibration

Branch `research/agent-120/s20261015T1625`, source commit `59779bc`
(development build; clean rebuild and independent review pending).
Directory: `proofs/contributions/agent-120/neutral-band-calibration/`.

## Reusable Lean interfaces (core Lean 4.19.0 + Std, standard axioms only)

| Declaration | Content |
|---|---|
| `Agent120.Neutral.step_tmpl` | For every base `b ≥ 2`: if the two band carries differ, one ordinary base-`b` reverse-and-add step maps the value of `B ++ (b-1)^g ++ C ++ (b-1)^g ++ reverse B` to the value of the explicit next template (gap `g - gam`). |
| `Agent120.Neutral.not_isPal_tmpl` | Same hypotheses, gap `≥ 2`: the value is not a base-`b` palindrome. |
| `Agent120.Neutral.lychrel_of_cycle` | A kernel-checkable cyclic interface certificate (`cycleOK`) with gain ≥ overflows gives a base-`b` Lychrel value for every gap `≥ 2 + overflows`. |
| `Agent120.Neutral.PowerTwo.lychrel2_22` etc. | `Lychrel 2 22`, `Lychrel 4 318`, `Lychrel 8 4522`, `Lychrel 16 69630` (kernel `decide`). |

## Scope

These are base-2^m calibration results: the repository's template-quotient
method does find Lychrel numbers where they are known to exist. They are
**not decimal results and say nothing about 196**. Exploratory finite-scope
searches find gain-1 cycles exactly in bases 2, 4, 8, 16, 32 among the tested
bases and none in base 10 within the stated caps (`NOTES.md`). For base 10,
persistence of a neutral outermost band forces an autonomous exterior map
`E_10`; no periodic orbit was found from any exterior of length ≤ 4 (cap 80).
An all-width obstruction for `E_10` is an open target, not claimed.
