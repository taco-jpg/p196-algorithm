# Agent-X28: a base-4 carry-gauge shock with an 18-step decimal band switch

**Classification:** PAPER PROOF (soundness of the affine RLE carry semantics, already established in the companion `AgentX28BinaryGaugeAvalanche20k` report); COMPUTED (20,001 exact symbolic states for all `r>=12062`, and independent every-step GMP/digit-list validation of the explicit 24,128-digit seed). This is not an infinite base-10 Lychrel certificate.

## New construction from the quaternary source

The power-of-two family in `reports/REPORT_203.md` includes the canonical base-4 word `W_r=10(3^r)23(0^r)`, for `r>=2`. Its proven base-4 orbit grows by returning to a template after a finite cycle. Apply the exact carry-gauge embedding (`b=4,k=3`, `B=k(b-1)+1=10`): multiply *input* digits `0,1,2,3` by 3, producing the DECIMAL number

`N_r = 30(9^r)69(0^r)`.

This is **not** a full-orbit conjugacy. The first reverse-and-add has the same carry bits as in base 4, but its output digits are perturbed by the carry coboundary `2*(c_{i+1}-c_i)`, and a terminal overflow remains digit 1 instead of being scaled. Unlike the binary-derived `90(9^r)09(0^r)` family, the quaternary-derived decimal orbit changes its central *pair-coefficient* bands from 9 to 0 at step **18** (not 20). The two distinct 9-plateaus last at least 12,054 columns at every time `0<=t<18`, and the two distinct 0-plateaus last at least 3 columns for every `18<=t<=20000`, uniformly for `r>=12062`.

## Soundness and its exact scope

For each digit run, the symbolic checker maintains an affine length `a*r+c`. It requires strictly positive lengths and nonnegative slope at the threshold `r=R`, so every represented run exists at every larger integer parameter. Scanning mirrored RLE words with the paired minimum guard `u(R)<=v(R) and u.slope<=v.slope` (or reverse) makes each chosen partition valid for all `r>=R`; a crossing comparison fails closed. For any constant pairword coefficient `q`, the carry transition `f_q(c)=floor((q+c)/10)` is idempotent on `{0,1}`. Thus a matched chunk of affine length `m` normalizes EXACTLY to a first digit `(q+c)%10` followed by `m-1` identical copies of `(q+f_q(c))%10`, and its new carry is `f_q(c)`. Appending the final carry 1 handles length growth. Merging neighboring equal digits preserves the represented word. Induction through `T` transitions therefore gives the literal decimal reverse-and-add state of **every** `N_r` for all integers `r>=R`, not just `r=R`. The paired RLE equality scanner yields a genuine unequal digit pair at each time `t=0..T` for every parameter and hence proves nonpalindromicity over that finite horizon. As in the companion report, this is a PAPER PROOF of a sound method, *not* a Lean formalization or an infinite orbit theorem.

This run checked `R=12062`, `T=20000` with **312,979,902** exact aligned RLE segment transitions; all 20,001 nonpalindrome checks and the band checks passed without unsafe symbolic comparisons, negative run lengths, or invalid digit/carry transitions. The lengths satisfy `L_0=2r+4`, `L_18=2r+11` (24,135 at the threshold), `L_20=2r+12`, and `L_20000=2r+8296` (32,420). At `r=12062`, the longest q0 band is just 5 cells at time 20,000; the minimum q0 maximum over the 18..20000 interval is 3. This narrow remaining reservoir is a concrete mechanism to target for self-renewal rather than merely pumping an initial length.

An exploratory uniformly guarded run at `R=12061` fails closed at time 19,999, while `R=12062` fails closed at time 20,002 if one tries extending the same symbolic partition. These failures do **not** establish a palindrome, nor do they exclude alternate branch partitions or a different infinite representation. They show the current two long 0-bands are essentially depleted at the end of the certified horizon. A potential infinite construction must obtain a recurrent 0-to-9 recharge with a phase-locked carry reset, or a different nondepleting supply of band length.

## Completely independent integer replay

`quaternary_replay.cpp` builds the whole decimal digit array from the four literal pieces, applies ordinary reflected-digit addition with base-10 carries, and independently builds the same number as a GNU GMP `mpz_class`. At each of 20,001 canonical states it compares the **entire** digit sequence to GMP's base-10 string after the separate integer addition `n += reverse_decimal_string_as_integer(n)`; it also checks nonpalindromicity and the same long paired-coefficient runs. No symbolic normalization or affine RLE data are imported into this replay. For `r=12062`, initial length is **24,128**, final length is **32,420**, zero arithmetic disagreements and zero palindromes; final FNV-1a 64-bit hash of the MSD-first number is `7ab87e9f1db231f0`. `r=12063` additionally passed 1,200 GMP cross-checks.

The smallest certified seed improves the binary-gauge example's 28,004 digits by 3,876 at the same 20,000-step horizon. This is a *new mechanism/seed*, not a claim of a globally shortest finite-horizon seed; other independent projects already have smaller seeds. Its distinctive features are the base-4 carry lift, earlier 18-step band switch, all-parameter affine verification, and near-exact 20,000-step depletion measurement.

## Reproduction

From repository root:

```sh
g++ -O3 -std=c++17 calculation/new_structures/agent-X28/quaternary_affine.cpp -o /tmp/x28q_affine
/tmp/x28q_affine 12062 20000

g++ -O3 -std=c++17 calculation/new_structures/agent-X28/quaternary_replay.cpp -lgmpxx -lgmp -o /tmp/x28q_gmp
/tmp/x28q_gmp 12062 20000
```

Reference output files: `calculation/new_structures/agent-X28/quaternary_affine_12062_20000.txt` and `calculation/new_structures/agent-X28/quaternary_replay_12062_20000.txt`. The family claim is **COMPUTED finite-horizon** supported by a PAPER PROOF of sound symbolic semantics. Neither a decimal Lychrel number nor a Lean-verified theorem has been established.