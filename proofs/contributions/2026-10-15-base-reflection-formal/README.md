# Integer reflection bridge in every base at least three

This package closes the integer algebra and coefficient-uniqueness gap in
`../2026-10-14-general-base-seams/GENERAL_BASE_SEAMS.md`. It contains 58 new
Lean declarations in four modules, plus a fresh rebuild and axiom audit of the nine
prerequisite declarations in `SignedDigitUniqueness.lean`.

## Exact representation

A list `xs` consists of pairs `(q_i,c_i)` in least-significant-first order.
The first coordinate is the original symmetric pair coefficient; the
second is the isolated-block outgoing carry. For arbitrary integer base
`b` and initial carry `i`, `raw b i xs` constructs

- first coefficient `q_0+i-b*c_0`;
- later coefficients `q_j+c_(j-1)-b*c_j`;
- the terminal coefficient `c_(L-1)`.

It has length `L+1`. At a reset seam this is the raw placed sum, including
the previous block's terminal carry; it is not required to be a digit
list. In particular, `ColumnConditions` permits each isolated incoming
bit to reset independently rather than equaling the previous outgoing
bit. The dependent reset module computes these carries by actual integer division
and derives this representation from raw isolated placement, as described below.

`eval` is ordinary low-first integer evaluation. `high` is reversed
integer evaluation; the theorem `high_eq_reverse_eval` proves the
relationship to actual list reversal, rather than assuming it.

The two central identities are

\[
\operatorname{eval}_b(\mathrm{raw}(b,i,xs))
 =\operatorname{eval}_b(Q)+i,
\]

\[
\operatorname{high}_b(\mathrm{raw}(b,i,xs))
 =b\operatorname{high}_b(Q)+(1-b^2)\operatorname{high}_b(C)+i b^L.
\]

They hold for arbitrary integer coefficients and carries, including the
empty list. They eliminate reciprocal evaluation and division from the
formal reflection proof.

## Checked symmetry consequences

For the width `L+1` case, assume `Q.reverse=Q` and
`(raw b 0 xs).reverse=raw b 0 xs`. The identities give

\[
(b-1)\operatorname{high}_b(Q)
 =(b-1)(b+1)\operatorname{high}_b(C).
\]

Cancellation (for `b != 1`) yields zero reversed evaluation of the
residual list `q_i-(b+1)c_i`. Under `b>=3` and explicit local column
normalization conditions, the signed uniqueness theorem proves
`q_i=(b+1)c_i` at every column. Each original coefficient is therefore
zero or `b+1`. A positive outside coefficient necessarily falls in the
second case. The carry residual interval is derived from the local
column equations, not assumed in `overflow_classification`.

For the width `L` case, the caller supplies an actual length-L list `e`
by `raw b 0 xs = e ++ [0]`, and assumes `e.reverse=e`. This different
width is essential. The same identities imply
`(1-b*b)*high b C=0`; carry-bit nonnegativity and signed uniqueness then
force all carries to vanish. The package proves both `q_i<=b-1` and
`e=Q`.

The local hypotheses are: `0<=q_i<=2*b-2`, outgoing carry in `{0,1}`,
and existence of an isolated incoming bit in `{0,1}` and a digit in
`[0,b-1]` satisfying `q_i+incoming=digit+b*outgoing`.

These are the two raw-symmetry classification branches in
`BaseReflection.lean` (15 declarations). The next two modules establish
the actual reset-normalization and canonical-width interfaces.

## Computed isolated blocks and ordinary normalization

`ResetNormalization.lean` adds 16 declarations. A Boolean flag marks each
block start. Its `columns` recursion sets the incoming carry to zero at
flagged positions, then computes outgoing carry by `(q+incoming)/b`.
`carry_bit` and `columns_conditions` derive all previous hypotheses from
`0<=q<=2*b-2`; no residual bounds or realizability are assumed.

