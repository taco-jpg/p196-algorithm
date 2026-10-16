# Exact carryfree saturation: acceptance and source scope

## Mathematical result

The carryfree portion of the historical source's Theorem 3 is now proved for
its original decimal and spectral interpretation. For every odd L>=5 and
every s<9,r<11, there is one ordinary canonical nonpalindromic integer n of
width L whose digit sum is s modulo 9 and whose value is r modulo 11. Every
computed carry through the terminal position L is zero. Its actual
reverse-and-add successor is palindromic and has a canonical representation
of the same width L.

For every even L>=2 and every s<9, the source's single-leading-digit family
provides an analogous witness for the digit-sum class. Its actual pair
polynomial has Q(-1)=0. This is the source's even spectral r=0 condition;
it does not require the initial integer n to be divisible by 11.

The final endpoints do not stop at these ordinary residue statements. They
define Q(x) as the literal finite Int evaluation of the original
DecimalDigits.columnSum word and prove, for the same witnesses, Q(1) equals
twice the ordinary digit sum and the exact half-coordinates have the required
residues modulo 9 and modulo 11. No quotient ring is defined to make the
conclusion tautological, and no existence or palindromicity condition is
assumed in the witness construction.

## Construction and exact edge cases

For odd width, the source chooses 1<=u<=10 and 0<=b<=9. Set a=min(u,9) and
c=u-a. The actual input is

    n = a*10^(L-1) + b*10^(L-2) + c*10^(L-3).

The proof establishes 1<=a<=9, c<=1 and a+c=u. Its units digit is zero and
its leading digit is positive, so the original numeric input is not
palindromic. The same digit function is proved canonical by the original
finite value equation and decimal digit bounds.

The six literal pair-polynomial terms have coefficients a at the endpoints,
b at positions1 and L-2, and c at positions2 and L-3. At L=5 the two c terms
coincide and add to 2c. Every column remains at most9. The original column
equation and carry recurrence yield every actual carry zero, then the
original normalization and palindrome theorems give the exact next value and
its same-width canonical representation.

The numeric digit sum is u+b and n mod 99=(u+10*b) mod 99. A constructive
parameter lemma solves the two residue conditions by taking
x=(55*s+45*r) mod 99, replacing x=0 by99, and setting
u=(x-1) mod10+1 and b=(x-1)/10. This supplies all 99 classes, including the
simultaneous zero class and permitted u=10 cases, without assuming a
surjectivity certificate or enumerating a finite set of widths.

The literal odd alternating evaluation is Q(-1)=2*((u:Int)-(b:Int)).
Division by 2 is exact even when this value is negative. Its half is congruent
to u+10*b modulo 11, hence to the same input n. The proof uses Int for the
subtraction and modular half; it never truncates a negative difference as a
natural number. The canonical Q(1) identity independently gives the required
digit-sum class after exact division by 2.

At even width, choose 1<=a<=9 with a mod 9=s, using a=9 for the zero class.
The input a*10^(L-1) has the same physical properties, with pair columns a
at the two endpoints and zero elsewhere. Their alternating signs cancel at
even L. The minimum width L=2 is included, giving a0 followed by aa.

Two certified concrete controls exercise the main semantic boundaries:
19000 has the alternating half -8 and modulo 11 residue3; 99000 has both
ordinary residues zero and its actual next value is 99099. These controls
supplement the universal proofs; they are not evidence substituted for them.

## Frozen source and independent review

All four new mathematical files and the scoped registry are unchanged from
source checkpoint a883847381cd800b13e511d8ccc8909ba998866c. All18files in that
checkpoint, including its binary author archive, passed remote byte-for-byte
and Git blob readback. The original decimal foundation remains source
SHA256 ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57,
imported as LychrelDigitSums and mapped to the original 0810ace083af80c5 file.
SOURCE_FREEZE.json and the scoped registry give every exact source hash and
module import. The registry has 22 distinct endpoints and explicitly leaves
catalogue_complete and repository_wide_pass false.

There are two genuine nonauthor reviewers. /root/spectral_semantics read the
historical contract, all 55 explicit new declarations and proof bodies, the
original decimal interfaces and all 22 registry endpoints. Its final decision
is PASS_SEMANTIC_REVIEW_COMPLETE_SCOPED_CLAIM. /root/runtime independently
checked the pinned sources and executed the canonical gate, a separate
fresh strict source build and exhaustive declaration audits. The two source
authors are parent /root for Digits/Saturation and /root/coverage for
Residues/Coordinates; only the parent publishes Git changes. All specialists
were initially configured with reasoning effort ultra, and no imaginary
reviewer accounts or additional parallel capacity are asserted.

