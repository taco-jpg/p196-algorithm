# Independent Incoming review

**Result: PASS for the fixed mathematical sources and the incremental source build described here.**

Reviewer: the genuine runtime delegate of Agent #108, session b31b8818. The reviewer did not author or edit `Agent108WindowIncoming.lean`. The reviewer did author its Obstruction and Embedding dependency modules; this is disclosed same-session nonauthor review of Incoming, not external-account peer review or independent authorship of every dependency.

The fixed Incoming source SHA256 is `8929758722b9d66c327654bb182c011b072be6aec100f801349e70040a65b5f6`.

## Build and declaration coverage

All ten Agent108 window modules were copied into one newly created empty directory and compiled in dependency order with official Lean 4.19.0 `--trust=0`. A separate module-origin audit was compiled afterward. All eleven commands exited 0. No previously built Agent108 window object was on the search path.

The original Agent13 foundation was reused from its previously independently rebuilt, source-pinned closure at commit `12a32789056f5eec8247166564ac2ef745c3c9d6`. Mathlib was reused at `c44e0c8ee63ca166450922a373c7409c5d26b00b`. This review did not rebuild those foundations or claim that a bare clean repository currently restores them automatically. Repository dependency materialization and canonical entry-point verification are separate packaging gates.

The audit enumerated 363 declarations by their actual Lean source module, including generated names. It classified 269 safe nonpartial declarations, 90 unsafe implementation declarations, and 4 partial implementation declarations. Every safe nonpartial declaration received an individual literal `#print axioms` report. All transitive axiom sets are subsets of `propext`, `Classical.choice`, and `Quot.sound`; no implementation axiom was added to that allowlist.

All 130 explicit source definitions and theorems have a one-to-one source/module/declaration/axiom correspondence. Incoming has 18 explicit source declarations: 16 public and 2 private. The two private helpers were inspected and separately audited by their real private declaration names. All ten original source hashes were unchanged after the run.

The exact source snapshots, full stdout/stderr, audit program, commands, source hashes, declaration metadata, and correspondence are retained in `attempts/001` and `latest-verification.json`. No failed run occurred in this independent Incoming review.

## Fixed source closure

| Module | SHA256 |
|---|---|
| Agent108WindowDefs | `147ae208dce3b612c6eb23091eab123b77bd46c86d216ab8a6199913015f0aa0` |
| Agent108WindowEmbedding | `1acb5964188bcb7828bec58cbd8b5328ff9d68467e5951eb3a4bf87d78eb4e7f` |
| Agent108WindowProducts | `2920c9da6e3c06c40a1d8478fe1af0d87b00627976f53856f75b90de32a1e584` |
| Agent108WindowWeights | `5bc7f457187ad0af4a4f7a340acf7f827b8e89537d73624519805d232c762eae` |
| Agent108WindowFamilyProducts | `d4449500c98887a82dca222af318e8d99e8ef0d1ad5e58719658406c1650fdc8` |
| Agent108WindowEndpoints | `ebabfbfd366729846656ff5a56891c22f9c7f0868fca9c5918be433e5d5fbc22` |
| Agent108WindowEndpointWeights | `21355018606cf7c2cfe8c33a008be815bd546bbafc31be69bc428624de0acab1` |
| Agent108WindowObstruction | `0dd91993667dddac3740ccadd7b2764cc2e6122121f19bd0a8354a9e0507a90a` |
| Agent108WindowFamilyRatio | `051dcb42849d9cffb2fec0de77af138b6d7d6c415ff27d65725dcdf9cfcf7afc` |
| Agent108WindowIncoming | `8929758722b9d66c327654bb182c011b072be6aec100f801349e70040a65b5f6` |

## Every Incoming source declaration

| Declaration | Visibility / kind | Transitive axioms |
|---|---|---|
| `finiteWindowWeight` | public def | propext, Classical.choice, Quot.sound |
| `finiteStateHalf_bounded` | public theorem | propext, Quot.sound |
| `finiteWindowWeight_pos` | public theorem | propext, Classical.choice, Quot.sound |
| `finiteWindowWeight_partial_sum_le_incoming` | public theorem | propext, Classical.choice, Quot.sound |
| `choiceBits` | public def | none |
| `ofFn_bitsFromList` | private theorem | propext, Quot.sound |
| `choiceBits_ofFn` | public theorem | propext, Quot.sound |
| `choiceBits_injective` | public theorem | propext, Quot.sound |
| `sum_choices_get` | private theorem | propext, Classical.choice, Quot.sound |
| `embeddedState_window_weight` | public theorem | propext, Classical.choice, Quot.sound |
| `embeddedTarget_window_weight` | public theorem | propext, Classical.choice, Quot.sound |
| `embedded_choice_weight_sum` | public theorem | propext, Classical.choice, Quot.sound |
| `embedded_window_family_le_incoming` | public theorem | propext, Classical.choice, Quot.sound |
| `actual_window_family_total` | public theorem | propext, Classical.choice, Quot.sound |
| `incoming_window_lower_bound` | public theorem | propext, Classical.choice, Quot.sound |
| `incoming_window_ratio` | public theorem | propext, Classical.choice, Quot.sound |
| `no_uniform_window_multiplier` | public theorem | propext, Classical.choice, Quot.sound |
| `not_exists_uniform_window_bound` | public theorem | propext, Classical.choice, Quot.sound |

