# Independent final semantic review

## Verdict

**PASS — exact semantic coverage of the selected overflow-saturation source claim. No proof-source repair is required by this review.**

The reviewer read all four frozen contribution modules in full, independently checked their SHA-256 values, compared their actual propositions and definitions with the original source and the accepted contract, and examined the retained author endpoint and residue axiom-output logs. The reviewer did not author or edit any proof module and did not run Lean in this review. Independent clean rebuilding and integration/publication remain separate verification activities; this document does not claim them.

The initial contract review is preserved unchanged as `CONTRACT_REVIEW.md` (SHA-256 `f30c40140519f179a7af7b2aee13844b95eaee7cb3a46932cdc91e4b865660df`). Its administrative request for final theorem identifiers is resolved: the task now lists the three actual endpoint declarations reviewed below.

## Frozen source identity

All files were read from the authorized shared-memory source directory `/dev/shm/p196-agent51/source`.

| File | Independently computed SHA-256 |
|---|---|
| `OverflowDigits.lean` | `65adeb3ae7bea93e390a95fc5f8b58ec43f0f64f01ed9db3f51392657ba89a41` |
| `OverflowWitness.lean` | `fbf7568256e31948a20563e5d9e1335ce45b6859d2343917395180970114c901` |
| `ResidueSums.lean` | `1333e156e2da6f02a18ff67f83e8ce36955e93c00e425cf67aff713f916140d4` |
| `Saturation.lean` | `e2379506a0b70c1502fea88e8daff4241282be73f6f11672effff182a10bc722` |
| Reused dependency `LychrelDigitSums.lean` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |

The imported dependency's actual local module filename is `LychrelDigitSums.lean`; no file named `OriginalLychrel.lean` was present in that directory. The actual module hash agrees with the pinned original dependency, Git blob `8a865176625283648a8a20dd2411ed77670eb0a2`.

The original source text remains unchanged: SHA-256 `d39212c9ab98f4c5b0fccb733d3b662e41a09804878178c82b8762684e97fb09`, previously independently checked Git blob `eac5b8f61385a615d9cc3e7796a4d698c66b716b`. Its repository location is `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/astra_spectral_carry_quotient.md`, Theorem 3, overflow paragraphs, at source snapshot `54ac7c885e54ce74190b85ec82cceca2b23c2e38`.

The reviewed final local task record has SHA-256 `26e1db864e187e33a40b7c3283f350121df47677d47624a903b2dac1356c38af`. It is evidence of the named contract, not an independent remote publication receipt. Its historical status text still describes earlier pending work; the actual frozen declarations and the explicitly attributed retained build results below are the evidence used here.

## Exact source-to-declaration map

Every declaration in this table is in namespace `P196.Agent51`.

| Source obligation | Reviewed declarations | Finding |
|---|---|---|
| Actual decimal witness with leading 9 and units 2 | `inputDigit`, `inputDigit_zero`, `inputDigit_last`, `witnessNumber`, `witness_positive`, `witness_canonical` | Exact ordinary-number construction with canonical input width L |
| Exactly k symmetric pairs with coefficient 11 and zero elsewhere | `inputDigit_pair`, `pairWord_values`, `pairWord_zero`, `witness_columnSum` | Equality with actual mirrored decimal digit sums on every used index |
| Input is nonpalindromic | `witness_not_palindrome` | Uses the established numeric palindrome equivalence and the contradictory outer digits 2 and 9 |
| Actual final overflow h = 1 | `witness_overflow` | Computes the true terminal carry through the existing proved overflow criterion |
| Next reverse-and-add output is a palindrome | `witness_step_palindrome` | Uses `Lychrel196.step` and `Lychrel196.Palindrome`, with the canonical arithmetic bridge |
| Exact output width L+1 | `witness_step_canonical` | Canonical representation of the same numeric next state at width L+1 |
| Literal finite coefficient evaluation | `polynomialValue`, `finiteSum_eq_range`, `polynomialValue_eq_finiteSum`, `witness_polynomialValue` | Exact sum of actual coefficients times integer powers |
| Q(1) = 22*k | `pairWord_value_one`, `witness_value_one` | Exact integer equality for arbitrary width and pair count satisfying 2*k <= L |
| Signed Q(-1), hence divisibility by 22 and zero at even width | `pairWord_value_neg_one`, `pairWord_neg_one_dvd`, `pairWord_neg_one_even`, `witness_value_neg_one` | Stronger exact formula: 22 when L and k are both odd, otherwise 0 |
| s = Q(1)/2 mod 9 and r = Q(-1)/2 mod 11 | `sourceS`, `sourceR`, `pairWord_half_value_one`, `witness_sourceS`, `witness_sourceR` | Literal integer division before reduction; no replacement residue property |
| All nine s classes | `residue_parameter` | Correct selection of k in 1,...,9, separate from arbitrary-width reasoning |
| Saturation at every L >= 18 | `overflow_saturation` | Complete existential witness with all required conclusions simultaneously |
| Original even/odd thresholds | `even_overflow_saturation`, `odd_overflow_saturation` | Exact source parity hypotheses and thresholds 18/19 |

