# Agent #10: bounded carry-history observability

## Status and scope

The checked `ActualCarryObservability.lean` proves that **ten complete consecutive carry words determine the initial mirrored pair-sum word, at every positive decimal width**. The checked local follow-up `DifferenceObservability.lean` strengthens this to **nine** by controlling neighboring coefficient differences; its publication and combined audit are tracked in issue #9. The statements concern ordinary reverse-and-add, continued after palindromes. They do not supply a predictable carry history, a closed safe language, or a proof about the infinite orbit of 196.

The original integer is not determined: 196 and 295 have pair word `(7,18,7)` and both map to 887. The pair word determines the next integer exactly, and therefore the entire subsequent ordinary trajectory.

There is an explicit six-observation collision: 917 and 908 have different initial pair words but the same complete carry words at times 0 through 5. They differ at time 6. Both trajectories encounter a palindrome at time 2, so this is a lower bound for continued dynamics, not for histories restricted to safe states. With the nine-word strengthening the optimal universal memory lies in **[7,9]**; optimality is not claimed.

This is AI-assisted research, extending the repository's existing eleven-word theorem and its first-discrepancy argument. No claim of literature novelty or independent human review is made.

## 1. Definitions and exact local relation

Write the input digits in least-significant-first order as `d_0,...,d_(L-1)` and set `q_i=d_i+d_(L-1-i)`. Thus `q` is symmetric, each coefficient lies in 0..18, its outside coefficient is positive, and an odd-width center is even. These conditions are exactly realizable by a positive ordinary integer.

The complete carry word is `(c_0,...,c_L)`, where `c_0=0` and `c_(i+1)=floor((q_i+c_i)/10)`. It includes the final overflow bit. The output digits are `e_i=q_i+c_i-10c_(i+1)`; append the digit 1 if `c_L=1`. Its mirrored sums are the next pair word.

For `L>=2`, let `p=q_0`, `z=q_1`, and `v=c_(L-2)`. Set

```
a = floor(p/10)
u = floor((z+v)/10)
b = floor((z+a)/10)
h = floor((p+u)/10).
```

Here `a=c_1`, `u=c_(L-1)`, `b=c_2`, and `h=c_L`. The exact next outside pair is

```
h=0: (2p+u-10a, 2z+a+v-10(b+u));
h=1: (p-10a+1, p+z+a+u-10(b+h)).
```

These formulas remain valid when the observed columns overlap, including widths two and three. `prefix_step_exact` and `prefix_overflow` prove the relation for the actual all-width map, not just for a freely selected control sequence.

Allowing `v` to vary freely gives a necessary finite graph with 342 states `(p,z)` and 684 controls. Its edge cost is `1-h`, the nonoverflow indicator. It is an overapproximation: an arbitrary graph path need not lift to a whole integer orbit.

## 2. Nine transitions force four nonoverflows

Define `m_0(s)=0` and

```
m_(k+1)(s)=min_v(1-h(s,v)+m_k(next(s,v))).
```

The exact graph minima for horizons 0 through 9 are

```
0,0,0,0,1,1,2,3,3,4.
```

The finite certificate stores `min(4,m_k(s))` for `1<=k<=8` in three-bit entries of a natural number. The proposed values are untrusted input: `rank_step_fin` checks all **6,156** local inequalities in the Lean kernel, and `next_valid_fin` checks graph closure. Generic induction then proves that every nine-edge path has cost at least four. The production proof uses `decide +kernel`, not `native_decide`.

Actual-orbit inclusion transfers this bound to every starting width at least two. The width-one case is checked separately on all 18 possible positive single coefficients, a superset of the admissible even centers. Finite-prefix congruence proves that irrelevant function values outside the actual width cannot affect this check. Thus every positive admissible decimal orbit has at least four nonoverflow steps in its first nine additions, and the same result applies on any tail by restarting at that state.

The counting horizon cannot be shortened to eight: the actual input 936 has overflow schedule `1,0,1,0,0,1,1,1`, hence only three nonoverflows. This does not prove that ten observations are necessary for reconstruction.

## 3. Ten-word reconstruction

Consider two equal-width trajectories with equal complete carry words. Let `D_t(x)=Q_t(x)-R_t(x)` be the difference of their pair-sum polynomials, zero-extended outside their actual width. Equal carries imply equal subsequent widths and cancel all affine carry contributions. Therefore

```
D_(t+1)=2D_t                 for a nonoverflow step;
D_(t+1)=(1+x)D_t             for an overflow step.
```

Consequently `D_K=2^N(1+x)^H D_0`, where `N+H=K`.

If `D_0` is nonzero, its least nonzero coefficient is a nonzero integer. Multiplication by `(1+x)` preserves that coefficient; each nonoverflow doubles it. At a time with an equal carry word, the column equation identifies the coefficient difference with a difference of two decimal output digits, so its absolute value is at most 9. Four preceding nonoverflows would give absolute value at least 16, a contradiction.

The nine-step count bound supplies those four nonoverflows before the tenth observed carry word. The formal proof reuses the existing `CarryHistory.iterPairs_endpoint_carry_history_injective`; it does not silently assume an unverified growth statement.

