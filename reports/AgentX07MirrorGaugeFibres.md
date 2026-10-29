# X07: exponential one-step preimage fibres of decimal reverse-and-add

**PAPER PROOF**: An explicit family of `3^g` distinct protected base-10 integers all maps to the **same** next integer, for arbitrarily large `g`, with a certified nonpalindromic prefix of any prescribed finite length. **COMPUTED**: complete one-step independent bigint controls for 9 and 729 variants, 1,000 of a 177,147-member family, and a full 20,001-step GMP + grade-school + quotient three-engine witness. **UNDECIDED**: a fixed-seed infinite decimal Lychrel certificate. No Lean claim.

## Exact inverse symmetry (all m, h)

From `AgentX07RepunitQuotient`, for `0<q<10^h`, `q=2 (mod 9)`, `m=digitlen(q)`, `A=10^m-q`:

    RAA((10^h-1)*q) = (10^h-1) * (10^m + 1 + rev_m(A) - A).

The successor depends on the entire `m`-digit **boundary** word `A` only through the antisymmetric digit reversal difference `D_m(A)=rev_m(A)-A`. If mirrored digit pairs `A[i],A[m-1-i]` are simultaneously increased by `δ` without crossing digit limits, their contribution to D is unchanged. With charge-preserving changes `sum δ=0 (mod 9)`, the input remains nonpalindromic and *all such distinct inputs merge after exactly one actual reverse-and-add step*. This is a constructive inverse fibre, not a palindrome-free claim about arbitrary numbers.

## Closed-form exponential family

Let `m=10+18k`, `r=m/2=5+9k`, and `g=floor((r-1)/2)`. Form the `m` digits of `A` by identical mirrored pairs: pair number 0 (the outermost) has digit `6`; all other `r-1` pairs have digit `4`. Partition the latter into `g` disjoint pairs of mirror-pairs (leave one unused when necessary). In group `j`, independently select `δ_j ∈ {-1,0,1}` and replace the two pair digits `4,4` with `4+δ_j,4-δ_j`. This produces exactly **3^g distinct** palindromic decimal words `A` with all digits between 3 and 6. All have the same digit sum

    sum_digits(A) = 2*(6+4*(r-1)) = 8*r+4 = 44+72*k = 8 (mod 9).

For any `h>=m+1`, put `q_A=10^m-A`, `N_A=(10^h-1)*q_A`. Every `q_A` is `2 (mod 9)`, has m digits and satisfies the protected quotient inequality. Because `rev_m(A)=A`, **all** the distinct actual decimal integers `N_A` satisfy the precise collapse identity

    N_A + reverse(N_A) = (10^h-1)*(10^m+1).

The common next state is also protected, with quotient `10^m+1`. The first states are nonpalindromes because their opposite endpoint digit pairs sum to 9, an odd number. Subsequent protected states cannot be palindromes by the mod-9 charge theorem. This is a true exponentially large one-step fibre of the decimal map, not merely a set of seeds with similar signatures.

Moreover the decimal digit count of a protected quotient grows by **at most one per operation** (`q_next<2*10^m`). Thus, for any finite `T>=1`, choosing `h>=m+T+1` ensures that **every** one of these `3^g` seed orbits is a nonpalindrome at steps `0..T`, independent of computation. This is a rigorous family of arbitrarily long finite-horizon witnesses, **not** an infinite orbit for any fixed h.

| m | g | mathematically distinct seeds | independent bigint one-step controls |
|---:|---:|---:|---:|
| 10 | 2 | 9 | all 9 |
| 28 | 6 | 729 | all 729 |
| 46 | 11 | 177,147 | 1,000 distinct samples |
| 64 | 15 | 14,348,907 | cardinality by formula only |

A mutation that changes two nonmirrored digits by +1 and -1 leaves charge 8 unchanged but breaks the common successor, an independent adversarial test (`A=6444444356` for m10).

## Independently replayed 20,001-step concrete decimal candidate

Take `m=10`, baseline palindromic `A=6444444446`, `q_A=3555555554`, and `h=8278`. Then

    N_0 = (10^8278 - 1) * 3555555554      (8,288 decimal digits)
    N_1 = (10^8278 - 1) * 10000000001     (8,289 digits).

From the universal quotient `q_1=10^10+1`, a standalone least-significant-digit quotient engine computes **20,000 further operations**; `q_20001` has **8,277** digits and is still `<10^8278`. It grew by 8,266 quotient digits after t=1, with FNV64 `882bbe1ad0ba698d` over low-first final quotient digits. Since quotient digit lengths never decrease, every intermediate state is protected.

A **third, independent route** applies genuine full-decimal reverse-and-add to the *actual* 8,288-digit integer at **every** step `t=0..20001`: `mpz_class` GMP whole numbers and an independent schoolbook decimal digit-vector engine produce identical complete numbers at every step; a separately implemented quotient digit engine also satisfies `N_t=(10^8278-1)*q_t` at every state. Every real decimal state is tested against its full reversal for palindrome equality. Outcome: **no palindromes, no engine mismatches**, final integer **16,555 digits**, full state FNV64 `b9dfb58f06f5d298`. Thus all nine `m=10` seeds with this h also have a 20,001-step safe prefix by the exact one-step collapse (the full GMP replay is performed for the displayed baseline; the other eight are supported by the proven identical successor).

## How this changes certificate search

The antisymmetric quotient difference offers an explicit, high-multiplicity **inverse construction** for targeted protected successors. Instead of enumerating every long decimal prefix, a bridge solver may search only `D_m(A)` and then populate the symmetric *gauge fibre* to satisfy separate exterior or collision constraints. The concrete collapse here does not regenerate the repunit exponent; the current search still needs an all-parameter renewal bridge `h -> h'>h` to reach an infinite proof. No exclusion or infinite-base-10 claim is made.

Reproduce with `sh calculation/new_structures/agent-X07/gauge_run.sh` (requires GMP development headers). Code: `gauge_preimages.py`, `scalar_trace.cpp`, `gmp_replay.cpp`; retained compact evidence `gauge_counts.json`, `gauge_measurements.json`. These files import the earlier mathematical quotient lemma, not duplicate its implementation.
