# Agent X10: complementary carry battery and exact 90-channel fission

**Scope:** PAPER PROOF of one-step identity and sound finite-gap two-edge format; COMPUTED 90-channel scan and 20,000-step finite universal families with independent ordinary-decimal replay. **Not** a Lean-verified or infinite Lychrel result and not a result about the orbit of 196.

## 1. Carry-fission identity, all positive lengths and every complementary digit

Fix decimal digits `A,C` in `{1,...,9}`, `B,D,a` in `{0,...,9}`, and positive integer `R`. Let `u=10A+B`, `v=10C+D`, and define

```
N_R = u a^R (9-a)^R v
s = A+D,  t = B+C+1.
```

Assume `10<=s<=18` and `10<=t<=19`. The exact decimal identity is

```
N_R + reverse(N_R) = H 0^(2R) L,
H = 100 + 10*(s-9) + (t-10),
L = 10*(t-10) + (s-10),    written as exactly two low decimal digits.
```

**Proof.** Base-10 grade-school addition starts with `D+A=s`: low digit `s-10` and carry 1. The next column adds `C+B+1=t`: next digit `t-10` and carry 1. The next `2R` columns each pair `a` with `9-a`, so `a+(9-a)+1=10`: each has output digit 0 and propagates carry 1, independently of R and a. The second-highest column outputs `t-10` and carry 1; the highest outputs `s-9` and carry 1, giving the extra leading 1. Concatenating the digits gives exactly `H` (three digits), `2R` zeros, and the padded two-digit `L`. The initial charged numeral is never a palindrome because the two central positions have unequal digits `a != 9-a` (integer digits). QED.

This is an **active carry battery**, not a neutral or absorbing band: every interior column has sum 9 but receives and propagates carry 1 and hence *discharges into zero* on the next integer. The seed interior can be arbitrarily long without increasing any verification state size. The map depends on `(u,v)` only via two carry-channel integers `(s,t)`, giving 9*10=90 possible channels; all are realizable by two-digit u,v.

## 2. Exact two-packet soundness and finite-gap criterion

After one fission, write the current numeral as

```
N = value_10(lo) + 10^M value_10(hi),     M=2R+2,
lo=(start,digit-array), hi=(start,digit-array), digits least significant first.
```

`lo` and `hi` may expand, change length and move their internal starts by integer offsets; the digits are kept canonically normalized (leading/trailing zero trim), and local internal carries are exact. At any state, let `a=lo.start`, `b=hi.start`, `l=lo.end`, `h=hi.end`. Require `a>=0`, `M+b>=l+1`, `M+b>=0`; equivalently `M>=max(1+l-b,-b)`, plus the trivially checkable nonzero high digit. These **disjointness and canonical-number guards** establish that the two polynomial parts are the genuine complete decimal digits, with a zero corridor between them.

The exact step is computed without constructing the long zeros: mirror the entire high packet around its local high endpoint `h` and add to the low packet; separately mirror the low packet into the high packet and add. Explicitly, each target packet is the *carry-normalized* coefficientwise sum of one packet and the reflection of the other at the common local top `h`; code `newpacket(lo,hi,h)` and `newpacket(hi,lo,h)`. Each local packet is normalized by finite grade-school carry propagation and zero trimming. The mirror of the high packet begins at `h-hi.end=0` in low-local coordinates, and the mirror of the low packet begins at `h-lo.end` in high-local coordinates. Because the guarded two regions are disjoint, carries inside one cannot modify the other. Thus the concatenation of the two new packets equals the **actual integer reverse-and-add successor**. (The successor must also meet the guards before the next application.) This is a direct positional digit proof, not an interpolation or numerical fit.

For any chosen finite T, compute the same packet recurrence `x_0,...,x_T` with `x_0=(L,H)` and set

```
Q_T = max(1, max_{0<=k<=T}(1 + lo_k.end-hi_k.start),
              max_{0<=k<=T}(-hi_k.start)).
```

If all low starts are nonnegative and every `x_k` has a nonzero highest digit, then **every `R` with `2R+2 >= Q_T`** generates exactly that same packet recurrence through T *further* ordinary decimal reverse-add additions, independent of R. The nonpalindrome predicate at each stage compares every low digit with its reflected high-digit partner and conversely (missing partners count as zero). It is a finite, exact decision for all sufficiently long corridor lengths. If every stage is nonpalindromic, then the original charged seed and those T+1 successors are all nonpalindromic. Proof: induction on the number of additions using the guarded exact one-step lemma. This theorem is finite-horizon only; it becomes an infinite certificate **only if** one additionally exhibits a closed all-time template/guard invariant, which has not been found.

## 3. Computed channel scan and best two cases

