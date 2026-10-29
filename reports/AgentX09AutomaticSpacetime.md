# X09: automatic spacetime certificates beyond finite-period centre grammars

**PAPER PROOF (conditional soundness/decidability of a new certificate format)**, with COMPUTED controls. **No decimal certificate**, and no theorem that 196 is Lychrel. The new invariant is an entire infinite two-coordinate spacetime array, not a regular language of individual pairwords or a finite-horizon substitution tile.

## 1. An explicit new format

Fix a base `b >= 2`. Supply finite deterministic synchronous binary automata for the following total/partial relations on natural-number tuples, with padded binary inputs read from least-significant bit to most-significant bit:

- `Len(t,n)`: the unique positive integer `n=L(t)` is the number of base-b digits at time `t`.
- `Digit_a(t,i)` for each `a=0,...,b-1`: the unique digit `a=d(t,i)` for `0<=i<L(t)`.
- `Carry_c(t,i)` for `c=0,1`: the unique normalisation carry `c=c(t,i)` for `0<=i<=L(t)`.

There is **no periodicity restriction in time**, no fixed-width centre, and no condition that the infinite digit array itself be a regular language under concatenation. The binary-index automata may distinguish `t&i` bit patterns, arbitrarily nested dyadic spatial intervals, and moving interfaces. The automata are finite certificates even if the lengths and structures they describe grow without bound.

## 2. Exact finite decision conditions

Form the following first-order constraints over nonnegative integers and binary-automatic predicates. All arithmetic except multiplication by the **fixed constant** b is addition, order, equality, and multiplication by constants. Set `n=L(t)`, `j=n-1-i`, `x=d(t,i)+d(t,j)+c(t,i)`.

1. `Len` is total and single-valued; `n>=1`; `Digit` and `Carry` are total and single-valued **inside** their indicated index domains; the leading digit satisfies `d(t,n-1)>0` for every `t`; and the supplied seed digits at `t=0` encode a given positive integer N.
2. For every `t`, `c(t,0)=0`, and every `0<=i<n` has `x=b*c(t,i+1)+d(t+1,i)`, with `d(t+1,i)` understood as an output digit (the next length is at least n). The bound `0<=c<=1` is checked by the Carry alphabet. This is exactly low-to-high normalisation of N + reverse(N).
3. For every `t`, `L(t+1)=n+c(t,n)`. If the final carry is 1, then `d(t+1,n)=1` (the overflow digit). If it is 0, the top ordinary output digit is already constrained by (2) and canonicality. Every digit of time t+1 lies in the prescribed range, so nothing is left unconstrained.
4. For every `t` there exists `i<n` with `d(t,i) != d(t,n-1-i)`. Equivalently, no pairword can be entirely even-paired in the stronger witness format; the direct inequality is the exact condition and does not need parity.

These are all **decidable, finite automata tests**. Encode `(t,i,j,n)` in synchronously padded binary. Relations `i+j+1=n`, `t'=t+1`, multiplication by fixed b and inequalities are regular relations. Preimages under conjunction are automata products; complement handles universal quantification; projection handles existential quantification. Construct automata recognizing violations of each item. A certificate passes if all are empty, with a finite initial-seed membership check. Automata determinization/projection may be expensive, but the procedure terminates for every supplied finite tuple of automata. No finite time bound is used in this decision.

## 3. Soundness theorem and proof

**Theorem (PAPER PROOF).** If the automata pass (1)--(4), then the base-b integer N encoded at time zero never attains a palindrome under the standard reverse-and-add operation. Proof: fix any t and use (1) to obtain exactly n canonical digits. Induct on i in (2), starting from `c(t,0)=0`, to show the output digits are precisely those of N_t + reverse_b(N_t) before possible leading overflow. Bound `c<=1` and (3) supply exactly the one possible new leading digit, with no other new positions. Thus the digit word at t+1 represents the actual arithmetic successor. Induction on t produces the genuine orbit for all t; (4) excludes palindromes at each t. This is a pure arithmetic induction plus finite-state inclusion, not a claim that any decimal automaton passes.

