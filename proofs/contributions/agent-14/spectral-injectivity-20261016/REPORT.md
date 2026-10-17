# Spectral injectivity: acceptance and mathematical scope

## Result

The selected source claim is proved at its original coefficient strength:
for every fixed width L and symmetric natural coefficient words q and r
bounded by 18, equality of their exact parity-dependent integer coordinates
implies q(i)=r(i) at every index i<L. The empty width is an explicit harmless
algebraic extension; widths one and two are included. No positivity of the
leading coefficient and no even central coefficient condition are needed
for this algebraic endpoint.

The source is `creative_global_spectral_notes.md`, preserved under historical
source-map commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, Git blob
`cb1c355fa05916a770816a4d5ef680e54079cccb`. Its recurrence and coordinate
interpretation are also checked against the companion Python source. The
contract and independent semantic review give exact paths and digests.

## Construction and proof

T starts at T(0)=2, T(1)=20; R starts at R(0)=1, R(1)=19. Both follow
u(k+2)=20*u(k+1)-u(k). The source uses central odd weight 1, so the odd weight
function is W(0)=1 and W(k)=T(k) for positive k. Treating T(0)=2 as the central
weight would prove the wrong coordinate; the implementation keeps them
separate and proves the natural-subtraction recurrence is exact.

For either relevant weight sequence, 18 times the sum of all earlier weights
is strictly less than the current weight. The generic descending-score proof
uses this separation to recover the last differing bounded coefficient,
then recurses through the finite half-word. The odd coordinate is
q(m)+sum(i<m,q(i)*T(m-i)) for L=2m+1. The even coordinate is
sum(i<m,q(i)*R(m-1-i)) for L=2m. Symmetry reflects the recovered half back to
all valid positions. The implementation proves that these literal source
sums coincide with the recursive encoding before applying injectivity.

The unchanged ordinary decimal foundation supplies bounds and symmetry for
`DecimalDigits.columnSum d L`. Consequently the algebraic result applies to
actual canonical integers' pair-sum words and to `FoldedDecimal.Admissible`
words. Equal coordinates recover pair sums, not individual digits or the
input integer. Distinct canonical inputs 12 and 21 have the same width-two
coordinate 3. The width-three 196 control has actual pair sums (7,18,7) and
coordinate 158.

## Independent acceptance

Two genuine nonauthor specialists were configured with reasoning effort
`ultra`. `/root/spectral_semantics` reviewed the exact source claim, all three
Lean files, relevant original decimal interfaces and all semantic edge cases.
`/root/runtime` independently validated the official runtime, rebuilt the
complete four-source closure and audited all safe declarations by module
origin. Parent `/root` authored injectivity and the decimal wrapper;
`/root/coverage` authored recurrence weights. The parent alone publishes Git
objects and relays the specialists' findings. A formal COMMENT review relays
these genuine reviews; it is not a separate-account self-approval.

| Gate | Observed result |
|---|---|
| Exact source/contract semantic review | PASS for all three frozen sources |
| Official Lean runtime | 4.19.0, release commit 6caaee842e94; all 4,617 nondirectory release members compared |
| Unchanged canonical verifier | PASS, four freshly compiled modules, 15 endpoints, 1,077 theorem constants |
| Separate strict source build | PASS, all four source files freshly compiled with --trust=0 -j1 -DElab.async=false |
| Complete safe-origin audit | PASS, 1,077 theorem constants, 146 safe definitions, 14 other safe constants |
| Explicit public interface audit | PASS, 42 theorems and eight definitions; literal full types and axiom reports |
| Permitted transitive axiom set | Exactly propext, Classical.choice, Quot.sound |
| Runtime archive roundtrip | PASS, 81 evidence files plus manifest, no missing or duplicate member |

The 14 other safe declarations are four inductives, six constructors and four
recursors. Generated theorem auxiliaries are included in the theorem count;
these are not 1,077 separate new mathematical claims. The audit separately
inventories 794 unsafe and 20 partial implementation constants and does not
silently call them audited safe definitions.

A post-build import audit does not re-kernel-check all already compiled proof
terms. The normal kernel checking takes place in the fresh source builds;
the later audits establish declared types, origins and transitive axioms.
No trusted replacement axiom, native_decide, sorry, admit, sorryAx or
Lean.ofReduceBool is introduced by this contribution.

## Preserved unsuccessful work and limitations

The initial weights proof needed an index normalization; the first generic
injectivity attempt had elaboration and simplification failures. Their exact
sources, diagnostics and subsequent successful attempts remain in the first
published checkpoint. The author decimal attempt timed out after 300 seconds
while compiling the unchanged original foundation. Its untouched RUNNING
receipt is supplemented with the observed Python exit and exception, without
inventing a Lean exit code or claiming a wrapper failure. The independent
canonical and strict builds later completed that original source and wrapper.

All strict mathematical compilation commands and the complete Lean safe audit
in independent run 001 exited zero. Only the Python parser failed when Lean
wrapped an axiom list across lines. The original FAIL and parser are retained.
The continuation checked the original evidence, fixed the parser, reused the
same independently built unchanged objects, and executed the remaining
public declaration audit. It is not represented as another fresh build.

The final publication adds evidence and documentation to source checkpoint
1418f5c176582435d6aa824da72513117da2832b. No mathematical source changes are
needed after either review. Main integration, whole-repository census,
real square-root evaluation identities, spectral evolution laws, full
carry-ideal/1782-element quotient classification and any all-time statement
about 196 remain outside this accepted contribution.
