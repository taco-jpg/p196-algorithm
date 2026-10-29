# A universal one-step quotient-pumping rule for the decimal period-eight exterior

**Label: PAPER PROOF.** Scope: all arbitrary palindromic central coefficient words and all spatial band-copy counts r>=1, for the eight specific phase words already recorded in `calculation/new_structures/agent-N10/phase.json`. This is a **new local certificate format**, not a decimal Lychrel certificate. Finite arithmetic is independently COMPUTED.

## Theorem (all centres, all repetitions)
Work in base 10 with palindromic pair-coefficient words (alphabet 0..18), least-significant position first. Let `B_t` (length 39) and `W_t` (length 20) be the eight phase words in `phase.json`, indexed t modulo eight. Let `T(P)` denote the pairword of the decimal carry-normalized value `val(P)`, allowing a terminal overflow. For arbitrary finite palindromic `C` and every r>=1, put
`P(t,r,C)=B_t ++ W_t^r ++ C ++ reverse(W_t^r) ++ reverse(B_t)`.
Define `I_t(P)` to insert `W_t` just after the first 39 entries and its reverse just before the last 39 entries. Then
`T(I_t(P(t,r,C))) = I_(t+1)(T(P(t,r,C)))`.
Both sides have identical decimal overflow. This identity does not require any upper bound, periodicity, or hypothesis on the *content* of C. For a literal integer-realization of an odd-length P, the middle pair coefficient must be even. The coefficient-word identity itself applies to any palindromic C.

## Proof by block normalization and finite phase arithmetic
For block X and carry c in {0,1}, write `norm(X,c)=(digits,carry_out)`. The transition on a coefficient p is `(p+c) mod 10`, `floor((p+c)/10)`. The carry map of a coefficient block is constant when the block contains a coefficient other than 9: once encountered, the two possible carries coalesce and stay equal. Every W_t and reverse(W_t) has this property.

Finite phase table, t=0..7:
```text
t                 0 1 2 3 4 5 6 7
carry(B_t,0)      1 1 0 1 0 1 0 0
carry(W_t,0/1)    1 1 0 1 0 1 0 0
carry(rev W,0/1)  1 1 0 1 0 0 0 0
final overflow    1 0 1 0 1 0 1 0
```
Thus the low block B_t enters W_t *at its fixed-point carry*. Normalizing the r identical W copies produces the same 20-digit block U_t repeated r times. The central block C is reached at the same carry for r and r+1. Write its arbitrary normalized digit sequence as D and its outgoing carry as u in {0,1}. On the high side, the first reverse(W_t) has a digit block X_(t,u), and each later reverse(W_t) has the same steady block Y_t independent of u; the cap reverse(B_t) produces Z_t and final overflow g_t, independent of C and r. Consequently the complete normalized digit word has the **exact** factorization
`A_t ++ U_t^r ++ D ++ X_(t,u) ++ Y_t^(r-1) ++ Z_t ++ [g_t if 1]`.
Here A_t is norm(B_t,0).digits. Increasing r to r+1 inserts one U_t before D and one Y_t before Z_t, without changing A,D,X,Z, u or g.

Reversal-pairing of that factorization now gives the theorem. All terms involving the unknown D match literally at corresponding positions after the symmetric pair of length-20 insertions. All steady interior copies contribute the *same* 20-coefficient block, which the finite phase arithmetic identifies with W_(t+1). The two cap interfaces and the single exceptional high-side X_(t,u) require only finitely many equality checks, for eight phases, u=0/1, and both g=0 and g=1 cases already present in the phase table. Their coefficients match exactly when the new block is inserted after 39 and before the reflected final 39. This proves the identity for every r by inserting one additional identical steady U/Y pair, and for every D because only its unmodified symbols (not their values) are used. Empty and odd-length D are covered by the same alignment with the appropriate central crossing.

The independent formal-symbol engine `symbolic_pump.py` implements the full normalization factorization with centre digits as *independent formal variables*, rather than substituting concrete C. It verifies 288 cases: 8 phases x 3 r values (1,2,3) x both possible u x 6 formal centre lengths (0,1,2,3,7,17); all pass. The repetition/centre-length generality follows from the explicit block factorization above, not from an extrapolation of those samples. The finite checks cover the cap identities and both possible centre-output carries.

## Genuine integer controls
`random_pump_control.py` independently builds real positive decimal integers from coefficient-pair digits, performs `int(s)+int(s[::-1])`, and tests exact *whole pairword* equality. Seed=1919610; for every t=0..7 and r in {1,2,3}, 100 independent random palindromic centres (odd-length ones have even middle coefficient), totaling 2,400 cases, all pass. The earlier `pump.cpp` checks 20,000 *consecutive actual integer* iterations across four distinct centres and also passes.

Reproduce both from the repository:
```sh
sh calculation/new_structures/agent-N10/run_universal.sh
```
No external packages; deterministic phase data committed previously. New source: `symbolic_pump.py`, `random_pump_control.py`, `run_universal.sh`.

## Precise missing condition for an infinite certificate
The theorem is a **one-step equivariance**, not closure of `P(t,r,C)` under T with r>=1. The central defect may consume the last surviving W block, as observed in finite seed experiments. To turn this into an all-time certificate, one must find a finite invariant boundary/centre language L_t such that for every P in L_t, T(P) belongs to L_(t+1), the guard r never drops to zero, and at least one fixed odd pair coefficient prevents palindromes. This is the next constructive search, not an exclusion result.

Lean proof sketch: formalize `norm_append` and `norm_repeat_const_carry` for W, then prove a `pairs_insert` lemma for the displayed factorization and discharge the eight concrete phase identities by `decide +kernel`. No Lean files are committed or claimed verified. The full repository checkout was unavailable from the local shell due GitHub DNS resolution, so repository-wide `tools/verify.py --changed` was not run.