`charged_edge_classification.cpp` deterministically enumerates `(s,t)` in `[10,18] x [10,19]` (90 channels), computes each sparse pair `(H,L)`, and runs **20,000** exact local carry steps, tracking the full-word palindrome predicate and the maximal certified guard. Thirteen channels have no palindrome throughout the 20,001 sparse states. Sorted first by survival and then by guard, their `(s,t; H,L; Q_20000; R_min)` values are:

```
(17,13; 183,37; 11953; 5976)   (16,16; 176,66; 11956; 5977)
(18,17; 197,78; 11967; 5983)   (17,14; 184,47; 11975; 5987)
(13,16; 146,63; 11988; 5993)   (15,18; 168,85; 12017; 6008)
(14,18; 158,84; 12034; 6016)   (17,19; 189,97; 12038; 6018)
(17,16; 186,67; 12040; 6019)   (15,19; 169,95; 12041; 6020)
(15,17; 167,75; 12055; 6027)   (13,17; 147,73; 12067; 6033)
(17,15; 185,57; 12082; 6040)
```

The other 77 channels have a symbolic palindrome by or before the tested horizon in the separated-packet model; **this is not** a claim of an exclusion for wider formats, arbitrary centres or infinite base-10 candidates, and is not the publication's purpose. Complete raw classification, including all 90 rows and first-palindrome index, is in `charged_edge_T20000.csv`. The best is a new *positive* family:

```
N_0(R) = 88 4^R 5^R 49 ,       R>=5976.
N_1(R) = 183 0^(2R) 37 .
```

`Q_20000=11953`, `M=2R+2`, so **every R>=5976** preserves the exact two-edge form and zero palindromes for `N_1,...,N_20001` (20,000 steps starting at N1), with N0 also nonpalindromic. This is 20,001 ordinary reverse-add operations total and 20,002 nonpalindromic states. The older channel `(13,16)` from `88 4^R 5^R 75 -> 146 0^(2R) 63` has `Q_20000=11988` and R>=5993. Both identities are exact in each R, as is the entire 20,000-step follow-up for every R meeting its guard.

## 4. Separate independent arithmetic controls

An independent C++ schoolbook decimal-array engine computes `N + reverse(N)` **over the entire numeral** at every step, and a separate two-end symbolic oracle predicts the complete word. It compares every digit, not just samples, and checks every actual numeral for palindromes. All tests passed:

| Charged seed | R | Initial → final digit length | Full-word matches | Nonpal states | FNV64 entire-word sequence |
| --- | ---: | --- | ---: | ---: | --- |
| `88 4^R 5^R 49` | 5976 | 11,956 → 20,264 | 20,001/20,001 | 20,002/20,002 | 5238618168155618011 |
| `88 4^R 5^R 49` | 5977 | 11,958 → 20,266 | 20,001/20,001 | 20,002/20,002 | 6745648121409070835 |
| `88 4^R 5^R 75` | 5993 | 11,990 → 20,245 | 20,001/20,001 | 20,002/20,002 | 7391909489669724506 |

The independent `charged_identity_control.py` uses native Python arbitrary-precision integers for **2,706** separate one-step fission identities, ranging over all 90 channels, 6 choices of `a`, 5 band lengths, and 6 additional positive-seed lengths. This catches wrong carries, reversed-block order, and off-by-one output width. Two 1,000-step full-word controls of `R=305` also test `a=0` and `a=4` (both yield the same discharged successor), with 1,001/1,001 word matches each.

## 5. Constructive frontier, not an infinite certificate

This is a **discharge** mechanism: an arbitrarily long complementary two-colour band becomes a zero corridor in one exact step, while leaving sparse edge packets that can be tracked by an exact, finite-interface recurrence. It improves the 20,000-step explicit charged seed to 11,956 digits and exposes 13 distinct carry channels. In the tested two-packet recurrence the edge support expands, consuming the zero gap (Q_T grows from 1 to 11,953); no automatic return to a fresh charge band has been established. The constructive next step is an exact **recharge** or packet-fission gate that transforms a sparse corridor after an entire front cycle back into a complementary band while restoring R, and then a checked all-R macrocycle. There is no unconditional proof of a base-10 Lychrel number or 196 here.

## 6. Reproduction

From repository root:

```
bash calculation/new_structures/agent-X10/charged_fission_reproduce.sh
```

This compiles the three C++ tools, rechecks the complete 90-channel 20k table and the best-channel packet trace, runs the native Python identity controls, and independently repeats three separate 20,001-step complete-word decimal orbits plus two 1001-step controls, comparing deterministic outputs to the checked-in compact traces. Requires only `g++` (C++17) and Python 3 stdlib. No Lean file is added; the repo-wide `tools/verify.py --changed` cannot run without a full repository checkout and Lean 4.19.0 on the machine running the agent.
