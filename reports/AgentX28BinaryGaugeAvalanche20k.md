# Agent-X28: binary carry-gauge lift and a 20-step decimal band phase change

**Status.** The carry-coboundary identity and the soundness of the affine symbolic checker have **PAPER PROOF** below. Its concrete 20,000-step run and two independent ordinary-number controls are **COMPUTED**. No Lean proof or infinite decimal Lychrel certificate is claimed.

## 1. A carry-preserving but *not* digit-preserving base change

Let `b>=2`, `k>=1`, and `B=k(b-1)+1`. Let `D=(d_0,...,d_{L-1})` be a canonical base-`b` number, written least-significant first, and define the base-`B` number `E_k(D)` with digits `k d_i`. (The leading digit stays nonzero.) Write `q_i=d_i+d_{L-1-i}`, and let `c_0=0`, `c_{i+1}=floor((q_i+c_i)/b)` be the carries in the base-`b` reverse-and-add step. The corresponding lifted sums are `k q_i`. The carry map at *any* column sum `q` has three branches:

- `q <= b-2`: outgoing carry zero for both incoming bits;
- `q = b-1`: outgoing carry equals incoming carry;
- `q >= b`: outgoing carry one for both incoming bits.

Indeed `kq+c < B` in the first branch, `kq+c = B-1+c` in the second, and `B <= kq+c < 2B` in the third. Hence the base-`B` carry history is **exactly the same** `c_i` for every input and every length. Let `e_i=q_i+c_i-b c_{i+1}` and `E_i=kq_i+c_i-B c_{i+1}` be normalized output digits. Their precise difference is

`E_i = k*e_i + (k-1)*(c_{i+1}-c_i)`.

Both output lengths are `L+c_L`. When `c_L=1`, both arithmetic outputs append the *same digit 1*, which is **not** multiplied by `k`. Thus this is a carry coboundary, not a conjugacy of complete orbits; the delta term vanishes exactly at columns where the carry bit is constant. This exact derivative suggests a search representation with a carried binary base word and sparse signed `±(k-1)` shocks at carry transitions. Direct literal binary-digit substitution fails, as documented earlier in `reports/REPORT_209.md` and `reports/REPORT_203.md`; this construction does **not** claim to evade those literal-code obstructions by an infinite embedding.

For `b=2,k=9,B=10`, start with the known binary-family word `W_r=10(1^r)01(0^r)` (`r>=2`) and apply the digit lift: `N_r=90(9^r)09(0^r)`. The first binary carry word changes from 0 to 1 at column `r` and back from 1 to 0 at column `2r+2` (low-first indices). Exactly those two columns generate the `+8` and `-8` changes in the first lifted decimal successor relative to nine times the binary output digits. A localized first-step deviation does not imply that the decimal and binary pairword dynamics will remain conjugate.

## 2. A fully sound affine run-length *finite-horizon* certificate format

A symbolic word is a list of triples `(digit, a, c)` denoting the digit repeated `a*r+c` times. The parameter domain is every integer `r>=R`. The checker requires, for every represented run, `a>=0` and `a*R+c>0`. Its initial low-first word is exactly `(0,r),(9,1),(0,1),(9,r),(0,1),(9,1)`, hence represents all `N_r`, with no truncation or numerical approximation.

For the symbolic one-step map, scan the RLE word from **both** ends simultaneously. If the two current lengths are `u(r)=a*r+c` and `v(r)=a'*r+c'`, choosing `u<=v` is permitted only if `u(R)<=v(R)` **and** `a<=a'`; choosing `v<=u` is permitted only with the opposite two inequalities. These guards make the chosen split valid for *every* larger parameter, not merely one test value. Each aligned run has constant pair coefficient `q` in `[0,18]`. Given incoming carry `c`, compute `c'=floor((q+c)/10)`. Since the decimal carry map is idempotent for constant `q`, the exact resulting output run of length `m>=1` is

`[(q+c) mod 10] ++ [((q+c') mod 10)^(m-1)]`.

Append leading carry 1 exactly when it exists. Adjacent equal output digits are merged, with affine lengths added. Strict positivity and uniform split guards are rechecked on every step. By induction on the number of steps, the next symbolic word denotes the **exact decimal reverse-and-add successor for every integer `r>=R`**. There is no assumption of bounded central width, regular cycle, limit passage, or heuristic interpolation from two sampled lengths.

