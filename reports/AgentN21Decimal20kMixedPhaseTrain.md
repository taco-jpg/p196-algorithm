# A 20,000-step decimal mixed-phase two-kink train

## Explicit finite-time construction and scope

**COMPUTED:** exactly 20,001 nonpalindromic states for each of four ordinary base-10 integer orbits, from t=0 through t=20,000 inclusive. This is a constructive finite-horizon result, **not** an infinite decimal Lychrel number, not a proof about 196, and not an infinite finite-state certificate. The novelty relative to the earlier 820-step four-packet construction is the large-horizon exact additive packet separation (20,000 iterations) with two *different spatial phases* modulo 9 and a complete independent GMP ordinary-integer replay for every state.

Let coefficient words be least-significant-first. Construct the 70,000-long palindromic coefficient word P0: use the first 34 coefficients

    B2 = (2,11,1,6,8,1,7,15,9,3,9,4,7,9,10,16,9,11,4,10,8,8,9,11,11,7,4,3,9,12,1,1,9,11)

followed up to index 34,999 by the 9-periodic lattice word

    W2 = (1,10,8,5,9,16,0,9,11)

then reflect. This is the p12/m9 base-10 phase-2 lattice from `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt` and is self-contained in `longtrain.cpp`. Define packet

    K = (6,1,0,1,11,14,10,6,11,16,1).

Create four words P0, PL, PR, PLR by inserting K and its mirrored copy at no site, at site 8,000 only, at site 22,000 only, or both. Anchor residues modulo 9 are 8 and 4, respectively, so the packet responses are not simple translations. For each pair coefficient x at positions i and n-1-i, realize a canonical ordinary decimal integer by splitting x into low digit lo=min(9,x), high digit hi=x-lo, except at i=0 choose both lo and hi positive. Both low and high extreme digits are nonzero and all digits lie in 0..9. The actual deterministic split is in `realize()` in `longtrain.cpp`; thus the initial seeds are unambiguously specified without embedding four 70,000-digit literals.

## Shape checked at every step

For t=0..20000 let P0(t), PL(t), PR(t), PLR(t) be the **exact actual pairwords** of the four reverse-and-add integer orbits. The checker confirms all four have the same canonical length

    n(t) = 70000 + 3*floor(t/12) + prefix[t mod 12],
    prefix = (0,0,0,1,1,1,1,2,2,2,2,3).

Let deltaL(t)=PL(t)-P0(t), deltaR(t)=PR(t)-P0(t) componentwise. The full pairwords are symmetric and satisfy for **every** t:

    PLR(t) = P0(t) + deltaL(t) + deltaR(t).

Each delta has a well-defined lower-half support interval. The two intervals remain disjoint; the left interval starts beyond index 34, and the right interval ends before midpoint minus 34. Their reflected high-half intervals are also disjoint. At the final t=20,000, n=75,000, the left support is [4249,16693] with 11,672 nonzero lower-half cells, and the right support is [18251,30694] with 11,652 nonzero cells. There are 1,557 unmodified lower-half coefficients strictly between the supports. The minimum inter-packet gap **over the whole run** is not claimed from snapshots; the checker asserts disjointness at all steps.

## Independent decimal integer arithmetic, controls and limitations

`longtrain.cpp` uses two deliberately separate arithmetic paths:

1. `step(Word)` does base-10, least-to-most-significant carry normalization of the symmetric coefficient word and reflects normalized digits to form the next pairword. This path contains **no** ordinary large integer conversion.
2. `realize`, `bigint_step`, `canonical` and `pairword` use GNU GMP `mpz_class`  arbitrary-precision integers, convert exact decimal digit strings, perform `N + int(reverse(decimal(N)))`, and independently reconstruct all coefficients from the resulting canonical decimal representation. All four integer orbits are checked at all 20,001 times for exact full pairword equality and nonpalindromicity.

The two algorithms agree on every digit of every pairword, not only checkpoints or a rolling hash. There is no random sampling or state cap. A separate 100-transition Python built-in-int control checks the same four-seed construction at 10,000-digit scale; a deliberately corrupted initial GMP integer is rejected at t=0 by the normal comparison. The strengthened pairword-only 20,000-step run independently checks the exact growth schedule, isolation from exterior and midpoint, support disjointness and additivity. The complete GMP run checks additivity and ordinary integer arithmetic at all 20,001 states. The compact per-1,000-step trace is retained in `trace_longtrain.txt` and checked by `diff`.

Run from the repository root:

    sh calculation/new_structures/agent-N21/run_longtrain.sh --quick
    sh calculation/new_structures/agent-N21/run_longtrain.sh

Dependencies: C++17 compiler, GNU GMP headers and `libgmpxx/libgmp`, Python 3. For direct fast isolation replay (without GMP): compile the same file, then run `longtrain 70000 20000 8000 22000 0`. The full GMP replay is `longtrain 70000 20000 8000 22000 1`. The runner includes all code and input constants needed to reproduce from this repository alone. Tested with g++14 and GMP in the working container. `tools/verify.py --changed` could not be run because the full repository checkout was not available through the local Git network. No Lean source is added.

The new evidence is much stronger finite longevity of an exact two-kink transduction than the old 820-step run, but does not establish a repeating finite-state rule or an infinite orbit. The growing packet interiors were checked and do not resemble a 9-periodic lattice; future work should seek scattering output that resets to bounded symbols instead of merely postponing collision with large initial gaps.
