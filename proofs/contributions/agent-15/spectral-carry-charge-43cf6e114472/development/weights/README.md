# U/S weights: authored attempts and verification

Author: the genuine `coverage_scout` specialist, explicitly reassigned by Agent 15 after the successful U/S coordination claim `9ff01fb85383833abe440d7f41bc7c249c332070`. This specialist authored only `SpectralWeights.lean`. The parent owns the binary evaluator, full-word theorem and all Git publication. The runtime and ownership specialists remain nonauthors for independent review.

## Exact result

`SpectralWeights.lean` imports only `Std` and exports the literal integer recurrence

```
recurrence a b 0 = a
recurrence a b 1 = b
recurrence a b (n+2) = 20*recurrence a b (n+1) - recurrence a b n
```

It defines `U = recurrence 0 1`, `S = recurrence 1 21`, `oddWeight n = U (n+1)` and `evenWeight n = S n`. Each used weight is positive; each next weight is at least 19 times its predecessor; and each weight strictly exceeds the sum of all preceding used weights. The finite sum is exactly `weightSum w 0 = 0` and `weightSum w (n+1) = weightSum w n + w n`.

All declarations use namespace `P196.Agent15.SpectralCarry`. Public endpoint types are:

```
oddWeight_pos (n : Nat) : 0 < oddWeight n
evenWeight_pos (n : Nat) : 0 < evenWeight n
oddWeight_growth (n : Nat) : 19 * oddWeight n <= oddWeight (n+1)
evenWeight_growth (n : Nat) : 19 * evenWeight n <= evenWeight (n+1)
oddWeight_superincreasing (n : Nat) : weightSum oddWeight n < oddWeight n
evenWeight_superincreasing (n : Nat) : weightSum evenWeight n < evenWeight n
```

The source definition and equations retain all indices. The odd zero recurrence term U(0) is never a used weight. The smallest used weight is 1 in both parities; the next used weights are 20 and 21. These facts are kernel equations, not sampled controls. The module contains no T/R coordinate, binary-word injection theorem, H/J definition, carry normalization, non-nine lemma, orbit theorem or palindrome claim.

## Proof structure

A private induction propagates the conjunction `0 < w n` and `19*w n <= w(n+1)` for a sequence satisfying the displayed recurrence. The induction step applies the exact recurrence and linear integer arithmetic. A second induction uses positivity and this growth bound to show that the sum of all earlier weights is smaller than the current weight. The public theorems instantiate these inductions with the two exact source sequences.

The proof uses ordinary kernel-checked `omega` proof terms. No proof hole, admitted declaration, unchecked evaluator, compiler oracle or new mathematical axiom is introduced.

## Preserved attempts

| Directory | Result | Exact change or purpose |
| --- | --- | --- |
| `attempt-001` | Compilation failed. | The arithmetic tactic treated `w(n+1+1)` and `w(n+2)` as different atoms. The complete original source, exact command and full failure log are preserved. |
| `attempt-002` | Compilation succeeded, exit 0. | An explicit `change` puts the induction goal at indices `n+1` and `n+2` before the arithmetic tactic. No mathematical assumption changed. |
| `audit-001` | Fresh source build and full public export audit both succeeded, exit 0. | Copies the final module into its own directory, rebuilds it, then prints every explicitly public definition and theorem and their transitive axioms. |

Each attempt stores the exact source snapshot, command, source/compiler SHA256 identities, timestamps, exit status and complete substantive output. No failed source was overwritten. Generated local object files are build byproducts and are not the mathematical evidence dependency.

The compiler executable is `/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean`, SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Every build uses `--trust=0 -j1 -DElab.async=false`. The fresh audit's `LEAN_PATH` points only to its own build directory in addition to the compiler's standard library location.

## Author audit and remaining gate

The final source SHA256 is `07b3831f17a0d2e43a7e27cfd8a63d364a98ccbbcef87362a20cfbf24fb49db1`. `audit-001/public-exports.json` enumerates 29 explicitly public declarations. `audit-001/WeightsExports.lean` contains both `#print` and `#print axioms` for each; `WeightsExports.log` retains their complete output.

Twenty-three definitions/equation theorems use no axioms. The six positivity, growth and domination theorems use only `propext` and `Quot.sound`. No other axiom appears in those transitive public chains.

This establishes a complete, author-checked weights module. It does not replace the required nonauthor review, the separate audit of private and generated module-origin mathematical declarations, or the clean final build of the whole charge-symmetry package. Those are assigned to independent specialists. No final package acceptance is asserted by this record.

## Original mathematical provenance

The original notes have Git blob `cb1c355fa05916a770816a4d5ef680e54079cccb`; the original `creative_global_spectral.py` has blob `730acd722bf017b6bf1e51e5a0411169a7804da4`, both retained at source pin `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`. The script's `carry_coordinates` function gives the U/S initial values, recurrence and parity-specific weights. The notes state that the used J weights dominate the sum of smaller weights. Agent 15 supplies formalization of that retained claim, without changing its original provenance.
