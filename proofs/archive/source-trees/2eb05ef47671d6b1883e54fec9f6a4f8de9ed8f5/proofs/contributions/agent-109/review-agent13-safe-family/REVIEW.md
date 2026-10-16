# Agent #109 independent review of `agent13-safe-predecessor-family`

Reviewed source: branch `formalize/agent-13/s20261015`, commit
`8b1e5d15b94ea67bbb8a522b40ba6643c17ef5ee`,
`proofs/contributions/agent-13/safe-predecessor-family/{Family,TargetSafety,Counting}.lean`
with `proofs/research/continuation/LychrelDigitSums.lean` from the same commit
(hashes in `reviewed_sources.sha256`). Answers `proofs/coordination/agent13-review-request.json`.

Kind: replication/review only; no new theorem is claimed by this record.

**Verdict: PASS** (INDEPENDENTLY-REVIEWED).

## Rebuild

* Independently downloaded official Lean 4.19.0 (`6caaee842e94`, tarball
  SHA-256 `6fe3ce97…ba813fe`). Sources extracted with `git show 8b1e5d1:…` into
  an empty directory; Agent #13's `check.py` and objects were not used.
  `LychrelDigitSums → Family → TargetSafety → Counting` all exit 0
  (`rebuild.log`).
* `ReviewAudit.lean` prints `#print axioms` for all 36 theorem declarations:
  see `axiom_summary.txt` — only subsets of `{propext, Classical.choice,
  Quot.sound}`; no `sorryAx`, no `Lean.ofReduceBool`. Token scan of the three
  sources: no `sorry/admit/native_decide/ofReduceBool/implemented_by/extern/axiom/unsafe`.

## Statement check (full names printed in `review_audit.log`)

* `Safe n := 0 < n ∧ ¬Lychrel196.Palindrome n ∧ ¬Lychrel196.Palindrome (Lychrel196.step n)`
  — the accepted semantics; input and target safety are proved, not assumed.
* `safe_predecessor_family m (hm : 2 ≤ m)`: an injective
  `f : Fin (9*10^(m-2)) → Nat` with `Safe y_m`, and for every `i`:
  `Safe (f i)`, `Lychrel196.step (f i) = y_m`, `f i < 10^(2m) < y_m`, where
  `y_m = 10^(2m)+99·10^(m-1)-1`. This is exactly the CONTRACT (a lower bound on
  the fiber; no exact whole-fiber cardinality is asserted).
* `family` uses least-significant-first digits: positions `< k` hold
  `9 - a(k-1-i)`, positions `k,k+1` hold `9`, positions `≥ k+2` hold `a(i-k-2)`;
  as a decimal string this is `A || 99 || complement(reverse A)` with full
  width. `#eval` of Lean's `predecessor` (k=1 all nine; k=3 five samples)
  equals the strings built directly from the contract in Python.
* `predecessor_complete`: every high word with digits ≤ 9 and positive leading
  digit is some indexed `predecessor` — completeness of the indexing.
* `safe_fibers_unbounded N`: some safe `y` has `N` distinct safe
  predecessors, each `< y`.

## Independent integer control

`independent_control.py` (from CONTRACT.md only): for `m = 2..6` all
`9·10^(m-2)` canonical words `A` give distinct `n_A` of width `2m` with
`step n_A = y_m` and `n_A`, `y_m`, `step y_m` non-palindromic: PASS. Additional
observation (not part of the reviewed claim): for `m = 2,3,4` a brute-force
scan of all `n ≤ y_m` finds that the **complete** fiber of `y_m` has exactly
`9, 90, 900` elements, i.e. equals the constructed family there.
