# P196 — the 196 reverse-and-add problem

Repeatedly reverse the digits of 196 and add: 196 → 887 → 1675 → 7436 → … No palindrome has ever been found.
Whether one ever appears (whether 196 is a *Lychrel number*) is an open problem.
This repository holds two things:

1. **Verified mathematics** (`lean/`): 71 machine-checked Lean 4 results about reverse-and-add,
   each with an explicit scope. They narrow the problem; **none of them settles it**.
2. **Computation** (`calculation/`): the GPU engine that iterates the actual orbit of 196.

## Main results

About the orbit of 196 itself:

- **Thirteen palindrome prefixes are impossible.** If the orbit of 196 ever reaches a palindrome, that palindrome
  does not begin with 10, 20, 32, 40, 41, 60, 64, 65, 76, 80, 81, 82 or 83
  (`Agent113.TwoDigit.no_196_thirteen_arith`, in `lean/P196/Core`).
- **Prefix 2641 is impossible.** No palindrome in the orbit of 196 begins with 2641
  (`Agent124.Cert117P2641K7.no_196_2641`, in `lean/P196/Agent117P2641`).

About the method and the general problem:

- **Prefix 620 cannot be excluded the same way with a short bound.** An explicit seed reaches a palindrome beginning
  with 620 after exactly 12 steps, so any ancestry bound for that family is at least 12. This says nothing about
  whether 620 occurs in the orbit of 196 (`lean/P196/Agent104P620Witness`).
- **A certificate would give a Lychrel number.** Any return certificate that passes the checker yields a number
  whose orbit never contains a palindrome (`Agent112.Admissibility.certificate_existence_of_check`, in
  `lean/P196/CertificateToLychrel`). No such certificate is known, and it would not by itself be about 196.

Everything else (one reverse-and-add step, carries, periodic words, affine run words, finite models) is listed
in **[RESULTS.md](RESULTS.md)**, grouped by topic, each with its exact scope.

## Open problems

1. **The orbit of 196.** Show that no iterate is a palindrome. Proven so far: only the prefix families above are excluded.
2. **Existence of any decimal Lychrel number.** Reduced to producing one return certificate that passes the
   checker (see `CertificateToLychrel`); none is known.
3. **More prefix families.** Extend the exclusions (prefix 620 needs depth at least 12). Unregistered drafts for
   other prefixes are listed in [ARCHIVE.md](ARCHIVE.md).

## Verify everything

Requirements: [elan](https://github.com/leanprover/elan) (installs Lean 4.19.0 automatically) and Python 3.

```bash
python3 tools/verify.py
```

This checks the repository rules (no unregistered or duplicate Lean files, no `sorry`/`axiom`/`native_decide`),
builds all 406 modules with `lake build`, and audits the axioms of all 1884 registered endpoints.
It prints `ALL CHECKS PASSED` on success (about 30–60 minutes on a laptop the first time).

## Layout

| Path | What it is |
| --- | --- |
| `RESULTS.md` | Every verified result, grouped by topic, with its scope |
| `lean/registry.json` | Machine-readable list of results: modules, root modules, checked endpoints |
| `lean/P196/<Result>/` | Lean modules introduced by that result. A result may also import modules of other results; modules used by ten or more results are in `lean/P196/Foundations/`. A few results consist only of other results' modules, so they have no directory |
| `tools/verify.py` | One-command verification |
| `calculation/` | GPU engine releases and the browser engine page |
| `AGENTS.md` | Rules for people and agents who add work |
| `ARCHIVE.md` | Where the pre-cleanup history, branches, pull requests and unregistered drafts are kept |

## History

Before 17 October 2026 this repository had about 170 branches, 160 pull requests and 7,000+ Lean files, about half
of them byte-identical copies. Everything was consolidated into this single branch: each verified result appears
exactly once, and every old branch and pull request is preserved as a tag. See [ARCHIVE.md](ARCHIVE.md).

## 中文概要

本仓库研究 196 的“逆序相加”问题（196 是否为 Lychrel 数，至今未解决）。`lean/` 里是 71 个经 Lean 4
机器验证的结论，每个都有明确适用范围，**没有一个证明了 196 是 Lychrel 数**。关于 196 本身最强的结论：其轨道上若出现回文，
开头不可能是 13 个指定的两位数，也不可能是 2641。另有一条条件路线：只要找到一个通过检查器的“返回证书”，就能得到某个
Lychrel 数（不一定是 196），但目前还没有这样的证书。完整列表见 [RESULTS.md](RESULTS.md)，一条命令验证：
`python3 tools/verify.py`。旧的分支、PR 和历史都保存在 tag 里，见 [ARCHIVE.md](ARCHIVE.md)。
