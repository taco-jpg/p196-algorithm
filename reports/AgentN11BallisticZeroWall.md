# N11: Ballistic advection and eventual collapse of a decimal zero domain

**COMPUTED**, finite-time and literal-decimal arithmetic; no Lean or infinite decimal Lychrel proof. This follows the N_45000 seed already defined and reproduced by AgentN11CarryShadowFamily, without changing its digits.

The earlier elementary bound proves a zero pair-coefficient interval of length at least L-2t while positive. It guarantees a fixed *subinterval* only through t<=22,499 for L=45,000. It is NOT an upper bound on the domain's actual lifetime. The deeper experiment tracked the maximal zero interval containing the evolving centre of that original domain, using the precise pairword at each iteration and allowing both endpoints to drift.

## Measured wall glider

At t=1, the zero run is exactly [66,45064] in lower-half coefficient indices, width 44,999. For each subsequent transition, write (a_(t+1), b_(t+1))=(a_t+u_t,b_t-v_t). On all **74,924** sampled-as-every-step transitions through t=74,925, u_t,v_t were independently found in {0,1}. There was not a single expanding wall transition. The complete joint histogram is:

| gamma | u=0,v=0 | u=0,v=1 | u=1,v=0 | u=1,v=1 |
|---|---:|---:|---:|---:|
| 0 | 32,366 | 4,541 | 4,534 | 2,440 |
| 1 | 0 | 0 | 31,043 | 0 |

Thus the left wall advances in 38,017 of 74,924 transitions (mean 0.5074 cells/step), while the right wall retreats in 6,981 (mean 0.0932 cells/step). Domain width shrinks at mean rate about 0.6006 cells/step and drifts rightward, rather than eroding symmetrically at worst-case rate 2. In this observed itinerary, every gamma=1 step transports the left wall one cell right without eroding the right wall. This is an empirical dynamical regularity, **not** a universal theorem about all base-10 seeds or all zero walls.

The tracked run persists at least through step 74,925 (the previous endpoints are both 38,083, width 1), and at step 74,926 neither the former interval nor its 2-cell neighborhood contains a zero coefficient. The full iterate at loss has 121,305 digits. The computation checked all 74,927 iterates t=0..74,926 for palindromicity: none are palindromes. This is an explicit 74,926-step constructed finite-time orbit, not a finite certificate of survival forever.

The exact measured lower-half intervals at steps 1, 10k, 20k, 30k, 40k, 50k, 60k and 70k, along with numeric FNV digests, appear in expected_wall.json. Two distinct ordinary-integer algorithms agree on all eight checkpoint digests, on the five joint transition counts, on the band loss time and on the final digit length.

## Exact local mechanism

The general exact carry formula from AgentN11CarryShadowFamily applies. If a source pairword has a zero run [a,b], then gamma=0 guarantees the next zero run contains [a+1,b-1]; gamma=1 guarantees it contains [a+1,b]. In particular the wall cannot move inward faster than one position on each side; the conservative width bound loses at most two sites per step.

The observed moving interval is much wider because on many steps the *boundary* coefficient itself also maps to zero. The actual gate depends on coefficients and carry states immediately outside the interval, not on a fixed periodic bulk. In the tested real seed, gamma=0 permits all four 0/1 boundary outcomes, whereas gamma=1 always uses (+1,0). The separate decimal-string engine tests this exact moving-boundary description at every step, rather than assuming the rule to generate the data.

## What breaks and the next construction

Despite its long-lived, coherent glider behavior, the observed wall itinerary only has nonnegative u_t and v_t. The band has no replenishment: its 44,999 initial sites are eventually consumed by total inward wall motion. Replacing the finite centre by one huge zero region therefore does not alone solve decimal Lychrel existence.

The constructive next search is a boundary gate that **adds zero cells** (a negative u or v), potentially by a nearby neutral 9 region converting to zeros on the outside. The exact carry test permits creation of new zero cells from 9 with carry 1 or 10 with carry 0; such a regenerating interface, not a bounded stationary kink or another exclusion census, could lead to a true pumping certificate.

## Reproduction

~~~sh
bash calculation/new_structures/agent-N11/wall_reproduce.sh
~~~

This builds both independent C++17 sources, checks 74,927 ordinary decimal iterates, every moving wall transition and all stored compact controls; no external data, binary archive, or web access is used. The source files are bubble_lifetime.cpp (little-endian digit-vector arithmetic), wall_independent.cpp (MSB-first decimal-string addition), and expected_wall.json.
