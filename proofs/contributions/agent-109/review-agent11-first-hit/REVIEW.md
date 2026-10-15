# Agent #109 independent review of `agent11-general-base-first-hit`

Reviewed source: branch `formalize/agent-11/s20261015-coverage`, verified source
commit `42a165aac1028d261dd4b1bd245c2e169748ff39`: the five Agent #11 modules
`HighBase{Normalization,Pairs,Threshold,Numeric,FirstHit}.lean` and the six pinned
prerequisites (`SignedDigitUniqueness`, `BaseReflection`, `ResetNormalization`,
`PhysicalWidth`, `SeamSafety`, `ReverseAdd`) from the same commit
(`reviewed_sources.sha256`; `HighBaseFirstHit.lean` = `5116f8b1…`, matching the task record).

Kind: replication/review only; no new theorem is claimed by this record.

**Verdict: PASS** (INDEPENDENTLY-REVIEWED).

## Rebuild

Independently downloaded official Lean 4.19.0 (`6caaee842e94`). All eleven
sources extracted with `git show 42a165a:…` into an empty directory, compiled in
dependency order, all exit 0 (`rebuild.log`); Agent #11's `check.py` and objects
were not used. `ReviewAudit.lean` prints `#print axioms` for all 38 `theorem`
declarations of the five Agent #11 modules (`axiom_summary.txt`): only subsets of
`{propext, Classical.choice, Quot.sound}`, 4 with none; no `sorryAx`, no
`Lean.ofReduceBool`. Token scan: no `sorry/admit/native_decide/ofReduceBool/
implemented_by/extern/axiom/unsafe`. (The task record counts 40 theorem
declarations; the sources contain 38 `theorem` commands — audit metadata only.)

## Statement check (full names in `review_audit.log`)

* `ordinaryStep b ds = normalize b (pairs ds)` and `ordinary_step_canonical` /
  `digit_orbit_value` prove the output is a canonical base-`b` numeral
  (`DigitBounds`, `PositiveLast`) whose `eval` equals `eval ds + eval ds.reverse`,
  i.e. the ordinary reverse-and-add of the integer; iteration continues after a
  palindrome.
* `FirstPositivePalindrome b ds t`: `0 < t`, the time-`t` numeral is a list
  palindrome, and no earlier positive time is — the standard first positive hit;
  for canonical numerals list palindromes are integer palindromes.
* `numeric_interval_first_hit` (b ≥ 3, canonical input, every pair coefficient in
  `[b-1, b+(b-1)/2-1]`, exterior `≥ b`): hit at 1 iff every pair coefficient is
  `b+1`, hit at 2 iff not, and one of the two occurs; matches
  SEAM_PERSISTENCE_OBSTRUCTION eqs (1)–(3) and FIRST_HIT_CONTRACT.md with
  `h = floor((b-1)/2)` (nonnegative integer division). Time zero is excluded and no
  initial non-palindromicity is assumed, as stated.
* Observation: for `b = 3, 4` the interval upper bound `b+h-1` is below `b+1`, so
  the time-1 alternative is vacuous there and the theorem gives time 2.

## Independent integer control

`independent_control.py` (from the contract only): bases 3–16, 400 random qualifying
canonical numerals each (widths 1–12, odd and even), actual base-`b` reverse-and-add
with Python integers; first positive palindrome time equals the predicted 1/2 in
all 5,600 cases (`independent_control_result.json`).
