# Independent review of Agent #106 run-birth modules

Task `agent103-review-agent106-births`. Replication/review only: **no new theorem**.

## Pinned inputs

| File (at source commit `8aa86f52e49cd1939125e53c3ddfc9f9215f82cd`) | SHA-256 |
|---|---|
| `proofs/contributions/agent-106/run-births/NoOverflowBirths.lean` | `27a95daf58e8685297094dba5c7d64eea4f01632550a9f8fc04482c066fb8638` |
| `proofs/contributions/agent-106/run-births/BaseBirths.lean` | `55d5db9e8ea7a67e7ec3b8eaf2991abf4b8d5f9d9c2a63e629a41857f7a603a0` |
| `proofs/research/continuation/LychrelDigitSums.lean` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` (project-pinned base) |

Compiler: official `lean-4.19.0-linux.tar.zst` from the leanprover/lean4 GitHub
release, SHA-256 `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`,
`Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)`.
Not the Actions artifact, and not Agent #106's `check.py`: an independent
toolchain download and hand-written commands.

## Rebuild (empty directory, `LEAN_PATH` = that directory only)

`lean -j1 -DElab.async=false -o M.olean M.lean` in dependency order:

| Module | Exit | Wall time |
|---|---|---|
| LychrelDigitSums | 0 | 86 s |
| NoOverflowBirths | 0 | 5 s |
| BaseBirths | 0 | 12 s (one unused-variable linter warning) |

Logs: `*.build.log` in this directory.

## Axiom audit

`AuditAll.lean` (generated here, retained) prints axioms for **all 21**
non-private top-level `theorem`/`def` declarations in both modules (private
helpers are covered transitively). Exit 0. Result: 17 use
`[propext, Classical.choice, Quot.sound]`, 2 use `[propext, Quot.sound]`, 2 use
none. No `sorryAx`, `Lean.ofReduceBool`, custom axiom, `native_decide`,
`implemented_by`, `extern` or `unsafe` in either source (text scan). Log:
`AuditAll.log`.

## Statement check

`nextColumns q L i` with `carry q L = 0` is, by definition in the base file,
`columnSum (output q) L i = (q i + carry q i)%10 + (q(L-1-i) + carry q (L-1-i))%10`,
and `Admissible` gives `q i = q (L-1-i)` and coefficients `<= 18`. Hence the
Lean carries `carry q i`, `carry q (L-1-i)` are exactly `a_i`, `beta_(i+1)` of
`ABSORBING_CORE.md` section 4, and `next_eighteen_iff_sum` /
`next_zero_iff_sum` state precisely its two unrestricted one-column
equivalences under the no-overflow hypothesis. The `_bits`, `fresh_*`,
emission and center corollaries are correct specializations (fresh = old
coefficient differs from the target; at a self-mirrored center the two
carries coincide, so the 9 branch is excluded by center parity).
`BaseBirths` states local base-`b` analogues over `Int` for the expression
`(x+a)%b + (x+c)%b`; its own docstring correctly notes it is not an overflow
transition formula.

Scope limits confirmed: all results are one-step/no-overflow (or purely
local). Nothing asserts run persistence, ancestry, the overflow birth case,
the all-`g` birth family, global extinction, an infinite safe orbit, or P196.

## Verdict

INDEPENDENTLY-REVIEWED (clean rebuild + axiom audit + statement check) for
these two modules at the pinned commit. Not INTEGRATED by this review.
