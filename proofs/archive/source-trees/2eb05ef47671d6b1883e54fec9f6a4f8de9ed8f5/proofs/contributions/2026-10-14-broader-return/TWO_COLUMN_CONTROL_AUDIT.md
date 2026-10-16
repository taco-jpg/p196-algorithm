# Exact controls and safety for the broader `(4,4)` return

The complete two-column control classification passes an independent
literal-integer audit. There are 16 returning binary control words and
three distinct prefix traces. Their control sets are

\[
00*0*11,\qquad 10*0*11,\qquad 10*1*0*.
\tag{1}
\]

The last pattern contains eight words; each of the first two contains
four. Thus assuming the single first trace would omit twelve returning
control words and two prefix branches.

## Actual-word interpretation

Let `Q0` be an admissible symmetric pair word of width at least two
whose first two coefficients are `(4,4)`. Let `Qt=G^t(Q0)` and define
the actual high-side two-column input

\[
c_t=\operatorname{carry}(Q_t,|Q_t|-2),\qquad 0\le t<7.
\]

Then `Q7` begins with `(4,4)` if and only if

\[
c_1=0\quad\text{and}\quad
\bigl[(c_3=0\land c_5=1\land c_6=1)
\ \lor\ (c_0=1\land c_3=1\land c_5=0)\bigr].
\tag{2}
\]

Positions 2 and 4 are free. Every one of the 128 possible input histories,
including those that fail to return, has whole overflow schedule
`(0,0,1,0,1,0,1)`. A successful return therefore increases width by three.

To justify the interpretation, normalize the low two coefficients with
incoming zero and the reversed high two coefficients with their actual
incoming carry `c`. If the latter has final carry zero, add the retained
digits at corresponding reflected positions. If it has final carry one,
the leading digit is one and the reflected high digits shift one place.
This is the actual two-column projection; it does not independently
assign any carry to the whole word. At width two or three the low and
high observations overlap, but both describe the same actual digits and
carries. The overlap restricts which input bits can occur; every actual
bit is still among the two retained choices. At width two the high-side
input is zero. Hence the projection and the sevenfold classification
remain valid, giving (1)--(2) throughout the stated domain.

The returning traces are:

| Phase | `00*0*11` | `10*0*11` | `10*1*0*` |
|---:|---|---|---|
| 0 | `(4,4)` | `(4,4)` | `(4,4)` |
| 1 | `(8,8)` | `(8,9)` | `(8,9)` |
| 2 | `(16,16)` | `(16,18)` | `(16,18)` |
| 3 | `(7,14)` | `(7,16)` | `(7,16)` |
| 4 | `(15,8)` | `(15,12)` | `(15,13)` |
| 5 | `(6,14)` | `(6,9)` | `(6,10)` |
| 6 | `(13,9)` | `(13,9)` | `(13,0)` |
| 7 | `(4,4)` | `(4,4)` | `(4,4)` |

A necessary graph for repeated returns must permit switching among these
three traces at the common phase-zero state. The classification does not
assert that any freely chosen sequence of their controls is realized by
one ordinary integer orbit.

## Exact safety condition for one actual return

Under (2), all seven positive ordinary successors are nonpalindromic if
and only if **both `Q0` and `Q1` contain a coefficient at least 10**.

At phases 0 and 1, the outside coefficients are respectively 4 and 8,
so the full normalization has no final overflow. The established
no-overflow palindrome criterion says that an admissible symmetric pair
word normalizes to a palindrome exactly when every coefficient is at
most 9. These are precisely the two tests stated above.

At phases 2, 4, and 6, the outside coefficients are 16, 15, and 13. The
least normalized digits are 6, 5, and 3, while the final leading digit
is 1, so all three outputs are nonpalindromic. At phase 3, the second
coefficient is either 14 or 16, producing a carry, while outside 7
prevents final overflow. At phase 5 the first and third branches visibly
contain 14 and 10. The second branch has prefix `(6,9)`, but its required
actual input is `c5=1`; therefore the earlier columns produced a carry,
which is impossible if all coefficients were at most 9. In every branch
outside 6 prevents final overflow, so that phase is also nonpalindromic.
This proves both directions of the safety condition without a middle
width bound or an assumed repeating branch.

## Independent arithmetic controls

`independent_two_column_audit.py` imports no producer code. At each of
the 896 individual transitions in the 128 histories, it normalizes the
ordinary coefficient integer for

\[
p\,(18c)\,p^R.
\]

The even middle coefficient forces carry `c` into the high prefix,
independently of its own incoming carry. Extracting ordinary decimal
digits and reflecting them independently reproduces every prefix and
overflow in `two_column_controls.json`. The checker also tests (2) for
all 128 histories and verifies that exactly the three displayed traces
return.

All literal words, normalized digits, returned prefixes, overflows,
and producer hashes are retained in `independent_two_column_audit.json`.
These are local one-step realizations used to audit the transducer, not
a claim that the 896 independently constructed words join into actual
trajectories. Run:

```sh
python -B proofs/contributions/2026-10-14-broader-return/independent_two_column_audit.py
```
