# Agent #109 independent review of `agent13-folded-binary-family` (PR #32)

Reviewed source: branch `formalize/agent-13/s20261015-folded`, audit commit
`905b41efee894f550b19ca2d4e910970d4d9637e` (Lean sources identical to proof commit
`10aa1bc`; the two commits differ only in README/check.py):
`proofs/contributions/agent-13/folded-binary-family/{Trace,WholeWord,Safety,Indexing}.lean`
with `proofs/research/continuation/LychrelDigitSums.lean` from the same commit
(`reviewed_sources.sha256`).

Kind: replication/review only; no new theorem is claimed by this record.

**Verdict: PASS** (INDEPENDENTLY-REVIEWED).

## Rebuild

Independently downloaded official Lean 4.19.0 (`6caaee842e94`); sources extracted with
`git show 905b41e:…` into an empty directory; `LychrelDigitSums → Trace → WholeWord →
Safety → Indexing`, all exit 0 in 1m24s (`rebuild.log`), without Agent #13's
`check.py`, workflow or objects (the author recorded local clean-core timeouts at a
200 s container limit; this rebuild completed). `ReviewAudit.lean` audits all 41
theorem declarations (`axiom_summary.txt`): only subsets of `{propext,
Classical.choice, Quot.sound}`, 4 with none; no `sorryAx`, no `Lean.ofReduceBool`.
Token scan of the four sources: clean.

## Statement check (full names in `review_audit.log`)

* `inputHalf` is `H = (5, M_1, …, M_r, 14, 18^k)` with `M_i ∈ {(9,9,9,9), (14,14,4,4)}`
  (`blockDigit`), `targetHalf` is `R = (11, 9^(4r+1), 18^k)`, `halfWidth = 4r+k+2`;
  `reflectHalf` reflects to the full even width. Matches CONTRACT.md / FOLDED §1.
* `exact_binary_family r k (0<k)`: an injective `Fin (2^r)` indexing of the
  reflected words, safety (`WordSafe`: admissible and `value q L` not a
  `Lychrel196.Palindrome`) of the target and of every input, zero final carry,
  `FoldedDecimal.nextColumns` equal to the target on the full width, and a positive
  canonical decimal realization `n` with `Lychrel196.step n` realizing the target
  and `n`, `step n`, `step (step n)` all non-palindromic.
* `binary_family_actual_step` applies to **every** canonical realization;
  `binary_family_initial_nonpalindrome` / `target_initial_nonpalindrome` give the
  universal initial non-palindromicity; `indexed_word_complete` shows every binary
  choice is indexed. All `r ≥ 0` (including `r = 0`) and `k ≥ 1` are covered.
* The `2^r` count is for the constructed family, as stated; no infinite safe orbit
  or 196 claim.

## Independent integer control

`independent_control.py` (from the contract only): `r = 0..5`, `k = 1..5`, every
binary word, 3 random canonical realizations each (945 integers): next pair word
equals the reflected `R` with no overflow, `n`, `T(n)`, `T(T(n))` non-palindromic,
and exactly `2^r` distinct input words: PASS.