**Lean sketch.** Define `AutoPred : (Fin k -> Nat) -> Prop` from a DFA over synchronized binary tracks; separately prove `regularAdd`, `regularLt`, Boolean closure and projection. Build an executable `bad` product automaton for each negated axiom. Once `empty_bad = true` is certified by an explicit finite reachability search, prove all instantiated axioms. Define `d : Nat -> Nat -> Fin b`, `len`, `carry` from functional predicates, and prove `step_eq` by carries induction; then `forall_t_not_pal` by t induction. Lean must check the automata directly; no `native_decide`, `sorry`, or bespoke axioms.

## 4. Why this is different from earlier formats

N09/N04/N07 describe regular *languages of folded pairwords* and demand successor-language inclusion. N03 uses path-return substitution loops with a centre bridge of eight time steps. N15 has an infinite spatial dyadic family but only a finite time slab (18 steps). This format instead requires a two-dimensional **automatic relation** on time and position, potentially with no temporal period and with moving boundaries: a single pair of coordinates indexes every state and every carry for all time. This is not a verified decimal model. A two-state synchronous DFAO for `popcount(t & i) mod 2` demonstrates the expressiveness: it realizes the classic scale-changing binary Sierpinski pattern on all `(t,i)`. The accompanying checker exhaustively cross-validates 65,536 coordinate pairs against Python popcount. The pattern alone is **not** a reverse-and-add orbit.

A plausible synthesis target is a decimal p8 exterior with its phase-dependent periodic carry cells, joined to a dyadic or automatic (not fixed-width) central regeneration cone. The search variables become finite digit/carry automata, and counterexamples are specific `(t,i)` coordinates emitted by emptiness checking. The hard remaining task is finding even one **base-10 satisfying instance**; general decidability does not imply one exists.

## 5. Computed data and stress tests

An independent C++ digit-array replay from 196 was carried to t=100,000; no palindrome occurred in any state t=0..100,000. The final string is 41,490 decimal digits with SHA256 `c1855622b791d153520ff5bd39e539fd3d04832e21258d59c46f399acbfd2511`; a separate Python arbitrary-precision integer implementation agrees at t=2,000. The half pairwords at t=10k,20k,40k,80k,100k have lengths 2,079,4,148,8,316,16,614,20,745. At t=100k, LZ78 finds 6,214 phrases (max length 6) versus 6,316 (max length 5) after a frequency-preserving shuffle; gzip ratios are 0.59007 versus 0.59585. This is weak compression evidence, not a statistical proof of incompressibility. Ordinary flat LZ78 did **not** expose a compelling substitutive infinite-time grammar. Thus the search is redirected to the typed spacetime carry automata rather than generic LZ extrapolation.

For a known positive **base-9 control** (existing Lean-verified `LatticeBand.Base9`), the separate test builds its 10-phase pairword `P_t=B_(t mod 10) ++ (W_(t mod 10)^inf)[:2+4*floor(t/10)+prefixGam] ++ reverse(B_(t mod 10))`, with 61-column B and spatial-period-4 W. This family is explicitly definable in Presburger arithmetic and hence binary-automatic. Using the repository's existing `cert_b9_rec0.json`, two independently coded digit/normalization algorithms agree with the asserted phase and length for 2,000 transitions, 16 of them with independent integer/divmod checks. This is a **format positive control**, not a new base-9 discovery or a completed base-10 certificate. The full automatic-model-checker and the explicit DFA encodings of this control are not implemented here; they are the next implementation targets.

Files and reproduction: `calculation/new_structures/agent-X09/{README.md,orbit.cpp,grammar_probe.py,automatic_spacetime.py,summary.json}`. Run the commands in README. No files from another agent were modified.