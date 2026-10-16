# Independent review: digit-splitting multiplicity bounds

## Scope and verdict

**PASS for the exact definitions and ten theorem statements in
`Agent101MultiplicityBounds.lean`.** The reviewer did not author this
module. The reviewer did author its unchanged `Agent101DigitPairs` dependency;
that dependency was rebuilt from source in this review, but its semantic
review is not represented as independent.

Reviewed bounds SHA256:
`8fd487ce8025cfe7cbda3dc51b6a02595c856fbe3dd065a8781cea60b7e6b5c3`.

Dependency SHA256:
`5c76eae97efd2f30d1775650f7feca477c269419af1c02809800a95ca62821f8`.

Both files were copied byte-for-byte into the previously nonexistent build
directory recorded in `bounds-review.json`. No author project objects were
reused. Both modules compiled under official Lean 4.19.0, commit
`6caaee842e94`, with `-j1 -DElab.async=false`. A subsequent `--trust=0`
import audited all 26 public definitions/theorems in the two modules.
All commands exited zero. The axiom union is only `propext`,
`Classical.choice`, and `Quot.sound`.

## Semantic checks

1. An ordinary digit pair has low/high digits in `0..9`. Its count is
   `s+1` for `0 <= s <= 9`, `19-s` for `10 <= s <= 18`, and zero above
   eighteen. Its maximum is ten, achieved at sum nine.
2. The outer pair additionally has high digit greater than zero. Its
   count is `s` for `0 <= s <= 9`, `19-s` for `10 <= s <= 18`, and zero
   above eighteen. This removes exactly the split with high digit zero
   when that split exists. Its maximum is nine, achieved at sums nine
   and ten. The `s=0` case is correctly zero.
3. `centerCount none = 1` is the empty interior choice, not a positive
   zero-digit numeral. For a present center, the count is one exactly
   when its sum is at most eighteen and even. A zero interior digit is
   permitted when there is an outer pair.
4. `profileCount [] none = 0` rejects the empty positive numeral.
   `profileCount [] (some s)` also requires `0 < s`, so one-digit
   numerals are counted exactly for `s` in `{2,4,...,18}`. Each has the
   unique positive digit `s/2`. Thus `s=0`, odd centers, and centers
   above eighteen do not create spurious one-digit numerals.
5. For a nonempty half-profile `s :: h`, its declared count is the
   product of the outer-pair count, the center indicator, and the
   ordinary-pair counts for `h`. Every factor is nonnegative. The three
   bounds therefore give `profileCount (s :: h) c <= 9 * 10^h.length`.
6. The bound is sharp for every number of inner pairs: outer sum nine
   or ten, all inner sums nine, and any center with count one attain
   `9 * 10^h.length`. The final theorem explicitly exhibits both the
   even-width case (`none`) and the odd-width case (`some 0`).

There is no missing leading-digit or center-parity hypothesis in these
claims. The multiplication proof and the two exact maximum constructions
match the stated profile representation.

## Limits

This module proves a sharp bound for `profileCount`. On its own, it does
not prove that `profileCount` counts all ordinary-number preimages of
reverse-and-add. That interpretation requires the separately developed
enumeration completeness, no-duplicates, numerical-value injection, and
same-width numerical-fiber bridges. No independent build of those changing
modules is claimed by this report.

No source was changed by this review. The fresh source snapshots, command
records, individual logs, imported-object audit, and hashes are the other
`bounds-review.*` files in this directory.
