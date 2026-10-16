# Agent #119: four-column three-digit prefix kernel (WIP)

Task `agent119-four-column-prefix-kernel` (claimed on `p196/coordination` at `b2c4da7`).
Contribution branch `research/agent-119/s20261015T1555`, base `main` `eec3d5f`.

**Status: WIP.** The structural modules below compile with official Lean 4.19.0
(`6caaee842e94`); their theorems are *conditional* on explicit finite certificate
checks that are not yet supplied. No prefix ancestry bound and no statement about
the orbit of 196 is claimed yet. Nothing here addresses the full P196 question.

Target (see the task record for the full 229-entry table): for each listed
three-digit prefix `abc` with bound `B`, every positive ordinary decimal `A`,
time `t` and palindrome `P` whose canonical numeral begins `a,b,c`:
`Lychrel196.orbit A t = P → t ≤ B`; hence `orbit 196 t` is never such a palindrome.
Source: written proof and Python certificate in
`proofs/chat-6acee928/originals/p196_four_column_obstruction.md` §4–6 (no Lean).

## Modules

| File | Content | Status |
|---|---|---|
| `FourColumnAncestry.lean` | `project4` (first `min L 4` pair sums), exact short words of widths 1–3, decidable short-descent check, `actual_iterPairs_rank4` | compiles; conditional |
| `ThreeDigitBridge.lean` | `Starts3`/`PalindromeStarts3`, `GrowthPrefix` (110/111/121/122), `overflow_palindrome_prefix` (covers leading digit 1), `canonical_last_step3`, `rootWords`, `last_step_root`, conditional endpoints `ancestry_bound_of_checks`, `no_196_of_checks` | compiles; conditional |

Reused unchanged (Agent #104, integrated): `PrefixInverse`, `FastInverse`,
`ActualPrefix`, `ShortBoundary`, `PrefixCertificate`, `PalindromeBridge`,
`certificate/LongRowsBase`, `certificate/FastRowsBase`; base
`proofs/research/continuation/LychrelDigitSums.lean`
(SHA256 `ca5f4652…0b57`).

The descending-prefix lemma used in the written source for the first inverse
step is **not** used: for all 229 classes the unrestricted inverse gives the same
bounds (exploratory Python; to be confirmed by the kernel certificate).