## 4. Nine-word strengthening by neighboring coefficients

Eight steps contain at least three nonoverflows: append one step and apply the checked nine-step bound, noting that the extra step contributes at most one.

Four or more nonoverflows again prove equality immediately. The remaining case has exactly three nonoverflows and five overflows. Thus

```
D_8=8(1+x)^5D_0.
```

Equal carries initially imply every coefficient of `D_0` lies in `[-9,9]`. Equal carries at time eight imply that every coefficient of `(1+x)^5D_0` is an integer in `[-1,1]`.

This is impossible for a nonzero integer series with coefficients bounded by 9. Shift to its least nonzero coefficient and, after changing sign, call the next coefficients `a,b,c,d`, with `a=1`. The first four smoothed coefficients are

```
a,
5a+b,
10a+5b+c,
10a+10b+5c+d.
```

Their unit bounds force `b` into `{-6,-5,-4}`. The third coefficient bound together with `c<=9` forces `b=-4,c=9`. The fourth expression is then `15+d`, which cannot lie in `[-1,1]` because `d>=-9`. Contradiction.

This argument does not require a degree bound, a search cap, or a prescribed carry schedule beyond the count. The formal source defines zero-extended differences and proves the complete difference recurrence, including the newly created overflow column. A general smoothing identity and strong induction handle the least coefficient without assuming enough room remains inside the original word. The final theorem is `DifferenceObservability.nine_carry_words_determine_pair_sums`; the numeric consequence identifies the next ordinary integer.

## 5. Exact decoder

The published direct decoder takes a supplied carry history at times `0,...,K`. It validates bit values, initial zeros, and width progression. The affine recurrence is

```
Q_K=2^N(1+x)^H Q_0+R_K,
```

where `R_K` is computed solely from the supplied carries, using the actual overflow reflection width. At endpoint column `i`, the possible pair sum belongs to

```
[max(0,10c_(i+1)-c_i), min(18,10c_(i+1)+9-c_i)].
```

This interval has width at most nine. When `2^N>9`, coefficients of `Q_0` are recovered from the outside inward: subtract already recovered lower-coefficient contributions and intersect the resulting interval with the integer lattice of spacing `2^N`. There is at most one choice. Canonical realizability and a complete exact-history replay are then required before returning a candidate.

The direct implementation is guaranteed to accept every genuine ten-word decimal history. It may report `InsufficientObservations` on a shorter uniquely identifying history: that exception describes the multiplier criterion, not actual ambiguity. The algebraic implementation also supports bases at least two whenever its explicitly tested multiplier exceeds `base-1`; no uniform ten-word bound in other bases is asserted.

For a fixed observation count, the direct decoder takes linear time and space in initial width. There is no integer-digit-splitting enumeration. The nine-word theorem suggests a constant-depth lookahead extension in the remaining multiplier-eight case; its implementation is a separate follow-up, not a claim about the currently published direct decoder.

## 6. Exact controls, trust boundary, and reproduction

The direct decoder passed all **198,909** canonical decimal pair words of widths one through eight. The independent integer oracle checked **1,989,090** ordinary transitions and **1,989,074** applicable actual-prefix transitions. Additional deterministic controls include 1,000 decimal words through width 500, 1,500 conditional decoder inputs in bases 2 through 16, malformed inputs, and all 40 internal single-bit mutations of the tested 196 history. The last experiment is not an error-correction guarantee.

Complete fixed-width collision partitions have no remaining ambiguity at seven observations through width eight. This bounded fact is not an all-width seven-word proof.

Exhaustive case-stream SHA-256:
`e161261deadeb9d069778605c36de53c53ff14e818b09e3d0f613ff0724e9d09`.

The pinned integrated core is `proofs/research/Lychrel196Research.lean`, SHA-256
`f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c`.
The compiler is official Lean 4.19.0, commit `6caaee842e94`. The distribution SHA-256 is
`6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.
Agent #5 supplied the reusable compiler bootstrap via Actions artifact 11948452826. The mathematical proof does not depend on an artifact or a network service after compilation.

Compile the integrated core once, then the production modules in dependency order with the corresponding source directories on `LEAN_PATH`. Do not import the historical `resume_*` modules alongside the integrated core: their declarations are already incorporated and cause duplicate-definition build errors.

The first production pair has 27 new theorem declarations and a fresh isolated rebuild with complete transitive axiom audits; its final conclusions use only `propext` and `Quot.sound`. The nine-word follow-up has 13 additional declarations, with the standard logical axioms `propext`, `Classical.choice`, and `Quot.sound`. There is no `sorry`, custom axiom, or compiler-trusted finite theorem in the accepted source. This is not a claim that every other repository module was audited in this session.

## Remaining research

Determine whether seven or eight complete observations always suffice, or construct a longer exact collision. The five-smoothing rigidity argument fails for four smoothings: bounded nonzero difference filters exist, so another ingredient is necessary. A difference-filter candidate alone need not lift to two actual equal-carry integer trajectories. Improve the practical decoder to use the nine-word theorem, and investigate histories restricted to palindrome-avoiding states. None of these tasks is replaced by a claim about the unresolved orbit of 196.
