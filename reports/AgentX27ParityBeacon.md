# X27: finite parity-beacon replay and one-input carry-prefix format

**Status: COMPUTED** for the decimal replay; **PAPER PROOF** for the generic arithmetic identities and the conditional format. **Not an infinite certificate.**

## Seed and independently checked facts

The ordinary decimal integer `N_0 = 1 (99)^47 6` has 96 digits, symmetric digit-pair coefficients `P_0=7`, `P_i=18` for `1<=i<=94` and `P_95=7` (least-significant-first, zero-based indexing). For each `t`, write `N_t` in canonical decimal digits `d_0,...,d_(n-1)`, let `P_i=d_i+d_(n-1-i)` for all `0<=i<n`, and set `F_k(N_t) := exists i < min(k,floor(n/2)), P_i odd`.

`verify.cpp` independently runs (1) literal-digit schoolbook decimal addition with an explicit one-bit carry, and (2) GMP arbitrary-precision integer addition after converting/reversing an independently generated decimal representation. Both engines are compared at **every state t=0..20000**, not just sampled checkpoints. At every step, the program also checks every resulting pair parity against the two-sided carry identities below and all 16 resulting prefix coefficients against the separate boundary transducer. All states have `F_16`; hence none is palindromic. The exact output at `t=20000` is 8,343 digits and mod 1,000,000,007 = 954753461. The first odd-pair index never exceeds 15 over these 20,001 states.

`longrun.cpp` extends the *literal-digit engine alone* through `t=100000`. Every state has `F_32`; the largest earliest-odd index is 25. Exactly 18 states fail `F_16`; first at `t=24456`. The scan sees no state with an all-even pairword, much less a palindrome. The longer test is explicitly **not independently replayed by GMP**.

## Exact carry-parity law (base-generic)

For base `b>=2` (the code instantiates `b=10`), let `P_i=d_i+d_(n-1-i)`, let `c_0=0`, `c_(i+1)=floor((P_i+c_i)/b)`, `e_i=P_i+c_i-b*c_(i+1)` and `g=c_n in {0,1}`. The next integer has digits `e_0,...,e_(n-1)` and, iff `g=1`, a new leading digit `1`.

If `g=0`, the new pair coefficients satisfy
`P'_i = (P_i+c_i-b*c_(i+1)) + (P_i+c_(n-1-i)-b*c_(n-i))`.
In even base, reduction modulo 2 gives `P'_i = c_i+c_(n-1-i) (mod 2)`; for odd base, use the full integer formula, not this parity simplification.

If `g=1`, `P'_0=e_0+1` and, for `1<=i<floor((n+1)/2)`,
`P'_i = (P_i+c_i-b*c_(i+1))+(P_(i-1)+c_(n-i)-b*c_(n-i+1))`.
In even base, these reduce to `P'_0=P_0+1 (mod 2)`, `P'_i=P_i+P_(i-1)+c_i+c_(n-i) (mod 2)`.

**Warning:** for odd `n=2m+1`, the actual middle `P_m=2*d_m` is always even, for *any* integer and any base. A proposed odd middle coefficient is impossible. The workable centre-adjacent witness is an off-middle odd coefficient, or an odd central pair when length is even. For the 20,001 replayed states, exactly 4,087 even-length states have an odd central pair. The obstruction here is deliberately peripheral, not central.

## Core-independent prefix transducer: a precise conditional format

Let `k<=floor(n/2)`, and let `p=(P_0,...,P_(k-1))`. From this alone compute low incoming carries `L_0=0`, `L_(i+1)=floor((p_i+L_i)/b)` for `0<=i<k`. Guess **one high incoming carry** `h_(k-1)=eta in {0,1}`, corresponding physically to `c_(n-k)`; then compute `h_(i-1)=floor((p_i+h_i)/b)` for `i=k-1,...,1`. Let `gamma=floor((p_0+h_0)/b)`. The actual overflow is `gamma` for the physical `eta`.

Define the successor prefix `q` of length `k` via

- `gamma=0`: `q_i=(p_i+L_i) mod b + (p_i+h_i) mod b` for all `0<=i<k`.
- `gamma=1`: `q_0=(p_0+L_0) mod b + 1`, and `q_i=(p_i+L_i) mod b + (p_(i-1)+h_(i-1)) mod b` for `1<=i<k`.

All sums above denote sums of *digits*, not addition modulo `b`. Direct indexing of both ends in schoolbook reverse-and-add proves exactness for any centre and any length `n>=2k`, including when `n` increases by one. It does not assume a periodic centre, absorbing band, fixed overflow stream, or anything about `P_i` for `i>=k`. This gives a **one-input nondeterministic finite prefix graph** on the alphabet `{0,...,2b-2}^k`, with at most two successors per vertex.

**Soundness criterion:** If a finite set `S` of prefix states contains the seed's first `k` coefficients, (i) is closed under *both* `eta=0,1` transitions, and (ii) each `p in S` has an odd coefficient, then every step of the genuine base-10 orbit (for any seed with at least `2k` digits and initial prefix in `S`) is nonpalindromic. Proof: `n_t` never decreases, the physical entering carry is one of the two quantified values, so induction puts every prefix in `S`; a palindrome has every digit-pair sum even. If the prefix graph is restricted by proven centre-to-boundary carry constraints, replacing the both-eta closure with those proven constraints is also sound.

This is a *format theorem*, **not** a closed finite decimal `S`. Unrestricted-eta breadth-first search from `(7,18^(k-1))` reaches an all-even state at depth 9 for `k=4`, depth 32 for `k=8`. For `k=12,16,24,32`, a cap of 500,000 states is reached without a conclusion (the generator's queue order and counters are documented in its output). It is unsafe to promote 100,000 empirical steps to an all-time claim. Next viable direction: constrain the single entering carry by a structured renewal/core stream, instead of accepting every counterfactual carry branch.

## Reproduction and scope

Run `bash calculation/new_structures/agent-X27/reproduce.sh`. The 20,000-state cross-check requires C++17 plus GMP and the 100,000-state audit requires C++17 only. `prefix_abstract.py` is a pure Python3 graph implementation; it computes exact transitions but its depth/cap outcomes are not no-go theorems.

Not claimed: actual 196, a periodic terminal template, a self-contained decimal infinite certificate, a new Lean-verified theorem, or any statement that 96 digits is a globally smallest seed. All 100,000-step statements are finite and conditional only on literal-digit computation.
