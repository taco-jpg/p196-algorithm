# W04: a rectangular, independently pumped 20,000-step decimal orbit family

**PAPER PROOF** for the conditional finite-state pumping implication and the six-edge universal all-width identities. **COMPUTED** for the finite witness and two independent 20,000-step ordinary-number replays. **UNDECIDED** beyond this horizon. Not a decimal Lychrel number, not a Lean theorem.

## The new construction relative to N19

N19 established a one-parameter diagonal ray `H0(k,k)` and a 20,000-step family obtained by increasing the two bulk lengths *together*. This result adds a genuine two-parameter rectangle: let `m,n >= 15000` be **independent**. Its initial even symmetric pairword has LSD-first folded half

    H0(m,n) = [10] ++ [8]^m ++ [5,11] ++ [16]^n ++ [8].

Create an ordinary decimal seed by splitting each folded coefficient `x` into a high digit `min(9,x)` and a low digit `x-min(9,x)`, reflecting these across the middle. The high leading digit is 9, so the seed is canonical and physical. This extends N19's synchronized ray to a full `N^2` counter region and lets a proposed PDR/IC3 frame constrain each resource separately. No infinite-time assertion follows.

## Finite universal six-edge checker, without synchronized lengths

`witness.json` gives the seven explicit phase tuples `(L,x,a,J,y,b,R)` of the *previously known* N19 six-phase decimal mechanism, parity flags `(0,1,1,1,1,0,0)` and overflow flags `(1,0,0,0,1,0)`. Put `H_t(M,N)=L_t ++ x_t^M ++ J_t ++ y_t^N ++ R_t` with `M,N>=3`. For all `M,N>=3` the **exact** reverse/add pairword edge is

    H_t(M,N) -> H_(t+1)(M+dm_t,N+dn_t),
    (dm_t,dn_t) = (-1,-1),(-1,-1),(-1,0),(-1,0),(-1,0),(0,0).

The fold parity is the phase-dependent flag above; `->` denotes complete palindromic-pairword normalization with its exact decimal overflow. The starting phase-0 parameters `m>=8,n>=5` keep the source runs >=3 through all six edges. The resulting phase-6 independent counters are exactly `(m-5,n-2)`. This is a six-step **transient** transport, not a return edge (the literal `L,J,R` blocks have changed).

Here is the *finite soundness checker*. A two-ended carry state before an outer folded column is `(a,z,h)`, where `a` is the lower incoming carry, `z` the high outgoing carry and `h` the preceding high normalized digit. Given input `p`, guess high incoming carry `r∈{0,1}` and require `z=floor((p+r)/10)`. Then `a'=floor((p+a)/10)`, `z'=r`, `h'=(p+r)%10`, and output coefficient is `(p+a)%10 + h'` for overflow 0, or `(p+a)%10 + (1 on the first column, otherwise h)` for overflow 1. The odd/even terminal checks the unique meeting carries and the central coefficient. These are exact schoolbook identities, with no independence assumption on the centre.

For each edge, the Python checker verifies an accepted finite source/target pair at `M=N=3` and finds two **distinct** paired-column positions lying inside the respective input AND output repeated runs where the complete carry state is unchanged. The positions, states and input/output symbols are embedded in `witness.json`; the script independently reconstructs and compares the object, and rejects a corrupted carry state. Inserting `q>=0` copies of the first self-loop and `r>=0` copies of the second self-loop preserves the entire accepting transducer path *independently*. Since each copy is strictly within the appropriate source and target constant run, the resulting words are precisely the claimed `(M+q,N+r)` templates. Soundness and uniqueness of decimal normalization yield the theorem **for all** run lengths, not by numerical extrapolation. Additional 99 ordinary-Python-bigint seed controls check actual digit arithmetic.

## Rectangle theorem through 20,000 steps

For the **single** reference seed `m=n=15000`, `independent_20k.cpp` executes genuine ordinary decimal digit-vector `N+reverse(N)` with low-to-high carry through every digit for **20,000 full steps**. At each `0<=t<20000`, it reconstructs the *complete* folded pairword of both source and target, finds ordered runs with bulk symbols `(8,16,14,10,2,4)[t%6]` and `(16,14,10,2,4,8)[t%6]`, and checks that the two longest appropriate bulk runs overlap between source and target in disjoint intervals. Inside **each** overlap the program reconstructs all three components of the actual two-ended carry state from its literal addition carry array and high output digits; it requires a genuine one-letter carry-state self-loop in each interval. Every verified carry self-loop is an exact local transducer equation, and the two chosen intervals are disjoint. Thus each complete reference edge admits **independent** insertion of *any* two nonnegative counts `q,r` of paired bulk symbols. Inducting on `t=0..20000` proves that the complete pairword at time t for arbitrary seed `(15000+q,15000+r)` is obtained from the reference halfword at t by extending the same two runs by `q,r`, without changing its finite exterior or centre.