For each symbolic state, another two-ended scanner compares aligned digits with the *same* universally valid split rules. Encountering an unequal pair proves **all** instantiated words are nonpalindromic. A separate pair-sum scanner checks disjoint long constant-coefficient plateaus. A run qualifying by its value at `R` must also have nonnegative affine slope, so it remains at least that long for all `r>=R`. These operations give a **sound finite-horizon family certificate**: if the finite computation accepts `t=0..T`, then every represented member avoids palindromes through time `T`; it makes no claim for `T+1`.

A Lean route is to define affine lengths as `Int×Int`, prove evaluation of a guarded minimum (`r>=R`), prove the constant-`q` normalizer by cases `q<=8,q=9,q>=10`, then define `rleStep` and show `eval (rleStep S) r = reverseAdd10 (eval S r)`. A Boolean interval checker can then replay the 20,001 symbolic words using `decide +kernel`. That formalization has **not** been implemented and must not be described as LEAN-VERIFIED.

## 3. Concrete result and independent arithmetic

The exact symbolic check accepts `R=14000`, `T=20000`: 312,031,239 paired run-segment transitions; 20,001 all-parameter nonpalindrome checks; no unsafe comparison, length, or overflow guard. At each `t<20`, there are at least two distinct mirrored coefficient-9 plateaus of length at least **13,991**. At each `20<=t<=20000`, there are two distinct mirrored coefficient-0 plateaus of length at least **1,957**. For all `r>=14000`, lengths are `2*r+4` initially, `2*r+13` at `t=20`, and `2*r+8298` at `t=20000`. The shock transition `9 -> 0` at `t=20` is an actual *pairword* phase change across a still-long variable band, independent of how large `r` is.

Independently, `lift_replay.cpp` constructs `r=14000` as an explicit decimal digit vector, repeatedly performs digitwise reverse-and-add, and in parallel updates a GNU GMP `mpz_class` using an independent base-10 string reversal plus integer addition. It checks exact equality of the complete canonical numbers at **every** one of the 20,001 states, checks nonpalindromicity and the two bands at each state, and stores compact checkpoints. Initial length **28,004**, final length **36,298**; final FNV-1a 64-bit of the most-significant-first decimal word `3e5fc41a315ba602`. A separate `r=14001` test agrees through 1,000 additions. `carry_gauge.py` performs 25,000 randomized cross-base identity controls (`2<=b<=32`, `1<=k<=31`, word lengths 1..120), including overflow handling.

Reproduction from the repository root:

```sh
g++ -O3 -std=c++17 calculation/new_structures/agent-X28/affine_carry.cpp -o /tmp/x28_affine
/tmp/x28_affine 14000 20000
python3 calculation/new_structures/agent-X28/carry_gauge.py 25000
g++ -O3 -std=c++17 calculation/new_structures/agent-X28/lift_replay.cpp -lgmpxx -lgmp -o /tmp/x28_replay
/tmp/x28_replay 14000 20000
```

Compact logs: `calculation/new_structures/agent-X28/affine_14000_20000.txt` and `calculation/new_structures/agent-X28/replay_14000_20000.txt`. They are **not** full orbit traces or evidence of infinite survival.

## 4. What breaks, and a structural next construction

The `9 -> 0` switch at `t=20` is favorable for a new **carry-reset reservoir** format: a band can be transmitted with its carry at coefficient 9, then switch to an absorbing coefficient 0 band without requiring a short, time-periodic kink. However, the two coefficient-0 reservoirs contract as their interfaces advance. For `r=14000`, their minimum length at `t=20000` is 1,957, not a replenished or time-periodic plateau. No mechanism here restores that reservoir indefinitely. A genuine infinite certificate would need a later `0 -> 9` recharge or a periodically transported reservoir with a nonnegative length drift, proved by an all-length loop in the affine RLE state graph, or a further finite-state quotient that closes the growing endpoints. Searching for that recharge is the new direction; extending the mere finite replay is not a substitute.

**Scope:** exact base-independent one-step carry theorem and a sound (but unformalized) symbolic family checker; computed base-10 20,000-step family. **No proof** of a base-10 Lychrel number, no statement about 196, and no Lean-verified construction.