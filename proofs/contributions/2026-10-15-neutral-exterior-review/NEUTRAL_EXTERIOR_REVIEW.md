# Independent review: neutral exterior and overflow

**Result: PASS.** The written all-base proof and its scope are sound.
This review inspected the producer note and checker, independently
audited its stored controls using ordinary integer evaluation, and
replayed the producer in a temporary directory. The original files were
preserved byte for byte.

## Mathematical and indexing checks

The first nonneutral index (j) exists because an all-neutral word
cannot generate a carry from initial carry zero. The neutral exterior
gives (j\ge1), and symmetry gives
(j\le\lfloor(M-1)/2\rfloor). If this first exceptional coefficient were
at most (b-2), its reflected occurrence at (M-1-j) would reset the
carry to zero; the remaining neutral suffix would preserve zero. Thus
overflow forces (p_j\ge b).

The low prefix has carry zero, hence (d_j=p_j-b\le b-2). The high
reflected occurrence forces outgoing carry one. Its following source
column is (M-j), which is neutral and emits zero. Crucially, this is
the reflection of (j) in the **actual output width (M+1)**. The
inequalities (1\le j\le\lfloor(M-1)/2\rfloor) ensure that (M-j<M), so
the partner is a real source column rather than the appended leading
digit. Therefore the claimed coefficient is exactly

\[
 R_j=d_j+d_{M-j}=p_j-b\le b-2.
\]

The argument remains valid when the exceptional index is an odd center:
its reflected occurrence is the same column, and the following column
is still the required neutral partner. No center-parity assumption is
used. Widths one and two have no nonneutral interior and cannot satisfy
the overflow premise. At base two, the conclusion is correctly a zero
pair coefficient.

For the stated two-step high-region consequence, the first updated
exterior lies in ([1,b-1]). A value at most (b-2) cannot generate a
final carry even with incoming carry one. If it is exactly (b-1), the
reviewed lemma excludes the overflow branch of a return to coefficients
all at least (b-1). The note correctly leaves possible nonoverflowing
returns untouched and asserts no infinite invariant.

## Independent finite audit

`independent_audit.py` reads the retained compressed table and verifies
its compressed and recovered hashes. It reconstructs each represented
integer by Horner evaluation and extracts its ordinary base-(b) digits
by division, without reproducing the producer's carry recursion. It
checks every output, actual width, overflow flag, reflected pair word,
and witness index.

All **22,773** unique inputs passed, including **11,355** overflow cases.
The input catalog counts agree independently for each base and length.
There are exactly 63 all-neutral controls, one for each of nine bases
and seven tested lengths; the relation
(2\cdot11,355+63=22,773) is also consistent with the low/high symmetry
of the first exceptional coefficient.

The producer was copied to a temporary directory and run there. Its
entire compressed archive and verification report were reproduced
exactly. `temporary_replay.log` retains that execution's output;
`independent_audit.json` pins the reviewed note, checker, archive, and
report hashes and records the original-file stability check.

The all-width result remains a written proof, supported by these finite
controls. This review makes no Lean-verification or external
peer-review claim.