## Witness construction and arithmetic semantics

The constructor's hypotheses are only `0 < k` and `2*k <= L`. They guarantee disjoint digit blocks: k twos at the least-significant end and k nines at the most-significant end. Each mirrored pair sums to 11. The middle gap may be empty; when the width is odd, its central coefficient is zero. No stronger hidden separation premise is introduced. In particular the boundary L = 2*k is included.

The input is `DecimalDigits.value (inputDigit L k) L`, not an abstract symbolic state. `witness_canonical` proves bounded digits, positive width, a nonzero leading digit, and exact value equality. This is a genuine exact-width canonical representation. `witness_not_palindrome` applies `DecimalDigits.palindrome_value_iff` to ordinary numeric reversal and uses unequal outer digits. It does not merely assert that a chosen representation lacks symmetry.

`witness_overflow` derives `DecimalDigits.carry (DecimalDigits.columnSum ...) L = 1` from the proved {0,11} criterion. In the source, h is the carry leaving column L-1; in the existing library, `carry q L` is the incoming carry to position L. These are the same actual terminal carry. Overflow is a conclusion, not an assumption of the witness or final saturation result.

`witness_step_palindrome` uses the existing exact bridge to `Lychrel196.step`. `witness_step_canonical` uses `FoldedDecimal.canonical_next_overflow` to append the computed carry as the leading digit. Consequently the output has exact width L+1; there is no leading-zero or fixed-width reversal ambiguity.

The final endpoint uses the same n and d for all conclusions. It neither obtains one witness for residues and another for arithmetic properties nor assumes reachability of that witness from an earlier orbit.

## Literal coefficient and division semantics

`polynomialValue q L x` is defined directly as the sum of `((q i : Int) * x^i)` over `List.range L`. `finiteSum` is an auxiliary recursive summation function, and `finiteSum_eq_range` proves its literal finite-list interpretation. The source polynomial is therefore preserved, including the signed powers at x = -1.

The actual `columnSum` and the convenient `pairWord` need agree only for i < L. That is exactly the hypothesis supplied to `polynomialValue_congr`; no unrestricted function equality is assumed. This matters because reflection uses natural subtraction and total functions may differ beyond the represented width. The final residue theorems are stated for the actual `DecimalDigits.columnSum`, and the bounded congruence transfers the explicit calculations correctly.

`pairWord_polynomial_blocks` splits the sum into disjoint blocks, with the middle zero gap handled under 2*k <= L. It holds for arbitrary natural L and k in that range. At x = 1, both k-term blocks have coefficient 11, giving Q(1) = 22*k. `pairWord_half_value_one` proves exact halving to 11*k before taking the modulus.

At x = -1, the proof evaluates the alternating prefix and its positional shift. The resulting identity is

    Q(-1) = if L mod 2 = 1 and k mod 2 = 1 then 22 else 0.

