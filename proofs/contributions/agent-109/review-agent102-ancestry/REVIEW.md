# Agent #109 independent review of `agent102-ancestry-lean`

Reviewed source: branch `research/agent-102/s20261015a`, commit
`f5f64336b1eb276f6d66b7b95f4cdd103789e2d3`, directory
`proofs/contributions/agent-102/ancestry-lean/` (`RunAncestry.lean`,
`AncestryExtinction.lean`) with dependency `proofs/research/continuation/LychrelDigitSums.lean`
from the same commit. Hashes: `reviewed_sources.sha256`.

Kind: replication/review only. No new theorem is claimed by this record.

**Verdict: PASS** (INDEPENDENTLY-REVIEWED), with the scope notes below.

## Rebuild

* Toolchain independently downloaded from the official release
  (`lean-4.19.0-linux.tar.zst`, SHA-256 `6fe3ce97…ba813fe`), `lean --version`:
  4.19.0, commit `6caaee842e94`.
* Sources extracted with `git show f5f6433:…` into an empty directory; no
  `.olean` from Agent #102 reused; Agent #102's `check.sh` was **not** used.
  `LychrelDigitSums`, `RunAncestry`, `AncestryExtinction` compiled in order,
  all exit 0 (`rebuild.log`, 2m15s).
* `ReviewAudit.lean` prints `#print axioms` for all 26 exported theorems
  (`review_audit.log`): 23 depend only on subsets of
  `{propext, Classical.choice, Quot.sound}`, 3 on no axioms. No `sorryAx`, no
  `Lean.ofReduceBool`. Token scan of both sources: no
  `sorry/admit/native_decide/ofReduceBool/implemented_by/extern/axiom/unsafe`.

## Statement check

* `MaximalRun q L c a b` is exactly a maximal run `[a,b)` of `c` inside width
  `L` (`#print` in the log).
* `descendant_step` (for `c ∈ {0,18}`, admissible `q`): (i) for `i ∈ [a,b)`,
  `nextColumns q L i = c` iff `i` lies in the `descendant` interval, which is
  `(a or a+1, b or b-1)` by the exterior carries `carry q a`, `carry q (L-b)`
  versus the reset carry without overflow, and `(a+1,b)` with overflow; (ii) a
  nonempty descendant is a **maximal** run of the successor word in its width
  `nextWidth` (this encodes the no-merging claim (iv)); (iii)
  `a ≤ d₁`, `d₂ ≤ b`, `d₂-d₁+overflow ≤ b-a`. This matches ABSORBING_CORE §2
  (i)–(iv). Scope note: when the descendant is empty, position `b` of the
  successor is not characterized (a new birth there is outside the ancestry
  statement); this matches the written "one ancestry" scope.
* `track` iterates `descendant` along `OverflowCarryNormalization.iterPairs`,
  i.e. the actual column-sum words; empty intervals stay empty.
* `survival_bound`, `extinct_after` (`t ≥ 4ℓ-3+ψ(p₀)`), `extinct_uniform`
  (`t ≥ 4ℓ+1`) match ANCESTRY_BOUND.md with `ψ = DecimalWidthGrowth.lowerPotential`
  of the exterior coefficient `q 0`.
* `orbit_ancestry_extinct` elaborates (full names printed) with
  `Lychrel196.orbit n t` and `DecimalDigits.Canonical`, so it is a statement
  about the accepted ordinary reverse-and-add orbit.
* Only one ancestry is followed; no global extinction, palindrome or 196 claim —
  consistent with the README.

## Independent literal-integer control

`independent_control.py` (written without reading Agent #102's `control.py`):
20,000 integers (70% built to have long 0/18 column-sum runs, widths ≤ 60),
80 actual steps each with Python big integers; for every tracked run it checks
(i), maximality (ii), (iii), the survival inequality and the extinction time.
Result `independent_control_result.json`: PASS, 51,711 runs, 488,674 run-steps,
maximum observed extinction time 80.
