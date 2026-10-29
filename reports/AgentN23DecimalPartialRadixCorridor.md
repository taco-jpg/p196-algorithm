# Agent N23: a uniform 174-step decimal pumping corridor with partial radix blocks

**COMPUTED** (exact sparse rational polynomial identities), not Lean, not an infinite base-10 orbit proof. This is a CONSTRUCTIVE family, not an exclusion census.

## Partial high-block identity (PAPER algebraic derivation)

Let B=10^k and N have base-B digits x_0,...,x_(n-1), least significant first. Suppose x_(n-1) has exactly h significant decimal digits, 1<=h<=k. Let rho_j(x) reverse the j decimal digits of x, padding interior blocks to width j before reversal. Splitting the decimal numeral into a full-width lower part plus its h-digit high block proves the *exact* identity

  Rev10(N)=rho_h(x_(n-1)) + 10^h * val_B([rho_k(x_(n-2)),...,rho_k(x_0)]).

Unlike naive base-B digit reversal, this remains correct for odd decimal lengths (h<k), including the high-digit carry of 1 that broke the two-step control. It only requires the top base-B digit to be fixed for the template and its decimal width h to remain constant. A literal-plus-affine-repeated-motif word has a sparse rational-polynomial value in Z=B^q (see AgentN23SparsePolynomialDigitBands.md). Deleting the top digit, reflecting the remaining pieces with rho_k and multiplying by 10^h preserves the polynomial representation. Thus *all* exact polynomial coefficient identities prove true decimal reverse-add for every q>=0, at arbitrary length. For nonpalindromicity use the positive-integer-root divisibility test from the earlier N23 result: multiply the nonzero difference polynomial by a common denominator and remove its lowest Z power; any integer root Z must divide the remaining nonzero constant. The checker exhausts all q with B^q <= |constant| and thereby decides every q>=0.

## Constructive 174-step family

Start from the genuine decimal number N0(q)=12 (99)^(52+q) 34, q>=0. For t=0..174, the ordinary decimal state after t reverse-add steps, represented in two-digit base-100 groups, has the precise complete digit form U_t ++ [99]^q ++ W_t, least significant first. Different U_t,W_t are generated automatically by mining the true decimal orbits for q=0,1,2,3,4; **mining is NOT the proof**. The independently implemented partial-high-block checker symbolically proves all 174 transitions at once as exact rational-polynomial identities and certifies N_t(q) != Rev10(N_t(q)) for every q>=0 and t<=174.

The first width q=0 has 54 base-100 groups at t=0 and 89 groups at t=174; more initial 99 pairs add exactly q groups. Unlike a 20,000-step single-seed replay, this establishes the stated 174-step property for infinitely many distinct integers with one finite algebraic check. Independent Python bigint arithmetic replays EVERY step and EVERY full state word for q in {0,1,2,10,50,100,250} without importing the polynomial routines.

## Failure frontier directs next format

At t=175 for qbase=50, the one-copy insertion relation U_t ++ [99]^q ++ W_t is not maintained between q=0 and q=1: a local [88] in the q=0 orbit becomes [98,89] in the q=1 orbit, instead of a single inserted [99]. This is not a failed palindrome test or proof of impossibility. It is a *carry-front collision* that induces a finite substitution. Repeat the same exact search with baseline 99-pair counts qbase 45..60: the earliest failure time ranges from 157 to 212 and the replacement words are in frontier.csv. Search next for one-counter/transducer rules that absorb [a] -> [b,c] at this collision, with a remembered phase, rather than requiring every additional pair to remain an untouched [99]. Nothing here asserts the front eventually palindromes or becomes periodic.

## Reproduction

Run from repository root:

    bash calculation/new_structures/agent-N23/reproduce_corridor.sh

The one-command runner generates the entire 175-state data JSON in /tmp, checks its SHA-256 76e9c877fa07b580e31e167d74ea8641eb0e54e443ebe1721337ecf204ac2882, executes 174 exact symbolic steps and the seven independent ordinary big-integer controls. The input base-9 source and first sparse-polynomial format are in the immediately preceding N23 commit. No shell checkout was available to run tools/verify.py --changed; standalone controls passed.