This is consistent with pairwise cancellation at even width and with the signed paired contributions at odd width. The fact that this chosen family never has negative Q(-1) does not remove integer semantics: the definition and the intermediate powers remain in `Int`. Both possible evaluations are divisible by 22, so halving gives 0 or 11 and the literal sourceR is zero. The code proves this directly from the exact evaluations.

`sourceS` and `sourceR` are the source expressions `(Q(1)/2)%9` and `(Q(-1)/2)%11`; they are not definitions that contain the desired target residue or existential assertion. The final equality to `(s : Int)` compares the literal residue with the requested natural class representative. No conclusion that an even-width input n is divisible by 11 appears.

## Quantifiers, boundaries, and finite reasoning

`overflow_saturation (L s : Nat) (hL : 18 <= L) (hs : s < 9)` is universally quantified over arbitrary width and every one of the nine natural residue representatives. It concludes existence of a positive canonical nonpalindromic input, actual overflow, a palindromic next output with canonical width L+1, and both literal residues. No conclusion or equivalent missing premise is included in its hypotheses.

`residue_parameter` enumerates only the nine residue values and chooses k from 1,...,9. Its cases are correct: for s = 0,...,8, the chosen k values are 9,5,1,6,2,7,3,8,4. From k <= 9 and L >= 18, the proof derives 2*k <= L and applies the unrestricted construction. The finite case split is therefore a finite modular choice inside an unbounded-width proof, not a finite substitute for saturation.

The even corollary adds L mod 2 = 0 and keeps threshold 18; the odd corollary adds L mod 2 = 1 and uses threshold 19. Their parity assumptions are unused in the proof because the stronger combined endpoint already applies. This is legitimate strengthening, not loss of an original case.

## Proof integrity and observed execution evidence

Full inspection of the four new modules and a declaration/forbidden-token scan found no custom axioms, unsafe declarations, `sorry`, `admit`, `native_decide`, or `Lean.ofReduceBool`. The proof dependency direction is acyclic: elementary digits and literal sums feed the actual witness bridge and final theorem. No hidden section variables, circular assumptions, inconsistent arithmetic bounds, or abstract replacement for numeric semantics were found.

The reviewer read the retained author records for:

- `LychrelDigitSums-001`: exact dependency hash above; recorded exit code 0, status PASS, source unchanged, 74.085780703 seconds.
- `ResidueSums-005`: exact residue-module hash above; recorded exit code 0, status PASS, source unchanged.
- `Saturation-001`: exact final-module hash above; recorded exit code 0, status PASS, source unchanged.

These records specify Lean 4.19.0 with `--trust=0 -j1 -DElab.async=false`. They are author-run evidence inspected by the reviewer, not executions performed by this reviewer. The retained `Saturation-001/compile.log` prints all eight exported declarations from that module, including all three saturation endpoints, with exactly the permitted foundational axiom set `[propext, Classical.choice, Quot.sound]`. The inspected residue log likewise contains only subsets of those permitted axioms, or no axioms for the definitions. These outputs are the actual retained transitive axiom reports, not an inference from tactic names.

A separate fresh independent rebuild of the full import closure is still a distinct acceptance gate. This semantic review neither substitutes for that gate nor asserts that the contribution is integrated into the accepted repository build.

## Publication and scope boundary

This verdict applies to the exact frozen local bytes listed above. The reviewer performed no remote writes or remote verification. The coordinator identified PR 148 checkpoint `e74d8f0c` as containing only the two initial root-authored modules; this review does not claim that checkpoint already contains the complete four-module contribution. Publication receipts and final repository inclusion must be supplied separately against matching hashes.

The exact selected source claim is semantically covered. The full carry-defect ideal and quotient-ring theorems, carry-free saturation, classification of all possible invariants, special-orbit reachability, and all-time 196 avoidance remain outside this review. No repaired or weakened substitute for the selected overflow claim was needed.
