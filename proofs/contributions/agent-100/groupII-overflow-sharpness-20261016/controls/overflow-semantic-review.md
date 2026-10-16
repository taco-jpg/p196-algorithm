# Group II overflow sharpness: independent semantic review

Status: **PASS — independent fresh canonical 18-module build plus explicit `--trust=0` full-import type-check and module-origin audit. All 52 new explicit exports are independently reviewed.**

Reviewer: Agent #100 `scope_audit`; author of no Lean theorem in this task. Claim `3dff9cae7193784bf851b183a5f0ea531e36eccb` / task blob `d308a57524a4ea5e2b0bfb1ed1809e299d50515f`.

## Result being reviewed

For the seven Group II cores, every spacer `r >= 1`, and exterior `1 <= p <= 9`, the actual two-step overlap holds exactly when `p <= 4`. The overlap predicate includes actual width compatibility and compares the full valid whole prefix to `shiftOne` of the actual component prefix after finite zero extension. For `5 <= p <= 9`, the actual signed difference is `x^(r+1) * (1 - x^2 - x^3 + x^5)`: six entries `(1,0,-1,-1,0,1)`, with four nonzero coefficients. The upper case is realized by ordinary reverse-add outputs for every original canonical whole-input realization.

This is a finite two-step statement for the stated cores and shift. It does not classify other cores, alternative shifts, future repairs, or infinite orbits. It does not assert a multiplicative relation between ordinary component/whole input integers or ordinary realizability of the raw redundant comparison word.

## Frozen source identity

- `proofs/Agent100GroupIIOverflowProfiles.lean`: SHA256 `1f2879f381efdc7d7d01217650949758394878f229b11de2f1664c04c50ad391`, Git blob `fc901380fa8a7d5e559e34fc11b5f08862b55331`, 26 explicit theorem exports.
- `proofs/Agent100GroupIIOverflowBridge.lean`: SHA256 `83e99438bbec009800bfb4cd206729352d77a456eba8bf875fe906c5c8d404fa`, Git blob `cf776d1eca09dfba9a9f27ec2399d978eee692c5`, 6 explicit theorem exports.
- `proofs/Agent100GroupIIOverflowDefect.lean`: SHA256 `d2240f0a3bb69f33524a43eee43600742c60b4fd1a715af63bc3f0a097bf1fcd`, Git blob `1c815fd2c2b58af56741f63df217728dee761763`, 6 explicit theorem exports.
- `proofs/Agent100GroupIIOverflowSharpness.lean`: SHA256 `f5372a43505665f5bf13c83a8900340091e247043a760c65defb76a4264bca4f`, Git blob `6f8a5125b0855b2d70858b18da45ccb9ab0c312b`, 9 explicit theorem exports.
- `proofs/Agent100GroupIIOverflowNumeric.lean`: SHA256 `220815c06fb95f0834c747c208edab3381f11494fa13ef8a12e507e0ef9b9d55`, Git blob `f116cf5bfa2c148a5c879ad398dca6730c14f5ff`, 5 explicit theorem exports.

## Statement and boundary checks

### Domain — PASS

UpperDomain is exactly r>=1,5<=p<=9,5<=u<=8,5<=v<=6,u+v<=13; seven Group II cores. No r>=2 replacement or group generalization.

### First step and p9r1 boundary — PASS

Full carry certificates apply through terminal widths, proving both first terminal carries zero; no unsupported small-exterior assumption. component->doubled component and initial->middle are actual finite prefixes.

### Second terminal carries and widths — PASS

Doubled component, middle, and raw redundant have terminal carry exactly1. Actual successor widths 2r+7,2r+8,2r+8 are established separately.

### Raw redundant restriction — PASS

redundant_not_admissible proves central coefficient4v>=20 violates bound18. Exact carry profile allows interior2, terminal1. No canonical realization of this comparison word asserted.

### Normalized defect — PASS

Difference uses Int, equals (1,1,0,-1,-1) on r+1..r+5, antisymmetric in old width2r+7 and nonzero. Both endpoints and r1 retained.

### Finite digits and columns — PASS

componentDigits and finiteNextComponent both clip after actual component successor width2r+7. The appended normalized carry digit at2r+6 is1; later tail is0.

### Concrete digit overlap bridge — PASS

redundant_extended_digits covers every valid index i<2r+8, including final i=2r+7. v=5 or6 central arithmetic is kernel decide, not extra hypothesis. Adjacent normalized sum<=9 follows from exact equality to bounded actual digits.

### Pair overlap bridge — PASS

redundant_next_is_finite_overlap compares actual raw nextColumns prefix width2r+8 to shiftOne of clipped next component. Proof explicitly treats i0, i2r+7, and interior; no constant extended tail used.

### External generic transport — DEPENDENCY_REVIEW_PASS

Agent8 source8874b2ee / blob91dd7832 / SHA55bad566 is unchanged and requires only common terminal carry1 plus old normalized defect antisymmetry. Its finite support includes both new boundaries. The final concrete application was reviewed in Defect and passed.

### Concrete use of Agent8 transport — PASS

Defect supplies proven equal terminalcarry1 and proven old-digit antisymmetry to unchanged common_carry_transport. supported_digit_defect identifies the entire zero-extended defect function before shifting, not only its old prefix.

### Signed difference orientation and support — PASS

Int difference is actual whole successor minus finite component overlap. It is +1 at r+1,r+6, -1 at r+3,r+4, zero elsewhere: six-entry pattern (1,0,-1,-1,0,1), polynomial x^(r+1)(1-x^2-x^3+x^5). All nonzero columns lie in width2r+8 including r1. Witness r+1 is unconditional within UpperDomain.

### Actual two-step orbits — PASS

