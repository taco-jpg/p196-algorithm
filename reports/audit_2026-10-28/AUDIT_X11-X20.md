# AUDIT X11-X20 — agent-V05 independent red-team review (2026-10-28)

**Proof-relevant finding:** **ISSUE X11**: the numbered conditions of the proposed *all-time rotation-sheet edge soundness theorem* omit the endpoint carry equation `C_p(q,n)=gamma` (where `gamma=n_next-n`). As written, they admit false reverse-and-add edges. A two-case counterexample, exact correction, and GMP-free reproducer follow. This is a defect of the **PAPER PROOF specification**, **not** a claim that X11's actual 20,000-step decimal replay is wrong. No decimal Lychrel certificate is found.

| Result(s) | Claim and scope | Label in notes | Independently reproduced? | Defect / caveat |
|---|---|---|---|---|
| X11 `QuadraticRotationSheets` | General rotation-sheet all-time criterion; exact Beatty one-step edge; 20k finite example | PAPER PROOF + COMPUTED | **Counterexample to theorem**, finite example N | **ISSUE**: missing `c_n=gamma`; unconditional edge theorem and proposed checker contract are unsound as written. Beatty edge itself follows by direct carry algebra. |
| X12 `DualClockEnvelope`, `TwoClock20000`, `TwoClockCentrePulse` | Finite two-clock splices and 20k trajectories, sampled `(q,r)` | COMPUTED | N | All published time/parameter scopes finite; no claimed universal all-time return. No contrary evidence from note review. |
| X13 `QuadrantAffinePumping` | Symbolic affine-run soundness and six uniform decimal transitions for independent `k,l>=6` | PAPER PROOF + COMPUTED | **Partial Y**: 6 explicit independent `(k,l)` six-step integer trajectories | No return `H6->H0`; no all-time certificate. Did not rerun complete symbolic 277-comparison oracle. |
| X14 `GuardedShell` | Arbitrary-core universal-edge conditional criterion; base-9 1000-step controls | PAPER PROOF + COMPUTED | N | Conditional universal robust-edge checker unimplemented; the 1000-step erosion is finite, not a repair cycle. |
| X15 `CoupledDefectPacket` | p8 packet, 88-step drift and 20k finite examples | COMPUTED + conditional PAPER PROOF | N | Finite defect-budget consumption; full GMP-dependent reproduction not run. |
| X16 `AutomaticCarryRibbon`, `ForcedCarryReset`, `NineStepAllWidths`, `NineStepNeutralPorts` | DFAO soundness specification; all-width 3/9-step resets; finite 20k | PAPER PROOF + COMPUTED | **Partial Y**: independent Python-int nine steps at `k=0..499` (4500 additions) | No observed contradiction; full substitution-factor proof, 3001-width run, and 20k replay not rerun. No return at step 9. |
| X17 `BranchingFoldedPump`, `ChargeSelectedGate`, `DoubleDefectCarryCancellation`, `NeutralCarryGate`, `PalindromeShadow20000`, `ProgrammableChargeGate` | Finite carry firewalls, mask gates, and long-lived shadows | COMPUTED + local PAPER identities | N | Finite corridor exhaustion and absent charge replenishment are explicitly acknowledged. GMP-dependent campaigns not run. |
| X18 `FourthRenewalFront` | Four 88-step attempted renewals, nonexhaustive beam | COMPUTED | N | Fourth renewal fails; finite local search only. |
| X19 `DualCounterSquare` | 20k four-corner 99-insertion square at one pair `(Q,R)` | COMPUTED | N | No universal two-counter pumping in time; original finite-only limits are stated. |
| X20 `IndependentDualCounter`, `UniformDualPump20k` | 480 exact symbolic steps for all `m,n>=40`, and a 20k two-quadrant finite lift | PAPER PROOF + COMPUTED | **Partial Y**: 5 independent Python-int orbits through 480 additions; two distinct bulk bands checked on all 481 phase points | Long 20k and Boolean-matrix idempotence not rerun. `P0` is the *pre-normalization* coefficient word and differs from `pairs(N0)`; distinguish this indexing in future invariant proofs. No returning junction. |

## X11: formal counterexample and corrected soundness obligation

X11's numbered obligations require `c_0=0`, for every `0<=i<n` the exact local equations `s_i=d_i+d_(n-1-i)+c_i`, `e_i=s_i mod 10`, `c_(i+1)=floor(s_i/10)`, and a proposed target length `n+gamma`, with a terminal target digit `e_n=1` **if gamma=1**. They never require `c_n=gamma` when `gamma=0` **or** `gamma=1`.

* **Dropped overflow (gamma=0):** LSD-first `D=[8,9]` is decimal **98**; local outputs are `[7,8]`, carries `(0,1,1)`. Proposed `E=[7,8]` is **87**, with nonzero leading digit and both words nonpalindromic. Every written edge obligation holds, yet the genuine next number is **187**, not 87.
* **Invented overflow (gamma=1):** LSD-first `D=[1,2]` is decimal **21**; local outputs `[3,3]`, carries `(0,0,0)`. Proposed `E=[3,3,1]` is **133** and both words are nonpalindromic. Every written edge obligation holds, including `e_2=1`, yet the genuine next number is **33**.

**PAPER PROOF, exact correction:** Multiply `d_i+d_(n-1-i)+c_i=e_i+10 c_(i+1)` by `10^i` and sum over the n source columns. With `c_0=0`, the carry terms telescope to

`N + reverse(N) = sum_(i=0)^(n-1) e_i 10^i + c_n 10^n`.

For a canonical target of length `n+gamma`, `gamma in {0,1}`, with `e_n=1` iff `gamma=1`, **`c_n=gamma` is necessary and sufficient** for the proposed next numeral to equal the true reverse-add successor. Every edge of a prospective infinite rotation-sheet certificate must check this boundary for **all symbolic q**. The proposed two-torus checker is not implemented, so no executable all-time decimal claim is invalidated, but a future checker omitting this boundary would accept phantom transitions.

**Reproduce** without GMP or repository dependencies: `python3 calculation/new_structures/agent-V05/x11_endpoint_carry.py`. This independently checks both false edges against ordinary integer reverse-add, and the corrected boundary on every two-digit source (90/90). The arithmetic defect concerns the **all-time proof checker soundness lemma**, not a finite horizon or a base-10 nonexistence claim.

## Independent controls and limitations

Additional separate ordinary Python-`int` arithmetic in this audit: X13's six source/target pairword transitions at `(6,6),(6,90),(97,6),(27,101),(100,537),(123,222)` agreed for all six edges; X16's nine-step Thue-Morse port formula and overflow bits agreed at widths 0..499 (zero errors in 4500 additions); X20's five `(m,n)=(40,40),(41,40),(40,41),(41,41),(52,67)` ordinary-integer orbits agreed with the disjoint 20/48 bulk windows through step 480, with no palindromes. These are **sample controls only** and not substitutes for the agents' universal symbolic proofs or heavy 20k reproductions. X20's `P0!=pairs(normalize(P0))` is an indexing caution, not a demonstrated false arithmetic edge.

**Audit coverage:** inspected all 21 X11–X20 result-note titles and mechanism-critical selected reports/source; did **not** run large GMP campaigns, repo-wide `tools/verify.py --changed`, Lean, or unimplemented verifier specifications (no full local checkout and no GMP requirement imposed on this audit). Negative findings about untested horizons are expressly not claimed. The only newly **decided** all-time-proof obligation is X11's missing endpoint condition.