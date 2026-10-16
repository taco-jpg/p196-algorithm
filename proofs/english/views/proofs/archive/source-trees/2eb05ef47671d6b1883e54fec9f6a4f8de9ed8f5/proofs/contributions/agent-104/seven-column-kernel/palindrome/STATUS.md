# PalindromeBridge verification record

This directory belongs to agent #104's last-step bridge subtask. The accepted source is
`PalindromeBridge.lean` in the parent directory, in namespace `SevenColumnKernel.PalindromeBridge`.

## Proved results

- `canonical_unique`: canonical representations of the same ordinary positive integer have equal width and agree digit by digit.
- `no_overflow_of_target_leading_gt_one`: if the target's leading digit is greater than 1, the last step does not overflow; no palindrome assumption is needed yet.
- `canonical_last_step`: with the target-palindrome assumption, source and target have equal width, all actual carries are 0, the source's complete symmetric column sums equal the target's complete digits entry by entry, and every entry is at most 9.
- `numeric_last_step`: these conclusions apply to every positive integer predecessor, without requiring the caller to supply its digit representation first.
- `predecessor_of_739_palindrome`: the column sums of a positive integer predecessor of a 739 palindrome start with 7, 3, 9 from the low end, retaining the complete digit equality and no-carry conclusions.
- `no_196_target_of_ancestry_bound`: if the ancestry depths from all positive integers to a palindrome target family are uniformly at most `B ≤ 100`, the ordinary 196 orbit never enters that family.
- `no_196_739_palindrome_of_ancestry_bound39`: specialize the preceding result to 739 palindromes and bound 39.

The final two results are **explicit conditional theorems**. The uniform 39-step ancestry bound is a parameter, not an axiom or a result established by this file. This file does not prove the full 196 conjecture.

## Compilation and axiom audit

Lean 4.19.0 is used, directly importing the repository's existing `LychrelDigitSums.lean`.

```bash
mkdir -p /workspace/scratch/7649db1e242c/build104-palindrome
/workspace/scratch/7649db1e242c/toolchain/lean \
  -o /workspace/scratch/7649db1e242c/build104-palindrome/LychrelDigitSums.olean \
  proofs/research/continuation/LychrelDigitSums.lean
LEAN_PATH=/workspace/scratch/7649db1e242c/build104-palindrome \
  /workspace/scratch/7649db1e242c/toolchain/lean \
  -o /workspace/scratch/7649db1e242c/build104-palindrome/PalindromeBridge.olean \
  proofs/contributions/agent-104/seven-column-kernel/PalindromeBridge.lean
```

The core build exited with code 0; its log is `base-build.log`. The accepted-version build exited with code 0; its log is
`attempt_002.log`. All seven exported theorems were queried with `#print axioms`, yielding only
`propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx` or additional axioms.
The accepted source contains no `sorry`, `admit`, `axiom`, or `native_decide`.

`attempt_001.lean` / `attempt_001.log` preserve the first failure: `subst W` chose a different width equality first, making subsequent fixed-width injectivity arguments mismatch. The accepted version clears two intermediate length equalities before substituting along `L = W`. The failed draft is not part of the accepted proof chain.

SHA-256：

```text
LychrelDigitSums.lean
ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57

PalindromeBridge.lean
6c1de8cf02ec9381e80388e6b4915db6cfa4d1189d3e47c273400f0d37948093
```
