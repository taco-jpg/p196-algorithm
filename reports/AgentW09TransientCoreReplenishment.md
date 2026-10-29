# W09: transient central-core replenishment, finite budget, and exact cap-return obstruction

## Scope

COMPUTED: two independent arithmetic implementations check 20000 real decimal reverse-and-add steps and the six-phase central coefficient block, with no palindrome. PAPER PROOF: the central insertion carry argument and conditional finite-state resource-renewal criterion. The first 24-step parameter family follows by induction from these identities and finite exact controls. UNDECIDED: infinite decimal Lychrel, returning cap, or Lean verification.

## The explicit seed and checked structure

Least-significant-first pair-coefficient cap:
L = (7,12,16,10,7,4,12,8,15,13,17,1,17,18,16,3,5,0,2,12,18,10,1).
Take P_0(k) = L ++ 8^(2k) ++ reverse(L).
Realize each coefficient p as a low digit floor(p/2) and a high digit ceil(p/2).
The resulting most-significant-first ordinary decimal integer is exactly

N_k = 46854264879199823016951 ++ 4^(2k) ++ 05961021898086746235863.

At k=22000 this has 44046 digits. The core is a pairword, not a claim that the number itself is palindromic.

Let x_t cycle through 8,16,14,10,2,4. For each t the actual pairword has exact factorization A_t ++ x_t^(w_t) ++ reverse(A_t), where the central run is maximal and A_t is a finite changing cap. Every one of the 20001 states has nonempty w_t; the arithmetic engines check this against the ordinary integer at every step.

## Exact centre insertion lemma and resource accounting

Define T(P): normalize the pair-coefficient word by ordinary base-10 carries, append a leading overflow digit if required, and take the reflected digit-pair sums. Let I_x insert a reflected pair of copies of x at the midpoint of a palindromic coefficient word; when the original length is odd, insert one x on either side of the old centre. Suppose the original word has at least six copies of x in its central run, with x from the six-element clock. Put c*=0 for x=2,4,8 and c*=1 for x=10,14,16. Then

T(I_x(P)) = I_(2*((x+c*) mod 10))(T(P)),

with identical terminal overflow and unchanged outer digit output.

Proof: on any homogeneous block with x != 9, normalization coalesces incoming carries 0 and 1 immediately after its first coefficient. Interior copies therefore always produce the steady digit (x+c*) mod 10, leaving the normalization state outside the inserted region untouched. Inserting two symmetric copies sufficiently deep inside a central run shifts the length by two but cannot affect the final overflow or outside digits. Pairing the resulting normalized output, including the gamma=1 one-cell reflection alignment, inserts exactly two central copies of twice the steady digit. Six central input coefficients provide the necessary two-sided margin; odd and even centre parities work identically because x is even. The six output letters are 8->16->14->10->2->4->8. This is a one-step arithmetic identity; its randomized 19200 exact controls are in pump_check.py, not the sole justification.

Therefore if the central run stays longer than six, the parameter k can be pumped by one without changing the full finite cap at a fixed t. Direct genuine Python integer controls at k=28,29,35,80 show, for every t from 0 through 24, the exact same entire A_t independent of k, an odd coefficient in A_t, and w_t = 2k + beta_t. The smallest reference core stays well beyond the six-cell margin. The induction using the insertion identity extends the finite 24-step statement to all k>=28. This gives a genuine positive replenishment: beta4=+8, beta6=+8, beta12=+5, beta18=+2, beta24=+1.

For the long 20000-step instance, the exact deficit beta_t = w_t-44000 and cap length |A_t| = (number_of_decimal_digits_t-w_t)/2 are:

| step | decimal length | centre width | beta | cap length | overflows |
|---:|---:|---:|---:|---:|---:|
| 0 | 44046 | 44000 | 0 | 23 | 0 |
| 4 | 44048 | 44008 | +8 | 20 | 2 |
| 6 | 44048 | 44008 | +8 | 20 | 2 |
| 12 | 44051 | 44005 | +5 | 23 | 5 |
| 18 | 44054 | 44002 | +2 | 26 | 8 |
| 24 | 44057 | 44001 | +1 | 28 | 11 |
| 30 | 44059 | 43997 | -3 | 31 | 13 |
| 36 | 44062 | 43990 | -10 | 36 | 16 |
| 1000 | 44443 | 43353 | -647 | 545 | 397 |
| 5000 | 46055 | 40709 | -3291 | 2673 | 2009 |
| 10000 | 48139 | 37375 | -6625 | 5382 | 4093 |
| 15000 | 50212 | 34038 | -9962 | 8087 | 6166 |
| 20000 | 52261 | 30723 | -13277 | 10769 | 8215 |

Thus the first six-step gain comes from conversion of three cap cells to homogeneous core, assisted by two length-overflow cells. The loss returns soon afterwards. Importantly, after 24 steps A_24 is not A_0 (length 28 versus 23), even though phase x_24=x_0 and beta_24=+1. The cap mismatch, rather than failure to find a positive short-term budget, is the exact missing recurrence condition.

## Conditional emitter-cycle certificate format

An emitter state is (finite phase q, finite cap A_q, central symbol x_q, unbounded width k>=K), denoting pairword A_q ++ x_q^k ++ reverse(A_q). A claimed edge q->q' has integer offset d and demands T(P(q,k))=P(q',k+d) for all k>=K with exact overflow, valid leading digit and an odd coefficient in the surviving cap. The core insertion lemma can discharge that all-k quantifier from one finite edge when its central margin is sound.

If finitely many edges return to the identical phase, entire cap and central symbol with total width offset D>=0, every intermediate accumulated offset keeps k>=K, and every state's odd cap guard holds, then every physically realized seed with sufficiently large k has an infinite palindrome-free orbit. Proof: iterate exact edges, the nonnegative net drift preserves the budget across cycles, the prefix minimum protects substeps, and odd pair coefficients exclude palindromes. Temporary negative substeps are allowed. This exact resource-graded renewal criterion demands a *cap return*, not merely positive width change. The exhibited 24-step path fails precisely this obligation. This conditional theorem is not a base-10 certificate.

Lean proof sketch: reuse existing normalization and pair lemmas, prove norm_repeat steady-carry for the six central values, discharge both input parities and gamma=0/1 for pairs_insert_core, and prove a finite edge-cycle induction tracking minimum prefix sum. No Lean code or kernel result is asserted.

## Reproduction and independent failure controls

From repo root run:

sh calculation/new_structures/agent-W09/reproduce.sh

The script compiles replay_digits.cpp (canonical decimal digit vector, low-to-high) and replay_limbs.cpp (independent base-1000 big integer; each step converts to canonical decimal, reverses that string, parses back into limbs, and adds in radix 1000). Both replay actual integers and independently check palindrome status and the entire central-run shape at all 20001 stages. The runner compares their checkpoint output byte for byte and compares against checkpoints.txt. Final check: 20000 additions; no palindromes; no shape failure; central width 30723; overflow count 8215; low-first FNV64 c8ea7c7e51e14bd9.

pump_check.py supplies 19200 randomized exact coefficient-pump checks (six phases, two parities, eight cap sizes and 200 trials), independent Python native-integer checks for k=28,29,35,80 over 37 states, an odd-cap guard at every t<=24, and a deliberately defective alternative cap that reaches an actual palindrome at t=5. This last test is a safety regression, not an exclusion census.

These are local checks. Git shell clone and repository-wide tools/verify.py --changed were unavailable in this working container, so neither an ALL CHECKS PASSED repository-verifier claim nor Lean verification is implied.

Next positive target: construct a boundary emitter repairing A_24 back to A_0 or a later cap in a finite cap-state loop while keeping the accumulated width credit nonnegative. The initial positive gain is real; *recurrent* replenishment remains open.