componentOrbit/wholeOrbit directly abbreviate existing iterPairs from original component/initial and original widths. Carry/extended congruence uses all relevant valid old columns, proving actual second widths2r+7/2r+8 and their complete valid prefixes.

### Exact overlap predicate and lower branch — PASS

TwoStepOverlap requires whole width=component width+1 and equality throughout actual whole width after component zero extension. Lower branch additionally proves returnedComponent zero outside width2r+6, allowing a valid all-point finiteWord identification before shiftOne.

### Sharpness theorem — PASS

two_step_overlap_iff is precisely FullDomain(r>=1,p1..9,seven cores) -> (TwoStepOverlap iff p<=4); upper failure is a witnessed coefficient discrepancy despite the correct width relation. No other core, shift, encoding, or later time is classified.

### All ordinary whole-input realizations — PASS

Numeric quantifies caller-supplied n,d universally, with original Canonical and every initial pair column as hypotheses. iterPairs_representation retains original n and gives canonical digits of orbit n 2, exact width2r+8 and every valid pair column. It does not select one convenient initial representative.

### Realizability and ordinary failure — PASS

upper_initial_realizable derives existence of positive original n from proven initial_admissible. realized_overflow_defect composes this existence with arbitrary-input numeric theorem. Failure is for full overlap of canonical whole output with actual symbolic component pair orbit; no ordinary realization of raw redundant is used.

### Precise output scope — PASS

The ordinary lift provides an output canonical representation e for every admissible original n,d; it does not assert a multiplication relation between two ordinary input integers, a separate component-integer theorem, palindrome safety, any alternative shift obstruction, or infinite nonreturn.

## Evidence separation and execution

The 420 archived diagnostics test one chosen canonical realization per input profile and do not establish universal mathematics. They were copied without rerunning, and both the complete JSON XZ and ownership snapshot archive were decompressed and byte-compared to the retained originals. The universally quantified ordinary-input result is supplied by Lean Numeric and its exact representation theorem, not inferred from those finite tests.

The final import closure is exactly 18 modules, rooted at `Agent100GroupIIOverflowNumeric`: six existing foundations, Group II Dynamics/Defect, five additional Agent #8 transport-chain modules, and five new overflow modules. One source-identical LychrelDigitSums module is shared by both chains. Agent #8 transport remains unchanged and attributed to its original author.

The independent run uses official Lean 4.19.0 and the unchanged canonical verifier in a new output directory, without author oleans. It checks every registered source SHA256/Git blob and actual imports, recompiles the full closure, checks all 52 new explicit exports, and audits every theorem constant originating in the selected modules. The actual complete theorem-axiom union is exactly `propext`, `Classical.choice`, and `Quot.sound`, as recorded in the finished raw audit and complete multiline ledger. A separate invocation receipt identifies this reviewer because the unchanged verifier internally labels itself Agent #1.

Default-sandbox compiler-startup failures were preserved separately as environment probes. They were resolved by the approved expanded execution environment with the same unchanged official compiler. Those probes were not proof compilations and are not classified as mathematical failures.

The single independent run completed with all 19 commands at exit 0: 18 module compilations and ProjectAudit. The audit covered 2,576 theorem constants (384 originating in the five new modules, including generated declarations). Every one of the 52 explicit exports was also matched between its complete multiline raw `#print axioms` list and the fresh full module-origin ledger. Exactly 51 explicit new exports use `propext` and `Quot.sound`; `two_step_overlap_iff` additionally uses `Classical.choice`. The complete closure union is precisely those three standard axioms. Fourteen existing unsafe implementation declarations are separately reported; none occurs in any audited theorem dependency set.

The two inherited endpoints `Agent100.GroupII.returnedComponent_core_table` and `Agent100.GroupII.returnedComponent_not_same_shape` both report all three standard axioms in this fresh run. Their earlier simplified ledger was not copied. See `verification/complete-axiom-ledger.json` and preserved raw logs.

The run source HEAD was `491b477889b6336f5386287e3665f6ce58a34d9b`; the original branch base was `d591ce6d0cbf2bceab219fe915b1cebcc16a5879`. The complete source publication is `686cac2696e4e4e059c1b9d6a313f5519f6f4176` (tree `6f25211e084ebee89ca964820e03258cd294b361`, Draft PR125). Independent immutable `git show` reads confirmed all 18 published source files are byte-identical to both their fresh build snapshots and the post-run local files. See `verification/post-build-source-identity.json`. This is scoped independent review and execution; repository-wide accepted-build integration is not claimed.

## Explicit trust-zero verification amendment

The original canonical run compiled all 18 sources fresh and audited all 2,576 theorem constants, but its 19 recorded command arguments did not explicitly request `--trust=0`. It must not be described as an explicit trust-zero run. To close that concrete remaining gate, the original `ProjectAudit.lean` was subsequently executed with `--trust=0 -j1 -DElab.async=false`, using the same original fresh source directory and its 18 newly produced local oleans. This was an actual additional execution with exit 0, not a second fresh source build.

The strict run typechecked the imported modules and repeated the full module-origin audit. All 2,576 declaration names and complete axiom sets match the earlier fresh audit, all 52 explicit endpoints were checked, and all source/olean post-hashes remain unchanged. The deterministic raw audit output has the same SHA256 as the earlier audit; the distinct strict argv, execution interval and exit status are retained in `verification/strict01/strict-import-verification.json`. No Lean mathematical source, canonical verifier, or original archive was changed.

The original `b371c559...` archive remains byte-for-byte intact as the original canonical evidence. The strict log, command/receipt, source/olean hashes and these corrected review documents are retained separately in `verification/strict01-evidence-amendment.tar.xz` and its manifest. The accurate combined label is **one fresh canonical18 build + one explicit trust0 full-import audit**.
