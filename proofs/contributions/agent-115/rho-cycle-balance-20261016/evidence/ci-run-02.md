# Run 02: Core/Std lacks the required Rat arithmetic instances

- Commit: `9c1aa9fd5b7a9a15e80fbf319252d3ff26b800ec`.
- Action run: https://github.com/taco-jpg/p196-algorithm/actions/runs/38972513182
- Job `117214025398`, result **failure**.
- Lean4.19 official archive checksum PASSED; all nine original import modules PASSED from scratch with `--trust=0`.
- `RhoCycleTargets.lean` again failed, this time because the pinned dependency closure does not provide the `Nat -> Rat` coercion and ordered `HDiv Rat Rat` instances assumed by the written rational notation. The compiler explicitly reported `failed to synthesize HDiv Rat Rat` and `HMul Nat Nat Rat`.
- This is a **representation/formalization failure**, not a counterexample to the external mathematical identity. Run logs and Actions artifact `12076892805` are retained.
- Correction: define exact numerator and positive denominator in `Nat` and express the recurrence as a *cross-multiplied polynomial equality*. This is equivalent to the rational identity; it needs the same original high-side update and suffix-padding proof, but no unavailable Rat typeclass instances.
- `RhoCycleLemmas.lean` was not reached in run02. No theorem accepted from that failed CI.