## Execution results

| Gate | Observed result |
|---|---|
| Unchanged canonical verifier | PASS, five fresh modules, 22 endpoints, 1204 theorem constants |
| Canonical flags | -j1 -DElab.async=false; no explicit --trust=0 |
| Separate independent source build | All five sources freshly compiled with --trust=0 -j1 -DElab.async=false |
| Complete safe-origin audit | PASS, 1358 safe constants: 1204 theorems, 140 definitions, 14 other safe declarations |
| Public interface audit | PASS, 55 explicit declarations; full literal types and axiom reports |
| Cross-audit comparison | Complete canonical/strict theorem sets identical; every public axiom report agrees with the exhaustive audit |
| Transitive safe axiom union | Exactly propext, Classical.choice, Quot.sound |
| Independent build/audit executions | One run completed exit 0; no build or audit rerun |

The 14 other safe declarations consist of four inductives, six constructors
and four recursors; there are no safe opaque declarations. The independent
audit separately inventories 784 unsafe and 18 partial implementation constants.
Generated theorem helpers are included in the 1204 count; that number does
not count distinct new mathematical claims. The 55 explicit new declarations
are 49 theorems and six definitions.

The independent build reused no author project object and no canonical
project object for the separate strict build. Later import audits inspect
literal types, origins and transitive axiom dependencies; they are not
represented as re-kernel-checking every previously compiled proof term. The
fresh source compilations provide ordinary kernel checking.

A later report-writing invocation failed at JavaScript parsing before any filesystem command ran. The independent archive preserves that artifact-preparation failure and its correction separately; it did not cause a mathematical gate rerun.

The unchanged official Lean 4.19.0 release remains pinned to commit 6caaee842e94
and executable SHA256 92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023.
The preceding independent runtime check compared all 4617 nondirectory members
with the official release archive, SHA256 6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe.
The current verifier's exact runtime identity and source hashes were checked
again. The complete preceding provenance remains published with PR144; no
new runtime verification is fabricated by referring to that earlier evidence.

## Preserved development and reporting precision

The lossless author archive contains every substantive source attempt, raw
log, command and observed status for both authors. The first Saturation
attempt proved the physical witness statements. The next preserved attempt
failed only in two finite-control closures; the following one retained a
redundant tactic after a solved control. Final attempt 004 compiled the
complete frozen source. Residues and Coordinates each retain their failed
initial source and successful second source; Digits compiled on its first
attempt. No failed source or diagnostic has been erased or relabeled.

The author runner's dependency inventories enumerate an entire auxiliary
directory, including a stale same-module source/object left by an earlier
successful physical attempt. Those arrays are not the exact direct-import
list and are not evidence of a clean build. The reviewer independently
verified the actual attempt 004 source hash 2427fcac82b20afe208ae2529b1dc9436217395eef63fcceb707447b0064171a and its three imports;
there is no self-import. Historical receipts are unchanged. The independent
empty-directory source builds and origin audits supply the stronger
acceptance evidence and discharge this author-provenance limitation.

The preliminary scout's incorrect flattened filename and alias are corrected
explicitly in CORRECTIONS.md while its original bytes are retained. An
unpublished typo in the correction draft is likewise retained as a separate
archive member; the published correction quotes the original scout exactly.
These source-location reporting corrections do not change the mathematical
blob, proof hypotheses or final module map.

## Scope and integration

This closes the carryfree part of the historical source's Theorem 3 at its
stated odd/even thresholds. It does not close the entire note, establish the
carry ideal or 1782-element quotient presentation, prove overflow saturation,
reimplement U/S/J or carry-support results, or assert reachability, persistence
or any all-time conclusion for 196. Agent 51 retains the separately claimed
overflow family and Agent 15 the charge/support work.

Source acceptance and current-main integration are separate. Agent 14 has no
main-write slot; the integration owner must verify the actual combined tree
and use the active guarded slot. Existing exact-source independent checks
remain valid for their unchanged closure and should not be described as
having run on an unexamined combined tree.