`placed` computes each isolated digit by remainder modulo `b`. At a reset
it adds the previous block's terminal carry to the new first digit,
without renormalizing that raw coefficient. It always includes the last
terminal carry slot. `placed_eq_raw` proves exact agreement with the
first module's representation, and `placed_eval` proves value preservation.

Every consecutive partition of a nonempty word is represented by setting
flags at its interior block starts. The first flag is immaterial because
initial carry is zero. Conversely, interior true flags split the word
into consecutive nonempty blocks. This is direct reset-stream semantics;
there is no separate formal nested-list/block-concatenation theorem.

`ordinary` uses the same division/remainder recursion with every reset
flag false. The two symmetry branches force equality with this actual
continuous-carry normalization. The proof shows that both classified
coefficient classes make all reset choices irrelevant.

## Canonical physical width and complete symmetry equivalence

`PhysicalWidth.lean` adds 21 declarations. It computes the final terminal
carry, proves it is a bit, and proves every reset normalization's terminal
carry is at most the ordinary terminal carry. Thus when the actual carry
is zero, the isolated raw sum also has a zero terminal slot; removing that
slot loses no coefficient. When the actual carry is one, its slot stays.

`atActualWidth` applies this exact width choice to raw placement;
`actualDigits` applies it to ordinary normalization. The checked theorem
`actual_width_symmetry_iff` proves symmetry of one iff symmetry of the
other, and `actual_width_symmetry_forces_equality` proves the lists equal
in either symmetric case.

The main theorem `canonical_raw_symmetry` additionally requires
`PositiveTerminal xs`, which is false for the empty list and requires
strict positivity of the highest input coefficient. It proves all of:

- every actual output digit lies in `[0,b-1]`;
- the actual output has a strictly positive final (leading) digit;
- its length is exactly `L+e`, where `e` is the computed actual carry bit;
- its evaluated integer equals the original coefficient-list value;
- raw symmetry at that actual width iff ordinary output palindromicity;
- in the symmetric case, raw output equals ordinary output.

Hence the width is canonical, not an arbitrary padded reflection width.
The core raw-symmetry theorem is now formalized in every base at least
three for arbitrary reset patterns. Remaining work outside this package
includes the separately defined seam polynomial/mass identity, an
interface to a project's ordinary seed/reversal representation if desired,
and any invariant through infinitely many iterations. There is no
infinite-orbit or Lychrel-existence claim.

## All-base outgoing-carry defect safety

`SeamSafety.lean` adds six declarations. For a fixed coefficient list and
incoming carry, equality of raw lists forces equality of their outgoing
carry lists whenever the base is nonzero. This is proved directly by
induction on the list and cancellation of multiplication by the base.

A palindromic actual output forces equality of the full raw placement and
ordinary normalization, including their terminal zero slots when there
is no overflow. Injectivity therefore forces every reset outgoing carry
to equal its corresponding actual outgoing carry. By contraposition,
**one unequal outgoing carry certifies a nonpalindromic actual output in
every base at least three**. The canonical wrapper includes the positive
terminal input condition and proves digit bounds, a positive leading
output digit, and numeric value alongside nonpalindromicity.

The index accessor uses the same zero default on both lists, so invalid
indices cannot manufacture a defect witness. This all-base carry-defect
criterion extends the external decimal obstruction. It does not assert
that the defect survives another step, and it does not require or claim
a formalized initial-run seam polynomial identity.

## Reproduce

From the repository root:

```sh
python proofs/contributions/2026-10-15-base-reflection-formal/check.py /path/to/lean
```

The checker requires Lean 4.19.0, builds all five exact source files in a
fresh temporary directory, audits all 67 declarations, permits only
`propext`, `Classical.choice`, and `Quot.sound`, and verifies that the
source hashes remain unchanged. `verification.json` records SHA-256 and
Git blob hashes; `compile.log` retains the complete audit. No previously
built local objects are used by this verification. Failed drafts are
retained separately as text and are not imported. Runtime binaries,
compiled objects and temporary copies are reproducible and excluded.
