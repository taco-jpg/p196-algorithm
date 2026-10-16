# Group II independent source-semantic review

**Disposition: SOURCE SEMANTICS REVIEW PASS.** Reviewer: Agent #100's genuine `scope_audit` subagent. The parent is the sole publisher. This final review inspected all four frozen Lean modules, containing 53 theorem declarations, and independently executed the finite controls. It does **not** claim an independent Lean rebuild. The parent reports successful compilation and print-axioms checks of these exact bytes; independent execution is separate evidence supplied by the runtime specialist. Exact source pins and declaration inventories are in `semantic-review.json`.

| Source | SHA-256 |
| --- | --- |
| `Agent100GroupIIDynamics.lean` | `07b8c8d8c0c6fa4aefa1034272464531e27353586066651fd5dda55408d3091c` |
| `Agent100GroupIISafety.lean` | `c41ca271d9749e90c4490e676cecfb9e1de5d52164ecd9ec2d3e136e0925ec9f` |
| `Agent100DoubleGate.lean` | `192b21fc4335c69850c4609084ca8c8c2482241204e9c71f4006c1bf87ab8ebb` |
| `Agent100GroupIIDefect.lean` | `7dce1b0a08a5c0d86cfaf4cbb3584a9a3c7a0f294602170e7b44c11111eadb0f` |

## Statement interpretation

`Agent100.GroupII.Domain` is exactly `r>=1`, `1<=p<=4`, `5<=u<=8`, `5<=v<=6`, `u+v<=13`. The natural-number domain contains seven `(u,v)` pairs. There are 28 choices after including the four outer parameters, with unbounded spacer parameter `r`. This is the Group II part of the written twenty-core result; it does not claim the full 80-gate classification.

The component has finite width `2*r+6`. Its two-step image has the six-column core `(1,4u-19,4v-18,4v-18,4u-19,1)` and `r-1` zeros on each side. The whole word has width `2*r+7` and its two-step image is the explicit `shiftOne` of that component. Both actual widths are retained, not assumed as an independent return premise.

At `r=1`, the six-column component core is adjacent to the outer coefficient. Applying `shiftOne` adds the newborn coefficient 1 to `4p`, producing `4p+1` in the whole word's second and penultimate columns. The definition using `shiftOne(returnedComponent ...)` and the explicit `returned_first_neighbor` theorem correctly preserve this case.

The `intermediate_overlap_fails` witness is column `r+1`. That column lies strictly inside both actual component/whole widths. The statement therefore expresses a genuine departure followed by the stated repair, rather than merely a commutation identity.

## Ordinary integer semantics

The `numeric_middle`, `numeric_return`, and `numeric_two_step_safety` statements quantify over the original `n` and an arbitrary canonical digit function `d`. Their proofs use `representation_next` on that `n`, then on its actual first iterate. No construction replaces `n` with a convenient representative. The exact `PairDelayBridge.palindrome_iff_bad` interface supplies safety at positive times one and two. Initial nonpalindromicity is not an assumption or conclusion.

The separate `realized_safe_gate` endpoint invokes `valid_word_realizable` using the newly established admissibility of the initial pair word. Thus its existential conclusion is nonvacuous and does not retain a hidden realizability premise. The arbitrary-realization theorem and this existence theorem serve distinct purposes.

For the double gate, the old Group I parameters `(p,u,v)=(1,1,6)` return to the actual Group II input `(4,5,5)` after two steps. `numeric_handoff` retains the original integer and obtains canonical digits for its real time-two iterate. `numeric_four_return` and `numeric_four_step_safety` then apply Group II to that iterate, using the actual orbit composition law. They do not assert that the time-four state returns to the original domain or yields an infinite recurrence.

## Finite-prefix scope and composition

The repository's pair dynamics use total functions `Nat -> Nat`, but representation and return lemmas state equality only inside the current width. An endpoint written as `G^2(Q)=Phi_1(G^2(A))` must use finite words or explicitly zero-extend the represented component. Applying bare `shiftOne` to the total `iterPairs` function at the whole word's new last index would read a component coefficient outside its represented width. The explicit supported `returnedComponent` avoids that issue.

The frozen DoubleGate module includes `two_steps_from_matching`, which transfers two actual steps using only equality of represented prefixes and proved terminal carry values. It does not require equality of irrelevant infinite tails. The new `component_three` theorem identifies the actual time-three component prefix with `component r 8 10 10`; `whole_three` identifies the corresponding whole word. The witness in `time_three_overlap_fails` is column `r+1`, strictly inside both widths, so the second departure is a genuine difference of the actual finite states. Together with the old first departure and the exact time-two and time-four returns, this establishes two finite departure/repair events.

## Defect mechanism and the precise exclusion

The Defect module uses signed `Int` differences. The coefficient difference between the actual middle word and the redundant comparison word is `(1,-19,-18,-19,1)` across the five central columns. After decimal carry normalization, the digit difference is `(1,1,0,-1,-1)`. This normalized difference is antisymmetric within width `2*r+7`, and therefore cancels in the next reflected column sum. The terminal carry of each comparison word is separately proved zero before using the no-overflow column formula. These are finite-width identities; no tail equality or actual trajectory of the redundant word is presumed.

The redundant comparison word is not an ordinary pair-sum state. Its central coefficient is `4*v`, at least 20 in Group II, while admissible pair sums are at most 18. `redundant_not_admissible` makes this obstruction explicit. The raw carry recurrence remains defined for those natural coefficients, and `redundantCarry` correctly allows the value 2. The proof never invokes the admissible-word ordinary realization bridge for this comparison word.

`returnedComponent_not_same_shape` excludes exactly equality with any `component r p' u' v'` on width `2*r+6`, with the same spacer `r`. Its witness is index `r`: the returned six-column shape has coefficient 1 there, while every member of the original four-column template has coefficient 0. Only `r>=1` is needed for this formal shape inequality. The theorem does not exclude a family at another width, another overlap shift, later returns, cycles, or an infinite trajectory. In particular, this statement must not be summarized as a general impossibility of further overlap repair.

## Independent finite diagnostics

The separate Python program constructs a canonical ordinary integer with each prescribed initial pair word and uses `n + int(str(n)[::-1])` for the primary trajectory. It compares the actual integer digits and pair words against a separately implemented grade-school carry normalization and against the written closed forms.

All 868 Group II controls passed: every seven-core/four-exterior combination for spacers 1 through 30 and 100. Another 31 controls passed for the Group I to Group II handoff, with overlap equality at times 0,2,4, failure at times 1,3, and all four positive ordinary outputs nonpalindromic. These primary controls used 3,720 ordinary additions. They verify only these finite inputs and do not prove the all-spacer statements.

The complete source, log, compact summary, and deterministic gzip payload are preserved beside this review. The gzip payload decompresses exactly to the complete 6,415,049-byte JSON trace. Its decoded SHA-256 is `bfffaab5af4b75fb622ca5458040df2fad367a5e83c088545cf470f3fe03045b`; the 110,090-byte stored gzip SHA-256 is `4cc42b595a29b15dbb8de1e9df72382112dd0091ff2b05d54bd3b3523447d99e`.

## Review disposition

No source-semantic defect remains in these four frozen modules. The review pins match the parent's final hashes exactly. Universal parameter and arbitrary-realization claims have the intended quantifiers; the shortest spacer is handled explicitly; the raw redundant comparison is distinguished from admissible states; the shape-exclusion theorem is limited to its stated spacer and width. Lean execution and axiom evidence remain a separate audit record supplied by the parent and runtime specialist. Finite diagnostics and source inspection do not replace that execution evidence.
