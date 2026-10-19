# P196 — the 196 reverse-and-add problem

Repeatedly reverse the digits of 196 and add: 196 → 887 → 1675 → 7436 → … No palindrome has ever been found.
Whether one ever appears (whether 196 is a *Lychrel number*) is an open problem.
This repository holds two things:

1. **Verified mathematics** (`lean/`): 114 machine-checked Lean 4 results about reverse-and-add,
   each with an explicit scope, plus 139 groups of unreviewed draft results. They narrow the problem; **none of them settles it**.
2. **Computation** (`calculation/`): the GPU engine that iterates the actual orbit of 196.

## Main results

About the orbit of 196 itself — palindrome prefixes that can never occur:

- **Thirteen two-digit prefixes:** 10, 20, 32, 40, 41, 60, 64, 65, 76, 80, 81, 82, 83
  (`Agent113.TwoDigit.no_196_thirteen_arith`, `lean/P196/Core`).
- **Three-digit prefixes 217, 218, 620, 739, 777** (`lean/P196/Agent118PrefixKernel`, `lean/P196/Agent124Prefix620`,
  `lean/P196/Agent104Prefix739`),
  and **33 further three-digit prefix classes** (`lean/P196/Agent124PrefixFiveSix`).
- **Longer prefixes:** 2641 (`lean/P196/Agent117P2641`), the longer-prefix refinement lists
  (`lean/P196/Agent124FourDigit`), and an explicit list of **277 digit prefixes** (`lean/P196/Agent124ForwardInvariant`).
- **A five-layer digit pattern** never occurs in the orbit of 196 (`lean/P196/Agent113FiveLayer`).
- **Eight palindrome families** dd 0…0 dd (d = 1, 2, 3, 4, 6, 7, 8, 9) never occur (`lean/P196/Agent119EightFamilies`).

Other facts about the orbit of 196:

- No iterate is divisible by 3 (or 9, or 99); from time 3 on every iterate is divisible by 11
  (`lean/P196/Agent315Orbit196Residues`, `lean/P196/Agent119EightFamilies`).
- **The first 101 iterates (times 0–100) are not palindromes** (`lean/P196/Orbit196Basics`).
- **The digit sum grows:** it exceeds any bound B within an explicit window of steps, from any starting time
  (`lean/P196/Orbit196Basics`, `lean/P196/Agent9DigitSumWindows`).

Altogether **321 of the 900 three-digit prefixes** are excluded, plus
1731 four-digit prefixes under the others; [RESULTS.md](RESULTS.md) has them in one combined table.

Each exclusion works the same way: every positive seed that reaches a palindrome with that prefix does so within a
few dozen steps, and the first 100 steps of 196 contain no palindrome.

Where this method stops:

- **14 three-digit prefixes cannot be handled this way** (112, 138, 164, 198, 248, 275, 398, 626, 710, 716, 790,
  911, 936, 952): the finite backward abstraction has a cycle for each (`lean/P196/Agent117RemainingCycles`).
  The bound for 620 is sharp at 12 steps (`lean/P196/Agent104P620Witness`).

About the general problem:

- **A certificate would give a Lychrel number.** Any return certificate that passes the checker yields a number
  whose orbit never contains a palindrome (`Agent112.Admissibility.certificate_existence_of_check`, in
  `lean/P196/CertificateToLychrel`). No such certificate is known, and it would not by itself be about 196.

Eleven of these results (Agent118PrefixKernel, Agent124Prefix620, Agent104Prefix739, Agent124PrefixFiveSix,
Agent124FourDigit, Agent124ForwardInvariant, Agent119EightFamilies, Agent113FiveLayer, Agent117RemainingCycles,
Agent315Orbit196Residues, Agent9DigitSumWindows) were unregistered drafts on old branches;
during the consolidation they were compiled and their axioms audited like everything else here, but nobody has
reviewed them independently yet.

Everything else (one reverse-and-add step, carries, periodic words, affine run words, finite models) is listed
in **[RESULTS.md](RESULTS.md)**, grouped by topic, each with its exact scope.

## Open problems

1. **The orbit of 196.** Show that no iterate is a palindrome. Proven so far: palindromes with the prefixes above
   never occur; every other prefix remains open.
2. **The 14 prefixes where the method stops** (see above) need a different argument.
3. **Existence of any decimal Lychrel number.** Reduced to producing one return certificate that passes the
   checker (see `CertificateToLychrel`); none is known.
4. **Other drafts.** Smaller unregistered drafts that compile are listed in [ARCHIVE.md](ARCHIVE.md).

## Verify everything

Requirements: [elan](https://github.com/leanprover/elan) (installs Lean 4.19.0 automatically) and Python 3.

```bash
python3 tools/verify.py
```

This checks the repository rules (no unregistered or duplicate Lean files, no `sorry`/`axiom`/`native_decide`),
builds all 4619 modules with `lake build`, and audits the axioms of all 5745 registered endpoints.
It prints `ALL CHECKS PASSED` on success (about 30–60 minutes on a laptop the first time).

To check only your own new or changed files (what contributors run before pushing; minutes instead of hours):

```bash
python3 tools/verify.py --changed
```

## Layout

| Path | What it is |
| --- | --- |
| `RESULTS.md` | Every verified result, grouped by topic, with its scope |
| `lean/registry.json` | Machine-readable list of results: modules, root modules, checked endpoints |
| `lean/P196/Drafts/` | Unreviewed draft results from the old branches (each file proves something found nowhere else) |
| `lean/P196/<Result>/` | Lean modules introduced by that result. A result may also import modules of other results; modules used by ten or more results are in `lean/P196/Foundations/`. A few results consist only of other results' modules, so they have no directory |
| `tools/verify.py` | One-command verification |
| `calculation/` | GPU engine releases and the browser engine page |
| `AGENTS.md` | Rules for people and agents who add work |
| `ARCHIVE.md` | Where the pre-cleanup history, branches, pull requests and unregistered drafts are kept |

## History

Before 17 October 2026 this repository had about 170 branches, 160 pull requests and 7,000+ Lean files, about half
of them byte-identical copies. Everything was consolidated into this single branch: each verified result appears
exactly once, and every old branch and pull request is preserved inside one of 60 archive tags. See [ARCHIVE.md](ARCHIVE.md).

## 中文概要

本仓库研究 196 的“逆序相加”问题（196 是否为 Lychrel 数，至今未解决）。`lean/` 里是 114 个经 Lean 4
机器验证的结论（另有 139 组未经审阅的草稿结论），每个都有明确适用范围，**没有一个证明了 196 是 Lychrel 数**。关于 196 本身：其轨道上若出现回文，
开头不可能是 13 个指定的两位数、217、218、620、739、777、另外 33 个三位数前缀类、2641，以及一份 277 个前缀的清单；
八类 dd0…0dd 回文也不会出现；
另有 14 个三位数前缀已证明这种方法处理不了。另有一条条件路线：只要找到一个通过检查器的“返回证书”，就能得到某个
Lychrel 数（不一定是 196），但目前还没有这样的证书。完整列表见 [RESULTS.md](RESULTS.md)，一条命令验证：
`python3 tools/verify.py`。旧的分支、PR 和历史都保存在 60 个存档 tag 里，见 [ARCHIVE.md](ARCHIVE.md)。
