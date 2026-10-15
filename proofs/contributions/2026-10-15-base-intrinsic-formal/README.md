# Intrinsic outgoing-carry defects in every base

This package extends the other proof stream's decimal result to arbitrary
integer bases. The prior result is `IntrinsicSeam.lean` at commit
`e52125515490b668d14e95b0cf8d31767bcde7c4`, under
`proofs/research/main_existence_attempt/continuation_pass/lean/`.
Its exact source SHA-256 is
`de764dffc4d72b3060c3648339116adc4cfeb3d425a2edd5ef4e42056ec36b20`.
Singleton maximality and the decimal high/9 characterization are prior
results, not claimed as new here. The new contribution is a formal
variable-base extension and its connection to the all-base canonical
ordinary reverse-and-add interface.

There are 27 new declarations (10 carry, 15 pattern, 2 ordinary-output)
and 82 prerequisite declarations. Fresh Lean 4.19.0 compilation and axiom
audit pass all 109 declarations.

## Exact characterization

Fix any base `b>=2` and any finite coefficient word with
`0<=q_i<=2*b-2`. A *high* coefficient is at least `b`; the *neutral*
coefficient is `b-1`. Coefficients are ordered least significant first.
No symmetry or positive-terminal hypothesis is needed for this part.

For an incoming bit `i`, the outgoing carry satisfies

\[
\left\lfloor\frac{q+i}{b}\right\rfloor=
\begin{cases}
0,&q<b-1,\\
i,&q=b-1,\\
1,&q\ge b.
\end{cases}
\]

Thus a singleton's outgoing carry differs from the actual outgoing carry
exactly when its coefficient is neutral and the actual incoming carry is
one. Singleton blocks minimize every isolated outgoing carry. Equivalently,
they simultaneously maximize every actual-minus-isolated carry defect.
Both inequalities are formally proved against arbitrary reset patterns.

The main theorem `exists_partition_defect_iff` proves

\[
\begin{split}
&\text{some consecutive partition has a nonzero outgoing-carry defect}\\
&\qquad\Longleftrightarrow
\text{the word contains adjacent coefficients }(h,b-1),\quad h\ge b.
\end{split}
\]

`HighNeutral` is a recursive scan; `highNeutral_iff_adjacent` proves its
explicit equivalent form `front ++ high :: (b-1) :: tail` with `high>=b`.
The proof follows a neutral run backwards to its first carry-producing
high coefficient. Its induction retains an arbitrary initial carry: a
leading neutral run may be active when the initial carry is one. Setting
that initial carry to zero discharges this exception for an actual word.

The existential theorem ranges over all tagged lists with the prescribed
coefficient projection. Their Boolean reset flags represent every
consecutive partition. The first flag has no effect at initial carry zero.
Pointwise comparisons use a zero default outside the word; both compared
lists have the same length, so invalid indices cannot witness a defect.

## Ordinary output safety and exact limits

For `b>=3`, `highNeutral_output_safe` combines the characterization with
the all-base raw-symmetry theorem. On a symmetric coefficient word, one
high/neutral adjacency certifies that its ordinary normalized output is
nonpalindromic.

`highNeutral_reverse_add_safety` derives the coefficient hypotheses from
canonical input digits and their actual reflected pair sums. It proves
that the ordinary reverse-and-add result has valid digits, a positive
leading digit, exact integer value `n+reverse_b(n)`, and a nonpalindromic
canonical digit expansion. It needs no selected partition or index as
input: the local pair pattern supplies the witness.

This is **not** a characterization of every nonpalindromic output.
Absence of a high/neutral adjacency means every partition has zero carry
defect, but the output may still be nonpalindromic. For example, decimal
pair coefficients `(12,12)` normalize to 132 without any neutral 9.

The combinatorial equivalence includes base two; output safety does not.
The kernel-checked `binary_safety_boundary` retains the exact counterexample

\[
110_2+11_2=1001_2.
\]

Its pair word `(1,2,1)` contains a high/neutral edge and has a nonzero
singleton carry defect, yet the ordinary output is palindromic.

No input-nonpalindromicity conclusion is asserted for arbitrary bases.
The prerequisite reverse-add package retains the odd-base control
`212_3+212_3=1201_3`: its palindromic input has a high/neutral pair word.
The external decimal input-parity argument must not be generalized to
odd bases.

These results turn a search over partitions into a local pattern test.
They do not prove that this pattern persists under iteration, and they
supply no infinite safe trajectory or Lychrel witness.

## Reproduce and audit

From the repository root:

```sh
python proofs/contributions/2026-10-15-base-intrinsic-formal/check.py /path/to/lean
```

The checker freshly builds all nine exact source files in an isolated
temporary directory, checks their source hashes remain unchanged, and
audits all 109 theorem declarations. Only `propext`, `Classical.choice`,
and `Quot.sound` are permitted. `verification.json` records SHA-256 and
Git blob identities; `compile.log` retains the complete audit. Rejected
drafts and failure replays are retained separately. No previously compiled
objects are used by verification; runtime binaries, generated objects,
and temporary build copies are excluded.
