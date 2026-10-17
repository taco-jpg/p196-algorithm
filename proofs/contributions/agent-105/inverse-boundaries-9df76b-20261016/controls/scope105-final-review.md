# Agent105 / scope105 final independent verification

**Result: PASS under the unchanged repository verifier and PASS under an additional explicit `--trust=0` replay.** The frozen mathematical sources were not edited during either replay.

Reviewer: Agent #105, session 9df76b, scope105. The reviewer authored the concrete witness control, independently reviewed the WidthSupport module, and performed the complete nine-module rebuild. Separate non-author semantic review of the witness, cross-width and palindrome modules is assigned to runtime105.

## Exact source boundary

- Published source commit: `5923015f86eb1ef898becd77ce2ee328ff338b69`.
- The unchanged verifier recorded `source_tree_clean: true`.
- Registry: `proofs/Agent105InverseBoundaries9df76b.registry.json`, SHA-256 `e3dd87aed89813c536910947176954521fd069c5fa1faeff9f3648ea19ab0c87`.
- Unchanged verifier: `proofs/verify_project__214bf7673efe116b.py`, SHA-256 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`.
- Official toolchain: Lean 4.19.0, release commit `6caaee842e94`.

| New module | Frozen SHA-256 |
| --- | --- |
| `Agent105WidthSupport9df76b` | `3411c212f4c7c05d1d91cc7249f1d6520f9da1202da6721ca9b1764944ff3da7` |
| `Agent105CrossWidth9df76b` | `a8fe89a91d79809bb3452a39775eb0cc9a06241d37e37c7ef916bf20f265d7a2` |
| `Agent105CrossWidthWitness9df76b` | `57d7fad87d320eddf13c32f35f2ab1cf11e2c318073c1cf2466e265baea73252` |
| `Agent105PalindromeImage9df76b` | `029bcf37c74d0d6a2b226cf60011ba7d66a3daee40087833f039b13be0e6cce6` |

The registry retains the exact original foundation and the four published Agent101 modules; their bytes, Git blob identities, and import closure were checked by the unchanged verifier.

## Two separate successful replays

The original verification at `verification/fresh-scope105-001/verification.json` reports `PASS`. It rebuilt all nine registered modules in a new directory and executed its generated `ProjectAudit.lean`, auditing every theorem whose module of origin belongs to the selected closure. This includes private and generated helper theorems. The source, compiler, registry and import checks are the repository's existing acceptance policy. The verifier was not modified.

The official `lean --help` output reports a default trust level of `max`. The original verifier's actual compiler arguments do **not** include `--trust=0`; this record does not describe them as if they did.

The supplemental run at `verification/strict-scope105-001/strict-verification.json` reports `PASS_EXPLICIT_TRUST_ZERO`. It copied only the original run's exact nine Lean source snapshots and exact generated ProjectAudit into another empty directory, then rebuilt every module and executed that same audit with explicit `--trust=0 -j1 -DElab.async=false`. All 11 commands, including the recorded official help call, exited zero. Its script, `controls/replay_strict_trust0.py`, supplements the original checker and does not alter its registry, source restrictions, import closure, or allowed-axiom policy.

- Original receipt SHA-256: `a309168ed0cb803c2c9b20156faab1c9bf4c564da62559d969e39127a9dbdddd`.
- Explicit-trust-zero receipt SHA-256: `f5c279db93de777711d6c3ae15756e70633015551e9f9754f7f5e647ff6f7320`.

## Audit result

Both runs audited **1,042 module-origin theorems**, with proof-axiom union exactly `Classical.choice`, `Quot.sound`, and `propext`. No audited theorem depends on `sorryAx`, a native-evaluation axiom, or any custom mathematical axiom. The 1,042 figure counts the complete dependency closure and generated helper declarations; it is not a claim of 1,042 new results. The registry lists 38 public endpoints for this contribution.

| Module | Audited theorem declarations |
| --- | ---: |
| `Lychrel196Research` | 787 |
| `Agent101DigitPairs` | 27 |
| `Agent101MultiplicityBounds` | 28 |
| `Agent101SplitEnumeration` | 58 |
| `Agent101NumericFibers` | 56 |
| `Agent105WidthSupport9df76b` | 8 |
| `Agent105CrossWidth9df76b` | 22 |
| `Agent105CrossWidthWitness9df76b` | 20 |
| `Agent105PalindromeImage9df76b` | 36 |

The checker separately records 22 unsafe implementation axioms generated inside existing foundation/Agent101 dependencies. They are not theorem proof dependencies. None originate in the four new Agent105 modules. These records remain visible in the unmodified audit output; they have not been silently discarded or described as absent.

## Semantic review and concrete controls

`controls/width-support-semantic-review.md` reviews all seven source theorems in WidthSupport, which the reviewer did not author. The review verifies actual canonical decimal width, equality only of in-range digits, the original numerical step bridge, and the deduction of adjacent widths with carries one and zero. It finds no semantic defect.

The witness module transports concrete positional digits through the original `reverse10_value` bridge. Its 18 public kernel controls establish canonical widths 6, 7, and 7, actual reversals 997002 and 98901, the common step value 1197801, and its nonpalindromicity; they also establish the 29/110 to 121 boundary. The original note supplies the two coefficient profiles and their nonpalindromic common output. It does not literally list 200799 and 1098900; this contribution supplies those canonical integer realizations. No new counterexample-discovery claim is made.

Witness attempt 001 is retained as a failure: four redundant `decide` tactics ran after rewriting had already closed the corresponding goals. Its failed elaboration produced a `sorryAx` audit line, which is not accepted evidence. Attempt 002 removes those redundant tactics and exits zero; the unchanged and strict final replays independently recheck the same frozen successful source.

## Scope of the accepted result

The cross-width results give necessary conditions for collisions at distinct input widths and an all-width bound of two finite pair-sum profiles for a numerical output. This is not a bound of two ordinary integer predecessors. No new general explicit union-of-two-`numericFiber` membership endpoint is claimed.

The palindrome result characterizes positive one-step palindrome targets by even width or even middle digit, supplies a same-width zero-carry predecessor, and, for target width at least two, supplies first occurrence at time one. These are one-step inverse results. No arbitrary-time nonpalindromicity, termination, or 196-resolution theorem is asserted. The source registry explicitly declines repository-wide catalogue completeness.
