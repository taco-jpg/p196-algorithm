# Run 01: genuine Lean compilation failed; source-only corrected

- Pinned push commit: `926e040adc3421039b1cfeb094d72794dfb482b1`.
- GitHub Actions run: https://github.com/taco-jpg/p196-algorithm/actions/runs/38972165580
- Job: `probe`, id `117212890665`, completed **failure**.
- Official Lean 4.19.0 release downloaded and checksum matched `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.
- Nine pinned original import modules passed from scratch with `lean --trust=0` (all exit 0).
- `RhoCycleTargets.lean` failed (exit 1): lines 19,20,28,29 used Lean type annotations `((n : Nat) : Rat)` that are *not* coercions; actual Nat expressions were rejected where Rat was required.
- `RhoCycleLemmas.lean` was **not compiled in this run** because the workflow correctly stopped at the failing dependency.
- Original failure and full logs remain in the Actions run artifact `12077830345`; no acceptance was claimed. Corrective attempt replaces those expressions with explicit `(↑(n) : Rat)` in the target and proof module. This record is retained after correction.