## Mathematical and semantic review

### Original full safe fiber

Incoming retains the original `FiniteWord`, `SafeState`, `MapsTo`, `safeFiber`, and `incoming` definitions. The state space is finite coefficient words with their exact declared width; equality does not identify different widths. The original `stateBox target.width` enumerates every coefficient function at every width up to the target width. `mapsTo_width_le` proves that every actual predecessor fits in this box. Filtering it by `SafeState` and `MapsTo` therefore gives the full actual safe fiber, rather than only the selected family.

The incoming sum includes overflow predecessors and odd source widths. There is no equal-width restriction on the full fiber. Equal even widths are proved only for the selected embedded subfamily. The theorem counts coefficient states as specified by the original operator; it does not assert one coefficient state is one distinct ordinary integer.

### Weight domain and positivity

At positive even width the weight is the arbitrary width factor `A L` times the product over complete unpadded `(b+1)`-windows of the first half. Since `b` is natural, every supported window width is positive and the `b=0` case is width one. `PositivePotential` is required only on legal windows of that exact length with coefficients at most 18. The bound on the extracted half follows from the original finite-state digit bound. Short halves give the empty product, which is positive.

The hypotheses require `A L>0` only at positive even widths, and require the arbitrary `oddWeight` extension to be positive on every safe odd-width state. These hypotheses make all terms in the original safe fiber nonnegative, which is precisely what the partial-sum inclusion uses. No missing odd-width term is discarded, and values on non-safe states or at unused width zero do not enter the argument.

### Selected family and exact enumeration

`choiceBits` reads the finite list `choices r` at index type `Fin (choices r).length`. Its inverse list identity follows from the proved exact length of each choice, so default values outside a list cannot erase a valid choice bit. `choices_nodup` and that inverse identity prove `choiceBits_injective`. Composing with `embeddedState_injective` establishes genuinely distinct selected finite states. The private finite-sum helper transports this same enumeration to the literal list sum, with no multiplicity change.

For every selected index, the original `familyState_spec` supplies actual safety and `MapsTo` to the displayed common target when `k>0`. The exact half-word equalities and equal widths identify each actual selected weight with the literal window weight and a common `A` factor. Taking `p=b+1` gives physical buffer `4*(b+1)=b+(3*b+4)`, precisely matching the independent extra-buffer parameter in the weight formula.

### Constants, total, and quantifiers

`actual_window_family_total` is an equality for the actual selected states. It uses the proved literal family sum and needs potential positivity for the ratio denominators. It does not need `k>0` or positivity of `A`, because it does not itself assert safety or divide by the actual target weight. The incoming lower bound adds the necessary `k>0` and global safe-state positivity hypotheses.

The actual target is safe and has strictly positive weight, so division in `incoming_window_ratio` is valid. The common even-width factor cancels exactly, even if it varies arbitrarily with width. The final obstruction fixes `k=1`, leaving the positive endpoint constant and positive insertion factor independent of `r`. As `r` varies, the proved geometric family lower bound exceeds every proposed real multiplier.

`no_uniform_window_multiplier` produces an actual `SafeState` target for each real `K`. `not_exists_uniform_window_bound` then negates existence of one real multiplier valid on every safe target for the fixed chosen window width, width factor, potential, and odd extension. This is not an interchange of the potential and target quantifiers and does not require a bound uniform over different potentials.

### Limits of the result

The proof rules out finite real uniform incoming multipliers for this positive, translation-invariant fixed-window class on the original folded safe-state operator. It does not address signed or vanishing potentials, position-dependent or unbounded-window weights, an orbit-specific bound, an infinite safe orbit, or the 196 existence problem. The original arithmetic representation theorems are reused without a new carry proof.

No mathematical correction to the fixed Incoming source was required. Repository-level dependency restoration and verification through the canonical build entry point remain distinct from this successful source-pinned incremental build.
