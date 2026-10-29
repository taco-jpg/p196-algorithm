# Agent N30: adversarial-centre carry-cone format (finite-horizon decimal family)

Status: **COMPUTED**, with an elementary conditional soundness argument given below. This is **not** an infinite decimal Lychrel certificate and **not** a result specifically about 196.

## A different certificate object: an exterior cone without an assumed centre

For an `n`-digit decimal integer `N`, a certified exterior of width `k`, where `n >= 2k+1`, specifies the digits

* `low[j] = digit j from the least significant side`;
* `high[j] = digit j from the most significant side`, for `0 <= j < k`.

The entire nonempty middle is unconstrained. Let `p[j] = low[j] + high[j]` in `[0,18]`. The pairword of `N` is known exactly on the first and last `k` positions (`p[0],...,p[k-1]` and its reversal); its middle is completely unspecified.

Define `r` by deleting the maximal suffix of 9s from `p[0..k-1]`, so `p[r-1] != 9`. If no such `r` exists, the cone cannot certify a next step. For any unknown inner carry `c in {0,1}`, the outgoing carry from `p[r-1]` towards the most significant end is independent of `c`, because `floor((p[r-1]+c)/10)` is constant precisely when `p[r-1] != 9`. Thus all more exterior high digits `p[0..r-2]`, and the final overflow `g`, are *exactly* computable without inspecting the middle. The lowest `r` normalized digits are also known, by normalization from the least significant end with initial carry 0.

**One-step soundness lemma.** Let the predicted low digits be `L[0..r-1]` and the predicted high digits in most-significant-first order be `H[0..r-2]` (normalize `p[r-2],...,p[0]` using the reset carry). Then `N + reverse(N)` has an exact, middle-independent exterior of width

`k' = r` if `g=1`, with `low' = L[0..r-1]` and `high' = [1] ++ H[0..r-2]`;

`k' = r-1` if `g=0`, with `low' = L[0..r-2]` and `high' = H[0..r-2]`.

Here `H[j]` is indexed from the most significant end. Note that the outer high digits resulting from the normalized sum are `H[0], H[1], ...`; the code stores them in that order. In particular, the new exterior never depends on the value or length of the middle, except for the minimal non-overlap condition. An input of `n >= 2k+1` digits yields an output of at least `n` digits, while `k' <= k`, so this condition survives forever as long as the cone remains nonempty. If **some** `low'[j] != high'[j]`, the output cannot be a palindrome. Induction proves the finite-horizon certificate: for any `T`, if the cone evaluator never loses all width and has an unequal exterior pair at all times `0..T`, *every initial middle word of every length >=1* avoids palindromes through time `T`.

For a future infinite theorem, augment this cone evaluator with a finite *renewal/pumping rule* that certifies new trusted interior pairs. The present algorithm is monotone `k' <= k` and therefore does not establish an infinite orbit.

## Explicit decimal family and 20,000-step certificate

`cone_family.cpp` deterministically generates 16,000 low-side digits and 16,000 high-side digits with a xorshift64 stream seeded `0x9a702f4ed37008c5`: for each `j`, draw successive 64-bit values `a,b` and use `low[j]=a mod 10`, `high[j]=b mod 10`; replace `high[0]` with `1+(high[0] mod 9)`. Let `M` be **any nonempty finite decimal word**, including words with zeros. For any such `M`, set

`N_0(M) = high[0] high[1] ... high[15999] ++ M ++ low[15999] ... low[1] low[0]`.

This is an infinite family of *finite-horizon* decimal seeds, since the centre word can have arbitrary length and content. The deterministic cone computation for **20,000** steps gives: `k0=16000`, `k20000=1866`, `8246` length overflows, `2380` extra width discards across runs of carry-transparent 9s (longest such run 5), and a nonpalindromic witness within the first 21 digit pairs at every step (maximum first witness index 20). All `20,001` orbit values including step zero are proven nonpalindromic by the conditional lemma + exact finite cone evaluation; no centre ever needs to be read.

The code **also** independently computes the complete decimal integer using its own base-`10^9` limb arithmetic (`BigInt::add`), reverses its full decimal representation, and checks every claimed boundary digit and the full palindrome predicate at each step. Three independent centre instances replayed successfully: `M=0`, `M=3^37`, `M=9^123`. Final full integer lengths were respectively 40,247, 40,283, 40,369 decimal digits. Unlike the cone, these independent replays are ordinary finite numerical tests, not the basis for quantification over all middles.

A separate Python exact-integer oracle runs `49,902` randomized one-step tests with centre lengths 1..100 and both incoming carry outcomes; all passed. The code and JSON record do not contain a complete giant orbit log.

## Reproduce

```bash
python3 calculation/new_structures/agent-N30/test_cone.py
c++ -O3 -std=c++17 calculation/new_structures/agent-N30/cone_family.cpp -o /tmp/n30_cone
/tmp/n30_cone 16000 20000 1 0
/tmp/n30_cone 16000 20000 37 3
/tmp/n30_cone 16000 20000 123 9
```

Expected last line has `VERDICT PASS`, `checked_integers=20001`, `remaining_k=1866`, `max_first_witness=20` for every run. No bound on `M` is assumed by the proof; the separate big-integer oracle is naturally run on a few representatives.

## Redirection

Carry-uncertain *fixed* exterior guards lose information; the constructive route is to track a **moving carry-reset cone** and discover a mechanism that periodically replenishes its certified width, rather than running another census of forbidden fixed centres.
