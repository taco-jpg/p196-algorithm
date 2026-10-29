# Agent X26: adversarial-centre shields (base 10)

**Status: COMPUTED** for the 20,000-step reference run and independent GNU MP replay; the finite propagation lemma below is a PAPER PROOF. This is a *finite-horizon universal family*, not an infinite Lychrel result.

## Exact setup
Digits are least-significant-first. For an ordinary decimal digit word D of length n, define its symmetric pair coefficient word P(D)_i=D_i+D_{n-1-i} (0..18). A reverse-add step normalizes P(D) from low to high with carry 0, then appends the final carry (0 or 1). Denote its new length by n+gamma. Pairword dynamics are exact: P(D_next)=pairs(norm(P(D))).

For L=22000, k=257 and **any** k-digit internal word C, including words with zero at the ends, define the actual integer with written decimal digits
N0(C) = 5 ++ 9^L ++ C ++ 9^L ++ 4.
The reference R0 uses C=9^k. Every N0(C) has 44259 digits, with the same nonzero most significant digit and least digit.

## Finite carry-confinement lemma (PAPER PROOF)
Suppose two symmetric pair words P,Q of equal length n agree outside the symmetric interval [ell,n-1-ell], with ell>=1, and have a common coefficient 18 at index h=n-ell (the first cell on the *high* side outside that interval). Normalize low-to-high, starting carry 0. The carries agree before index ell. They may disagree inside the interval. At index h, 18+c has carry-out 1 for either c=0 or c=1, so the carries agree above h. Thus the normalized digit words differ only within [ell,h]. Their final overflow bit gamma is identical. After reflection and pairwise addition, the new pair words agree outside the symmetric interval [ell', n+gamma-1-ell'], where ell'=ell-1+gamma. Indeed, gamma=0 reflects [ell,n-ell] to [ell-1,n-1-ell], and gamma=1 reflects it to itself. This is an **exact** implication for every possible inner coefficient word, without assuming a periodic or bounded centre.

## Universal induction and safety witness
For the reference and *any* C, pairword differences at t=0 are inside [L+1,L+k]. Put G_t=sum_{j<t}gamma_j and ell_t=L+1-t+G_t. The reference length is n_t=2L+k+2+G_t and the high-side collar index is
h_t=n_t-ell_t=L+k+1+t,
independent of the unknown centre and of the overflow schedule. The checked reference pairwords have coefficient 18 at every index [h_t, 2L+k] and its reflection for all t=0..20000. Consequently the lemma applies inductively (for t<20000) to *every* C, gives a common overflow schedule, and proves all perturbed pairwords agree with the reference outside the predicted interval. It also proves that every candidate has two exact coefficient-18 collar bands of length >=L-t at each t, since [h_t,2L+k] lies outside the possible defect box.

To certify nonpalindromicity, let w_t be the smallest low-end index at which the reference *digits* differ from their reversed partners. At t=0, the two outer digits are 4 and 5 for every C. At t>=1, the normalization part of the lemma shows the arbitrary-centre digits agree with reference digits outside [ell_{t-1},n_{t-1}-ell_{t-1}], including reflected low-end witness positions whenever w_t<ell_{t-1}-1. The reference enumeration checks the stricter w_t<ell_t-2 at each t. Numerically max(w_t)=25, min(ell_t)=10275; therefore no member of the family is palindromic at any t<=20000. This is finite induction over an exhaustively checked *reference trajectory*, not a proof for every t>=0.

## Reproduction, independent checks
From repository root:
```sh
cd calculation/new_structures/agent-X26
g++ -O3 -std=c++17 -Wall -Wextra -Werror universal.cpp -o universal
./universal 22000 20000 257 > checkpoints-replay.tsv
g++ -O3 -std=c++17 gmp.cpp -lgmpxx -lgmp -o gmp
./gmp 22000 20000 1000 > gmp-replay.tsv
```
The first code independently normalizes pair words and performs literal decimal digit-array arithmetic at **every** step, checks both 18 collars and the outer nonpalindrome witness at **every** step, and replays one deliberately nonuniform Thue-Morse 8/9 centre. GNU MP constructs actual ordinary big integers and performs 20,000 independent bigint reverse-and-add steps, checking palindromicity each time; its 21 checkpoints agree on length and FNV-1a-64 checksum with the digit-array Thue-Morse replay. No cryptographic guarantee is claimed for the checksum; the engines implement independent arithmetic and hash only for compact comparison.

Summary: G_20000=8274; digits 44259 -> 52533; minimum L-t=2000; minimum ell=10275; max witness 25. The Thue-Morse example is a nonconstant {17,18}-coefficient initial centre in pairword form. Its earlier L=12000 experimental variant has 1851 coefficient-18 collars at t=20000 but is NOT the basis of the universal proof.

## Exact limitation and next direction
The guaranteed moat decreases by one per time step, L-t. To get an infinite decimal certificate one would need a true **recharging rule** which increases the protected 18 band or replaces it by an invariant safety witness before depletion, with all centre perturbations included. This result only proves 20000 safe steps, no matter how many centre choices there are. It is not a statement about the orbit of the integer 196.
