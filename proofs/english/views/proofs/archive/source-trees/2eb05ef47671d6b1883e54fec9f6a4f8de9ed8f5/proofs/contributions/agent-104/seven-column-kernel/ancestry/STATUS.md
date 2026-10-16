# ActualAncestry verification record

Accepted source: `ActualAncestry.lean` in the parent directory.

SHA-256：`3d7c904ae0abbd6e3eb132959a7a0fae230725a49808a05653206787d1a8149e`。

## Exact conclusions and remaining finite premises

`actual_iterPairs_rank` proves the following for an actual variable-width `iterPairs` orbit in the ordinary digit model:
if the tree lookup assigns rank `r` to the endpoint projection, the actual number of steps is at most `r`.
The projection is `wordPrefix q (min L 7)`; short words retain their complete length.
In the induction, each long-source edge uses the already-proved completeness theorem `actual_mem_prefixPredecessors`;
each short-source edge uses the exact exclusion condition covering all 10467 admissible short sources.

`short_target_unique` and `target_project_mem_initialWords` show that every projection of the target's last predecessor belongs to a finite family:
the complete six-column word `[7,3,9,9,3,7]`, together with all 10000 words `[7,3,9,a,b,c,d]`, whose four free digits range over 0–9.
This conclusion places no bound on the target length, internal digits, or length of a zero run.

`canonical_last_step_initial` uses the published `PalindromeBridge` to connect the last ordinary numerical step to this finite initial family.
`ancestry_bound39_of_finite_checks` then bounds actual ancestry depth from every positive integer source by 39.
`no_196_739_palindrome_of_finite_checks` combines this with the kernel-checked absence of palindromes at times 0–100 to exclude 739 palindromes from the ordinary 196 orbit at every time.

The last two results **still explicitly carry the following three finite-certificate premises**. This file does not treat those premises as completed instances:

1. `CheckedRows tree (longPred 7)`: every tree row checks the complete executable inverse enumeration.
2. `∀ s ∈ shortWords, lookup tree (nextWord s) = none`: the actual images of all admissible short sources lie outside the tree.
3. `∀ p ∈ targetInitialWords, checkInitial tree 38 p = true`: every initial projection has a stored rank at most 38.

The ancestry-depth bound itself is not assumed here; the composition from the finite checks to ordinary-integer conclusions has been proved.
This concerns only the 739-palindrome target family, not the full 196 conjecture.

## Author compilation

Lean 4.19.0; both `ancestry/long-rows-base.log` and `ancestry/attempt_002.log` record exit code 0.
`attempt_002.lean` is a complete snapshot of the accepted source.

```bash
LEAN_PATH=/workspace/scratch/7649db1e242c/build104-base:/workspace/scratch/7649db1e242c/build104-inverse:/workspace/scratch/7649db1e242c/build104-cert \
  /workspace/scratch/7649db1e242c/toolchain/lean \
  -o /workspace/scratch/7649db1e242c/build104-ancestry/LongRowsBase.olean \
  proofs/contributions/agent-104/seven-column-kernel/certificate/LongRowsBase.lean
LEAN_PATH=/workspace/scratch/7649db1e242c/build104-ancestry:/workspace/scratch/7649db1e242c/build104-base:/workspace/scratch/7649db1e242c/build104-inverse:/workspace/scratch/7649db1e242c/build104-projection:/workspace/scratch/7649db1e242c/build104-short:/workspace/scratch/7649db1e242c/build104-cert:/workspace/scratch/7649db1e242c/build104-palindrome \
  /workspace/scratch/7649db1e242c/toolchain/lean \
  -o /workspace/scratch/7649db1e242c/build104-ancestry/ActualAncestry.olean \
  proofs/contributions/agent-104/seven-column-kernel/ActualAncestry.lean
```

The six exported axiom audits contain only `propext`, `Classical.choice`, and `Quot.sound`.
There is no `sorryAx` or new axiom. The accepted source contains no `sorry`, `admit`, `axiom`, or `native_decide`.
The author used compiled outputs of the submodules. Another audit agent handles the independent clean build, with its result recorded separately.

`attempt_001.lean` and `attempt_001.log` preserve the first failure: constant indices and `min 6 7` were not explicitly reduced in the short-target uniqueness proof, so `omega`/`simp` did not close the goals.
The second draft passed after symmetry facts received explicit types such as `q 0 = q 2`, and the six-column target was rewritten as `segment q 0 6`.
The failed draft is not part of the accepted proof chain.