At every reference state, the checker verifies at least one odd pair coefficient (observed minimum **two**). Every bulk symbol being inserted is **even**, so these witnesses remain at precisely their unaffected positions in the pumped pairword. A palindrome would have all pair coefficients even. Therefore **every seed in the independent rectangular family is nonpalindromic through t=20000**. The two bulk intervals always remain ordered and disjoint. Minimum source/target overlap widths of the reference across all edges are `1820,1786`; the minimum odd count across all 20,001 states is 2. The checker deliberately fails closed when any state, overlap, carry or safety guard does not match.

This is a finite-horizon proof object checked by code, not a Lean kernel proof. In IC3 terminology it is a bounded chain of 20,001 symbolic frames, each a two-counter cylinder with a fixed finite interface and two independently pumpable transitions. The resource update is *negative*, hence **there is no infinite inductive frame**. The next distinctive objective is a centre/glider transition that adds at least five first-band cells and two second-band cells per complete six-step cycle, or an alternate phase return with a nonnegative counter vector, without losing the exact carry interface.

## Independent physical replay and control output

Two **distinct** transition implementations evaluate the *off-diagonal* seed `(m,n)=(15000,16000)` at every one of the 20,001 states. `independent_20k.cpp` performs schoolbook digit-vector addition; `independent_gmp.cpp` constructs `mpz_class` integers and computes `N += mpz_class(reverse(decimal_string(N)))` at each step, independently extracting the folded coefficients from the decimal string. Both require a nonpalindrome and ordered paired-clock runs of length >=100 at **every** step. The two implementations agree at all five checkpoints on the complete-number FNV-1a digest, trajectory metadata digest, length and two run lengths:

| t | digits | first run | second run | full-number FNV-1a |
|---:|---:|---:|---:|---|
| 0 | 62008 | 15000 | 16000 | `a68ded9be4dce159` |
| 5000 | 64083 | 11656 | 12701 | `74c3a64cfc9ee20` |
| 10000 | 66171 | 8342 | 9397 | `e0b95978a86c23cd` |
| 15000 | 68210 | 5068 | 6097 | `4be963ab548b47d4` |
| 20000 | 70241 | 1820 | 2786 | `67dc3790ddabed81` |

The full five-checkpoint **trace metadata** digest at step 20000 is `1d9bfad14d64185c`. The digest includes *all* 20,001 state lengths and selected run lengths; it is equal in the two arithmetic implementations. A deliberate wrong hash is rejected by the comparator. An intentionally impossible run threshold of `16001` is rejected by the digit verifier. Ordinary big-integer controls of the six symbolic edges cover 99 distinct pairs of input run lengths plus the short diagonal controls `(5,5),(6,6),(7,7)`.

### Exact reproduction

From repository root:

    bash calculation/new_structures/agent-W04/run.sh

Requirements: Python 3, `g++ -std=c++17`, and GMP development headers/libraries (`-lgmpxx -lgmp`). The full GMP replay is substantially slower than the digit-vector engine; do not interpret an interrupted GMP run as a check passing. The script runs all three modes and ends in `AGENT_W04_ALL_CHECKS_PASSED`. Every source file and the compact finite six-edge certificate are in `calculation/new_structures/agent-W04/`. No release zip, old source mutation, generated binaries or large trace bundles are needed.

## Honest limits

The family says **nothing** about the 20,001st or later transition. Two finite source counters are eroding, so this result does not furnish a decimal Lychrel number or infinite inductive IC3 invariant. It builds directly on N19's existing six-phase mechanism, while establishing independent (`q,r`) pumping and proving/replaying a genuinely off-diagonal 20,000-step family. No Lean theorem or repo-wide `verify.py --changed` invocation was possible in this tool environment because shell `git clone` cannot resolve `github.com`; no such verification is claimed. Non-Lean source and result only.