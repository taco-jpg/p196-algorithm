# UnboundedBirths development record

Frozen source: `../../UnboundedBirths.lean`.
Namespace: `RunBirths.UnboundedBirths`.
SHA-256: `2b1d22d74db73da5ef93cdd8f559d859a6d0a066d5df777c01234c59af458666`.

## Mathematical statement

For all natural k,r, the even-width source

`(1,9^k,1,10,9^(2r),10,1,9^k,1)`

has width `2k+2r+6`, is `Admissible`, and contains neither 0 nor 18. Its
actual recursive decimal carry is 1 exactly on the incoming-carry interval
`[k+3,k+2r+4]`, and is 0 elsewhere. In particular the actual terminal carry
is 0. The exact actual `nextColumns` successor at unchanged width is

`(2,18^k,3,1,0^(2r),1,3,18^k,2)`.

The target's 0 positions are exactly `[k+3,k+2r+3)` and its 18 positions
are exactly `[1,k+1)` and `[k+2r+5,2k+2r+5)`. All these coefficients come
from source 9s. The formulas include empty bands (k=0 and/or r=0), while
k,r>=1 exhibits simultaneous nonempty births of both kinds.

`numeric_family_realized` provides an actual positive integer n and
canonical digit realizations of n and step(n), with full-width column sums
equal to the source and target respectively. Thus the parameter family is
not a freely chosen pair of local carry bits.

`arbitrarily_long_birth_bands(B)` supplies an admissible source with no
extreme coefficient at all and one actual step containing simultaneously
B+1 consecutive new zeros and B+1 consecutive new 18s. This remains a
single-step assertion; it does not prove recurrence, orbit closure,
infinite safety, or occurrence on the orbit of 196.

## Existing related results checked

The existing `SeamAnnihilation.lean` family `(10,9^k,10)` has an actual
overflow and produces a long zero region. It does not state this combined
no-overflow family with simultaneous arbitrary 0 and 18 births. The
existing `RegenerationGate` modules supply the explicit column-balance /
carry-induction proof technique. A targeted Lean/Markdown search for an
already named unbounded-birth or same-source-family theorem returned no
matches (`prior_search.log`); this is a repository-scope check, not a
mathematical novelty claim.

## Verification evidence

- `finite_controls_positive.py/json/log`: 576 cases k,r=1..24; exact source
  and target coefficients, recursive carries, canonical realization, and
  direct integer n+reverse(n) were checked.
- `finite_controls.py/json/log`: expanded 625 cases k,r=0..24, additionally
  covering every empty-band boundary. All checks pass. Each finite control
  checks the exact zero/18 counts as well, although the universal count
  theorem is developed separately in `PopulationGrowth.lean`.
- `attempt_001.lean/log`: the initial 20-theorem module compiled on its
  first attempt, exit 0, no warnings.
- `attempt_002.lean/log`: the frozen 22-theorem module, including explicit
  numeric and arbitrary-size wrappers, compiled exit 0, no warnings.
- All 22 exported theorem declarations have `#print axioms`. The output
  contains only `propext`, `Classical.choice`, and `Quot.sound`; there is no
  `sorryAx`, custom axiom, or native-decision proof.

The Lean module imports only `LychrelDigitSums`. Compilation used Lean
4.19.0, `LD_PRELOAD=/workspace/scratch/50e90e07524e/runtime/readlink_self.so`,
and `LEAN_PATH=/workspace/scratch/50e90e07524e/build106`.

Independent reviewer: `/root/base_generalization`; its fresh-source
rebuild and independent 67-case integer checks are recorded separately
under `review/base-reviewer`.
