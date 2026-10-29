# Constructive decimal quotient guard transport with a 136-state erosion cycle

**Label: PAPER PROOF**, finite base-10 local identities independently audited COMPUTED. This is a sharpening of `AgentN10ArbitraryFiniteDecimalShell`, not an exclusion of any centre.

## Arbitrary spatial-cut lemma
The prior result only guaranteed that r complete W periods shrink to r-1 after each step. We now permit a *partial* final period. Fix phase t in {0,...,7}, any r>=1 and residue j in {0,...,19}, and put `A=B_t ++ W_t^r ++ W_t[:j]`, with length `h=39+20r+j`. Let `P=A ++ C ++ reverse(A)` for any palindromic central coefficient word C. Define `d=2` if `A[-1]=9`, otherwise `d=1`. Then the actual one-step coefficient pairword T(P) agrees exactly with `B_(t+1) ++ W_(t+1)^infinity` through its first **h-d coefficients**; its decimal overflow equals `(10101010)[t]`. Thus the exterior cut can advance inward by no more than two coefficient positions per step. Both source and target high sides are reflected by palindromicity.

## Proof
For any base-10 coefficient p in 0..18, the carry maps from c=0 and c=1 coalesce immediately if and only if p!=9. In all eight explicit W_t rows, no pair of 9s is adjacent, even cyclically. The cap B_t and at least one full W_t fix the low carry entering C and absorb the outgoing high carry before it reaches reverse B_t, so the overflow and the 39-column next cap are independent of C.

Normalize low and high periodic segments separately, with the central normalized digit sequence D represented by arbitrary independent symbols and its outgoing carry u universally in {0,1}. All 20 interior residues use the known period-20 digit blocks. When A[-1]!=9, the high-side carry is erased at the first shared coefficient after C, so the first h-1 output paired coefficients are independent of D and u. If A[-1]=9, the preceding coefficient is not 9, erasing the carry one position later and leaving the first h-2 pairs fixed. The exact fixed values on that prefix are the next phase's known B/W bulk, as can be checked in the finite eight-phase, twenty-residue carry table. This proves the displayed one-step rule for every r and C; increasing r merely repeats already absorbed steady blocks.

The standalone exact finite-symbol checker `partial_guard.py` verifies 8 temporal phases x 3 band counts x 20 cut residues x 2 outgoing central carries x 5 mutually independent symbolic centre lengths = **4,800** checks, all PASS. A different checker `partial_bigint_control.py` constructs real decimal integers with random centres of either parity and computes `int(s)+int(s[::-1])`, verifying **3,840** one-step cases. The general r and C quantifiers follow from the block-factorization argument, not from extrapolating samples.

## Deterministic guard automaton and exact 136/140 calculation
If the current proven prefix length is h and h>=39+20, its final periodic index is `j=(h-40) mod 20`. Evolve finite state `(t mod 8,j)` via
`d=2 if W_t[j]==9 else 1`,
`(t,j) -> ((t+1) mod 8,(j-d) mod 20)`.
Start at `(0,19)`, corresponding to any complete-band seed with h0=39+20k. The directed functional orbit has exactly 136 states before returning to (0,19). Along this period there are 132 unit losses and four double losses, total **140** lost coefficient positions. This is an exact finite 160-state arithmetic calculation, reproducible with `guard_cycle.py`.

Let `a_i` be the listed loss values in one 136-step cycle, and define
`D(H)=140 floor(H/136) + sum_(i=0)^(H mod 136 - 1) a_i`.
For any horizon H, choose `k=1+ceil(D(H)/20)`. Then the initial h0=39+20k maintains h_t>=39+20 for every t<=H. Since the first 39 coefficients at every phase have an odd entry, no iterate is a palindrome through H. Every output length increases according to the overflow stream 10101010, so `n_t=78+40k+ceil(t/2)` for empty central core.

At H=20,000, `20,000=147*136+8`, the first eight losses total eight, so `D(20,000)=147*140+8=20,588`. A conservative rigorously certified choice is **k=1,031** and initial integer length **41,318 digits**. The proven final prefix is at least `39+20*1031-20588=71` coefficients. This bound is conservative: an independent ordinary-decimal digit-list replay of k=1,031 passes all 20,000 additions without palindrome, finishes with 51,318 digits, and still matches at least 803 complete lattice periods.

## Reproduction
```sh
sh calculation/new_structures/agent-N10/run_guard.sh
```
Regenerates phase data, executes the 4,800 symbolic and 3,840 genuine-integer checks, computes the exact 136-cycle loss, then independently replays the 41,318-digit seed for 20,000 steps in C++.

This proves arbitrarily long finite decimal palindrome-free trajectories with a quantitative shell bound. It does not prove a fixed infinite decimal Lychrel orbit, because the guaranteed shell still erodes. Lean proof sketch: formalize `norm_append`, the carry-coalescence criterion p!=9, periodic 20-column pair-normalization, and the 160-state phase/residue transition; discharge the eight-by-twenty finite identities with `decide +kernel`. No Lean files were added. Shell GitHub DNS prevented a checkout and `tools/verify.py --changed`.
